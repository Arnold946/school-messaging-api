import logging

from django.conf import settings
from django.utils import timezone
from twilio.rest import Client

from messagerie.models import NotificationTarget


logger = logging.getLogger(__name__)


class WhatsAppService:
    """
    Service responsable de l'envoi des messages WhatsApp
    via Twilio et de la mise à jour du NotificationTarget.
    """

    @staticmethod
    def send(target: NotificationTarget) -> str | None:
        """
        Envoie un message WhatsApp pour un NotificationTarget donné.

        Retourne:
        - le SID Twilio en cas de succès
        - None en cas d'échec
        """

        eleve = target.eleve
        notification = target.notification

        phone = f"whatsapp:{eleve.telephone_parent}"
        message = notification.contenu

        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

        try:
            response = client.messages.create(
                from_=settings.TWILIO_WHATSAPP_SANDBOX,
                to=phone,
                body=message
            )

            # Mise à jour du suivi
            target.statut = "envoye"
            target.twilio_sid = response.sid
            target.date_envoi = timezone.now()
            target.error_message = None
            target.save()

            logger.info(
                f"WhatsApp envoyé avec succès | "
                f"target_id={target.id} | sid={response.sid}"
            )

            return response.sid

        except Exception as e:
            # Gestion d'erreur propre
            target.statut = "echoue"
            target.error_message = str(e)
            target.save()

            logger.error(
                f"Échec envoi WhatsApp | "
                f"target_id={target.id} | erreur={str(e)}"
            )

            return None
