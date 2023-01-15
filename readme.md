### Exploring Hyperbolic Geometry (as a Computer Scientist)

Always been a fan of the whole "if you can't explain it, you don't understand it" line of thinking, and as I've spent some time trying to wrap my head around hyperbolic geometry and its application to graph embeddings as of late, figured might as well make a git page about it. 

## Preliminaries

Most every computer scientist can remember back to the early days of their studies when they had to do that most computer scientific of things: drawing a binary tree by hand. Now, if you're anything like me, you remember no matter how you try to draw it, if the tree gets big enough you're going to run out of room on the paper and just cause yourself general annoyance. Now, there's a very good reason for that, and it has to do with a property that we all probably also learned, in that the number of nodes at a given level $l$, where the level of the root is 0, of a balanced binary tree is $2^l$. At face value this is just another boring old equation, but when we compare it to the growth patterns of a standard circle in a 2d Euclidean space, the again familiar $\pi r^2$. Here we note something critical, while the volume of Euclidean space increases polynomially with its radius, a tree increases exponentially with its depth. 

This difference, while something most of us just store and don't think much of, actually has profoud implications: a tree of sufficient depth cannot be well represented in a standard Euclidean space, the amount of tree simply grows faster than the amount of space. For visualizations graph layouts can be envisioned to mitigate the problem, but for embeddings, where distances in the embedding space should correspond to distances in the graph, we are left with no choice but to arbitrarily increase dimensionality to the detriment of most any best practice. 

Now this again at face value might seem a big claim to make: and it is - it wasn't proved rigorously until Bourgain's 1986 paper which involves a lot of lovely math and works on a Banach space (which is a superset of Euclidean space satisfying some axioms we don't really need to worry about here). Nevertheless, the proof is out there if your functional analysis is good enough to read it: no complete k-ary tree can be embedded in a Euclidean space without distorting its edge distances. 

### Expand with cool visualizations about attempts to embed trees in Euclidean spaces, add citation for Bourgain

## Enter: Hyperbolic Geometry

Luckily for us, there's far more out there than Euclidean geometry, and before you go getting scared, it's not some high fancy theoretic concept, the Earth is spherical (said to have Elliptic Geometry), which itself is not Euclidean. You can go look at most any map, and without that knowledge you'd probably be deeply confused as to why flights from San Francisco to Dubai need to go over the North Pole. Asking that question gets us to an important concept: that most concepts in Euclidean space have direct generalizations in non-Euclidean spaces. 

### Expand with cool visualizations about spherical geometry and that SFO/Dubai

# Geodesics
First amongst those generalizations is that of the geodesic. A very fancy sounding word that means little more than a straight line. It should be common knowledge that if you have two points in space, the shortest distance between them (assuming no obstacles) is a straight line. Well, as we saw above, the flight path on the Earth's elliptic surface is not the same as on the Euclidean map, and that's simply because the geometry works out that way - the geodesic on elliptical geometry has its own solution (called a great circle), which has its own fancy formulas that we don't need to go into here. What we can note though, is that the formula for the distance between two points (in two dimensions for ease of example) highlights the differences between the two geometries. 

$d_{Euclid}(x,y) = \sqrt{(x_1 - y_1)^2 + (x_2 - y_2)^2}$

$d_{Elliptic}(x,y) = r * arccos(sin(x_1)sin(y_1) + cos(x_1)cos(y_1)cos(x_2-y_2))$

Where $r$ is the radius of the sphere being computed on. So, despite vastly different formulas, these equations represent the exact same thing: the length of the shortest path between the two points on their respective surfaces. 

# Curvature

Now you may be wondering, gosh, why are the two so different? Well, it comes down to one aspect: curvature. There's plenty of other spaces with more complex properties, but in our limited case, curvature is all there is. Euclidean space, as we all know, is a simple plane, expanding endlessly everywhere, perfectly flat and abstract. The further we get away from some point, the distance from ourselves to that point increases at some constant pace. Elliptic geometry is different, if we start from some point, our distance from that point does not grow linearly, as on Earth if you walk in one direction endlessly you'll end back right where you started - if you go far enough the distance to where you started actually starts to decrease. The key difference is curvature, where Euclidean space is flat, or have zero curvature, elliptic spaces have a positive curvature. 

This finally brings us to what we've been building towards - hyperbolic geometry. Imagine the Earth as a perfect sphere - with some unit curvature $c$. We can then imagine the opposite of this, some surface with curvature $-c$. That is to say, if in an elliptical space the space curves down, relative to say yourself on the Earth's surface, a hyperbolic space will do much the opposite - it will curve upwards. 

### again - add cool graphics

## Hyperbolic Properties

So, with all that out of the way, we can roughly conceive of what hyperbolic geometry is. Now the questions become - why is it useful? And if it is, how do we represent something we can barely visualize? Both, luckily for us, are deeply well studied. 

# Hyperbolic spaces grow exponentially

# The Poincare Model

# The Hyperboloid Model

## Hyperbolic Neural Networks
