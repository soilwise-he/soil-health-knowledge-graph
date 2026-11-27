# refer to https://github.com/ChristopheCruz/LLM4KGC/blob/main/Evaluate_graphs/graph_matching.py

from collections import Counter, defaultdict
from typing import NamedTuple

import numpy as np
from rdflib import BNode
import torch
from torch.nn.utils.rnn import pad_sequence
import time
import threading
from rouge_score import rouge_scorer
from bert_score.utils import get_model, get_tokenizer, lang2model, model2layers, sent_encode
from transformers import RobertaTokenizer
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction
from scipy.optimize import Bounds, LinearConstraint, linear_sum_assignment, milp
from scipy.sparse import lil_matrix
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
import re
import networkx as nx
from sklearn import preprocessing
from sklearn.metrics import precision_score, recall_score, f1_score

def modify_graph(original_graph):
    """
    Convert the original graph to lowercase and strip spaces.
    
    Parameters:
    - original_graph: List of lists representing a graph
    
    Returns:
    - modified_graph: Modified graph with lowercase and stripped strings
    """
    modified_graph = []
    for x in original_graph:
        modified_graph.append([str(t).lower().strip() for t in x])
    return modified_graph


class TripleMatchCounts(NamedTuple):
    """Distinct triple counts for P/R/F1 and predicted occurrence counts for accuracy."""
    matched: int
    predicted: int
    gold: int
    matched_occurrences: int
    predicted_occurrences: int


def _match_triple(triple):
    # Keep graph-local blank identity separate from ordinary text, even a literal like "<blank1>".
    return tuple(term if isinstance(term, BNode) else str(term).strip().lower() for term in triple)


def _blank_pattern(triple):
    """Give each blank endpoint a slot within the triple. A self-loop repeats its slot."""
    subject, predicate, obj = triple
    slots = {}

    def endpoint(term):
        if isinstance(term, BNode):
            return slots.setdefault(term, len(slots))
        return term

    pattern = (endpoint(subject), predicate, endpoint(obj))
    return pattern, tuple(slots)


def _solve_blank_assignment(single, linked):
    """Choose an injective prediction-to-gold mapping maximizing the supplied rewards."""
    candidates = set(single)
    for first, second in linked:
        candidates.update((first, second))
    if not candidates:
        return {}

    pairs = sorted(candidates)
    pred_nodes = sorted({p for p, _ in pairs})
    gold_nodes = sorted({g for _, g in pairs})
    pred_index = {node: i for i, node in enumerate(pred_nodes)}
    gold_index = {node: i for i, node in enumerate(gold_nodes)}

    if not linked:
        weights = np.zeros((len(pred_nodes), len(gold_nodes)), dtype=np.int64)
        for (p, g), weight in single.items():
            weights[pred_index[p], gold_index[g]] = weight
        rows, cols = linear_sum_assignment(weights, maximize=True)
        return {pred_nodes[i]: gold_nodes[j] for i, j in zip(rows, cols) if weights[i, j]}

    # A blank-to-blank triple earns its reward only when both endpoint pairs are chosen.
    # Constrain its reward variable y by each binary assignment variable (y <= x1 and y <= x2).
    pair_index = {pair: i for i, pair in enumerate(pairs)}
    node_rows = len(pred_nodes) + len(gold_nodes)
    constraints = lil_matrix((node_rows + 2 * len(linked), len(pairs) + len(linked)))
    upper = np.ones(constraints.shape[0])
    upper[node_rows:] = 0
    rewards = np.zeros(constraints.shape[1])
    for (p, g), col in pair_index.items():
        constraints[pred_index[p], col] = 1
        constraints[len(pred_nodes) + gold_index[g], col] = 1
        rewards[col] = single.get((p, g), 0)
    for i, (endpoints, weight) in enumerate(linked.items()):
        bonus_col = len(pairs) + i
        rewards[bonus_col] = weight
        for offset, pair in enumerate(endpoints):
            row = node_rows + 2 * i + offset
            constraints[row, bonus_col] = 1
            constraints[row, pair_index[pair]] = -1

    result = milp(
        c=-rewards, integrality=np.ones(len(rewards)), bounds=Bounds(0, 1),
        constraints=LinearConstraint(constraints.tocsc(), -np.inf, upper),
        options={'mip_rel_gap': 0.0},
    )
    if not result.success:
        raise RuntimeError(f'Blank-node alignment did not reach an optimum: {result.message}')
    return {p: g for (p, g), col in pair_index.items() if result.x[col] > 0.5}


