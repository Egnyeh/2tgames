from typing import Iterable
import mariadb
from app.auth.auth import get_hash_password
from app.models import (AdminDb, ClienteDb, ProductCreate, ProductUpdate, UserCreate, UserDb, ProductOut)


db_config = {
    "host": "myapidb",
    "port": 3306,
    "user": "myapi",
    "password": "myapi",
    "database": "myapi"
}

# ------------- USUARY FUNCTIONS --------------

def insert_user(user: UserCreate) -> int:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            hashed_password = get_hash_password(user.password)
            #Consultas preparadas para evitar SQL Injection
            sql_usuario = "insert into usuario (email, nombre, password, tipo) values (?, ?, ?, ?)"
            values = (user.email, user.nombre, hashed_password, user.tipo)
            cursor.execute(
                sql_usuario, values
            )
            user_id = cursor.lastrowid
        
            if user.tipo == "cliente":
                sql_cliente = "insert into cliente (id, username) values (?, ?)"
                values_cliente = (user_id, user.username)
                cursor.execute(
                    sql_cliente, values_cliente
                )
            elif user.tipo == "admin":
                sql_admin = "insert into admin (id, username, fecha_alta) values (?, ?, CURDATE())"
                values_admin = (user_id, user.username)
                cursor.execute(
                    sql_admin, values_admin
                )
            
            conn.commit()
            return cursor.lastrowid


def get_user_by_username(username: str) -> ClienteDb | AdminDb | None:
    with mariadb.connect(**db_config) as conn:
        sql_cliente = """ 
            SELECT u.id, u.email, u.nombre, u.password, u.tipo, c.username
            FROM usuario u
            INNER JOIN cliente c ON u.id = c.id
            WHERE c.username = ?
        """
        cursor.execute(sql_cliente, (username,))
        row = cursor.fetchone()

        if row: 
            return ClienteDb(
                id=row[0],
                email=row[1],
                nombre=row[2],
                password=row[3],
                tipo=row[4],
                username=row[5]
            )
        
        sql_admin = """
            SELECT u.id, u.email, u.nombre, u.passwor, u.tipo, a.username, a.fecha_alta
            FROM usuario u
            INNER JOIN admin a ON u.id = a.id
            WHERE a.username = ?
            """
        cursor.execute(sql_admin, (username,))
        row = cursor.fetchone()

        if row:
            return AdminDb(
                id=row[0],
                email=row[1],
                nombre=row[2],
                password=row[3],
                tipo=row[4],
                username=row[5],
                fecha_alta=row[6]
            )
        
        return None


def get_user_by_id(user_id: int) -> ClienteDb | AdminDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql_cliente = """ 
                SELECT u.id, u.email, u.nombre, u.password, u.tipo, c.username
                FROM usuario u
                INNER JOIN cliente c ON u.id = c.id
                WHERE u.id = ?
            """
            cursor.execute(sql_cliente, (user_id,))
            row = cursor.fetchone()

            if row: 
                return ClienteDb(
                    id=row[0],
                    email=row[1],
                    nombre=row[2],
                    password=row[3],
                    tipo=row[4],
                    username=row[5]
                )
            
            sql_admin = """
                SELECT u.id, u.email, u.nombre, u.password, u.tipo, a.username, a.fecha_alta
                FROM usuario u
                INNER JOIN admin a ON u.id = a.id
                WHERE u.id = ?
                """
            cursor.execute(sql_admin, (user_id,))
            row = cursor.fetchone()

            if row:
                return AdminDb(
                    id=row[0],
                    email=row[1],
                    nombre=row[2],
                    password=row[3],
                    tipo=row[4],
                    username=row[5],
                    fecha_alta=row[6]
                )
            
            return None


# ------------- PRODUCT FUNCTIONS --------------

def get_all_products() -> list[ProductOut]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, nombre, descripcion, categoria, precio_unitario, stock FROM producto"
            cursor.execute(sql)
            rows = cursor.fetchall()

            products = []
            for row in rows:
                products.append(
                    ProductOut(
                        id=row[0],
                        nombre=row[1],
                        descripcion=row[2],
                        categoria=row[3],
                        precio_unitario=row[4],
                        stock=row[5]
                    )
                )
            return products


