import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",         # ← Vacía si no usás contraseña
        database="tienda"
    )
