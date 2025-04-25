from database.db_connection import get_db_connection
from HService.domain.models import Product


def fetch_all_products() -> list[Product]:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [Product(**row) for row in rows]

def fetch_product_by_name(name: str) -> Product | None:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos WHERE name = %s", (name,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return Product(**row) if row else None