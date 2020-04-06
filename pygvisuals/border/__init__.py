"""
Package for Borders compatible with PyGame's Surfaces;
intended for useage together with PyGVisuals' Widgets.
"""

__all__ = ["Border", "ColoredBorder", "CompoundBorder", "BevelBorder", "RoundedBorder"]


from .border import Border
from .coloredborder import ColoredBorder
from .compoundborder import CompoundBorder
from .bevelborder import BevelBorder
from .roundedborder import RoundedBorder
