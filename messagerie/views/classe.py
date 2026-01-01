from rest_framework.viewsets import ModelViewSet

from messagerie.models import Classe
from messagerie.serializers import ClasseSerializer


class ClasseViewSet(ModelViewSet):
    queryset = Classe.objects.all()
    
    serializer_class = ClasseSerializer