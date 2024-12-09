import numpy as np
from itertools import batched
from tqdm import tqdm

print("Booting...")
with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()

nums = [int(n) for n in input_text]
memsize = np.sum(nums)

print(f"\tmemsize:\t{memsize}")

memory = np.full(memsize, -1, dtype=np.int16)

head = 0
filenum = 0
numiter = iter(nums)
for i in batched(nums + [0], 2):
    filelen, spacelen = i
    memory[head : head + filelen] = filenum
    head += filelen
    filenum += 1

    head += spacelen

memcpy = memory.copy()
memcpy2 = memory.copy()
# print(memory)

print("Defragmenting... ", end="")

lhead = 0
rhead = memsize - 1

# Search for first free space
while memory[lhead] != -1:
    lhead += 1

c = np.uint64(0)

while lhead < rhead:
    # Move file from right to left
    memory[lhead] = memory[rhead]
    memory[rhead] = -1

    # Search free space from the left
    while memory[lhead] != -1:
        lhead += 1
    # Search file to move from the right
    while memory[rhead] == -1:
        rhead -= 1


def checksum(mem):
    check = np.uint64(0)
    for i, x in enumerate(mem):
        if x != -1:
            check += i * x
    return check


c = checksum(memory)

print(f"Done\n\tFiles:\t\t{np.max(memory)}\n\tChecksum:\t{c}")

print("Defragmenting again... ")

lhead = 0
rhead = memsize - 1
f = -1
last_block_pos = rhead

with tqdm(total=memsize) as pbar:
    while rhead > 0:
        # search block from the right
        while (f := memcpy[rhead]) == -1:
            rhead -= 1

        block_end = rhead

        # found block end, looking for block start
        while memcpy[rhead] == f:
            rhead -= 1

        block_len = block_end - rhead

        # look for space from the right
        lhead = 0
        lblockstart = 0
        while lhead - lblockstart < block_len and lhead <= rhead:
            while lhead <= rhead and memcpy[lhead] != -1:
                lhead += 1

            lblockstart = lhead
            while lhead - lblockstart <= block_len and memcpy[lhead] == -1:
                lhead += 1
                # print(f, block_len, lhead - lblockstart, lhead, rhead)
        if lhead <= rhead or lhead - lblockstart >= block_len:
            # print(f"putting {rhead} to {lblockstart}")
            memcpy[lblockstart : lblockstart + block_len] = f
            memcpy[rhead + 1 : block_end + 1] = -1
        else:
            # print(f"rejected with {lhead} > {rhead}")
            pass
        pbar.update(last_block_pos - rhead)
        last_block_pos = rhead
        # print(f"{memcpy[:20]}", end="")

# memstr = list(nums)
# rhead = len(memstr)
# while rhead > 0:
#     # get the block on the right
#     fsize = memstr[rhead]

#     # Search for an empty block on the left
#     lhead = 1
#     while memstr[lhead] < fsize and lhead < rhead:
#         lhead += 2
#     if lhead < rhead:
#         # Foudna  place to put this block
#         memstr[lhead] = 0
#         memstr.insert(lhead, fsize)

c2 = checksum(memcpy)
# print("".join([str(m) if m >= 0 else "." for m in memcpy2]))
# print("".join([str(m) if m >= 0 else "." for m in memcpy]))
print(f"Done\n\tFiles:\t\t{np.max(memcpy)}\n\tChecksum:\t{c2}")
