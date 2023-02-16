import datetime

from django.db import models
import uuid

# Create your models here.


class Officer(models.Model):
    full_name = models.CharField(max_length=200)
    unique_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.unique_id}: {self.full_name}"


def default_expiration_date():
    return datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=2)


class OfficerToken(models.Model):
    officer = models.ForeignKey(Officer, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4)
    expiration_date = models.DateTimeField(default=default_expiration_date)


class Driver(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"[{self.email}] {self.full_name}"


class Vehicle(models.Model):
    licence_plate = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.licence_plate} - {self.model} / {self.color}"


class Ticket(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    officer = models.ForeignKey(Officer, on_delete=models.CASCADE)
    infraction_date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField()
