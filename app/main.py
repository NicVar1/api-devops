from fastapi import FastAPI
from app.routes import client_routes, purchase_routes

app = FastAPI(
    title="VISE Payments API",
    description="API REST para procesar pagos con diferentes tipos de tarjetas",
    version="1.0.0"
)

# Incluir rutas
app.include_router(client_routes.router)
app.include_router(purchase_routes.router)

@app.get("/")
async def root():
    return {"message": "VISE Payments API - Sistema de procesamiento de pagos"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
