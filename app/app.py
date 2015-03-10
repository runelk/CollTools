from flask import Flask, render_template

# app = Flask(__name__)
# app.config.from_object('config.default.Config')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/depgraph')
def depgraph():
    return "Unimplemented"


@app.route('/conll')
def conll():
    return "Unimplemented"

