"""
Package for Borders compatible with pygame's Surfaces;
intended for useage together with PyGVisuals' widgets.
"""

__all__ = ["Border", "ColoredBorder", "CompoundBorder", "BevelBorder", "RoundedBorder"]


from .border import Border
from .colored_border import ColoredBorder
from .compound_border import CompoundBorder
from .bevel_border import BevelBorder
from .rounded_border import RoundedBorder
