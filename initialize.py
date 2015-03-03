#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys
import depgrams.conll as conll
import json
import sqlite3
from rdflib import Graph, Literal, URIRef, BNode, Namespace, RDF
import urlparse
from config.default import Config
import os
import pyorient

c = Config()


def mypath(p):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), p)


def db_conll_init(conll_filename, db_filename=mypath(c.DB_PATH_CONLL)):
    sql_create = codecs.open('./sql/conll.sql', 'r', 'utf-8').read()
    sql_insert = codecs.open('./sql/conll_insert.sql', 'r', 'utf-8').read()

    conll_data = conll.read(conll_filename)

    db = sqlite3.connect(db_filename)
    cur = db.cursor()
    cur.execute(sql_create)
    cur.executemany(sql_insert, conll_data)
    db.commit()
    db.close()


def orientdb_init(db_conll_filename=mypath(c.DB_PATH_CONLL),
                  db_addr="localhost",
                  db_port=2424,
                  user_root="root",
                  pwd_root="testingorient",
                  user_write="init",
                  pwd_write="init999",
                  db_name="test01"):

    c = pyorient.OrientDB(db_addr, 2424)
    c.connect(user_root, pwd_root)

    # Start with an empty database
    if c.db_exists(db_name, pyorient.STORAGE_TYPE_MEMORY):
        c.db_drop(db_name)
    c.db_create(db_name,
                pyorient.DB_TYPE_GRAPH,
                pyorient.STORAGE_TYPE_MEMORY)
    c.db_open(db_name, user_root, pwd_root)
    c.command(" ".join([
        "insert into ouser set",
        ", ".join([
            "name = '%s'" % user_write,
            "password = '%s'" % pwd_write,
            "status = 'ACTIVE'",
            "roles = (select from ORole where name = 'admin')"
        ])
    ]))
    c.db_close()

    c = pyorient.OrientDB(db_addr, 2424)
    c.connect(user_root, pwd_root)
    c.db_open(db_name, user_write, pwd_write)

    c.command("create class Conll extends V")
    c.command("create class Sentence extends V")
    c.command("create class Word extends V")
    c.command("create class Document extends V")

    # A Conll class Contains sentences
    c.command("create class Contains extends E")
    # For the Conll data
    c.command("create class Head extends E")

    db = sqlite3.connect(db_conll_filename)
    cur = db.cursor()

    for row in cur.execute(" ".join([
        'select distinct document from conll',
        'order by document asc'
    ])).fetchall():
        content = {'name': row[0]}
        cmdV = "create vertex Conll content %s" % json.dumps(content)
        res = c.command(cmdV.encode('utf-8'))

    for row in cur.execute(" ".join([
        'select distinct document, sid from conll',
        'order by document asc, sid asc'
    ])).fetchall():
        content = {'conll': row[0], 'id': row[1]}
        cmdV = "create vertex Sentence content %s" % json.dumps(content)
        res = c.command(cmdV.encode('utf-8'))

        c.command(" ".join([
            "create edge Contains from",
            "(select from Conll where name = '%s')" % row[0],
            "to",
            "(select from Sentence where conll = '%s' and id = %s)" % (
                content['conll'], content['id']
            )
        ]).encode('utf-8'))

    for row in cur.execute(" ".join([
            'select distinct',
            ', '.join([
                'document',
                'sid',
                'cid',
                'form',
                'lemma',
                'cpostag',
                'head',
                'deprel']),
            'from conll',
            'order by document asc, sid asc'
    ])).fetchall():
        content = {
            'conll': row[0],
            'sid': row[1],
            'id': row[2],
            'form': row[3],
            'lemma': row[4],
            'cpostag': row[5]
        }
        cmdV = "create vertex Word content %s" % json.dumps(content)
        c.command(cmdV.encode('utf-8'))
        c.command(" ".join([
            "create edge Contains from",
            "(select from Sentence where conll = '%s' and id = %s)" % (
                content['conll'],
                json.dumps(content['sid'])
            ),
            "to",
            "(select from Word where conll = '%s' and sid = %s and id = %s)" % (
                content['conll'],
                json.dumps(content['sid']),
                json.dumps(content['id'])
            )
        ]).encode('utf-8'))

        c.command(" ".join([
            "create edge Head from",
            "(select from Word where conll = '%s' and sid = %s and id = %s)" % (
                content['conll'],
                content['sid'],
                content['id']
            ),
            "to",
            "(select from Word where conll = '%s' and sid = %s and id = %s)" % (
                content['conll'],
                content['sid'],
                row[6]
            ),
            "set deprel = '%s'" % row[7]
        ]).encode('utf-8'))

    c.db_close()


def rdf_init(rdf_db_filename=mypath(c.DB_PATH_RDFLIB),
             db_conll_filename=mypath(c.DB_PATH_CONLL)):

    g = Graph(store=c.RDFLIB_STORE_TYPE,
              identifier=c.RDFLIB_STORE_IDENTIFIER_TEST)
    g.open(rdf_db_filename, create=True)
    g.bind("dgr", c.RDF_NAMESPACE_DEPGRAMS)
    ns_dgr = Namespace(c.RDF_NAMESPACE_DEPGRAMS)

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

    g.close()


def db_init(db_filename=mypath(c.DB_PATH_MAIN)):
    sql_word = codecs.open('./sql/word.sql', 'r', 'utf-8').read()
    sql_relation = codecs.open('./sql/relation.sql', 'r', 'utf-8').read()
    db = sqlite3.connect(db_filename)
    cur = db.cursor()
    cur.execute(sql_word)
    cur.execute(sql_relation)
    db.commit()
    db.close()


def db_insert_words(doc_filename, depseqs, db_filename=mypath(c.DB_PATH_MAIN)):
    sql_insert = 'INSERT INTO word (document, form, postag, freq) ' + \
                 'VALUES (?, ?, ?, ?)'
    wordlist = ((doc_filename, w[0], w[1], depseqs['words'][w]) for w in depseqs['words'])
    db = sqlite3.connect(db_filename)
    cur = db.cursor()
    cur.executemany(sql_insert, wordlist)
    db.commit()
    db.close()


def db_insert_relations(doc_filename, depseqs,
                        db_filename=mypath(c.DB_PATH_MAIN)):
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


def print_words(depseqs, cutoff=1):
    for k, v in sorted(depseqs['words'].iteritems(),
                       key=lambda ii: ii[1], reverse=True):

        if v <= cutoff:
            break

        print u"{0}\t{1}".format(
            u"{0}\t{1}".format(k[0], k[1]), v
        ).encode('utf-8')


def main(filename, input_enc='utf-8'):
    # Create preliminary conll database
    # db_conll_init(filename)
    # Extract information from a conll file
    # depseqs = conll.depsequences(codecs.open(filename, 'r', input_enc))
    # Create main database
    # db_init()
    # Insert word information from the conll file
    # db_insert_words(filename, depseqs)
    # Insert relation information from the conll file
    # db_insert_relations(filename, depseqs)

    # DEPRECATED
    # # Create RDF store
    # rdf_init()

    # Create OrientDB graph
    orientdb_init()

if __name__ == "__main__":
    main(sys.argv[1])
