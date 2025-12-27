from django.db import models


class Notification(models.Model):
    TYPE_CHOICES = [
        ('communique', 'Communiqué'),
        ('note', 'Note'),
        ('absence', 'Absence'),
        ('bulletin', 'Bulletin'),
    ]

    CANAL_CHOICES = [
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('whatsapp', 'WhatsApp'),
        ('notification', 'Notification interne'),
    ]

    titre = models.CharField(max_length=128)
    contenu = models.TextField()

    type_notification = models.CharField(max_length=50, choices=TYPE_CHOICES)
    canal = models.CharField(max_length=30, choices=CANAL_CHOICES)

    cree_par = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="notifications_creees")

    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre