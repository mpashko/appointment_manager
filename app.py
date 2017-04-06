from flask import Flask
from environment import Environment
import os

app = Flask(__name__)
app.secret_key = 'secret'
env = Environment()

from view import *

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
