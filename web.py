from typing import Dict, List

from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

tasks = [
    {
        'id': 1,
        'title': "Aller à l'épicerie",
        'done': False
    },
    # {
    #     'id': 2,
    #     'title': "Étudier pour l'examen d'électromag",
    #     'done': False
    # }
]


class HelloResource(Resource):

    def get(self):
        return {'message': 'Bonjour le monde!'}


class TodosResource(Resource):

    def __init__(self, tasks):
        self.tasks = tasks

    def get(self):
        return tasks

    def post(self):
        ids = [task['id'] for task in self.tasks]
        new_id = max(ids) + 1

        if 'title' not in request.form:
            return {'error': 'Must provide "title" data'}, 400

        if 'done' in request.form:
            done = bool(request.form['done'])
        else:
            done = False

        self.tasks.append(
            {
                'id': new_id,
                'title': request.form['title'],
                'done': done
            }
        )

        return {'message': 'Tâche ajoutée'}, 201


class TodoResource(Resource):

    def __init__(self, tasks: List[Dict]):
        self.tasks = tasks

    def get(self, task_id):
        for task in self.tasks:
            if task['id'] == task_id:
                return task

        return {'error': f'Task ID "{task_id}" not found'}, 404

    def put(self, task_id):
        if 'done' in request.form:
            done = request.form['done']
        else:
            return {'error': 'Must provide "done" data, ex. {"done": true}'}, 400

        for task in self.tasks:
            if task['id'] == task_id:
                task['done'] = done
                return {'message': f'"{task_id}" updated'}, 200

        return {'error': f'Not Found: "{task_id}"'}, 404

    def delete(self, task_id):
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                del self.tasks[i]
                return {'message': 'Deleted'}, 200

        return {'error': f'Not Found: "{task_id}"'}, 404


api.add_resource(HelloResource, '/hello_world')
api.add_resource(TodosResource, '/todo', resource_class_kwargs={'tasks': tasks})
api.add_resource(TodoResource, '/todo/<int:task_id>', resource_class_kwargs={'tasks': tasks})

if __name__ == '__main__':
    app.run(debug=True)
