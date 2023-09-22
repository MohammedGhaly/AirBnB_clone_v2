#!/usr/bin/python3
"""
a script that starts a Flask web application
listening on 0.0.0.0, port 5000
"""
from flask import Flask
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello():
    """returns simple sentence on (/) route"""
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """returns (HBNB) on routing to (/hbnb)"""
    return 'HBNB'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
