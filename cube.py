#!.\venv_9\Scripts\python.exe

# Documentation
#   https://www.glowscript.org/docs/VPythonDocs/index.html

# VPython for Beginners
#   https://www.youtube.com/playlist?list=PLdCdV2GBGyXOnMaPS1BgO7IOU_00ApuMo

# Draw a 4 x 4 x 4 cube

from vpython import *
# from vpython.no_notebook import stop_server
import os
import signal


def shutdown(keyup_event):
    if keyup_event.key == 'x':
        print('You pressed "x"')
        global running
        running = False
        # See https://github.com/BruceSherwood/vpython-jupyter/issues/148
        # stop_server()  # RuntimeError: Event loop is closed
        os.kill(os.getpid(), signal.SIGINT)


def showSphere(evt):
    loc = evt.pos
    sphere(pos=loc, radius=0.1, color=color.green)


def define_boxes_lights():
    list_box = []
    for x in range(4):
        list_box.append([])
        for y in range(4):
            list_box[x].append([])
            for z in range(4):
                list_box[x][y].append(
                    box(
                        pos=vector(x-1.5, y-1.5, z-1.5),
                        size=vector(0.5, 0.5, 0.5),
                        color=color.gray(1),
                        opacity=0.1,
                    )
                )

    return list_box


def get_coordinates_box():
    global x, y, z
    z += 1
    if z > 3:
        z = 0
        y += 1
        if y > 3:
            y = 0
            x += 1
            if x > 3:
                return False
    print(x, y, z)
    return True


def select_box():
    boxes[x][y][z].color = color.cyan
    boxes[x][y][z].opacity = 0.5


# SELECT A BOX By MOUSE CLICK
#   https://www.glowscript.org/docs/VPythonDocs/mouse.html
#   scene.mouse.pick

scene = canvas(title='3D Cube', width=600, height=600)
scene.bind('keyup', shutdown)
scene.bind('click', showSphere)
scene.waitfor("draw_complete")

# For camera angle motion
theta = 0
d_theta = 0.05

# For selecting boxes
d_time = 0.033
time = 0
x = y = 0
z = -1
select = True

boxes = define_boxes_lights()


# print(scene.camera.pos)
# print(scene.camera.axis)

running = True

while running:
    rate(30)
    # scene.camera.pos = vector(2 * cos(theta), 2 * sin(theta), 6)
    # scene.camera.axis = vector(2 * cos(theta), 2 * sin(theta), -10)
    # theta += d_theta

    if select:
        time += d_time
        if time > 1:
            time = 0
            select = get_coordinates_box()
            if select:
                select_box()
