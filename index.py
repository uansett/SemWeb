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

endpoint.setQuery(construct_query%{'uri':"http://dbpedia.org/resource/Asturias"})
endpoint.setReturnFormat(XML)

graph = endpoint.query().convert()

'''
for s, p, o in graph:
    print s.encode('utf-8'), p.encode('utf-8'), o.encode('utf-8')
'''

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

query = graph.query("""
        PREFIX dbpo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?location ?party ?leader
        WHERE {
        <http://dbpedia.org/resource/Asturias> rdfs:label ?location .
        <http://dbpedia.org/resource/Asturias> dbpo:leaderName ?leaderResource .
        ?leaderResource rdfs:label ?leader .
        <http://dbpedia.org/resource/Asturias> dbpo:leaderParty ?partyResource .
        ?partyResource rdfs:label ?party .
        FILTER(LANG(?location)="%(lang)s" && LANG(?party)="%(lang)s" && LANG(?leader)="%(lang)s") .}""" %{'lang':Language})

print "RESULTS:"

for row in query.result:
    print(("The leader party of %s is %s who's leader is %s." % row).encode('utf-8'))

