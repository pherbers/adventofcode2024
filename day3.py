import re

with open("day3.txt") as f:
    e=f.read()
#e="xmul(2,4)&mul[3,7]!^don't()don't()_mul(5,5)+mul(32,64](mul(11,8)undo()do()?mul(8,5))"*2
donts = e.split("don't()")
e = donts[0]
for dont in donts[1:]:
    _, _, do = dont.partition("do()")
    e += do

mulre=re.compile(r"mul\((\d+),(\d+)\)")
instances=mulre.finditer(e)
c = 0
for match_i in instances:
    c += int(match_i.group(1)) * int(match_i.group(2))
print(c)

