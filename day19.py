import time
from collections import defaultdict

with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()

# We are going full CYK algo baybeeee

rules, _, words = input_text.partition("\n\n")
rules = sorted([r.strip() for r in rules.split(",")], key=len, reverse=True)

print(f"The rules: {rules}")


def recognize(rules, word):
    openset = [([], word)]
    closedset = set()
    correct = set()
    while len(openset) > 0:
        build, w = openset.pop()
        # print("="*len(build), "."*len(w))
        for rule in rules:
            if len(w) == 0:
                correct.add(tuple(build))
            if w.startswith(rule):
                b = build + [rule]
                new_w = w[len(rule) :]
                if new_w not in closedset:
                    openset.append((b, new_w))
                    closedset.add(new_w)
    return correct


def recognize_all(rules, word):
    openset = [([], word)]
    correct = set()
    while len(openset) > 0:
        build, w = openset.pop()
        # print("="*len(build), "."*len(w))
        for rule in rules:
            if len(w) == 0:
                correct.add(tuple(build))
            if w.startswith(rule):
                b = build + [rule]
                new_w = w[len(rule) :]
                openset.append((b, new_w))
    return correct


count = 0
total = 0
for word in words.splitlines():
    successful_builds = recognize(rules, word)
    if len(successful_builds) > 0:
        count += 1
        total += len(successful_builds)
        print(f"{word} matches the language in {len(successful_builds)} ways")
    else:
        print(f"{word} does not match the language")
print(f"{count} words match the language of the towels ({total} total ways)")

# import concurrent.futures

# with concurrent.futures.ThreadPoolExecutor() as executor:
#     future_word = {
#         executor.submit(recognize, rules, word): word for word in words.splitlines()
#     }
#     for future in concurrent.futures.as_completed(future_word):
#         word = future_word[future]
#         successful_builds, t = future.result()
#         if len(successful_builds) > 0:
#             count += 1
#             print(
#                 f"{word} matches the language in at least {len(successful_builds)} ways (took {t:04f} seconds)"
#             )
#         else:
#             print(f"{word} does not match the language")
# print(f"{count} words match the language of the towels")
