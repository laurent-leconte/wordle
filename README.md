# Wordle

A dump of resources to study Wordle word frequencies and best moves, built for [this blog post](https://lau.rent/posts/wordle-opening-moves.html)

## Content

The main file to explore the data is wordle.ipynb. It should be enough to reproduce all the results from the post.

The pure Python files contain variations on the basic scoring algorithm, in an attempt to improve its efficiency.

The other resources are word lists. The initial word lists are `core.txt` and `extended.txt`; the `*_pairs.json` `*_triplets.json` are the (scored and ranked) results for the pair-finding and triplet-finding algorithms respectively.
