import os

from fastapi import HTTPException
from fpdf import FPDF, fpdf
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from db.crud.general import get_person_age
from db.crud.nomination_event.nomination_event import get_nomination_event_pdf_data_db, \
    get_nominations_event_participant_count_db, get_nomination_events_all_names_db, \
    get_nomination_events_all_names_by_owner_db, get_nomination_events_full_info_db, \
    get_nomination_events_full_info_by_owner_db, append_event_nomination_db, \
    delete_nomination_event_db, close_registration_nomination_event_db, open_registration_nomination_event_db, \
    get_nomination_event_db, get_judge_command_ids_db
from db.crud.participant_nomination_event.participant_nomination_event import get_participants_of_nomination_event_db
from db.models.event import Event
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from db.models.participant import Participant
from db.models.user import User
from db.schemas.nomination_event.nomination_event import NominationEventSchema
from db.schemas.nomination_event.nomination_event_participant_count import NominationEventParticipantCountSchema
from db.schemas.nomination_event.nomination_event_type import NominationEventType
from managers.event import EventManager
from managers.nomination import NominationManager
from managers.team import TeamManager


class NominationEventManager:
    __db: Session

    def __init__(self, db: Session):

        self.__db = db

        self.__team_manager = TeamManager(db)
        self.__nomination_manager = NominationManager(db)
        self.__event_manager = EventManager(db)

        self.__nomination_event_does_not_exist_error = "nomination event does not exist"
        self.__nomination_event_already_exist_error = "nomination event already exist"
        self.__tournament_already_started_error = "tournament already started"
        self.__tournament_started_error = "tournament started"
        self.__tournament_not_started_error = "tournament not started"
        self.__wrong_nomination_event_type_error = "wrong nomination event type"
        self.__participant_not_in_nomination_event = "participant not in nomination event"
        self.__registration_finished_error = "registration finished"
        self.__participant_already_in_nomination_event = "participant already in nomination event"
        self.__user_not_in_judge_command_error = "user not in judge command"

    def get_nomination_event_pdf(self, data: list[type(Event), type(Nomination), type(NominationEvent)]):

        pdf_data = get_nomination_event_pdf_data_db(self.__db, data)

        pdf = FPDF(orientation='L')
        pdf.add_page()
        pdf.add_font('fontF', 'B', os.path.join(".", 'Roman.ttf'))
        pdf.set_font('fontF', 'B', 12)
        pdf.write(text='''
                                                                                                                        
                                ЗАЯВКА ______________________________________________________области
                                на участие в открытом республиканском IT-чемпионате «РобИн-2024». 
        \n''')

        with pdf.table() as table:
            table._first_row_as_headings = False
            table._num_heading_rows = 0
            row = table.row()
            row.cell("№\nп/п", align=fpdf.Align.C)
            text = "Фамилия Имя Отчество участника"
            row.cell(text, align=fpdf.Align.C)
            row.cell("Область", align=fpdf.Align.C)
            row.cell("Число, месяц, год рождения, количество полных лет на начало проведения мероприятия", align=fpdf.Align.C)
            row.cell("Компетенция", align=fpdf.Align.C)
            row.cell("Программное обеспечение", align=fpdf.Align.C)
            row.cell("Привозимое оборудование", align=fpdf.Align.C)
            row.cell("Учреждение образования (название полностью), класс.", align=fpdf.Align.C)
            row.cell(
                 "Учреждение дополнительного образования детей и молодежи (или иное) и объединение по интересам, в котором занимается участник", align=fpdf.Align.C)
            row.cell("Фамилия, имя, отчество, место работы педагога, контакты", align=fpdf.Align.C)
            for item in pdf_data:
                for i, participant in enumerate(item.participants):
                    row = table.row()
                    row.cell()
                    row.cell(
                        f"{participant.first_name} "
                        f"{participant.second_name} "
                        f"{participant.third_name}", align=fpdf.Align.C
                    )
                    row.cell(f"{participant.region}")
                    row.cell(f"{participant.birth_date.strftime('%d-%m-%y')}, \n {get_person_age(participant.birth_date)} лет", align=fpdf.Align.C)
                    row.cell(f"{item.nomination_name}", align=fpdf.Align.C)
                    row.cell(f"{participant.software}", align=fpdf.Align.C)
                    row.cell(f"{participant.equipment}", align=fpdf.Align.C)
                    row.cell(f"{participant.educational_institution}", align=fpdf.Align.C)
                    row.cell(f"{participant.additional_educational_institution}", align=fpdf.Align.C)
                    row.cell(f"{participant.supervisor_first_name} {participant.supervisor_second_name} {participant.supervisor_third_name}", align=fpdf.Align.C)
        pdf.write(text='''
                                            Приложение: согласие на обработку и хранение персональных данных участников. 
                                    
                                    Начальник главного управления                          подпись                                                                                                   И.О.Ф.
                                    по образованию                                                      м.п.
                                    
                                    
                                    * заполняется, если участника отправляет учреждение дополнительного образования детей и молодежи (или иное)
''')
        return pdf.output()

    def get_nomination_event_or_raise_if_not_found(
            self,
            nomination_db: type(Nomination),
            event_db: type(Event),
            type_: NominationEventType
    ):
        nomination_event_db = get_nomination_event_db(self.__db, nomination_db, event_db,  type_)
        if not nomination_event_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__nomination_event_does_not_exist_error}
            )
        return nomination_event_db

    def get_nomination_event_data(self, event_db: type(Event)) -> list[NominationEventParticipantCountSchema]:
        return get_nominations_event_participant_count_db(
            self.__db,
            event_db
        )

    def list(self, offset: int, limit: int) -> list[NominationEventSchema]:
        nominations_events = get_nomination_events_all_names_db(self.__db, offset, limit)
        return nominations_events

    def list_by_owner(
            self, offset: int, limit: int, owner_id: int) -> list:
        nominations_events = get_nomination_events_all_names_by_owner_db(self.__db, offset, limit, owner_id)
        return nominations_events

    def list_full_info(self, offset: int, limit: int) -> list:
        nominations_events = get_nomination_events_full_info_db(self.__db, offset, limit)
        return nominations_events

    def list_full_info_by_owner(
            self, offset: int, limit: int, owner_id: int) -> list:
        nominations_events = get_nomination_events_full_info_by_owner_db(self.__db, offset, limit, owner_id)
        return nominations_events

    def append(self,  nomination_db: type(Nomination), event_db: type(Event), user_db, type_: NominationEventType):
        append_event_nomination_db(self.__db, nomination_db, event_db, user_db, type_)

    def delete(self, nomination_event_db: type(NominationEvent)):
        delete_nomination_event_db(self.__db, nomination_event_db)

    def close_registration(self, nomination_event_db: type(NominationEvent)):
        close_registration_nomination_event_db(self.__db, nomination_event_db)

    def open_registration(self, nomination_event_db: type(NominationEvent)):
        open_registration_nomination_event_db(self.__db, nomination_event_db)

    def get_nomination_event_participant_emails(
            self,
            nomination_event_db: type(NominationEvent)
    ):
        return set(
            participant_db.email for participant_db in
            get_participants_of_nomination_event_db(self.__db, nomination_event_db)
        )

    def raise_exception_if_participant_not_in_nomination_event(
            self,
            participant_email: EmailStr,
            nomination_event_db: type(NominationEvent)
    ):
        nomination_event_participant_emails = self.get_nomination_event_participant_emails(
            nomination_event_db
        )

        if participant_email not in nomination_event_participant_emails:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__participant_not_in_nomination_event}
            )

    def raise_exception_if_exists(
            self,
            event_db: type(Event),
            nomination_db: type(Nomination),
            type_: NominationEventType
    ):
        nomination_event_db = get_nomination_event_db(self.__db, nomination_db, event_db, type_)
        if nomination_event_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__nomination_event_already_exist_error}
            )

    def raise_exception_if_tournament_started(self, nomination_event_db: type(NominationEvent)):
        if nomination_event_db.tournament_started:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"message": self.__tournament_started_error}
            )

    def raise_exception_if_tournament_not_started(
            self,
            nomination_event_db: type(NominationEvent)
    ):
        if not nomination_event_db.tournament_started:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"message": self.__tournament_not_started_error}
            )

    def raise_exception_if_participant_in_nomination_event(
            self,
            participant_db: type(Participant),
            nomination_event_db: type(NominationEvent)
    ):
        nomination_event_participant_emails = self.get_nomination_event_participant_emails(
            nomination_event_db
        )
        if participant_db.email in nomination_event_participant_emails:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__participant_already_in_nomination_event}
            )

    def raise_exception_if_registration_finished(
            self,
            nomination_event_db: type(NominationEvent)
    ):
        if nomination_event_db.registration_finished:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__registration_finished_error}
            )

    def raise_exception_if_user_not_in_judge_command(
            self,
            event_db: type(Event),
            nomination_event_db: type(NominationEvent),
            user_db: type(User)
    ):
        judge_command_ids = get_judge_command_ids_db(event_db.owner_id, nomination_event_db)
        if user_db.id not in judge_command_ids:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__user_not_in_judge_command_error}
            )
