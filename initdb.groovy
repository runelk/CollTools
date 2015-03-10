import static groovy.io.FileType.FILES

def docNameFromFilename(path) { (path =~ /^[\.\/]*(.+?)\..*$/)[0][1] }

def addConllV(g, docPath) {
  def docName = docNameFromFilename(docPath)
  g.addVertex(null, ['class': 'Conll', 'name': docName])
}

def addSentence(g, position, conllV) {
  def sentV = g.addVertex(null, ['class': 'Sentence', 'position': position])
  g.addEdge(conllV, sentV, 'contains')
  return sentV
}

def addWord(g, position, form, lemma, sentenceV) {
  def wordV = g.addVertex(null, ['class': 'Word', 'position': position, 'form': form, 'lemma': lemma])
  g.addEdge(sentenceV, wordV, 'contains')
  return wordV
}

def start(graphLocation, conllDocs) {
  g = new OrientGraph(graphLocation, "admin", "admin")

  g.V.each({ g.removeVertex(it) })
  g.commit()
  g.E.each({ g.removeEdge(it) })
  g.commit()

  // g.V.remove()
  // g.E.remove()

  conllDocs.each {
    println "Registering " + it
    def conllV = addConllV(g, it)
    def conllData = new File(it)
    def sid = 1
    def sentenceV = addSentence(g, sid, conllV)
    def deprels = []
    def words = [:]

    conllData.eachLine {
      if (!it.empty) {
  	def spl = it.split("\t")
  	def wid = spl[0]
  	def form = spl[1]
  	def lemma = spl[2]
  	def cpostag = spl[3]
  	def postag = spl[4]
  	def feats = spl[5]
  	def head = spl[6]
  	def deprel = spl[7]
  	def phead = spl[8]
  	def pdeprel = spl[9]

  	def wordV = addWord(g, wid, form, lemma, sentenceV)
  	words[wid] = wordV
  	deprels.push([wid, deprel, head])
      } else {
  	sid += 1

	if (!words.containsKey("0")) {
	  def rootV = addWord(g, "0", "[ROOT]", "", sentenceV)
	  words["0"] = rootV
	}

  	for (rel in deprels) {
  	  // g.addEdge(words[r[0]], words[r[2]], 'head', ['deprel': r[1]])
	  def word1V = words[rel[0]]
	  def deprelStr = rel[1]
	  def word2V = words[rel[2]]
  	  g.addEdge(word1V, word2V, 'head', ['deprel': deprelStr])
  	}
  	deprels = []
  	words = [:]
      }
    }
    g.commit()
  }
}

def GRAPH_LOCATION = "plocal:./db/orientdb/test02"

def fileList = []
new File('./data').eachFileRecurse(FILES) { f ->
  if (f.name.endsWith('.conll')) {
    fileList << f.toString()
  }
}

start(
  // "plocal:/Users/rkn083/mystuff/projects/iln/nodalida_2015/colltools/tools/orientdb-community-2.0.3/databases/test02",
  // ["/Users/rkn083/mystuff/projects/iln/nodalida_2015/colltools/test/SA02SvLe01.txt.short.conll.dep"]
  // ["test/SA02SvLe01.txt.short.conll.dep"]
  GRAPH_LOCATION,
  fileList
)

