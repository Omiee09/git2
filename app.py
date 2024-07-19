from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# SQLite3 Database initialization
def init_db():
    conn = sqlite3.connect('todo.db')
    print("Opened database successfully")

    conn.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        );
    ''')
    print("Table created successfully")
    conn.close()

init_db()

# Route to display all todos
@app.route('/')
def index():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM todos ORDER BY id DESC')
    todos = cursor.fetchall()
    conn.close()
    return render_template('index.html', todos=todos)

# Route to add a new todo
@app.route('/add', methods=['POST'])
def add_todo():
    task = request.form['task']
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO todos (task) VALUES (?)', (task,))
    conn.commit()
    conn.close()
    flash('Task added successfully!', 'success')
    return redirect(url_for('index'))

# Route to delete a todo
@app.route('/delete/<int:id>', methods=['POST'])
def delete_todo(id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM todos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
