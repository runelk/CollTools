from flask import Flask, render_template, request
import json
import requests

app = Flask(__name__)
app.config.from_object('config')

GREMLIN_URL = 'http://localhost:8182/graphs/test02/tp/gremlin'


def gq(q):
    """Executes a Gremlin query against the default graph.
"""
    r = requests.get(GREMLIN_URL, params={'script': q})
    if r.json() and 'results' in r.json():
        return r.json()['results']
    return {
        'status': 'error',
        'url': r.url
    }


def gq_document(name):
    return gq("g.V('class', 'Conll').has('name', '%s')" % name)


def gq_document_sentences(name):
    return gq("g.V('class', 'Conll').has('name', '%s')" % name)


###############################################################################
# WEB INTERFACE
###############################################################################


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/gremlin/')
def gremlin():
    return render_template('gremlin.html')


###############################################################################
# API
###############################################################################


@app.route('/api/v1/')
def api_v1():
    return json.dumps({'status': 'unimplemented'})


@app.route('/api/v1/documents')
def api_v1_documents():
    res = gq("g.V('class', 'Conll')")
    return json.dumps(res)


@app.route('/api/v1/document/<path:name>')
def api_v1_document(name):
    res = gq_document(name)
    return json.dumps(res)


@app.route('/api/v1/document/<path:name>/sentences')
def api_v1_document_sentences(name):
    res = gq_document_sentences(name)
    return json.dumps(res)


@app.route('/api/v1/vertices')
def api_v1_vertices():
    r = requests.get(GREMLIN_URL)
    jsn = r.json()
    return json.dumps(jsn)

########################################
# GREMLIN

@app.route('/api/v1/gremlin', methods=['GET', 'POST'])
def api_v1_gremlin():
    q = request.args.get('q', '')
    res = gq(q)
    return json.dumps({
        'query': q,
        'result': res
    })
    # r = requests.get(GREMLIN_URL)
    # jsn = r.json()
    # return json.dumps(jsn)
