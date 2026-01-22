# v1.1.0 release notes

2026.01.20


AATC v1.1.0 makes a few addition to previous AATC (aatc.ttl) version.

* Instead of including only Getty AAT concepts with both English and Dutch labels, v1.1.0 includes also concepts without Dutch labels.
* scope notes (`skos:scopeNote`) are included with each concept
* source (`dcterms:source`) is included with each concept
* Deprecated terms are also included, and identified with the statements `owl:deprecated true` and `dc:isReplacedBy aatc:XYZ` as recommended by [Skosmos](https://github.com/NatLibFi/Skosmos/wiki/Data-Model). 

Resulting in a total of:

* Active Concepts: 58114
* Active Concepts with Dutch textual labels: 42539
* Deprecated Concepts: 1029

5811
TODO:
- [x] concept definitions/descriptions - in http://vocab.getty.edu/ontology#ScopeNote value nodes
- 
- [x] add dct:source to each concept = vocab.getty.edu
- [x] add dc:source = "getty research institute"
- in the ConceptScheme or dataset, add a mention of the Getty

