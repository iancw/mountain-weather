from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify

import record_db
from datetime import datetime, timedelta

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

@app.route('/location/<int:loc_id>/temp')
def get_temperature(loc_id):
  start = request.args.get('from', '')
  end = request.args.get('to', '')
  end = datetime.now()
  start = end - timedelta(weeks=2)
  loc = g.db.locs()[loc_id]
  #return "From: {0}, to:{1} for loc: {2}".format(start, end, loc.name)
  dates, temps = g.db.air_temps(loc, start, end)
  return jsonify({'dates': dates.tolist(), 'temps': temps.tolist()})


if __name__ == '__main__':
  app.run()
