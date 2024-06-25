import json
from http.cookiejar import Cookie

import httpx
from httpx import Cookies


class MacrosHandler:
    def __init__(self, client):
        self.client = client
        self.event_data = {"name": "string", "date": "2024-06-25"}
        self.user_data = {"email": "test@mail.ru", "password": "7689462"}
        self.nomination_data = {"name": "string", "type": "olympyc"}

    def __get_id_by_name(self, event_name):
        response = self.client.get(url='http://127.0.0.1:8000/api/event/event?offset=0&limit=10', cookies=self.cookie)
        events = [json.loads(item) for item in response.text.strip('][').split(', ')]
        event = list(filter(lambda x:x["name"] == self.event_data["name"], events))[0]
        return event["id"]

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
        print('appen nomination :: ', end='')
        event_id = self.__get_id_by_name(self.event_data["name"])
        print({
                "event_id": event_id,
                "nomination_name": self.nomination_data["name"],
                "type": self.nomination_data["type"]
            })
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



if __name__ == "__main__":
    with httpx.Client() as client:
        macros_handler = MacrosHandler(client)

        macros_handler.login()
        macros_handler.create_event()
        macros_handler.append_nomination()
