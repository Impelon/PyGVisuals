# -*- coding: cp1252 -*-

import pygame
from . import coloredborder

class RoundedBorder(coloredborder.ColoredBorder):

    """
    Border with rounded corners
    """

    def __init__(self, width, height, color, radius):
        """
        Initialisation of a RoundedBorder

        parameters:     int width of the RoundedBorder on the left and right sides or tuple for each side specifically
                        int height of the RoundedBorder on the top and bottom sides or tuple for each side specifically
                        tuple of format pygame.Color representing the RoundedBorder's color
                        int radius of the circles on the corners of the RoundedBorder
        return values:  -
        """
        super(RoundedBorder, self).__init__(width, height, color)
        self.radius = radius

    def getBorderedImage(self, surface):
        """
        Draw the RoundedBorder and return the bordered result

        parameters:     pygame.Surface the image to be bordered
        return values:  pygame.Surface the bordered result
        """
        try:
            if not self.isEmptyBorder():
                rect            = surface.get_rect()
                size            = self.getBounds(rect)
                bordered        = pygame.Surface(size.size, 0, surface)
                bordered.blit(self._getRoundRect(size, self.color), size)
                bordered.blit(self._getRoundRect(rect, (255, 255, 255, 255)), (self.left, self.top), special_flags = pygame.BLEND_RGBA_SUB)
                bordered.blit(surface, (self.left, self.top))
                return bordered
        except:
            return surface

    def _getRoundRect(self, rect, color):
        """
        Draw a rectangle with rounded corners and return the bordered result

        parameters:     pygame.Rect the bounds of the rectangle to be drawn
                        tuple of format pygame.Color for the color to draw with
        return values:  pygame.Surface the rectangle
        """
        rect.topleft = 0, 0
        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        surface.fill(color, rect.inflate(-2 * self.radius, 0))
        surface.fill(color, rect.inflate(0, -2 * self.radius))
        corners = rect.inflate(-2 * self.radius, -2 * self.radius)
        pygame.draw.circle(surface, color, corners.topleft, self.radius)
        pygame.draw.circle(surface, color, corners.topright, self.radius)
        pygame.draw.circle(surface, color, corners.bottomleft, self.radius)
        pygame.draw.circle(surface, color, corners.bottomright, self.radius)
        return surface
