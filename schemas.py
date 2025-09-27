"""
Esquemas Pydantic para validación de datos
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from decimal import Decimal

# Categorías válidas para los productos
CATEGORIAS_VALIDAS = ["Pan", "Pasteleria", "Bebidas", "Otros"]

class ProductoBase(BaseModel):
    """Esquema base para Producto"""
    nombre: str = Field(..., max_length=150, description="Nombre del producto")
    sku: str = Field(..., description="SKU único del producto")
    categoria: str = Field(..., description="Categoría del producto")
    precio_unitario: Decimal = Field(..., gt=0, decimal_places=2, description="Precio unitario")
    stock: int = Field(..., ge=0, description="Cantidad en stock")
    disponible: bool = Field(default=True, description="Disponibilidad del producto")
    
    @validator('categoria')
    def validar_categoria(cls, v):
        if v not in CATEGORIAS_VALIDAS:
            raise ValueError(f'Categoría debe ser una de: {", ".join(CATEGORIAS_VALIDAS)}')
        return v
    
    @validator('nombre')
    def validar_nombre(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Nombre no puede estar vacío')
        return v.strip()
    
    @validator('sku')
    def validar_sku(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('SKU no puede estar vacío')
        return v.strip()

class ProductoCreate(ProductoBase):
    """Esquema para crear un producto"""
    pass

class ProductoUpdate(BaseModel):
    """Esquema para actualizar un producto"""
    nombre: Optional[str] = Field(None, max_length=150)
    sku: Optional[str] = None
    categoria: Optional[str] = None
    precio_unitario: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    stock: Optional[int] = Field(None, ge=0)
    disponible: Optional[bool] = None
    
    @validator('categoria')
    def validar_categoria(cls, v):
        if v is not None and v not in CATEGORIAS_VALIDAS:
            raise ValueError(f'Categoría debe ser una de: {", ".join(CATEGORIAS_VALIDAS)}')
        return v
    
    @validator('nombre')
    def validar_nombre(cls, v):
        if v is not None and (not v or len(v.strip()) == 0):
            raise ValueError('Nombre no puede estar vacío')
        return v.strip() if v else v
    
    @validator('sku')
    def validar_sku(cls, v):
        if v is not None and (not v or len(v.strip()) == 0):
            raise ValueError('SKU no puede estar vacío')
        return v.strip() if v else v

class ProductoResponse(ProductoBase):
    """Esquema para respuesta de Producto"""
    id: int
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ProductoList(BaseModel):
    """Esquema para lista de productos"""
    items: list[ProductoResponse]
    total: int
    
    class Config:
        from_attributes = True
