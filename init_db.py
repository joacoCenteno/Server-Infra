import os
import sys
from dotenv import load_dotenv

load_dotenv()

def init_postgres():
    use_sqlite = os.getenv('USE_SQLITE', 'false').lower() in ('true', '1', 'yes')

    if use_sqlite:
        print("[*] Modo SQLite activado en .env.")
        from app import create_app
        from app.models import db
        app = create_app()
        with app.app_context():
            db.create_all()
        print("[OK] Base de datos SQLite inicializada exitosamente.")
        return True

    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'postgres')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    target_db = os.getenv('DB_NAME', 'todo_db')

    print(f"[*] Conectando a PostgreSQL en {db_host}:{db_port} con usuario '{db_user}'...")

    try:
        # Conectar a la base de datos predeterminada 'postgres'
        conn = psycopg2.connect(
            dbname='postgres',
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Verificar si la base de datos ya existe
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{target_db}';")
        exists = cur.fetchone()

        if not exists:
            cur.execute(f'CREATE DATABASE "{target_db}";')
            print(f"[OK] Base de datos '{target_db}' creada con exito.")
        else:
            print(f"[INFO] La base de datos '{target_db}' ya existe.")

        cur.close()
        conn.close()

        # Sincronizar las tablas
        print("[*] Sincronizando tablas en la base de datos...")
        from app import create_app
        from app.models import db

        app = create_app()
        with app.app_context():
            db.create_all()
        print(f"[OK] Tablas listas y sincronizadas en PostgreSQL ({target_db}).")
        return True

    except psycopg2.OperationalError as e:
        print("\n[ERROR] No se pudo conectar a PostgreSQL:")
        print("  -> Asegurate de que el servicio PostgreSQL este corriendo.")
        print("  -> Verifica que DB_PASSWORD en el archivo .env coincida con la contrasenia de tu PostgreSQL.")
        print("  -> Detalle del error:")
        try:
            print(f"     {e}")
        except Exception:
            print("     Fallo de autenticacion de contrasenia o host inaccesible.")
        return False
    except Exception as e:
        print(f"\n[ERROR] Ocurrio un error inesperado: {e}")
        return False

if __name__ == '__main__':
    success = init_postgres()
    if not success:
        sys.exit(1)
