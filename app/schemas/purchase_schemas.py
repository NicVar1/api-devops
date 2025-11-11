from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PurchaseRequest(BaseModel):
    clientId: int = Field(..., alias="clientId")
    amount: float = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    purchaseDate: datetime = Field(..., alias="purchaseDate")
    purchaseCountry: str = Field(..., min_length=2, max_length=50, alias="purchaseCountry")

class PurchaseDetails(BaseModel):
    clientId: int = Field(..., alias="clientId")
    originalAmount: float = Field(..., alias="originalAmount")
    discountApplied: float = Field(..., alias="discountApplied")
    finalAmount: float = Field(..., alias="finalAmount")
    benefit: Optional[str] = None

class PurchaseApprovedResponse(BaseModel):
    status: str
    purchase: PurchaseDetails

class PurchaseRejectedResponse(BaseModel):
    status: str
    error: str
