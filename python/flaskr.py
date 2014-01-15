from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify

import record_db
from datetime import datetime, timedelta
import urllib2

DATABASE = 'test.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__, static_folder='static', static_url_path='')
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

def start_end():
  end = datetime.now()
  start = end - timedelta(weeks=1)
  return (start, end)

@app.route('/')
def index():
  locs = g.db.locs()
  start, end = start_end()
  end_str = end.strftime("%m/%d/%Y")
  start_str = start.strftime("%m/%d/%Y")
  return render_template('index.html', locations=locs, start=start_str, end=end_str)

def help_start_end(request):
  start = urllib2.unquote(request.args.get('start', ''))
  end = urllib2.unquote(request.args.get('end', ''))
  if not end:
    tmp, end = start_end()
  else:
    end = datetime.strptime(end, '%m/%d/%Y')
  if not start:
    start, tmp =start_end()
  else:
    start = datetime.strptime(start, '%m/%d/%Y')
  return start, end

@app.route('/location/<int:loc_id>/data')
def get_data(loc_id):
  start, end = help_start_end(request)
  loc = g.db.locs()[loc_id-1]
  data = {}
  if request.args.get('temps') == '1':
    dates, temps = g.db.air_temps(loc, start, end)
    data['dates'] = dates.tolist()
    data['temps'] = temps.tolist()
  if request.args.get('winds') == '1':
    dates, winds = g.db.wind_speed(loc, start, end)
    data['dates'] = dates.tolist()
    data['winds'] = winds.tolist()

  return jsonify(data)

if __name__ == '__main__':
  app.run()
