import numpy as np

from matplotlib import pyplot
from queue import PriorityQueue
from collections import defaultdict

with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()



B_WALL = 1
B_EMPTY = 0
mapsize = (71,71)

karte = np.full(mapsize, B_EMPTY)
maxlines = 1024
inlines = input_text.splitlines()
for line in inlines[:maxlines]:
    x,_,y = line.partition(",")
    karte[int(x),int(y)] = B_WALL

adjacency = [(-1, 0), (0, -1), (0, 1), (1, 0)]

def inbounds(pos, shape):
    return pos[0] >= 0 and pos[1] >= 0 and pos[0] < shape[0] and pos[1] < shape[1]

def dijkstra(karte, start, end):
    graph = np.full(
        (karte.shape[0], karte.shape[1]), np.iinfo(np.uint32).max, dtype=np.uint32
    )
    openset = PriorityQueue()
    openset.put((0, start[0], start[1]))  # x,y,rot
    prev = defaultdict(list)
    while not openset.empty():
        node_cost, node_x, node_y = openset.get()
        # print(node_x, node_y, rot)
        for x, y in adjacency:
            # print(x, y, r, c)
            adj_x = x + node_x
            adj_y = y + node_y

            if not inbounds((adj_x, adj_y), karte.shape):
                continue
            if karte[adj_x, adj_y] == B_EMPTY:
                if graph[adj_x, adj_y] > node_cost + 1:
                    graph[adj_x, adj_y] = node_cost + 1
                    openset.put((node_cost + 1, adj_x, adj_y))
                    prev[(adj_x, adj_y)] = [(node_x, node_y)]
                elif graph[adj_x, adj_y] == node_cost + 1:
                    prev[(adj_x, adj_y)].append((node_x, node_y))
                    # print("Double found", (x, y, r), (node_x, node_y, rot))
    return graph, prev


start = np.array((0,0))
end = np.array(karte.shape)-1

karte[*start] = B_EMPTY
karte[*end] = B_EMPTY

print(karte)
print(start, end)

graph, prev = dijkstra(karte, start, end)
graph[np.where(graph == np.iinfo(np.uint32).max)] = 0

pyplot.imshow(graph)
print(f"Running and running: {graph[*end]}")
pyplot.show()
morebytes = maxlines
while graph[*end] != 0:
    # drop the byte
    morebytes += 1
    x,_,y = inlines[morebytes].partition(",")
    karte[int(x),int(y)] = B_WALL

    #repeat until done
    graph, _ = dijkstra(karte, start, end)
    graph[np.where(graph == np.iinfo(np.uint32).max)] = 0
    print(".", end="", flush=True)


pyplot.imshow(graph)
print(f"Can't get out: {inlines[morebytes]}")
pyplot.show()
