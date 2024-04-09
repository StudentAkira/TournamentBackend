from sqlalchemy.orm import Session

from db.models.participant import Participant
from db.models.team import Team


def get_emails_of_teams_participants_db(teams: list[type(Team)]) -> list[str]:
    participants_emails = []
    for team_db in teams:
        for participant in team_db.participants:
            participants_emails.append(participant.email)
    return participants_emails


def append_participant_to_team_db(db: Session, participant_db: type(Participant), team_db: type(Team)):
    participant_db.teams.append(team_db)
    db.add(participant_db)
    db.commit()


def delete_participant_from_team_db(db: Session, participant_db: type(Participant), team_db: type(Team)):
    participant_db.teams.remove(team_db)
    db.add(participant_db)
    db.commit()
