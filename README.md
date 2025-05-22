
# Getty - Art and Architecture Thesaurus (AAT) - Analysis and Generation of *slim* AATC

## Report
See https://doi.org/10.5281/zenodo.15487726

## the Getty AAT Landscape Analysis

### Analysis Structure 
- [`gettyOverview.ipynb`](gettyOverview.ipynb) contains an overview of the following of the main conceptual and technical aspects of Getty AAT and ULAN
- [`AAT_concepts.ipynb`](AAT_concepts.ipynb) delves into the semantic anatomy of a AAT concept; And explain how AAT hierarchies are created.
- `resources.md`(resources.md) provides a list of the documentation that was consulted in the process of creating the landscape analysis. 

### Setup
If you want to be able to execute the code in this repository, please take note of the following: 
- This notebook is written with the assumption that you run it in [Visual Studio Code](https://code.visualstudio.com/), with the following extensions: Python, SPARQL Executor, and REST Client. Some functionality may otherwise not be available.
- Please install the packages that are specified in `requirements.txt`(requirements.txt). 


## Generate:Art and Architecture Thesaurus Concepts (AATC) - Controlled Vocabulary

The Art and Architecture Thesaurus Concepts (AATC) is a *slim*, or a subsection of Getty AAT concepts. 

In more technical terms, the AATC is a SKOS concept scheme that restructures the concepts from the Art and Architecture Thesaurus (AAT) into a flat controlled vocabulary, and excludes non-concepts, such as facets, hierarchies and guide terms. 
The result is a controlled vocabulary where each term is a `skos:Concept`, member of `aatc: skos:ConceptScheme`, with English(@en) and Dutch(@nl) labels. 

Original URIs are kept, and users are encourage to find more information and reference the term through its URI. 

Output: [aatc.ttl](aatc.ttl) 

### Motivation 

AATC development was motivated by the need to index AAT terms in a Skosmos server, so that AAT terms could be used easily queried via the Skosmos API and easily used by software applications to classify data with AAT terms.

Since our current use-cases, that called for the us of AAT concepts, were not concerned with parent/child relation between concepts, we have decided to remove the hierarchical relations of AAT. Instead, we focused on creating a flat controlled vocabulary, containing all concepts that included both English and Dutch labels.

### AATC Creation & Validation

The Jupyter notebook [aatc_generation.ipynb](aatc_generation.ipynb) documents the AATC generation process, via `CONSTRUCT` SPARQL query, that transforms the query result onto a new structure, saved in the RDF based turtle (.ttl) format and can be seen in [aatc.ttl](aatc.ttl) (~8Mb).

The script **[aatc_generate.py](aatc_generate.py)** only performs the generation of the AATC.
* requirements: [SPARQLWrapper](https://sparqlwrapper.readthedocs.io/en/latest/) 

The script **[aatc_validate.py](aatc_validate.py)** only performs the validation of the AATC agains the [aatc_shacl.ttl](aatc_shacl.ttl) SHACL rules. If the validation fails, script will output an AssertionError 
* requirements: [rdflib](https://rdflib.readthedocs.io/en/stable/), [pyshacl](https://github.com/RDFLib/pySHACL)
* also possible to run shape with [Apache Jena's SHACL command](https://jena.apache.org/documentation/shacl/) `shacl v --shapes aatc_shacl.ttl --data aatc.ttl`

