from collections import Counter
from functools import partial, wraps, lru_cache

# Initial version
def diff_v1(word1, word2):
    well_placed = [c1 if c1 == c2 else None for c1, c2 in zip(word1, word2)]
    well_placed_counter = Counter(well_placed)
    letters1 = Counter(word1)
    letters2 = Counter(word2)
    not_placed = []
    for letter, count in letters1.items():
        matches = min(count, letters2.get(letter, 0)) - well_placed_counter.get(letter, 0)
        not_placed.extend([letter]*matches)
    return well_placed, not_placed

def delta(well_placed, not_placed, well_placed2):
    result = not_placed.copy()
    for (a,b) in zip(well_placed, well_placed2):
        #if letter is well placed in first word AND not well placed in second word
        if a and not b and a in result:
            result.remove(a)
    return result

def merge(list1, list2):
    result = []
    for a in list1:
        if a in list2:
            list2.remove(a)
        result.append(a)
    result.extend(list2)
    return result

def diff2_base(diff_func, base, word1, word2):
    well_placed1, not_placed1 = diff_func(base, word1)
    not_placed1 = not_placed1.copy()  # make copies in case diff_func results are cached
    well_placed2, not_placed2 = diff_func(base, word2)
    not_placed2 = not_placed2.copy()
    well_placed = [a or b for (a,b) in zip(well_placed1, well_placed2)]
    not_placed = merge(delta(well_placed1, not_placed2, well_placed2), delta(well_placed2, not_placed1, well_placed1))
    return well_placed, not_placed

diff2_v1 = partial(diff2_base, diff_v1)
diff2_v1.__name__ = "diff2_v1"

# v2
def diff_inline(word1, word2):
    """ diff_v2 inlines the operations from diff_v1 in a single loop """
    well_placed = []
    well_placed_counter = {}
    letters1 = {}
    letters2 = {}
    for c1, c2 in zip(word1, word2):
        if c1 == c2:
            well_placed.append(c1)
            well_placed_counter[c1] = well_placed_counter.get(c1, 0) + 1
        else:
            well_placed.append(None)
        letters1[c1] = letters1.get(c1, 0) + 1
        letters2[c2] = letters2.get(c2, 0) + 1
    not_placed = []
    for letter, count in letters1.items():
        matches = min(count, letters2.get(letter, 0)) - well_placed_counter.get(letter, 0)
        not_placed.extend([letter]*matches)
    return well_placed, not_placed


def simple_cache(fun):
    cache = {}
    @wraps(fun)
    def wrapper(*args, **kwargs):
        if args in cache:
            return cache[args]
        else:
            result = fun(*args, **kwargs)
            cache[args] = result
            return result
    return wrapper


diff2_inline = partial(diff2_base, diff_inline)
diff2_inline.__name__ = "diff2_inline"

diff_inline_cached = lru_cache(maxsize=None)(diff_inline)
diff2_inline_cached = partial(diff2_base, diff_inline_cached)
diff2_inline_cached.__name__ = "diff2_inline_cached"

diff_functions = [diff_v1, diff_inline]
diff2_functions = [diff2_v1, diff2_inline, diff2_inline_cached]

# for triplets
def extended_diff(word1, word2, greens=None, yellows=None):
    # well_placed, not_placed = diff_inline_cached(word1, word2)
    well_placed, not_placed = diff_inline(word1, word2)
    if greens or yellows:
        # merge previous results
        new_greens = [a or b for (a,b) in zip(greens, well_placed)]
        new_yellows = merge(delta(greens, not_placed, well_placed), delta(well_placed, yellows, greens))
        return new_greens, new_yellows
    return well_placed, not_placed


def diff_n(base, words):
    greens = None
    yellows = None
    for word in words:
        greens, yellows = extended_diff(base, word, greens, yellows)
    return greens, yellows


# scoring functions
WELL_PLACED_BONUS = 2

def average(l):
    return sum(l) / len(l)

def score_all(word, corpus):
    def score_one(w1, w2):
        greens, yellows = diff_inline(w1, w2)
        a = sum([1 if a else 0 for a in greens])
        return a*WELL_PLACED_BONUS + len(yellows)
    return average([score_one(w, word) for w in corpus])

def cached_score_all(cached_diffs, word):
    def score_one(word1, g, y, word2):
        greens, yellows = extended_diff(word1, word2, g, y)
        green_count = sum([1 if a else 0 for a in greens])
        return green_count*WELL_PLACED_BONUS + len(yellows)
    return average([score_one(*c, word) for c in cached_diffs])

def score_n_all(words, corpus):
    def score_n_1(base, words):
        greens, yellows = diff_n(base, words)
        green_count = sum([1 if a else 0 for a in greens])
        return green_count*WELL_PLACED_BONUS + len(yellows)
    return average([score_n_1(w, words) for w in corpus])

