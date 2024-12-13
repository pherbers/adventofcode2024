import numpy as np
import re

# from matplotlib import pyplot

with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()

in_re = re.compile(
    r"""Button A: X\+(\d+), Y\+(\d+)\s*Button B: X\+(\d+), Y\+(\d+)\s*Prize: X=(\d+), Y=(\d+)"""
)

machine_list = []
for find in in_re.findall(input_text):
    machine_list.append(
        {
            "a_x": int(find[1 - 1]),
            "a_y": int(find[2 - 1]),
            "b_x": int(find[3 - 1]),
            "b_y": int(find[4 - 1]),
            "p_x": int(find[5 - 1]),
            "p_y": int(find[6 - 1]),
        }
    )


def costfunc(a_n, b_n):
    return a_n * 3 + b_n


def play_machine(m):
    arr = np.zeros((100, 100))
    a_x = m["a_x"]
    a_y = m["a_y"]
    b_x = m["b_x"]
    b_y = m["b_y"]
    p_x = m["p_x"]
    p_y = m["p_y"]

    for a, b in np.ndindex(arr.shape):
        pos_x = a * a_x + b * b_x
        pos_y = a * a_y + b * b_y
        # print(a, b, pos_x, pos_y)
        if pos_x == p_x and pos_y == p_y:
            arr[a, b] = -costfunc(a, b)
    # print(a_x, a_y, b_x, b_y, p_x, p_y)
    a_n, b_n = np.unravel_index(np.argmin(arr), arr.shape)
    cost = int(-np.amin(arr))
    if cost > 0:
        print(f"Found best solution: ({a_n:3d}|{b_n:3d}): {cost:5d}")
    else:
        print("No possible solution for this machine")
    # pyplot.imshow(-arr, cmap="Greens")
    # pyplot.show()
    return cost, a_n, b_n


total_cost = sum([play_machine(m)[0] for m in machine_list])

print(f"Total cost: {int(total_cost)}")
