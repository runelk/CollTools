#!/usr/bin/env python

import codecs
import sys
import depgrams.conll as conll
import json
import sqlite3
from rdflib import Graph, Literal, URIRef, BNode, Namespace, RDF
import urlparse


DB_FILENAME = 'db/test.db'
DB_CONLL_FILENAME = 'db/conll.db'
RDF_DB_FILENAME = 'db/rdf.bdb'
RDF_DEPGRAMS_PREFIX = 'http://localhost:5000/depgrams/0.1/'


def db_conll_init(conll_filename, db_filename=DB_CONLL_FILENAME):
    sql_create = codecs.open('./sql/conll.sql', 'r', 'utf-8').read()
    sql_insert = codecs.open('./sql/conll_insert.sql', 'r', 'utf-8').read()
    conll_data = conll.read(conll_filename)

    db = sqlite3.connect(db_filename)
    cur = db.cursor()
    cur.execute(sql_create)
    cur.executemany(sql_insert, conll_data)
    db.commit()
    db.close()


def rdf_init(rdf_db_filename=RDF_DB_FILENAME,
             db_conll_filename=DB_CONLL_FILENAME):

    g = Graph(store='Sleepycat', identifier="test")
    g.open(rdf_db_filename, create=True)
    # g = Graph()
    # prefix = 'http://localhost/'
    g.bind("dgr", RDF_DEPGRAMS_PREFIX)
    ns_dgr = Namespace(RDF_DEPGRAMS_PREFIX)

    sql_select = 'SELECT document, sid, head, deprel, cid FROM conll ' + \
                 'ORDER BY document, sid, head, deprel, cid'
    db = sqlite3.connect(db_conll_filename)
    cur = db.cursor()
    cur.execute(sql_select)
    rows = cur.fetchall()

    for row in rows:
        g.add((
            URIRef(urlparse.urljoin(
                ns_dgr, "/".join((row[0], str(row[1]), str(row[2])))
            )),
            URIRef(urlparse.urljoin(ns_dgr, row[3])),
            URIRef(urlparse.urljoin(
                ns_dgr, "/".join((row[0], str(row[1]), str(row[4])))
            ))
        ))

    # print g.serialize(format='turtle')
    g.close()


def db_init(db_filename=DB_FILENAME):
    sql_word = codecs.open('./sql/word.sql', 'r', 'utf-8').read()
    sql_relation = codecs.open('./sql/relation.sql', 'r', 'utf-8').read()

    db = sqlite3.connect(db_filename)
    cur = db.cursor()
    cur.execute(sql_word)
    cur.execute(sql_relation)
    db.commit()
    db.close()


def db_insert_words(doc_filename, depseqs, db_filename=DB_FILENAME):
    sql_insert = 'INSERT INTO word (document, form, postag, freq) ' + \
                 'VALUES (?, ?, ?, ?)'
    wordlist = ((doc_filename, w[0], w[1], depseqs['words'][w]) for w in depseqs['words'])

    db = sqlite3.connect(db_filename)
    cur = db.cursor()
    cur.executemany(sql_insert, wordlist)
    db.commit()
    db.close()


def db_insert_relations(doc_filename, depseqs, db_filename=DB_FILENAME):
    sql_insert = 'INSERT INTO relation ' + \
                 '(document, form1, postag1, rel, form2, postag2, freq) ' + \
                 'VALUES (?, ?, ?, ?, ?, ?, ?)'
    rellist = ((doc_filename,
                r[0], r[1],
                r[2],
                r[3], r[4],
                depseqs['relations'][r])
               for r in depseqs['relations'])

    db = sqlite3.connect(db_filename)
    cur = db.cursor()
    cur.executemany(sql_insert, rellist)
    db.commit()
    db.close()


def print_relations(depseqs, cutoff=1):
    for k, v in sorted(depseqs['relations'].iteritems(),
                       key=lambda ii: ii[1], reverse=True):

        if v <= cutoff:
            break

        print "{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(elm for elm in [
            k[0][0], k[0][1], k[1], k[2][0], k[2][1], v
        ])

        # print u"{0}\t{1}\t{2}\t{3}".format(
        #     u"{0}({1})".format(k[0][0], k[0][1]),
        #     k[1],
        #     u"{0}({1})".format(k[2][0], k[2][1]),
        #     v).encode('utf-8')


def print_words(depseqs, cutoff=1):
    for k, v in sorted(depseqs['words'].iteritems(),
                       key=lambda ii: ii[1], reverse=True):

        if v <= cutoff:
            break

        print u"{0}\t{1}".format(
            u"{0}\t{1}".format(k[0], k[1]), v
        ).encode('utf-8')


def main(filename, input_enc='utf-8'):

    db_conll_init(filename)
    depseqs = conll.depsequences(codecs.open(filename, 'r', input_enc))

    db_init()
    db_insert_words(filename, depseqs)
    db_insert_relations(filename, depseqs)

    rdf_init()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
