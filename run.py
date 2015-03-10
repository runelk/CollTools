#!/usr/bin/env python

from app import app
app.run(debug=True)

# app = Flask(__name__)
# app.config.from_object('config.default.Config')

# import webapp.app


# app.config.from_envvar('COLLTOOLS_SETTINGS')
# db = SQLAlchemy(app)
# G = Graph(
#     store=app.config['RDFLIB_STORE_TYPE'],
#     identifier=app.config['RDFLIB_STORE_IDENTIFIER_TEST']
# )


# class Word(db.Model):
#     __tablename__ = 'word'
#     id = Column(Integer, primary_key=True)
#     document = Column(String(120))
#     form = Column(String(120))
#     postag = Column(String(120))
#     freq = Column(Integer)


# class Relation(db.Model):
#     __tablename__ = 'relation'
#     id = Column(Integer, primary_key=True)
#     document = Column(String(180))
#     form1 = Column(String(180))
#     postag1 = Column(String(180))
#     rel = Column(String(180))
#     form2 = Column(String(180))
#     postag2 = Column(String(180))
#     freq = Column(Integer)


# with app.app_context():
#     db.create_all()


# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/depgraph')
# def depgraph():
#     return "Unimplemented"


# @app.route('/conll')
# def conll():
#     return "Unimplemented"

############################################################
# API


# @app.route('/api/v1/graph')
# def api_conll():
#     return json.dumps({"status": 'unimplemented'})


# @app.route('/api/v1/conll')
# def api_conll():
#     return json.dumps({"status": 'unimplemented'})


# @app.route('/api/v1/conll')
# def api_conll():
#     return json.dumps({"status": 'unimplemented'})


# @app.route('/api/v1/conll')
# def api_conll():
#     return json.dumps({"status": 'unimplemented'})


# @app.route('/api/v1/conll')
# def api_conll():
#     return json.dumps({"status": 'unimplemented'})

###############################################################################
# NB: Probably deprecated stuff below here
###############################################################################

# @app.route('/api/v1/words')
# def words():
#     return jsonify({'words': [
#         {'document': w.document,
#          'form': w.form, 'postag': w.postag,
#          'freq': w.freq}
#         for w in Word.query.all()
#     ]})

# @app.route('/api/v1/relations')
# def relations():
#     return jsonify({'relations': [
#         {'document': r.document,
#          'form1': r.form1, 'postag1': r.postag1,
#          'rel': r.rel,
#          'form2': r.form2, 'postag2': r.postag2,
#          'freq': r.freq}
#         for r in Relation.query.all()
#     ]})
#     test = Relation.query.all()
#     print test[0]
#     return jsonify(test)


# @app.route('/rdf/test')
# def rdftest():
#     # g = Graph(store=app.config['RDFLIB_STORE_TYPE'],
#     #           identifier=app.config['RDFLIB_STORE_IDENTIFIER_TEST'])
#     # g.open(app.config['DB_PATH_RDFLIB'])
#     G.bind("dgr", app.config['RDF_NAMESPACE_DEPGRAMS'])
#     ns_dgr = Namespace(app.config['RDF_NAMESPACE_DEPGRAMS'])
#     # res = []
#     # for s, o, p in g:
#     #     res.append(str(s))
#     s = G.serialize(format='pretty-xml')
#     return s

# if __name__ == '__main__':
#     app.run()
