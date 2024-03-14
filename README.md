I am learning bioinformatics, this is the code I am writing.

# Requirements

- Python 3

# Install

```sh
pip install -r requirements.txt
```

# Lint

```sh
black *.py
```

## Algorithms

- [Needleman Wunsch](./needleman_wunsch.py)

```sh
# Basic
python needleman_wunsch.py "GTCGACGCA" "GGATACA"

# Custom weights
python needleman_wunsch.py "GTCGACGCA" "GGATACA" --gap -1 --mismatch 0 --match 3
```
