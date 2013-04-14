from SPARQLWrapper import SPARQLWrapper, JSON, XML
import rdflib
from rdflib.graph import Graph,  Store,  URIRef,  Literal
from rdflib.namespace import Namespace, RDF, RDFS
from rdflib import plugin

rdf_xml_data = '''
@prefix dbpo: <http://dbpedia.org/ontology/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix qm: <http://www.qmul.ac.uk/semweb/g7/ontology/#> .
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
memory_store = plugin.get('IOMemory', Store)()
graph_id = URIRef(u'http://qmul.ac.uk/semweb/g7/store')

rdflib.plugin.register('sparql', rdflib.query.Processor,
                       'rdfextras.sparql.processor', 'Processor')
rdflib.plugin.register('sparql', rdflib.query.Result,
                       'rdfextras.sparql.query', 'SPARQLQueryResult')
g = Graph(store=memory_store, identifier=graph_id) 
g.parse(data=rdf_xml_data, format='turtle')
g.parse('ontology.owl')

query = """
SELECT * WHERE {
        ?s ?p http://schema.org/Movie .
}
"""
for row in g.query(query):
    print row

for ns in g.namespaces():
    print "Prefix: %s => URI: %s" %ns

for film in g.subjects(object=URIRef("http://shema.org/Movie"),  predicate=None):
    print film
