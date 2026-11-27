"""Bidirectional Graph Similarity (Lermanda et al., ESWC 2026, §3.1).

https://doi.org/10.1007/978-3-032-25156-5_2
Both scores are distances. A lower value indicates closer alignment.
"""

import re
from functools import cache
from pathlib import Path
from typing import NamedTuple

import nltk
import numpy as np
from nltk.tokenize.punkt import PunktSentenceTokenizer, load_punkt_params
from rdflib import BNode
from scipy.spatial.distance import cdist


class BIGSScore(NamedTuple):
    coverage: float  # source sentence to its closest triple
    fidelity: float  # triple to its closest source sentence


@cache
def _english_tokenizer():
    cache_dir = str(Path('.cache/nltk_data').resolve())
    if cache_dir not in nltk.data.path:
        nltk.data.path.append(cache_dir)
    resource = 'tokenizers/punkt_tab/english/'
    try:
        directory = nltk.data.find(resource)
    except LookupError:
        nltk.download('punkt_tab', download_dir=cache_dir, quiet=True, raise_on_error=True)
        directory = nltk.data.find(resource)
    params = load_punkt_params(directory)
    # Keep in-text citations and common scientific abbreviations in their sentence.
    params.abbrev_types.update({'al', 'e.g', 'i.e', 'fig', 'figs', 'eq'})
    return PunktSentenceTokenizer(params)


_LIST_MARKER = re.compile(r'^(?:[•●▪‣]|[-*]|\d+[.)])\s+')


def source_sentences(paragraph: str) -> list[str]:
    """Split sentences and list items, attaching a colon-ended lead-in to each item."""
    lines = [line.strip() for line in paragraph.splitlines() if line.strip()]
    sentences = []
    lead = ''
    for index, line in enumerate(lines):
        marker = _LIST_MARKER.match(line)
        if marker:
            line = line[marker.end():].rstrip(';').strip()
        else:
            lead = ''
        parts = _english_tokenizer().tokenize(line)
        if marker and parts and lead:
            parts[0] = f'{lead} {parts[0]}'
        if (not marker and parts and parts[-1].endswith(':')
                and index + 1 < len(lines) and _LIST_MARKER.match(lines[index + 1])):
            lead = parts.pop().removesuffix(':').rstrip()
        sentences.extend(parts)
    return sentences


def verbalize_triples(triples) -> list[str]:
    """Join normalized RDF terms, keeping one phrase per triple, including metadata.

    The notebook supplies human-readable predicates and named nodes. For blank
    nodes, prefer their own label, then their type, then a stable generic phrase.
    """
    triples = list(triples)
    blank_names = {}
    priority = {'preferred label': 0, 'label': 1, 'type': 2}
    for subject, predicate, obj in triples:
        if isinstance(subject, BNode) and predicate in priority and not isinstance(obj, BNode) and obj:
            candidate = (priority[predicate], str(obj))
            if subject not in blank_names or candidate < blank_names[subject]:
                blank_names[subject] = candidate

    def term_text(term):
        if isinstance(term, BNode):
            return blank_names[term][1] if term in blank_names else 'unnamed entity'
        return str(term)

    return sorted(' '.join(term_text(term) for term in triple) for triple in triples)


def bigs_distances(sentence_vectors, triple_vectors) -> BIGSScore:
    """Compute the paper's two exact mean nearest-neighbour cosine distances."""
    if not len(sentence_vectors) or not len(triple_vectors):
        raise ValueError('BIGS requires at least one source sentence and one triple.')
    distances = cdist(sentence_vectors, triple_vectors, metric='cosine')
    if not np.isfinite(distances).all():
        raise ValueError('BIGS requires finite, nonzero embeddings.')
    return BIGSScore(coverage=float(distances.min(axis=1).mean()),
                     fidelity=float(distances.min(axis=0).mean()))


def score_benchmark(paragraphs, graphs_by_model, encoder, *, batch_size=16):
    """Score aligned lists of verbalized graphs. Missing or empty graphs stay unscored.

    Each unique string is encoded once across the benchmark. All occurrences count
    in the score, and each nearest-neighbour search stays within its paragraph.
    """
    sentences = [source_sentences(text) for text in paragraphs]
    if any(not parts for parts in sentences):
        raise ValueError('Each source paragraph must contain at least one sentence.')
    vocabulary = {sentence for parts in sentences for sentence in parts}
    for model, graphs in graphs_by_model.items():
        if len(graphs) != len(sentences):
            raise ValueError(f'{model} has {len(graphs)} graphs for {len(sentences)} paragraphs.')
        for graph in graphs:
            if graph:
                vocabulary.update(graph)

    texts = sorted(vocabulary)
    embeddings = encoder.encode(texts, batch_size=batch_size, convert_to_numpy=True,
                                show_progress_bar=False)
    positions = {text: index for index, text in enumerate(texts)}

    def vectors(parts):
        return embeddings[[positions[part] for part in parts]]

    source_vectors = [vectors(parts) for parts in sentences]
    return {
        model: [bigs_distances(source, vectors(graph)) if graph else None
                for source, graph in zip(source_vectors, graphs, strict=True)]
        for model, graphs in graphs_by_model.items()
    }
