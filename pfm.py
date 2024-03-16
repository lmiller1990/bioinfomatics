import pandas as pd
import math
import numpy as np

sequences = [
    "AATGCGGA",
    "AATGTGGC",
    "ACTGTGGC",
    "CGTGTGGC",
    "CGTGTGGC",
    "GGTGTGGC",
    "GGTGTGGC",
    "GGTGTGGC",
    "GGTGTGGG",
    "GGTGTGGG"
]

nt = ["A", "C", "G", "T"]

seqs = pd.DataFrame(list(s) for s in sequences)

pfm = pd.DataFrame(np.zeros((4, len(sequences[0]))), index=nt)
# column_labels =[i for i in range(len(sequences[0]))]
# pfm.columns = column_labels

# or
# for n in nt:
#     pfm.loc[n] = seqs.apply(lambda col: (col == n).sum())

for col in seqs.columns:
  for n in nt:
    # 1 is peusdocount
    c = (seqs[col] == n).sum() + 1
    pfm.loc[n, col] = c
   
ppm = pd.DataFrame(np.zeros(pfm.shape), index=pfm.index, columns=pfm.columns, dtype=float)

for col in seqs.columns:
  total = pfm[col].sum()
  ppm[col] = round(pfm[col] / total, 2)

# Step 4 - adjust PPM by background probability
# Human
bg_prob = {
  "A": 0.233,
  "C": 0.268,
  "G": 0.267,
  "T": 0.231
}

for col in ppm.columns:
  for n in nt:
    val = ppm.loc[n, col]
    ppm.loc[n,col]= round(val / bg_prob[n], 2)


#  Step 5: Position Weight Matrix (PWM)
pwm = pd.DataFrame(np.zeros(pfm.shape), index=pfm.index, columns=pfm.columns)

for col in pwm.columns:
  for n in nt:
    val = ppm.loc[n, col]
    pwm.loc[n,col]= round(math.log2(val), 2)

s1 = "ATGCGATGACCTGCGGC"

def search(s1: str, pwm: pd.DataFrame) -> tuple[int, str]:
  n = pwm.shape[1]
  bestidx = -1
  best_score = 0
  for i in range(len(s1) - n+1):
    window = s1[i:i+n]
    score = 0

    for j, nt in enumerate(window):
      score = score + pwm.loc[nt,j]

    if score > best_score:
      bestidx = i
      best_score = score

  return bestidx, s1[bestidx:bestidx+n]
    

best_idx, best_seq = search(s1, pwm)

print(s1)
print(" " * (best_idx - 1), "^" * len(best_seq), "<- most likely to be motif")