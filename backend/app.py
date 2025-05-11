from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
# 允许所有源
CORS(app, resources={r"/*": {"origins": "*"}})

@app.before_request
def before_request():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            urgency INTEGER NOT NULL,
            importance INTEGER NOT NULL,
            completed BOOLEAN DEFAULT FALSE
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return jsonify([{
        'id': task[0],
        'title': task[1],
        'description': task[2],
        'urgency': task[3],
        'importance': task[4],
        'completed': task[5]
    } for task in tasks])


@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, description, urgency, importance)
        VALUES (?,?,?,?)
    ''', (data['title'], data['description'], data['urgency'], data['importance']))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': task_id}), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE tasks
        SET title = ?, description = ?, urgency = ?, importance = ?, completed = ?
        WHERE id = ?
    ''', (data.get('title'), data.get('description'), data.get('urgency'), data.get('importance'), data.get('completed'), task_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task updated successfully'})


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task deleted successfully'})


if __name__ == '__main__':
    app.run(debug=False)