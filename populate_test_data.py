from tests.factories import products_data
from store.schemas.product import ProductIn
from store.usecases.product import product_usecase
import asyncio
import traceback

async def populate_data():
    products = products_data()
    for product_dict in products:
        product = ProductIn(**product_dict)
        try:
            result = await product_usecase.create(product)
            print(f"✅ Created: {result.name} - R$ {result.price}")
        except Exception as e:
            print(f"❌ Error creating {product_dict['name']}: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            traceback.print_exc()  # Mostra o traceback completo
            print("---")

if __name__ == "__main__":
    print("Populating test data...")
    asyncio.run(populate_data())