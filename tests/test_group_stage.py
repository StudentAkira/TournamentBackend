import json

import httpx
from httpx import Cookies
from sqlalchemy import func, and_

from .config import *

client = TestClient(app)

class MacrosHandler:
    def __init__(self, client_: httpx.Client):
        self.client = client_
        self.event_data = {"name": "string", "date": "2024-06-25"}
        self.user_data = {"email": "test@mail.ru", "password": "7689462"}
        self.nomination_data = {"name": "string", "type": "olympic"}

        self.participant_id = 0
        self.__participant_count = 12
        self.__group_count = 4

    def __get_participant_data(self, participant_id):
        return {
            "email": f"participant{participant_id}@mail.ru",
            "first_name": f"participant{participant_id}",
            "second_name": f"participant{participant_id}",
            "third_name": f"participant{participant_id}",
            "region": f"participant{participant_id}",
            "birth_date": "2024-06-26",
            "educational_institution": f"participant{participant_id}",
            "additional_educational_institution": f"participant{participant_id}",
            "supervisor_first_name": f"participant{participant_id}",
            "supervisor_second_name": f"participant{participant_id}",
            "supervisor_third_name": f"participant{participant_id}",
        }

    def __get_append_team_participant_data(self, i):
        return {
            "nomination_event": {
                "event_id": 1,
                "nomination_id": 1,
                "type": "olympic"
            },
            "team_id": i,
            "team_participants": [
                {
                    "participant_id": i,
                    "softwares": [
                        {
                            "name": "string"
                        }
                    ],
                    "equipments": [
                        {
                            "name": "string"
                        }
                    ]
                }
            ]
        }

    def __get_id_by_name(self, event_name):
        response = self.client.get(url='http://127.0.0.1:8000/api/event/event?offset=0&limit=10', cookies=self.cookie)
        events = [json.loads(item) for item in response.text.strip('][').split(', ')]
        event = list(filter(lambda x: x["name"] == self.event_data["name"], events))[0]
        return event["id"]

    def create_admin(self):
        print('create admin :: ')
        response = self.client.get(url='http://127.0.0.1:8000/api/user/create_admin')
        print(response.text)

    def login(self):
        print('login :: ', end='')
        response = self.client.post(url='http://127.0.0.1:8000/api/auth/login', json=self.user_data)
        token = response.cookies.get('token')
        cookie = Cookies()
        cookie.set(name="token", value=token, domain='127.0.0.1', path='/')
        self.cookie = cookie
        print(response.text)

    def create_event(self):
        print('create event :: ', end='')
        response = self.client.post(url='http://127.0.0.1:8000/api/event/event', json=self.event_data, cookies=self.cookie)
        print(response.text)

    def append_nomination(self):
        print('append nomination :: ', end='')
        event_id = self.__get_id_by_name(self.event_data["name"])
        response = self.client.post(
            url='http://127.0.0.1:8000/api/nomination_event/append_nomination_for_event',
            json={
                "event_id": event_id,
                "nomination_name": self.nomination_data["name"],
                "type": self.nomination_data["type"]
            },
            cookies=self.cookie
        )
        print(response.text)

    def create_participants(self, db: Session):
        print('create participants :: ')
        last_id = db.query(func.max(Participant.id)).scalar()
        self.participant_id = last_id if last_id else 0 + 1
        for i in range(self.participant_id, self.participant_id + self.__participant_count):
            response = client.post(
                url='http://127.0.0.1:8000/api/participant/participant',
                json=self.__get_participant_data(i)
            )
            print(i, response.text)

    def append_team_participants_to_nomination_event(self):
        print('team participant append to event nomination :: ')
        for i in range(self.participant_id, self.participant_id + self.__participant_count):
            response = client.post(
                url='http://127.0.0.1:8000/api/team_participant_nomination_event/team_participant',
                json=self.__get_append_team_participant_data(i)
            )
            print(response.text)

    def start_group_stage(self):
        print('start group stage :: ')
        response = client.post(
            url='http://127.0.0.1:8000/api/tournaments/start_group_stage',
            json={
              "nomination_event": {
                "event_id": 1,
                "nomination_id": 1
              },
              "group_count": self.__group_count
            }
        )
        print(response.text)

def test_group_stage():
    macros_handler = MacrosHandler(client)
    macros_handler.create_admin()
    macros_handler.login()
    macros_handler.create_event()
    macros_handler.append_nomination()
    macros_handler.create_participants(db)
    macros_handler.append_team_participants_to_nomination_event()
    macros_handler.start_group_stage()
    assert 200 != 200
