from datetime import datetime
from app.models.client import Client, CardType
from app.models.purchase import Purchase, ProcessedPurchase
from app.utils.date_utils import get_weekday
from app.utils.discount_utils import calculate_discount

class PurchaseService:
    
    RESTRICTED_COUNTRIES_BLACK_WHITE = {"China", "Vietnam", "India", "Iran"}
    
    def process_purchase(self, client: Client, purchase: Purchase) -> tuple[bool, ProcessedPurchase, str]:
        """Procesa una compra aplicando restricciones y beneficios según el tipo de tarjeta"""
        
        # Validar restricciones por país para Black y White
        if client.card_type in [CardType.BLACK, CardType.WHITE]:
            if purchase.purchase_country in self.RESTRICTED_COUNTRIES_BLACK_WHITE:
                error_msg = f"El cliente con tarjeta {client.card_type.value} no puede realizar compras desde {purchase.purchase_country}"
                return False, None, error_msg
        
        # Calcular descuentos según el tipo de tarjeta
        discount_amount, benefit_description = self._calculate_card_benefits(
            client, purchase
        )
        
        final_amount = purchase.amount - discount_amount
        
        processed_purchase = ProcessedPurchase(
            client_id=client.client_id,
            original_amount=purchase.amount,
            discount_applied=discount_amount,
            final_amount=final_amount,
            benefit=benefit_description
        )
        
        return True, processed_purchase, ""
    
    def _calculate_card_benefits(self, client: Client, purchase: Purchase) -> tuple[float, str]:
        """Calcula los beneficios (descuentos) según el tipo de tarjeta"""
        
        weekday = get_weekday(purchase.purchase_date)
        is_foreign_purchase = purchase.purchase_country != client.country
        
        if client.card_type == CardType.CLASSIC:
            return 0.0, None
        
        elif client.card_type == CardType.GOLD:
            return self._calculate_gold_benefits(purchase.amount, weekday)
        
        elif client.card_type == CardType.PLATINUM:
            return self._calculate_platinum_benefits(purchase.amount, weekday, is_foreign_purchase)
        
        elif client.card_type == CardType.BLACK:
            return self._calculate_black_benefits(purchase.amount, weekday, is_foreign_purchase)
        
        elif client.card_type == CardType.WHITE:
            return self._calculate_white_benefits(purchase.amount, weekday, is_foreign_purchase)
        
        return 0.0, None
    
    def _calculate_gold_benefits(self, amount: float, weekday: int) -> tuple[float, str]:
        """Calcula beneficios para tarjeta Gold"""
        # Lunes, martes y miércoles (0, 1, 2), compras > 100 USD = 15% descuento
        if weekday in [0, 1, 2] and amount > 100:
            discount = calculate_discount(amount, 15)
            return discount, "Lunes/Martes/Miércoles - Descuento 15%"
        return 0.0, None
    
    def _calculate_platinum_benefits(self, amount: float, weekday: int, is_foreign: bool) -> tuple[float, str]:
        """Calcula beneficios para tarjeta Platinum"""
        discounts = []
        
        # Lunes, martes y miércoles, compras > 100 USD = 20% descuento
        if weekday in [0, 1, 2] and amount > 100:
            discounts.append((calculate_discount(amount, 20), "Lunes/Martes/Miércoles - Descuento 20%"))
        
        # Sábados, compras > 200 USD = 30% descuento
        if weekday == 5 and amount > 200:
            discounts.append((calculate_discount(amount, 30), "Sábado - Descuento 30%"))
        
        # Compras en el exterior = 5% descuento
        if is_foreign:
            discounts.append((calculate_discount(amount, 5), "Compra en el exterior - Descuento 5%"))
        
        if discounts:
            # Aplicar el mejor descuento
            best_discount = max(discounts, key=lambda x: x[0])
            return best_discount
        
        return 0.0, None
    
    def _calculate_black_benefits(self, amount: float, weekday: int, is_foreign: bool) -> tuple[float, str]:
        """Calcula beneficios para tarjeta Black"""
        discounts = []
        
        # Lunes, martes y miércoles, compras > 100 USD = 25% descuento
        if weekday in [0, 1, 2] and amount > 100:
            discounts.append((calculate_discount(amount, 25), "Lunes/Martes/Miércoles - Descuento 25%"))
        
        # Sábados, compras > 200 USD = 35% descuento
        if weekday == 5 and amount > 200:
            discounts.append((calculate_discount(amount, 35), "Sábado - Descuento 35%"))
        
        # Compras en el exterior = 5% descuento
        if is_foreign:
            discounts.append((calculate_discount(amount, 5), "Compra en el exterior - Descuento 5%"))
        
        if discounts:
            # Aplicar el mejor descuento
            best_discount = max(discounts, key=lambda x: x[0])
            return best_discount
        
        return 0.0, None
    
    def _calculate_white_benefits(self, amount: float, weekday: int, is_foreign: bool) -> tuple[float, str]:
        """Calcula beneficios para tarjeta White"""
        discounts = []
        
        # Lunes a viernes, compras > 100 USD = 25% descuento
        if weekday in [0, 1, 2, 3, 4] and amount > 100:
            discounts.append((calculate_discount(amount, 25), "Lunes a Viernes - Descuento 25%"))
        
        # Sábados y domingos, compras > 200 USD = 35% descuento
        if weekday in [5, 6] and amount > 200:
            discounts.append((calculate_discount(amount, 35), "Fin de semana - Descuento 35%"))
        
        # Compras en el exterior = 5% descuento
        if is_foreign:
            discounts.append((calculate_discount(amount, 5), "Compra en el exterior - Descuento 5%"))
        
        if discounts:
            # Aplicar el mejor descuento
            best_discount = max(discounts, key=lambda x: x[0])
            return best_discount
        
        return 0.0, None

purchase_service = PurchaseService()
