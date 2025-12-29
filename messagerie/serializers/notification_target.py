from rest_framework import serializers

from messagerie.models import NotificationTarget


class NotificationTargetSerializer(serializers.ModelSerializer):
    eleve = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = NotificationTarget
        fields = [
            'id',
            'eleve',
            'statut',
            'date_envoi',
            'date_lecture',
        ]
