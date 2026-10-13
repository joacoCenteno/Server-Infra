import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # debug=True para recarga automática en desarrollo
    print("\n" + "=" * 60)
    print(">>> API To-Do List Iniciada")
    print(f"[*] Interfaz y Documentacion: http://127.0.0.1:{port}/")
    print(f"[*] Endpoint Tareas:           http://127.0.0.1:{port}/api/tasks")
    print(f"[*] Endpoint Health Check:     http://127.0.0.1:{port}/api/health")
    print("=" * 60 + "\n")
    app.run(host='127.0.0.1', port=port, debug=True)
