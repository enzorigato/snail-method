# Snail Method.

Imagine you have two rectangles. Have you ever wondered how many of the smaller you can fit into the big one? Maybe not, but here’s a simple tool you can use to find it.

## The idea behind the project.

Let $r_{1}$ and $r_{2}$ be two rectangles. To the best of my knowledge, there’s no result that states what is the maximum number of (non-overlapping) $r_{2}$ inside one single $r_{1}$ (whose copies are disposed horizontally or vertically, namely whose dimensions are, in general, parallel to the $r_{1}$ ones), avoiding classical methods of optimization, such as bin packing.

<p  align="center">
<img src="pics\snail_method_pic1.jpg">

However, the algorithm returns results for which I can’t find counterexamples that perform better than this, let’s say, “optimal conjecture”. Strictly speaking, from a pure theoretical point of view, either this is a method that always converges to the optimum (in this case I still need to find a proof of that), either there exists another method which can perform better. If you are able to find an answer to this question, please contact me!

### How does Snail Method work?

The basic idea, again, is that you have two rectangles of different dimensions. Let’s assume at least one can fit into the big one. The big rectangle can be partitioned into three distinct areas, namely <span style="color:green">horizontal</span>, <span style="color:orange">vertical</span> and the remainder rectangles, the so called <span style="color:blue">epsilon-rectangles</span>:

<p  align="center">
<img src="pics\snail_method_pic2.jpg">

Snail Method (the name arises in the algorithm filling procedure strategy, precisely it tries to do it in a “spiral” way, in a snail shape) easily computes how many small rectangles can be positioned in each area.

### On the complexity of the method.

Every disposition is fully identified by the number of horizontal columns (equivalently, vertical columns) of small boxes exists per area. Moreover, for every distinct disposition, the cardinality of small boxes per area is just a fixed number of operations.

<p  align="center">
<img src="pics\snail_method_pic3.jpg">

As a consequence, computational complexity is easily said to be mostly dependent on the magnitude of the difference of the dimensions of the rectangles: intuitively, the more $r_{2}$ is smaller than $r_{1}$, the more different eligible dispositions to be compared we have. More precisely, let's call $x_{1}$, $x_{2}$ the larger dimension of the two rectangles. Then the complexity of snail method is $O(\lfloor\frac{x_{1}}{x_{2}}\rfloor)$.

That’s the worst case. Snail Method stops earlier if it detects, for instance, optimum is reached by a surface comparison of the rectangles.

## The tech side.

Snail method has been fully developed in Python, and it’s mostly based on native libraries, such as tkinter for the GUI, but I also used numpy and matplotlib.

### How can I play with it?

In order to try Snail Method on your own, you should follow the following steps:
* download the project;
* install the requirements;
* run gui.py;
* let the interface guide you!

Working on the package creation...

## Contributors.

[enzorigato](https://github.com/enzorigato) is the only contributor (up to now!).

## Licence.

This project is licensed under the MIT License - see the LICENSE.md file for details.
