from app.models.client import Client, CardType

class CardService:
    
    RESTRICTED_COUNTRIES_BLACK_WHITE = {"China", "Vietnam", "India", "Iran"}
    
    def validate_card_eligibility(self, client: Client) -> tuple[bool, str]:
        """Valida si un cliente es elegible para el tipo de tarjeta solicitada"""
        
        if client.card_type == CardType.CLASSIC:
            return True, "Cliente apto para tarjeta Classic"
        
        elif client.card_type == CardType.GOLD:
            if client.monthly_income < 500:
                return False, "El cliente no cumple con el ingreso mínimo de 500 USD para Gold"
            return True, "Cliente apto para tarjeta Gold"
        
        elif client.card_type == CardType.PLATINUM:
            if client.monthly_income < 1000:
                return False, "El cliente no cumple con el ingreso mínimo de 1000 USD para Platinum"
            if not client.vise_club:
                return False, "El cliente no cumple con la suscripción VISE CLUB requerida para Platinum"
            return True, "Cliente apto para tarjeta Platinum"
        
        elif client.card_type == CardType.BLACK:
            if client.monthly_income < 2000:
                return False, "El cliente no cumple con el ingreso mínimo de 2000 USD para Black"
            if not client.vise_club:
                return False, "El cliente no cumple con la suscripción VISE CLUB requerida para Black"
            if client.country in self.RESTRICTED_COUNTRIES_BLACK_WHITE:
                return False, f"El cliente no puede solicitar tarjeta Black desde {client.country}"
            return True, "Cliente apto para tarjeta Black"
        
        elif client.card_type == CardType.WHITE:
            if client.monthly_income < 2000:
                return False, "El cliente no cumple con el ingreso mínimo de 2000 USD para White"
            if not client.vise_club:
                return False, "El cliente no cumple con la suscripción VISE CLUB requerida para White"
            if client.country in self.RESTRICTED_COUNTRIES_BLACK_WHITE:
                return False, f"El cliente no puede solicitar tarjeta White desde {client.country}"
            return True, "Cliente apto para tarjeta White"
        
        return False, "Tipo de tarjeta no válido"

card_service = CardService()
