import re
from django.core.validators import validate_email as django_validate_email
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé pour l'application de messagerie scolaire.

    - Connexion par email
    - Gestion des rôles (principal, censeur, enseignant)
    - Support des mots de passe temporaires
    - Validation du numéro de téléphone camerounais
    """
    ROLE_CHOICES = [
        ('principal', 'Principal'),
        ('censeur', 'Censeur'),
        ('enseignant', 'Enseignant'),
    ]

    PHONE_REGEX = r"^(?:\+237)?6\d{8}$"

    # -----------------------
    # Champs principaux
    # -----------------------
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)  # Email obligatoire pour login
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='principal')

    # -----------------------
    # Mot de passe temporaire
    # -----------------------
    is_temporary_password = models.BooleanField(default=False)

    # -----------------------
    # Paramètres Django
    # -----------------------
    USERNAME_FIELD = 'email'  # Login via email
    REQUIRED_FIELDS = ['username']  # username requis pour création

    def __str__(self):
        return f"{self.username} ({self.role})"

    # -----------------------
    # Validation globale
    # -----------------------
    def clean(self):
        """Validation globale du modèle avant sauvegarde."""
        # -----------------------
        # Email
        # -----------------------
        if self.email:
            value = self.email.strip().lower()
            try:
                django_validate_email(value)
            except ValidationError:
                raise ValidationError({"email": "Email invalide"})

            qs = User.objects.exclude(pk=self.pk).filter(email=value)
            if qs.exists():
                raise ValidationError({"email": "Cet email est déjà utilisé"})
            self.email = value

        # -----------------------
        # Téléphone
        # -----------------------
        if self.phone_number:
            value = self.phone_number.replace(" ", "").replace("-", "")
            if not re.match(self.PHONE_REGEX, value):
                raise ValidationError({
                    "phone_number": (
                        "Le numéro doit commencer par 6 et contenir 9 chiffres, "
                        "avec éventuellement +237 au début."
                    )
                })
            if not value.startswith("+237"):
                value = "+237" + value

            qs = User.objects.exclude(pk=self.pk).filter(phone_number=value)
            if qs.exists():
                raise ValidationError({"phone_number": "Ce numéro est déjà utilisé"})
            self.phone_number = value

    # -----------------------
    # Sauvegarde
    # -----------------------
    def save(self, *args, **kwargs):
        """Appel automatique de clean() avant l’enregistrement."""
        self.full_clean()
        super().save(*args, **kwargs)
