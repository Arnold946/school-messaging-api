class WhatsAppService:
    @staticmethod
    def send(phone_number: str, message: str):
        """
        Envoi WhatsApp
        """
        print(f"[WHATSAPP] → {phone_number} : {message}")
