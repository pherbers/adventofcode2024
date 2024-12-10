import pygame
from pygame import Color

import numpy as np
from itertools import pairwise


with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()
lines = input_text.splitlines()
karte = np.zeros((len(lines), len(lines)), dtype=np.uint8)

for x, line in enumerate(lines):
    for y, c in enumerate(line.strip()):
        karte[y, x] = int(c)

colormap = [  # https://lospec.com/palette-list/dull-aquatic
    Color("#372f3a"),
    Color("#464459"),
    Color("#545e72"),
    Color("#5d7680"),
    Color("#6a9395"),
    Color("#7bad9f"),
    Color("#8eb29a"),
    Color("#b3c6b4"),
    Color("#c5d2ce"),
    Color("#d3d8d9"),
]

path_colormap = [
    Color("#8c8fae"),
    Color("#584563"),
    Color("#3e2137"),
    Color("#9a6348"),
    Color("#d79b7d"),
    Color("#f5edba"),
    Color("#c0c741"),
    Color("#647d34"),
    Color("#e4943a"),
    Color("#9d303b"),
    Color("#d26471"),
    Color("#70377f"),
    Color("#7ec4c1"),
    Color("#34859d"),
    Color("#17434b"),
    Color("#1f0e1c"),
]

# colormap = np.array([(c.r, c.g, c.b) for c in colormap])


def inbounds(pos, shape):
    return pos[0] >= 0 and pos[1] >= 0 and pos[0] < shape[0] and pos[1] < shape[1]


adjacency = list([np.array(a) for a in [(-1, 0), (0, -1), (0, 1), (1, 0)]])


# DFS function
def dfs(karte, start):
    open_set = [np.array(start)]
    closed_map = np.zeros(karte.shape, dtype=np.uint8)
    path_map = np.full(karte.shape, -1)

    while len(open_set) > 0:
        node = open_set.pop()
        height = karte[*node]
        for direction, adjacent in enumerate(adjacency):
            p = node + adjacent
            if not inbounds(p, closed_map.shape):
                continue
            if closed_map[*p]:
                continue
            if karte[*p] == height + 1:
                open_set.append(p)
                path_map[*p] = direction
        closed_map[*node] = 1

    peaks = np.where((closed_map * karte) == 9)
    for peak_x, peak_y in zip(*peaks):
        peak_start = np.array((peak_x, peak_y))

        # Hike down the mountain to whence you came
        yield hike_path(peak_start, path_map)


def hike_path(peak_start, path):
    hiker = peak_start.copy()
    yield hiker.copy()
    while path[*hiker] != -1:
        direction = adjacency[path[*hiker]]
        hiker -= direction
        yield hiker.copy()


# pygame setup
pygame.init()
pygame.display.set_caption("a short, exhaustive hike")
game_scale = 16
screen_size = np.array(karte.shape) * game_scale

screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
running = True

karte_surf = pygame.Surface(karte.shape)
karte_scale = pygame.Surface(screen_size)

# Draw background map
for (x, y), val in np.ndenumerate(karte):
    karte_surf.set_at((x, y), colormap[val])

path_surf = pygame.Surface(screen_size)
path_surf.set_colorkey(Color("Black"))

border_color = Color((16, 16, 16))


def draw_line(surf, p1, p2, color=Color("red"), offset=np.array((0, 0))):
    c1 = p1 * game_scale + game_scale / 2 + offset
    c2 = p2 * game_scale + game_scale / 2 + offset
    pygame.draw.line(surf, border_color, c1, c2, width=3)
    pygame.draw.line(surf, color, c1, c2, width=1)
    pygame.draw.circle(surf, border_color, c1, 1)
    pygame.draw.circle(surf, border_color, c2, 1)


# Find and draw hiking paths
def find_hiking_paths():
    starting_points = np.where(karte == 0)

    for start in zip(*starting_points):
        print(f"Searching for paths from {start}")
        # DFS Search
        dfs_it = dfs(karte, start)

        yield dfs_it


c = 0

hiking_paths = find_hiking_paths()

update_event = pygame.USEREVENT + 1
pygame.time.set_timer(update_event, 100)

# Draw counters
# offsets for better visibility
offset_grid_x, offset_grid_y = np.meshgrid(np.linspace(-6, 4, 6), np.linspace(-6, 4, 6))
col_index = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == update_event:
            try:
                hiking_path = next(hiking_paths)
            except StopIteration:
                print(f"Number of possible hikes: {c}")
                pygame.time.set_timer(update_event, 0)
                continue
            for path in hiking_path:
                c += 1
                # Draw path
                path_color = path_colormap[col_index]
                col_index += 1
                col_index %= len(path_colormap)
                offset = np.array(
                    [offset_grid_x.flat[col_index], offset_grid_y.flat[col_index]]
                )
                for prev, node in pairwise(path):
                    draw_line(path_surf, prev, node, path_color, offset=offset)

    # Render
    pygame.transform.scale_by(karte_surf, game_scale, karte_scale)

    screen.blit(karte_scale, (0, 0))
    screen.blit(path_surf, (0, 0))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60


pygame.quit()
