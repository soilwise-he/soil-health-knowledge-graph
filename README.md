# Soil health knowledge graph: A demo
This demo of soil health knowledge graph currently contains:
- A simple "ground-truth" example of converting text to RDF statements;
- Zero-shot and few-shot (one-shot) examples of converting text to RDF statements with LLMs (OpenAI GPT);
- Visualizing RDF knowledge graphs;
- Evaluating different conversion strategies using F1 score and Exact Match;
- Merging and post-processing knowledge graphs to detect duplicates and conflicts;
- Interlinking to external databases using metadata extracted from Zenodo;
  - Filling in keywords extracted from titles and descriptions for metadata entries missing keywords and storing under the custom namespace "ex:autoSubject".
- Validating the (extended) knowledge graph by question answering using NLQ.

To-do:
- Replace the custom namespace "ex:autoSubject" with more elegant approach, such as (singleton) Named Graphs / N-QUADs;
- Find / Develop better evaluation matrics for semantic matching;
- Try Retrieval-Augmented Generation (RAG) technique for ;
- Try multi-step pipeline extraction and conversion from text to RDF for comparison;
- Also convert tables & figures to RDF statements with multimodel LLMs;
