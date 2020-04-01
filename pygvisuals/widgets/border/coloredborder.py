# -*- coding: cp1252 -*-

import pygame
from . import border

class ColoredBorder(border.Border):

    """
    Border with a color
    """

    def __init__(self, width, height, color):
        """
        Initialisation of a ColoredBorder

        parameters:     int width of the ColoredBorder on the left and right sides or tuple for each side specifically
                        int height of the ColoredBorder on the top and bottom sides or tuple for each side specifically
                        tuple of format pygame.Color representing the ColoredBorder's color
        return values:  -
        """
        super(ColoredBorder, self).__init__(width, height)
        self.color = color

    def getBorderedImage(self, surface):
        """
        Draw the ColoredBorder and return the bordered result

        parameters:     pygame.Surface the image to be bordered
        return values:  pygame.Surface the bordered result
        """
        try:
            if not self.isEmptyBorder():
                rect        = surface.get_rect()
                size        = self.getBounds(rect)
                bordered    = pygame.Surface(size.size, 0, surface)
                bordered.fill(self.color)
                bordered.fill((0, 0, 0, 0), rect.move(self.left, self.top))
                bordered.blit(surface, (self.left, self.top))
                return bordered
        except:
            return surface
