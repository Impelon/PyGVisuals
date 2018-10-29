# -*- coding: cp1252 -*-

import pygame
from . import border

class BevelBorder(border.Border):

    """
    Border with two colors, creating a bevel-effect
    """

    def __init__(self, width, height, upper, lower):
        """
        Initialisation of a BevelBorder

        parameters:     int width of the BevelBorder on the left and right sides or tuple for each side specifically
                        int height of the BevelBorder on the top and bottom sides or tuple for each side specifically
                        tuple of format pygame.Color representing the BevelBorder's upper color
                        tuple of format pygame.Color representing the BevelBorder's lower color
        return values:  -
        """
        super(BevelBorder, self).__init__(width, height)
        self.upper = upper
        self.lower = lower

    def getBorderedImage(self, surface):
        """
        Draw the BevelBorder and return the bordered result

        parameters:     pygame.Surface the image to be bordered
        return values:  pygame.Surface the bordered result
        """
        try:
            if not self.isEmptyBorder():
                rect        = surface.get_rect()
                size        = self.getBounds(rect)
                bordered    = pygame.Surface(size.size, 0, surface)
                bordered.fill(self.upper)
                bordered.fill(self.lower, size.move(self.width + self.left, self.height + self.top))
                bordered.fill((0, 0, 0, 0), rect.move(self.left, self.top))
                bordered.blit(surface, (self.left, self.top))
                return bordered
        except:
            return surface
