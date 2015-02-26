
import collections
import codecs
import re

# id = cells[0]
# form = cells[1]
# lemma = cells[2]
# cpostag = cells[3]
# postag = cells[4]
# feats = cells[5]
# head = cells[6]
# deprel = cells[7]
# phead = cells[8]
# pdeprel = cells[9]


def read(conll_filename):
    f = codecs.open(conll_filename, 'r', 'utf-8')

    doc_id = re.match('^(.+?)\.txt', conll_filename).group(1)

    sid = 1
    result = []

    for l in f:
        s = l.strip().split()
        if s:
            result.append([doc_id, sid] + s)
        else:
            sid += 1

    return result

def depsequences(conll_file, n=2):
    """Extract dependency sequences of length n from conll_file.

The contents of conll_file must conform to the CONLL data format.
Returns a list of lists (length: n) containing the dependency sequences.
If n is omitted, bigrams are returned by default."""

    sentences = conll_file.read().split("\n\n")

    result = []

    for sentence in sentences:
        words = {}
        relations = []

        for line in sentence.split("\n"):
            cells = line.strip().split()
            if cells:
                words[cells[0]] = {'form': cells[1], 'cpostag': cells[3]}
                relations.append((cells[6], cells[7], cells[0]))

        if '0' not in words:
            words['0'] = {'form': None, 'cpostag': None}

        result.append({'words': words, 'relations': relations})

    words_global = collections.Counter()
    rels_global = collections.Counter()
    # words_global = {}
    # rels_global = {}

    for i, sentence in enumerate(result):
        # for word in sentence['words'].values():
        #     words_global[(word['form'], word['cpostag'])] += 1

        # for rel in sentence['relations']:
        #     w1 = (
        #         sentence['words'][rel[0]]['form'],
        #         sentence['words'][rel[0]]['cpostag']
        #     )
        #     relation = rel[1]
        #     w2 = (
        #         sentence['words'][rel[2]]['form'],
        #         sentence['words'][rel[2]]['cpostag']
        #     )

        #     rels_global[(w1, relation, w2)] += 1
        for word in sentence['words'].values():
            words_global[(word['form'], word['cpostag'])] += 1

        for rel in sentence['relations']:
            rels_global[(
                sentence['words'][rel[0]]['form'],
                sentence['words'][rel[0]]['cpostag'],
                rel[1],
                sentence['words'][rel[2]]['form'],
                sentence['words'][rel[2]]['cpostag']
            )] += 1

    return {'words': words_global, 'relations': rels_global}
