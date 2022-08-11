import json
from time import time
from diff_functions import diff_n, score_all, score_n_all, cached_score_all

def load_words(filename):
    with open(filename) as f:
        return f.read().split()
        

def search(pairs, corpus, cached_scores, core, threshold=5):
    best = 0
    results = []
    for i, p in enumerate(pairs):
        print(f"***** {i} {p[1]} {p[2]} *****")
        pair_score = p[0]
        pair_diffs = [(w, *diff_n(w, p[1:])) for w in core]
        for third in corpus:
            third_score = cached_scores[third]
            if pair_score + third_score < threshold:
                break
            score = cached_score_all(pair_diffs, third)
            triplet = (p[1], p[2], third)
            if score > threshold:
                results.append((score, *triplet))
            if score > best:
                print(f'New best: {triplet} {score}')
                best = score
    return sorted(results, reverse=True)

def find_triplets(corpus="extended", num_pairs=100):
    print("Loading words...")
    start = time()
    core = load_words('core.txt')
    extended = load_words('extended.txt')

    extended_pairs = json.load(open('extended_pairs.json'))
    core_pairs = json.load(open('core_pairs.json'))
    print("Done loading words in %.2f seconds." % (time() - start))

    print("Caching word scores...")
    start = time()
    cached_scores = {}
    for w in extended:
        cached_scores[w] = score_all(w, core)
    extended_by_score = [x[0] for x in sorted(cached_scores.items(), key=lambda x: x[1], reverse=True)]
    core_set = set(core)
    core_by_score = [x for x in extended_by_score if x in core_set]
    print("Done caching word scores in %.2f seconds." % (time() - start))

    print("Searching for triplets...")
    start = time()
    pairs = core_pairs[:num_pairs] if corpus == "core" else extended_pairs[:num_pairs]
    corpus_list = core_by_score if corpus == "core" else extended_by_score
    results = search(pairs, corpus_list, cached_scores, core)
    print("Done searching in %.2f seconds." % (time() - start))

    json.dump(results, open(f'{corpus}_triplets.json', 'w'))


if __name__ == "__main__":
    find_triplets(num_pairs=1000)