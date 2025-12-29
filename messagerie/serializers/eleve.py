from rest_framework import serializers

from messagerie.models import Eleve
from messagerie.serializers.classe import ClasseSerializer


class EleveWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eleve
        fields = [
            'nom',
            'prenom',
            'telephone_parent',
            'classe',
        ]


class EleveReadSerializer(serializers.ModelSerializer):
    classe = serializers.StringRelatedField()

    class Meta:
        model = Eleve
        fields = [
            'id',
            'nom',
            'prenom',
            'telephone_parent',
            'classe',
        ]
