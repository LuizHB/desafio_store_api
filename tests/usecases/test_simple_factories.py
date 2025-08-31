import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal
from tests.factories import product_data

# Mock do pymongo antes de importar anything
with patch.dict('sys.modules', {
    'pymongo': MagicMock(),
    'pymongo.errors': MagicMock(),
}):
    # Mock das settings
    with patch('store.core.config.settings') as mock_settings:
        mock_settings.DATABASE_URL = "mongodb://localhost:27017/test_db"
        
        # Mock do db_client
        with patch('store.db.mongo.db_client', MagicMock()):
            # Agora importar
            from store.usecases.product import ProductUsecase
            from store.schemas.product import ProductIn


@pytest.mark.asyncio
async def test_simple_create_with_factory():
    """Teste simples de criação com factory"""
    # Criar usecase
    usecase = ProductUsecase()
    usecase.collection = AsyncMock()
    
    # Dados da factory
    factory_data = product_data()
    product_schema = ProductIn(**factory_data)
    
    # Mock do insert
    usecase.collection.insert_one = AsyncMock()
    
    # Executar
    result = await usecase.create(body=product_schema)
    
    # Verificar
    assert result.name == "Iphone 14 Pro Max"
    assert result.quantity == 10
    assert result.price == Decimal("8.500")