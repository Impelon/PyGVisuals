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
            x: An integer specifing the x-coordinate of the widget.
                This is the horizontal distance from the left reference point.
            y: An integer specifing the y-coordinate of the widget.
                This is the vertical distance from the top reference point.
            width: An integer specifing the width of the widget.
            height: An integer specifing the height of the widget.
            text: A string specifing the content of the widget.
                The default value is an empty string.
            font: A font-like object that can be interpreted by pygame.font as a Font.
                The default value is the global default for fonts.
        """
        super(Label, self).__init__(x, y, width, height, text, font)

    def _getAppearance(self, *args):
        """
        Blits the label's text to the underlying surface and returns the result.

        inherit_docstring::
        """
        surface = super(Label, self)._getAppearance(*args)
        center = surface.get_rect().center
        size = self.font.size(self.text)
        coords = (center[0] - size[0] / 2, center[1] - size[1] / 2)
        surface.blit(self._render(self.text), coords)
        return surface


# inherit docs from superclass
Label = inherit_docstrings_from_superclass(Label)
