"""
Modelos de la base de datos usando SQLAlchemy
"""
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class Producto(Base):
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    sku = Column(String(20), unique=True, nullable=False, index=True)
    categoria = Column(String(20), nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    disponible = Column(Boolean, default=True)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Producto(id={self.id}, nombre='{self.nombre}', sku='{self.sku}')>"
