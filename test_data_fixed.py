from tests.factories import products_data
from store.schemas.product import ProductIn
from store.usecases.product import product_usecase
import asyncio
import traceback

async def populate_data():
    print("Starting database population with UUID fix...")
    
    products = products_data()
    for product_dict in products:
        try:
            print(f"Creating product: {product_dict['name']}")
            product = ProductIn(**product_dict)
            
            # Forçar conversão de UUID para string
            product_data = product.model_dump()
            if 'id' in product_data:
                product_data['id'] = str(product_data['id'])
            
            result = await product_usecase.create(ProductIn(**product_data))
            print(f"✅ Created: {result.name} - R$ {result.price}")
            
        except Exception as e:
            print(f"❌ Error creating {product_dict['name']}: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            traceback.print_exc()
            print("---")

if __name__ == "__main__":
    print("Populating test data with UUID fix...")
    asyncio.run(populate_data())