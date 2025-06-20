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

## 📦 Repository Contents

```

.
├── LICENSE
├── README.md
├── requirements.txt          # Python dependencies
├── KGC\_pipeline.ipynb        # Jupyter notebook demonstrating the full KG‑construction pipeline
├── uk2us.py                  # Utility script (UK ↔ US spelling normalizer)
├── widoco.properties         # Configuration for generating ontology documentation
│
├── top\_level\_KG.ttl          # Top‑level schema (RDF/Turtle)
├── soil\_health\_KG.ttl        # Full Soil Health KG (RDF/Turtle)
├── shKG\_metadata.ttl         # Metadata describing the KG
├── example\_SWR.trig          # Example serialization (TriG)
│
├── example\_sparql\_queries/   # SPARQL queries & usage examples
├── ex\_ontovocabs/            # Example ontology‐vocabulary alignments
├── in\_ontovocabs/            # Ontology vocabulary imports
├── benchmarks/               # text2KG benchmark dataset and scripts
├── imgs/                     # Diagrams & figures
└── …

````

---

## 🚀 Quick Start

1. **Clone** this repository  
   ```bash
   git clone https://github.com/soilwise-he/soil-health-knowledge-graph.git
   cd soil-health-knowledge-graph
````

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

## 🔗 Resources

* **Zenodo DOI & Data Archive**:
  [https://doi.org/10.5281/zenodo.14936019](https://doi.org/10.5281/zenodo.14936019)
* **Interactive Browser**:
  [https://soilwise-he.github.io/soil-health](https://soilwise-he.github.io/soil-health)
* **SPARQL Endpoint**:
  [https://repository.soilwise-he.eu/sparql/](https://repository.soilwise-he.eu/sparql/)

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
Please see [CONTRIBUTING.md](./CONTRIBUTING.md) (if you add one) or open an issue.

---

## 📄 License

* **Code**: MIT License  [See `LICENSE`](./LICENSE)
* **Data & Ontologies**: CC BY 4.0  (Creative Commons Attribution 4.0 International)

---

```

**Next steps**  
- Add a `CONTRIBUTING.md` if you expect outside collaborators.  
- Embed badges (e.g. CI status, Python versions, code coverage) as you set up workflows.  
- Update any paths or descriptions once you finalize scripts or data locations.
