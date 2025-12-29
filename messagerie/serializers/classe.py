from rest_framework import serializers

from messagerie.models import Classe


class ClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classe
        fields = [
            'nom',
            'niveau',
        ]