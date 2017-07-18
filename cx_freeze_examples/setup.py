from cx_Freeze import Executable, setup

executables = [Executable('example.py')]

setup(name='hello_world',
      version='0.0.1',
      description='My Hello World App!',
      executables=executables)
