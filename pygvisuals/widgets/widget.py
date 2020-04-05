# --- imports
# pygame imports
import pygame
import pygame.sprite

# local imports
from .border import Border

defaultBorder = Border(0, 0)
"""Border to be used by default."""
defaultForeground = (255, 255, 255)
"""Color to be used by default for the foreground of a widget."""
defaultBackground = (0, 0, 0)
"""Color to be used by default for the background of a widget."""
disabeledOverlay = (150, 150, 150, 150)
"""Color to overlay when a widget is disabled."""


class Widget(pygame.sprite.DirtySprite):

    """
    Underlying class for interactive GUI-objects with PyGame;
    intended for use together with pygame.sprite.LayeredDirty.
    """

    def __init__(self, x, y, width, height):
        """
        Initialisation of a basic Widget.
        The unit for the following lengths is pixel.

        Args:
            x: An integer specifing the x-coordinate of the widget.
                This is the horizontal distance from the left reference point.
            y: An integer specifing the y-coordinate of the widget.
                This is the vertical distance from the top reference point.
            width: An integer specifing the width of the widget.
            height: An integer specifing the height of the widget.
        """
        super(Widget, self).__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self._bounds = self.image.get_rect().move(x, y)
        self.rect = self._bounds.copy()
        self._border = defaultBorder
        self._focus = False
        self._active = True
        self._foreground = defaultForeground
        self._background = defaultBackground

    def markDirty(self, overwriteDirtyForever=False):
        """
        Mark the widget as dirty and therefore to be redrawn in the next draw-cycle.

        Args:
            overwriteDirtyForever: A boolean indicating whether this should overwrite the dirty-forever state.
                The default is False meaning that a widget which is marked as dirty-forever
                will not be clean after the next cycle when this method was called on it.
        """
        if not self.isDirtyForever() or overwriteDirtyForever:
            self.dirty = 1

    def markDirtyForever(self):
        """
        Mark the widget as constantly dirty and therefore to be redrawn periodically with every draw-cycle.
        """
        self.dirty = 2

    def markClean(self):
        """
        Mark the widget as clean and therefore not to be redrawn in the next draw-cycle.
        """
        self.dirty = 0

    def isDirty(self):
        """
        Return if the widget is dirty and will be redrawn in the next draw-cycle.
        """
        return self.dirty >= 1

    def isDirtyForever(self):
        """
        Return if the widget is constantly dirty and will be redrawn periodically with every draw-cycle.
        """
        return self.dirty >= 2

    def setVisible(self, visible):
        """
        Set the widget's visibility.
        Invisible widgets will not be drawn and are inactive.

        Args:
            visible: A boolean indicating whether the widget should be visible.

        Returns:
            Itsself (the widget) for convenience.
        """
        visible = bool(visible)
        if self.visible != visible:
            self.visible = visible
            self.setActive(visible)
        return self

    def isVisible(self):
        """
        Return whether the widget is visible.
        Invisible widgets will not be drawn and are inactive.

        Returns:
            A boolean indicating whether the widget is declared visible.
        """
        return self.visible

    def setFocused(self, focused):
        """
        Set whether the widget is focused.

        A widget will be focused automatically if it is clicked on.
        Although the default implementation does not process this information,
        subclasses may use this information to determine if the user-interaction
        was meant to be processed by them or not.

        Args:
            visible: A boolean indicating whether the widget should be focused.

        Returns:
            Itsself (the widget) for convenience.
        """
        focused = bool(focused)
        if self._focus != focused:
            self._focus = focused
            self.markDirty()
        return self

    def isFocused(self):
        """
        Return whether the widget is focused.
        A widget will be focused automatically if it is clicked on.

        Returns:
            A boolean indicating whether the widget is declared focused.
        """
        return self._focus

    def setActive(self, active):
        """
        Set the widget as active and therefore as interactive.
        An inactive widget should not be interactable and will have an overlay painted on.

        Args:
            active: A boolean indicating whether the widget should be active

        Returns:
            Itsself (the widget) for convenience.
        """
        active = bool(active)
        if self._active != active:
            self._active = active
            self.markDirty()
        return self

    def isActive(self):
        """
        Return whether the widget is active.
        An inactive widget should not be interactable and will have an overlay painted on.

        Returns:
            A boolean indicating whether the widget is active.
        """
        return self._active

    def setBounds(self, rect):
        """
        Set the widget's bounds according to a pygame.Rect.
        This can be used to change the position of the widget or its size.

        Args:
            rect: A pygame.Rect with the according position and size.

        Returns:
            Itsself (the widget) for convenience.
        """
        self._bounds = rect
        self.markDirty()
        return self

    def getBounds(self):
        """
        Return the widget's bounds (position and size).

        Returns:
            A pygame.Rect with the bounds of the widget.
        """
        return self._bounds

    def setBorder(self, border):
        """
        Set the widget's border.

        Args:
            border: A PyGVisuals-Border to be set.

        Returns:
            Itsself (the widget) for convenience.
        """
        if isinstance(border, Border):
            self._border = border
            self.markDirty()
        return self

    def getBorder(self):
        """
        Return the widget's border.

        Returns:
            A PyGVisuals-Border belonging to the widget.
        """
        return self._border

    def setForeground(self, color):
        """
        Set the widget's foreground-color (not used by basic implementation).

        Args:
            color: A color-like object that can be interpreted as a color by pygame (such as a tuple with RGB values).

        Returns:
            Itsself (the widget) for convenience.
        """
        self._foreground = color
        self.markDirty()
        return self

    def setBackground(self, color):
        """
        Set the widget's background-color.

        Args:
            color: A color-like object that can be interpreted as a color by pygame (such as a tuple with RGB values).

        Returns:
            Itsself (the widget) for convenience.
        """
        self._background = color
        self.markDirty()
        return self

    def getForeground(self):
        """
        Return the widget's foreground-color (not used by basic implementation).

        Returns:
            A color-like object that represents the widget's foreground color.
        """
        return self._foreground

    def getBackground(self):
        """
        Return the widget's background-color.

        Returns:
            A color-like object that represents the widget's background color.
        """
        return self._background

    def update(self, *args):
        """
        Perform any updates on the widget if needed.

        This is a basic implementation of focus, active-state and border-rendering;
        used for interaction in more advanced widget-classes.

        Args:
            *args: Any argument needed for the update. This can include an optional pygame.event.Event to process.
        """
        if self.isActive() and len(args) > 0:
            event = args[0]
            if event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 2, 3):
                self.setFocused(self.rect.collidepoint(event.pos))
        if self.isDirty():
            self.rect = self._border.getBounds(self._bounds)
            self.image = self._getAppearance(*args)
            if not self.isActive():
                inactive = self.image.copy()
                inactive.fill(disabeledOverlay)
                self.image.blit(inactive, (0, 0))
            self.image = self._border.getBorderedImage(self.image)

    def _getAppearance(self, *args):
        """
        Return the underlying widget's appearance.

        This includes a basic implementation of background-coloring.

        This is an internal function.

        Args:
            *args: Any argument needed for the update. This can include an optional pygame.event.Event to process.

        Returns:
            The underlying widget's appearance as a pygame.Surface.
        """
        surface = pygame.Surface(self._bounds.size, pygame.SRCALPHA)
        surface.fill(self._background)
        return surface
