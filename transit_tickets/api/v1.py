import datetime
import uuid
from typing import List, Optional, Any

from django.http import HttpRequest
from ninja import NinjaAPI
from ninja.pagination import paginate, PageNumberPagination
from ninja.security import HttpBearer
from pydantic import EmailStr

from transit_tickets import models
from transit_tickets.api.schemas import Ticket, TicketResponse


class FieldValidationError(Exception):
    def __init__(self, location: List[str], msg: str):
        self.location = location
        self.msg = msg
        self.type = "value_error.field"

    def __str__(self):
        return f"[{self.type}] - {self.msg}"


class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Optional[Any]:
        uuid_token = uuid.UUID(token)
        officer_token = models.OfficerToken.objects.filter(
            token=uuid_token, expiration_date__gte=datetime.datetime.now(tz=datetime.timezone.utc)
        ).first()

        if officer_token is None:
            return None

        return officer_token.officer


api_router = NinjaAPI()


@api_router.get("/")
def status(*args):
    return {"status": "ok"}


@api_router.post("/v1/cargar_informacion", auth=AuthBearer(), response=Ticket)
def create_ticket(request, ticket: Ticket):
    officer_ticket = models.Ticket()
    vehicle = models.Vehicle.objects.filter(licence_plate=ticket.placa_patente).first()
    if vehicle is None:
        raise FieldValidationError(
            ["body", "placa_patente"], "No existe un vehículo con esa placa"
        )

    officer_ticket.vehicle = vehicle
    officer_ticket.officer = request.auth
    officer_ticket.comments = ticket.comentarios
    officer_ticket.infraction_date = ticket.timestamp
    officer_ticket.save()

    return ticket


@api_router.get("/v1/generar_informe", response=List[TicketResponse])
@paginate(PageNumberPagination)
def generate_report(request, email: EmailStr) -> List[Ticket]:
    tickets_query = models.Ticket.objects.filter(vehicle__driver__email=email)
    # solve N + 1 problem
    tickets_query = tickets_query.select_related("vehicle")
    return tickets_query


@api_router.exception_handler(FieldValidationError)
def handle_validation_error(request, exc: FieldValidationError):
    return api_router.create_response(
        request,
        {"detail": [{"loc": exc.location, "msg": exc.msg, "type": exc.type}]},
        status=422,
    )
