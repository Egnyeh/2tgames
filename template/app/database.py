from app.models import UserDb

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