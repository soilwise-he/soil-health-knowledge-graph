# Ontology-Compliant Soil Health Knowledge Graph

This repository contains the open-source code and resources for the paper: "Make soil healthy again: Construction of ontology-compliant soil health knowledge graph with large language models".

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14936019.svg)](https://doi.org/10.5281/zenodo.14936019)

## Overview

Soil health is crucial for environmental sustainability and food security, but knowledge about it is spread across many different sources. This makes it hard to use this knowledge effectively. Knowledge graphs (KGs) can solve this problem by organizing information in a structured way. This project presents a soil health KG created from scientific literature to address this issue.

Our KG is made up of 10,707 RDF triples that describe 2,070 entities, including 1,837 concepts related to soil. The KG was built using a pipeline that employs large language models (LLMs) to speed up the process. We worked with soil science experts to make sure the information in the KG is accurate. The KG's ability to answer relevant questions was also tested and confirmed by these experts.

## Key Features

* **Ontology-Compliant:** The KG aligns with established ontologies to ensure structured and semantically rich data.
* **Expert-Validated:** Soil science experts reviewed and confirmed the factual representation and accuracy of the KG.
* **LLM-Powered Construction:** We used a pipeline with LLMs to efficiently extract information from text.
* **Richly Interlinked:** The KG is linked to external vocabularies and thesauri like AGROVOC, GloSIS, and ISO 11074.

## Knowledge Graph Details

* **Total RDF Triples:** 10,707
* **Total Entities:** 2,070
    * **Soil-Related Concepts:** 1,837
    * **Bibliographic References:** 158
    * **Other Entities:** Policies, standards, geographical regions, etc.
* **Classes and Properties:** 20 classes and 205 properties from selected ontologies.

## Knowledge Graph Construction

The KG was built using a pipeline that includes the following steps:

1.  **Knowledge Source Pre-processing:** The main source of information was the "Soil Monitoring in Europe: Indicators and Thresholds for Soil Health Assessments" report from the European Environment Agency.
2.  **KG Generation with LLMs:** We used GPT-4o to generate RDF triples from the text. This process included steps to handle complex statements with blank nodes and to validate and repair the Turtle syntax.
3.  **KG Post-processing:** This manual and automated step involved aligning the KG with ontologies, integrating different KG segments, normalizing entities, and disambiguating relationships with the help of soil scientists.
4.  **KG Enrichment:** We added inverse properties to complete the KG and linked it to external vocabularies using `skos:exactMatch` and `skos:closeMatch`.

## Resources

* **HTML Page:** You can browse the concepts and relationships in the KG here: [https://soilwise-he.github.io/soil-health](https://soilwise-he.github.io/soil-health)
* **SPARQL Endpoint:** For programmatic access and querying, the SPARQL endpoint is available at: [https://repository.soilwise-he.eu/sparql/](https://repository.soilwise-he.eu/sparql/)
* **Datasets:** The KG, ontology schema, text2KG benchmark dataset, and validation dataset with competency questions are available in this repository and on Zenodo.

## Applications

This soil health KG can be used for several purposes:

* **Backbone of a Soil Knowledge Repository:** The KG can serve as the foundation for a larger repository of soil-related data and knowledge.
* **KG-Based Question Answering:** The dataset of competency questions and SPARQL queries can be used to develop a natural language querying system.
* **A Benchmark for text2KG:** The dataset of text segments and their corresponding RDF triples can be used to test and evaluate text-to-knowledge-graph models.
