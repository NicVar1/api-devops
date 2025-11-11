from fastapi import APIRouter, HTTPException
from app.controllers.client_controller import client_controller
from app.schemas.client_schemas import ClientCreateRequest

from opentelemetry import trace, metrics

router = APIRouter()

# Inicializa tracer y meter
tracer = trace.get_tracer("apivise.client.tracer")
meter = metrics.get_meter("apivise.client.meter")

# Contador de registros de clientes
client_registration_counter = meter.create_counter(
    "apivise.client.registrations",
    description="Número de intentos de registro de clientes",
)

@router.post("/client")
async def register_client(request: ClientCreateRequest):
    """Registra un nuevo cliente con trazas y métricas"""
    # Creamos un nuevo span manual para rastrear este endpoint
    with tracer.start_as_current_span("register_client") as span:
        try:
            # Agregamos información útil como atributos al span
            span.set_attribute("endpoint", "/client")
            span.set_attribute("client.name", getattr(request, "name", "unknown"))
            span.set_attribute("operation", "register_client")

            # Contamos cada intento de registro (éxito o error)
            client_registration_counter.add(1, {"status": "attempt"})

            # Llamamos al controlador
            success, response = client_controller.register_client(request)

            # Registramos el resultado
            if not success:
                span.set_attribute("status", "failed")
                client_registration_counter.add(1, {"status": "failed"})
                return response

            span.set_attribute("status", "success")
            client_registration_counter.add(1, {"status": "success"})
            return response

        except Exception as e:
            # Marcamos el error en el span
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            client_registration_counter.add(1, {"status": "error"})

            raise HTTPException(
                status_code=500,
                detail=f"Error interno del servidor: {str(e)}"
            )