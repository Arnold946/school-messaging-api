from django.utils import timezone
from rest_framework import serializers

from messagerie.models import Notification, Eleve, NotificationTarget
from messagerie.serializers.notification_target import NotificationTargetSerializer


class NotificationWriteSerializer(serializers.ModelSerializer):
    """
    Serializer dédié à la CRÉATION d'une notification.

    Il accepte des champs "virtuels" (eleve_id, classe_id, send_to_all)
    qui permettent de déterminer les destinataires, sans être stockés
    directement dans le modèle Notification.
    """

    # Champ virtuel : envoi ciblé à un élève précis
    eleve_id = serializers.IntegerField(required=False, write_only=True)

    # Champ virtuel : envoi à tous les élèves d'une classe
    classe_id = serializers.IntegerField(required=False, write_only=True)

    # Champ virtuel : diffusion globale à tout l'établissement
    send_to_all = serializers.BooleanField(required=False, write_only=True)

    class Meta:
        model = Notification
        fields = [
            'titre',
            'contenu',
            'type_notification',
            'canal',
            'eleve_id',
            'classe_id',
            'send_to_all',
        ]

    def validate(self, attrs):
        """
        Validation métier globale.

        Règle :
        - EXACTEMENT un seul mode de destination doit être fourni.
        - Pas zéro, pas plusieurs.
        """

        eleve_id = attrs.get('eleve_id')
        classe_id = attrs.get('classe_id')
        send_to_all = attrs.get('send_to_all')

        # On compte combien de modes de destination sont renseignés
        provided = sum([
            bool(eleve_id),
            bool(classe_id),
            bool(send_to_all),
        ])

        if provided != 1:
            raise serializers.ValidationError(
                "Vous devez choisir UN seul mode de destination : "
                "élève, classe ou tout l’établissement."
            )

        return attrs

    def create(self, validated_data):
        """
        Création de la notification et de ses destinataires.

        Étapes :
        1. Création de la notification (entité centrale)
        2. Résolution des élèves concernés
        3. Création des NotificationTarget (relations)
        """

        # Récupération de l'utilisateur connecté depuis le contexte
        request = self.context['request']
        user = request.user

        # Extraction des champs virtuels
        # pop() est obligatoire pour éviter des erreurs SQL
        eleve_id = validated_data.pop('eleve_id', None)
        classe_id = validated_data.pop('classe_id', None)
        send_to_all = validated_data.pop('send_to_all', False)

        # Création de la notification (sans destinataires)
        notification = Notification.objects.create(
            cree_par=user,
            **validated_data
        )

        # Détermination des élèves ciblés selon le mode choisi
        if eleve_id:
            eleves = Eleve.objects.filter(id=eleve_id)

        elif classe_id:
            eleves = Eleve.objects.filter(classe_id=classe_id)

        elif send_to_all:
            eleves = Eleve.objects.all()

        # Sécurité supplémentaire :
        # empêche la création de notifications sans destinataires réels
        if not eleves.exists():
            raise serializers.ValidationError(
                "Aucun élève trouvé pour cette sélection."
            )

        # Préparation des relations Notification ↔ Élève
        # (pas d'accès à la base ici, uniquement en mémoire)
        now = timezone.now()
        targets = [
            NotificationTarget(
                notification=notification,
                eleve=eleve,
                date_envoi = now
            )
            for eleve in eleves
        ]

        # Insertion en masse pour des raisons de performance
        NotificationTarget.objects.bulk_create(targets)

        return notification


class NotificationReadSerializer(serializers.ModelSerializer):
    """
    Serializer dédié à la LECTURE des notifications.

    Il expose :
    - l'auteur
    - les informations de la notification
    - les destinataires (via NotificationTarget)
    """

    # Affichage lisible de l'auteur (via __str__ du modèle User)
    cree_par = serializers.StringRelatedField()

    # Liste des destinataires associés à la notification
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
