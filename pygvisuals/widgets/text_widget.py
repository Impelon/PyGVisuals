# --- imports
# pygame imports
import pygame
import pygame.font as fnt

# local imports
from .widget import Widget
from ..designs import getDefaultDesign, getFallbackDesign

fnt.init()

# set defaults
getFallbackDesign().font = fnt.Font(None, 18)
"""Font to be used by default by widgets displaying text."""


class TextWidget(Widget):

    """
    Underlying class for widgets using text/strings.
    """

    def __init__(self, x, y, width, height, text="", font=getDefaultDesign().font):
        """
        Initialisation of a TextWidget.

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
        super(TextWidget, self).__init__(x, y, width, height)
        self._antialiased = True
        self.font = font
        self.text = text

    def setText(self, text):
        """
        Set the widget's string-representation of its content.

        Args:
            text: A string with the content to set.

        Returns:
            Itsself (the widget) for convenience.
        """
        self._text = str(text)
        self.markDirty()
        return self

    def getText(self):
        """
        Return the widget's string-representation of its content.

        Returns:
            A string representing the content of the widget.
        """
        return self._text

    def setFont(self, font):
        """
        Set the widget's font used when rendering text.

        Args:
            font: A font-like object that can be interpreted by pygame.font as a Font.

        Returns:
            Itsself (the widget) for convenience.
        """
        self._font = font
        self.markDirty()
        return self

    def getFont(self):
        """
        Return the widget's font used when rendering text.

        Returns:
            A font-like object that can be interpreted by pygame.font as a Font.
        """
        return self._font

    def setAntialiasing(self, antialiased):
        """
        Set whether the widget's text will be antialiased when rendered or not.

        Args:
            antialiased: A boolean indicating whether the text should be rendered with antialiasing.

        Returns:
            Itsself (the widget) for convenience.
        """
        antialiased = antialiased
        antialiased = bool(antialiased)
        if self.antialiased != antialiased:
            self._antialiased = antialiased
            self.markDirty()
            self.update()
        return self

    def isAntialiasing(self):
        """
        Return whether the widget's text will be antialiased when rendered or not.

        Returns:
            A boolean indicating whether the text is rendered with antialiasing.
        """
        return self._antialiased

    def _render(self, text, color=None, background=None):
        """
        Create a new surface with the text drawn on it.

        This is a wrapper-function for pygame.Font.render with appropiate
        values according to this widget's properties.
        The font and antialias will be the widget's font and antialiased properties.

        Args:
            text: A string with the text to be rendered.
            color: A color to draw to text with.
                If this is a falsy value (e.g. None), the widget's foreground-color will be used.
                The default value is None, meaning that the foreground will be used.
            background: A color to be used as background behind the text (same as with pygame.Font.render).
                If this is a falsy value (e.g. None), the background will be transparent.
                The default value is None, meaning that no color is used for the background.

        Returns:
            A pygame.Surface with the text drawn on it.
        """
        if not color:
            color = self.foreground
        return self.font.render(text, self.antialiased, color, background)

    text = property(getText, setText, doc="""The widget's string-representation of its content.""")
    font = property(getFont, setFont, doc="""The widget's font used when rendering text.""")
    antialiased = property(isAntialiasing, setAntialiasing, doc="The widget's status as a boolean "
                           "regarding whether antialiasing is used when rendering text.")
