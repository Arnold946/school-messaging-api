from rest_framework.viewsets import ModelViewSet

from messagerie.models import Notification
from messagerie.serializers import NotificationReadSerializer, NotificationWriteSerializer


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all().select_related('cree_par').prefetch_related('targets')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return NotificationReadSerializer
        return NotificationWriteSerializer