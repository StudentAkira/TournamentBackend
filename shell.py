from typing import cast
from db.database import *
from sqlalchemy import and_
from db.models.event import Event
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from itertools import combinations


from db.models.user import User
from db.models.group import Group
from db.models.bracket import Bracket
from db.models.nominatuin_event_judge import NominationEventJudge
from db.models.team_participant_nomination_event import TeamParticipantNominationEvent
from db.models.team_participant import TeamParticipant
from db.models.token import Token
from db.models.team import Team
from db.models.participant import Participant
from db.models.group import Group
from db.models.group_team import GroupTeam
from db.models.bracket_team import BracketTeam
from db.models.match import Match
from db.schemas.group_tournament import GetGroupsOfTournamentSchema, GroupSchema
from db.schemas.participant import ParticipantSchema
from db.schemas.team_participant import TeamParticipantsSchema

db = SessionLocal()


def counting_sort(arr):
    max_val = max(arr)
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    sorted_arr = []
    for i in range(len(count)):
        sorted_arr.extend([i] * count[i])
    return sorted_arr


nomination_name = "string"
event_name = "string"
nomination_event_type = "olympyc"
group_count = 2


event_db = db.query(Event).filter(
cast("ColumnElement[bool]", Event.name == event_name)).first()
nomination_db = db.query(Nomination).filter(
cast("ColumnElement[bool]", Nomination.name == nomination_name)).first()
nomination_event_db = db.query(NominationEvent).filter(
and_(
    NominationEvent.event_id == event_db.id,
    NominationEvent.nomination_id == nomination_db.id,
    NominationEvent.type == nomination_event_type
)
).first()


# for group in nomination_event_db.groups:
#     print(group.id)
#     for match in group.matches:
#         print(f"\t{match.match_queue_number} {match.team1.id if match.team1 else None} {match.team2.id if match.team2 else None}")


for group in nomination_event_db.groups:
    for team in group.teams:
        db.query(GroupTeam).filter(and_(
            GroupTeam.tournament_group_id == group.id,
            GroupTeam.team_id == team.id
        )).delete()
    for match in group.matches:
        db.query(Match).filter(Match.id == match.id).delete()
    db.query(Group).filter(Group.id == group.id).delete()
db.refresh(nomination_event_db)
nomination_event_db.tournament_started = False
print(nomination_event_db.groups)
db.commit()

#
# nomination_event_db.tournament_started = True
#
# team_ids = set(team_participant_db.team_id for team_participant_db in nomination_event_db.team_participants)
# teams_db = db.query(Team).filter(Team.id.in_(team_ids)).all()
# groups = [Group() for i in range(group_count)]
# index = 0
# while teams_db:
#     groups[index % group_count].teams.append(teams_db.pop(0))
#     index += 1
#
# for group in groups:
#     pairs = list(combinations(set(group.teams), 2))
#     print([team_db.id for team_db in group.teams])
#     for pair in pairs:
#         print(pair[0].id, pair[1].id)
#     print('---')
#
# nomination_event_db.groups.extend(groups)
