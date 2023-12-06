import os

from flask import Flask, jsonify, request
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()

tasks = [
    {
        'id': 1,
        'title': 'Comprar mantimentos',
        'done': False
    },
    {
        'id': 2,
        'title': 'Estudar para a prova',
        'done': False
    }
]

@app.route('/', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    return jsonify({'task': task})

@app.route('/', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        return jsonify({'error': 'A tarefa deve ter um título'}), 400

    task = {
        'id': tasks[-1]['id'] + 1 if tasks else 1,
        'title': request.json['title'],
        'done': False
    }

    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Tarefa não encontrada'}), 404

    task['title'] = request.json.get('title', task['title'])
    task['done'] = request.json.get('done', task['done'])

    return jsonify({'task': task})

@app.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(host= '0.0.0.0' , port= os.getenv("PORT", "3000"))
