import pygame
from pygame import Color

import numpy as np


with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()
lines = input_text.splitlines()
karte = np.array([[ord(s) - 64 for s in line] for line in lines], dtype=np.uint8)
print(karte)

adjacency = list([np.array(a) for a in [(-1, 0), (0, -1), (0, 1), (1, 0)]])


def inbounds(pos, shape):
    return pos[0] >= 0 and pos[1] >= 0 and pos[0] < shape[0] and pos[1] < shape[1]


# DFS function
def dfs(karte, start):
    open_set = [np.array(start)]
    closed_map = np.zeros(karte.shape, dtype=np.uint8)
    plotpoints = []
    plant = karte[*start]

    while len(open_set) > 0:
        node = open_set.pop()
        if closed_map[*node]:
            continue
        else:
            closed_map[*node] = 1
        if karte[*node] == plant:
            plotpoints.append(node.copy())
            for adj in adjacency:
                p = node + adj
                if not inbounds(p, karte.shape):
                    continue
                open_set.append(p.copy())
    return plotpoints


def calc_perimeter(plot, karte):
    perimeter = 0
    for p_x, p_y in plot:
        for adj in adjacency:
            p_a = np.array((p_x + adj[0], p_y + adj[1]))
            if not inbounds(p_a, karte.shape) or karte[*p_a] != karte[p_x, p_y]:
                perimeter += 1
    return perimeter


def calc_sides(plot):
    plot = np.array(plot)
    min_x, min_y = np.min(plot, axis=0)
    max_x, max_y = np.max(plot, axis=0)
    open_map = np.zeros((max_x - min_x + 3, max_y - min_y + 3))
    plot -= np.array((min_x - 1, min_y - 1))
    open_map[*zip(*plot)] = 1
    # print(open_map)

    # Source: It came to me in a dream
    delta_top = (
        np.sum(
            np.diff(
                np.logical_and(open_map[1:, ...], np.logical_not(open_map[:-1, ...])),
                axis=1,
            )
        )
        // 2
    )

    delta_bottom = (
        np.sum(
            np.diff(
                np.logical_and(open_map[:-1, ...], np.logical_not(open_map[1:, ...])),
                axis=1,
            )
        )
        // 2
    )

    delta_left = (
        np.sum(
            np.diff(
                np.logical_and(open_map[..., 1:], np.logical_not(open_map[..., :-1])),
                axis=0,
            )
        )
        // 2
    )

    delta_right = (
        np.sum(
            np.diff(
                np.logical_and(open_map[..., :-1], np.logical_not(open_map[..., 1:])),
                axis=0,
            )
        )
        // 2
    )
    # print(delta_top, delta_bottom, delta_left, delta_right)

    return delta_top + delta_bottom + delta_left + delta_right


c = 0
c2 = 0

for (x, y), pflanze in np.ndenumerate(karte):
    if pflanze == 0:
        continue
    plot = dfs(karte, (x, y))
    area = len(plot)
    perimeter = calc_perimeter(plot, karte)
    sides = calc_sides(plot)
    c += area * perimeter
    c2 += area * sides
    print(
        f"Plant {chr(pflanze+64)}\tArea:\t{area}\tPerimeter\t{perimeter}\tSides:\t{sides}\tCost 1:\t{area*perimeter}\tCost 2:\t{sides*area}"
    )
    karte[*zip(*plot)] = 0

print(f"Total cost 1: {c}")
print(f"Total cost 2: {c2}")
