Date: 2012-09-13
Title: Bouncing Balls with Pygame
Tags: python, pygame
Slug: bouncing-balls
Category: Blog

![Bouncing Balls with Pygame](./images/bouncingballs.png)

I have recently played around with Pygame module. It was a fun experience. I decided to use Pygame to write a simple classic bouncing balls simulation.

You can have a look at the code [here](https://github.com/khuevu/pygames/tree/master/bouncingball)

The Ball object has methods to detect collisions with walls and other balls; callable method `update()` to update its position and method `draw` to redraw. BallWorld is the Game object containing game logics. It contains the list of balls, loop through all balls to update their positions each refresh.  

A few things to note: 

* Each ball object has a `CollisionResponse` object. `CollisionResponse` object contains information on the coming collision: new speed, direction. If the ball is not likely to collide at the moment (not going to collide within a very small EPSILON time), the collision time will be set to infinity.
* Positions of ball objects will be calculated at a fixed time interval (`TimeStep`) to calibrate ball movements per frame refresh. 
* The use of EPSILON number to estimate comparison as we will not have exact numbers when calculating with float type

Have fun !. 

Ah, well, it is not actually a game per se, but it is fun to watch all the balls bouncing. You can try to adjust the number of balls, speeds, etc...


