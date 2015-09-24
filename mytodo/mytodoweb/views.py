#!/usr/bin/env python2
#Copyright (C) 2015 Mohamed Aziz knani

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>

from . import app, database, tools
from flask import jsonify, request, abort

@app.route('/api/get/', methods=['GET', 'POST'])
def apiget():
  t = request.args.get('action')
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    a = []
    if not tools.checkuser(username, password):
      abort(400)
    s = database.Session()
    if t == 'all':
      a = s.query(database.Todo).filter(database.Todo.owner == tools.getOwnerbyUsername(username)).all()
    elif t == 'ls':
      a = s.query(database.Todo).filter(database.Todo.owner == tools.getOwnerbyUsername(username),
                                        database.Todo.done == 0).all()
    elif t == 'search':
      if request.args.has_key('tag'):
        search = request.args.get('tag')
        a = s.query(database.Todo).filter(database.Todo.owner == tools.getOwnerbyUsername(username),
                                        database.Todo.todotext.like('%'+search+'%')).all()
    # My fast an dirty hack ( This is ugly I know )
    c = dict()
    for i, x in enumerate(a):
      del x.__dict__['_sa_instance_state']
      c[str(i)] = x.__dict__
    return jsonify(c)
  else:
    return 'Send a post request containing username and password'

@app.route('/api/set/', methods=['GET', 'POST'])
def  apiset():
  t = request.args.get('action')
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    a = []

    if not tools.checkuser(username, password):
      abort(400)

    s = database.Session()

    if request.args.has_key('index'):
      index = int(request.args.get('index'))

      if (t == 'done' or t == 'undone'):
        a = s.query(database.Todo).filter(database.Todo.owner == tools.getOwnerbyUsername(username),
                                          database.Todo.id  == index).first()
        a.done = 1 if t == 'done' else 0
        s.commit()

      if t == 'remove':
        a = s.query(database.Todo).filter(database.Todo.owner == tools.getOwnerbyUsername(username),
                                          database.Todo.id  == index).first()
        if not a is None:
          s.delete(a)
          s.commit()

    if request.form.has_key('text'):
      text = request.form.get('text')
      if t == 'add':
        a = database.Todo(tools.getOwnerbyUsername(username), text)
        s.add(a)
        s.commit()
    return ''
  else:
    return 'Send a post request containing username and password'