def _blank_mapping(gold, predicted):
    gold_by_pattern = defaultdict(list)
    for triple in gold:
        pattern, blanks = _blank_pattern(triple)
        if blanks:
            gold_by_pattern[pattern].append(blanks)
    if not gold_by_pattern:
        return {}

    single, linked = Counter(), Counter()
    # One extra distinct match outweighs every possible gain in predicted occurrences.
    distinct_weight = sum(predicted.values()) + 1
    for triple, occurrences in predicted.items():
        pattern, pred_blanks = _blank_pattern(triple)
        for gold_blanks in gold_by_pattern.get(pattern, ()):
            pairs = tuple(zip(pred_blanks, gold_blanks))
            weight = distinct_weight + occurrences
            if len(pairs) == 1:
                single[pairs[0]] += weight
            else:
                linked[pairs] += weight
    return _solve_blank_assignment(single, linked)


def get_triple_match_counts(gold_graph, pred_graph):
    """Match one normalized paragraph pair, preserving RDFLib BNodes for structural alignment."""
    gold = {_match_triple(triple) for triple in gold_graph}
    predicted = Counter(_match_triple(triple) for triple in pred_graph)
    mapping = _blank_mapping(gold, predicted)
    matched = matched_occurrences = 0
    for (subject, predicate, obj), count in predicted.items():
        if isinstance(subject, BNode) and subject not in mapping:
            continue
        if isinstance(obj, BNode) and obj not in mapping:
            continue
        aligned = (mapping.get(subject, subject), predicate, mapping.get(obj, obj))
        if aligned in gold:
            matched += 1
            matched_occurrences += count
    return TripleMatchCounts(
        matched, len(predicted), len(gold), matched_occurrences, sum(predicted.values())
    )


def get_triple_match_prf(gold_graphs, pred_graphs):
    """Micro-average exact triple matches, aligning blank nodes independently in each graph pair."""
    counts = [get_triple_match_counts(g, p) for g, p in zip(gold_graphs, pred_graphs)]
    matched = sum(c.matched for c in counts)
    if not matched:
        return 0.0, 0.0, 0.0
    predicted = sum(c.predicted for c in counts)
    gold = sum(c.gold for c in counts)
    return matched / predicted, matched / gold, 2 * matched / (predicted + gold)


def get_triple_match_accuracy(pred_graph, gold_graph):
    """Fraction of predicted triple occurrences matched under the same blank-node alignment."""
    counts = get_triple_match_counts(gold_graph, pred_graph)
    return counts.matched_occurrences / counts.predicted_occurrences if counts.predicted_occurrences else 0.0


def get_graph_match_accuracy(pred_graphs, gold_graphs):
    """
    Compute accuracy for entire graph matches between gold and predicted graphs.
    
    Parameters:
    - pred_graphs: List of predicted graphs
    - gold_graphs: List of gold graphs
    
    Returns:
    - acc: Accuracy for entire graph matches
    """
    matchs = 0
    i = 1
    for pred, gold in zip(pred_graphs, gold_graphs):
        g1 = nx.MultiDiGraph()
        g2 = nx.MultiDiGraph()
        print(i)
        for edge in gold:
            g1.add_node(str(edge[0]).lower().strip(), label=str(edge[0]).lower().strip())
            g1.add_node(str(edge[2]).lower().strip(), label=str(edge[2]).lower().strip())
            g1.add_edge(str(edge[0]).lower().strip(), str(edge[2]).lower().strip(), label=str(edge[1]).lower().strip())
