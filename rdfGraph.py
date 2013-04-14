from SPARQLWrapper import SPARQLWrapper, JSON, XML
import rdflib
from rdflib.graph import Graph,  Store,  URIRef,  Literal
from rdflib.namespace import Namespace, RDF, RDFS
from rdflib import plugin

rdf_xml_data = '''
@prefix dbpo: <http://dbpedia.org/ontology/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix qm: <http://www.qmul.ac.uk/semweb/g7/ontology/> .
@prefix so: <http://schema.org/> .


qm:Quentin_Tarantino a qm:Director .
qm:Eric_Toledano a qm:Director .
qm:Oliver_Nakache a qm:Director .
qm:David_Fincher a qm:Director .



qm:Pulp_Fiction a qm:Film .
qm:Pulp_Fiction rdfs:label "Pulp Fiction" .
qm:Pulp_Fiction qm:hasDirector qm:Quentin_Tarantino .
qm:Pulp_Fiction qm:hasBudget "1850000"^^qm:Budget .


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


print g.serialize(destination=None,  format='turtle', base=None,  encoding=None)

print "Number of triples in the graph: %i" %len(g)
g.parse(data=rdf_xml_data, format="turtle")
print "Number of triples in the graph after parsing the string: %i" %len(g)
print "Number of triples in the graph after parsing the string: %i" %len(g)


"""endpoint = SPARQLWrapper("http://dbpedia.org/sparql")"""

print g.serialize(destination=None,  format='turtle', base=None,  encoding=None)

print ("TRYING TO QUERY THE LOCAL RDF STORE:")

result = g.query("""
    PREFIX dbpo: <http://dbpedia.org/ontology/> 
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    PREFIX qm: <http://www.qmul.ac.uk/semweb/g7/ontology/> 
    PREFIX so: <http://schema.org/> 

    SELECT ?x ?y
    WHERE{
        ?x qm:hasDirector qm:Quentin_Tarantino .
        ?x rdfs:label ?y .
    }

""")

for row in result.result:
    print(("%s %s" % row).encode('utf-8'))

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
