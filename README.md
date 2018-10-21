# Puzzle

I've recently taken up a fondness for puzzles. Over a conversation one night,
we joked how cool it would be to have a digital puzzle. It actually
wouldn't be such a crazy idea - each puzzle piece would need to have some sort of
tiny sensor to understand it's location relative to the others, and some tiny
digital display that a mapped portion of an image would be shown on. Given that
we have something like the Kindle, the technology for "long lasting and low power
images" didn't seem that far off.

But the use of sensors is a bit out of my budget and current knowledge base. As
I usually do, I thought of breaking the problem into smaller pieces (pun intended).
Perhaps there is a similar problem I can solve that would be a step in the right 
direction? How about a robot that solves puzzles? 

## High Level Algorithm

A "robot puzzle solver" means that we do the following:

 1. We take a picture of all the puzzle pieces on some consistently colored surface.
 2. The puzzle pieces are segmented.
 3. We represented features and edges of the pieces.
 4. Based on these features, the segmented pieces are put together by an algorithm.

## Variables

Some things we would need to account for in the above (and these are general notes 
for now).

 - the puzzle pieces would ideally have consistent lighting and all be turned with picture upwards.
 - the camera, even from the top down, would introduce a bit of skew, both for shape and for color.
 - we can't make any assumption about the shape or position of the pieces. This means that although we could represent an edge as some sort of curve, the second you introduce a weirdo pieces that doesn't work well with the assumption, the algorithm breaks. For this reason, we might consider a pixel-based approach.
 - It could be the case that the algorithm can solve a puzzle as would a human - perhaps the edge pieces are easiest to do first, and then work from corners in?
 - We could do a recursive backtracking approach, where we start with edges, then work inwards from the corners, and choose the most probable piece given each new location with two "decided" edges. But as soon as the probabilities of a correct piece drop below some threshold, we should turn back.
 - Puzzles are real, and thus inherently imperfect. There needs to be an allowed margin of error.

## Applications

As silly as this is, there are some fun applications for a robot puzzle solver.

 - Puzzles are currently ranked on number of pieces, but I've found this isn't a good representation for how difficult they are. The robot puzzle solver could come up with a metric that represents difficulty based on the algorithm.
 - Has anyone ever wondered how much harder it is to solve a puzzle if you are color blind? Given a metric of difficulty, we can see how that changes with different variables removed. For example, if we remove color, how much longer does the algorithm take?

# Puzzle Solver

I want to document this process, because it's a relatively complex problem that requires
image processing, machine learning, and lots of creativity that will feel overwhelming if not broken
into... pieces (okay I'll stop that). The first thing I decided to do was work with some "dummy" data.
I'm actually set up in a good position because I have a fully assembed puzzle that I can photograph, label
with "ground truth," and then test by breaking apart and photographing the pieces in many different
ways. But to start, I want to just try and represent a puzzle.
