from flask import Blueprint, request, jsonify, render_template
from app.models import db, Task

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def home():
    """Página de inicio con documentación interactiva para probar la API en el navegador"""
    return render_template('index.html')


@api_bp.route('/api/health', methods=['GET'])
def health_check():
    """Verifica el estado de la API y la conexión a la base de datos"""
    try:
        db.session.execute(db.text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'message': 'API y conexión a PostgreSQL funcionando correctamente.'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': 'No se pudo conectar a PostgreSQL. Verifica el usuario y contraseña en el archivo .env',
            'detail': str(e) if str(e) else 'Fallo de autenticación o base de datos inexistente.'
        }), 503


@api_bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    """
    Listar tareas con soporte de filtros opcionales.
    Query params:
      - completed: true|false (filtrar por terminadas o pendientes)
      - search: texto a buscar en título o descripción
      - order: desc|asc (orden cronológico, por defecto desc)
    """
    try:
        query = Task.query

        # Filtro por estado
        completed_param = request.args.get('completed')
        if completed_param is not None:
            if completed_param.lower() in ['true', '1', 'yes']:
                query = query.filter_by(completed=True)
            elif completed_param.lower() in ['false', '0', 'no']:
                query = query.filter_by(completed=False)

        # Filtro de búsqueda
        search_param = request.args.get('search')
        if search_param:
            search_pattern = f"%{search_param.strip()}%"
            query = query.filter(
                (Task.title.ilike(search_pattern)) | 
                (Task.description.ilike(search_pattern))
            )

        # Orden
        order_param = request.args.get('order', 'desc').lower()
        if order_param == 'asc':
            query = query.order_by(Task.created_at.asc())
        else:
            query = query.order_by(Task.created_at.desc())

        tasks = query.all()
        return jsonify({
            'count': len(tasks),
            'tasks': [task.to_dict() for task in tasks]
        }), 200

    except Exception as e:
        return jsonify({'error': 'Error al obtener las tareas', 'detail': str(e)}), 500


@api_bp.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Obtener el detalle de una tarea por su ID"""
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'error': f'No se encontró la tarea con ID {task_id}'}), 404
    return jsonify({'task': task.to_dict()}), 200


@api_bp.route('/api/tasks', methods=['POST'])
def create_task():
    """
    Crear una nueva tarea.
    Cuerpo esperado (JSON):
      {
        "title": "Título de la tarea" (requerido),
        "description": "Detalles adicionales" (opcional),
        "completed": false (opcional, por defecto false)
      }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'El cuerpo de la solicitud debe ser un JSON válido.'}), 400

    title = data.get('title')
    if not title or not str(title).strip():
        return jsonify({'error': 'El campo "title" es obligatorio y no puede estar vacío.'}), 400

    description = data.get('description', '')
    completed = bool(data.get('completed', False))

    try:
        new_task = Task(
            title=title.strip(),
            description=description.strip() if description else None,
            completed=completed
        )
        db.session.add(new_task)
        db.session.commit()

        return jsonify({
            'message': 'Tarea creada exitosamente.',
            'task': new_task.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al guardar la tarea en la base de datos', 'detail': str(e)}), 500


@api_bp.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Editar los campos de una tarea existente.
    Cuerpo esperado (JSON):
      {
        "title": "Nuevo título" (opcional si mantiene el anterior),
        "description": "Nueva descripción",
        "completed": true|false
      }
    """
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'error': f'No se encontró la tarea con ID {task_id}'}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'El cuerpo de la solicitud debe ser un JSON válido.'}), 400

    if 'title' in data:
        new_title = data['title']
        if not new_title or not str(new_title).strip():
            return jsonify({'error': 'El campo "title" no puede estar vacío.'}), 400
        task.title = str(new_title).strip()

    if 'description' in data:
        task.description = str(data['description']).strip() if data['description'] is not None else None

    if 'completed' in data:
        task.completed = bool(data['completed'])

    try:
        db.session.commit()
        return jsonify({
            'message': f'Tarea {task_id} actualizada exitosamente.',
            'task': task.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al actualizar la tarea', 'detail': str(e)}), 500


@api_bp.route('/api/tasks/<int:task_id>/complete', methods=['PATCH'])
def complete_task(task_id):
    """
    Terminar una tarea (marcar como completada).
    Si se envía {"completed": false} en el cuerpo opcional, permite desmarcarla.
    Por defecto, marca completed = True.
    """
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'error': f'No se encontró la tarea con ID {task_id}'}), 404

    data = request.get_json(silent=True) or {}
    # Si viene explícito lo toma, si no, lo marca como True (terminar)
    new_status = data.get('completed', True)
    task.completed = bool(new_status)

    try:
        db.session.commit()
        estado_texto = "terminada" if task.completed else "marcada como pendiente"
        return jsonify({
            'message': f'Tarea {task_id} {estado_texto} exitosamente.',
            'task': task.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al cambiar estado de la tarea', 'detail': str(e)}), 500


@api_bp.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Eliminar una tarea por su ID"""
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'error': f'No se encontró la tarea con ID {task_id}'}), 404

    try:
        deleted_data = task.to_dict()
        db.session.delete(task)
        db.session.commit()

        return jsonify({
            'message': f'Tarea {task_id} eliminada exitosamente.',
            'deleted_task': deleted_data
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error al eliminar la tarea', 'detail': str(e)}), 500
