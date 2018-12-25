"""AlayaNotes

Usage:
  main.py [run]
  main.py initdb
"""
from docopt import docopt
from dotenv import load_dotenv
from alayatodo import app
import subprocess
import os


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


if __name__ == '__main__':
    load_dotenv()
    args = docopt(__doc__)
    if args['initdb']:
        _run_sql('resources/database.sql')
        _run_sql('resources/fixtures.sql')
        print "AlayaTodo: Database initialized."
    else:
        app.run(use_reloader=True)
