import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.backend.config import get_settings
from src.backend.infrastracture.db.sqlalchemy.user.models import UserModel
from src.backend.infrastracture.security.argon2.hasher import Argon2Hasher

settings = get_settings()

def create_user():
    engine= create_engine(f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_NAME}")
    Session = sessionmaker(bind=engine)
    user = UserModel(
        id=uuid.uuid4(),
        email="admin@example.com",
        first_name="admin",
        last_name="user",
        role="admin",
        username="admin",
        password_hash=Argon2Hasher().hash("Admin@1234")
    )
    with Session() as session:
        session.add(user)
        session.commit()
        session.close()

create_user()