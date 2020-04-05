import pygame
import widget

WHEN_NEEDED = 0
NEVER = 1
ALWAYS = 2

defaultXBarDrawMode = WHEN_NEEDED
defaultYBarDrawMode = WHEN_NEEDED

defaultXBarColor = (120, 120, 120, 120)
defaultYBarColor = (120, 120, 120, 120)


class ScrollWidget(widget.Widget):

    """
    Underlaying class for Widgets using scrollable content.
    """

    def __init__(self, x, y, width, height):
        """
        Initialisation of a ScrollWidget

        parameters:     int x-coordinate of the ScrollWidget (left)
                        int y-coordinate of the ScrollWidget (top)
                        int width of the ScrollWidget
                        int height of the ScrollWidget
        return values:  -
        """
        super(ScrollWidget, self).__init__(x, y, width, height)
        self._xBarDrawMode = defaultXBarDrawMode
        self._yBarDrawMode = defaultYBarDrawMode
        self._xBarColor = defaultXBarColor
        self._yBarColor = defaultYBarColor
        self._xViewpoint = 0
        self._yViewpoint = 0
        self._xBarRect = pygame.Rect(self.getXViewpoint() - 15, self.rect.h - 5, 30, 5)
        self._yBarRect = pygame.Rect(self.rect.w - 5, self.getYViewpoint() - 15, 5, 30)

    def setXScrollbarDrawMode(self, mode):
        """
        Set the ScrollWidget's mode for when to draw the x-scrollbar

        parameters:     int the mode
        return values:  ScrollWidget ScrollWidget returned for convenience
        """
        self._xBarDrawMode = mode
        return self

    def setYScrollbarDrawMode(self, mode):
        """
        Set the ScrollWidget's mode for when to draw the y-scrollbar

        parameters:     int the mode
        return values:  ScrollWidget ScrollWidget returned for convenience
        """
        self._yBarDrawMode = mode
        return self

    def getXScrollbarDrawMode(self):
        """
        Return the ScrollWidget's mode for when to draw the x-scrollbar

        parameters:     -
        return values:  int the mode
        """
        return self._xBarDrawMode

    def getYScrollbarDrawMode(self):
        """
        Return the ScrollWidget's mode for when to draw the y-scrollbar

        parameters:     -
        return values:  int the mode
        """
        return self._yBarDrawMode

    def setXScrollbarColor(self, color):
        """
        Set the ScrollWidget's color of the x-scrollbar

        parameters:     tuple of format pygame.Color representing the ScrollWidget's x-scrollbar-color
        return values:  ScrollWidget ScrollWidget returned for convenience
        """
        self._xBarColor = color
        return self

    def setYScrollbarColor(self, color):
        """
        Set the ScrollWidget's color of the y-scrollbar

        parameters:     tuple of format pygame.Color representing the ScrollWidget's y-scrollbar-color
        return values:  ScrollWidget ScrollWidget returned for convenience
        """
        self._yBarColor = color
        return self

    def getXScrollbarColor(self):
        """
        Return the ScrollWidget's color of the x-scrollbar

        parameters:     -
        return values:  tuple of format pygame.Color representing the ScrollWidget's x-scrollbar-color
        """
        return self._xBarColor

    def getYScrollbarColor(self):
        """
        Return the ScrollWidget's color of the y-scrollbar

        parameters:     -
        return values:  tuple of format pygame.Color representing the ScrollWidget's y-scrollbar-color
        """
        return self._yBarColor

    def setXViewpoint(self, x):
        """
        Set the ScrollWidget's x-viewpoint

        parameters:     int the value the x-viewpoint should be set to
        return values:  -
        """
        self._xViewpoint = x
        self.markDirty()

    def getXViewpoint(self):
        """
        Return the ScrollWidget's x-viewpoint

        parameters:     -
        return values:  int the ScrollWidget's x-viewpoint
        """
        return self._xViewpoint

    def moveXViewpoint(self, amount):
        """
        Move the ScrollWidget's x-viewpoint by the given amount

        parameters:     int the amount the x-viewpoint should be moved by
        return values:  -
        """
        self.setXViewpoint(self.getXViewpoint() + amount)

    def setYViewpoint(self, y):
        """
        Set the ScrollWidget's y-viewpoint

        parameters:     int the value the y-viewpoint should be set to
        return values:  -
        """
        self._yViewpoint = y
        self.markDirty()

    def getYViewpoint(self):
        """
        Return the ScrollWidget's y-viewpoint

        parameters:     -
        return values:  int the ScrollWidget's y-viewpoint
        """
        return self._yViewpoint

    def moveYViewpoint(self, amount):
        """
        Move the ScrollWidget's y-viewpoint by the given amount

        parameters:     int the amount the y-viewpoint should be moved by
        return values:  -
        """
        self.setYViewpoint(self.getYViewpoint() + amount)

    def update(self, *args):
        """
        Handles the scrolling

        parameters: tuple arguments for the update (first argument should be an instance pygame.event.Event)
        return values: -
        """
        self._xBarRect.x = self.getXViewpoint()
        self._yBarRect.y = self.getYViewpoint()

        if len(args) > 0 and self.isActive():
            event = args[0]
            if event.type == pygame.MOUSEBUTTONUP:
                if self.isFocused():
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        if event.button == 4:
                            self.moveXViewpoint(-1)
                        elif event.button == 5:
                            self.moveXViewpoint(1)
                    else:
                        if event.button == 4:
                            self.moveYViewpoint(-1)
                        elif event.button == 5:
                            self.moveYViewpoint(1)
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0] and self.isFocused():
                    if self._xBarRect.move(self._bounds.x, self._bounds.y).collidepoint(event.pos):
                        self.setXViewpoint(event.pos[0] - self._xBarRect.x)
                    elif self._yBarRect.move(self._bounds.x, self._bounds.y).collidepoint(event.pos):
                        self.setYViewpoint(event.pos[1] - self._yBarRect.y)
        super(ScrollWidget, self).update(*args)

    def _drawXScrollbar(self, surface):
        surface.fill(self._xBarColor, self._xBarRect)

    def _drawYScrollbar(self, surface):
        surface.fill(self._yBarColor, self._yBarRect)

    def _getAppearance(self, *args):
        """
        Return the underlying Widget's appearance;
        Renders the ScrollWidget's Scrollbars

        private function

        parameters:     tuple arguments for the update (first argument should be an instance pygame.event.Event)
        return values:  pygame.Surface the underlying Widget's appearance
        """
        surface = super(ScrollWidget, self)._getAppearance(*args)
        if self._xBarDrawMode == NEVER:
            pass
        elif self._xBarDrawMode == ALWAYS:
            self._drawXScrollbar(surface)
        elif self._xBarDrawMode == WHEN_NEEDED and len(args) > 0 and self.isActive():
            event = args[0]
            if event.type == pygame.MOUSEMOTION and self.isFocused():
                if self._xBarRect.move(self._bounds.x, self._bounds.y).inflate(self.rect.w - self._xBarRect.w, 20).collidepoint(event.pos):
                    self._drawXScrollbar(surface)
        if self._yBarDrawMode == NEVER:
            pass
        elif self._yBarDrawMode == ALWAYS:
            self._drawYScrollbar(surface)
        elif self._yBarDrawMode == WHEN_NEEDED and len(args) > 0 and self.isActive():
            event = args[0]
            if event.type == pygame.MOUSEMOTION and self.isFocused():
                if self._yBarRect.move(self._bounds.x, self._bounds.y).inflate(20, self.rect.h - self._yBarRect.h).collidepoint(event.pos):
                    self._drawYScrollbar(surface)
        return surface
