import numpy as np

with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()


# e = """47|53
# 97|13
# 97|61
# 97|47
# 75|29
# 61|13
# 75|53
# 29|13
# 97|29
# 53|29
# 61|53
# 97|53
# 61|29
# 47|13
# 75|47
# 97|75
# 47|61
# 75|61
# 47|29
# 75|13
# 53|13

# 75,47,61,53,29
# 97,61,53,29,13
# 75,29,13
# 75,97,47,61,53
# 61,13,29
# 97,13,75,29,47"""
e = input_text
rulesstr, _, pagesstr = e.partition("\n\n")

from collections import defaultdict

rules = defaultdict(list)

for r in rulesstr.splitlines():
    k, _, v = r.partition("|")
    rules[int(k)].append(int(v))

pages = []
for p in pagesstr.splitlines():
    pages.append([int(i) for i in p.split(",")])

print(rules)
print(pages)


def check_page(page):
    for pi, p in enumerate(page):
        if p in rules:
            for r in rules[p]:
                if r in page:
                    ri = page.index(r)
                    if ri < pi:
                        return (pi, ri)
    return -1


c = 0
incorrect = []
for page in pages:
    if check_page(page) == -1:
        print(",".join([str(s) for s in page]) + " is valid")
        c += page[(len(page)) // 2]
    else:
        print(",".join([str(s) for s in page]) + " is invalid")
        incorrect.append(page)
print(c)
print(incorrect)


from collections import deque


class Graph:
    def __init__(self, n):
        self.n = n
        self.graph = defaultdict(list)
        self.in_degree = [0] * n

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.in_degree[v] += 1


def kahn_topological_sort(graph):
    # Queue to hold nodes with no incoming edges
    queue = deque([node for node in range(graph.n) if graph.in_degree[node] == 0])

    topological_order = []

    while queue:
        node = queue.popleft()
        topological_order.append(node)

        # For each outgoing edge from the current node
        for neighbor in graph.graph[node]:
            # Decrease the in-degree of the neighbor
            graph.in_degree[neighbor] -= 1
            # If the neighbor has no other incoming edges, add it to the queue
            if graph.in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Check if topological sorting is possible (graph should have no cycles)
    if len(topological_order) == graph.n:
        return topological_order
    else:
        # If not all nodes are in topological order, there is a cycle
        return "Graph has at least one cycle"


g = Graph(max([max(p) for p in rules.values()]) + 1)
for r in rulesstr.splitlines():
    k, _, v = r.partition("|")
    g.add_edge(int(k), int(v))

topo = kahn_topological_sort(g)
print(topo)


def sort_page(page):
    while (t := check_page(page)) != -1:
        i, j = t
        pi = page[i]
        pj = page[j]
        page[j] = pi
        page[i] = pj
    print(page)


c2 = 0
for page in incorrect:
    sort_page(page)
    c2 += page[(len(page)) // 2]
print(c2)
