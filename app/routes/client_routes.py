from fastapi import APIRouter, HTTPException
from app.controllers.client_controller import client_controller
from app.schemas.client_schemas import ClientCreateRequest

router = APIRouter()

@router.post("/client")
async def register_client(request: ClientCreateRequest):
    """Registra un nuevo cliente"""
    try:
        success, response = client_controller.register_client(request)
        
        if not success:
            return response
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
