from datetime import datetime
from app.models.purchase import Purchase
from app.services.purchase_service import purchase_service
from app.repositories.client_repository import client_repository
from app.repositories.purchase_repository import purchase_repository
from app.schemas.purchase_schemas import (
    PurchaseRequest, 
    PurchaseApprovedResponse, 
    PurchaseRejectedResponse,
    PurchaseDetails
)

class PurchaseController:
    
    def process_purchase(self, request: PurchaseRequest) -> tuple[bool, dict]:
        """Procesa una compra aplicando las reglas de negocio"""
        
        # Buscar cliente
        client = client_repository.find_by_id(request.clientId)
        if not client:
            response = PurchaseRejectedResponse(
                status="Rejected",
                error=f"Cliente con ID {request.clientId} no encontrado"
            )
            return False, response.dict()
        
        # Crear modelo de compra
        purchase = Purchase(
            client_id=request.clientId,
            amount=request.amount,
            currency=request.currency,
            purchase_date=request.purchaseDate,
            purchase_country=request.purchaseCountry
        )
        
        # Procesar compra
        is_approved, processed_purchase, error_message = purchase_service.process_purchase(
            client, purchase
        )
        
        if not is_approved:
            response = PurchaseRejectedResponse(
                status="Rejected",
                error=error_message
            )
            return False, response.dict()
        
        # Guardar compra procesada
        purchase_repository.save(processed_purchase)
        
        # Crear respuesta
        purchase_details = PurchaseDetails(
            clientId=processed_purchase.client_id,
            originalAmount=processed_purchase.original_amount,
            discountApplied=processed_purchase.discount_applied,
            finalAmount=processed_purchase.final_amount,
            benefit=processed_purchase.benefit
        )
        
        response = PurchaseApprovedResponse(
            status="Approved",
            purchase=purchase_details
        )
        
        return True, response.dict()

purchase_controller = PurchaseController()
