from django.db import models


class NotificationTarget(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('envoye', 'Envoyé'),
        ('echoue', 'Échoué'),
        ('lu', 'Lu'),
    ]

    notification = models.ForeignKey(
        "Notification",
        on_delete=models.CASCADE,
        related_name='targets'
    )

    destinataire = models.ForeignKey(
    "accounts.User",
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente'
    )

    date_envoi = models.DateTimeField(null=True, blank=True)
    date_lecture = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('notification', 'destinataire')

    def __str__(self):
        return f"{self.notification.titre} → {self.destinataire}"