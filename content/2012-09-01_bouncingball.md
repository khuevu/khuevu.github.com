Title: Bouncing Balls with Pygame
Tags: python, pygame
Category: Technology
Image: /images/bouncingballs.png
Summary: A simple simulation of many balls being held in a vacuum room. The balls move in all directions, bounce off each other or the walls. They keep on bouncing forever because nothing stops them. In vacuum, the friction is negligible and the total kinetic energy of all the balls stays the same, assuming there is no energy loss due to heating.

![Bouncing Balls with Pygame](/images/bouncingballs.png)

I have recently played around with Pygame module and decided to use Pygame to write a simple classic bouncing balls simulation. It was fun. You can have a look at the code [here](https://github.com/khuevu/pygames/tree/master/bouncingball)

The Ball class has methods to detect collisions with walls and other balls; method `update()` to update its position and method `draw()` to redraw. BallWorld contains the main game logics. It keeps track of the list of balls, loops through all balls to update their positions each refresh.  

A few things to note: 

* Each ball object has a `CollisionResponse` object. `CollisionResponse` object contains information on the coming collision: new speed, direction. If the ball is not likely to collide at the moment (not going to collide within a very small EPSILON time), the collision time will be set to infinity.
* Positions of ball objects will be calculated at a fixed time interval (`TimeStep`) to calibrate ball movements per frame refresh. 

Have fun !. 

Ah, well, it is not actually a game per se, but it is fun to watch all the balls bouncing. 


