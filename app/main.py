from fastapi import FastAPI
from app.routes import client_routes, purchase_routes

# --- 🔹 OpenTelemetry imports (solo trazas, sin métricas)
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


# --- 🔹 Configurar el recurso (nombre del servicio)
resource = Resource.create({"service.name": "apivise"})

# --- 🔹 Configurar exportador OTLP (gRPC)
otlp_exporter = OTLPSpanExporter(
    endpoint="http://otel-collector:4317",  # collector en docker-compose
    insecure=True
)

# --- 🔹 Configurar el TracerProvider
trace_provider = TracerProvider(resource=resource)
trace_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(trace_provider)

# --- 🔹 Crear tracer
tracer = trace.get_tracer("apivise.tracer")

# --- 🔹 Crear la app FastAPI
app = FastAPI(
    title="VISE Payments API",
    description="API REST para procesar pagos con diferentes tipos de tarjetas",
    version="1.0.0"
)

# --- 🔹 Instrumentar FastAPI para generar trazas automáticamente
FastAPIInstrumentor.instrument_app(app)

# --- 🔹 Incluir rutas
app.include_router(client_routes.router)
app.include_router(purchase_routes.router)

# --- 🔹 Endpoint raíz
@app.get("/")
async def root():
    with tracer.start_as_current_span("root_request") as span:
        span.set_attribute("endpoint", "root")
        return {"message": "VISE Payments API - Sistema de procesamiento de pagos"}

# --- 🔹 Ejecutar app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
