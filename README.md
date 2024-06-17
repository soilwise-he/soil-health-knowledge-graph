# Soil health knowledge graph: A demo
### This demo of soil health knowledge graph currently contains:
- A simple "ground-truth" example of converting text to RDF statements;
- Zero-shot and few-shot (one-shot) examples of converting text to RDF with LLMs (OpenAI GPT);
- Visualizing the knowledge graph;
- Evaluating different conversion strategies using the F1 score and exact match;
- Merging and post-processing knowledge graphs to detect duplicates and conflicts;
- Interlinking to external databases using metadata extracted from Zenodo;
  - Filling in keywords extracted from titles and descriptions for metadata entries missing keywords and storing them under the custom namespace "ex:autoSubject".
- Validating the (extended) knowledge graph by question-answering using NLQ.

### To-do:
See [Issues](https://github.com/soilwise-he/soil-health-knowledge-graph/issues).

### Motivation:
The concept of soil health lacks a universally agreed-upon definition and can vary in interpretation in the context of research versus policymaking. However, within the literature, many factors and indicators are cited as measures of soil health, as highlighted in the European Environment Agency's (EEA) [report](https://op.europa.eu/en/publication-detail/-/publication/1687a21d-9df1-11ed-b508-01aa75ed71a1). Thus, it is advantageous to extract the soil health concepts outlined in this report into a knowledge graph, facilitating systematic organization of this information for machine interpretation and seamless integration with other knowledge repositories. Such a resource would aid users—be they farmers, policymakers, or researchers—in efficiently accessing relevant information, encompassing factors influencing soil health, associated indicators, and their respective normal ranges.

### Ontology:
Currently, the ontology used for the soil health knowledge graph is a combination of the [SKOS Core](https://www.w3.org/2009/08/skos-reference/skos.html), [Dublin Core](https://www.dublincore.org/specifications/dublin-core/), and [RDF schema](https://www.w3.org/TR/rdf-schema/). When using LLMs to convert text to RDF statements, only these common standard ontologies are imported, as these are included in the knowledge of LLMs. Furthermore, since the ontology for describing soils, such as [GloSIS](https://glosis-ld.github.io/glosis/), already exists, the general ontologies will be replaced by the domain-specific ontology during post-processing. Obviously, the specialized ontology is not the knowledge of LLMs, so the inclusion of the domain-specific ontology occurs only in post-processing.
