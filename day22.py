import numpy as np
from tqdm import tqdm

with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()


def step1(num):
    m1 = num * 64
    m2 = mix(num, m1)
    m3 = prune(m2)
    return m3


def step2(num):
    m1 = np.floor_divide(num, 32)
    m2 = mix(num, m1)
    m3 = prune(m2)
    return m3


def step3(num):
    m1 = num * 2048
    m2 = mix(num, m1)
    m3 = prune(m2)
    return m3


def mix(num1, num2):
    return np.bitwise_xor(num1, num2)


def prune(num):
    return np.mod(num, 16777216)


def next_secret(num):
    m1 = step1(num)
    m2 = step2(m1)
    m3 = step3(m2)
    return m3

iterations = 2000
n = np.array([int(x) for x in input_text.splitlines()], dtype=np.int64)
secrets = np.zeros((iterations+1, n.shape[0]), dtype=np.int64)
secrets[0,...] = n
for i in range(iterations):
    secrets[i+1,...] = next_secret(secrets[i,...])

secretsum = np.sum(secrets[-1])
print(f"Secret sum: {secretsum}")

prices = np.mod(secrets, 10)
price_changes = np.diff(prices, axis=0)

possible_price_changes = np.meshgrid(np.arange(-9,10),np.arange(-9,10),np.arange(-9,10),np.arange(-9,10))

buymask = np.zeros(prices.shape, dtype=np.int32)

print("Checking possible iterations")
indices = set()
for i in tqdm(range(iterations - 4)):
    p = price_changes[i:i+4,...]
    for monke in range(prices.shape[1]):
        indices.add(tuple(p[...,monke]))
print(f"{len(indices)} possible price change keys")
print("Acquiring bananas")

bananas = []
for ip in tqdm(indices):
    p = np.array(ip).reshape(-1,1)
    sell_price = {}
    for i in range(iterations - 4):
        change_hit = np.all(p == price_changes[i:i+4,...], axis=0)
        if np.any(change_hit):
            price_slice = prices[i+4:i+5,...]
            first_price = price_slice[np.where(change_hit.reshape(1,-1))]
            for sp in np.argwhere(change_hit).flat:
                if int(sp) not in sell_price:
                    sell_price[sp] = price_slice[..., int(sp)][0]
    total_price = sum(sell_price.values())
    bananas.append((total_price, p))
    
best_bananas, winning_price = max(bananas, key=lambda x: x[0])
print(f"Banana hoard: {best_bananas} at {tuple(winning_price)}")
