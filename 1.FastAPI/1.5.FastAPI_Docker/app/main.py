import sqlite3
from fastapi import FastAPI, Form, HTTPException

app = FastAPI()

@app.get('/')
def root():
    return {'Introduction': 'todo app API'}

@app.get('/tasks')
def get_tasks():
    with sqlite3.connect('todo.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM tasks')
        return cur.fetchall()

@app.post('/tasks')
def add_task(id = Form(), title = Form(), description = Form(None), time = Form(), status = Form()):
    with sqlite3.connect('todo.db') as conn:
        cur = conn.cursor()
        cur.execute(f'''INSERT INTO tasks (id, title, description, time, status) 
                        VALUES("{id}", "{title}", "{description}", "{time}", {status})''')
        conn.commit()
    return {"task added": (id, title, description, time, status)}

@app.delete('/tasks/{id}')
def delete_task(id):
    with sqlite3.connect('todo.db') as conn:
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM tasks WHERE id="{id}"')
        record = cur.fetchall()
        if not len(record):
            raise HTTPException(404, 'task not found')
        
        cur.execute(f'DELETE FROM tasks WHERE id="{id}"')
        conn.commit()
    return {'task deleted': record[0]}

@app.put('/tasks/{id}')
def update_task(id, title = Form(None), description = Form(None), time = Form(None), status = Form(None)):
    with sqlite3.connect('todo.db') as conn:
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM tasks WHERE id="{id}"')
        record = cur.fetchall()

        if not len(record):
            raise HTTPException(404, 'task not found')
        
        record = record[0]
        if title is None: title = record[1]
        if description is None: description = record[2]
        if time is None: time = record[3]
        if status is None: status = record[4]

        cur.execute(f'''UPDATE tasks
                        SET 
                            title="{title}",
                            description="{description}",
                            time="{time}",
                            status={status} 
                        WHERE id="{id}"''')
        conn.commit()
        
    return {"task updated": (id, title, description, time, status)}
        