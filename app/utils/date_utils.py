from datetime import datetime

def get_weekday(date: datetime) -> int:
    """
    Retorna el día de la semana como entero
    0 = Lunes, 1 = Martes, ..., 6 = Domingo
    """
    return date.weekday()

def get_weekday_name(date: datetime) -> str:
    """Retorna el nombre del día de la semana en español"""
    days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    return days[date.weekday()]
