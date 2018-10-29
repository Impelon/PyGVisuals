# -*- coding: cp1252 -*-

import pygame.sprite
import pygame
from .border import Border

defaultBorder       = Border(0, 0)
defaultForeground   = (255, 255, 255)
defaultBackground   = (0, 0, 0)
disabeledOverlay    = (150, 150, 150, 150)

class Widget(pygame.sprite.DirtySprite):

    """
    Underlying class for interactive GUI-objects with PyGame;
    extends pygame.sprite.DirtySprite
    intended for use together with pygame.sprite.LayeredDirty
    """
    
    def __init__(self, x, y, width, height):
        """
        Initialisation of a Widget

        parameters:     int x-coordinate of the Widget (left)
                        int y-coordinate of the Widget (top)
                        int width of the Widget
                        int height of the Widget
        return values:  -
        """
        super(Widget, self).__init__()
        self.image          = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self._bounds        = self.image.get_rect().move(x, y)
        self.rect           = self._bounds.copy()
        self._border        = defaultBorder
        self._focus         = False
        self._active        = True
        self._foreground    = defaultForeground
        self._background    = defaultBackground

    def markDirty(self):
        """
        Mark the Widget as dirty and therefore to be redrawn in the next cycle

        parameters:     -
        return values:  -
        """
        if not self.isDirtyForever():
            self.dirty = 1

    def markDirtyForever(self):
        """
        Mark the Widget as constantly dirty and therefore to be redrawn periodically

        parameters:     -
        return values:  -
        """
        self.dirty = 2

    def markClean(self):
        """
        Mark the Widget as clean and therefore not to be redrawn in the next cycle

        parameters:     -
        return values:  -
        """
        self.dirty = 0

    def isDirty(self):
        """
        Return if the Widget is dirty and will be redrawn in the next cycle

        parameters:     -
        return values:  boolean is the Widget dirty
        """
        return self.dirty >= 1

    def isDirtyForever(self):
        """
        Return if the Widget is constantly dirty and will be redrawn periodically

        parameters:     -
        return values:  boolean is the Widget constantly dirty
        """
        return self.dirty >= 2

    def setVisible(self, visible):
        """
        Set the Widget as visible

        parameters:     boolean if the Widget should be visible
        return values:  Widget Widget returned for convenience
        """
        if self.visible != bool(visible):
            self.visible = bool(visible)
            self.setActive(bool(visible))
        return self
    
    def isVisible(self):
        """
        Return if the Widget is visible

        parameters:     -
        return values:  boolean is the Widget visible
        """
        return self.visible

    def setFocused(self, focused):
        """
        Set the Widget as focused

        parameters:     boolean if the Widget should be focused
        return values:  Widget Widget returned for convenience
        """
        if self._focus != bool(focused):
            self._focus = bool(focused)
            self.markDirty()
        return self

    def isFocused(self):
        """
        Return if the Widget is focused

        parameters:     -
        return values:  boolean is the Widget focused
        """
        return self._focus

    def setActive(self, active):
        """
        Set the Widget as active and therefore as interactive

        parameters:     boolean if the Widget should be active
        return values:  Widget Widget returned for convenience
        """
        if self._active != bool(active):
            self._active = bool(active)
            self.markDirty()
        return self

    def isActive(self):
        """
        Return if the Widget is active

        parameters:     -
        return values:  boolean is the Widget active
        """
        return self._active

    def setBounds(self, rect):
        """
        Set the Widget's bounds

        parameters:     pygame.Rect the Rect to be set
        return values:  Widget Widget returned for convenience
        """
        self._bounds = rect
        self.markDirty()
        return self

    def getBounds(self):
        """
        Return the Widget's bounds

        parameters:     -
        return values:  pygame.Rect the bounds of the Widget
        """
        return self._bounds

    def setBorder(self, border):
        """
        Set the Widget's border

        parameters:     border.Border the Border to be set
        return values:  Widget Widget returned for convenience
        """
        if isinstance(border, Border):
            self._border = border
            self.markDirty()
        return self

    def getBorder(self):
        """
        Return the Widget's border

        parameters:     -
        return values:  border.Border the Widget's border
        """
        return self._border

    def setForeground(self, color):
        """
        Set the Widget's foreground-color (not used by basic implementation)

        parameters:     tuple tuple of format pygame.Color representing the color to be set
        return values:  Widget Widget returned for convenience
        """
        self._foreground = color
        self.markDirty()
        return self

    def setBackground(self, color):
        """
        Set the Widget's background-color

        parameters:     tuple a tuple of format pygame.Color representing the color to be set
        return values:  Widget Widget returned for convenience
        """
        self._background = color
        self.markDirty()
        return self

    def getForeground(self):
        """
        Return the Widget's foreground-color (not used by basic implementation)

        parameters:     -
        return values:  tuple of format pygame.Color representing the Widget's foreground-color
        """
        return self._foreground

    def getBackground(self):
        """
        Return the Widget's background-color 

        parameters:     -
        return values:  tuple of format pygame.Color representing the Widget's background-color
        """
        return self._background

    def update(self, *args):
        """
        Perform any updates on the Widget if needed;
        basic implementation of focus, active-state and border-rendering;
        used for interaction in more advanced, derivated Widget-classes

        parameters:     tuple arguments for the update (first argument should be an instance pygame.event.Event)
        return values:  -
        """
        if self.isActive() and len(args) > 0:
            event = args[0]
            if event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 2, 3):
                self.setFocused(self.rect.collidepoint(event.pos))
        if self.isDirty():
            self.rect   = self._border.getBounds(self._bounds)
            self.image  = self._getAppearance(*args)
            if not self.isActive():
                inactive = self.image.copy()
                inactive.fill(disabeledOverlay)
                self.image.blit(inactive, (0, 0))
            self.image  = self._border.getBorderedImage(self.image)

    def _getAppearance(self, *args):
        """
        Return the underlying Widget's appearance;
        basic implementation of background-coloring

        private function

        parameters:     tuple arguments for the update (first argument should be an instance pygame.event.Event)
        return values:  pygame.Surface the underlying Widget's appearance
        """
        surface = pygame.Surface(self._bounds.size, pygame.SRCALPHA)
        surface.fill(self._background)
        return surface
