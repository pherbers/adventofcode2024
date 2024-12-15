import numpy as np
import re
import time

from matplotlib import pyplot

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


def play_advanced_machine(m):
    a_x = m["a_x"]
    a_y = m["a_y"]
    b_x = m["b_x"]
    b_y = m["b_y"]
    p_x = m["p_x"] + 10000000000000
    p_y = m["p_y"] + 10000000000000

    max_a = max(p_x // a_x, p_y // a_y) + 1
    max_b = max(p_x // b_x, p_y // b_y) + 1
    print(max_a, max_b)
    arr = np.zeros((max_a, max_b))

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
    pyplot.imshow(-arr, cmap="Greens")
    pyplot.show()
    return cost, a_n, b_n


def play_advanced_machine2(m):
    a_x = m["a_x"]
    a_y = m["a_y"]
    b_x = m["b_x"]
    b_y = m["b_y"]
    p_x = m["p_x"] + 10000000000000
    p_y = m["p_y"] + 10000000000000

    pos_x = 0
    pos_y = 0
    max_a = min(p_x // a_x, p_y // a_y) + 1
    max_b = min(p_x // b_x, p_y // b_y) + 1
    a = 0
    b = max_b
    print(max_a, max_b)
    cost = costfunc(max_a, max_b)

    while True:
        if pos_x < p_x and pos_y < p_y:
            a += 1
        else:
            b -= 1
        if a > max_a or b < 0:
            a = 0
            b = 0
            break

        pos_x = a * a_x + b * b_x
        pos_y = a * a_y + b * b_y
        if pos_x == p_x and pos_y == p_y:
            cost = min(cost, costfunc(a, b))
            print(a, b, costfunc(a, b))
        # print(a, b, pos_x, pos_y)

    if cost == costfunc(max_a, max_b):
        print("Found no advanced solution")
        return 0
    print(f"Found advanced solution: {cost:5d}")
    return cost


total_cost = sum([play_machine(m)[0] for m in machine_list])
total_cost2 = sum([play_advanced_machine2(m) for m in machine_list])

# print(play_advanced_machine2(machine_list[0]))
# print(play_machine(machine_list[0]))
print(f"Total cost: {int(total_cost)}")
print(f"Total cost 2: {int(total_cost2)}")
