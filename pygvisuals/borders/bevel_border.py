# --- imports
# local imports
from .border import Border
from ..util import inherit_docstrings_from_superclass


class BevelBorder(Border):

    """
    Border with two colored lines, creating a simple bevel-effect.
    """

    def __init__(self, width, height, upper, lower, lower_has_left_side=False):
        """
        Initialisation of a BevelBorder.

        Args:
            inherit_doc:: arguments
            upper: A color-like object that can be interpreted as a color by pygame (such as a tuple with RGB values).
                This will be used as the color for the upper side of the border.
            lower: A color-like object that can be interpreted as a color by pygame (such as a tuple with RGB values).
                This will be used as the color for the lower side of the border.
            lower_has_left_side: A boolean indicating whether the left side
                will be filled in with the same color as the lower/bottom side.
                The default is False, which means that the left side will have the same color as the top side.
        """
        super(BevelBorder, self).__init__(width, height)
        self.upper = upper
        self.lower = lower
        self.lower_has_left_side = lower_has_left_side

    def _drawBorder(self, surface, original_rect, bordered_rect, *args):
        surface.fill(self.upper)
        lower_rect = bordered_rect.move(self.right + self.left, self.right + self.top)
        if self.lower_has_left_side:
            lower_rect.width -= self.right
            lower_rect.left -= self.right
        surface.fill(self.lower, lower_rect)
        return surface


# inherit docs from superclass
BevelBorder = inherit_docstrings_from_superclass(BevelBorder)
