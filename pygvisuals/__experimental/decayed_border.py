# --- imports
# local imports
from .border import Border
from ..util import inherit_docstrings_from_superclass


class DecayedBorder(Border):

    """
    Border ...
    """

    def __init__(self, border):
        """
        Initialisation of a DecayedBorder.

        Args:
            border: ...
        """
        super(DecayedBorder, self).__init__((border.left, border.right), (border.top, border.bottom))
        self.border = border

    def getBorderedImage(self, surface):
        try:
            if not self.isEmptyBorder():
                return self.border.getBorderedImage(surface)
        except:
            pass
        return surface


# inherit docs from superclass
CompoundBorder = inherit_docstrings_from_superclass(CompoundBorder)
