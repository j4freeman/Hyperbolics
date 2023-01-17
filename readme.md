# Exploring Hyperbolic Geometry (as a Computer Scientist)

Always been a fan of the whole "if you can't explain it, you don't understand it" line of thinking, and as I've spent some time trying to wrap my head around hyperbolic geometry and its application to graph embeddings as of late, figured might as well make a git page about it. 

## Preliminaries

Most every computer scientist can remember back to the early days of their studies when they had to do that most computer scientific of things: drawing a binary tree by hand. Now, if you're anything like me, you remember no matter how you try to draw it, if the tree gets big enough you're going to run out of room on the paper and just cause yourself general annoyance. Now, there's a very good reason for that, and it has to do with a property that we all probably also learned, in that the number of nodes at a given level $l$, where the level of the root is 0, of a balanced binary tree is $2^l$. At face value this is just another boring old equation, but when we compare it to the growth patterns of a standard circle in a 2d Euclidean space, the again familiar $\pi r^2$. Here we note something critical, while the volume of Euclidean space increases polynomially with its radius, a tree increases exponentially with its depth. 

This difference, while something most of us just store and don't think much of, actually has profoud implications: a tree of sufficient depth cannot be well represented in a standard Euclidean space, the amount of tree simply grows faster than the amount of space. For visualizations graph layouts can be envisioned to mitigate the problem, but for embeddings, where distances in the embedding space should correspond to distances in the graph, we are left with no choice but to arbitrarily increase dimensionality to the detriment of most any best practice. 

