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

from mytodo.mytodoweb import app

# Disable debug in production
app.config['DEBUG'] = False

app.config["HOST"] = '0.0.0.0'
app.config["PORT"] = 5000

# Change this; as suggested in Flask docs you may want
# to use urandom
app.secret_key = 'My-really-top-key'

# Set your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/mohamed/todo.db'


