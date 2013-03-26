from SPARQLWrapper import SPARQLWrapper, JSON 

endpoint = SPARQLWrapper("http://dbpedia.org/sparql")
# This query filters all labels other than the ones in English and Spanish.

endpoint.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    PREFIX dbpp: <http://dbpedia.org/property/>
    PREFIX dbpr: <http://dbpedia.org/resource/>
    PREFIX dbpo: <http://dbpedia.org/ontology/>
    PREFIX so: <http://schema.org/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    

    SELECT DISTINCT ?film ?birthDate ?directorResource
        WHERE { 
        ?film rdf:type dbpo:Film .
        ?film dbpo:director ?directorResource .
        ?directorResource rdfs:label "Quentin Tarantino"@en .
        ?directorResource dbpp:birthDate ?birthDate .
        } LIMIT 100 """)

endpoint.setReturnFormat(JSON) 
results = endpoint.query().convert()
for res in results["results"]["bindings"] : 
    print res['birthDate']['value'].encode('utf-8')
