from motor.motor_asyncio import AsyncIOMotorClient
from store.core.config import settings
from bson import Binary
import uuid


class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None
    
    def connect(self):
        # Configurar UUID representation
        self.client = AsyncIOMotorClient(
            settings.DATABASE_URL,
            uuidRepresentation='standard'  # ADICIONAR ESTA LINHA
        )
        self.db = self.client.get_database()
    
    def close(self):
        if self.client:
            self.client.close()


# A instância deve ser criada aqui
db_client = MongoDB()