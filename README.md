# Soil health knowledge graph: A demo
### This demo of soil health knowledge graph currently contains:
- A simple "ground-truth" example of converting text to RDF statements;
- Zero-shot and few-shot (one-shot) examples of converting text to RDF with LLMs (OpenAI GPT);
- Visualizing the knowledge graph;
- Evaluating different conversion strategies using the F1 score and exact match;
- Merging and post-processing knowledge graphs to detect duplicates and conflicts;
- Interlinking to external databases using metadata extracted from Zenodo;
  - Filling in keywords extracted from titles and descriptions for metadata entries missing keywords and storing them under the custom namespace "ex:autoSubject".
- Validating the (extended) knowledge graph by question-answering using NLQ.

### To-do:
- Replace the custom namespace "ex:autoSubject" with a more elegant approach to mark AI-generated keywords, such as (singleton) Named Graphs / N-QUADs;
- Find and/or develop better evaluation matrices for semantic matching;
- Introduce domain-specific ontologies, such as GloSIS, in post-processing;
- Try Retrieval-Augmented Generation (RAG) to customize prompts according to the input text;
- Try multi-step pipeline extraction and conversion from text to RDF for comparison;
- Convert tables and figures in the report to RDF statements with multimodal LLMs;
- Better visualization strategies, such as visualizing only concepts and their relations.
