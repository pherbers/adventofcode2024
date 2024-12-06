with open("day4.txt") as f:
    e = f.read()
# e = """MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX"""

# e = """ABCDEF
# GHIJKL
# MNOPQR
# STUVWX
# YZ1234
# 567890
# BLABLI
# SCHOKO"""
lines = e.splitlines()
print(len(lines), len(lines[0]))
c = 0


def rollstr(str, i):
    return str[i:] + str[:i]


def rotstr(str_arr):
    return [
        "".join([str_arr[i][j] for i in range(len(str_arr))])
        for j in range(len(str_arr[0]))
    ]


# lines
for line in lines:
    c += line.count("XMAS")
    c += line.count("SAMX")

print(c)

# columns
columns = rotstr(lines)
for col in columns:
    c += col.count("XMAS")
    c += col.count("SAMX")
print(c)

x = len(lines)
y = len(lines[0])


shift_r = rotstr([rollstr(s + " ", i) for i, s in enumerate(lines)])
shift_l = rotstr([rollstr(s + " ", -i) for i, s in enumerate(lines)])
# diag1 = [[lines[j - i][i] for i in range(min(j + 1, y))] for j in range(x)]
# diag2 = [[lines[y - i][j - i] for i in range(min(j + 1, x))] for j in range(y)]
# diag3 = [[lines[j - i][y - i] for i in range(min(j + 1, y))] for j in range(x)]
# diag4 = [[lines[y - i][y - j + i] for i in range(min(j + 1, x))] for j in range(y)]
# diag4 = [[columns[y - i][j - i] for i in range(min(j + 1, y))] for j in range(x)]
# diag2 = [[lines[x - i][j - i] for i in range(j + 1)] for j in range(x + y)]

for d in shift_r + shift_l:
    d = "".join(d)
    c += d.count("XMAS")
    c += d.count("SAMX")

# [print(" ".join(lin)) for lin in lines]
# print("")
# [print(" ".join(col)) for col in columns]
# print("")
# print("\n".join(shift_r))
# print("")
# print("\n".join(shift_l))
print(c)


def textconvolve_2d(text, pattern):
    score = 0
    py = len(pattern)
    px = len(pattern[0])
    tx = len(text[0])
    ty = len(text)
    # print(tx, ty, px, py)
    for x in range(tx - px + 1):
        for y in range(ty - py + 1):
            cut = [l[x : x + px] for l in text[y : y + py]]
            # print(x, y, cut, pattern)
            score += pattern_score(cut, pattern)
    return score


def pattern_score(p1, p2):
    for i in range(len(p2[0])):
        for j in range(len(p2)):
            if p2[j][i] == " ":
                continue
            elif p2[j][i] != p1[j][i]:
                return 0
    return 1


pat1 = """M M
 A 
S S
""".splitlines()
pat2 = """M S
 A 
M S
""".splitlines()
pat3 = """S S
 A 
M M
""".splitlines()
pat4 = """S M
 A 
S M
""".splitlines()
s = 0
s += textconvolve_2d(lines, pat1)
s += textconvolve_2d(lines, pat2)
s += textconvolve_2d(lines, pat3)
s += textconvolve_2d(lines, pat4)
print(s)
