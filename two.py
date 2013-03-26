from SPARQLWrapper import SPARQLWrapper, JSON 

endpoint = SPARQLWrapper("http://dbpedia.org/sparql")
# This query filters all labels other than the ones in English and Spanish.

endpoint.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    PREFIX dbpr: <http://dbpedia.org/resource/>
    PREFIX dbpo: <http://dbpedia.org/ontology/>

    SELECT ?film_titl
        WHERE { 
        ?film_titl rdf:type dbpo:Film .
        } LIMIT 10 """)

endpoint.setReturnFormat(JSON) 
results = endpoint.query().convert()
for res in results["results"]["bindings"] : 
    print res['film_titl']['value'].encode('utf-8')
