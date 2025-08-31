from typing import List, Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal
import pymongo
from pymongo.errors import PyMongoError
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import NotFoundException, BaseException


class ProductUsecase:
    def __init__(self) -> None:
        # Garantir que o cliente está conectado
        if not db_client.client:
            db_client.connect()
        
        self.client: AsyncIOMotorClient = db_client.client
        self.database: AsyncIOMotorDatabase = db_client.db
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        try:
            product_model = ProductModel(**body.model_dump())
            await self.collection.insert_one(product_model.model_dump())
            return ProductOut(**product_model.model_dump())
        except PyMongoError as e:
            raise BaseException(message=f"Error inserting product: {str(e)}")

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductOut(**result)

    async def query(self, min_price: Optional[Decimal] = None, max_price: Optional[Decimal] = None) -> List[ProductOut]:
        query_filter = {}
        
        # Adicionar filtro de preço se fornecido
        if min_price is not None and max_price is not None:
            query_filter["price"] = {"$gt": float(min_price), "$lt": float(max_price)}
        elif min_price is not None:
            query_filter["price"] = {"$gt": float(min_price)}
        elif max_price is not None:
            query_filter["price"] = {"$lt": float(max_price)}
        
        return [ProductOut(**item) async for item in self.collection.find(query_filter)]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        # Adicionar updated_at automaticamente
        update_data = body.model_dump(exclude_none=True)
        update_data["updated_at"] = datetime.utcnow()
        
        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": update_data},
            return_document=pymongo.ReturnDocument.AFTER,
        )
        
        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")
        
        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        result = await self.collection.delete_one({"id": id})

        return True if result.deleted_count > 0 else False


product_usecase = ProductUsecase()