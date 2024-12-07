# Advent of Code 2024 Diary
## Day 01
ez one liners. Did this one on my phone so i don't have the code anymore sry.

## Day 02
I love it when I can use obscure numpy functions.

## Day 03
Tricky to do with regex. It seems easy at first, but then you notice the rules about greedy and non-greedy searches with regex. I had to use splits and pratitions instead.

## Day 04
The first part alone got me pretty messed up. I spent an embarrassingly long time on the diagonals with list comprehensions until I noticed that I can just do a staggered roll and rotate. Part 2 was more direct for me at least. I wrote a 2D Convolution function for text, which worked like a charm.

## Day 05
Part 1 was pretty straight forward. For part 2 I thought I could find a DAG with the Kahn algorithm, but alas, the input data was cyclic. Too bad. So I just switched numbers and rechecked until the line was sorted. Fortunately, the pages did not contain circles.

## Day 06
I don't care what comes after this, this is my visual magnum opus for this year. Fully simulated in pygame, even for part 2. It takes hours to run, but it's a nice screen saver!

Edit: It took hours for the simulation to run through. And then I accidentally cancelled it at around 200 Simulations left because I wanted to work on day 7... 

Edit Edit: FINALLY got all the bugs fixed, after two days... Also a speedup, it now takes 5 minutes in pygame.

## Day 07
Part 1 was ez with a bit of binary juggling, but of course part 2 has three operands.
Switching to ternary thanks to numpys base_repr function made it possible, but the combinatorics make this surprisingly resource heavy. Early stopping helps out tho.
