from django.core.mail import send_mail
from django.conf import settings

def send_temporary_password_email(user, temp_password):
    """
    Envoie un email contenant le mot de passe temporaire à l'utilisateur.
    """
    subject = "Votre compte a été créé"
    message = (
        f"Bonjour {user.first_name},\n\n"
        f"Votre compte a été créé avec succès.\n"
        f"Voici votre mot de passe temporaire : {temp_password}\n\n"
        "Veuillez le changer dès votre première connexion.\n\n"
        "Cordialement,\nL’équipe de gestion."
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