#        print(pred)
        i+=1
        for edge in pred:
          #  print(edge)
         #   print(i)
        #    i+=1
            if len(edge) == 2:
                edge.append('NULL')
            elif len(edge) == 1:
                edge.append('NULL')
                edge.append('NULL')
            g2.add_node(str(edge[0]).lower().strip(), label=str(edge[0]).lower().strip())
            g2.add_node(str(edge[2]).lower().strip(), label=str(edge[2]).lower().strip())
            g2.add_edge(str(edge[0]).lower().strip(), str(edge[2]).lower().strip(), label=str(edge[1]).lower().strip())

        if nx.is_isomorphic(g1, g2, edge_match=lambda x, y: x == y):
            matchs += 1
    acc = matchs/len(pred_graphs)
    return acc

def get_tokens(gold_edges, pred_edges):
    """
    Tokenize edge text for G-BLEU. Spaces separate words, and any semicolons
    already present in the input are treated as punctuation.
    
    Parameters:
    - gold_edges: List of gold edges
    - pred_edges: List of predicted edges
    
    Returns:
    - gold_tokens: Tokenized gold edges
    - pred_tokens: Tokenized predicted edges
    """
    nlp = English()
    tokenizer = Tokenizer(nlp.vocab, infix_finditer=re.compile(r'''[;]''').finditer)

    gold_tokens = []
    pred_tokens = []

    for i in range(len(gold_edges)):
        gold_tokens_edges = []
        pred_tokens_edges = []

        for sample in tokenizer.pipe(gold_edges[i]):
            gold_tokens_edges.append([j.text for j in sample])
        for sample in tokenizer.pipe(pred_edges[i]):
            pred_tokens_edges.append([j.text for j in sample])
        gold_tokens.append(gold_tokens_edges)
        pred_tokens.append(pred_tokens_edges)

    return gold_tokens, pred_tokens


def split_to_edges(graphs):
    """Return one subject predicate object string per triple for G-BLEU and G-ROUGE."""
    return [[" ".join(terms) for terms in modify_graph(graph)] for graph in graphs]


def legacy_character_edges(graphs):
    """Reproduce the character-separated input used by the existing BERTScore baseline."""
    return [[";".join(str(triple)).lower().strip() for triple in graph] for graph in graphs]


