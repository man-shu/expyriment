#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A line bisection task.

This example is also appropriate to illustrates the use of the Android runtime environment for Exypriment on tablet PC.

"""

from expyriment import control, stimuli, io, design, misc

design.defaults.experiment_background_colour = misc.constants.C_GREY
design.defaults.experiment_foreground_colour = misc.constants.C_BLACK
line_length = 200

def line_bisection(line_length, position):
    button = stimuli.Rectangle(size=(40,20),
                position=(exp.screen.size[0]/2-25, 15-exp.screen.size[1]/2))
    button_text = stimuli.TextLine(text="ok", position=button.position,
                                text_colour=misc.constants.C_WHITE)
    mark_position = None
    while True:
        canvas = stimuli.BlankScreen()
        line = stimuli.Rectangle(size=(line_length,3), position=position,
                    colour=misc.constants.C_BLACK)
        line.plot(canvas)
        if mark_position is not None:
            button.plot(canvas)
            button_text.plot(canvas)
            markline = stimuli.Rectangle(size=(1,25),
                        position=(mark_position, line.position[1]),
                        colour=misc.constants.C_RED)
            markline.plot(canvas)

        canvas.present()

        _id, pos, _rt = exp.mouse.wait_press()
        if abs(pos[1]-line.position[1])<=50 and\
                    abs(pos[0]-line.position[0])<=line_length/2:
            mark_position = pos[0]
        else:
            if button.overlapping_with_position(pos):
                return mark_position - line.position[0]

exp = control.initialize()

# make touch button box
buttonA = stimuli.Rectangle(size=(80, 40), position=(-60, 0))
buttonB = stimuli.Rectangle(size=(80, 40), position=(60, 0))
textA = stimuli.TextLine(text="quit", position=buttonA.position,
            text_colour=misc.constants.C_WHITE)
textB = stimuli.TextLine(text="next", position=buttonB.position,
            text_colour=misc.constants.C_WHITE)
touchButtonBox = io.TouchScreenButtonBox(button_fields=[buttonA, buttonB],
                stimuli=[textA, textB])

control.start(exp)

exp.mouse.show_cursor()
while True:
    rx, ry = ((exp.screen.size[0]-line_length)/2, (exp.screen.size[1]-50)/2)
    pos = [design.randomize.rand_int(-rx, rx), design.randomize.rand_int(-ry, ry)]
    judgment = line_bisection(line_length, position=pos)
    exp.data.add(pos +[judgment])
    touchButtonBox.show()
    btn, _rt = touchButtonBox.wait()
    if btn==buttonA:
        break

control.end()
