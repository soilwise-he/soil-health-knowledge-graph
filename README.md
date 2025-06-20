# Soil Health Knowledge Graph

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Zenodo DOI](https://zenodo.org/badge/doi/10.5281/zenodo.14936019.svg)](https://doi.org/10.5281/zenodo.14936019)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)

This repository contains the open‑source code, data, and examples supporting the paper:

> **Make soil healthy again: Construction of ontology‑compliant soil health knowledge graph with large language models**
> *B. Wang, L. Moreira de Sousa & A. Fensel*

## ✨ Abstract

Soil health is fundamental to environmental sustainability and food security, yet relevant knowledge remains fragmented across diverse sources, hindering its effective application. Knowledge graphs (KGs) offer a robust solution by integrating disparate information into a structured, semantically rich format. Addressing this need, we present an ontology-compliant **soil health knowledge graph** (SHKG) derived from domain literature. Our KG comprises **10,707 RDF triples** that represent **2,070 entities** (including **1,837 soil-related concepts**), aligned with established ontologies. We employed a KG construction pipeline that utilizes **large language models** (LLMs) to accelerate the construction of such a KG. The resulting KG was validated through its ability to answer a series of competency questions reviewed by soil science experts, and the KG's factual representation was reviewed and confirmed by them as well. Finally, we propose several potential applications for our KG. The KG, ontology schema, and associated datasets are made publicly available here.

---

## 📈 Overview of Core Concepts

Illustration of the core concepts and their relationships in the SHKG:

![Soil Health KG overview](imgs/soil_health_KG.svg)

## 🛠️ Pipeline of KG Construction

We utilized a pipeline that incorporates LLMs for the extraction of relevant information from the source text, followed by post-processing and alignment with established ontologies:

![Text2KG pipeline](imgs/text2KG.svg)

---

## 📦 Repository Contents

```
.
├── LICENSE
├── README.md
├── requirements.txt          # Python dependencies
├── KGC_pipeline.ipynb        # Jupyter notebook demonstrating the full KG‑construction pipeline
├── uk2us.py                  # Utility script (UK ↔ US spelling normalizer)
├── widoco.properties         # Configuration for generating ontology documentation
│
├── top_level_KG.ttl          # Core concepts and their relationships in the SHKG (RDF/Turtle)
├── soil_health_KG.ttl        # Full Soil Health KG (RDF/Turtle)
├── shKG_metadata.ttl         # Metadata describing the KG
├── example_SWR.trig          # Example SoilWise knowledge repository (TriG)
│
├── example_sparql_queries/   # Example SPARQL queries
├── ex_ontovocabs/            # Linked soil-related vocabularies & thesauri
├── in_ontovocabs/            # Imported ontologies & schemas
├── benchmarks/
│   ├── text_RDF_gs.json       # Text-to-RDF gold standard benchmark
│   └── CQs_SPARQL_ea.json     # Competency question, SPARQL query, and expected answer dataset for KG validation
├── imgs/
└── …
```

---

## 🚀 Quick Start

1. **Clone** this repository

   ```bash
   git clone https://github.com/soilwise-he/soil-health-knowledge-graph.git
   cd soil-health-knowledge-graph
   ```

2. **Install** dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. **Explore the KG**

   * Load the main graph in Python or any RDF tool:

     ```python
     from rdflib import Graph
     g = Graph().parse("soil_health_KG.ttl", format="turtle")
     print(len(g), "triples loaded")
     ```

   * Run example SPARQL queries in `example_sparql_queries/` or via the public endpoint at:
     [https://repository.soilwise-he.eu/sparql/](https://repository.soilwise-he.eu/sparql/)

4. **Run the pipeline**
   Open and run `KGC_pipeline.ipynb` to see:

   * LLM‑driven triple generation (via GPT‑4o prompts)
   * Turtle syntax check & repair
   * Ontology alignment, entity normalization & relation disambiguation
   * KG enrichment (invertible relations, external vocabularies)
   * KG validation
   * Example SoilWise knowledge repository (interlink with 200 Zenodo metadata records)

---

## 🔗 Resource Availability

* **Interactive Browser**:  [https://soilwise-he.github.io/soil-health](https://soilwise-he.github.io/soil-health)
* **SPARQL Endpoint**:  [https://repository.soilwise-he.eu/sparql/](https://repository.soilwise-he.eu/sparql/)
* **Searchable Vocabulary Browser**:  [https://voc.soilwise-he.containers.wur.nl/](https://voc.soilwise-he.containers.wur.nl/)

---

## 🔗 Imported Ontologies & Schemas

To ensure our soil health KG aligns with recognized standards, we incorporate a variety of well-established ontologies and schemes.

* [SKOS Core](https://www.w3.org/2009/08/skos-reference/skos.html)
* [Dublin Core](https://www.dublincore.org/specifications/dublin-core/)
* [RDF Schema](https://www.w3.org/TR/rdf-schema/)
* [Agrontology](https://aims.fao.org/aos/agrontology)
* [Semanticscience Integrated Ontology (SIO)](https://sio.semanticscience.org/)
* [Open Biological and Biomedical Ontology (OBO)](https://obofoundry.org/)
* [QUDT](https://qudt.org/)
* [Ontology of Units of Measure (OM)](http://www.ontology-of-units-of-measure.org/resource/om-2/)
* [PROV-O](https://www.w3.org/TR/prov-o/)
* [Schema.org](https://schema.org/)
* [SWEET ontology](http://sweetontology.net/)
* [Wikidata](https://www.wikidata.org/)
* [Biolink Model](https://biolink.github.io/biolink-model/)
* [Allotrope Foundation Ontology](https://www.allotrope.org/ontologies)
* [REPRODUCE-ME Ontology](https://w3id.org/reproduceme)
* [BioAssay Ontology (BAO)](http://bioassayontology.org/)
* [Time Ontology](https://www.w3.org/TR/owl-time/)

The KG leverages **20 classes** and **205 properties** drawn from above ontologies to formally define the types of entities and their relationships. All 20 classes come from existing ontologies, while **45** of the 205 properties are defined by us and the rest come from existing ontologies.

## 🔗 Linked Vocabularies & Thesauri

The KG is enriched by interlinking to controlled vocabularies and thesauri in the field of soil science to align with standard terminologies.

* [AGROVOC](http://aims.fao.org/aos/agrovoc)
* [ISO 11074:2025](https://data.geoscience.earth/ncl/ISO11074v2025)
* [GloSIS ontology](https://glosis-ld.github.io/glosis/)
* [INRAE Thesaurus](http://opendata.inrae.fr/thesaurusINRAE/)
* [GEMET Thesaurus](https://www.eionet.europa.eu/gemet/)

---

## 💡 Applications

1. **Semantic Backbone** for a broader SoilWise knowledge repository, an [example](https://github.com/soilwise-he/soil-health-knowledge-graph/blob/main/example_SWR.trig) of interlinking with 200 Zenodo metadata records is provided.
2. **Natural‑language Question Answering** over the KG via NL → SPARQL
3. **Benchmark** for text2KG: converting scientific text → ontology‑compliant RDF

---

## 🙏 Acknowledgements

This work was supported by the EU's Horizon Europe research and innovation programme within the [SoilWise](https://cordis.europa.eu/project/id/101112838) project (grant agreement ID: 101112838).

## 📝 To-do

See [Issues](https://github.com/soilwise-he/soil-health-knowledge-graph/issues) for planned tasks and enhancements.

---

## 📄 License

* **Code**: MIT License  [See `LICENSE`](./LICENSE)
* **Data & Ontologies**: CC BY 4.0  (Creative Commons Attribution 4.0 International)
