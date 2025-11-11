from app.models.client import Client
from app.services.card_service import card_service
from app.repositories.client_repository import client_repository
from app.schemas.client_schemas import ClientCreateRequest, ClientResponse, ClientRejectedResponse

class ClientController:
    
    def register_client(self, request: ClientCreateRequest) -> tuple[bool, dict]:
        """Registra un nuevo cliente si cumple con los requisitos"""
        
        # Crear modelo de cliente
        client = Client(
            client_id=None,
            name=request.name,
            country=request.country,
            monthly_income=request.monthlyIncome,
            vise_club=request.viseClub,
            card_type=request.cardType
        )
        
        # Validar elegibilidad
        is_eligible, message = card_service.validate_card_eligibility(client)
        
        if not is_eligible:
            response = ClientRejectedResponse(
                status="Rejected",
                error=message
            )
            return False, response.dict()
        
        # Guardar cliente
        saved_client = client_repository.save(client)
        
        response = ClientResponse(
            clientId=saved_client.client_id,
            name=saved_client.name,
            cardType=saved_client.card_type,
            status="Registered",
            message=message
        )
        
        return True, response.dict()

client_controller = ClientController()
