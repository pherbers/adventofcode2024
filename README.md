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
Switching to ternary thanks to numpys `base_repr` function made it possible, but the combinatorics make this surprisingly resource heavy. Early stopping helps out tho.

## Day 08
`np.where` saves the day again. `np.where` would I be today without that function.

## Day 09
Now entering: Edge Case City, `population <= len(me)`. Code so slow I have to use `tqdm`. Sums so large I need to `int64`. What has it come to?

## Day 10
Quick and Dirty Depth First Search! Because it is fun I made the DFS results an Iterable for visualizing. Should also keep memory efficiency through that.

## Day 11
Part 2 went from "oh no my RAM is in paging hell after 45 iterations" to "400ms execution time" by switching from a list to a dictionary (since the order of the stones is irrelevant, thanks reddit)

## Day 12
Fun task this time. For part 2 I initially wanted to do marching cubes, but the holes inside of plots would not have worked with what I tried. I came up with a weird way of doing a sweeping convolution with boolean material implication and diffs and sums. I'm not writing it down how it works (my mind is an enigma).

# Day 13
Part 1 was easy to brute force, but I had to give up on Part 2 because even my more efficient search did not work. There has to be a closed form solution, I'm pretty sure, that can give you all possible combinations... Maybe some other time.

# Day 14
Finally, using pygame is paying off! I do these visualizations more for myself, but this made Part 2 pretty straight forward.

# Day 15
I should make a proper pygame engine for this. Didn't think I would use my setup so often. Worked perfectly for the box pushing. Just needed a DFS again for part 2.

# Day 16
A Dijkstra AND a DFS?! Is this a crossover episode? No pygame this time, just matplotlib.
