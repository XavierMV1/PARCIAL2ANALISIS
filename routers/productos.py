"""
Endpoints para la gestión de productos
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from crud import producto_crud
from schemas import ProductoCreate, ProductoUpdate, ProductoResponse, ProductoList
import logging

logger = logging.getLogger(__name__)

# Crear el router
router = APIRouter(
    prefix="/api/v1/productos",
    tags=["productos"],
    responses={404: {"description": "Producto no encontrado"}},
)

@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo producto
    
    - **nombre**: Nombre del producto (máximo 150 caracteres)
    - **sku**: SKU único del producto
    - **categoria**: Categoría (Pan, Pasteleria, Bebidas, Otros)
    - **precio_unitario**: Precio unitario (mayor a 0)
    - **stock**: Cantidad en stock (mayor o igual a 0)
    - **disponible**: Disponibilidad del producto (opcional, default: true)
    """
    try:
        # Verificar si el SKU ya existe
        existing_producto = producto_crud.get_producto_by_sku(db, producto.sku)
        if existing_producto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El SKU ya existe"
            )
        
        db_producto = producto_crud.create_producto(db, producto)
        return db_producto
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error al crear producto: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/", response_model=ProductoList)
def listar_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Listar todos los productos con paginación
    
    - **skip**: Número de registros a saltar (default: 0)
    - **limit**: Límite de registros a retornar (default: 100)
    """
    try:
        productos = producto_crud.get_productos(db, skip=skip, limit=limit)
        total = producto_crud.count_productos(db)
        return ProductoList(items=productos, total=total)
    except Exception as e:
        logger.error(f"Error al listar productos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    """
    Obtener un producto por ID
    
    - **producto_id**: ID del producto a consultar
    """
    try:
        producto = producto_crud.get_producto(db, producto_id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
        return producto
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener producto: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(
    producto_id: int, 
    producto_update: ProductoUpdate, 
    db: Session = Depends(get_db)
):
    """
    Actualizar un producto existente
    
    - **producto_id**: ID del producto a actualizar
    - **producto_update**: Datos a actualizar (todos los campos son opcionales)
    """
    try:
        # Verificar si el producto existe
        existing_producto = producto_crud.get_producto(db, producto_id)
        if not existing_producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
        
        # Verificar si el nuevo SKU ya existe (si se está actualizando)
        if producto_update.sku and producto_update.sku != existing_producto.sku:
            sku_exists = producto_crud.get_producto_by_sku(db, producto_update.sku)
            if sku_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El SKU ya existe"
                )
        
        db_producto = producto_crud.update_producto(db, producto_id, producto_update)
        return db_producto
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error al actualizar producto: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un producto
    
    - **producto_id**: ID del producto a eliminar
    """
    try:
        deleted = producto_crud.delete_producto(db, producto_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al eliminar producto: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
