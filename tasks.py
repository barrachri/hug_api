# Stdlib imports
import time
# 3rd party lib imports
from invoke import task, run

@task
def test(ctx):
    print("Running tests.....")
    time.sleep(5)
    ctx.run("py.test -v")

@task
def hug(ctx):
    print("Running hug.....")
    time.sleep(5)
    print("Serving on localhost:8000")
    ctx.run("hug -f app.py")

@task
def deploy(ctx):
    print("Running gunicorn.....")
    time.sleep(5)
    ctx.run("gunicorn app:__hug_wsgi__")
