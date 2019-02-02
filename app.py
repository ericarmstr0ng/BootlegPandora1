from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('base.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


if __name__ == '__main__':
    app.run()
