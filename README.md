# Soil health knowledge graph: A demo

## This demo of soil health knowledge graph currently contains

![image](https://github.com/soilwise-he/soil-health-knowledge-graph/blob/main/LLM4KG.svg)

## To-do

See [Issues](https://github.com/soilwise-he/soil-health-knowledge-graph/issues).

## Motivation

The concept of soil health lacks a universally agreed-upon definition and can vary in interpretation in the context of research versus policymaking. However, within the literature, many factors and indicators are cited as measures of soil health, as highlighted in this European Environment Agency's (EEA) [report](https://www.eea.europa.eu/publications/soil-monitoring-in-europe). Thus, it is advantageous to extract the soil health concepts outlined in this report into a knowledge graph, facilitating systematic organization of these knowledge for machine interpretation and allowing for integration with other knowledge repositories. Such a resource would aid users—be they farmers, policymakers, or researchers—in efficiently accessing relevant information, encompassing factors influencing soil health, associated indicators, and their respective normal ranges.

Once we establish this soil health knowledge graph, we aim to enhance it by interlinking a vast array of external data and knowledge to create a soil knowledge repository. A primary method for integrating external data involves keyword matching, where each concept within the graph serves as a keyword. These keywords allow us to search and link metadata from external databases, literature, and other web resources back to the corresponding concepts in the knowledge graph. This process depends on keyword extraction techniques to supplement metadata entries that are missing keywords.

Building this knowledge repository in a top-down manner, guided by the structure of the knowledge graph, offers several advantages. The top-down approach provides a more controllable and orderly construction process compared to bottom-up methods, enhancing the ease of knowledge sharing, including improved reuse of knowledge. Furthermore, because the repository structurally aligns with the knowledge graph, with external data directly linked to its concepts, the repository becomes more functional for applications. For example, understanding the relationships between concepts is crucial when developing a recommender system that operates over the knowledge repository.

## Ontologies/Vocabularies/Schemas used

- [SKOS Core](https://www.w3.org/2009/08/skos-reference/skos.html)
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/)
- [AGROVOC](https://aims.fao.org/aos/agrovoc)
- [GloSIS](https://glosis-ld.github.io/glosis/)
- [Agrontology](https://aims.fao.org/aos/agrontology)
- [QUDT](https://qudt.org/)
- [EuroVoc](https://op.europa.eu/en/web/eu-vocabularies)
