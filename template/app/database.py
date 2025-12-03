import mariadb

from app.models import UserDb


db_config = {
    "host": "myapidb",
    "puerto": "33006",
    "user": "myapi",
    "password": "myapi",
    "database": "myapi"
}


def insert_user(user: UserDb) -> int:
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            #Consultas preparadas para evitar SQL Injection
            sql = "insert into users (name, username, password) values (?, ?, ?)"
            values = (user.name, user.username, user.password)
            cursor.execute(
                sql, values
            )
            return cursor.lastrowid


def get_user_by_username(username: str) -> UserDb | None:
    return None


users: list[UserDb] = [
    UserDb(
        id=1, 
        name="Alice", 
        username="alice", 
        password="$2b$12$9kYeU2vjcgea2kJdJ7KgNO5pnTFOXOCSzTWTHTRvfp1d13R6KYCLq"
        ),
    UserDb(
        id=2,
        name="Bob", 
        username="bob", 
        password="$2b$12$EuCDdv7QdBhQK5fFT.c/nugU7WgiDsV07.rz1mxmHiiqS1tTGtLYe"
        ),
]