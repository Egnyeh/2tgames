from typing import Iterable
import mariadb
from app.auth.auth import get_hash_password
from app.models import (
    AdminDb,
    ClienteDb,
    ProductCreate,
    ProductUpdate,
    UserCreate,
    UserOut,
    ProductOut,
)


db_config = {
    "host": "myapidb",
    "port": 3306,
    "user": "myapi",
    "password": "myapi",
    "database": "myapi",
}

# ------------- USUARY FUNCTIONS --------------


def insert_user(user: UserCreate) -> UserOut:  # ✅ Cambiado de int a UserOut
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            hashed_password = get_hash_password(user.password)
            # Consultas preparadas para evitar SQL Injection
            sql_usuario = "insert into usuario (email, nombre, password, tipo) values (?, ?, ?, ?)"
            values = (user.email, user.nombre, hashed_password, user.tipo)
            cursor.execute(sql_usuario, values)
            user_id = cursor.lastrowid

            if user.tipo == "cliente":
                sql_cliente = "insert into cliente (id, username) values (?, ?)"
                values_cliente = (user_id, user.username)
                cursor.execute(sql_cliente, values_cliente)
            elif user.tipo == "admin":
                sql_admin = "insert into admin (id, username, fecha_alta) values (?, ?, CURDATE())"
                values_admin = (user_id, user.username)
                cursor.execute(sql_admin, values_admin)

            conn.commit()

            return UserOut(
                id=user_id,
                email=user.email,
                username=user.username,
                name=user.nombre,
                tipo=user.tipo,
            )


def get_user_by_username(username: str) -> ClienteDb | AdminDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
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
                    username=row[5],
                )

            sql_admin = """
                SELECT u.id, u.email, u.nombre, u.password, u.tipo, a.username, a.fecha_alta
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
                    fecha_alta=row[6],
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
                    username=row[5],
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
                    fecha_alta=row[6],
                )

            return None


# ------------- PRODUCT FUNCTIONS --------------


def get_all_products() -> list[ProductOut]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, nombre, descripcion, categoria, precio_unitario, stock, disponibilidad FROM producto"
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
                        stock=row[5],
                        disponibilidad=row[6],
                    )
                )
            return products


def get_product_by_id(product_id: int) -> ProductOut | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, nombre, descripcion, categoria, precio_unitario, stock, disponibilidad FROM producto WHERE id = ?"
            cursor.execute(sql, (product_id,))
            row = cursor.fetchone()

            if row:
                return ProductOut(
                    id=row[0],
                    nombre=row[1],
                    descripcion=row[2],
                    categoria=row[3],
                    precio_unitario=row[4],
                    stock=row[5],
                    disponibilidad=row[6],
                )
            return None


def search_products_by_name(nombre: str) -> list[ProductOut]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = """
                SELECT id, nombre, descripcion, categoria, precio_unitario, stock, disponibilidad 
                FROM producto 
                WHERE nombre LIKE ?
            """
            # El % permite buscar coincidencias parciales
            cursor.execute(sql, (f"%{nombre}%",))
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
                        stock=row[5],
                        disponibilidad=row[6],
                    )
                )
            return products


def insert_product(product: ProductCreate) -> int:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO producto (nombre, descripcion, categoria, precio_unitario, stock, disponibilidad)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            values = (
                product.nombre,
                product.descripcion,
                product.categoria,
                product.precio_unitario,
                product.stock,
                product.disponibilidad,
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
            if product.disponibilidad is not None:
                campos.append("disponibilidad = ?")
                valores.append(product.disponibilidad)

            if not campos:
                return False  # Si no hay nada que actualizar

            valores.append(product_id)
            sql = f"UPDATE producto SET {', '.join(campos)} WHERE id = ?"
            cursor.execute(sql, valores)  # ✅ AÑADIDO: Faltaba ejecutar el SQL
            conn.commit()
            return (
                cursor.rowcount > 0
            )  # Devuelve true si actualizamos al menos una fila


def delete_product(product_id: int) -> bool:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "DELETE FROM producto WHERE id = ?"
            cursor.execute(sql, (product_id,))
            conn.commit()
            return cursor.rowcount > 0  # Devuelve true si borramos al menos una fila


# ------------- ORDER FUNCTIONS --------------


def add_product_to_order(
    numero_pedido: int, id_producto: int, cantidad: int, precio: float | None = None
) -> int | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            # Comprobar si el pedido existe
            cursor.execute(
                "SELECT numero_pedido FROM pedido WHERE numero_pedido = ? LIMIT 1", 
                (numero_pedido,),
            )
            if cursor.fetchone() is None:
                return None

            # Comprobar si el producto existe
            cursor.execute(
                "SELECT precio_unitario FROM producto WHERE id = ? LIMIT 1",
                (id_producto,),
            )
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


def create_order_with_items(order: dict, items: Iterable[dict]) -> int | None:
    try:
        with mariadb.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                sql_pedido = """
                    INSERT INTO pedido(id_usuario, fecha_pedido, precio_total, estado)
                    VALUES (?, ?, ?, ?)
                """  

                values_order = (
                    order["id_usuario"],
                    order["fecha_pedido"],
                    order["precio_total"],
                    order["estado"],
                )
                cursor.execute(sql_pedido, values_order)
                numero_pedido = cursor.lastrowid

                # Insertar productos
                if items:
                    sql_item = """
                        INSERT INTO linea_pedido (numero_pedido, id_producto, precio, cantidad)
                        VALUES (?, ?, ?, ?)
                    """
                    for item in items:
                        id_producto = item["id_producto"]
                        cantidad = item["cantidad"]
                        precio = item.get("precio")
                        cursor.execute(
                            sql_item, (numero_pedido, id_producto, precio, cantidad)
                        )

                conn.commit()
                return numero_pedido
    except mariadb.Error as e:
        print(f"Error al crear pedido: {e}")
        return None


def get_orders_by_user(user_id: int) -> list[dict]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = """
                SELECT p.numero_pedido, p.id_usuario, p.fecha_pedido, p.precio_total, p.estado
                FROM pedido p
                WHERE p.id_usuario = ?
            """  
            cursor.execute(sql, (user_id,))
            rows = cursor.fetchall()

            orders = []
            for row in rows:
                orders.append(
                    {
                        "numero_pedido": row[0],
                        "id_usuario": row[1],
                        "fecha_pedido": row[2],  
                        "precio_total": row[3],
                        "estado": row[4],
                    }
                )
            return orders

def get_order_lines(numero_pedido: int) -> list[dict]:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = """
                SELECT id, numero_pedido, id_producto, precio, cantidad
                FROM linea_pedido
                WHERE numero_pedido = ?
            """
            cursor.execute(sql, (numero_pedido,))
            rows = cursor.fetchall()
            
            lineas = []
            for row in rows:
                lineas.append({
                    "id": row[0],
                    "numero_pedido": row[1],
                    "id_producto": row[2],
                    "precio": row[3],
                    "cantidad": row[4]
                })
            return lineas