def get_product_by_id(product_id: int) -> ProductOut | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, nombre, descripcion, categoria, precio_unitario, stock FROM producto WHERE id = ?"
            cursor.execute(sql, (product_id,))
            row = cursor.fetchone()
            
            if row:
                return ProductOut(
                    id=row[0],
                    nombre=row[1],
                    descripcion=row[2],
                    categoria=row[3],
                    precio_unitario=row[4],
                    stock=row[5]
                )
            return None


def insert_product(product: ProductCreate) -> int:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO producto (nombre, descripcion, categoria, precio_unitario, stock)
                VALUES (?, ?, ?, ?, ?)
            """
            values = (
                product.nombre,
                product.descripcion,
                product.categoria,
                product.precio_unitario,
                product.stock
            )
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid


def update_product(product_id: int, product: ProductUpdate) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            campos = []
            valores = []
        
            if product.nombre is not None:
                campos.append("nombre = ?")
                valores.append(product.nombre)
            if product.descripcion is not None:
                campos.append("descripcion = ?")
                valores.append(product.descripcion)
            if product.categoria is not None:
                campos.append("categoria = ?")
                valores.append(product.categoria)
            if product.precio_unitario is not None:
                campos.append("precio_unitario = ?")
                valores.append(product.precio_unitario)
            if product.stock is not None:
                campos.append("stock = ?")
                valores.append(product.stock)
            
            if not campos:
                return False  #Si no hay nada que actualizar
            
            valores.append(product_id)
            sql= f"UPDATE producto SET {', '.join(campos)} WHERE id = ?"
            conn.commit()
            return cursor.rowcount > 0 #Devuelve true si actualizamos al menos una fila

def delete_product(product_id: int) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "DELETE FROM producto WHERE id = ?"
            cursor.execute(sql, (product_id,))
            conn.commit()
            return cursor.rowcount > 0 #Devuelve true si borramos al menos una fila


# ------------- ORDER FUNCTIONS --------------

def add_product_to_order(numero_pedido: int, id_producto: int,  cantidad: int, precio: float | None = None) -> int | None:
    try:

        # Comprobar si el pedido existe
        with mariadb.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT FROM pedido WHERE numero_pedido = ? LIMIT 1", (numero_pedido,))
                if cursor.fetchone() is None:
                    return None
                
        # Comprobar si el producto existe
        cursor.execute("SELECT precio_unitario FROM producto WHERE id = ? LIMIT 1", (id_producto,))
        result = cursor.fetchone()
        if result is None:
            return None
        
        if precio is None:
            precio = result[0] 

        sql = """
            INSERT INTO linea_pedido (numero_pedido, id_producto, precio, cantidad)
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(sql, (numero_pedido, id_producto, precio, cantidad))  
        conn.commit()
        return cursor.lastrowid
    except mariadb.Error as e:
        print("Error al cargar el producto en pedido, ", e)
        return None

def create_order_with_items(pedido:dict, items: Iterable[dict]) -> int | None:
        try:
            conn = mariadb.connect(**db_config)
            try: 
                cursor = conn.cursor()

                sql_pedido = """
                    INSERT INTO pedido(id_usuario, fecha_peido, precio_total, estado)
                    VALUES (?, ?, ?, ?)
                """
                values_pedido =(
                    pedido['id_usuario'],
                    pedido['fecha_pedido'],
                    pedido['precio_total'],
                    pedido['estado']
                )
                cursor.execute(sql_pedido, values_pedido)
                numero_pedido = cursor.lastrowid
                
                # Insertar productos
                sql_item = """
                    INSERT INTO linea_pedido (numero_pedido, id_producto, precio, cantidad)
                    VALUES (?, ?, ?, ?)
                """
                item_values = []
                for item in items:
                    id_producto = item["id_producto"]
                    cantidad = item["cantidad"]
                    precio = item.get("precio")
                    item_values.append((numero_pedido, id_producto, precio, cantidad))

                if item_values:
                    cursor.execute(sql_item, item_values)
                conn.commit()
                return numero_pedido
            except Exception as e:
                conn.rollback()
                print("Error al crear el pedido con items: ", e)
                return None
            finally:
                cursor.close()
                conn.close()
        except mariadb.Error as e:
            print("Error de conexión a la base de datos: ", e)
            return None