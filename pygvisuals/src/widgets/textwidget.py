# -*- coding: cp1252 -*-

import widget
import pygame
import pygame.font as fnt

fnt.init()
defaultFont = fnt.Font(None, 18)

class TextWidget(widget.Widget):

    """
    Underlying class for Widgets using text/strings;
    """
    
    def __init__(self, x, y, width, height, text = "", font = defaultFont):
        """
        Initialisation of a TextWidget

        parameters:     int x-coordinate of the TextWidget (left)
                        int y-coordinate of the TextWidget (top)
                        int width of the TextWidget
                        int height of the TextWidget
                        string test of the TextWidget
                        pygame.font.Font font of the TextWidget
        return values:  -
        """
        super(TextWidget, self).__init__(x, y, width, height)
        self._text = text
        self._font = font
        
    def setText(self, text):
        """
        Set the TextWidget's text

        parameters:     string the text to be set
        return values:  TextWidget TextWidget returned for convenience
        """
        self._text = str(text)
        self.markDirty()
        return self

    def getText(self):
        """
        Return the TextWidget's text

        parameters:     -
        return values:  string the TextWidget's text
        """
        return self._text

    def setFont(self, font):
        """
        Set the TextWidget's text

        parameters:     pygame.font.Font the Font to be set
        return values:  TextWidget TextWidget returned for convenience
        """
        if isinstance(font, fnt.Font):
            self._font = font
            self.markDirty()
        return self

    def getFont(self):
        """
        Return the TextWidget's font

        parameters:     -
        return values:  pygame.font.Font the TextWidget's font
        """
        return self._font
