# This the server code that will be used to get the todo's
# and store them into an sqlite3 database
# this is too simple code

import socket
import thread
import random
import string
import sqlite3
import base64
import time

auth_user = {
  'user' : '',
  'token': ''
}

auth_users = []
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('localhost', 7060))
sock.listen(10)
dbcon = sqlite3.connect('todo.db', check_same_thread=False)

class database(object):

  def __init__(self, user, token):
    self.user=user
    self.token = token

  def listall(self):
    with dbcon:
      user = self._get_username(self.token)
      # get owner id
      user_id = self._get_id_by_username(self.user)
      cur = dbcon.cursor()
      cur.execute('SELECT * FROM Todo WHERE owner=(?)', (user_id,))
      return cur.fetchall()

  def check_token(self, token):
    return self.token == token

  def _get_username(self, token):
    # this will return the index in the list of the dict we are looking for
    #lst = next(index for (index, d) in enumerate(auth_users) if d['token']==token)
    for i, dic in enumerate(auth_users):
      if dic['token']==token:
        return auth_users[i]['user']
        break
      return False
  def _get_id_by_username(self, user):
    with dbcon:
      cur = dbcon.cursor()
      cur.execute('SELECT id FROM Users WHERE username=(?)', (user,))
      return cur.fetchone()[0]

def generate_token(length):
  pool = string.letters + string.digits
  return ''.join(random.choice(pool) for i in xrange(length))

def check_duplicated_users(user, auth_users):
  # ugly and non performant code
  found = False
  for elem in auth_users:
    if elem['user'] == user['user']:
      found = True
      break
  return found

def workerthread(conn):
  while True:
    data= conn.recv(1024)
    if not data:
      break
    dat = data.split()
    if dat :
      if dat[0] == 'auth' :
        with dbcon:
          # Just logging in
          cur = dbcon.cursor()
          cur.execute('SELECT username,password FROM Users WHERE username=(?)', (dat[1],))
          data = cur.fetchone()
        if dat[1] == data[0] and dat[2] == data[1]:
          token = generate_token(64)
          if not token :
            conn.send('FAI')
            break
          conn.send('SUC')
          auth = auth_user
          auth['user'] = dat[1]
          auth['token'] = token
          print time.strftime("Request Sent from "+auth['user'] +" %Y-%m-%d %H:%M")
          del dat[:]

          # Don't reauthentificate users
          if not check_duplicated_users(auth, auth_users):
            auth_users.append(auth)
          # send back to the client the key
          conn.send(token)
        else :
          conn.send('FAI')
      elif dat[0] == 'lsall' and len(dat)==3:
        usr = database(dat[1], dat[2])
        a=usr.listall()
        conn.send(base64.b64encode(str(a)))
  conn.close()

while True:
  try :
    conn, adr  = sock.accept()
    thread.start_new_thread(workerthread, (conn,))
  except KeyboardInterrupt :
    print 'Bye!'
    break
sock.close()

