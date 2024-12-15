import pygame
import numpy as np
import itertools

with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()

WIDEMODE = True

B_EMPTY = 0
B_CRATE = 2
B_CRATE_R = 3
B_WALL = 4
B_ROBOT = 6

karte_text, op_text = input_text.split("\n\n")

op_text = op_text.replace("\n", "")
n_steps = len(op_text)
steps = 0
ops = iter([o for o in op_text])
op_dict = {
    "^": np.array((-1,0)),
    "<": np.array((0,-1)),
    "v": np.array((1,0)),
    ">": np.array((0, 1))
}

karte_text = karte_text.replace(".", str(B_EMPTY))
karte_text = karte_text.replace("O", str(B_CRATE))
karte_text = karte_text.replace("#", str(B_WALL))
karte_text = karte_text.replace("@", str(B_ROBOT))

if WIDEMODE:
    karte = np.array([list(itertools.chain.from_iterable([(int(i), int(i)+1 if i == str(B_CRATE) else int(i)) for i in line])) for line in karte_text.splitlines()])
else:
    karte = np.array([[int(i) for i in line] for line in karte_text.splitlines()])
print(karte)

color_bg = "#4b4b5e"
color_crate = "#bf9a84"
color_crate_r = "#d4c9ba"
color_robot = "#946663"
color_wall = "#80627e"
color_grid =  "#797d91"

color_map = [
    color_bg, color_bg, color_crate, color_crate_r, color_wall, color_wall, color_robot
]

class Robot:
    def __init__(self, pos):
        self.pos = np.array(pos)
        global karte

    def move(self, dir):
        global karte
        if dir not in op_dict:
            return False
        d = op_dict[dir]
        move_to_pos = self.pos + d
        # Collision detection
        target = karte[*move_to_pos]
        if target == B_EMPTY:
            karte[*self.pos] = 0
            karte[*move_to_pos] = B_ROBOT
            self.pos = move_to_pos.copy()
            return True
        elif target == B_CRATE or target == B_CRATE_R:
            if WIDEMODE:
                return self.move_crate_wide(d)
            else:
                return self.move_crate(d)
        else:
            # Hit a wall, do nothing
            return False
        
    def move_crate(self, d):
        # move the crate as far as possible
        move_to_pos = self.pos + d
        crate_to = move_to_pos.copy()
        while True:
            crate_to += d
            if karte[*crate_to] == B_WALL:
                # Cant push because of wall
                return False
            if karte[*crate_to] == B_EMPTY:
                # can push crate
                karte[*self.pos] = 0
                karte[*move_to_pos] = B_ROBOT
                self.pos = move_to_pos.copy()
                karte[*crate_to] = B_CRATE
                return True
            
    def move_crate_wide(self, d):
        move_to_pos = self.pos + d
        success = move_crate(move_to_pos, d)
        if success:
            karte[*self.pos] = 0
            karte[*move_to_pos] = B_ROBOT
            self.pos = move_to_pos
        return success

    def __repr__(self):
        return f"p={self.pos[0]},{self.pos[1]}"
    
def move_crate(pos: np.ndarray, dirc: np.ndarray):
    open_set = [pos.copy()]
    closed_set = []
    closed_type = []
    while len(open_set) > 0:
        block_pos = open_set.pop()
        block = karte[*block_pos]
        if block == B_EMPTY:
            continue
        elif block == B_WALL:
            return False
        
        if block_pos.tobytes() in closed_set:
            continue

        if block == B_CRATE:
            pos_l = block_pos.copy()
            pos_r = block_pos + np.array((0,1))
        elif block == B_CRATE_R:
            pos_l = block_pos + np.array((0,-1))
            pos_r = block_pos.copy()
        closed_set.append(pos_l.tobytes())
        closed_set.append(pos_r.tobytes())

        open_set.append(pos_l+dirc)
        open_set.append(pos_r+dirc)
    
    for pos_byte, crate_type in zip(closed_set, itertools.cycle([B_CRATE, B_CRATE_R])):
        crate_pos = np.frombuffer(pos_byte, pos.dtype)
        karte[*crate_pos] = B_EMPTY

    for pos_byte, crate_type in zip(closed_set, itertools.cycle([B_CRATE, B_CRATE_R])):
        crate_pos = np.frombuffer(pos_byte, pos.dtype)

        new_crate_pos = crate_pos + dirc
        karte[*new_crate_pos] = crate_type

    return True
    
robot_start = np.array(np.where(karte == B_ROBOT)).reshape(2, -1)[...,0]
karte[np.where(karte == B_ROBOT)] = B_EMPTY
karte[*robot_start] = B_ROBOT
print(robot_start)
robot = Robot(robot_start)
# pygame setup
pygame.init()
pygame.display.set_caption("f*** my stupid robot life...")
game_scale = 16
screen_size = np.array(karte.shape)[::-1] * game_scale

screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
running = True

karte_surf = pygame.Surface(karte.shape[::-1])

karte_scale = pygame.Surface(screen_size)
pygame.transform.scale_by(karte_surf, game_scale, karte_scale)

def draw_grid(surf_size, grid_size, color_bg, color_grid):
    # from https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame
    blockSize = game_scale  # Set the size of the grid block
    surf = pygame.Surface(surf_size)
    surf.fill(color_bg)
    for x in range(0, surf_size[0], grid_size):
        pygame.draw.line(surf, color_grid, (x-1, 0), (x-1, surf_size[1]), 2)
    for y in range(0, surf_size[1], grid_size):
        pygame.draw.line(surf, color_grid, (0, y-1), (surf_size[0], y-1), 2)
    return surf


grid = draw_grid(screen_size, game_scale, color_bg, color_grid)

def calc_gps(karte):
    crate_x, crate_y = np.where(karte == B_CRATE)
    score = 0
    for c_x, c_y in zip(crate_x, crate_y):
        score += c_x * 100 + c_y
    return score


move_robot_event = pygame.USEREVENT + 1
pygame.time.set_timer(move_robot_event, 50)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == move_robot_event:
            try:
                op = next(ops)
                steps += 1
                pygame.display.set_caption(f"Robot move: {op} | ({steps:4}/{n_steps})")
                robot.move(op)
            except StopIteration:
                pygame.time.set_timer(move_robot_event, 0)
                pygame.display.set_caption("Robot done")
                print(calc_gps(karte))

    for (y,x), val in np.ndenumerate(karte):
        karte_surf.set_at((x,y), color_map[val])
    pygame.transform.scale_by(karte_surf, game_scale, karte_scale)
    # flip() the display to put your work on screen
    screen.blit(karte_scale, (0, 0))
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60


pygame.quit()
