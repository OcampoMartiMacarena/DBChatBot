from database.mysql_product_repository import fetch_all_products, fetch_product_by_name
from HService.domain.dialogue_manager import Product

def get_all_products() -> list[Product]:
    return fetch_all_products()

def get_product_by_name(name: str) -> Product | None:
    return fetch_product_by_name(name)