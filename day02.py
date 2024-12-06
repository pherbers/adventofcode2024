import numpy as np

with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()


count = 0


def isvalid(b):
    a = np.diff(b)
    return np.all(np.logical_and(a > 0, a <= 3)) or np.all(
        np.logical_and(a < 0, a >= -3)
    )


for i in input_text.splitlines():
    a = [int(j) for j in i.split()]

    if isvalid(a):
        count += 1
    else:
        for i in range(0, len(a)):
            s1 = a[:i]
            s1.extend(a[i + 1 :])
            if isvalid(s1):
                count += 1
                print(a)
                break

print(count)
