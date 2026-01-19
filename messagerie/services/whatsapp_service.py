from django.conf import settings
from twilio.rest import Client
import logging

logger = logging.getLogger(__name__)

class WhatsAppService:
    @staticmethod
    def send(phone_number: str, message: str) -> str:
        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

        try:
            msg = client.messages.create(
                body=message,
                from_=settings.TWILIO_WHATSAPP_SANDBOX,
                to=f"whatsapp:{phone_number}"
            )
            logger.info(f"WhatsApp envoyé | SID={msg.sid}")
            return msg.sid
        except Exception as e:
            logger.error(f"Erreur WhatsApp Twilio : {e}")
            raise
