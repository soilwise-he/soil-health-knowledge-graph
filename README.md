# Soil Health Knowledge Graph

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Zenodo DOI](https://zenodo.org/badge/doi/10.5281/zenodo.14936019.svg)](https://doi.org/10.5281/zenodo.14936019)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)

This repository contains the open‑source code, data, and examples supporting the paper:

> **Make soil healthy again: Construction of ontology‑compliant soil health knowledge graph with large language models**
> *B. Wang, L. Moreira de Sousa & A. Fensel*
> *ISWC 2025*

Our work produces an ontology‑compliant **Soil Health Knowledge Graph** (SHKG) of over 10 700 RDF triples, derived from major soil‑health literature via a mixed pipeline of LLM‑assisted extraction and expert curation.

---

## 📈 Overview of Core Concepts

Illustration of the core concepts and their relationships in the SHKG:

![Soil Health KG overview](imgs/soil_health_KG.svg)

## 🛠️ Pipeline of KG Construction

End‑to‑end pipeline from text to knowledge graph:

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
├── top_level_KG.ttl          # Top‑level schema (RDF/Turtle)
├── soil_health_KG.ttl        # Full Soil Health KG (RDF/Turtle)
├── shKG_metadata.ttl         # Metadata describing the KG
├── example_SWR.trig          # Example serialization (TriG)
│
├── example_sparql_queries/   # SPARQL queries & usage examples
├── ex_ontovocabs/            # Example ontology‐vocabulary alignments
├── in_ontovocabs/            # Ontology vocabulary imports
├── benchmarks/               # text2KG benchmark dataset and scripts
├── imgs/                     # Diagrams & figures
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
   * Run example SPARQL queries in `example_sparql_queries/` or via the public endpoint.

4. **Run the pipeline**
   Open and run `KGC_pipeline.ipynb` to see:

   * Document pre‑processing
   * LLM‑driven triple extraction (via GPT‑4o prompts)
   * Turtle repair & validation
   * Ontology alignment, entity normalization & relation disambiguation
   * KG enrichment (inverses, SKOS mappings, external vocabularies)

---

## 🔗 Imported Ontologies & Schemas

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

## 🔗 Linked Vocabularies & Thesauri

* [AGROVOC](http://aims.fao.org/aos/agrovoc)
* [ISO 11074:2025](https://data.geoscience.earth/ncl/ISO11074v2025)
* [GloSIS ontology](https://glosis-ld.github.io/glosis/)
* [INRAE Thesaurus](http://opendata.inrae.fr/thesaurusINRAE/)
* [GEMET Thesaurus](https://www.eionet.europa.eu/gemet/)

---

## 💡 Applications

1. **Semantic Backbone** for a broader SoilWise knowledge repository
2. **Natural‑language Question Answering** over the KG via NL → SPARQL
3. **Benchmark** for text2KG: mapping scientific text → ontology‑compliant RDF

---

## 📝 How to Cite

```bibtex
@inproceedings{wang2025soil,
  author    = {Beichen Wang and Luís Moreira de Sousa and Anna Fensel},
  title     = {Make soil healthy again: Construction of ontology-compliant soil health knowledge graph with large language models},
  booktitle = {Proceedings of the ISWC 2025 – International Semantic Web Conference},
  year      = {2025}
}
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
See [CONTRIBUTING.md](./CONTRIBUTING.md) or open an [issue](https://github.com/soilwise-he/soil-health-knowledge-graph/issues).

## 📝 To-do

See [Issues](https://github.com/soilwise-he/soil-health-knowledge-graph/issues) for planned tasks and enhancements.

---

## 📄 License

* **Code**: MIT License  [See `LICENSE`](./LICENSE)
* **Data & Ontologies**: CC BY 4.0  (Creative Commons Attribution 4.0 International)
