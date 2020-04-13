"""
A script which shows off PyGVisuals' design-system.
"""

# --- imports
# preinstalled python libraries
import sys

# pygame imports
import pygame
from pygame.locals import *

# local imports
import pygvisuals.widgets as gui
import pygvisuals.borders as brd
from pygvisuals.designs import getDesignRegister, getRegisteredDesign, Design

pygame.init()

# setting display

screen = pygame.display.set_mode((700, 400), DOUBLEBUF, 32)
pygame.mouse.set_visible(1)

background = pygame.Surface(screen.get_rect().size)
background.fill((255, 255, 255))

group = []

# Here we create a function which inverts the background's color.


def invert_background(*args):
    copy = background.copy()
    background.fill((255, 255, 255))
    background.blit(copy, (0, 0), special_flags=BLEND_RGB_SUB)
    screen.blit(background, (0, 0))
    for widget in group:
        screen.blit(widget.image, widget.rect.topleft)


def main_loop():
    """
    Draw and update the window content, handle input events
    """
    global group

    # Here we first create some widgets to show of the designs with.

    # This is a Label; it simply displays some text.
    l = gui.Label(20, 20, 200, 50, "widgets for demonstration")
    # This is an Entry; it accepts input from the user.
    e = gui.Entry(20, 90, 100, 20)
    # Here we create a local function that toggles the active-status of the entry.

    def toggle(*args):
        e.active = not e.active
    # These are Buttons; they react to the user clicking on it and execute a callback-function if clicked.
    b = gui.Button(20, 130, 300, 50, "toggle active-status of entry above", callback=toggle)
    f = gui.Button(20, 200, 300, 50, "invert background color", callback=invert_background)
    # This is a Listbox; It displays a given list as strings on new lines/entries; in this example the list contains some widgets, but it can contain practically anything.
    x = gui.Listbox(20, 270, 250, 100, editable=True)
    x.setList(["test"] + list(range(1, 13, 3)))

    demo = [l, e, b, f, x]

    # Now we create the widgets necessary to change the design.

    a = gui.Label(480, 20, 200, 50, "select a design below")
    # This Listbox will contain all registered designs.
    d = gui.Listbox(480, 90, 200, 200)
    d.setList(list(getDesignRegister().keys()))
    # We now create a function to change the design according to the selected design in the Listbox.

    def change_design(*args):
        index = d.getSelection()[0]
        if index >= 0 and index <= len(d.getList()):
            design = getRegisteredDesign(d.getList()[index])
            if design:
                design.applyToWidgets(demo)
    c = gui.Button(480, 310, 200, 50, "apply selected design", callback=change_design)

    selector_ui = [a, d, c]

    # We will also create a custom design here, to make the UI look nicer.
    selector_ui_design = Design(border=brd.BevelBorder(4, 4, (215, 175, 245), (175, 125, 215)),
                                foreground=(255, 245, 255),
                                background=(175, 155, 185))

    selector_ui_design.applyToWidgets(selector_ui)

    # Here we create a sprite-group to gather all of our widgets.
    group = pygame.sprite.LayeredDirty(demo + selector_ui)

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
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main_loop()
main_loop()
