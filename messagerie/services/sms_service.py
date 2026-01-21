import logging

from django.conf import settings
from django.utils import timezone
from twilio.rest import Client

from messagerie.models import NotificationTarget


logger = logging.getLogger(__name__)


class SmsService:
    """
    Service responsable de l'envoi des SMS
    via Twilio et du suivi d'envoi.
    """

    @staticmethod
    def send(target: NotificationTarget) -> str | None:
        """
        Envoie un SMS pour un NotificationTarget donné.

        Retourne :
        - le SID Twilio si succès
        - None si échec
        """

        eleve = target.eleve
        notification = target.notification

        phone = eleve.telephone_parent
        message = notification.contenu

        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

        try:
            response = client.messages.create(
                from_=settings.TWILIO_SMS_FROM,
                to=phone,
                body=message
            )

            target.statut = "envoye"
            target.twilio_sid = response.sid
            target.date_envoi = timezone.now()
            target.error_message = None
            target.save()

            logger.info(
                f"SMS envoyé avec succès | "
                f"target_id={target.id} | sid={response.sid}"
            )

            return response.sid

        except Exception as e:
            target.statut = "echoue"
            target.error_message = str(e)
            target.save()

            logger.error(
                f"Échec envoi SMS | "
                f"target_id={target.id} | erreur={str(e)}"
            )

            return None
