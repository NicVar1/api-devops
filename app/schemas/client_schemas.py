from pydantic import BaseModel, Field
from typing import Optional
from app.models.client import CardType

class ClientCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=2, max_length=50)
    monthlyIncome: float = Field(..., ge=0, alias="monthlyIncome")
    viseClub: bool = Field(..., alias="viseClub")
    cardType: CardType = Field(..., alias="cardType")

class ClientResponse(BaseModel):
    clientId: int = Field(..., alias="clientId")
    name: str
    cardType: CardType = Field(..., alias="cardType")
    status: str
    message: str

class ClientRejectedResponse(BaseModel):
    status: str
    error: str
