#!/usr/bin/python3
"""
a script that starts a Flask web application
listening on 0.0.0.0, port 5000
"""
from flask import Flask, render_template
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


@app.route('/c/<text>')
def c_is_fun(text):
    """returns 'C' followed by the value of text"""
    return f"C {text.replace('_', ' ')}"


@app.route('/python')
@app.route('/python/<text>')
def python_is_cool(text='is cool'):
    """returns 'Python' followed by the value of text"""
    return f"Python {text.replace('_', ' ')}"


@app.route('/number/<int:n>')
def is_a_number(n):
    '''returns “n is a number” only if n is an integer'''
    return f'{n} is a number'


@app.route('/number_template/<int:n>')
def number_temp(n):
    '''returns a template with “Number: n” only if n is an integer'''
    return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>')
def number_odd_or_even(n):
    '''returns a template with “Number: n odd|even” only if n is an integer'''
    if n % 2:
        odd_or_even = 'odd'
    else:
        odd_or_even = 'even'

    info = {
            'number': n,
            'odd_or_even': odd_or_even
           }
    return render_template('6-number_odd_or_even.html', info=info)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
