def get_all_kmers(frags, k) -> list[str]:
  if k is None:
    raise RuntimeError("Need to provide k")
  
  kmers = set()
  
  for frag in frags:
    leng = len(frag)
    if leng <= 4:
      kmers.add(frag)
    else:
      # sliding window
      i = 0
      while i <= leng - k:
        kmer = frag[i:i+k]
        kmers.add(kmer)
        i += 1

  return list(kmers)

def find_overlap(kmer, rest):
  """
  kmer = HAPP
  kmers = ["NESS", "APPI"]
  HAPP
    APPI
  """
  leng = len(kmer)
  init = kmer[1:leng]
  for frag in rest:
    guess = frag[0:leng-1]
    if guess == init:
      return frag

def construct_directed_graph(kmers: list[str], start_kmer: str):
  # init = "HAPP"
  # kmers.remove(init)
  # kmers.insert(0, init)
  print(kmers)
  graph = {}
  for kmer in kmers:
    res = find_overlap(kmer, kmers)
    graph[kmer] = res
    print(f"{kmer} -> {res}")

  return graph

def build_genome(graph, start_node):
  curr_node = start_node
  seq = curr_node
  run = [curr_node]

  while curr_node != None:
    nxt = graph[curr_node]
    if nxt == None:
      break
    seq += nxt
    run.append(nxt)
    curr_node = nxt

  return seq, run

fragments = [
  "HAPPI",
  "PINE",
  "INESS",
  "APPIN",
]

kmers = get_all_kmers(fragments, k=4)
graph = construct_directed_graph(kmers, "HAPP")
print(graph)
[genome, arr] = build_genome(graph, "HAPP")
print(arr)


# def merge_max_overlap(strings):
#     max_overlap = 0
#     merged_string = None
#     pair_to_merge = (None, None)

#     # Find the pair of strings with the maximum overlap
#     for i in range(len(strings)):
#         for j in range(len(strings)):
#             if i != j:
#                 s1, s2 = strings[i], strings[j]
#                 overlap_len = len(s2)
#                 while overlap_len > 0 and not s1.endswith(s2[:overlap_len]):
#                     overlap_len -= 1
#                 if overlap_len > max_overlap:
#                     max_overlap = overlap_len
#                     pair_to_merge = (i, j)
#                     merged_string = s1 + s2[overlap_len:]

#     # If no overlap, just concatenate
#     if max_overlap == 0:
#         merged_string = strings[0] + strings[1]
#         pair_to_merge = (0, 1)

#     # Return the pair to merge, the resulting merged string, and the length of the overlap
#     return pair_to_merge, merged_string, max_overlap

# def shortest_common_superstring(strings):
#     while len(strings) > 1:
#         pair_to_merge, merged, _ = merge_max_overlap(strings)
#         first, second = pair_to_merge
#         # Merge the pair into one string, remove the originals
#         strings.append(merged)
#         strings.pop(max(first, second))  # Remove higher index first to avoid reindexing
#         strings.pop(min(first, second))
    
#     return strings[0]

# # Example usage
# strings = ['HAPP', 'APPI', 'PPIN', 'PINE', 'INES', 'NESS']
# result = shortest_common_superstring(strings)
# print(result)
