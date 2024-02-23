from db.schemas import Participant, Event, Nomination, Team


class ParticipationsService:

    def __init__(self, db):
        self.__db = db

    def get_my_events(self, token: str):
        pass

    def get_nominations(self, start, limit):
        pass

    def create_event(self, token: str, event: Event, nominations: list[Nomination] | None = None):
        pass

    def create_nominations(self, token: str, nominations: list[Nomination]):
        pass

    def specify_nominations_for_event(self, token: str, event: Event, nominations: list[Nomination]):
        pass

    def create_team(self, token: str, team: Team):
        pass

    def create_participant(self, token: str, participant: Participant, teams: list[Team] | None = None):
        pass

    def specify_teams_for_participant(self, token: str, teams: list[Team], participant: Participant):
        pass
