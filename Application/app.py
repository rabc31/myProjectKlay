from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DATABASE = 'data.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        with sqlite3.connect(DATABASE) as conn:
            conn.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
            conn.commit()
        
        return redirect('/success')

    return render_template('form.html')

@app.route('/success')
def success():
    return '<h2>Data saved successfully! <a href="/">Go back</a></h2>'

# Add the /users route here
@app.route('/users')
def users():
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.execute('SELECT id, name, email FROM users')
        users = cur.fetchall()
    
    return render_template('users.html', users=users)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
