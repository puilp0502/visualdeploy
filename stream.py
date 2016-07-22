import subprocess
import os

from flask import Flask, Response

from visualdeploy import execute


app = Flask(__name__)


@app.route("/stream")
def stream():
    # commands = ['echo {}sec; sleep {}'.format(i, 1) for i in range(0, 10)]
    python = '~/webapp/venv/bin/python3'
    pip = '~/webapp/venv/bin/pip3'
    manage_py = '~/webapp/manage.py'

    commands = [
        'cd ~',
        'git clone https://github.com/sample/webapp',
        'cd webapp',
        'git pull origin master',
        'git reset --hard origin/master',
        '-cp ~/production.py ~/webapp/webapp/settings/',  # Secret command!

        'cd ~/webapp/static/',
        'npm install',
        'bower install',
        'webpack',

        'cd ~/webapp',
        'virtualenv -p python3 venv',
        '{pip} install -r ~/webapp/requirements.txt'.format(pip=pip),
        '{python} {manage_py} collectstatic --noinput'.format(python=python, manage_py=manage_py),
        '{python} {manage_py} makemigrations --noinput'.format(python=python, manage_py=manage_py),
        '{python} {manage_py} migrate --noinput'.format(python=python, manage_py=manage_py),
        'touch ~/webapp/webapp/wsgi.py',
    ]
    resp = Response(execute(commands), mimetype='text/html')
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
