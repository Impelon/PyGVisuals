from . import __init__ as helper
import pygame.font as fnt
from ..border import ColoredBorder, CompoundBorder

"""
A dark design for PyGVisuals-widgets;
"""

design = {"border": CompoundBorder(ColoredBorder(1, 1, (200, 200, 200)), ColoredBorder(2, 2, (50, 50, 50))),
          "foreground": (200, 200, 200),
          "background": (30, 30, 30),
          "disabeledOverlay": (255, 50, 50, 150),
          "font": fnt.Font(None, 20),
          "selection": (45, 255, 100, 120),
          "hovered": (45, 255, 100, 60),
          "pressed": (45, 255, 100, 120)}

def applyDesign():
    """
    Apply this design to change the default display of widgets

    parameters:     -
    return values:  -
    """
    helper.applyDesign(design)

def applyDesignToWidgets(widgets):
    """
    Apply this design to change the supplied widgets

    parameters:     iterable iterable of widgets
    return values:  -
    """
    helper.applyDesignToWidgets(design, widgets)
