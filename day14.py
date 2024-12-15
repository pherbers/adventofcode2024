# Example file showing a basic pygame "game loop"
import pygame
from pygame import Color
import numpy as np
import re

with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()

karte = np.zeros((101, 103), dtype=np.uint8)


class Robot:
    def __init__(self, robot_id, pos, vel):
        self.robot_id = robot_id
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        global karte
        karte[*self.pos] += 1

    def draw(self, surf):
        color = colormap[min(karte[*self.pos], len(colormap) - 1)]
        surf.set_at(self.pos, color)

    def move(self):
        global karte
        self.pos += self.vel
        self.pos %= karte.shape
        karte[*self.pos] += 1

    def __repr__(self):
        return f"p={self.pos[0]},{self.pos[1]} v={self.vel[0]},{self.vel[1]}"


robot_re = re.compile(r"^p=(-?\d+),(-?\d+)\s+v=(-?\d+),(-?\d+)$")
robots = []
for i, line in enumerate(input_text.splitlines()):
    match = robot_re.match(line)
    px, py, vx, vy = match[1], match[2], match[3], match[4]
    robots.append(Robot(i, (int(px), int(py)), (int(vx), int(vy))))

print("\n".join([str(r) for r in robots]))

# pygame setup
pygame.init()
pygame.display.set_caption("f*** my stupid robot life...")
game_scale = 8
screen_size = np.array(karte.shape) * game_scale

# Colors
colormap = [
    Color("#ad2340"),
    Color("#d65b49"),
    Color("#f28f61"),
    Color("#fab269"),
]

color_block = (138, 143, 196)
color_bg = Color("#060423")
color_crate = (240, 212, 114)
color_grid = Color("#0e0b38")
color_robot = (216, 128, 56)


screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
running = True

karte_surf = pygame.Surface(karte.shape)
karte_surf.set_colorkey(0)

karte_scale = pygame.Surface(screen_size)
karte_scale.set_colorkey(0)
pygame.transform.scale_by(karte_surf, game_scale, karte_scale)


def draw_grid(surf_size, grid_size, color_bg, color_grid):
    # from https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
    blockSize = game_scale  # Set the size of the grid block
    surf = pygame.Surface(surf_size)
    surf.fill(color_bg)
    for x in range(0, surf_size[0], grid_size):
        pygame.draw.line(surf, color_grid, (x, 0), (x, surf_size[1]), 2)
    for y in range(0, surf_size[1], grid_size):
        pygame.draw.line(surf, color_grid, (0, y), (surf_size[0], y), 2)
    return surf


grid = draw_grid(screen_size, game_scale, color_bg, color_grid)

move_robot_event = pygame.USEREVENT + 1
pygame.time.set_timer(move_robot_event, 10)
step = 0


def calc_security(karte):
    kx, ky = karte.shape
    tl = karte[: kx // 2, : ky // 2]
    tr = karte[kx // 2 + 1 :, : ky // 2]
    bl = karte[: kx // 2, ky // 2 + 1 :]
    br = karte[kx // 2 + 1 :, ky // 2 + 1 :]
    # print(karte.shape, tl.shape, tr.shape, bl.shape, br.shape)
    sec = np.sum(tl) * np.sum(tr) * np.sum(bl) * np.sum(br)

    return sec


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == move_robot_event or event.type == pygame.KEYDOWN:
            karte.fill(0)
            for robot in robots:
                robot.move()
            step += 1
            security = calc_security(karte)
            print(f"Step {step:2}, Security: {security:4}")
            if step == 999999:
                pygame.time.set_timer(move_robot_event, 0)
                pass
            if (step - 79) % 101 == 0:
                karte_surf.fill(0)
                for robot in robots:
                    robot.draw(karte_surf)
                pygame.transform.scale_by(karte_surf, game_scale, karte_scale)
                # flip() the display to put your work on screen
                screen.blit(grid, (0, 0))
                screen.blit(karte_scale, (0, 0))
                pygame.image.save(screen, f"img/{step:06}.png")

    karte_surf.fill(0)
    for robot in robots:
        robot.draw(karte_surf)
    pygame.transform.scale_by(karte_surf, game_scale, karte_scale)
    # flip() the display to put your work on screen
    screen.blit(grid, (0, 0))
    screen.blit(karte_scale, (0, 0))
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60


pygame.quit()
