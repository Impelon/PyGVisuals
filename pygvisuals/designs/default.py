from . import __init__ as helper
import pygame.font as fnt
from ..border import Border

"""
The default design hardcoded into PyGVisuals-widgets;
Can be used as template for other designs
"""

design = {"border": Border(0, 0),
          "foreground": (255, 255, 255),
          "background": (0, 0, 0),
          "disabeledOverlay": (150, 150, 150, 150),
          "font": fnt.Font(None, 18),
          "selection": (45, 110, 235, 120),
          "hovered": (200, 200, 150, 50),
          "pressed": (200, 200, 150, 100)}

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
