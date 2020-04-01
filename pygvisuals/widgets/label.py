# -*- coding: cp1252 -*-

from . import textwidget
import pygame


class Label(textwidget.TextWidget):

    """
    Label for displaying text
    """

    def __init__(self, x, y, width, height, text = "", font = textwidget.defaultFont):
        """
        Initialisation of a Label

        parameters:     int x-coordinate of the Label (left)
                        int y-coordinate of the Label (top)
                        int width of the Label
                        int height of the Label
                        string text of the Label
                        pygame.font.Font font of the Label
                return values:  -
                """
        super(Label, self).__init__(x, y, width, height, text, font)

    def _getAppearance(self, *args):
        """
        Blits the text to the Label's Surface and returns the result.

        private function

        parameters:     tuple arguments for the update (first argument should be an instance pygame.event.Event)
        return values:  pygame.Surface the underlying Widget's appearance
        """
        surface = super(Label, self)._getAppearance(*args)
        center  = surface.get_rect().center
        size    = self._font.size(self._text)
        coords  = (center[0] - size[0] / 2, center[1] - size[1] / 2)
        surface.blit(self._font.render(str(self._text), pygame.SRCALPHA, self._foreground), coords)
        return surface
