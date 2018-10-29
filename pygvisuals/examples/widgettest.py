# -*- coding: cp1252 -*-

"""
Simple and ugly testscript that shows most of PyGVisuals' widgets
"""

#Modules#

import random
import os, sys
import pygame
import pygvisuals.src.widgets as gui
import pygvisuals.src.widgets.border as brd
from pygvisuals.src.io import StreamRedirector
from pygame.locals import *

pygame.init()

#Setting Display#

screen = pygame.display.set_mode((700,400),0|DOUBLEBUF|RESIZABLE,32)
pygame.mouse.set_visible(1)
pygame.key.set_repeat(1, 50)

background = pygame.Surface((700,350))
background.fill((255,255,255))

image = pygame.Surface((250, 200))
pygame.draw.ellipse(image, (255, 0, 255), pygame.Rect(0, 0, 250, 200))

i = None
b = None

def main_loop():
    """
    Draw and update the window content, handle input events

    parameters:     -
    return values:  -
    """
    global i, b
    w = gui.Widget(50, 50, 50, 50).setBackground((255, 0, 0)).setBorder(gui.border.RoundedBorder((10, 80), (5, 10), (0, 0, 0), 8))
    r = brd.CompoundBorder(brd.CompoundBorder(brd.BevelBorder(2, 2, (30, 90, 150), (30, 190, 50)), brd.ColoredBorder(3, 3, (130, 190, 250, 200))), brd.ColoredBorder(2, 2, (30, 90, 150, 100)))
    e = gui.Entry(10, 10, 100, 25).setBackground((0, 120, 255)).setBorder(r).setValidation(isNumber)
    b = gui.Button(100, 100, 100, 50, "click", callback = button1).setBackground((255, 255, 0)).setForeground((0, 0, 0))
    l = gui.Label(250, 50, 75, 50, "text").setBackground((0, 255, 0)).setForeground((0, 0, 0))
    x = gui.Listbox(50, 150, 250, 100).setBackground((255, 155, 0)).setBorder(brd.RoundedBorder(4, 4, (0, 0, 0), 15)).setList([w, e, b, l])
    i = gui.Imagebox(350, 150, 150, 100, image).setBackground((255, 155, 0)).setBorder(brd.RoundedBorder(4, 4, (0, 0, 0), 15))

    sys.stdout = StreamRedirector(sys.stdout, (lambda s: x.insert(1, s)))

    group = pygame.sprite.LayeredDirty([w, e, b, l, x, i])
    
    going = True
    while going:
        #Handle Input Events#
        mouse_down = False
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            group.update(event)
        group.draw(screen, background)
        pygame.display.update()
        pygame.time.wait(100)
    pygame.quit()
    sys.exit()

def button1():
    print("Button b clicked!")
    global i
    if i != None:
        i.setVisible(not i.isVisible())

def isNumber(newtext, oldtext, widget):
    """
    Validation function for an Entry; limits inputs to numbers

    parameters:     str the text to be set
                    str the current text
                    gui.Entry the entry affected
    return values:  boolean is the operation valid
    """
    global b
    if b != None:
        b.setActive(not b.isActive())
    return not newtext or newtext.isdigit()

#Automatic Start#

if __name__ == "__main__":
    main_loop()
main_loop()
