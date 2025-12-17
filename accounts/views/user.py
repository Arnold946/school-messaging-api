from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models.user import User
from accounts.permissions import IsPrincipal
from accounts.serializers.user import UserWriteSerializer, UserReadSerializer
from accounts.services.email_service import send_temporary_password_email


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les utilisateurs (CRUD complet).
    Lors de la création :
      - si aucun mot de passe n’est fourni → le serializer génère un mdp temporaire
      - la vue envoie l’email si mdp temporaire
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserWriteSerializer
    permission_classes = [IsAuthenticated, IsPrincipal]

    def get_serializer_class(self):
        """Utilise un serializer différent pour lecture/écriture."""
        if self.action in ["list", "retrieve"]:
            return UserReadSerializer
        return UserWriteSerializer

    # ------------------------------------------------------------
    # CRÉATION D’UN UTILISATEUR (POST)
    # ------------------------------------------------------------
    def create(self, request, *args, **kwargs):
        """
        Crée un utilisateur.
        Si le serializer génère un mot de passe temporaire :
            → on envoie un email
            → on inclut un message d'avertissement dans la réponse
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Création de l'utilisateur (le serializer gère le mdp)
        user = serializer.save()

        # Vérifier si le serializer a généré un mot de passe temporaire
        temp_password = getattr(user, "_temp_password_plain", None)

        # --- Cas 1 : Mot de passe temporaire généré ---
        if temp_password:
            send_temporary_password_email(user, temp_password)

            data = UserReadSerializer(user, context={"request": request}).data
            return Response(
                {
                    "message": (
                        "Utilisateur créé avec un mot de passe temporaire "
                        "(transmis par email)."
                    ),
                    "user": data,
                },
                status=status.HTTP_201_CREATED,
            )

        # --- Cas 2 : Mot de passe fourni par l'admin ---
        data = UserReadSerializer(user, context={"request": request}).data
        return Response(data, status=status.HTTP_201_CREATED)
