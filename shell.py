import os
from io import BytesIO

from fpdf import FPDF
from fpdf.enums import PageMode
from reportlab.pdfgen import canvas

from db.database import *
from sqlalchemy import and_
from db.models.event import Event
from db.models.nomination import Nomination
from db.models.nomination_event import NominationEvent
from db.models.participant import Participant
from db.models.team import Team
from db.models.team_participant import TeamParticipant
from db.models.team_participant_nomination_event import TeamParticipantNominationEvent
from db.models.token import Token
from db.models.user import User
from db.schemas.user import UserSchema

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


test = UserSchema(
    email="test@mail.ru",
    first_name="test",
    second_name="test",
    third_name="test",
    phone="+375-29-768-94-62",
    role="admin"
)

pdf = FPDF(orientation='L')
pdf.add_page()
pdf.add_font('fontF', 'B', os.path.join(".", 'Roman.ttf'))
pdf.set_font('fontF', 'B', 14)
c = 1


with pdf.table() as table:
    table._first_row_as_headings = False
    table._num_heading_rows = 0
    print(table.__dir__())
    print(table._first_row_as_headings)
    print(table._padding)
    print(table._outer_border_margin)
    print(table._fpdf)
    print(table._headings_style)
    print(table._gutter_height)
    print(table._gutter_width)
    print(table._wrapmode)
    row = table.row()
    row.cell("0"*10)
    row.cell("1"*10)
    row.cell("2"*10)
    row.cell("3"*10)
    row.cell("4"*10)
    row.cell("5"*10)
    row.cell("6"*10)
    row.cell("7"*10)
    row.cell("8"*10)
    row.cell("9"*10)
    for j in range(30):
        row = table.row([f"test" for k in range(10)])

with open("tmp.pdf", "wb") as f:
    f.write(pdf.output())
