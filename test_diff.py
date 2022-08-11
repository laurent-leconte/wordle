import pytest

from diff_performance import diff_functions, diff2_functions, diff_n


def compare(diff_result, str1, str2):
    print(diff_result, str1, str2)
    wp, np = diff_result
    wp2 = [None if c == '*' else c for c in str1]
    np2 = list(str2)
    assert wp == wp2
    assert(sorted(np) == sorted(np2))

diff_test_data = [
    (("aaaaa", "bbbbb"), ("*****", "")),
    (("abcde", "axxxx"), ("a****", "")),
    (("abcde", "abcde"), ("abcde", "")),
    (("aabcd", "aabcd"), ("aabcd", "")),
    (("abcde", "bcdea"), ("*****", "abcde")),
    (("aayyy", "axxxa"), ("a****", "a")),
    (("axaxc", "xxaab"), ("*xa**", "ax")),
]

@pytest.mark.parametrize("input,expected", diff_test_data)
def test_diff(input, expected):
    for diff_func in diff_functions:
        compare(diff_func(*input), *expected)

diff2_test_data = [
    (("aaaaa", "bbbbb", "ccccc"), ('*****', '')),
    (("aaaaa", "abbbb", "aaccc"), ('aa***', '')),
    (("aaxxx", "abbbb", "acxca"), ('a*x**', 'a')),
    (("aaxxx", "bbbaa", "cxxca"), ('**x**', 'aax')),
    (("toxic", "train", "taper"), ('t**i*', '')),
    (("rapid", "train", "taper"), ('*api*','r')),
    (("affix", "taper", "bring"), ('*****','ai')),
    (("tapir", "train", "taper"), ('tapir', '')),
    (("tapir", "train", "paste"), ('ta*i*', 'rp')),
]


@pytest.mark.parametrize("input,expected", diff2_test_data)
def test_diff2(input, expected):
    for diff_func in diff2_functions:
        compare(diff_func(*input), *expected)


@pytest.mark.parametrize("input,expected", diff2_test_data)
def test_diff_n(input, expected):
    base, *words = input
    compare(diff_n(base, words), *expected)

idempotency_test_data = [
    (("aaaaa", "bbbbb"), ("aaaaa", "bbbbb", "bbbbb")),
    (("abcde", "axxxx"), ("abcde", "axxxx", "axxxx")),
    (("abcde", "abcde"), ("abcde", "abcde", "abcde")),
    (("aabcd", "aabcd"), ("aabcd", "aabcd", "aabcd")),
    (("abcde", "bcdea"), ("abcde", "bcdea", "bcdea")),
    (("aayyy", "axxxa"), ("aayyy", "axxxa", "axxxa")),
    (("axaxc", "xxaab"), ("axaxc", "xxaab", "xxaab")),
]


@pytest.mark.parametrize("diff_input,diff2_input", idempotency_test_data)
def test_idempotency_diff2(diff_input, diff2_input):
    for diff, diff2 in zip(diff_functions, diff2_functions):
        assert diff(*diff_input) == diff2(*diff2_input)


@pytest.mark.parametrize("diff_input,diff2_input", idempotency_test_data)
def test_idempotency_diff_n(diff_input, diff2_input):
    base1, *words1 = diff_input
    base2, *words2 = diff2_input
    words3 = words2 + [words2[-1]]
    assert diff_n(base1, words1) == diff_n(base2, words2)
    assert diff_n(base1, words1) == diff_n(base2, words3)