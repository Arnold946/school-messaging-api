from rest_framework.viewsets import ModelViewSet

from messagerie.models import Eleve
from messagerie.serializers import EleveReadSerializer, EleveWriteSerializer


class EleveViewSet(ModelViewSet):
    queryset = Eleve.objects.select_related('classe')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return EleveReadSerializer
        return EleveWriteSerializer