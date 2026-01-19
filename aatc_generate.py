#####
# script creates a Getty AAT (https://vocab.getty.edu/aat/)  slim (a) subsection of Getty AAT concepts
# via a SPARQL CONSTRUCT query
# saving the results onto the aatc.ttl file, referred to The Art and Architecture Thesaurus Concepts (AATC)
#   
# Transformation
# AAT gvp:concepts with labels in EN or NL become a skos:Concept with rdfs:label @en @nl
# lang: @en-US is converted to @en 
# AAT concept become members (skos:inScheme) of the http://vocabularies.dans.knaw.nl/aatconcepts skos:ConceptScheme
#####

from SPARQLWrapper import SPARQLWrapper, TURTLE
from datetime import date

prefixes = '''    
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX aat: <http://vocab.getty.edu/aat/>
PREFIX gvp: <http://vocab.getty.edu/ontology#> 
PREFIX gvp_lang: <http://vocab.getty.edu/language/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX skosxl: <http://www.w3.org/2008/05/skos-xl#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX aatc: <http://vocabularies.dans.knaw.nl/aatconcepts/>
'''    

def sparql_query(query):
    '''
    function 
    * receives SPARQL query as input 
    * runs the query against Getty Vocabularies SPARQL endpoint    
    * returns the results in turtle (ttl) format
    '''
    endpoint = "http://vocab.getty.edu/sparql"
    sparql = SPARQLWrapper(endpoint)
    query = prefixes + query     
    sparql.setQuery(query)
    sparql.setReturnFormat(TURTLE)
    results = sparql.query().convert()
    return results


def print_sparql_results(results):
    for row in results["results"]["bindings"]:
        return (row)

today = date.today().strftime("%Y-%m-%d")
version = '1.1.0'
getty_concepts_construct = '''
CONSTRUCT {
    <http://vocabularies.dans.knaw.nl/aatconcepts> a skos:ConceptScheme ;
        dcterms:title "The Art and Architecture Thesaurus Concepts"@en ;
        rdfs:label "The Art and Architecture Thesaurus Concepts"@en ;
        rdfs:comment "The Art and Architecture Thesaurus Concepts (AATC) is a SKOS concept scheme..."@en ;
        dcterms:creator <https://ror.org/008pnp284> , <https://orcid.org/0000-0002-7839-3698> ;
        dcterms:created "%s"^^xsd:date ;
        owl:versionInfo "%s" ;
        dcterms:license <http://opendatacommons.org/licenses/by/1.0/> .

    ?concept a skos:Concept ;
        skos:inScheme <http://vocabularies.dans.knaw.nl/aatconcepts> ;
        skos:prefLabel ?label_fixed_en ;
        skos:prefLabel ?label_literal_nl .

    ?obsolete a skos:Concept ;
        skos:prefLabel ?prefLabel ;
        dcterms:isReplacedBy ?replacement ;
        owl:deprecated true .
}
WHERE {
    # First pattern, for active concepts
    {
        ?concept a gvp:Concept ;
            skos:inScheme aat: ;
            skosxl:prefLabel ?preflabel ;
            gvp:prefLabelGVP ?gpvlabel .
        FILTER( !STRSTARTS(str(?concept), str(gvp_lang:)) )
        ?gpvlabel skosxl:literalForm ?label_literal_en .
        OPTIONAL { ?preflabel  dcterms:language aat:300388256 ; skosxl:literalForm ?label_literal_nl . }
        BIND(
            IF(LANG(?label_literal_en) = "en-us",
                STRLANG(STR(?label_literal_en), "en"),
                ?label_literal_en)
            AS ?label_fixed_en
        )
    }
    # Second pattern, for obsolete subjects
    UNION 
      {
        ?obsolete a gvp:ObsoleteSubject ;
            skos:prefLabel ?prefLabel .
        FILTER( STRSTARTS(str(?obsolete), str(aat:)) )
        ?obsolete  dcterms:isReplacedBy ?replacement .
    }
}
''' % (today, version)


print(getty_concepts_construct)

construct_results = sparql_query(query=getty_concepts_construct)

with open('aatc.ttl', 'wb') as att_subjects_f:
    att_subjects_f.write(construct_results)

