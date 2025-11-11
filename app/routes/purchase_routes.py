from fastapi import APIRouter, HTTPException
from app.controllers.purchase_controller import purchase_controller
from app.schemas.purchase_schemas import PurchaseRequest

router = APIRouter()

@router.post("/purchase")
async def process_purchase(request: PurchaseRequest):
    """Procesa una compra"""
    try:
        success, response = purchase_controller.process_purchase(request)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
