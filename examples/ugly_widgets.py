"""
Simple and ugly testscript that shows most of PyGVisuals' widgets.
"""

# --- imports
# preinstalled python libraries
import random
import os
import sys

# pygame imports
import pygame
from pygame.locals import *

# local imports
import pygvisuals.widgets as gui
import pygvisuals.borders as brd
from pygvisuals.io import StreamRedirector

pygame.init()

# setting display

screen = pygame.display.set_mode((700, 400), 0 | DOUBLEBUF | RESIZABLE, 32)
pygame.mouse.set_visible(1)
pygame.key.set_repeat(1, 50)

background = pygame.Surface((700, 350))
background.fill((255, 255, 255))

image = pygame.Surface((250, 200))
pygame.draw.ellipse(image, (255, 0, 255), pygame.Rect(0, 0, 250, 200))

i = None
b = None


def main_loop():
    """
    Draw and update the window content, handle input events
    """
    global i, b
    # You can create various widgets; do not worry about the complicated values,
    # they are just there to show off the different functionalities available.

    # This is a generic Widget with no additional functions.
    w = gui.Widget(50, 50, 50, 50).setBackground((255, 0, 0, 100)).setBorder(brd.RoundedBorder((10, 80), (5, 10), (0, 0, 0), 8))
    # This is a Border consistent of 3 different borders; any widget can have borders.
    r = brd.CompoundBorder(brd.CompoundBorder(brd.BevelBorder(2, 2, (30, 90, 150), (30, 190, 50)),
                                              brd.ColoredBorder(3, 3, (130, 190, 250, 200))), brd.ColoredBorder(2, 2, (30, 90, 150, 100)))
    # This is an Entry; it accepts input from the user. Different things can be done with this; here we validate input to only accept numbers.
    e = gui.Entry(10, 10, 100, 25).setBackground((0, 120, 255)).setBorder(r).setValidation(isNumber)
    # This is a Button; it reacts to the user clicking on it and executes a callback-function if clicked.
    b = gui.Button(100, 100, 100, 50, "click", callback=button1).setBackground((255, 255, 0)).setForeground((0, 0, 0))
    # This is a Label; it simply displays some text.
    l = gui.Label(250, 50, 75, 50, "text").setBackground((0, 255, 0)).setForeground((0, 0, 0))
    # This is a Listbox; It displays a given list as strings on new lines/entries; in this example the list contains some widgets, but it can contain practically anything.
    x = gui.Listbox(50, 150, 250, 100).setBackground((255, 155, 0)).setBorder(brd.RoundedBorder(4, 4, (0, 0, 0), 15)).setList([w, e, b, l])
    # Any widget can display a pygame-Surface as a background-image. This could be an actual Image, but here it's just a Surface.
    i = gui.Entry(350, 150, 150, 100).setBackgroundImage(image).setBackground((255, 155, 0)).setBorder(brd.RoundedBorder(4, 4, (0, 100, 0), 15))

    # Here we create and assign a StreamRedirector which takes a stream and computes a callback function on each line.
    # In this case we use it to copy output from the console to the Listbox created above.
    sys.stdout = StreamRedirector(sys.stdout, (lambda s: x.insert(1, s)))

    # Here we create a sprite-group to gather all of our widgets.
    group = pygame.sprite.LayeredDirty([w, e, b, l, x, i])

    # generic pygame-Loop which draws and updates our sprite-group
    try:
        going = True
        while going:
            # handle input events
            for event in pygame.event.get():
                if event.type == QUIT:
                    going = False
                group.update(event)
            group.draw(screen, background)
            pygame.display.update()
            pygame.time.wait(100)
    except Exception:
        # in case something does not work out...
        import traceback
        print("Something has gone wrong...")
        print(traceback.format_exc())
        print(screen, background, group)
    finally:
        pygame.quit()
        sys.exit()


def button1():
    """
    Callback function for the button.
    This will toggle the Imagebox' visibility.
    """
    print("Button b clicked!")
    # some side-effects for fun
    global i
    if i != None:
        i.setVisible(not i.isVisible())


def isNumber(newtext, oldtext, widget):
    """
    Validation function for an Entry; limits inputs to numbers.
    (Also has the side-effect of toggeling the button's active state.)

    Args:
        newtext: A String with the new content for the component.
        oldtext: A String with the old content of the component.
        widget: The Entry affected by this change/validation.

    Returns:
        A boolean indicating whether the change should be made / is valid.
    """
    # some side-effects for fun
    global b
    if b != None:
        b.setActive(not b.isActive())
    return not newtext or newtext.isdigit()


if __name__ == "__main__":
    main_loop()
main_loop()
