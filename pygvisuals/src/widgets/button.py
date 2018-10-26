# -*- coding: cp1252 -*-

from . import textwidget, imagebox
import pygame

defaultHovered    = (200, 200, 150, 50)
defaultPressed    = (200, 200, 150, 100)

class Button(textwidget.TextWidget, imagebox.Imagebox):

    """
    Clickable buttons with alternatively an image added
    """

    def __init__(self, x, y, width, height, text = "", font = textwidget.defaultFont, callback = None):
        """
        Initialisation of a Button

        parameters:     int x-coordinate of the Button (left)
                        int y-coordinate of the Button (top)
                        int width of the Button
                        int height of the Button
                        string text of the Button
                        pygame.font.Font font of the Button
                        function callback function to be called when Button is pressed
                return values:  -
                """
        super(Button, self).__init__(x, y, width, height, text, font)
        self._callback      = callback
        self._state         = 0
        self._hoveredcolor  = defaultHovered
        self._pressedcolor  = defaultPressed

    def setHoveredColor(self, color):
        """
        Set the Buttons's color overlay when hovered over

        parameters:     tuple a tuple of format pygame.Color representing the color to be set
        return values:  Widget Widget returned for convenience
        """
        self._hoveredcolor = color
        self.markDirty()
        return self

    def getHoveredColor(self):
        """
        Return the Buttons's color overlay when hovered over

        parameters:     -
        return values:  tuple of format pygame.Color representing the Buttons's color overlay when hovered over
        """
        return self._hoveredcolor

    def setPressedColor(self, color):
        """
        Set the Buttons's color overlay when pressed

        parameters:     tuple a tuple of format pygame.Color representing the color to be set
        return values:  Widget Widget returned for convenience
        """
        self._pressedcolor = color
        self.markDirty()
        return self

    def getPressedColor(self):
        """
        Return the Buttons's color overlay when pressed

        parameters:     -
        return values:  tuple of format pygame.Color representing the Buttons's color overlay when pressed
        """
        return self._pressedcolor

    def setCallback(self, callback):
        """
        Set the Button's callback-function

        parameters:     function function that executes on click
        return values:  Button Button returned for convenience
        """
        if callable(callback):
            self._callback = callback
        return self

    def getCallback(self):
        """
        Return the Button's callback-function

        parameters:     -
        return values:  function the Buttons's callback-function
        """
        return self._callback

    def isHovered(self):
        """
        Return if the Button is hovered over

        parameters:     -
        return values:  boolean is the Button hovered over
        """
        return self._state == 1

    def isPressed(self):
        """
        Return if the Button is pressed

        parameters:     -
        return values:  boolean is the Button pressed
        """
        return self._state >= 2

    def update(self, *args):
        """
        Handles the clicking of the Button and calls the function given in the constructor.

        parameters: tuple arguments for the update (first argument should be an instance pygame.event.Event)
        return values: -
        """
        if self._state:
            if self._state >= 2:
                self._state = 1
            else:
                self._state = 0
            self.markDirty()
        if len(args) > 0 and self.isActive():
            event = args[0]
            if event.type == pygame.MOUSEBUTTONUP and self.isFocused():
                if self.rect.collidepoint(event.pos):
                    if event.button == 1:
                        try:
                            self._callback()
                        except Exception as e:
                            print(repr(e))
            elif event.type == pygame.MOUSEBUTTONDOWN and self.isFocused():
                if self.rect.collidepoint(event.pos):
                    if event.button == 1:
                        self._state = 2
                    else:
                        self._state = 1
                    self.markDirty()
            elif event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    if event.buttons[0] and self.isFocused():
                        self._state = 2
                    else:
                        self._state = 1
                    self.markDirty()

        super(Button, self).update(*args)

    def _getAppearance(self, *args):
        """
        Blits the text to the Button's Surface and returns the result.

        private function

        parameters:     tuple arguments for the update (first argument should be an instance pygame.event.Event)
        return values:  pygame.Surface the underlying Widget's appearance
        """
        surface = super(Button, self)._getAppearance(*args)
        center  = surface.get_rect().center
        size    = self._font.size(self._text)
        coords  = (center[0] - size[0] / 2, center[1] - size[1] / 2)
        surface.blit(self._font.render(str(self._text), pygame.SRCALPHA, self._foreground), coords)
        if self._state:
            overlay = surface.copy()
            if self._state == 2:
                overlay.fill(self._pressedcolor)
            else:
                overlay.fill(self._hoveredcolor)
            surface.blit(overlay, (0, 0))
        return surface
