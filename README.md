# Make Soil Healthy Again: Construction of an Ontology-Compliant Soil Health Knowledge Graph with Large Language Models

This repository contains the open-source code and datasets for the paper, "Make soil healthy again: Construction of ontology-compliant soil health knowledge graph with large language models."

## Abstract

Soil health is fundamental to environmental sustainability and food security, yet relevant knowledge remains fragmented across diverse sources, hindering its effective application. Knowledge graphs (KGs) offer a robust solution by integrating disparate information into a structured, semantically rich format. Addressing this need, this paper presents an ontology-compliant soil health KG derived from domain literature. Our KG comprises 10,707 RDF triples that represent 2,070 entities (including 1,837 soil-related concepts), aligned with established ontologies. We employed a KG construction pipeline that utilizes large language models to accelerate the construction of such a KG. The resulting KG was validated through its ability to answer a series of competency questions reviewed by soil science experts, and the KG's factual representation was reviewed and confirmed by them as well. Finally, we propose several potential applications for our KG. The KG, ontology schema, and associated datasets are made publicly available.

**Keywords**: knowledge graph, soil health, ontology-compliance, large language models

## Resource Availability

The resources associated with this project are publicly available:

* **Knowledge Graph and Ontology Schema**: The soil health KG and its associated ontology schema are available at [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14936019.svg)](https://doi.org/10.5281/zenodo.14936019).
* **HTML Page**: An HTML page for Browse the concepts and relationships in the KG can be accessed at [https://soilwise-he.github.io/soil-health](https://soilwise-he.github.io/soil-health).
* **SPARQL Endpoint**: For programmatic access and querying, a SPARQL endpoint is provided at [https://repository.soilwise-he.eu/sparql/](https://repository.soilwise-he.eu/sparql/).
* **Datasets and Code**: This repository contains the text2KG benchmark dataset, the validation dataset with Competency Questions (CQs), and the code and prompts for the KG generation pipeline.

## Knowledge Graph Construction Pipeline

We utilized a pipeline that incorporates Large Language Models (LLMs) for the extraction of relevant information from the source text, followed by post-processing and alignment with established ontologies. The construction of our soil health KG was accelerated by using GPT-4o to generate RDF KG segments from selected paragraphs in the EU soil health report.

![Knowledge graph construction pipeline](https://github.com/soilwise-he/soil-health-knowledge-graph/blob/main/figure1.png?raw=true)
*Figure 1: The blue modules indicate manual involvement, while other modules are automated. The green modules represent the use of LLMs. The outputs of LLMs are RDF triples serialized in Turtle.*

## Applications

Our soil health KG has several potential applications:

* **Backbone of a Soil Knowledge Repository**: It can serve as the semantic backbone for a systematic soil knowledge repository, created by interlinking external data and knowledge.
* **KG-based Question Answering**: The validation dataset, which includes natural language CQs, corresponding SPARQL queries, and expected answers, provides a foundation for developing question answering (QA) capabilities.
* **A Benchmark for text2KG**: The dataset, which maps text to ontology-compliant RDF triples, can serve as a benchmark for text-to-knowledge-graph (text2KG) tasks.

## Citation

If you use the resources from this paper, please cite:

```bibtex
@inproceedings{wang2025soil,
  author    = {Beichen Wang and Lu{\'i}s Moreira de Sousa and Anna Fensel},
  title     = {Make soil healthy again: Construction of ontology-compliant soil health knowledge graph with large language models},
  booktitle = {Proceedings of the ISWC 2025 - International Semantic Web Conference},
  year      = {2025}
}
```

## License

All resources related to this project are licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0) license.

## Acknowledgements

This work was supported by the EU's Horizon Europe research and innovation programme within the Soil Wise project (grant agreement ID: 101112838).
