from django.db import models


class Classe(models.Model):
    nom = models.CharField(max_length=10, null=True)
    niveau = models.CharField(max_length=15)


    def __str__(self):
        return f"{self.niveau} - {self.nom}"