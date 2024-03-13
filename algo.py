import pandas as pd
import numpy as np

match = 1
miss = -1
gap = -2

def main():
  # Define your sequences
  s1 = "GAT"
  s2 = "TAGGT"

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
          pass
        elif value == 0:
          up = df.iat[i-1, j] + gap
          left = df.iat[i ,j-1] + gap
          ismatch = match if df.index[i] == df.columns[j] else miss
          diag = ismatch + df.iat[i-1,j-1]
          best = max(diag, up, left)
          df.iat[i, j] = best
          def fn(dir): 
            print(f"best for [{i},{j}] ({df.index[i]} {df.columns[j]}) is {dir} ", end="")

          if best == up:
            fn("up")
            print(f"from [{i-1}, {j}]")
            traceback.iloc[i,j] = [i-1,j]
          elif best == left:
            fn("left")
            print(f"from [{i}, {j-1}]")
            traceback.iat[i, j] = [i,j-1]
          elif best == diag:
            fn("diag")
            print(f"from [{i-1}, {j-1}]")
            traceback.iat[i, j] = [i-1,j-1]

  print(df)

  return df

df = main()

# print(df)