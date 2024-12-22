import numpy as np
from tqdm import tqdm

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
shortcuts = []
cutlen = 20
for x in range(-cutlen, cutlen+1):
    for y in range(-cutlen, cutlen+1):
        if abs(x) + abs(y) <= cutlen:
            shortcuts.append((x,y))

def inbounds(pos, shape):
    return pos[0] >= 0 and pos[1] >= 0 and pos[0] < shape[0] and pos[1] < shape[1]

for x, y in tqdm(np.ndindex((karte.shape[0], karte.shape[1])), total=karte.shape[0]*karte.shape[1]):
    if karte[x,y] == B_EMPTY:
        for cx, cy in shortcuts:
            if not inbounds((x+cx, y+cy), karte.shape):
                continue
            if karte[x+cx, y+cy] == B_EMPTY:
                cc = int(graph[x, y])
                ct = int(graph[x + cx, y + cy])
                shortcut = (ct - cc) - abs(cx) - abs(cy)
                if shortcut >= 100:
                    count+=1
                    cuts.append(((x,y), (cx,cy), shortcut))

pyplot.imshow(graph)
# x, y, shortcut = zip(*cuts)
cuts = sorted(cuts, key=lambda c: c[2])
cuts_dict = defaultdict(list)
for cut in cuts:
    cuts_dict[cut[2]].append((cut[0], cut[1]))
for cv, ci in cuts_dict.items():
    print(cv, len(ci))
# pyplot.plot(y, x, "r.")
print(f"Total cuts: {count}")
pyplot.show()
