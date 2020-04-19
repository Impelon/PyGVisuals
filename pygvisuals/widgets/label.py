# --- imports
# local imports
from .text_widget import TextWidget
from ..designs import getDefaultDesign
from ..util import inherit_docstrings_from_superclass


class Label(TextWidget):

    """
    A label for displaying simple text.
    """

    def __init__(self, x, y, width, height, text="", font=getDefaultDesign().font):
        """
        Initialisation of a Label.

        Args:
            inherit_doc:: arguments
        """
        super(Label, self).__init__(x, y, width, height, text, font)

    def _getAppearance(self, *args):
        """
        Additionally blits the label's text to the underlying surface and returns the result.

        inherit_doc::
        """
        surface = super(Label, self)._getAppearance(*args)
        center = surface.get_rect().center
        size = self.font.size(self.text)
        coords = (center[0] - size[0] / 2, center[1] - size[1] / 2)
        surface.blit(self._render(self.text), coords)
        return surface


# inherit docs from superclass
Label = inherit_docstrings_from_superclass(Label)
