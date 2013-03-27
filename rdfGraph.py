from SPARQLWrapper import SPARQLWrapper, JSON, XML
import rdflib
from rdflib.graph import Graph,  Store,  URIRef,  Literal
from rdflib.namespace import Namespace, RDF, RDFS
from rdflib import plugin

rdf_xml_data = '''
@prefix dbpo: <http://dbpedia.org/ontology/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<http://dbpedia.org/resource/Shakira> a dbpo:Person .
 <http://dbpedia.org/resource/Shakira> rdfs:label "Shakira" .   
'''

memory_store = plugin.get('IOMemory',  Store)()

graph_id = URIRef('http://qmul.ac.uk/semweb/g7')

g = Graph(store=memory_store, identifier=graph_id)
dbpr = Namespace('http://dbpedia.org/resource/')
dbpo = Namespace('http://dbpedia.org/ontology/')
so = Namespace('http//schema.org/')
xsd = Namespace('http://www.w3.org/2001/XMLSchema')

g.bind('dbpr', dbpr)
g.bind('dbpo', dbpo)
g.bind('so', so)
g.bind('xsd', xsd)

""" Adding triples manually """
g.add((dbpr['Bruce Willis'], RDF.type, dbpo['Person']))
g.add((dbpr['Bruce Willis'], RDFS.label, Literal('Bruce Willis')))

print g.serialize(destination=None,  format='turtle', base=None,  encoding=None)

print "Number of triples in the graph: %i" %len(g)
g.parse(data=rdf_xml_data, format="turtle")
print "Number of triples in the graph after parsing the string: %i" %len(g)


"""endpoint = SPARQLWrapper("http://dbpedia.org/sparql")"""





"""
CONSTRUCT{
        ?film rdf:type dbpo:Film .
        ?film dbpp:name ?filmTitle .
        ?film dbpo:director ?directorResource .
        ?directorResource dbpo:birthName ?directorName .
        ?directorResource dbpp:birthDate ?birthDate .
        FILTER(str(?birthDate)  =  '1963-03-27') .
}
WHERE {
        ?film rdf:type dbpo:Film .
        ?film dbpp:name ?filmTitle .
        ?film dbpo:director ?directorResource .
        ?directorResource dbpo:birthName ?directorName .
        ?directorResource dbpp:birthDate ?birthDate .
        FILTER(str(?birthDate)  =  '1963-03-27') .
}
"""