def _token_batches(edges, length, max_edges, max_tokens):
    """Group similar lengths and bound the number of padded tokens per batch."""
    ordered = sorted(edges, key=length, reverse=True)
    start = 0
    while start < len(ordered):
        count = min(max_edges, max(1, max_tokens // length(ordered[start])))
        yield ordered[start:start + count]
        start += count


class GraphBERTScorer:
    """Reuse a BERTScore model and its CPU cache of edge embeddings across graph sets.

    'auto' selects FP16 on CUDA compute capability 7.0+ and FP32 elsewhere.
    'mixed' uses CUDA autocast for the encoder and FP32 for token similarities.
    'fp32' uses reference precision throughout. The cache belongs to this instance.
    """

    def __init__(self, model_type=None, *, batch_size=None, precision='auto', device=None):
        self.device = torch.device(device or ('cuda' if torch.cuda.is_available() else 'cpu'))
        if precision == 'auto':
            use_half = self.device.type == 'cuda' and torch.cuda.get_device_capability(self.device)[0] >= 7
            precision = 'fp16' if use_half else 'fp32'
        if precision not in ('fp16', 'mixed', 'fp32') or (self.device.type != 'cuda' and precision != 'fp32'):
            raise ValueError("Use 'auto' or 'fp32' on any device, or 'fp16' or 'mixed' on CUDA.")
        self.mixed_precision = precision == 'mixed'
        self.dtype = torch.float16 if precision == 'fp16' else torch.float32
        self.batch_size = batch_size if batch_size is not None else (512 if self.device.type == 'cuda' else 64)
        if self.batch_size < 1:
            raise ValueError('batch_size must be positive')
        model_type = model_type or lang2model['en']
        layers = model2layers[model_type]
        print(f'G-BERTScore uses {model_type} layer {layers} on {self.device} ({precision}).')
        self.tokenizer = get_tokenizer(model_type, use_fast=False)
        self.model = get_model(model_type, layers).to(self.device, dtype=self.dtype)
        self.embeddings = {}

    def _tokenize(self, batch):
        if isinstance(self.tokenizer, RobertaTokenizer) and self.tokenizer.is_fast:
            # Match BERTScore's RoBERTa prefix-space and truncation rules with the same tokenizer.
            return self.tokenizer(
                [edge.strip() for edge in batch], add_special_tokens=True, add_prefix_space=True,
                max_length=self.tokenizer.model_max_length, truncation=True, return_attention_mask=False,
            ).input_ids
        # Transformers 5 removed the special-token builder used by BERTScore for empty text.
        return [sent_encode(self.tokenizer, e) if e.strip() else self.tokenizer.encode('') for e in batch]

    def _encode_missing(self, edges):
        tokens = {}
        missing = list(edges.difference(self.embeddings))
        for start in range(0, len(missing), 2048):
            batch = missing[start:start + 2048]
            for edge, ids in zip(batch, self._tokenize(batch)):
                tokens[edge] = torch.tensor(ids, dtype=torch.long)
        pad = self.tokenizer.pad_token_id
        for batch in _token_batches(tokens, lambda edge: len(tokens[edge]), self.batch_size, 4096):
            ids = pad_sequence([tokens[e] for e in batch], batch_first=True, padding_value=pad)
            lengths = [len(tokens[e]) for e in batch]
            mask = torch.arange(ids.shape[1]) < torch.tensor(lengths)[:, None]
            hidden = self.model(ids.to(self.device), attention_mask=mask.to(self.device))[0]
            vectors = torch.nn.functional.normalize(hidden.float(), dim=-1).to(self.dtype).cpu()

            # CLS and SEP can be the best matching token, but have zero averaging weight.
            weights = mask.clone()
            for special in (self.tokenizer.cls_token_id, self.tokenizer.sep_token_id):
                if special is not None:
                    weights &= ids != special
            weights = weights.float()
            weights /= weights.sum(dim=1, keepdim=True).clamp_min(1)
            for i, (edge, length) in enumerate(zip(batch, lengths)):
                self.embeddings[edge] = vectors[i, :length], weights[i, :length]

    def _blocks(self, edges):
        # Tile the token similarity matrix independently of the number of edge pairs.
        batches = _token_batches(edges, lambda e: len(self.embeddings[e][0]), len(edges), 4096)
        blocks = []
        start = 0
        for batch in batches:
            vectors, weights = zip(*(self.embeddings[e] for e in batch))
            vectors = pad_sequence(vectors, batch_first=True).to(self.device)
            weights = pad_sequence(weights, batch_first=True).to(self.device)
            blocks.append((slice(start, start + len(batch)), vectors, weights))
            start += len(batch)
        return blocks

    def _matched_total(self, gold, pred):
        gold_blocks, pred_blocks = self._blocks(gold), self._blocks(pred)
        scores = torch.empty((len(gold), len(pred)), device=self.device, dtype=torch.float32)
        for rows, g, gw in gold_blocks:
            for cols, p, pw in pred_blocks:
                cosines = (g.flatten(0, 1) @ p.flatten(0, 1).T).view(*g.shape[:2], *p.shape[:2])
                recall = (cosines.amax(dim=3).float() * gw[:, :, None]).sum(dim=1)
                precision = (cosines.amax(dim=1).float() * pw[None, :, :]).sum(dim=2)
                f1 = 2 * precision * recall / (precision + recall)
                scores[rows, cols] = f1.nan_to_num(nan=0.0)
        scores = scores.cpu().numpy()
        rows, cols = linear_sum_assignment(scores, maximize=True)
        return scores[rows, cols].sum(dtype=np.float64)

    @torch.inference_mode()
    def __call__(self, all_gold_edges, all_pred_edges):
        graphs = list(zip(all_gold_edges, all_pred_edges))
        edges = {edge for gold, pred in graphs for side in (gold, pred) for edge in side}
        with torch.autocast(self.device.type, dtype=torch.float16, enabled=self.mixed_precision):
            self._encode_missing(edges)
        values = np.zeros((3, len(graphs)), dtype=np.float64)
        with torch.autocast(self.device.type, enabled=False):
            for i, (gold, pred) in enumerate(graphs):
                if len(gold) and len(pred):
                    total = self._matched_total(gold, pred)
                    values[:, i] = total / len(pred), total / len(gold), 2 * total / (len(pred) + len(gold))
        return tuple(values)


def get_bert_score(all_gold_edges, all_pred_edges, model_type=None, *, batch_size=None, precision='fp32'):
    """Return per-graph precision, recall and F1 using BERTScore and optimal edge matching.

    For multiple prediction sets, pass a single GraphBERTScorer to show_edge_metric.
    batch_size caps the number of unique edge texts per encoder batch.
    """
    scorer = GraphBERTScorer(model_type, batch_size=batch_size, precision=precision)
    return scorer(all_gold_edges, all_pred_edges)


def _edge_match_prf(gold_graphs, pred_graphs, score_pair):
    """Match edges by maximum total score and return per-graph precision, recall and F1."""
    precisions, recalls, f1s = [], [], []
    for gold_edges, pred_edges in zip(gold_graphs, pred_graphs):
        scores = np.zeros((len(pred_edges), len(gold_edges)))
        for pred_idx, pred_edge in enumerate(pred_edges):
            for gold_idx, gold_edge in enumerate(gold_edges):
                scores[pred_idx, gold_idx] = score_pair(gold_edge, pred_edge)

        rows, cols = linear_sum_assignment(scores, maximize=True)
        matched = scores[rows, cols].sum()
        precision = matched / len(pred_edges)
        recall = matched / len(gold_edges)
        f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
        precisions.append(precision)
        recalls.append(recall)
        f1s.append(f1)
    return np.array(precisions), np.array(recalls), np.array(f1s)


def get_graph_bleu(gold_tokens, pred_tokens):
    """Score graphs by sentence BLEU between tokenized edges."""
    def score_pair(gold, pred):
        return sentence_bleu([gold], pred, smoothing_function=SmoothingFunction().method1)

    return _edge_match_prf(gold_tokens, pred_tokens, score_pair)


def get_graph_rouge(gold_sent, pred_sent):
    """Score graphs by ROUGE-2 precision between edge strings."""
    scorer_rouge = rouge_scorer.RougeScorer(['rouge2'], use_stemmer=True)

    def score_pair(gold, pred):
        return scorer_rouge.score(gold, pred)['rouge2'].precision

    return _edge_match_prf(gold_sent, pred_sent, score_pair)


def get_bleu_rouge(gold_tokens, pred_tokens, gold_sent, pred_sent):
    """Return ROUGE precision, recall and F1 followed by the same three BLEU arrays."""
    rouge = get_graph_rouge(gold_sent, pred_sent)
    bleu = get_graph_bleu(gold_tokens, pred_tokens)
    return rouge + bleu


def return_eq_node(node1, node2):
    """
    Equality function for nodes.
    
    Parameters:
    - node1: First node
    - node2: Second node
    
    Returns:
    - Equality of nodes based on label
    """
    return node1['label'] == node2['label']


def return_eq_edge(edge1, edge2):
    """
    Equality function for edges.
    
    Parameters:
    - edge1: First edge
    - edge2: Second edge
    
    Returns:
    - Equality of edges based on label
    """
    return edge1['label'] == edge2['label']

def get_ged(gold_graph, pred_graph=None, check_interval=10.0, stable_threshold=5, max_time=300.0, verbose=False):
    """
    Compute approximate graph edit distance (GED) between gold and predicted graphs
    using iterative optimization with early stopping when the value stabilizes.
    
    Uses a background thread for the optimizer so that time monitoring works reliably
    even when the optimizer takes a long time between yielding values.
    
    Parameters:
    - gold_graph: Gold graph (list of triples)
    - pred_graph: Predicted graph (default is None)
    - check_interval: Time interval (seconds) between stability checks (default: 10.0)
    - stable_threshold: Number of consecutive unchanged checks before stopping (default: 5)
    - max_time: Maximum total computation time in seconds as safety net (default: 300.0)
    - verbose: If True, print progress information (default: False)
    
    Returns:
    - ged: Graph edit distance normalized by a constant
    """
    g1 = nx.MultiDiGraph()
    g2 = nx.MultiDiGraph()

    for edge in gold_graph:
        g1.add_node(str(edge[0]).lower().strip(), label=str(edge[0]).lower().strip())
        g1.add_node(str(edge[2]).lower().strip(), label=str(edge[2]).lower().strip())
        g1.add_edge(str(edge[0]).lower().strip(), str(edge[2]).lower().strip(), label=str(edge[1]).lower().strip())
    

    if pred_graph is None:
        return 1

    for edge in pred_graph:
        if len(edge) == 2:
            edge.append('NULL')
        elif len(edge) == 1:
            edge.append('NULL')
            edge.append('NULL')
        g2.add_node(str(edge[0]).lower().strip(), label=str(edge[0]).lower().strip())
        g2.add_node(str(edge[2]).lower().strip(), label=str(edge[2]).lower().strip())
        g2.add_edge(str(edge[0]).lower().strip(), str(edge[2]).lower().strip(), label=str(edge[1]).lower().strip())

    normalizing_constant = g1.number_of_nodes() + g1.number_of_edges() + g2.number_of_nodes() + g2.number_of_edges()

    if verbose:
        print(f"[GED] Graph sizes: g1({g1.number_of_nodes()} nodes, {g1.number_of_edges()} edges), "
              f"g2({g2.number_of_nodes()} nodes, {g2.number_of_edges()} edges)")
        print(f"[GED] Starting iterative optimization (check every {check_interval}s, "
              f"stable threshold={stable_threshold}, max time={max_time}s)")

    # Shared state between main thread and optimizer thread
    state = {
        'best_ged': None,
        'finished': False,
        'lock': threading.Lock()
    }
    stop_event = threading.Event()
    
    def optimizer_worker():
        """Run optimizer in background, updating best_ged as improvements are found."""
        try:
            optimizer = nx.optimize_graph_edit_distance(
                g1, g2, node_match=return_eq_node, edge_match=return_eq_edge
            )
            for ged in optimizer:
                if stop_event.is_set():
                    break
                with state['lock']:
                    state['best_ged'] = ged
        except Exception as e:
            if verbose:
                print(f"[GED] Optimizer error: {e}")
        finally:
            with state['lock']:
                state['finished'] = True
    
    # Start optimizer in background thread
    worker_thread = threading.Thread(target=optimizer_worker, daemon=True)
    worker_thread.start()
    
    # Main thread: monitor progress with time-based checks
    start_time = time.time()
    last_checked_ged = None
    stable_count = 0
    check_count = 0
    
    while True:
        time.sleep(check_interval)
        elapsed = time.time() - start_time
        check_count += 1
        
        with state['lock']:
            current_ged = state['best_ged']
            is_finished = state['finished']
        
        # Check if optimizer finished naturally
        if is_finished:
            if verbose:
                print(f"[GED] Optimizer finished after {elapsed:.1f}s with GED={current_ged}")
            break
        
        # Print progress
        if verbose:
            print(f"[GED] Check #{check_count} at {elapsed:.1f}s: GED={current_ged}, "
                  f"Stable count={stable_count}/{stable_threshold}")
        
        # Check stability
        if current_ged is not None:
            if last_checked_ged is not None and current_ged == last_checked_ged:
                stable_count += 1
                if stable_count >= stable_threshold:
                    if verbose:
                        print(f"[GED] Converged (stable for {stable_count} checks) with GED={current_ged}")
                    stop_event.set()
                    break
            else:
                stable_count = 0
            last_checked_ged = current_ged
        
        # Check timeout
        if elapsed >= max_time:
            if verbose:
                print(f"[GED] Max time ({max_time}s) reached, returning best GED={current_ged}")
            stop_event.set()
            break
    
    # Wait briefly for thread to acknowledge stop (don't block forever)
    worker_thread.join(timeout=2.0)
    
    with state['lock']:
        best_ged = state['best_ged']
    
    # Fallback if no result was obtained
    if best_ged is None:
        if verbose:
            print("[GED] No result obtained, using simple upper bound")
        # Simple upper bound: delete all from g1, insert all to g2
        best_ged = g1.number_of_nodes() + g1.number_of_edges() + g2.number_of_nodes() + g2.number_of_edges()

    normalized_ged = best_ged / normalizing_constant
    
    if verbose:
        print(f"[GED] Final: raw GED={best_ged}, normalized={normalized_ged:.4f}")
    
    return normalized_ged


def get_oep(gold_graph, pred_graph=None):
    """
    Compute optimal edit paths (OEP) between gold and predicted graphs.
    
    Parameters:
    - gold_graph: Gold graph
    - pred_graph: Predicted graph (default is None)
    
    Returns:
    - x: Optimal edit paths
    """
    g1 = nx.MultiDiGraph()
    g2 = nx.MultiDiGraph()

    for edge in gold_graph:
        g1.add_node(str(edge[0]).lower().strip(), label=str(edge[0]).lower().strip())
        g1.add_node(str(edge[2]).lower().strip(), label=str(edge[2]).lower().strip())
        g1.add_edge(str(edge[0]).lower().strip(), str(edge[2]).lower().strip(), label=str(edge[1]).lower().strip())


    normalizing_constant = g1.number_of_nodes() + g1.number_of_edges() + 30

    if pred_graph is None:
        return 1

    for edge in pred_graph:
        if len(edge) == 2:
            edge.append('NULL')
        elif len(edge) == 1:
            edge.append('NULL')
            edge.append('NULL')
        g2.add_node(str(edge[0]).lower().strip(), label=str(edge[0]).lower().strip())
        g2.add_node(str(edge[2]).lower().strip(), label=str(edge[2]).lower().strip())
        g2.add_edge(str(edge[0]).lower().strip(), str(edge[2]).lower().strip(), label=str(edge[1]).lower().strip())

    x, ged = nx.optimal_edit_paths(g1, g2, node_match=return_eq_node, edge_match=return_eq_edge)

    #assert ged #<= normalizing_constant

    return x #/ normalizing_constant



def calculate_hallucination(lst):
    """
    Calculate hallucination in a list.
    
    Parameters:
    - lst: List of elements
    
    Returns:
    - True if there is hallucination, otherwise False
    """
    hall = 0
    for el in lst:
        if el[0] == None:
            hall+=1
    if hall>0:
        return True
    #return hall # We can do this if we want to return the number exact of hallucinations in each graph
    
 
def calculate_omission(lst):
    """
    Calculate omission in a list.
    
    Parameters:
    - lst: List of elements
    
    Returns:
    - True if there is omission, otherwise False
    """
    omiss = 0
    for el in lst:
        if el[1] == None:
            omiss+=1
    if omiss>0:
        return True
    #return omiss  # We can do this if we want to return the number exact of omissions in each graph
