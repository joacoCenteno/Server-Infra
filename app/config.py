import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'todo-secret-key-super-secure')

    # Parámetros de PostgreSQL
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'todo_db')

    # URL de conexión PostgreSQL explícita con el driver psycopg2
    DEFAULT_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', DEFAULT_DATABASE_URL)

    # Opción opcional para desarrollo rápido local con SQLite si aún no configuró la contraseña de Postgres
    if os.getenv('USE_SQLITE', 'false').lower() in ('true', '1', 'yes'):
        SQLALCHEMY_DATABASE_URI = 'sqlite:///todo.db'

    # Normalizar URLs para usar siempre psycopg2
    if SQLALCHEMY_DATABASE_URI:
        if SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql+psycopg2://', 1)
        elif SQLALCHEMY_DATABASE_URI.startswith('postgresql://') and not SQLALCHEMY_DATABASE_URI.startswith('postgresql+'):
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgresql://', 'postgresql+psycopg2://', 1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
