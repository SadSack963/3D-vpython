#!.\venv_9\Scripts\python.exe

"""
    A program to draw a 4 x 4 x 4 cube of boxes
    The mouse can be used to select a box by left clicking on it.

    Documentation
      https://www.glowscript.org/docs/VPythonDocs/index.html

    VPython for Beginners
      https://www.youtube.com/playlist?list=PLdCdV2GBGyXOnMaPS1BgO7IOU_00ApuMo

    Rotate the camera view: drag with the right mouse button (or Ctrl-drag left button).
    Zoom: drag with left and right mouse buttons (or Alt/Option-drag or scroll wheel).
    Pan: Shift-drag.
    Touch screen: swipe or two-finger rotate; pinch/extend to zoom.

    VPython Axis orientation
              | +y
              |
              |
              |
              |          +x
              +------------
             /
            /
        +z /
"""

from vpython import *
# from vpython.no_notebook import stop_server
import os
import signal

# CONSTANTS

# Cube Dimensions
X = 4
Y = 4
Z = 4

# Angle of box rotation (radians) per 1/30 second
phi = 0.02


def shutdown(keyup_event):
    """
    Close the browser window and stop all HTTP server processes when the 'x' key is pressed
    """
    if keyup_event.key == 'x':
        print('You pressed "x"')
        # Stop the game loop
        global running
        running = False
        # Kill all HTTP server processes
        # See https://github.com/BruceSherwood/vpython-jupyter/issues/148
        # stop_server()  # RuntimeError: Event loop is closed
        os.kill(os.getpid(), signal.SIGINT)


def define_boxes(a: int, b: int, c: int):
    """
    Create a 3D array of boxes
    """
    array_boxes = []
    for x in range(a):
        array_boxes.append([])
        for y in range(b):
            array_boxes[x].append([])
            for z in range(c):
                array_boxes[x][y].append(
                    box(
                        pos=vector(x-1.5, y-1.5, z-1.5),
                        size=vector(0.5, 0.5, 0.5),
                        color=color.gray(1),
                        opacity=0.1,
                        spin=False,
                    )
                )
    return array_boxes


def get_object():
    """
    Select the object under the mouse cursor when left-clicked
    https://www.glowscript.org/docs/VPythonDocs/mouse.html
    """
    obj = scene.mouse.pick
    for a in range(X):
        for b in range(Y):
            for c in range(Z):
                if boxes[a][b][c] == obj:
                    select_box(a, b, c)
                    return


def select_box(a: int, b: int, c: int):
    """
    Set the attributes for the selected box
    """
    boxes[a][b][c].color = color.cyan
    boxes[a][b][c].opacity = 0.5
    boxes[a][b][c].spin = True


def spin_box(angle):
    """
    Rotate the selected box if the spin attribute is True

    :param angle: angle to rotate - radians
    :return: nothing
    """
    for a in range(X):
        for b in range(Y):
            for c in range(Z):
                if boxes[a][b][c].spin:
                    boxes[a][b][c].rotate(angle=angle, axis=vec(0, 1, 0))


# Define the canvas
scene = canvas(title='3D Cube', width=600, height=600)

# Keyboard and mouse bindings
scene.bind('keyup', shutdown)
scene.bind('click', get_object)

# Create a cube of boxes
boxes = define_boxes(X, Y, Z)

# Wait for the browser to open and render the page
scene.waitfor("draw_complete")

# Game loop
running = True
while running:
    rate(30)  # Update 30 times per second
    # Spin all selected boxes
    spin_box(phi)
