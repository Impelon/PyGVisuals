# -*- coding: cp1252 -*-

from . import widget
import pygame

class IconWidget(widget.Widget):

    """
    Underlying class for Widgets using icons/surfaces/images;
    """
    
    def __init__(self, x, y, width, height, icon = None):
        """
        Initialisation of a IconWidget

        parameters:     int x-coordinate of the IconWidget (left)
                        int y-coordinate of the IconWidget (top)
                        int width of the IconWidget
                        int height of the IconWidget
                        pygame.Surface icon/surface of the IconWidget
        return values:  -
        """
        super(IconWidget, self).__init__(x, y, width, height)
        if icon == None:
            icon = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.setIcon(icon)
        
    def setIcon(self, icon):
        """
        Set the IconWidget's icon/surface

        parameters:     pygame.Surface icon/surface to be set
        return values:  IconWidget IconWidget returned for convenience
        """
        if isinstance(icon, pygame.Surface):
            self._icon = icon.convert_alpha(super(IconWidget, self)._getAppearance())
            self.markDirty()
        return self

    def getIcon(self):
        """
        Return the IconWidget's icon/surface

        parameters:     -
        return values:  pygame.Surface icon/surface of the IconWidget
        """
        return self._icon
