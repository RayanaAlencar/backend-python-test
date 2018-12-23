from alayatodo import app, db
from alayatodo.models import User,Todo
from flask import (
    redirect,
    render_template,
    request,
    session
    )


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l.decode('utf-8') for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username = username,password = password).first()

    if user:
        session['user'] = {"username": user.username,
                           "password": user.password,
                           "id":user.id}
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    user_id = session['user'].get('id')
    print( 'todo details...')
    todo = Todo.query.filter_by(id = id).first()
    if todo.user_id != user_id :
        return render_template('404.html')
    return render_template('todo.html', todo = todo)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    user_id = session['user'].get('id')
    todos = Todo.query.filter_by(user_id = user_id)
    return render_template('todos.html', todos = todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    user_id = session['user']['id']
    description = request.form.get('description', '')
    new_Todo = Todo(user_id, description)
    db.session.add(new_Todo)
    db.session.commit()
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/todo')
