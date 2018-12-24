from alayatodo import app,db,ma
from alayatodo.models import User,Todo,TodoSchema
from sqlalchemy.exc import SQLAlchemyError
from flask import (
    redirect,
    render_template,
    request,
    session,
    jsonify,
    flash,
    url_for
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
    if todo is None:
        return render_template('404.html')
    if todo.user_id != user_id :
        return render_template('404.html')
    return render_template('todo.html', todo = todo)


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    user_id = session['user'].get('id')
    page = request.args.get('page', 1, type=int)
    next_url = None
    prev_url = None
    todos = Todo.query.filter_by(user_id = user_id).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    if not todos.items:
        return render_template('404.html')
    if todos.has_next:
        next_url = url_for('todos', page=todos.next_num)
    if todos.has_prev:
        prev_url = url_for('todos', page=todos.prev_num)
    return render_template('todos.html', todos = todos,
                           next_url=next_url,
                           prev_url=prev_url)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    user_id = session['user']['id']
    description = request.form.get('description', '')
    new_Todo = Todo(user_id, description,False)
    try:
        db.session.add(new_Todo)
        db.session.commit()
        flash('Todo '+ new_Todo.description + ' added with Success!', 'success')
    except SQLAlchemyError:
        db.session.rollback()
        flash('Something went wrong. Please try again later', 'danger')
    except AssertionError:
        flash('A Todo must have a description', 'danger')
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todo.query.filter_by(id = id).first()
    try:
        db.session.delete(todo)
        db.session.commit()
        flash('Todo '+ todo.description + ' deleted with Success!', 'success')
    except SQLAlchemyError:
        db.session.rollback()
        flash('Something went wrong. Please try again later','danger')
    return redirect('/todo')


@app.route('/todo/update/<id>', methods=['POST'])
def todo_update(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todo.query.filter_by(id = id).first()
    todo.complete = not(todo.complete)
    try:
        db.session.commit()
        flash('Todo '+ todo.description + ' updated with Success!', 'success')
    except SQLAlchemyError:
        db.session.rollback()
        flash('Something went wrong. Please try again later','danger')
    return redirect('/todo')


@app.route('/todo/<id>/json', methods=['GET'])
def todo_json(id):
    if not session.get('logged_in'):
        return redirect('/login')
    user_id = session['user'].get('id')
    todo = Todo.query.filter_by(id = id).first()
    if todo is None:
        return render_template('404.html')
    if todo.user_id != user_id :
        return render_template('404.html')
    todo_schema = TodoSchema()
    todo_json = todo_schema.dump(todo).data
    return jsonify({'Todo': todo_json})
