from SPARQLWrapper import SPARQLWrapper, JSON, XML
import rdflib
from rdflib.graph import Graph,  Store,  URIRef,  Literal
from rdflib.namespace import Namespace, RDF, RDFS
from rdflib import plugin
endpoint = SPARQLWrapper("http://dbpedia.org/sparql")



rdf_xml_data = '''
@prefix dbpo: <http://dbpedia.org/ontology/> .
@prefix dbpr: <http://dbpedia.org/resource/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix qm: <http://qmul.ac.uk/sw/g7/ontology#> .
@prefix so: <http://schema.org/> .


dbpr:Quentin_Tarantino a qm:Director .
dbpr:Eric_Toledano a qm:Director .
dbpr:Oliver_Nakache a qm:Director .
dbpr:David_Fincher a qm:Director .


qm:Pulp_Fiction a qm:Film .
qm:Pulp_Fiction rdfs:label "Pulp Fiction" .
qm:Pulp_Fiction qm:hasDirector qm:Quentin_Tarantino .
qm:Pulp_Fiction_Budget a qm:Budget .
qm:Pulp_Fiction qm:hasBudget qm:Pulp_Fiction_Budget .
qm:Pulp_Fiction_Budget qm:hasValue "185000"^^rdfs:float .

qm:Fear_And_Loathing_In_Las_Vegas a qm:Film .
qm:Fear_And_Loathing_In_Las_Vegas rdfs:label "Fear and Loathing in Las Vegas" .

<http://dbpedia.org/resource/Frank_Darabont> qm:hasDirected qm:Fear_And_Loathing_in_Las_Vegas .

'''
memory_store = plugin.get('IOMemory', Store)()
graph_id = URIRef(u'http://qmul.ac.uk/sw/g7/store')

rdflib.plugin.register('sparql', rdflib.query.Processor,
                       'rdfextras.sparql.processor', 'Processor')
rdflib.plugin.register('sparql', rdflib.query.Result,
                       'rdfextras.sparql.query', 'SPARQLQueryResult')
g = Graph(store=memory_store, identifier=graph_id) 
g.parse('ontology2.owl')
g.parse('Frank_Darabont.n3', format='turtle')
g.parse('Grammy_Award_winners.n3', format='turtle') 
g.parse(data=rdf_xml_data, format='turtle')

query = """
PREFIX qm: <http://qmul.ac.uk/sw/g7/ontology#>
PREFIX dbpr: <http://dbpedia.org/resource/>
PREFIX purl: <http://purl.org/dc/terms/>

SELECT ?person WHERE {
        ?person rdf:type qm:Director .
        ?person <http://purl.org/dc/terms/subject> <http://dbpedia.org/resource/Category:Grammy_Award_winners> .
}
"""
for row in g.query(query):
    print row

#for ns in g.namespaces():
#    print "Prefix: %s => URI: %s" %ns

#for film in g.subjects(object=URIRef("http://qmul.ac.uk/sw/g7/ontology#Film"),  predicate=None):
#    print film
