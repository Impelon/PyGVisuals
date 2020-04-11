"""
Package for design templates for application with widgets
"""

__all__ = ["default_design"]

from .design import Design

__fallback_design = Design()
__default_design = Design(fallback=__fallback_design)

# implement as property
default_design = __default_design
