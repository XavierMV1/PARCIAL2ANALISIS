"""
Operaciones CRUD para productos
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from models import Producto
from schemas import ProductoCreate, ProductoUpdate
import logging

logger = logging.getLogger(__name__)

class ProductoCRUD:
    """Clase para operaciones CRUD de productos"""
    
    def create_producto(self, db: Session, producto: ProductoCreate) -> Producto:
        """
        Crear un nuevo producto
        
        Args:
            db: Sesión de la base de datos
            producto: Datos del producto a crear
            
        Returns:
            Producto creado
            
        Raises:
            IntegrityError: Si el SKU ya existe
        """
        try:
            db_producto = Producto(**producto.dict())
            db.add(db_producto)
            db.commit()
            db.refresh(db_producto)
            return db_producto
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Error de integridad al crear producto: {e}")
            raise ValueError("El SKU ya existe")
        except Exception as e:
            db.rollback()
            logger.error(f"Error inesperado al crear producto: {e}")
            # Si es un error de SQLite relacionado con restricciones únicas
            if "UNIQUE constraint failed" in str(e) or "duplicate key" in str(e).lower():
                raise ValueError("El SKU ya existe")
            raise
    
    def get_producto(self, db: Session, producto_id: int) -> Optional[Producto]:
        """
        Obtener un producto por ID
        
        Args:
            db: Sesión de la base de datos
            producto_id: ID del producto
            
        Returns:
            Producto encontrado o None
        """
        return db.query(Producto).filter(Producto.id == producto_id).first()
    
    def get_productos(self, db: Session, skip: int = 0, limit: int = 100) -> List[Producto]:
        """
        Obtener lista de productos con paginación
        
        Args:
            db: Sesión de la base de datos
            skip: Número de registros a saltar
            limit: Límite de registros a retornar
            
        Returns:
            Lista de productos
        """
        return db.query(Producto).offset(skip).limit(limit).all()
    
    def get_producto_by_sku(self, db: Session, sku: str) -> Optional[Producto]:
        """
        Obtener un producto por SKU
        
        Args:
            db: Sesión de la base de datos
            sku: SKU del producto
            
        Returns:
            Producto encontrado o None
        """
        return db.query(Producto).filter(Producto.sku == sku).first()
    
    def update_producto(self, db: Session, producto_id: int, producto_update: ProductoUpdate) -> Optional[Producto]:
        """
        Actualizar un producto
        
        Args:
            db: Sesión de la base de datos
            producto_id: ID del producto a actualizar
            producto_update: Datos a actualizar
            
        Returns:
            Producto actualizado o None si no existe
            
        Raises:
            IntegrityError: Si el SKU ya existe
        """
        try:
            db_producto = self.get_producto(db, producto_id)
            if not db_producto:
                return None
            
            # Actualizar solo los campos proporcionados
            update_data = producto_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_producto, field, value)
            
            db.commit()
            db.refresh(db_producto)
            return db_producto
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Error de integridad al actualizar producto: {e}")
            raise ValueError("El SKU ya existe")
        except Exception as e:
            db.rollback()
            logger.error(f"Error inesperado al actualizar producto: {e}")
            # Si es un error de SQLite relacionado con restricciones únicas
            if "UNIQUE constraint failed" in str(e) or "duplicate key" in str(e).lower():
                raise ValueError("El SKU ya existe")
            raise
    
    def delete_producto(self, db: Session, producto_id: int) -> bool:
        """
        Eliminar un producto
        
        Args:
            db: Sesión de la base de datos
            producto_id: ID del producto a eliminar
            
        Returns:
            True si se eliminó, False si no existe
        """
        db_producto = self.get_producto(db, producto_id)
        if not db_producto:
            return False
        
        db.delete(db_producto)
        db.commit()
        return True
    
    def count_productos(self, db: Session) -> int:
        """
        Contar total de productos
        
        Args:
            db: Sesión de la base de datos
            
        Returns:
            Número total de productos
        """
        return db.query(Producto).count()

# Instancia global del CRUD
producto_crud = ProductoCRUD()
