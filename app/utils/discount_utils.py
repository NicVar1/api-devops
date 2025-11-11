def calculate_discount(amount: float, percentage: int) -> float:
    """Calcula el monto de descuento basado en el porcentaje"""
    return round(amount * (percentage / 100), 2)

def apply_discount(amount: float, percentage: int) -> float:
    """Aplica el descuento y retorna el monto final"""
    discount = calculate_discount(amount, percentage)
    return round(amount - discount, 2)
