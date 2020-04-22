# --- imports
# local imports
from .border import Border
from ..util import inherit_docstrings_from_superclass


class CompoundBorder(Border):

    """
    Border composed of two other borders.
    """

    def __init__(self, inner, outer):
        """
        Initialisation of a CompoundBorder.

        Args:
            inner: A border which will be used as the inner part of the CompoundBorder.
            outer: A border which will be used as the outer part of the CompoundBorder.
        """
        super(CompoundBorder, self).__init__((inner.left + outer.left, inner.right + outer.right),
                                             (inner.top + outer.top, inner.bottom + outer.bottom))
        self.inner = inner
        self.outer = outer

    def getBorderedImage(self, surface, *args):
        try:
            if not self.isEmptyBorder():
                return self.outer.getBorderedImage(self.inner.getBorderedImage(surface, *args), *args)
        except:
            pass
        return surface


# inherit docs from superclass
CompoundBorder = inherit_docstrings_from_superclass(CompoundBorder)
