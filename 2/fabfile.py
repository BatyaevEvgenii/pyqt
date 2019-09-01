# shortcut для подмодулей, будет выполняться в любой локальной среде
from fabric.api import local

def server():
    local('python server')

def client():
    local('python client')

# def client(mode):
#     local(f'python client --mode {mode}')

def test():
    local('pytest --cov-report term-missing --cov server')

def kill():
    local('lsof -t -i tcp:8000 | xargs kill')