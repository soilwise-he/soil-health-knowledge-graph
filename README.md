# Soil health knowledge graph: A demo
### This demo of soil health knowledge graph currently contains:
- A simple "ground-truth" example of converting text to RDF statements;
- Zero-shot and few-shot (one-shot) examples of converting text to RDF with LLMs (OpenAI GPT);
- Interlinking concepts from the soil health knowledge graph with the [AGROVOC](https://aims.fao.org/aos/agrovoc) Thesaurus;
- Visualizing the knowledge graph;
- Evaluating different conversion strategies using the F1 score and exact match;
- Merging and post-processing knowledge graphs to detect duplicates and conflicts;
- Interlinking to external databases, such as soil-related metadata records harvested from Zenodo, by keyword matching;
  - Filling in keywords generated from the title and description for metadata records that are missing keywords;
  - Introducing a quad-store with named graphs to store generated keywords in the named graph called "generated";
  - Storing concepts from the soil health knowledge graph in the named graph "concept" and raw metadata records in the named graph "metadata".
- Validating the (expanded) knowledge graph by question-answering using NLQ.

### To-do:
See [Issues](https://github.com/soilwise-he/soil-health-knowledge-graph/issues).

### Motivation:
The concept of soil health lacks a universally agreed-upon definition and can vary in interpretation in the context of research versus policymaking. However, within the literature, many factors and indicators are cited as measures of soil health, as highlighted in the European Environment Agency's (EEA) [report](https://op.europa.eu/en/publication-detail/-/publication/1687a21d-9df1-11ed-b508-01aa75ed71a1). Thus, it is advantageous to extract the soil health concepts outlined in this report into a knowledge graph, facilitating systematic organization of this information for machine interpretation and seamless integration with other knowledge repositories. Such a resource would aid users—be they farmers, policymakers, or researchers—in efficiently accessing relevant information, encompassing factors influencing soil health, associated indicators, and their respective normal ranges.

Once we establish this soil health knowledge graph, we aim to enhance it by interlinking a vast array of external data and knowledge to create a comprehensive soil knowledge repository. A primary method for integrating external data involves keyword matching, where each concept within the graph serves as a keyword. These keywords allow us to search and link metadata from external databases, literature, and other web resources back to the corresponding concepts in the knowledge graph.

Building this knowledge repository in a top-down manner, guided by the structure of the knowledge graph, offers several advantages. The top-down approach provides a more controllable and orderly construction process compared to bottom-up methods, enhancing the ease of knowledge sharing, including improved reuse of information. Furthermore, because the repository structurally aligns with the knowledge graph, with external data directly linked to its concepts, the repository becomes more functional for applications. For example, understanding the relationships between concepts is crucial when developing a recommender system that operates over the knowledge repository.

### Ontologies:
Currently, ontologies used for the soil health knowledge graph is a combination of the [SKOS Core](https://www.w3.org/2009/08/skos-reference/skos.html) and [Dublin Core](https://www.dublincore.org/specifications/dublin-core/). When using LLMs to convert text to RDF statements, only these common standard ontologies are imported, as these are internal knowledge of LLMs. Furthermore, since domain-specific ontologies, such as [GloSIS](https://glosis-ld.github.io/glosis/) and [Agrontology](https://aims.fao.org/aos/agrontology), already exists, the generic ontologies will be partially replaced by these domain-specific ontologies.
