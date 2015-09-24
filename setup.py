

from setuptools import setup

setup(
  name='mytodo',
  version='0.2.1',
  description='The free/libre todo list manager',
  url='https://github.com/mohamed-aziz/mytodo',
  author='Mohamed Aziz Knani',

  author_email='medazizknani@gmail.com',

  license='GPL3',
  packages=['mytodo',
            'mytodo.mytodoweb',
            'mytodo.img'],
  scripts=[
    'mytodo/mytodo_cli',
    'mytodo/mytodo_server',
    'mytodo/mytodo_gui'
  ],
  package_data={
    'mytodo.img' : ['close.png', 'done.png']
  },

  install_requires=[
    'requests',
    'flask',
    'sqlalchemy'
  ]
)
