import record_db
import os

def db_url():
  return os.environ.get('DATABASE_URL')

def init_db():
  db = record_db.connect(db_url())
  record_db.init_database(db)


if __name__ == '__main__':
  init_db()
