

from mytodoweb import app

# Disable debug in production
app.config['DEBUG'] = True

# Change this; as suggested in Flask docs you may want
# to use urandom
app.secret_key = 'My-really-top-key'

# Set your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/mohamed/myFiles/mytodo/todo.db'


