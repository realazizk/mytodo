
from . import database

def checkuser(username, password):
  if username is None or password is None:
    return False
  s = database.Session()
  # Checks if the username exists
  found = s.query(database.User).filter_by(username = username).first()
  if found is None:
    return False

  if found.username != username or found.password != password:
    return False

  return True

def getOwnerbyUsername(username):
  s = database.Session()
  return s.query(database.User).filter_by(username = username).first().id
