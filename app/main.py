from fastapi import FastAPI
from app.routes import client_routes, purchase_routes

# --- 🔹 OpenTelemetry imports
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor



# --- 🔹 Configurar el recurso (nombre del servicio)
resource = Resource.create({"service.name": "apivise"})

# --- 🔹 Configurar exportadores hacia el collector
otlp_exporter = OTLPSpanExporter(
    endpoint="http://otel-collector:4317",  # nombre del contenedor collector
    insecure=True
)
metric_exporter = OTLPMetricExporter(
    endpoint="http://otel-collector:4317",
    insecure=True
)

# --- 🔹 Configurar providers
trace_provider = TracerProvider(resource=resource)
trace_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(trace_provider)

meter_provider = MeterProvider(
    resource=resource,
    metric_readers=[PeriodicExportingMetricReader(metric_exporter)]
)
metrics.set_meter_provider(meter_provider)

# --- 🔹 Crear tracer y meter
tracer = trace.get_tracer("apivise.tracer")
meter = metrics.get_meter("apivise.meter")

# --- 🔹 Métrica personalizada
request_counter = meter.create_counter(
    "apivise.requests",
    description="Número de peticiones por endpoint",
)

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
    request_counter.add(1, {"endpoint": "root"})
    return {"message": "VISE Payments API - Sistema de procesamiento de pagos"}

# --- 🔹 Ejecutar app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
