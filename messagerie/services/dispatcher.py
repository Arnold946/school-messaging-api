from .sms_service import SmsService
from .whatsapp_service import WhatsAppService


class NotificationDispatcher:

    @staticmethod
    def dispatch(target):
        """
        Envoie la notification selon le canal choisi.
        """
        eleve = target.eleve
        notification = target.notification

        phone = eleve.telephone_parent
        message = notification.contenu

        if notification.canal == 'SMS':
            SmsService.send(phone, message)

        elif notification.canal == 'WHATSAPP':
            WhatsAppService.send(phone, message)
