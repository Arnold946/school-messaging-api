from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from accounts.serializers.auth import CustomTokenObtainPairSerializer, ChangePasswordSerializer

User = get_user_model()


# ------------------------------------------------------------
# LOGIN JWT PERSONNALISÉ
# ------------------------------------------------------------
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    View permettant de générer les tokens JWT (access + refresh) via email + password.
    Utilise le serializer CustomTokenObtainPairSerializer pour :
    - enrichir le payload du token
    - personnaliser la réponse JSON
    """
    serializer_class = CustomTokenObtainPairSerializer


# ------------------------------------------------------------
# CHANGEMENT DE MOT DE PASSE
# ------------------------------------------------------------
class ChangePasswordView(APIView):
    """
    Permet à un utilisateur de changer son mot de passe.
    Typiquement utilisé lors de la première connexion si le mot de passe est temporaire.
    """
    permission_classes = [permissions.IsAuthenticated]  # Seuls les utilisateurs connectés peuvent changer leur mdp

    def post(self, request, *args, **kwargs):
        """
        Endpoint POST pour permettre à un utilisateur de changer son mot de passe.

        Route typique : /api/auth/change-password/
        Payload attendu (JSON) :
            {
                "old_password": "ancien_mdp",
                "new_password": "nouveau_mdp"
            }

        Notes :
        - Seuls les utilisateurs authentifiés peuvent accéder à cette route.
        - Vérifie que l'ancien mot de passe est correct avant de permettre le changement.
        - Met à jour le flag `is_temporary_password` si le mot de passe était temporaire.
        """

        # -------------------------------
        # Instanciation et validation du serializer
        # -------------------------------
        serializer = ChangePasswordSerializer(data=request.data)
        # is_valid(raise_exception=True) :
        # - valide les champs (ancien et nouveau mot de passe)
        # - lève automatiquement une exception HTTP 400 si invalides
        serializer.is_valid(raise_exception=True)

        # -------------------------------
        # Récupération de l'utilisateur courant
        # -------------------------------
        # request.user est peuplé par le middleware d'authentification (JWT / session)
        user = request.user

        # -------------------------------
        # Vérification de l'ancien mot de passe
        # -------------------------------
        # check_password() compare le mot de passe fourni au hash stocké en DB
        if not user.check_password(serializer.validated_data["old_password"]):
            # Réponse 400 si le mot de passe actuel ne correspond pas
            # Retour structuré côté client pour afficher un message spécifique
            return Response(
                {"old_password": ["Mot de passe actuel incorrect."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # -------------------------------
        # Mise à jour sécurisée du mot de passe
        # -------------------------------
        # set_password() hash le mot de passe correctement
        # NE JAMAIS stocker le mot de passe en clair (user.password = "...")
        user.set_password(serializer.validated_data["new_password"])

        # Mise à jour du flag : utilisateur n'a plus de mot de passe temporaire
        user.is_temporary_password = False

        # Persistance en base
        user.save()

        # -------------------------------
        # Réponse HTTP de succès
        # -------------------------------
        # Status 200 OK avec un message simple et lisible côté client
        return Response(
            {"detail": "Mot de passe mis à jour avec succès."},
            status=status.HTTP_200_OK
        )

