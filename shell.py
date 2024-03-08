import time

from sqlalchemy import and_

from db.crud.nomination_event import get_nomination_event_db
from db.database import *
from db import models
from db.schemas.nomination_event import NominationEventSchema
from db.schemas.team import TeamParticipantsSchema


db = SessionLocal()


events_db = db.query(models.Event).all()
nomination_event_full_info_list = []
for event_db in events_db:
    for nomination_db in event_db.nominations:
        nomination_event_db = db.query(models.NominationEvent).\
            filter(and_(models.NominationEvent.nomination_id == nomination_db.id, models.NominationEvent.event_id == event_db.id)).first()

        team_ids = set(team_participant.team_id for team_participant in nomination_event_db.team_participants)
        participant_ids = [team_participant.participant_id for team_participant in nomination_event_db.team_participants]

        team_id_data = db.query(models.Team.id, models.Team).filter(models.Team.id.in_(team_ids)).all()
        participant_id_data = db.query(models.Participant.id, models.Participant).filter(
            models.Participant.id.in_(participant_ids)).all()

        team_id_names_dict = {key: value for key, value in team_id_data}
        participant_id_email_dict = {key: value for key, value in participant_id_data}

        teams = []

        for team_id in team_ids:
            team = team_id_names_dict[team_id]
            teams.append(team)

        print(event_db.name)
        print("\t", nomination_db.name)

        nomination_event_full_info = NominationEventSchema(
            event_name=event_db.name,
            nomination_name=nomination_db.name,
            teams=[
                TeamParticipantsSchema.from_orm(
                    team
                ) for team in teams
            ]
        )

    nomination_event_full_info_list.append(nomination_event_full_info)


# nomination_events_db = db.query(models.NominationEvent).all()
# nomination_event = {}
# for nomination_event_db in nomination_events_db:
#
#     team_ids = [team_participant.team_id for team_participant in nomination_event_db.team_participants]
#     participant_ids = [team_participant.participant_id for team_participant in nomination_event_db.team_participants]
#
#     team_id_names = db.query(models.Team.id, models.Team.name).filter(models.Team.id.in_(team_ids)).all()
#     participant_id_emails = db.query(models.Participant.id, models.Participant.email).filter(
#         models.Participant.id.in_(participant_ids)).all()
#
#     team_id_names_dict = {key: value for key, value in team_id_names}
#     participant_id_email_dict = {key: value for key, value in  participant_id_emails}
#
#     team = {}
#
#     for team_id in team_ids:
#         key = team_id_names_dict[team_id]
#         team[key] = team.get(key, []) + [
#             participant_id_email_dict[team_participant.participant_id] for team_participant in nomination_event_db.team_participants
#             if team_participant.team_id == team_id]
#
#     print(team)