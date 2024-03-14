import pandas as pd
import numpy as np
from typing import List, Dict, TypeAlias
import argparse

TracebackMap: TypeAlias = Dict[str, List[int]]
Traceback: TypeAlias = List[List[int]]

parser = argparse.ArgumentParser(description='Run Needleman Wunsch')

parser.add_argument('s1', type=str, help='First sequence')
parser.add_argument('s2', type=str, help='Second sequence')

parser.add_argument('--gap', type=int, default=-2, help='Gap penalty (default: -2)')
parser.add_argument('--mismatch', type=int, default=-1, help='Mismatch penalty (default: -1)')
parser.add_argument('--match', type=int, default=1, help='Match score (default: 1)')

# Parse the arguments
args = parser.parse_args()

gap = args.gap
mismatch = args.mismatch
match = args.match

def align(df: pd.DataFrame, trace: Traceback) -> tuple[str, str]:
    a1 = ""
    a2 = ""
    previ = 0
    prevj = 0

    for [i, j] in trace:
        if i != previ:
            a1 = a1 + df.index[i]
        else:
            # horizontal
            a1 = a1 + "-"
        if j != prevj:
            a2 = a2 + df.columns[j]
        else:
            # vertical
            a2 = a2 + "-"
        previ = i
        prevj = j
    return a1, a2


def make_traceback(df: pd.DataFrame, traceback_map: TracebackMap) -> Traceback:
    [i, j] = df.shape
    i = i - 1
    j = j - 1
    path: List[List[int]] = [[i, j]]
    nxt = traceback_map[f"{i},{j}"]

    while nxt != [0, 0]:
        path.append(nxt)
        i = nxt[0]
        j = nxt[1]
        nxt = traceback_map[f"{i},{j}"]

    path.reverse()
    return path


def main(s1, s2) -> tuple[str, str]:
    # Define your sequences
    s1 = "GTCGACGCA"
    s2 = "GATTACA"

    # Initialize the extended matrix with zeros, accounting for the extra row and column
    m = np.zeros((len(s1) + 1, len(s2) + 1), dtype=int)

    # Convert the NumPy array to a Pandas DataFrame with placeholders for the extra row and column
    df = pd.DataFrame(m, index=[""] + list(s1), columns=[""] + list(s2))

    t = np.empty((len(s1) + 1, len(s2) + 1), dtype=object)

    # Update the first row and first column with the decrementing values
    df.iloc[0, :] = np.arange(0, -2 * (len(s2) + 1), -2)  # First row
    df.iloc[:, 0] = np.arange(0, -2 * (len(s1) + 1), -2)  # First column

    traceback_map: TracebackMap = {}

    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            # Do not mutate gap values (first row/col)
            if i == 0 or j == 0:
                continue
            # Otherwise, do the calc
            up = df.iat[i - 1, j] + gap
            left = df.iat[i, j - 1] + gap
            ismatch = match if df.index[i] == df.columns[j] else mismatch
            diag = ismatch + df.iat[i - 1, j - 1]
            best = max(diag, up, left)
            df.iat[i, j] = best

            if best == up:
                traceback_map[f"{i},{j}"] = [i - 1, j]
            elif best == left:
                traceback_map[f"{i},{j}"] = [i, j - 1]
            elif best == diag:
                traceback_map[f"{i},{j}"] = [i - 1, j - 1]

    trace = make_traceback(df, traceback_map)
    a1, a2 = align(df, trace)

    return a1, a2

if __name__ == '__main__':
  s1, s2 = main(args.s1, args.s2)
  print(s1)
  print(s2)