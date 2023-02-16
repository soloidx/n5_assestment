from django.test import TestCase, Client
import datetime
import json
from transit_tickets.models import Driver, Officer, OfficerToken, Vehicle, Ticket


class CargarInformacionTestCase(TestCase):
    def setUp(self) -> None:
        self.test_driver = Driver.objects.create(
            full_name="Driver 1", email="driver1@mail.com"
        )
        self.test_vehicle = Vehicle.objects.create(
            licence_plate="test001",
            model="toyota",
            color="plomo",
            driver=self.test_driver,
        )

        self.test_officer = Officer.objects.create(
            full_name="Officer 1", unique_id="off001"
        )
        self.test_token = OfficerToken.objects.create(officer=self.test_officer)

    def test_endpoint_Without_token_should_be_unauthorized(self):
        c = Client()
        response = c.post("/api/v1/cargar_informacion")
        self.assertEqual(response.status_code, 401)

    def test_endpoint_with_token_should_pass(self):
        token = self.test_token.token
        response = self.client.post(
            "/api/v1/cargar_informacion",
            data={"foo": "bar"},
            HTTP_AUTHORIZATION=f"Bearer {token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 422)

    def test_endpoint_with_token_and_data_should_work(self):
        token = self.test_token.token
        test_data = {
            "placa_patente": self.test_vehicle.licence_plate,
            "timestamp": datetime.datetime.now(),
            "comentarios": "comentario de ejemplo",
        }
        response = self.client.post(
            "/api/v1/cargar_informacion",
            data=test_data,
            HTTP_AUTHORIZATION=f"Bearer {token}",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def tearDown(self) -> None:
        self.test_officer.delete()
        self.test_driver.delete()


class GenerarInformeTestCase(TestCase):
    def setUp(self) -> None:
        self.test_driver = Driver.objects.create(
            full_name="Driver 2", email="driver2@mail.com"
        )
        self.test_vehicle = Vehicle.objects.create(
            licence_plate="test002",
            model="toyota",
            color="negro",
            driver=self.test_driver,
        )

        self.test_officer = Officer.objects.create(
            full_name="Officer 1", unique_id="off001"
        )
        self.test_token = OfficerToken.objects.create(officer=self.test_officer)

        [
            Ticket.objects.create(
                vehicle=self.test_vehicle,
                officer=self.test_officer,
                infraction_date=datetime.datetime.now(),
                comments="test %s" % x,
            )
            for x in range(3)
        ]

    def test_endpoint_Without_token_should_be_unauthorized(self):
        raw_response = self.client.get("/api/v1/generar_informe", {'email': self.test_driver.email})
        response = raw_response.json()
        self.assertEqual(len(response['items']), 3)

