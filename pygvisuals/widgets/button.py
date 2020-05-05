# --- imports
# pygame imports
import pygame

# local imports
from .label import Label
from ..designs import getDefaultDesign, getFallbackDesign
from ..util import inherit_docstrings_from_superclass

# set defaults
getFallbackDesign().hovered_overlay = (200, 200, 150, 50)
"""Color used by default to overlay when a button is hovered over."""
getFallbackDesign().pressed_overlay = (200, 200, 150, 100)
"""Color used by default to overlay when a button is pressed."""


class Button(Label):

    """
    Clickable buttons with a simple text display.
    """

    def __init__(self, x, y, width, height, text="", font=getDefaultDesign().font, callback=None):
        """
        Initialisation of a Button.

        Args:
            inherit_doc:: arguments
            callback: A callable object to be called when the button is pressed.
                There are no arguments passed and the return value will be ignored.
                If this is a falsy value, no function will be called when the button is pressed;
                The default value is None, meaning that the button will not have any special behaivour when pressed.
        """
        super(Button, self).__init__(x, y, width, height, text, font)
        self._state = 0
        self.callback = callback
        self.hovered_overlay = getDefaultDesign().hovered_overlay
        self.pressed_overlay = getDefaultDesign().pressed_overlay

    def setHoveredOverlay(self, color):
        """
        Set the button's color to overlay when hovered over.

        Args:
            color: A color-like object that can be interpreted as a color by pygame (such as a tuple with RGB values).

        Returns:
            Itsself (the widget) for convenience.
        """
        self._hovered_overlay = color
        self.markDirty()
        return self

    def getHoveredOverlay(self):
        """
        Return the button's color to overlay when hovered over.

        Returns:
            A color-like object that represents the button's color overlay when hovered over.
        """
        return self._hovered_overlay

    def setPressedOverlay(self, color):
        """
        Set the button's color to overlay when pressed.

        Args:
            color: A color-like object that can be interpreted as a color by pygame (such as a tuple with RGB values).

        Returns:
            Itsself (the widget) for convenience.
        """
        self._pressed_overlay = color
        self.markDirty()
        return self

    def getPressedOverlay(self):
        """
        Return the button's color to overlay when pressed.

        Returns:
            A color-like object that represents the button's color overlay when pressed.
        """
        return self._pressed_overlay

    def setCallback(self, callback):
        """
        Set the button's function to be called when it is pressed.

        Args:
            callback: A callable object to be called when the button is pressed.
                If this is a falsy value, no function will be called when the button is pressed.

        Returns:
            Itsself (the widget) for convenience.
        """
        self._callback = callback
        return self

    def getCallback(self):
        """
        Return the button's function to be called when it is pressed.

        Returns:
            A callable object that is called when the button is pressed.
        """
        return self._callback

    def isHovered(self):
        """
        Return whether the button is hovered over.

        Returns:
            A boolean indicating whether the button is hovered over.
        """
        return self._state == 1

    def isPressed(self):
        """
        Return whether the button is pressed.

        Returns:
            A boolean indicating whether the button is pressed.
        """
        return self._state >= 2

    def update(self, *args):
        """
        Additionally handles the clicking of the button and calls the callback-function.

        inherit_doc::
        """
        if self._state:
            if self._state >= 2:
                self._state = 1
            else:
                self._state = 0
            self.markDirty()
        if len(args) > 0 and self.isActive():
            event = args[0]
            pressed = None
            if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
                pressed = event.button == 1
            elif event.type == pygame.MOUSEMOTION:
                pressed = event.buttons[0]

            if pressed is not None and self.rect.collidepoint(event.pos):
                self._state = 1
                if pressed:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.isFocused() and self.callback:
                            try:
                                self.callback()
                            except Exception as e:
                                print(repr(e))
                    elif event.type == pygame.MOUSEBUTTONDOWN or self.isFocused():
                        self._state = 2
                self.markDirty()

        super(Button, self).update(*args)

    def _getAppearance(self, *args):
        """
        Additionally fills the surface with the appropriate overlay.

        inherit_doc::
        """
        surface = super(Button, self)._getAppearance(*args)
        if self.pressed or self.hovered:
            overlay = pygame.Surface(self.bounds.size, pygame.SRCALPHA)
            if self.pressed:
                overlay.fill(self.pressed_overlay)
            else:
                overlay.fill(self.hovered_overlay)
            surface.blit(overlay, (0, 0))
        return surface

    hovered_overlay = property(lambda obj: obj.getHoveredOverlay(), lambda obj, arg: obj.setHoveredOverlay(arg), doc="The widget's color to overlay when it is hovered over.")
    pressed_overlay = property(lambda obj: obj.getPressedOverlay(), lambda obj, arg: obj.setPressedOverlay(arg), doc="The widget's color to overlay when it is pressed.")
    callback = property(lambda obj: obj.getCallback(), lambda obj, arg: obj.setCallback(arg), doc="The widget's function to be called when it is pressed.")
    hovered = property(lambda obj: obj.isHovered(), doc="The widget' status as a boolean regarding whether it is hovered over.")
    pressed = property(lambda obj: obj.isPressed(), doc="The widget' status as a boolean regarding whether it is pressed.")


# inherit docs from superclass
Button = inherit_docstrings_from_superclass(Button)
