# -*- coding: cp1252 -*-

"""
Package for design templates for application with widgets
"""

from os.path import dirname, basename, isfile
import glob
modules = glob.glob(dirname(__file__) + "/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

from ...widgets import *

def applyDesign(design, widgets = None):
    """
    Apply this design to change the default display of widgets and of the supplied widgets

    parameters:     dict the map of configurations made by the design
                    iterable iterable of widgets
    return values:  -
    """
    applyDesignAsDefault(design)
    if widgets:
        applyDesignToWidgets(design, widgets)

def applyDesignAsDefault(design):
    """
    Apply this design to change the default display of widgets

    parameters:     dict the map of configurations made by the design
    return values:  -
    """
    widget.defaultBorder                    = design["border"]
    widget.defaultForeground                = design["foreground"]
    widget.defaultBackground                = design["background"]
    widget.disabeledOverlay                 = design["disabeledOverlay"]
    textwidget.defaultFont                  = design["font"]
    selectiontextwidget.defaultSelection    = design["selection"]
    button.defaultHovered                   = design["hovered"]
    button.defaultPressed                   = design["pressed"]

def applyDesignToWidgets(design, widgets):
    """
    Apply this design to change the supplied widgets

    parameters:     dict the map of configurations made by the design
                    iterable iterable of widgets
    return values:  -
    """
    widget.disabeledOverlay                 = design["disabeledOverlay"]
    if widgets:
        for w in widgets:
            applyDesignToWidget(design, w)

def applyDesignToWidget(design, w):
    """
    Apply this design to change the supplied widget

    parameters:     dict the map of configurations made by the design
                    Widget Widget to apply the design to
    return values:  -
    """
    try:
        w.setBorder(design["border"])
    except: pass
    try:
        w.setForeground(design["foreground"])
    except: pass
    try:
        w.setBackground(design["background"])
    except: pass
    try:
        w.setFont(design["font"])
    except: pass
    try:
        w.setSelectionColor(design["selection"])
    except: pass
    try:
        w.setHoveredColor(design["hovered"])
    except: pass
    try:
        w.setPressedColor(design["pressed"])
    except: pass
    w.markDirty()
    
