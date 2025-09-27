"""
Configuración de tests con Pytest
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
import tempfile

from database import Base, get_db
from main import app
from models import Producto
from crud import producto_crud

# Base de datos de prueba en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override para obtener la sesión de prueba"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def setup_database():
    """Configurar base de datos de prueba"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(setup_database):
    """Cliente de prueba para FastAPI"""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def sample_producto():
    """Datos de ejemplo para un producto"""
    return {
        "nombre": "Pan Francés",
        "sku": "PAN-0001",
        "categoria": "Pan",
        "precio_unitario": 1.25,
        "stock": 120,
        "disponible": True
    }

@pytest.fixture
def sample_producto_2():
    """Segundo conjunto de datos de ejemplo para un producto"""
    return {
        "nombre": "Croissant",
        "sku": "PAS-0101",
        "categoria": "Pasteleria",
        "precio_unitario": 2.75,
        "stock": 60,
        "disponible": True
    }
