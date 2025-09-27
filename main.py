"""
Aplicación principal FastAPI para el Sistema de Gestión de Productos de Panadería
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from database import engine
from models import Base
from routers.productos import router as productos_router

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(
    title="Sistema de Gestión de Productos de Panadería",
    description="""
    API REST para la gestión de productos de una panadería.
    
    ## Características
    
    * **CRUD completo** para productos
    * **Validación** de datos con Pydantic
    * **Base de datos** PostgreSQL con SQLAlchemy
    * **Documentación** automática con Swagger
    
    ## Reglas de Negocio
    
    * SKU único por producto
    * Categorías válidas: Pan, Pasteleria, Bebidas, Otros
    * Precio unitario mayor a 0
    * Stock mayor o igual a 0
    * Campos obligatorios: nombre, sku, categoria, precio_unitario, stock
    """,
    version="1.0.0",
    contact={
        "name": "Christian Xwer Reyes Valenzuela",
        "email": "0907-22-6610",
    },
    license_info={
        "name": "MIT",
    },
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(productos_router)

@app.get("/")
def root():
    """
    Endpoint raíz de la API
    """
    return {
        "message": "Bienvenido al Sistema de Gestión de Productos de Panadería",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    """
    Endpoint de verificación de salud de la API
    """
    return {"status": "healthy", "message": "API funcionando correctamente"}

# Manejador global de excepciones
@app.exception_handler(Exception)
def global_exception_handler(request, exc):
    """
    Manejador global de excepciones
    """
    logger.error(f"Error no manejado: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error interno del servidor",
            "type": "internal_server_error"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
