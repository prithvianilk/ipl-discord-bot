from os import environ
from flask import Flask

app = Flask(name)
app.run(environ.get('PORT'))