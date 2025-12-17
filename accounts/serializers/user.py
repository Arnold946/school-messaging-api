import re
import string
import random

from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email as django_validate_email

from accounts.models.user import User


# ============================================================
# SERIALIZER DE LECTURE (GET)
# ============================================================
class UserReadSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "role_display",
            "phone_number",
            "date_joined",
            "is_active",
        ]
        read_only_fields = ["id", "date_joined", "role_display"]


# ============================================================
# SERIALIZER D'ÉCRITURE (POST / PUT / PATCH)
# ============================================================
class UserWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "phone_number",
            "password",
        ]

    # ------------------------------------------------------------
    # Utilitaire interne : génération mot de passe temporaire
    # ------------------------------------------------------------
    def _generate_temp_password(self, length=8):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    # ------------------------------------------------------------
    # VALIDATION EMAIL
    # ------------------------------------------------------------
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("L'adresse email est obligatoire")

        value = value.strip().lower()

        try:
            django_validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Email invalide")

        user_id = self.instance.id if self.instance else None
        if User.objects.exclude(id=user_id).filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé")

        return value

    # ------------------------------------------------------------
    # VALIDATION TELEPHONE
    # ------------------------------------------------------------
    def validate_phone_number(self, value):
        if not value:
            raise serializers.ValidationError("Le numéro de téléphone est obligatoire")

        value = value.replace(" ", "").replace("-", "")
        value = re.sub(r"^(?:\+237|00237)?", "", value)

        if not re.match(r"^6\d{8}$", value):
            raise serializers.ValidationError(
                "Le numéro doit commencer par 6 et contenir 9 chiffres."
            )

        value = "+237" + value

        user_id = self.instance.id if self.instance else None
        if User.objects.exclude(id=user_id).filter(phone_number=value).exists():
            raise serializers.ValidationError("Ce numéro est déjà utilisé")

        return value

    # ------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------
    def create(self, validated_data):
        password = validated_data.pop("password", None)

        user = User(**validated_data)

        if password:
            # mot de passe normal
            user.set_password(password)
            user.is_temporary_password = False

        else:
            # mot de passe temporaire automatique
            temp_password = self._generate_temp_password()
            user.set_password(temp_password)
            user.is_temporary_password = True

            # IMPORTANT : stocker le mdp temporaire pour la vue
            user._temp_password_plain = temp_password

        user.save()
        return user

    # ------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
            instance.is_temporary_password = False

        instance.save()
        return instance
