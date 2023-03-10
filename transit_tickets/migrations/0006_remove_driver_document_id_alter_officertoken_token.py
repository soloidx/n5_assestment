# Generated by Django 4.1.6 on 2023-02-14 04:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        (
            "transit_tickets",
            "0005_driver_email_ticket_officer_alter_officertoken_token",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="driver",
            name="document_id",
        ),
        migrations.AlterField(
            model_name="officertoken",
            name="token",
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
