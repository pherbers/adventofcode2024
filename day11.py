import numpy as np


with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()

stones = input_text.split()

iterations = 75

for i in range(iterations):
    newstones = []
    for stone in stones:
        istone = int(stone)
        if istone == 0:
            newstones.append("1")
        elif len(stone) % 2 == 0:
            stone1 = int(stone[: len(stone) // 2])
            stone2 = int(stone[len(stone) // 2 :])
            newstones.append(str(stone1))
            newstones.append(str(stone2))
        else:
            newstones.append(str(istone * 2024))
    stones = newstones
    print(f"Iteration {i+1:02d}, {len(stones):8d}")
