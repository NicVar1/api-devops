from fastapi import APIRouter, HTTPException
from opentelemetry import trace, metrics

from app.controllers.purchase_controller import purchase_controller
from app.schemas.purchase_schemas import PurchaseRequest

router = APIRouter()

# Inicializa tracer y meter
tracer = trace.get_tracer("apivise.purchase.tracer")
meter = metrics.get_meter("apivise.purchase.meter")

# Contador de compras procesadas
purchase_counter = meter.create_counter(
    "apivise.purchase.processed",
    description="Número de compras procesadas por estado",
)

@router.post("/purchase")
async def process_purchase(request: PurchaseRequest):
    """Procesa una compra con trazas y métricas"""
    with tracer.start_as_current_span("process_purchase") as span:
        try:
            # Añadimos información contextual al span
            span.set_attribute("endpoint", "/purchase")
            span.set_attribute("operation", "process_purchase")
            span.set_attribute("purchase.client_id", getattr(request, "client_id", "unknown"))
            span.set_attribute("purchase.total", getattr(request, "total", 0))

            # Contamos cada intento de compra
            purchase_counter.add(1, {"status": "attempt"})

            # Lógica del controlador
            success, response = purchase_controller.process_purchase(request)

            if not success:
                span.set_attribute("status", "failed")
                purchase_counter.add(1, {"status": "failed"})
                return response

            # Éxito
            span.set_attribute("status", "success")
            purchase_counter.add(1, {"status": "success"})
            return response

        except Exception as e:
            # Registrar el error en la traza
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            purchase_counter.add(1, {"status": "error"})

            raise HTTPException(
                status_code=500,
                detail=f"Error interno del servidor: {str(e)}"
            )