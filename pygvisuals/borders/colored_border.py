# --- imports
# local imports
from .border import Border
from ..util import inherit_docstrings_from_superclass


class ColoredBorder(Border):

    """
    Border with a color.
    """

    def __init__(self, width, height, color):
        """
        Initialisation of a ColoredBorder.

        Args:
            inherit_doc:: arguments
            color: A color-like object that can be interpreted as a color by pygame (such as a tuple with RGB values).
                This will be used as the color for the border.
        """
        super(ColoredBorder, self).__init__(width, height)
        self.color = color

    def _drawBorder(self, surface, original_rect, bordered_rect, *args):
        surface.fill(self.color)
        return surface


# inherit docs from superclass
ColoredBorder = inherit_docstrings_from_superclass(ColoredBorder)
