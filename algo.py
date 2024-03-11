import pandas as pd
import numpy as np

match = 1
miss = -1
gap = -2

def main():
  # Define your sequences
  s1 = "ATTC"
  s2 = "ATC"

  # s1 = "GAA"
  # s2 = "GGAA"

  # Initialize the extended matrix with zeros, accounting for the extra row and column
  m = np.zeros((len(s1) + 1, len(s2) + 1), dtype=int)

  # Convert the NumPy array to a Pandas DataFrame with placeholders for the extra row and column
  df = pd.DataFrame(m, index=[''] + list(s1), columns=[''] + list(s2))

  t = np.empty((len(s1) + 1, len(s2) + 1), dtype=object)
  traceback = pd.DataFrame(t, index=[''] + list(s1), columns=[''] + list(s2))

  # Update the first row and first column with the decrementing values
  df.iloc[0, :] = np.arange(0, -2 * (len(s2) + 1), -2)  # First row
  df.iloc[:, 0] = np.arange(0, -2 * (len(s1) + 1), -2)  # First column

  for i in range(df.shape[0]):  # Iterate over rows
    for j in range(df.shape[1]):  # Iterate over columns
        value = df.iat[i, j]
        if i == 0 and j == 0:
           continue
        elif value == 0:
          up = df.iat[i-1, j] + gap
          left = df.iat[i ,j-1] + gap
          ismatch = match if df.index[i] == df.columns[j] else miss
          diag = ismatch + df.iat[i-1,j-1]
          best = max(diag, up, left)
          df.iat[i, j] = best
          if best == up:
            traceback.iloc[i,j] = [i-1,j]
          elif best == left:
            traceback.iat[i, j] = [i,j-1]
          elif best == diag:
            traceback.iat[i, j] = [i-1,j-1]

  col_len = len(df.columns)
  row_len = len(df.index)

  i = row_len-1
  j = col_len-1
  s1align = []
  s2align = []
  init = True
  prev = None
  next = None

  while True:
    if next is not None and next[0] == 0 and next[1] == 0:
      break
    if init:
      s1align.append(traceback.index[i])
      s2align.append(traceback.columns[j])
      init = False
      next = traceback.iat[i, j]
    else:
      # going up
      if prev is not None and prev[1] == next[1]:
        s1align.append('-')
        s2align.append(traceback.columns[next[1]])
      elif prev is not None and prev[0] == next[0]:
        print("here")
        s2align.append('-')
        s1align.append(traceback.columns[next[0]])
      else:
        s1align.append(traceback.index[next[0]])
        s2align.append(traceback.columns[next[1]])
      prev = next[:]
      next = traceback.iat[next[0], next[1]]

  return df, s1align[::-1], s2align[::-1]

df, s1align, s2align = main()

print(df)
print("Alignment\n")
print("".join(s1align))
print("".join(s2align))