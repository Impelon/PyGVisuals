from . import __init__ as helper
import pygame.font as fnt
from ..border import RoundedBorder, CompoundBorder

"""
A cold design for PyGVisuals-widgets;
"""

design = {"border": CompoundBorder(RoundedBorder(3, 3, (150, 190, 255, 200), 8), RoundedBorder(2, 2, (30, 90, 150), 8)),
          "foreground": (255, 255, 255),
          "background": (120, 160, 200),
          "disabeledOverlay": (150, 150, 250, 150),
          "font": fnt.Font(None, 18),
          "selection": (45, 110, 235, 120),
          "hovered": (150, 200, 250, 50),
          "pressed": (150, 200, 250, 100)}

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
