from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Purchase:
    client_id: int
    amount: float
    currency: str
    purchase_date: datetime
    purchase_country: str
    
@dataclass
class ProcessedPurchase:
    client_id: int
    original_amount: float
    discount_applied: float
    final_amount: float
    benefit: Optional[str] = None
