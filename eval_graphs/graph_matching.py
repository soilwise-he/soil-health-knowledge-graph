# refer to https://github.com/ChristopheCruz/LLM4KGC/blob/main/Evaluate_graphs/graph_matching.py

import numpy as np
import time
import threading
from rouge_score import rouge_scorer
from bert_score import score as score_bert
from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.bleu_score import SmoothingFunction
from scipy.optimize import linear_sum_assignment
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


def get_triple_match_prf(gold_graphs, pred_graphs):
    """
    Compute micro-averaged Precision, Recall, and F1 over exact triple matches (case-insensitive).
    
    Parameters:
    - gold_graphs: List of gold graphs (each graph is a list of triples)
    - pred_graphs: List of predicted graphs (each graph is a list of triples)
    
    Returns:
    - precision: Micro-averaged precision
    - recall: Micro-averaged recall
    - f1: Micro-averaged F1 score
    """

    def _norm_triple(triple):
        return tuple(str(t).lower().strip() for t in triple)

    gold_sets = [set(_norm_triple(t) for t in graph) for graph in gold_graphs]
    pred_sets = [set(_norm_triple(t) for t in graph) for graph in pred_graphs]

    tp = sum(len(g & p) for g, p in zip(gold_sets, pred_sets))
    fp = sum(len(p - g) for g, p in zip(gold_sets, pred_sets))
    fn = sum(len(g - p) for g, p in zip(gold_sets, pred_sets))

    if tp == 0:
        return 0.0, 0.0, 0.0
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    if precision + recall == 0:
        return precision, recall, 0.0
    f1 = 2 * precision * recall / (precision + recall)
    return precision, recall, f1

def get_triple_match_accuracy(pred_graph, gold_graph):
    """
    Compute accuracy for triple matches between gold and predicted graphs.
    
    Parameters:
    - pred_graph: Predicted graph
    - gold_graph: Gold graph
    
    Returns:
    - acc: Accuracy for triple matches
    """
    pred = modify_graph(pred_graph)
    gold = modify_graph(gold_graph)    
    matchs = 0
    for x in pred:
        if x in gold:
            matchs += 1
    acc = matchs/len(pred)
    return acc

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
    Tokenize gold and predicted edges using SpaCy.
    
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
    """
    Convert graphs into a list of processed edges.
    
    Parameters:
    - graphs: List of graphs
    
    Returns:
    - processed_graphs: List of processed edges
    """
    
    processed_graphs = []
    for graph in graphs:
        #print(graph)
        processed_graphs.append([";".join(str(triple)).lower().strip() for triple in graph])
    return processed_graphs


def get_bert_score(all_gold_edges, all_pred_edges, model_type=None):
    """
    Compute BERT score for gold and predicted edges.
    
    Parameters:
    - all_gold_edges: List of gold edges
    - all_pred_edges: List of predicted edges
    - model_type: BERT model to use (default: roberta-large for English)
    
    Returns:
    - precisions: Precision scores
    - recalls: Recall scores
    - f1s: F1 scores
    """
    references = []
    candidates = []

    ref_cand_index = {}
    for (gold_edges, pred_edges) in zip(all_gold_edges, all_pred_edges):
        for (i, gold_edge) in enumerate(gold_edges):
            for (j, pred_edge) in enumerate(pred_edges):
                references.append(gold_edge)
                candidates.append(pred_edge)
                ref_cand_index[(gold_edge, pred_edge)] = len(references) - 1

    # Pass model_type if specified
    if model_type:
        _, _, bs_F1 = score_bert(cands=candidates, refs=references, model_type=model_type, idf=False, device='cpu')
    else:
        _, _, bs_F1 = score_bert(cands=candidates, refs=references, lang='en', idf=False, device='cpu')

    print("Computed bert scores for all pairs")

    precisions, recalls, f1s = [], [], []
    for (gold_edges, pred_edges) in zip(all_gold_edges, all_pred_edges):
        score_matrix = np.zeros((len(gold_edges), len(pred_edges)))
        for (i, gold_edge) in enumerate(gold_edges):
            for (j, pred_edge) in enumerate(pred_edges):
                score_matrix[i][j] = bs_F1[ref_cand_index[(gold_edge, pred_edge)]]

        row_ind, col_ind = linear_sum_assignment(score_matrix, maximize=True)

        sample_precision = score_matrix[row_ind, col_ind].sum() / len(pred_edges)
        sample_recall = score_matrix[row_ind, col_ind].sum() / len(gold_edges)

        precisions.append(sample_precision)
        recalls.append(sample_recall)
        f1s.append(2 * sample_precision * sample_recall / (sample_precision + sample_recall))

    return np.array(precisions), np.array(recalls), np.array(f1s)


# Note: These graph matching metrics are computed by considering each graph as a set of edges and each edge as a
# sentence
def get_bleu_rouge(gold_tokens, pred_tokens, gold_sent, pred_sent):
    """
    Compute BLEU and ROUGE scores for tokenized sentences.
    
    Parameters:
    - gold_tokens: Tokenized gold sentences
    - pred_tokens: Tokenized predicted sentences
    - gold_sent: Gold sentences
    - pred_sent: Predicted sentences
    
    Returns:
    - precisions_rouge: Precision scores for ROUGE
    - recalls_rouge: Recall scores for ROUGE
    - f1s_rouge: F1 scores for ROUGE
    - precisions_bleu: Precision scores for BLEU
    - recalls_bleu: Recall scores for BLEU
    - f1s_bleu: F1 scores for BLEU
    """
    scorer_rouge = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rouge3', 'rougeL'], use_stemmer=True)

    precisions_bleu = []
    recalls_bleu = []
    f1s_bleu = []

    precisions_rouge = []
    recalls_rouge = []
    f1s_rouge = []

    for graph_idx in range(len(gold_tokens)):
        score_bleu = np.zeros((len(pred_tokens[graph_idx]), len(gold_tokens[graph_idx])))
        score_rouge = np.zeros((len(pred_tokens[graph_idx]), len(gold_tokens[graph_idx])))
        for p_idx in range(len(pred_tokens[graph_idx])):
            for g_idx in range(len(gold_tokens[graph_idx])):
                score_bleu[p_idx, g_idx] = sentence_bleu([gold_tokens[graph_idx][g_idx]], pred_tokens[graph_idx][p_idx], smoothing_function=SmoothingFunction().method1)
                score_rouge[p_idx, g_idx] = \
                    scorer_rouge.score(gold_sent[graph_idx][g_idx], pred_sent[graph_idx][p_idx])['rouge2'].precision

        def _scores(cost_matrix):
            row_ind, col_ind = linear_sum_assignment(cost_matrix, maximize=True)
            precision = cost_matrix[row_ind, col_ind].sum() / cost_matrix.shape[0]
            recall = cost_matrix[row_ind, col_ind].sum() / cost_matrix.shape[1]
            f1 = (2 * precision * recall) / (precision + recall) if precision + recall > 0 else 0
            return precision, recall, f1

        precision_bleu, recall_bleu, f1_bleu = _scores(score_bleu)
        precisions_bleu.append(precision_bleu)
        recalls_bleu.append(recall_bleu)
        f1s_bleu.append(f1_bleu)

        precision_rouge, recall_rouge, f1_rouge = _scores(score_rouge)
        precisions_rouge.append(precision_rouge)
        recalls_rouge.append(recall_rouge)
        f1s_rouge.append(f1_rouge)

    return np.array(precisions_rouge), np.array(recalls_rouge), np.array(f1s_rouge), np.array(
        precisions_bleu), np.array(recalls_bleu), np.array(f1s_bleu)


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
