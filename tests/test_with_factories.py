from decimal import Decimal

def test_product_factory():
    """Testa a factory de produto único"""
    from tests.factories import product_data
    
    data = product_data()
    
    assert data["name"] == "Iphone 14 Pro Max"
    assert data["quantity"] == 10
    assert data["price"] == "8.500"
    assert data["status"] == True


def test_products_factory():
    """Testa a factory de múltiplos produtos"""
    from tests.factories import products_data
    
    data = products_data()
    
    assert len(data) == 4
    assert data[0]["name"] == "Iphone 11 Pro Max"
    assert data[3]["price"] == "10.500"


def test_factories_with_schemas():
    """Testa as factories com os schemas"""
    from tests.factories import product_data, products_data
    from store.schemas.product import ProductIn
    
    # Testa produto único
    product_dict = product_data()
    product_schema = ProductIn(**product_dict)
    
    assert product_schema.name == "Iphone 14 Pro Max"
    assert product_schema.quantity == 10
    assert product_schema.price == Decimal("8.500")
    
    # Testa múltiplos produtos
    products_list = products_data()
    for product_dict in products_list:
        product_schema = ProductIn(**product_dict)
        assert product_schema.name.startswith("Iphone")
        assert product_schema.quantity > 0