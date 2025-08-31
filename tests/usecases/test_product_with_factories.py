import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal
from tests.factories import product_data, products_data


@pytest.mark.asyncio
async def test_create_product_with_factory_data():
    """Testa criação de produto usando dados da factory"""
    # Mock das settings primeiro
    with patch('store.core.config.settings') as mock_settings:
        mock_settings.DATABASE_URL = "mongodb://localhost:27017/test_db"
        
        # Mock do db_client antes de importar
        with patch('store.db.mongo.db_client', MagicMock()):
            # Agora importar o usecase
            from store.usecases.product import ProductUsecase
            from store.schemas.product import ProductIn
            
            usecase = ProductUsecase()
            usecase.collection = AsyncMock()
            
            # Usar dados da factory
            factory_data = product_data()
            product_data_schema = ProductIn(**factory_data)
            
            usecase.collection.insert_one = AsyncMock()
            
            result = await usecase.create(body=product_data_schema)
            
            assert result.name == "Iphone 14 Pro Max"
            assert result.quantity == 10
            assert result.price == Decimal("8.500")


@pytest.mark.asyncio
async def test_query_with_price_filter_factory_data():
    """Testa query com filtro de preço usando dados da factory"""
    with patch('store.core.config.settings') as mock_settings:
        mock_settings.DATABASE_URL = "mongodb://localhost:27017/test_db"
        
        with patch('store.db.mongo.db_client', MagicMock()):
            from store.usecases.product import ProductUsecase
            
            usecase = ProductUsecase()
            usecase.collection = AsyncMock()
            
            # Mock dos produtos da factory (convertendo para dict com preço como Decimal)
            factory_products = []
            for product in products_data():
                product_dict = product.copy()
                product_dict["price"] = Decimal(product["price"])
                product_dict["id"] = "test-id"
                product_dict["created_at"] = "2023-01-01T00:00:00"
                product_dict["updated_at"] = "2023-01-01T00:00:00"
                factory_products.append(product_dict)
            
            usecase.collection.find = AsyncMock(return_value=factory_products)
            
            # Testar filtro de preço (5000 < price < 8000)
            result = await usecase.query(
                min_price=Decimal("5000"),
                max_price=Decimal("8000")
            )
            
            # Deve retornar 2 produtos: Iphone 12 (5.500) e Iphone 13 (6.500)
            assert len(result) == 2
            prices = [product.price for product in result]
            assert Decimal("5.500") in prices
            assert Decimal("6.500") in prices