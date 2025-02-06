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
getty_concepts_construct = '''
CONSTRUCT {
    <http://vocabularies.dans.knaw.nl/aatconcepts> a skos:ConceptScheme ;
        dct:title "The Art and Architecture Thesaurus Concepts"@en ;
        rdfs:label "The Art and Architecture Thesaurus Concepts"@en ;
        rdfs:comment "The Art and Architecture Thesaurus Concepts (AATC) is a SKOS concept scheme that restructures the concepts from the Art and Architecture Thesaurus (AAT) into a flat controlled vocabulary, and excludes non-concepts, such as facets, hierarchies and guide terms. The result is a controlled vocabulary where each term is a skos:Concept, member of aatc: skos:ConceptScheme, with English(@en) and Dutch(@nl) labels. Original URI are kept, and users are encourage to find more information and reference the term through its URI. AATC development was motivated by the need to index AAT terms in a Skosmos server, so that AAT terms could be used easily queried via the Skosmos API and easily used by software applications to classify data with AAT terms"@en ;
        dct:creator <https://ror.org/008pnp284> , <https://orcid.org/0000-0002-7839-3698> ;
        dct:created "%s"^^xsd:date ;
        dcterms:license <http://opendatacommons.org/licenses/by/1.0/> .
        
    ?concept a skos:Concept ;
        skos:inScheme <http://vocabularies.dans.knaw.nl/aatconcepts> ;
        skos:prefLabel ?label_literal_en ;
        skos:prefLabel ?label_literal_nl ;
        dcterms:issued ?issuedDate .
}

WHERE {
    ?concept a gvp:Concept ;
        skos:inScheme aat: ;
        skosxl:prefLabel ?preflabel .
        
    OPTIONAL {?concept dcterms:issued ?issuedDate .}

    { ?preflabel  dcterms:language aat:300388277 ; skosxl:literalForm ?label_literal_en.  } # lang: @en
                 
    UNION

    { ?preflabel  dcterms:language aat:300387822 ; skosxl:literalForm ?label_literal_en_us . 
      BIND (STRLANG(STR(?label_literal_en_us), 'en') AS  ?label_literal_en)} # lang: @en-US - converts to @en
    
    UNION
    
    { ?preflabel  dcterms:language aat:300388256 ; skosxl:literalForm ?label_literal_nl . } # lang: @nl 
    FILTER( STRSTARTS(str(?concept), str(aat:)) )
}
ORDER BY ?concept

'''  % today
print(getty_concepts_construct)

construct_results = sparql_query(query=getty_concepts_construct)

with open('aatc.ttl', 'wb') as att_subjects_f:
    att_subjects_f.write(construct_results)
