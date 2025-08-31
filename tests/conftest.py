import pytest
import os
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configura variáveis de ambiente necessárias para os testes
os.environ['DATABASE_URL'] = os.getenv('DATABASE_URL', 'mongodb://localhost:27017/test_db')

# Mock das dependências do MongoDB antes de importar qualquer coisa
@pytest.fixture(scope="session", autouse=True)
def mock_db_dependencies():
    """Mock das dependências do MongoDB"""
    import sys
    
    # Mock do motor
    mock_motor = MagicMock()
    mock_motor.AsyncIOMotorClient = MagicMock()
    sys.modules['motor.motor_asyncio'] = mock_motor
    
    # Mock do pymongo
    mock_pymongo = MagicMock()
    mock_pymongo.ReturnDocument = MagicMock()
    mock_pymongo.errors = MagicMock()
    sys.modules['pymongo'] = mock_pymongo
    
    yield

# Fixture para mock da coleção
@pytest.fixture
def mock_collection():
    return AsyncMock()

# Fixture para o usecase com mock
@pytest.fixture
def product_usecase(mock_collection):
    """ProductUsecase com coleção mockada"""
    # Mock do db_client para evitar conexões reais
    with patch('store.usecases.product.db_client', MagicMock()):
        from store.usecases.product import ProductUsecase
        
        usecase = ProductUsecase()
        usecase.collection = mock_collection
        return usecase

# Configuração para testes assíncronos
@pytest.fixture(scope="session")
def event_loop():
    """Cria uma event loop para testes assíncronos"""
    policy = asyncio.WindowsSelectorEventLoopPolicy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

# Fixture para mock das settings
@pytest.fixture(autouse=True)
def mock_settings():
    """Mock das settings para evitar validation errors"""
    with patch('store.core.config.settings') as mock_settings:
        mock_settings.DATABASE_URL = "mongodb://localhost:27017/test_db"
        mock_settings.PROJECT_NAME = "Store API Test"
        mock_settings.ROOT_PATH = "/"
        yield mock_settings