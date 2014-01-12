from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

import record_db

DATABASE = 'test.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
# alternately:  app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.before_request
def before_request():
  g.db = record_db.connect('sqlite:///test.db')

@app.teardown_request
def teardown_request(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

@app.route('/')
def index():
  locs = g.db.locs()
  return render_template('index.html', locations=locs)


if __name__ == '__main__':
  app.run()
