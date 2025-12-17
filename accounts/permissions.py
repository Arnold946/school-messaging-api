from rest_framework.permissions import BasePermission


# ============================================================
# 🔒 MOT DE PASSE TEMPORAIRE
# ============================================================

class MustChangePassword(BasePermission):
    """
    Bloque l'accès aux API tant que l'utilisateur
    utilise un mot de passe temporaire.
    """

    message = (
        "Vous devez changer votre mot de passe "
        "avant d'accéder à cette ressource."
    )

    def has_permission(self, request, view):
        user = request.user

        # Laisser DRF gérer les non-authentifiés (401)
        if not user or not user.is_authenticated:
            return True

        # Autoriser la vue de changement de mot de passe
        if view.__class__.__name__ == "ChangePasswordView":
            return True

        # Bloquer si mot de passe temporaire
        return not user.is_temporary_password


# ============================================================
# 🧱 PERMISSION GÉNÉRIQUE PAR RÔLE
# ============================================================

class HasRole(BasePermission):
    """
    Permission générique basée sur un ou plusieurs rôles.
    À spécialiser par héritage.
    """

    allowed_roles = []
    message = "Vous n'avez pas l'autorisation d'accéder à cette ressource."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return user.role in self.allowed_roles


# ============================================================
# 👑 PERMISSIONS PAR RÔLE
# ============================================================

class IsPrincipal(HasRole):
    message = "Accès réservé au principal."
    allowed_roles = ["principal"]


class IsCenseur(HasRole):
    message = "Accès réservé au censeur."
    allowed_roles = ["censeur"]


class IsEnseignant(HasRole):
    message = "Accès réservé à l'enseignant."
    allowed_roles = ["enseignant"]


# ============================================================
# 🤝 PERMISSIONS MULTI-RÔLES
# ============================================================

class IsPrincipalOrCenseur(HasRole):
    message = "Accès réservé au principal ou au censeur."
    allowed_roles = ["principal", "censeur"]


class IsStaff(BasePermission):
    """
    Autorise tous les utilisateurs ayant un rôle valide.
    """

    message = "Accès réservé au personnel."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return user.role in ["principal", "censeur", "enseignant"]
