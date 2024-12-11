import numpy as np
from tqdm import tqdm
from collections import defaultdict

with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()

stone_list = [int(i) for i in input_text.split()]

field = defaultdict(int)

for stone in stone_list:
    field[stone] += 1

iterations = 75

for it in range(iterations):
    newfield = defaultdict(int)
    for stone, nstones in tqdm(field.items()):
        if stone == 0:
            newfield[1] += nstones
        elif (sl := (len(s := str(stone)))) % 2 == 0:
            newfield[int(s[: sl // 2])] += nstones
            newfield[int(s[sl // 2 :])] += nstones
        else:
            newfield[stone * 2024] += nstones
    field = newfield
    print(f"Iteration {it+1:02d}, {sum(field.values()):16d} stones")
    # print(field)
