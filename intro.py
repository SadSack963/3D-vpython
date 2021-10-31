# A VPython tutorial
#   https://www.glowscript.org/docs/VPythonDocs/VPython_Intro.pdf

"""
    3D Objects
        See vpython.py class standardAttributes() for accepted arguments.

    Convenient Defaults
        Objects can be specified with convenient defaults:
        arrow() is equivalent to arrow(pos=vector(0,0,0), axis=vector(1,0,0), radius=1)
        box() is equivalent to box(pos=vector(0,0,0), size=vector(1,1,1))
        cone() is equivalent to cone(pos=vector(0,0,0), axis=vector(1,0,0), radius=1)
        curve() establishes an "empty" curve to which points can be appended
        cylinder() is equivalent to cylinder(pos=vector(0,0,0), axis=vector(1,0,0), radius=1)
        ellipsoid() is equivalent to ellipsoid(pos=vector(0,0,0), size=vector(1,1,1))
        frame() establishes a frame with pos=vector(0,0,0) and axis=vector(1,0,0)
        helix() is equivalent to helix(pos=vector(0,0,0), axis=vector(1,0,0), radius=1, thickness=0.05, coils=5)
        pyramid() is equivalent to pyramid(pos=vector(0,0,0), size=vector(1,1,1), axis=vector(1,0,0))
        ring() is equivalent to ring(pos=vector(0,0,0), axis=vector(1,0,0), radius=1)
        sphere() is equivalent to sphere(pos=vector(0,0,0), radius=1 )


    https://www.glowscript.org/docs/VPythonDocs/canvas.html
    A canvas called "scene" is created automatically.
    Default lights:
        scene.lights = [
            distant_light(direction=vec( 0.22,  0.44,  0.88), color=color.gray(0.8)),
            distant_light(direction=vec(-0.88, -0.22, -0.44), color=color.gray(0.3))
        ]
    To change light colours:
        scene.lights[n].color = color.red
    Similarly, scene.objects is a list of all (visible) objects
"""

from vpython import *
from time import sleep


scene = canvas(title='Ball in a Box.', width=800, height=600, resizable=True)

wall_left = box(pos=vector(-6, 0, 0), size=vector(0.2, 12, 12), color=color.green, opacity=0.3)
wall_right = box(pos=vector(6, 0, 0), size=vector(0.2, 12, 12), color=color.green, opacity=0.3)
wall_bottom = box(pos=vector(0, -6, 0), size=vector(12, 0.2, 12), color=color.blue, opacity=0.3)
wall_top = box(pos=vector(0, 6, 0), size=vector(12, 0.2, 12), color=color.blue, opacity=0.3)
wall_back = box(pos=vector(0, 0, -6), size=vector(12, 12, 0.2), color=color.red, opacity=0.3)
wall_front = box(pos=vector(0, 0, 6), size=vector(12, 12, 0.2), color=color.red, opacity=0)


ball = sphere(pos=vector(-5, 0, 0), radius=0.5, color=color.cyan, make_trail=True, retain=100)

ball.velocity = vector(25, 5, 15)
delta_time = 0.005
t = 0

# Vector arrow
v_scale = 0.1
v_arrow = arrow(pos=ball.pos, axis=v_scale * ball.velocity, color=color.yellow)

scene.autoscale = False

# sleep(1)  # Allow time for the web page to render
scene.waitfor("draw_complete")  # Wait for the end of the next update of the canvas by the web browser

while t < 10:
    # An animation loop must contain a rate statement (or sleep or waitfor statement).
    # Otherwise the browser page will lock up with no possibility of updating the page.
    rate(100)  # FPS - VPython checks to see whether 1/100 second has elapsed since the previous iteration

    # Move the ball
    ball.pos = ball.pos + ball.velocity * delta_time
    t = t + delta_time
    # Draw a vector arrow
    v_arrow.pos = ball.pos
    v_arrow.axis = v_scale * ball.velocity

    # Detect collision with left and right walls
    if ball.pos.x > wall_right.pos.x:
        ball.velocity.x = -ball.velocity.x
    if ball.pos.x < wall_left.pos.x:
        ball.velocity.x = -ball.velocity.x
    # Detect collision with top and bottom walls
    if ball.pos.y > wall_top.pos.y:
        ball.velocity.y = -ball.velocity.y
    if ball.pos.y < wall_bottom.pos.y:
        ball.velocity.y = -ball.velocity.y
    # Detect collision with front and back walls
    if ball.pos.z > wall_front.pos.z:
        ball.velocity.z = -ball.velocity.z
    if ball.pos.z < wall_back.pos.z:
        ball.velocity.z = -ball.velocity.z
