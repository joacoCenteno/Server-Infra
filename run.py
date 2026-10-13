import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    ip_address = os.environ.get('IP_ADDRESS', '127.0.0.1')
    # debug=True para recarga automática en desarrollo
    print("\n" + "=" * 60)
    print(">>> API To-Do List Iniciada")
    print(f"[*] Interfaz y Documentacion: http://{ip_address}:{port}/")
    print(f"[*] Endpoint Tareas:           http://{ip_address}:{port}/api/tasks")
    print(f"[*] Endpoint Health Check:     http://{ip_address}:{port}/api/health")
    print("=" * 60 + "\n")
    app.run(host=ip_address, port=port, debug=True)
