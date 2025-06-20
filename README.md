# Make Soil Healthy Again: Construction of an Ontology-Compliant Soil Health Knowledge Graph with Large Language Models

This repository contains the open-source code, datasets, and documentation for the paper, "Make soil healthy again: Construction of ontology-compliant soil health knowledge graph with large language models."

## Abstract

Soil health is fundamental to environmental sustainability and food security, yet relevant knowledge remains fragmented across diverse sources, hindering its effective application. Knowledge graphs (KGs) offer a robust solution by integrating disparate information into a structured, semantically rich format. Addressing this need, this paper presents an ontology-compliant soil health KG derived from domain literature. Our KG comprises 10,707 RDF triples that represent 2,070 entities (including 1,837 soil-related concepts), aligned with established ontologies. We employed a KG construction pipeline that utilizes large language models to accelerate the construction of such a KG. The resulting KG was validated through its ability to answer a series of competency questions reviewed by soil science experts, and the KG's factual representation was reviewed and confirmed by them as well. Finally, we propose several potential applications for our KG. The KG, ontology schema, and associated datasets are made publicly available.

**Keywords**: knowledge graph, soil health, ontology-compliance, large language models

## Resource Availability

The resources associated with this project are publicly available:

* **Knowledge Graph and Ontology Schema**: The soil health KG and its associated ontology schema are available at [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14936019.svg)](https://doi.org/10.5281/zenodo.14936019).
* **HTML Page**: An HTML page for Browse the concepts and relationships in the KG can be accessed at [https://soilwise-he.github.io/soil-health](https://soilwise-he.github.io/soil-health).
* **SPARQL Endpoint**: For programmatic access and querying, a SPARQL endpoint is provided at [https://repository.soilwise-he.eu/sparql/](https://repository.soilwise-he.eu/sparql/).
* **Datasets and Code**: This repository contains the text2KG benchmark dataset, the validation dataset with Competency Questions (CQs), and the code and prompts for the KG generation pipeline.

## Knowledge Graph Overview

[cite_start]The resulting soil health KG comprises **10,707 RDF triples** [cite: 161][cite_start], describing **2,070 distinct entities**[cite: 161]. [cite_start]The majority of these (1,837) represent soil-related concepts extracted from knowledge sources[cite: 162]. [cite_start]The KG leverages **20 classes and 205 properties** drawn from the selected ontologies to formally define the types of entities and their relationships[cite: 164].

The image below shows an overview of the core concepts and their relationships in the soil health KG:

![Overview of the core concepts and their relationships in the soil health knowledge graph](https://github.com/soilwise-he/soil-health-knowledge-graph/blob/main/imgs/soil_health_KG.svg)

## Pipeline for Constructing the Knowledge Graph

We utilized a pipeline that incorporates Large Language Models (LLMs) for the extraction of relevant information from the source text, followed by post-processing and alignment with established ontologies.

![Pipeline of constructing the knowledge graph](https://github.com/soilwise-he/soil-health-knowledge-graph/blob/main/imgs/text2KG.svg)

## Ontologies and Vocabularies

### Ontologies/Schemas Imported

[cite_start]To ensure our soil health KG aligns with recognized standards, we incorporate a variety of well-established ontologies and schemes. [cite: 59]

- [SKOS Core](https://www.w3.org/2009/08/skos-reference/skos.html)
- [Dublin Core](https://www.dublincore.org/specifications/dublin-core/)
- [RDF Schema](https://www.w3.org/TR/rdf-schema/)
- [Agrontology](https://aims.fao.org/aos/agrontology)
- [Semanticscience Integrated Ontology](https://sio.semanticscience.org/)
- [Open Biological and Biomedical Ontology](https://obofoundry.org/)
- [QUDT](https://qudt.org/)
- [OM](http://www.ontology-of-units-of-measure.org/resource/om-2/)
- [PROV-O](https://www.w3.org/TR/prov-o/)
- [Schema.org](https://schema.org/)
- [SWEET ontology](http://sweetontology.net/)
- [Wikidata](https://www.wikidata.org/)
- [Biolink](https://biolink.github.io/biolink-model/)
- [Allotrope Foundation Ontology](https://www.allotrope.org/ontologies)
- [BioAssay Ontology](http://bioassayontology.org/)
- [Time Ontology](https://www.w3.org/TR/owl-time/)

### Vocabularies/Thesauri Linked

[cite_start]The KG is enriched by interlinking to controlled vocabularies and thesauri in the field of soil science to align with standard terminologies. [cite: 156]

- [AGROVOC](http://aims.fao.org/aos/agrovoc)
- [ISO 11074:2025](https://data.geoscience.earth/ncl/ISO11074v2025)
- [GloSIS ontology](https://glosis-ld.github.io/glosis/)
- [INRAE Thesaurus](http://opendata.inrae.fr/thesaurusINRAE/)
- [GEMET Thesaurus](https://www.eionet.europa.eu/gemet/)

## Applications

Our soil health KG has several potential applications:

* [cite_start]**Backbone of a Soil Knowledge Repository**: It can serve as the semantic backbone for a systematic soil knowledge repository, created by interlinking external data and knowledge. [cite: 195]
* [cite_start]**KG-based Question Answering**: The validation dataset, which includes natural language CQs, corresponding SPARQL queries, and expected answers, provides a foundation for developing question answering (QA) capabilities. [cite: 218]
* [cite_start]**A Benchmark for text2KG**: The dataset, which maps text to ontology-compliant RDF triples, can serve as a benchmark for text-to-knowledge-graph (text2KG) tasks. [cite: 227, 230]

## To-Do

See [Issues](https://github.com/soilwise-he/soil-health-knowledge-graph/issues) for a list of planned features and known issues.

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

[cite_start]All resources related to this project are licensed under the Creative Commons Attribution 4.0 International (CC BY 4.0) license. [cite: 247]

## Acknowledgements

[cite_start]This work was supported by the EU's Horizon Europe research and innovation programme within the Soil Wise project (grant agreement ID: 101112838). [cite: 248]
