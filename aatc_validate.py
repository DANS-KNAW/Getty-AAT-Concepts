from pyshacl import validate
from rdflib import Graph

data = Graph()
data.parse("aatc.ttl")

shacl = Graph()
shacl.parse("aatc_shacl.ttl")

r = validate(data,
      shacl_graph=shacl,
      ont_graph=None,
      inference='rdfs',
      abort_on_first=False,
      allow_infos=False,
      allow_warnings=False,
      meta_shacl=False,
      advanced=False,
      js=False,
      debug=False)
conforms, results_graph, results_text = r
print(conforms)

assert conforms is True, f"ERROR: {results_text}" 