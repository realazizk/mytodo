
# Mytodo

#### Warning : this software is still in development don't use in production.


Mytodo is a free/libre (as in speech) todolist manager it protects tottally the privacy of the user because the user himself will setup and hack this script for his own sake, basically this project focuses more on the user freedom rather than the quality of the software which comes in a second place.

This project mainly contains two parts the server part which is a really simple python code you can setup on any old machine or even a raspberry pi and a client software.

For the client part have already :

  - A console based client.
  - A really simple gui tool.

## Setting Up:

this project is written in python (version 2) so you need to have it installed if you are running a GNU/Linux distro like debian or whatever I suppose that you have it installed.

it also depends on wxpython and sqlite3 if you are using a GNU/Linux distro you can get it:
for example on debian :

> sudo  apt-get install python-wxgtkx.y sqlite3



You can clone the repository using

>git clone https://github.com/mohamed-aziz/mytodo.git

or you can download the zip.

Once your clone is done  and the dependencies are satisified you can simply run the server on your local computer if you don't have another machine and simply run the client that you want it could be the cli one if you are CLI nerd like me.
if you run the server on another computer you have to edit mytodo_cli.py code and set up your ip (local or external).

I can't tell you more it's not hacking anymore, discover the rest by yourself.

Happy hacking !

------------------

## TODO or brainstorming:
  - Write a web application.
  - Write an android application (using kivy maybe I started discovering it)
  - Improve the networking code
  - Improve the GUI
  - Add the ability to record sounds and videos
  - The ability to draw using the mouse or the touchpad


(This ideas are worthless if they are not implemented)
