from decimal import Decimal
from tests.factories import product_data, products_data

def test_factory_basic():
    """Teste básico das factories"""
    # Testar factory de produto único
    data = product_data()
    assert data["name"] == "Iphone 14 Pro Max"
    assert data["quantity"] == 10
    assert data["price"] == "8.500"
    
    # Testar factory de múltiplos produtos
    all_data = products_data()
    assert len(all_data) == 4
    assert all_data[0]["name"] == "Iphone 11 Pro Max"
    assert all_data[3]["price"] == "10.500"
    
    print("Factories funcionando corretamente!")


def test_factory_with_decimal():
    """Teste das factories com Decimal"""
    from store.schemas.product import ProductIn
    
    # Testar conversão para Decimal
    data = product_data()
    product = ProductIn(**data)
    
    assert product.price == Decimal("8.500")
    assert isinstance(product.price, Decimal)
    
    # Testar todos os produtos - CORRIGINDO O NOME DA VARIÁVEL
    all_products_data = products_data()  # Mudei o nome para evitar conflito
    for prod_data in all_products_data:  # Mudei o nome da variável do loop
        product = ProductIn(**prod_data)
        assert isinstance(product.price, Decimal)
    
    print("Conversão para Decimal funcionando!")