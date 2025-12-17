from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer JWT personnalisé pour l'application.

    Objectifs :
    1. Permettre la connexion avec email + mot de passe (via le modèle User personnalisé).
    2. Ajouter des informations utiles de l'utilisateur dans le payload JWT.
    3. Personnaliser la réponse JSON lors de l'authentification.
    """

    @classmethod
    def get_token(cls, user):
        """
        Surcharge de la méthode `get_token` pour enrichir le payload du JWT.

        Args:
            user (User): instance de l'utilisateur connecté.

        Returns:
            token (RefreshToken): token JWT avec champs personnalisés.

        Explications :
        - `super().get_token(user)` crée le token de base (access + refresh).
        - On ajoute des champs supplémentaires pour le front-end et les permissions.
        - Ces champs seront encodés dans le JWT et disponibles lors de la vérification du token.
        """
        token = super().get_token(user)

        # Ajouter des champs spécifiques au business logic
        token["role"] = user.role  # Rôle de l'utilisateur (ex: enseignant, principal)
        token["username"] = user.username  # Nom d'utilisateur lisible
        token["is_temporary_password"] = user.is_temporary_password  # Flag mot de passe temporaire
        token["email"] = user.email  # Email de l'utilisateur

        return token

    def validate(self, attrs):
        """
        Surcharge de `validate` pour personnaliser la réponse de login.

        Args:
            attrs (dict): données de connexion reçues (email + password).

        Returns:
            dict: réponse JSON enrichie avec les informations utilisateur.

        Explications :
        - `super().validate(attrs)` effectue la validation standard (vérifie email/password, génère tokens).
        - On ajoute un objet `user` dans la réponse JSON pour éviter un deuxième appel API côté front.
        """
        data = super().validate(attrs)

        data["user"] = {
            "id": self.user.id,
            "email": self.user.email,
            "username": self.user.username,
            "role": self.user.role,
            "is_temporary_password": self.user.is_temporary_password,  # permet au front de forcer le changement de mdp
        }

        return data


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer dédié au changement de mot de passe.

    Utilisation typique : première connexion ou réinitialisation par admin.
    """
    old_password = serializers.CharField(required=True)  # mot de passe actuel (sécurité)
    new_password = serializers.CharField(required=True)  # nouveau mot de passe souhaité

    def validate_new_password(self, value):
        """
        Validation du nouveau mot de passe.

        Règles business :
        - Minimum 6 caractères pour garantir une complexité minimale.
        - On peut ajouter ici des règles supplémentaires (chiffres, majuscules, caractères spéciaux, etc.)
        """
        if len(value) < 6:
            raise serializers.ValidationError("Le mot de passe doit avoir au moins 6 caractères.")
        return value
