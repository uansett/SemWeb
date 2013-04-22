from SPARQLWrapper import SPARQLWrapper, JSON, XML
import rdflib
from rdflib.graph import Graph,  Store,  URIRef,  Literal
from rdflib.namespace import Namespace, RDF, RDFS
from rdflib import plugin
import sys
# The Endpoint configuration
endpoint = SPARQLWrapper("http://dbpedia.org/sparql")
construct_query = '''
PREFIX qm: <http://qmul.ac.uk/sw/g7/ontology#> 
PREFIX dbpo: <http://dbpedia.org/ontology/> 
PREFIX dbpp: <http://dbpedia.org/property/>

CONSTRUCT {
?film a qm:Film .
?film qm:isDirectedBy ?director .
?director a qm:Director .
?film qm:hasBudget ?budget .
?film qm:isDistributedBy ?distributor .
?distributor a qm:Organisation .

}
WHERE{
?film a dbpo:Film . 
?film dbpo:director ?director .
?director a dbpo:Agent . 
?film dbpo:budget ?budget .
?film dbpo:distributor ?distributor .
} LIMIT 1000

'''

endpoint.setQuery(construct_query)

endpoint.setReturnFormat(RDF)
# END Endpoint configuration

rdf_xml_data = '''
@prefix dbpo: <http://dbpedia.org/ontology/> .
@prefix dbpr: <http://dbpedia.org/resource/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix qm: <http://qmul.ac.uk/sw/g7/ontology#> .
@prefix dbpd: <http://dbpedia.org/datatype/> .


dbpr:Quentin_Tarantino a qm:Director .
dbpr:Eric_Toledano a qm:Director .
dbpr:Oliver_Nakache a qm:Director .
dbpr:David_Fincher a qm:Director .

qm:Pulp_Fiction a qm:Film .
qm:Pulp_Fiction rdfs:label "Pulp Fiction" .
qm:Pulp_Fiction qm:hasDirector qm:Quentin_Tarantino .
qm:Pulp_Fiction_Budget a qm:Budget .
qm:Pulp_Fiction qm:hasBudget "185000"^^dbpd:usDollar .

qm:Fear_And_Loathing_In_Las_Vegas a qm:Film .
qm:Fear_And_Loathing_In_Las_Vegas rdfs:label "Fear and Loathing in Las Vegas" .
qm:Fear_And_Loathing_in_Las_Vegas qm:isDirectedBy dbpr:Frank_Darabont .


'''
memory_store = plugin.get('IOMemory', Store)()
graph_id = URIRef(u'http://qmul.ac.uk/sw/g7/store')

rdflib.plugin.register('sparql', rdflib.query.Processor,
                       'rdfextras.sparql.processor', 'Processor')
rdflib.plugin.register('sparql', rdflib.query.Result,
                       'rdfextras.sparql.query', 'SPARQLQueryResult')
g = Graph(store=memory_store, identifier=graph_id) 
g = endpoint.query().convert()
g.parse('ontology2.owl')
g.parse('Frank_Darabont.n3', format='turtle')
g.parse('Grammy_Award_winners.n3', format='turtle') 
g.parse(data=rdf_xml_data, format='turtle')

def runQuery(customQuery=""):
    query = """
    PREFIX qm: <http://qmul.ac.uk/sw/g7/ontology#>
    PREFIX dbprc: <http://dbpedia.org/resource/Category:>
    PREFIX purl: <http://purl.org/dc/terms/>
    PREFIX dbpo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dbpd: <http://dbpedia.org/datatype/>
    PREFIX dbpp: <http://dbpedia.org/property/>

    SELECT ?film ?budget ?director ?organisation WHERE {
        ?film a qm:Film .
        ?film qm:hasBudget ?budget .
        ?film qm:isDirectedBy ?director .
        ?film qm:isDistributedBy ?organisation .
        ?director purl:subject dbprc:Grammy_Award_winners .
    }
    """
    if(customQuery  ==  "i"):
        query = open('input.txt', 'r').read()
        print query

    for row in g.query(query):
        print row


def main():
    print("Welcome. Type i for using the input.txt file for custom queries or just enter for a pre-made query showing films with budget and organisation made by a director who also got a Grammy Award") 
    queryv = raw_input("i or blank: ")
    runQuery(queryv)
    



if  __name__ =='__main__':main()
