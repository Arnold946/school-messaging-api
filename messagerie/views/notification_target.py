from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from messagerie.models import NotificationTarget
from messagerie.serializers import NotificationTargetSerializer


class NotificationTargetViewSet(ReadOnlyModelViewSet):
    """
    Consultation des notifications envoyées
    et accusé de lecture interne.
    """

    queryset = NotificationTarget.objects.select_related(
        'eleve', 'notification'
    )
    serializer_class = NotificationTargetSerializer

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """
        Marque la notification comme lue (accusé interne).
        """
        target = self.get_object()

        # Idempotence
        if target.statut != 'lu':
            target.statut = 'lu'
            target.date_lecture = timezone.now()
            target.save()

        return Response({'status': 'ok'})
