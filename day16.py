import numpy as np
import re

from matplotlib import pyplot
from queue import PriorityQueue, Queue
from collections import defaultdict

with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()

B_WALL = ord("#")
B_EMPTY = ord(".")

karte = np.array(
    [np.fromiter([ord(c) for c in line], np.int8) for line in input_text.splitlines()],
    np.int8,
)


def dijkstra(karte, start, end):
    graph = np.full(
        (karte.shape[0], karte.shape[1], 4), np.iinfo(np.uint32).max, dtype=np.uint32
    )
    graph[start[0], start[1]]
    openset = PriorityQueue()
    openset.put((0, start[0], start[1], 1))  # x,y,rot
    prev = defaultdict(list)
    while not openset.empty():
        node_cost, node_x, node_y, rot = openset.get()
        # print(node_x, node_y, rot)
        if rot == 0:
            adj = (
                (node_x, node_y, 1, 1000),
                (node_x, node_y, 3, 1000),
                (node_x + 1, node_y, rot, 1),
            )
        elif rot == 1:
            adj = (
                (node_x, node_y, 2, 1000),
                (node_x, node_y, 0, 1000),
                (node_x, node_y + 1, rot, 1),
            )
        elif rot == 2:
            adj = (
                (node_x, node_y, 1, 1000),
                (node_x, node_y, 3, 1000),
                (node_x - 1, node_y, rot, 1),
            )
        elif rot == 3:
            adj = (
                (node_x, node_y, 2, 1000),
                (node_x, node_y, 0, 1000),
                (node_x, node_y - 1, rot, 1),
            )
        for x, y, r, c in adj:
            # print(x, y, r, c)
            if karte[x, y] == B_EMPTY:
                if graph[x, y, r] > node_cost + c:
                    graph[x, y, r] = node_cost + c
                    openset.put((node_cost + c, x, y, r))
                    prev[(x, y, r)] = [(node_x, node_y, rot)]
                elif graph[x, y, r] == node_cost + c:
                    prev[(x, y, r)].append((node_x, node_y, rot))
                    # print("Double found", (x, y, r), (node_x, node_y, rot))
    return graph, prev


# Return all paths from start to end
def dfs_all_paths(prev_map, end, rot):
    open_set = Queue()
    for r in rot:
        open_set.put((end[0], end[1], r))
    closed_set = set()
    while not open_set.empty():
        node = open_set.get()
        print(node)
        if node in closed_set:
            continue
        closed_set.add(node)
        if node in prev_map:
            for n in prev_map[node]:
                open_set.put(n)
    return closed_set


start = np.array(np.where(karte == ord("S"))).reshape(2)
end = np.array(np.where(karte == ord("E"))).reshape(2)

karte[*start] = B_EMPTY
karte[*end] = B_EMPTY

print(karte)
print(start, end)
graph, prev = dijkstra(karte, start, end)
graph_best = np.min(graph, axis=2)
graph_best[np.where(karte == B_WALL)] = 0

end_rot = np.where(graph[end[0], end[1], ...] == np.min(graph[end[0], end[1], ...]))[0]
print(end_rot)
possible_spaces = dfs_all_paths(prev, end, end_rot)
possible_spaces = set([(x, y) for x, y, _ in possible_spaces])
print(len(possible_spaces))

pyplot.imshow(graph_best)
x, y = zip(*possible_spaces)
pyplot.plot(y, x, "b.")
print(f"Reindeer score: {graph_best[*end]}")
pyplot.show()
