def test_import_step_by_step():
    """Testa importação passo a passo"""
    # 1. Primeiro import básico
    from decimal import Decimal
    assert Decimal is not None
    
    # 2. Import das exceções
    from store.core.exceptions import NotFoundException, BaseException
    assert NotFoundException is not None
    assert BaseException is not None
    
    # 3. Import dos schemas
    from store.schemas.product import ProductIn, ProductUpdate
    assert ProductIn is not None
    assert ProductUpdate is not None
    
    print("Todos os imports funcionaram!")