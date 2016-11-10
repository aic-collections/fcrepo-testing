from rdflib.graph import Graph
from rdflib import Namespace, URIRef, Literal

class GraphOperation:
    
    def __init__(self, config):
        self.config = config
    
    def fetchRDF(self, rdffile):
        '''Open RDF file and modify URIs'''
        rdf = ''
        with open(rdffile) as f:
            for line in f:
                l = line.replace('%BASE%', self.config['fcrepo']['base'])
                l = l.replace('%BASE_NOSLASH%', self.config['fcrepo']['base'][:-1])
                rdf = rdf + l
        return rdf
    
    def loadGraph(self, rdffile):
        '''Load RDF into graph'''
        rdf = self.fetchRDF(rdffile)
        self.g = Graph()
        self.g.parse(data=rdf, format="xml")
    
    def getSubjects(self, limit):
        '''SUBJECTS generator'''
        q = "SELECT DISTINCT ?s WHERE { ?s <http://www.w3.org/2004/02/skos/core#prefLabel> ?o . }"
        if int(limit) > 0:
            q = q + " LIMIT " + str(limit)
        results = self.g.query(q)
        subjects = []
        for subject in results:
            s = subject.s.__str__()
            subjects.append(s)
        return subjects