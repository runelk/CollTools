
from flask import Flask, jsonify, url_for
from flask.ext.sqlalchemy import SQLAlchemy
# from webapp.database import Base
from sqlalchemy import Column, Integer, String
# import webapp.models as models
from rdflib import Graph, Namespace

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/test.db'
app.debug = True
db = SQLAlchemy(app)
g = Graph(store='Sleepycat')


class Word(db.Model):
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True)
    document = Column(String(120))
    form = Column(String(120))
    postag = Column(String(120))
    freq = Column(Integer)


class Relation(db.Model):
    __tablename__ = 'relation'
    id = Column(Integer, primary_key=True)
    document = Column(String(180))
    form1 = Column(String(180))
    postag1 = Column(String(180))
    rel = Column(String(180))
    form2 = Column(String(180))
    postag2 = Column(String(180))
    freq = Column(Integer)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return "Hello Flask"


@app.route('/api/v1/words')
def words():
    return jsonify({'words': [
        {'document': w.document,
         'form': w.form, 'postag': w.postag,
         'freq': w.freq}
        for w in Word.query.all()
    ]})


@app.route('/api/v1/relations')
def relations():
    return jsonify({'relations': [
        {'document': r.document,
         'form1': r.form1, 'postag1': r.postag1,
         'rel': r.rel,
         'form2': r.form2, 'postag2': r.postag2,
         'freq': r.freq}
        for r in Relation.query.all()
    ]})
    test = Relation.query.all()
    print test[0]
    return jsonify(test)


@app.route('/rdf/test')
def rdftest():
    g = Graph(store='Sleepycat', identifier="test")
    g.open('db/rdf.bdb')
    g.bind("dgr", 'http://localhost:5000/depgrams/0.1/')
    ns_dgr = Namespace('http://localhost:5000/depgrams/0.1/')
    # res = []
    # for s, o, p in g:
    #     res.append(str(s))
    s = g.serialize(format='pretty-xml')
    g.close()
    return s

if __name__ == '__main__':
    app.run()
