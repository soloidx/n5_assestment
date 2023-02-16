from datetime import datetime

from ninja import Schema, ModelSchema, Field

from transit_tickets import models


class Ticket(Schema):
    placa_patente: str
    timestamp: datetime
    comentarios: str


class TicketResponse(Schema):
    placa_patente: str = Field(..., alias="vehicle.licence_plate")
    timestamp: datetime = Field(..., alias="infraction_date")
    comentarios: str = Field(..., alias="comments")
