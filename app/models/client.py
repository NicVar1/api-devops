from dataclasses import dataclass
from typing import Optional
from enum import Enum

class CardType(str, Enum):
    CLASSIC = "Classic"
    GOLD = "Gold"
    PLATINUM = "Platinum"
    BLACK = "Black"
    WHITE = "White"

@dataclass
class Client:
    client_id: Optional[int]
    name: str
    country: str
    monthly_income: float
    vise_club: bool
    card_type: CardType
    
    def __post_init__(self):
        if isinstance(self.card_type, str):
            self.card_type = CardType(self.card_type)
