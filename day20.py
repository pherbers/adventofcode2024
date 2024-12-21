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

adjacency = [(-1, 0), (0, -1), (0, 1), (1, 0)]

def a_star(karte, start, end):
    graph = np.full(karte.shape, np.iinfo(np.uint32).max, dtype=np.uint32)
    fMap = np.full(karte.shape, 2**32, dtype=np.float64)

    graph[*start] = 0
    openset = PriorityQueue()
    fMap[*start] = h(start[0], start[1], end[0], end[1])
    openset.put((fMap[*start], start[0], start[1]))  # x,y,rot
    prev = defaultdict(list)

    while not openset.empty():
        _, node_x, node_y = openset.get()
        if node_x == end[0] and node_y == end[1]:
            break
        for dx, dy in adjacency:
            x = dx + node_x
            y = dy + node_y
            if karte[x, y] == B_EMPTY:
                c = graph[(node_x, node_y)] + 1
                if graph[x,y] > c:
                    graph[x, y] = c
                    dist = h(x, y, end[0], end[1])
                    openset.put((dist, x, y))
                    prev[x,y] = (node_x, node_y)
    return graph, prev

def h(x, y, ex, ey):
    return np.linalg.norm((x-ex, y-ey))

# Return path from start to end
def reconstruct_path(prev_map, end, rot):
    current = (end[0], end[1])
    path = [current]
    while current in prev_map:
        current = prev[current]
        path.append(current)
    return path


start = np.array(np.where(karte == ord("S"))).reshape(2)
end = np.array(np.where(karte == ord("E"))).reshape(2)

karte[*start] = B_EMPTY
karte[*end] = B_EMPTY

print(karte)
print(start, end)
graph, prev = a_star(karte, start, end)

graph[np.where(karte == B_WALL)] = 0

# path = reconstruct_path(prev, end, start)
# print(len(path))
count = 0

cuts = []

for nx, ny in np.ndindex((karte.shape[0]-2, karte.shape[1]-2)):
    x = nx - 1
    y = ny - 1
    if karte[x,y] == B_WALL:
        if karte[x-1, y] == B_EMPTY and karte[x+1, y] == B_EMPTY:
            c_l = int(graph[x-1, y])
            c_r = int(graph[x+1, y])
            shortcut = abs(c_l - c_r)
            if shortcut >= 100:
                count+=1
                cuts.append((x,y, shortcut))
        if karte[x, y-1] == B_EMPTY and karte[x, y+1] == B_EMPTY:
            c_u = int(graph[x, y-1])
            c_d = int(graph[x, y+1])
            shortcut = abs(c_u - c_d)
            if shortcut >= 100:
                count+=1
                cuts.append((x,y, shortcut))

print(count)
pyplot.imshow(graph)
x, y, shortcut = zip(*cuts)
pyplot.plot(y, x, "r.")
pyplot.show()
