import numpy as np
from tqdm import tqdm

with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()

def read_code(text:str):
    if text.strip() == "":
        return None, None
    l = list(text.splitlines())
    typ = "lock"
    if l[0][0] == ".":
        # key
        l.reverse()
        typ = "key"
    
    arr = [0,0,0,0,0]
    for lnum, line in enumerate(l):
        for cnum, c in enumerate(line):
            if c == "#":
                arr[cnum] = lnum
    return np.array(arr), typ

def find_keys(lock, keys):
    kl = keys + lock
    kf = kl <= 5
    kt = np.all(kf, axis=1)
    return np.where(kt)[0]


locks = []
keys = []

for text in input_text.split("\n\n"):
    t, typ = read_code(text)
    if typ == "lock":
        locks.append(t)
    elif typ == "key":
        keys.append(t)

print(f"Locks: {len(locks)}")
print(f"Keys: {len(keys)}")

vlocks = np.vstack(locks)
vkeys = np.vstack(keys)

key_dict = {}

for lock in tqdm(locks):
    fitting_key_indices = find_keys(lock, vkeys)
    fitting_keys = vkeys[fitting_key_indices,...]
    # print(lock, "=>", fitting_keys)
    key_dict[tuple(lock)] = fitting_keys

score = 0
for l, k in key_dict.items():
    score += len(k)
print("Key-Lock combos:", score)
