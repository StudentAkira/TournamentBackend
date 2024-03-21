import os
from typing import cast

from fastapi import HTTPException
from fpdf import FPDF
from sqlalchemy import exists, and_
from sqlalchemy.orm import Session
from starlette import status

from db.crud.event import get_event_by_name_db
from db.crud.nomination_event import get_nomination_events_full_info_db, \
    get_nomination_events_all_names_by_owner_db, \
    get_nomination_events_full_info_by_owner_db, \
    get_nomination_events_all_names_db, append_event_nominations_db, get_nominations_event_participant_count_db, \
    delete_nomination_event_db, append_nomination_for_event_db, get_nomination_event_pdf_data_db
from db.models.event import Event
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from db.schemas.event import EventGetNameSchema
from db.schemas.nomination_event import NominationEventSchema, NominationEventDataSchema, NominationEventDeleteSchema, \
    NominationEventParticipantCountSchema
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

    def get_nomination_event_pdf(self, data: list[NominationEventSchema]):
        pdf_data = get_nomination_event_pdf_data_db(self.__db, data)

        pdf = FPDF(orientation = 'L')
        pdf.add_page()
        pdf.add_font('fontF', 'B', os.path.join(".", 'Roman.ttf'))
        pdf.set_font('fontF', 'B', 14)
        with pdf.table() as table:
            table._first_row_as_headings = False
            table._num_heading_rows = 0
            row = table.row()
            text = "Фамилия Имя Отчество"
            row.cell(text)
            row.cell("Область")
            row.cell("Число, месяц, год рождения, количество полных лет на начало проведения мероприятия")
            row.cell("Компетенция")
            row.cell("Программное обеспечение")
            row.cell("Привозимое оборудование")
            row.cell("Учреждение образования (название полностью), класс.")
            row.cell(
                 "Учреждение дополнительного образования детей и молодежи (или иное) и объединение по интересам, в котором занимается участник")
            row.cell("Фамилия, имя, отчество, место работы педагога, контакты")
            for item in pdf_data:
                for i, participant in enumerate(item.participants):
                    row = table.row()
                    row.cell(
                        f"{participant.first_name} "
                        f"{participant.second_name} "
                        f"{participant.third_name}"
                    )
                    row.cell(f"{participant.region}")
                    row.cell(f"{participant.birth_date}")
                    row.cell(f"{item.nomination_name}")
                    row.cell(f"{participant.software}")
                    row.cell(f"{participant.equipment}")
                    row.cell(f"{participant.educational_institution}")
                    row.cell(f"{participant.additional_educational_institution}")
                    row.cell(f"{participant.supervisor_first_name} {participant.supervisor_second_name} {participant.supervisor_third_name}")
        return pdf.output()

    def get_nomination_event_data(self, event_name: str) -> list[NominationEventParticipantCountSchema]:
        return get_nominations_event_participant_count_db(
            self.__db,
            event_name
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

    def append(self, nomination_event_data: NominationEventSchema):
        append_nomination_for_event_db(self.__db, nomination_event_data)

    def append_many(self, event_data: EventGetNameSchema, nominations: list):
        append_event_nominations_db(self.__db, event_data, nominations)

    def delete(self, nomination_event_data: NominationEventDeleteSchema):
        delete_nomination_event_db(self.__db, nomination_event_data)

    def raise_exception_if_not_found(
            self,
            nomination_name: str,
            event_name: str,
            nomination_event_type: str
    ):
        entity_exists = self.check_nomination_event_exists(
            nomination_name,
            event_name,
            nomination_event_type
        )

        if not entity_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": self.__nomination_event_does_not_exist_error}
            )

    def raise_exception_if_exists(self,  nomination_event_data: NominationEventSchema):

        entity_exists = self.check_nomination_event_exists(
            nomination_event_data.nomination_name,
            nomination_event_data.event_name,
            nomination_event_data.type
        )

        if entity_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"error": self.__nomination_event_already_exist_error}
            )

    def check_nomination_event_exists(
            self,
            nomination_name: str,
            event_name: str,
            nomination_event_type: str
    ) -> bool:
        event_db = self.__db.query(Event).filter(
            cast("ColumnElement[bool]",
                 Event.name == event_name
                 )
        ).first()
        nomination_db = self.__db.query(Nomination).filter(
            cast("ColumnElement[bool]",
                 Nomination.name == nomination_name,
                 )
        ).first()

        entity_exists = self.__db.query(
            exists(

            ).where(
                cast("ColumnElement[bool]", NominationEvent.event_id == event_db.id)
            ).where(
                cast("ColumnElement[bool]", NominationEvent.nomination_id == nomination_db.id)
            ).where(
                cast("ColumnElement[bool]", NominationEvent.type == nomination_event_type)
            )
        ).scalar()

        return entity_exists