Now this again at face value might seem a big claim to make: and it is - it wasn't proved rigorously until Bourgain's 1986 paper which involves a lot of lovely math and works on a Banach space (which is a superset of Euclidean space satisfying some axioms we don't really need to worry about here). Nevertheless, the proof is out there if your functional analysis is good enough to read it: no complete k-ary tree can be embedded in a Euclidean space without distorting its edge distances. 

# Expand with cool visualizations about attempts to embed trees in Euclidean spaces, add citation for Bourgain

## Enter: Hyperbolic Geometry

Luckily for us, there's far more out there than Euclidean geometry, and before you go getting scared, it's not some high fancy theoretic concept, the Earth is spherical (said to have Elliptic Geometry), which itself is not Euclidean. You can go look at most any map, and without that knowledge you'd probably be deeply confused as to why flights from San Francisco to Dubai need to go over the North Pole. Asking that question gets us to an important concept: that most concepts in Euclidean space have direct generalizations in non-Euclidean spaces. 

# Expand with cool visualizations about spherical geometry and that SFO/Dubai

### Geodesics
First amongst those generalizations is that of the geodesic. A very fancy sounding word that means little more than a straight line. It should be common knowledge that if you have two points in space, the shortest distance between them (assuming no obstacles) is a straight line. Well, as we saw above, the flight path on the Earth's elliptic surface is not the same as on the Euclidean map, and that's simply because the geometry works out that way - the geodesic on elliptical geometry has its own solution (called a great circle), which has its own fancy formulas that we don't need to go into here. What we can note though, is that the formula for the distance between two points (in two dimensions for ease of example) highlights the differences between the two geometries. 

$d_{Euclid}(x,y) = \sqrt{(x_1 - y_1)^2 + (x_2 - y_2)^2}$

$d_{Elliptic}(x,y) = r * arccos(sin(x_1)sin(y_1) + cos(x_1)cos(y_1)cos(x_2-y_2))$

Where $r$ is the radius of the sphere being computed on. So, despite vastly different formulas, these equations represent the exact same thing: the length of the shortest path between the two points on their respective surfaces. 

### Curvature

Now you may be wondering, gosh, why are the two so different? Well, it comes down to one aspect: curvature. There's plenty of other spaces with more complex properties, but in our limited case, curvature is all there is. Euclidean space, as we all know, is a simple plane, expanding endlessly everywhere, perfectly flat and abstract. The further we get away from some point, the distance from ourselves to that point increases at some constant pace. Elliptic geometry is different, if we start from some point, our distance from that point does not grow linearly, as on Earth if you walk in one direction endlessly you'll end back right where you started - if you go far enough the distance to where you started actually starts to decrease. The key difference is curvature, where Euclidean space is flat, or have zero curvature, elliptic spaces have a positive curvature. 

This finally brings us to what we've been building towards - hyperbolic geometry. Imagine the Earth as a perfect sphere - with some unit curvature $c$. We can then imagine the opposite of this, some surface with curvature $-c$. That is to say, if in an elliptical space the space curves down, relative to say yourself on the Earth's surface, a hyperbolic space will do much the opposite - it will curve upwards. 

# again - add cool graphics

## Hyperbolic Properties

So, with all that out of the way, we can roughly conceive of what hyperbolic geometry is. Now the questions become - why is it useful? And if it is, how do we represent something we can barely visualize? Both, luckily for us, are deeply well studied. 

### Hyperbolic spaces grow exponentially

So, through all the above we've noted two things: Euclidean space isn't our only option, and trees grow exponentially, faster than Euclidean space does. As we've been going on and on about hyperbolics, it would seem natural to examine the formula for the area of a circle in a hyperbolic space: 

$\pi R^2 R (cosh(2r/R) - 1)$

Now you may be saying - well that just adds a cosine term, that's hardly useful. And if that was a standard cosine, you'd be right, but we're looking at it's hyperbolic variant which has an exceedingly interesting property, it's just a decomposition of the standard exponential: $e^x = sinh(x) + cosh(x)$ - both the hyperbolic sine and cosines are exponential curves. Given that, it becomes clear that the area of the hyperbolic space grows exponentially with its radius, just as the trees we're looking at do. 

### The Poincaré Disk Model

Now that we see we can fit the tree into a hyperbolic space, we need to question how to represent them. Representing a Euclidean space is easy enough - we percieve our world as one. An elliptic space is likewise easy, because we see plenty of spheres in our world too. Hyperbolic space is different however, it grows faster than Euclidean space, and in the same sense, the hyperbolic plane is larger than the Euclidean, even though both are infinite. 

One of the earliest (and easiest to visualize) attempts at visualizing this was done by Henri Poincaré in the late 19th century. The actual maths behind the representation is again complex and past the scope of what we can cover here, but a key visualization lets us understand the exponential growth:

# insert graphic of a tesselation

Critically - each colored region in the disk has the same hyperbolic area - with the center of the disk having the least density and density increasing exponentially towards the edges. 

### The Hyperboloid Model

The disk model is excellent for visualizations, but the maths behind it are numerically unstable. Another model of hyperbolic geometry, the Hyperboloid model proposed by Minkowski, instead of representing the plane on a disk represents it on the upper plane of a $n+1$ dimensional hyperboloid, and if you like myself can't for the life of you remember what a hyperboloid looks like, well, here you are:

# insert graphic of a hyperboloid

### Relating the two

As both this and the disk model represent the same thing, it seems clear there should be some mapping between the two - and indeed it's even simpler than you would expect. The disk model is merely the projection of the hyperboloid onto it's center, something again hard to visualize without a graphic: 

# insert the hyperpboloid/disk mapping graphic thingy

This has excellent properties for visualition - any model trained on the hyperboloid can easily be mapped to a disk for ease of visualization, something we will make extensive use of later on. 

## Hyperbolic Neural Networks

Now all this is well and good, we've described the movitation for using hyperbolic spaces as well as what they are in the first place. What we've largely neglected is just how annoying they are in general - we don't usually get nice convenient easy to remember formulas, and visualization and intuition is largely a pain. To actually embed these trees however we need to learn some mapping, from the vertices of the tree to points in hyperbolic space. Rik Sarkar has an excellent paper on a simple algorithm to do this for an arbitrary tree, but the method is restricted to abstract structures. It also considers purely minimizing distortion of the tree - which again in an abstract case is useful but in the real world there's often other characteristics to consider. Additionally there are many use cases where a given graph may exhibit some properties of a tree but not be perfectly so - an aspect well studied and typically measured by Gromov's $\delta$-hyperbolicity which seeks to define to what extent a given space (or graph) is hyperbolic by measuring, for any four points $x, y, z, w$ in that space: 

$(x, z)_w >= min((x,y)_w, (y,z)_w) - \delta$

such that: $(a,b)_c = 1/2(d(x,y) + d(x,z) - d(y,z)). $

Which also previews an alternative definition based on the triangle inequality, but again the math becomes more obsucre. 

With all that in mind, lets assume we have some tree structure and want to embed it to a hyperbolic space. While at first glance you might say great, lets just use a hyperbolic distance metric on a standard autoencoder architecture and call it a day, that unfortunately misses a few key steps. Chami et al's fantastic paper covers them all in detail, but here we'll still try to describe some of the key steps. 

# Euclidean to Hyperbolic Mappings



### add citation for Sarkar algorithm, gromov hyperbolicity, chami's HGCN
