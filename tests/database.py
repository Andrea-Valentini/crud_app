from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import Settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{Settings.DB_USER}:{Settings.DB_PASSWORD}@{Settings.DB_HOST_NAME}/{Settings.DB_NAME}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
