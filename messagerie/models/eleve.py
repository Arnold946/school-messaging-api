from django.db import models


class Eleve(models.Model):
    nom = models.CharField(max_length=80)
    prenom = models.CharField(max_length=80)
    telephone_parent = models.CharField(max_length=15)
    classe = models.ForeignKey(
        "Classe",
        on_delete=models.CASCADE,
        related_name='eleves'
    )


    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.classe})"