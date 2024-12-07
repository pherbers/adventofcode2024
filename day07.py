import numpy as np

with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()

lines_str = input_text.splitlines()
lines = []


def check(values, result):
    # print(values, result)
    n_ops = len(values) - 1
    for a in range(2**n_ops):
        res = values[0]
        for x in range(n_ops):
            # print(f"{a:b}, {(2 ** x):b}")
            op_type = np.bitwise_and(a, 2**x)
            if op_type == 0:
                # Add
                res += values[x + 1]
            else:
                # Mult
                res *= values[x + 1]
        if res == result:
            print(f"Found result for {result}:{values}")
            return result
    return 0


def check2(values, result):
    # print(values, result)
    n_ops = len(values) - 1
    for a in range(3**n_ops):
        res = values[0]
        for x in range(n_ops):
            ternary = np.base_repr(a, base=3).zfill(n_ops)
            op_type = int(ternary[x])

            if op_type == 0:
                # Add
                res += values[x + 1]
            elif op_type == 1:
                # Mult
                res *= values[x + 1]
            elif op_type == 2:
                # Concat
                res = int(str(res) + str(values[x + 1]))
            if res > result:
                return 0
        # print(f"{ternary}, {res}")
        if res == result:
            print(f"Found result for {result}:{values}")
            return result
    return 0


c = 0


for line in lines_str:
    result, _, values = line.partition(": ")
    c += check2([int(v) for v in values.split(" ")], int(result))

print(f"Result: {c}")
