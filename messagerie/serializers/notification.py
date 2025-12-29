from rest_framework import serializers

from messagerie.models import Notification
from messagerie.serializers.notification_target import NotificationTargetSerializer


class NotificationWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = [
            'titre',
            'contenu',
            'type_notification',
            'canal',
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        notification = Notification.objects.create(
            cree_par = user,
            **validated_data
        )

        return notification



class NotificationReadSerializer(serializers.ModelSerializer):
    cree_par = serializers.StringRelatedField()
    targets = NotificationTargetSerializer(many=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'titre',
            'contenu',
            'type_notification',
            'canal',
            'cree_par',
            'date_creation',
            'targets',
        ]