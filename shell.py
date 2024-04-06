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
from db.schemas.nomination_event import NominationEventSchema
from db.schemas.participant import ParticipantSchema
from db.schemas.team_participant import TeamParticipantsSchema

db = SessionLocal()


# def quick_sort(arr):
#     if len(arr) <= 1:
#         return arr
#     pivot = arr[len(arr) // 2]
#
#     left = [x for x in arr if x < pivot]
#     middle = [x for x in arr if x == pivot]
#     right = [x for x in arr if x > pivot]
#
#     return quick_sort(left) + middle + quick_sort(right)
#
#
# def distribute_playoff_bracket(players):
#     bracket = {}  # Initialize an empty playoff bracket
#
#     # Define the quarterfinal matchups
#     quarterfinals = [
#         (players[i], players[-i - 1]) for i in range(len(players) // 2)
#     ]
#
#     # Populate the bracket with the quarterfinal matchups
#     bracket['Quarterfinals'] = quarterfinals
#
#     # Define and populate the subsequent rounds based on the winners
#     num_rounds = len(bin(len(players) // 2)) - 2  # Determine number of rounds based on players
#     for i in range(num_rounds):
#         round_name = f"Round {i + 1}"
#         if round_name not in bracket:
#             bracket[round_name] = []
#         winners = []
#         for matchup in bracket[f'Round {i}'] if i > 0 else bracket['Quarterfinals']:
#             winner = max(matchup, key=lambda x: x[1])
#             winners.append(winner)
#         bracket[round_name] = [(winners[j], winners[-j - 1]) for j in range(len(winners) // 2)]
#
#     return bracket
#
#
# # List of players sorted by decreasing score (for demonstration, you can generate it programmatically)
# players = [(i, 5 - i) for i in range(1, 6)]
# print(players)
#
# # Distribute players in the playoff bracket
# playoff_bracket = distribute_playoff_bracket(players)
#
# # Print the playoff bracket
# for round_name, matchups in playoff_bracket.items():
#     print(round_name)
#     for matchup in matchups:
#         print(f"{matchup[0]} vs. {matchup[1]}")
#     print()

owner = db.query(User).filter(User.id == 1).first()
event_db = Event(name="string", owner=owner)
nomination_db = Nomination(name="string")
event_db.nominations.append(nomination_db)

db.add(nomination_db)
db.add(event_db)
db.commit()

nomination_event_db = db.query(NominationEvent).filter(
    and_(
        NominationEvent.event_id == event_db.id,
        NominationEvent.nomination_id == nomination_db.id
    )
).first()

for i in range(6):
    participant_db = Participant(
        email=f"user{i+1}@example.com",
        first_name=f"user{i+1}",
        second_name=f"user{i+1}",
        third_name=f"user{i+1}",
        region=f"user{i+1}",
        birth_date="2003-05-19",
        educational_institution="user{i+1}",
        additional_educational_institution="user{i+1}",
        supervisor_first_name="user{i+1}",
        supervisor_second_name="user{i+1}",
        supervisor_third_name="user{i+1}",
        hidden=False,

        creator=owner
    )
    team_db = Team(name=f"default_team_{participant_db.email}", creator=owner)
    participant_db.teams.append(team_db)
    db.add(participant_db)
db.commit()

for i in range(6):

    participant_db = db.query(Participant).filter(Participant.email == f"user{i+1}@example.com").first()
    team_db = db.query(Team).filter(Team.name == f"default_team_user{i+1}@example.com").first()

    team_participant_db = db.query(TeamParticipant).filter(and_(
        TeamParticipant.participant_id == participant_db.id,
        TeamParticipant.team_id == team_db.id
    )).first()
    nomination_event_db.team_participants.append(team_participant_db)

db.add(nomination_event_db)
db.commit()