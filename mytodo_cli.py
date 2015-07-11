import socket
import argparse
from sys import argv
import base64
# Here set your user and password
user = {
  'user' : 'mohamed',
  'pass' : 'root',
  'token': ''
}

def argument_parser():
  parser = argparse.ArgumentParser(description='mytodo script')
  parser.add_argument('command', help='type in your command')
  parser.add_argument('-u', help='Set up your username from the database' ,dest='user')
  parser.add_argument('-p', help='Set up your password from the database', dest='passwd')
  args = parser.parse_args()
  return (args.command, args.user or user['user'], args.passwd or user['pass'])

def connectuser(user):
  # authentificate
  sock.send('auth %s %s' % (user['user'], user['pass']))
  if sock.recv(3) == 'SUC' :
    token = sock.recv(64)
    user['token'] = token
  else :
    sock.close()
    print 'Could not connect'
    exit(0)
  return user

def command(com, user, token):
  sock.send('%s %s %s' % (com, user, token))
  data = sock.recv(4096)
  # I think this can cause security issue
  return eval(base64.b64decode(data))

def display(out):
  import colorama
  for i, row in enumerate(out):
    print '%i) %s' % (i, row[2])

if __name__ == '__main__':
  com, user['user'], user['pass'] = argument_parser()
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_adress = ('localhost', 7060)
    sock.connect(server_adress)
    user = connectuser(user)
    out = command(com, user['user'], user['pass'])
    print out
  except:
    print 'Server is closed, please run it'
    exit(0)
  print user


