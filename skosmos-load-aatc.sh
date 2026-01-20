#!/bin/bash

AAT_CONF=$':AATC a skosmos:Vocabulary, void:Dataset ;
dc:title "The Art and Architecture Thesaurus Concepts"@en ;
skosmos:shortName "AATC";
dc:subject :cat_general ;
void:uriSpace "http://vocabularies.dans.knaw.nl/";
skosmos:language "en", "nl";
skosmos:defaultLanguage "en";
skosmos:showTopConcepts false ;
skosmos:fullAlphabeticalIndex true ;
skosmos:groupClass isothes:ConceptGroup ;
void:sparqlEndpoint <http://fuseki-cache:80/skosmos/sparql> ; 
skosmos:sparqlGraph <http://vocabularies.dans.knaw.nl/aatconcepts/> .'

# clone skosmos
git clone --depth 1 -b v3.0 https://github.com/NatLibFi/Skosmos.git 
# append to aatc config for skosmos (original: https://github.com/DANS-KNAW/dans-core-systems/blob/e12619520b3f48ab4a3d46bc09bc79cb5c3dd1b2/provisioning/files/vocabs/aatc.conf)
echo "$AAT_CONF" >> Skosmos/dockerfiles/config/config-docker-compose.ttl
# start docker containers # more on Skosmos containers in Skosmos/dockerfiles/README.md
cd Skosmos
docker compose up -d

sleep 2
cd ..
# Load aatc.ttl to Fuseki on graph http://vocabularies.dans.knaw.nl/aatconcepts/
curl -X POST -H "Content-Type: text/turtle" -T aatc.ttl "http://localhost:9030/skosmos/data?graph=http://vocabularies.dans.knaw.nl/aatconcepts/"

echo "AATC in Skosmos: http://localhost:9090/AATC"

