# -*- coding: cp1252 -*-

import pygame

class Border(object):

    """
    Underlying class for Borders;
    intended for use together with pygame.Surface
    """

    def __init__(self, width, height):
        """
        Initialisation of a Border

        parameters:     int width of the Border on the left and right sides or tuple for each side specifically
                        int height of the Border on the top and bottom sides or tuple for each side specifically
        return values:  -
        """
        super(Border, self).__init__()
        if isinstance(width, tuple):
            self.left   = width[0]
            self.width  = width[1]
        else:
            self.left   = width
            self.width  = width
        if isinstance(height, tuple):
            self.top    = height[0]
            self.height = height[1]
        else:
            self.top    = height
            self.height = height

    def getBorderedImage(self, surface):
        """
        Draw the Border and return the bordered result

        parameters:     pygame.Surface the image to be bordered
        return values:  pygame.Surface the bordered result
        """
        if isinstance(surface, pygame.Surface) and not self.isEmptyBorder():
            rect            = surface.get_rect()
            size            = self.getBounds(rect)
            bordered        = pygame.Surface(size.size, 0, surface)
            bordered.fill((0, 0, 0))
            bordered.fill((0, 0, 0, 0), rect.move(self.left, self.top))
            bordered.blit(surface, (self.left, self.top))
            return bordered
        return surface

    def getBounds(self, rect):
        """
        Return the adjusted bounds so that they fit the Border

        parameters:     pygame.Rect the original bounds
        return values:  pygame.Rect the adjusted bounds
        """
        if isinstance(rect, pygame.Rect):
            bordered = rect.inflate(self.width + self.left, self.height + self.top)
            bordered.top = rect.top - self.top
            bordered.left = rect.left - self.left
            return bordered
        return rect

    def isEmptyBorder(self):
        """
        Return if the Border is empty and therefore of zero size

        parameters:     -
        return values:  boolean is the Border empty
        """
        return (self.left + self.top + self.width + self.height) == 0
