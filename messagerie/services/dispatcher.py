from .sms_service import SmsService
from .whatsapp_service import WhatsAppService


class NotificationDispatcher:

    @staticmethod
    def dispatch(target):
        """
        Envoie la notification selon le canal choisi
        et met à jour le NotificationTarget.
        """

        canal = target.notification.canal

        if canal == 'SMS':
            SmsService.send(target)

        elif canal == 'WHATSAPP':
            WhatsAppService.send(target)

