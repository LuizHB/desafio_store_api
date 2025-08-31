import asyncio
from store.db.mongo import db_client  # CORRIGIDO: db_client em vez de mongodb

async def test_connection():
    try:
        db_client.connect()
        print("✅ MongoDB connected successfully")
        print(f"Database: {db_client.db.name}")
        
        # Testar listar coleções
        collections = await db_client.db.list_collection_names()
        print(f"Collections: {collections}")
        
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_connection())