from SPARQLWrapper import SPARQLWrapper, JSON 

endpoint = SPARQLWrapper("http://dbpedia.org/sparql")
# This query filters all labels other than the ones in English and Spanish.

endpoint.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    PREFIX dbpp: <http://dbpedia.org/property/>
    PREFIX dbpr: <http://dbpedia.org/resource/>
    PREFIX dbpo: <http://dbpedia.org/ontology/>
    PREFIX so: <http://schema.org/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema/>
    

    SELECT DISTINCT ?filmTitle ?birthDate ?directorName 
        WHERE { 
        ?film rdf:type dbpo:Film .
        ?film dbpp:name ?filmTitle .
        ?film dbpo:director ?directorResource .
        ?directorResource dbpo:birthName ?directorName .
        ?directorResource dbpp:birthDate ?birthDate .
        FILTER(str(?birthDate)  =  '1963-03-27')
        } LIMIT 1 """)

endpoint.setReturnFormat(JSON) 
results = endpoint.query().convert()

print results

"""for res in results["results"]["bindings"] : 
    pint (res['filmTitle']['value'] + " : " +res['directorName']['value']).encode('utf-8')
    """
