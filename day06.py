# Example file showing a basic pygame "game loop"
import pygame
import numpy as np

with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()

input_text = input_text.replace(".", "0")
input_text = input_text.replace("#", "1")

start_pos = (0, 0)

lines = input_text.splitlines()
karte = np.zeros((len(lines), len(lines)), dtype=np.uint8)
visited = np.zeros((len(lines), len(lines)), dtype=np.uint8)
for x, line in enumerate(lines):
    for y, c in enumerate(line.strip()):
        if c == "^":
            start_pos = (y, x)
            continue

        karte[y, x] = int(c)


# pygame setup
pygame.init()
pygame.display.set_caption("f*** my stupid guard life...")
game_scale = 6
screen_size = np.array(karte.shape) * game_scale

color_block = (138, 143, 196)
color_bg = (28, 22, 24)
color_crate = (240, 212, 114)
color_path = (154, 64, 126)
color_guard = (216, 128, 56)

screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
running = True

karte_surf = pygame.Surface(karte.shape)

karte_scale = pygame.Surface(screen_size)
pygame.transform.scale_by(karte_surf, game_scale, karte_scale)

guard_dir = 0
guard_pos = np.array(start_pos)
guard_sprite = pygame.Surface((game_scale, game_scale))

guard_sprite.fill(color_guard)
pygame.draw.line(
    guard_sprite, (255, 255, 255), (0, game_scale), (game_scale // 2 - 1, 0)
)
pygame.draw.line(
    guard_sprite,
    (255, 255, 255),
    (game_scale - 1, game_scale),
    (game_scale // 2, 0),
)

move_guard_event = pygame.USEREVENT + 1


crate_pos = np.array((0, 0))
crate_index = 0
first_try = True


def reset():
    global karte_surf
    global karte
    global first_try
    global crate_pos
    global crate_index
    global guard_history
    global visited
    visited = np.zeros((len(lines), len(lines)), dtype=np.uint8)

    global guard_dir
    global guard_pos
    guard_dir = 0
    guard_pos = np.array(start_pos)
    if not first_try:
        if crate_index >= guard_history.shape[1]:
            global running
            global loops
            running = False
            print(f"Simulation finished. {len(set(loops))} simulations end in loops.")
            return
        karte[*crate_pos] = 0
        gp = guard_history[..., crate_index]
        # print(gp)
        crate_index += 1
        # guard_pos = gp
        # guard_dir = gd
        crate_pos = gp
        karte[*crate_pos] = 2

        print(f"Resetting simulation, attempt ({crate_index}/{guard_history.shape[1]})")

    karte_surf.fill(color_bg)
    for iy, ix in np.ndindex(karte.shape):
        k = karte[iy, ix]
        if k == 1:
            karte_surf.set_at((iy, ix), color_block)
        elif k == 2:
            karte_surf.set_at((iy, ix), color_crate)
        else:
            karte_surf.set_at((iy, ix), color_bg)


reset()
reset_flag = False
guard_history = None


def move_guard():
    global guard_dir
    global guard_pos
    global karte
    global visited
    global guard_history
    global crate_index

    if guard_dir == 0:
        new_pos = guard_pos + np.array((0, -1))
    if guard_dir == 1:
        new_pos = guard_pos + np.array((1, 0))
    if guard_dir == 2:
        new_pos = guard_pos + np.array((0, 1))
    if guard_dir == 3:
        new_pos = guard_pos + np.array((-1, 0))

    if visited[*guard_pos] == 0:
        visited[*guard_pos] = guard_dir + 1

    # OOB detection
    if (
        new_pos[0] < 0
        or new_pos[1] < 0
        or new_pos[0] >= karte.shape[0]
        or new_pos[1] >= karte.shape[1]
    ):
        return 1

    # Collision detection
    if karte[*new_pos] >= 1:
        # Rotate instead
        guard_dir = (guard_dir + 1) % 4
    else:
        if first_try:
            # guard_history.append((guard_pos, guard_dir))
            pass
        guard_pos = new_pos
        karte_surf.set_at(guard_pos, color_path)

    # Loop Detection
    if visited[*guard_pos] == (guard_dir + 1):
        # print(guard_pos, visited[*guard_pos], guard_dir, crate_pos, np.sum(visited > 0))
        return 2

    return 0


loops = []
pygame.time.set_timer(move_guard_event, 1)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == move_guard_event and first_try:
            move_result = move_guard()
            if move_result == 1:
                print(
                    f"Reached the border with {np.sum(np.clip(visited, 0, 1))} visited"
                )
                reset_flag = True
        if event.type == move_guard_event and not first_try and reset_flag == False:
            while (move_result := move_guard()) == 0:
                pass
            if move_result == 1:
                print(
                    f"Reached the border with {np.sum(np.clip(visited, 0, 1))} visited"
                )
                reset_flag = True
            if move_result == 2:
                loops.append(crate_index)
                print(f"Loop detected! This is number {len(loops)}")
                reset_flag = True

            # fill the screen with a color to wipe away anything from last frame
            screen.fill("purple")

            # RENDER YOUR GAME HERE
            pygame.transform.scale_by(karte_surf, game_scale, karte_scale)

            screen.blit(karte_scale, (0, 0))
            screen.blit(
                pygame.transform.rotate(guard_sprite, -90 * guard_dir),
                guard_pos * game_scale,
            )
    if first_try:
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        # RENDER YOUR GAME HERE
        pygame.transform.scale_by(karte_surf, game_scale, karte_scale)

        screen.blit(karte_scale, (0, 0))
        screen.blit(
            pygame.transform.rotate(guard_sprite, -90 * guard_dir),
            guard_pos * game_scale,
        )
    # flip() the display to put your work on screen
    pygame.display.flip()
    if reset_flag:
        reset_flag = False
        if move_result == 2:
            pass
            pygame.image.save_extended(screen, f"loop_{len(loops)}.png")
        if first_try:
            pygame.time.set_timer(move_guard_event, 50)
            guard_history = np.array(np.nonzero(visited))
            print(guard_history)
            first_try = False
        reset()

    clock.tick(60)  # limits FPS to 60


pygame.quit()
