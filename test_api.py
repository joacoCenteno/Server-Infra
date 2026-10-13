import unittest
from app import create_app
from app.models import db, Task

class TestTodoApi(unittest.TestCase):
    def setUp(self):
        # Configurar app para pruebas con base de datos SQLite en memoria
        self.app = create_app(config_override={
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_health_check(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')

    def test_create_task(self):
        payload = {
            'title': 'Comprar cafe',
            'description': 'Cafe en grano de especialidad'
        }
        response = self.client.post('/api/tasks', json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('task', data)
        self.assertEqual(data['task']['title'], 'Comprar cafe')
        self.assertFalse(data['task']['completed'])

    def test_create_task_validation_error(self):
        # Título vacío o no enviado
        response = self.client.post('/api/tasks', json={'title': '   '})
        self.assertEqual(response.status_code, 400)

    def test_list_tasks(self):
        # Crear 2 tareas
        self.client.post('/api/tasks', json={'title': 'Tarea 1'})
        self.client.post('/api/tasks', json={'title': 'Tarea 2'})

        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['count'], 2)
        self.assertEqual(len(data['tasks']), 2)

    def test_get_single_task(self):
        res = self.client.post('/api/tasks', json={'title': 'Tarea individual'})
        task_id = res.get_json()['task']['id']

        response = self.client.get(f'/api/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['task']['id'], task_id)

    def test_update_task(self):
        res = self.client.post('/api/tasks', json={'title': 'Titulo viejo', 'description': 'Desc vieja'})
        task_id = res.get_json()['task']['id']

        # Editar
        payload = {
            'title': 'Titulo nuevo',
            'description': 'Desc actualizada'
        }
        response = self.client.put(f'/api/tasks/{task_id}', json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['task']['title'], 'Titulo nuevo')
        self.assertEqual(data['task']['description'], 'Desc actualizada')

    def test_complete_task(self):
        res = self.client.post('/api/tasks', json={'title': 'Tarea por completar'})
        task_id = res.get_json()['task']['id']

        # Marcar como completada / terminada
        response = self.client.patch(f'/api/tasks/{task_id}/complete')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['task']['completed'])

        # Desmarcar (marcar como no completada)
        response_undo = self.client.patch(f'/api/tasks/{task_id}/complete', json={'completed': False})
        self.assertEqual(response_undo.status_code, 200)
        data_undo = response_undo.get_json()
        self.assertFalse(data_undo['task']['completed'])

    def test_delete_task(self):
        res = self.client.post('/api/tasks', json={'title': 'Tarea a eliminar'})
        task_id = res.get_json()['task']['id']

        # Eliminar
        response = self.client.delete(f'/api/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)

        # Verificar que ya no existe
        res_get = self.client.get(f'/api/tasks/{task_id}')
        self.assertEqual(res_get.status_code, 404)

if __name__ == '__main__':
    unittest.main()
