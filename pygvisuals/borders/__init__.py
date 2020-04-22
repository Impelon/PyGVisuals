"""
Package for borders compatible with pygame's surfaces;
intended to be used together with PyGVisuals' widgets.
"""

__all__ = ["BevelBorder", "Border", "ColoredBorder", "CompoundBorder", "RoundedBorder"]


from .bevel_border import BevelBorder
from .border import Border
from .colored_border import ColoredBorder
from .compound_border import CompoundBorder
from .rounded_border import RoundedBorder
