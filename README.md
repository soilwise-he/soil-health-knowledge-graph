# Construction of an Ontology-Compliant Soil Health Knowledge Graph with Large Language Models

[cite_start]This repository contains the open-source code and resources for the paper: "Make soil healthy again: Construction of ontology-compliant soil health knowledge graph with large language models".

[cite_start]Our work introduces an ontology-compliant soil health Knowledge Graph (KG) constructed from domain literature, with the assistance of Large Language Models (LLMs) to expedite the process. [cite_start]This KG aims to integrate fragmented soil health knowledge into a structured and semantically rich format.

## About the Project

[cite_start]Soil health is a cornerstone of environmental sustainability and food security. [cite_start]However, the relevant knowledge is often dispersed across various sources, making it difficult to apply effectively. [cite_start]Knowledge Graphs offer a solution by structuring this information.

[cite_start]This project presents a soil health KG that contains 10,707 RDF triples, representing 2,070 entities, including 1,837 soil-related concepts. [cite_start]The KG is aligned with established ontologies and was validated by soil science experts through a series of competency questions.

[cite_start]The primary knowledge source for our KG is the "Soil Monitoring in Europe: Indicators and Thresholds for Soil Health Assessments" report from the European Environment Agency.

## The Knowledge Graph

[cite_start]The soil health KG provides a FAIR (Findable, Accessible, Interoperable, and Reusable) representation of knowledge in the domain.

* [cite_start]**Size**: 10,707 RDF triples, 2,070 entities (1,837 soil-related concepts).
* **Ontologies**: We used a range of ontologies to structure the KG, including:
    * [cite_start]Simple Knowledge Organization System (SKOS) for the conceptual framework.
    * [cite_start]Dublin Core for bibliographic resources.
    * [cite_start]Agrontology, Semanticscience Integrated Ontology, Open Biological and Biomedical Ontology, and others for representing complex relationships.
* [cite_start]**Ontology Extension**: We defined new properties, such as `she:alters` and `she:sequesters`, to capture domain-specific relationships, ensuring all entities and relations have a formal definition.

## Resources

[cite_start]All resources are licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0) license.

* [cite_start]**Knowledge Graph and Ontology Schema**: The soil health KG and its ontology are available for download.
* [cite_start]**HTML Browser**: An HTML page for Browse the concepts and relationships in the KG can be accessed at: [https://soilwise-he.github.io/soil-health](https://soilwise-he.github.io/soil-health)[cite: 244].
* [cite_start]**SPARQL Endpoint**: For programmatic access and querying, a SPARQL endpoint is provided at: [https://repository.soilwise-he.eu/sparql/](https://repository.soilwise-he.eu/sparql/)[cite: 245].
* [cite_start]**Datasets**: The text2KG benchmark dataset and the validation dataset with competency questions are also available.
* [cite_start]**Code and Prompts**: The code for the KG generation pipeline and the prompts used are included in this repository.

## Cite this work

If you use the resources in this repository, please cite our paper:

```bibtex
@inproceedings{wang2025soil,
  title={Make soil healthy again: Construction of ontology-compliant soil health knowledge graph with large language models},
  author={Wang, Beichen and de Sousa, Lu{\'\i}s Moreira and Fensel, Anna},
  year={2025},
  url={[https://doi.org/10.5281/zenodo.14936019](https://doi.org/10.5281/zenodo.14936019)}
}
