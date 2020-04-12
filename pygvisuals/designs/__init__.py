"""
Package for design templates for application with widgets
"""

__all__ = ["setDefaultDesign", "getDefaultDesign", "getFallbackDesign"]

from .design import Design

__fallback_design = Design()
__default_design = Design(fallback=__fallback_design)

def setDefaultDesign(design):
    """
    Set the default-design to a copy of the given design.
    The fallback will be replaced by an internal fallback.

    Args:
        design: A PyGVisuals-design to set as default.
    """
    global __default_design
    design = design.copy()
    design.fallback = __fallback_design
    __default_design = design

def getDefaultDesign():
    """
    Return the default-design to be used for defaults for all widgets.

    Returns:
        A PyGVisuals-design that is being used as default.
    """
    return __default_design

def getFallbackDesign():
    """
    Return the fallback-design to be used as fallback for all default-designs.

    Returns:
        A PyGVisuals-design that is being used as fallback.
    """
    return __fallback_design
