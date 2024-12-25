import numpy as np
from tqdm import tqdm

with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()

edges = [tuple(a.split("-")) for a in input_text.splitlines()]
# print(edges)
nodes = set()
for a,b in edges:
    nodes.add(a)
nodes = list(sorted(nodes))

n_nodes = len(nodes)

e = np.zeros((n_nodes, n_nodes), dtype=bool)
for a,b in edges:
    i_a = nodes.index(a)
    i_b = nodes.index(b)
    e[i_a, i_b] = True
    e[i_b, i_a] = True

def find_cycles(start, e, depth=3):
    cycles = []
    openset = [(start, 0, [])]
    while len(openset) > 0:
        node, d, prevs = openset.pop()
        cons = np.argwhere(e[...,node])
        if d < depth:
            for c in cons.flat:
                if d==0 or c != prevs[-1]:
                    openset.append((c, d+1, prevs+[node]))
        elif d == depth:
            if node == start:
                cycles.append(prevs)
    return cycles

# Educate urself: https://en.wikipedia.org/wiki/Clique_problem
def find_all_max_cliques(e):
    R = set()
    X = set()
    P = set(range(e.shape[0]))

    return BronKerbosch(R, P, X)

# https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
def BronKerbosch(R:set, P:set, X:set):
    if len(P) == 0 and len(X) == 0:
        return [frozenset(R)]
    results = []
    for v in P:
        nv = set(np.argwhere(e[...,v]).flat)
        vs = set([v])

        res = BronKerbosch(R.union(vs), P.intersection(nv), X.intersection(nv))
        P = P.difference(vs)
        X = X.union(vs)
        results.extend(res)
    return results

cycles = []
for i, node in enumerate(tqdm(nodes)):
    cycles.extend(find_cycles(i, e))
cycles_text = [[nodes[c] for c in cycle] for cycle in cycles]
cycles_set = set([frozenset(c) for c in cycles_text])
print(f"Cycles found: {len(cycles_set)}")

cycles_t = list(filter(lambda c: any([n.startswith("t") for n in c]), cycles_set))
print(f"Cycles with the T: {len(cycles_t)}")

print("Finding cliques...")
cliques = []
cliques = find_all_max_cliques(e)
cliques_text = [[nodes[c] for c in sorted(clique)] for clique in sorted(cliques, key=len)]
print("All cliques:")
for clique in cliques_text:
    print(" > " + ",".join(clique))
