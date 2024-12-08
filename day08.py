import numpy as np

with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()


karte = np.array([[ord(x) for x in y] for y in input_text.splitlines()], dtype=np.byte)
nodes = np.zeros(karte.shape)
nodes2 = np.zeros(karte.shape)

dot = ord(".")

print(karte)

unique = np.unique(karte)


def find_antinodes(pos1, pos2):
    if np.all(pos1 == pos2):
        return None, None
    delta = pos2 - pos1
    return pos1 - delta, pos2 + delta


def inbounds(pos, shape):
    # Why is there no np function for this? Am I stupid??
    return pos[0] >= 0 and pos[1] >= 0 and pos[0] < shape[0] and pos[1] < shape[1]


print([chr(u) for u in unique])

for u in unique:
    if u == dot:
        continue
    indices = np.array(np.where(karte == u)).transpose()
    # print(indices)
    for i in indices:
        for j in indices:
            if np.all(i == j):
                continue
            a1, a2 = find_antinodes(i, j)
            # print(i, j, a1, a2)
            if inbounds(a1, karte.shape):
                nodes[*a1] = 1
            if inbounds(a2, karte.shape):
                nodes[*a2] = 1
print(nodes)
print(np.count_nonzero(nodes))


print("Part Deux")


def find_antinodes2(pos1, pos2, bounds):
    if np.all(pos1 == pos2):
        return None, None

    delta = pos2 - pos1
    positions = []
    d = np.array(pos1)
    while inbounds(d, bounds):
        positions.append(np.array(d))
        d -= delta
    d = np.array(pos2)
    while inbounds(d, bounds):
        positions.append(np.array(d))
        d += delta

    return positions


for u in unique:
    if u == dot:
        continue
    indices = np.array(np.where(karte == u)).transpose()
    # print(indices)
    for i in indices:
        for j in indices:
            if np.all(i == j):
                continue
            positions = find_antinodes2(i, j, karte.shape)
            # print(i, j, positions)
            for a in positions:
                if inbounds(a, karte.shape):
                    nodes2[*a] = 1

print(nodes2)
print(np.count_nonzero(nodes2))
