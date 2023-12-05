import os

from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': 'Criar o dockerfile',
        'nome' : os.getenv("NOME","Eduardo"),
        'cpf_do_responsavel': os.getenv("CPF", "123.456.789-10"),
        'done': False
    },
    {
        'id': 2,
        'title': 'Fazer o deployment',
        'nome' : os.getenv("NOME2","Marcos"),
        'cpf_do_responsavel': os.getenv("CPF2", "222.456.888-20"),
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
        'nome': request.json['nome'],
        'title': request.json['title'],
        'cpf_do_responsavel':request.json['cpf_do_responsavel'],
        'done': False
    }

    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Tarefa não encontrada'}), 404
    task['nome'] = request.json.get('nome', task['nome'])
    task['title'] = request.json.get('title', task['title'])
    task['cpf_do_responsavel']=request.json.get('cpf_do_responsavel', task['cpf_do_responsavel'])
    task['done'] = request.json.get('done', task['done'])

    return jsonify({'task': task})

@app.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(host= '0.0.0.0' , port=8000)
