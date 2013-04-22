#!/usr/bin/env python
# -*- coding: utf-8 -*-

from SPARQLWrapper import SPARQLWrapper,  JSON,  XML

import rdflib
from rdflib.graph import Graph
from rdflib.namespace import Namespace
from rdflib import plugin

endpoint = SPARQLWrapper("http://dbpedia.org/sparql")

"""
PART 1: Build a local RDF graph using a Construct query over DBpedia
"""

construct_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

CONSTRUCT {
<%(uri)s> a ?type .
<%(uri)s> ?property ?value .
<%(uri)s> rdfs:label ?label .
?value rdfs:label ?vlabel .
?property rdfs:label ?plabel . }

WHERE {
<%(uri)s> a ?type.
<%(uri)s> ?property ?value .
    <%(uri)s> rdfs:label ?label .
    ?value rdfs:label ?vlabel .
?property rdfs:label ?plabel . }"""

endpoint.setQuery(construct_query%{'uri':"http://dbpedia.org/resource/Film"})
endpoint.setReturnFormat(XML)

graph = Graph()
graph = endpoint.query().convert()


for s, p, o in graph:
    print s.encode('utf-8'), p.encode('utf-8'), o.encode('utf-8')


"""
PART 2: query the resulting resulting RDF graph
"""
plugin.register(
        'sparql',  rdflib.query.Processor, 
        'rdfextras.sparql.processor',  'Processor')
plugin.register(
        'sparql', rdflib.query.Result, 
        'rdfextras.sparql.query', 'SPARQLQueryResult')

Language = 'en'

#query = graph.query("""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#
#SELECT DISTINCT ?film_title ?film_abstract
#WHERE {
#?film_title rdf:type <http://dbpedia.org/ontology/Film> .
#?film_title rdfs:comment ?film_abstract .
#} LIMIT 1000 OFFSET 0""")        
        
#print "RESULTS:"

#for row in query.result:
#    print(("%s %s" % row).encode('utf-8'))

