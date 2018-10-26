from . import __init__ as helper
import pygame.font as fnt
from ..border import RoundedBorder, CompoundBorder

"""
A futuristic design for PyGVisuals-widgets;
Good for HUDs, etc.
"""

design = {"border": CompoundBorder(RoundedBorder(2, 2, (50, 100, 255, 150), 4), RoundedBorder(4, 4, (50, 50, 50, 50), 4)),
          "foreground": (50, 100, 255, 150),
          "background": (50, 50, 50, 50),
          "disabeledOverlay": (100, 100, 255, 150),
          "font": fnt.Font(None, 18),
          "selection": (100, 100, 255, 100),
          "hovered": (100, 100, 255, 50),
          "pressed": (100, 100, 255, 100)}

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
