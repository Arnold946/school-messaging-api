from django.conf import settings
from twilio.rest import Client


class SmsService:
    @staticmethod
    def send(phone_number: str, message: str):
        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

        client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )