"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
"""
from docopt import docopt
from dotenv import load_dotenv
from flask_migrate import init,upgrade,migrate
from sqlalchemy.exc import SQLAlchemyError
from alayatodo import app,db,MIGRATION_DIR
from alayatodo.models import User,Todo
import subprocess
import logging
import os

logging.basicConfig()
logger = logging.getLogger('logger')


def _run_sql(filename):
    try:
        subprocess.check_output(
            "sqlite3 %s < %s" % (app.config['DATABASE'], filename),
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError, ex:
        print ex.output
        os.exit(1)

def create_users():
    user1 = User(username='user1')
    user1.set_password('user1')

    user2 = User(username='user2')
    user2.set_password('user2')

    user3 = User(username='user3')
    user3.set_password('user3')

    users = [user1,user2,user3]
    try:
        db.session.add_all(users)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        print 'Something went wrong'

def create_todos():
    todo1 = Todo(1, 'Vivamus tempus',False)
    todo2 = Todo(1, 'lorem ac odio',False)
    todo3 = Todo(1, 'Ut congue odio',True)
    todo4 = Todo(1, 'Sodales finibus',False)
    todo5 = Todo(1, 'Accumsan nunc vitae',False)
    todo6 = Todo(2, 'Lorem ipsum',False)
    todo7 = Todo(2, 'In lacinia est',False)
    todo8 = Todo(2, 'Odio varius gravida',False)

    todos = [todo1,todo2,todo3,todo4,
             todo5,todo6,todo7,todo8]
    try:
        db.session.add_all(todos)
        db.session.commit()
    except SQLAlchemyError,err:
        print(err)
        db.session.rollback()
        print 'Something went wrong'

if __name__ == '__main__':
    load_dotenv()
    args = docopt(__doc__)
    if args['initdb']:
        with app.app_context():
            _run_sql('resources/database.sql')
            upgrade()
            create_users()
            create_todos()
            #_run_sql('resources/fixtures.sql')
            print "AlayaTodo: Database initialized."
    else:
        app.run(use_reloader=True)
