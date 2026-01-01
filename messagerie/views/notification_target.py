from rest_framework.viewsets import ReadOnlyModelViewSet

from messagerie.models import NotificationTarget
from messagerie.serializers import NotificationTargetSerializer


class NotificationTargetViewSet(ReadOnlyModelViewSet):
    queryset = NotificationTarget.objects.select_related('eleve', 'notification')
    serializer_class = NotificationTargetSerializer