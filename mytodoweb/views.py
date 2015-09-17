

from . import app, database
from flask import jsonify

@app.route('/api/get/<string:username>', methods=['GET'])
def apiget(username):
  s = database.Session()
  a = s.query(database.Todo).filter(database.Todo.owner == 1).all()

  # My fast an dirty hack
  c = dict()
  for i, x in enumerate(a):
    del x.__dict__['_sa_instance_state']
    c[str(i)] = x.__dict__

  return jsonify(c)

