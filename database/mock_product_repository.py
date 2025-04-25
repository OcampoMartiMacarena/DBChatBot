from HService.domain.models import Product

# Esta lista simula los datos como si vinieran de una base de datos real
MOCK_PRODUCTS = [
    Product(id=1, name="Notebook Lenovo", description="Notebook con 8GB RAM y SSD 256GB", price=250000, in_stock=True, discount_percent=10),
    Product(id=2, name="Mouse Gamer RGB", description="Mouse con luces y sensor óptico", price=8000, in_stock=True, discount_percent=5),
    Product(id=3, name="Auriculares Bluetooth", description="Inalámbricos con cancelación de ruido", price=15000, in_stock=False, discount_percent=0),
    Product(id=4, name="Teclado Mecánico", description="Switches rojos y retroiluminación RGB", price=12000, in_stock=True, discount_percent=15),
]

def get_all_mock_products():
    return MOCK_PRODUCTS

def get_mock_product_by_name(name: str):
    return next((p for p in MOCK_PRODUCTS if name.lower() in p.name.lower()), None)