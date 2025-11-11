from typing import List
from app.models.purchase import ProcessedPurchase

class PurchaseRepository:
    def __init__(self):
        self._purchases: List[ProcessedPurchase] = []
    
    def save(self, purchase: ProcessedPurchase) -> ProcessedPurchase:
        self._purchases.append(purchase)
        return purchase
    
    def find_by_client_id(self, client_id: int) -> List[ProcessedPurchase]:
        return [p for p in self._purchases if p.client_id == client_id]
    
    def find_all(self) -> List[ProcessedPurchase]:
        return self._purchases.copy()

# Singleton instance
purchase_repository = PurchaseRepository()
