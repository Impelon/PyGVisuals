# -*- coding: cp1252 -*-

import pygame
import border

class CompoundBorder(border.Border):

    """
    Border composed of two other Border-instances
    """

    def __init__(self, inner, outer):
        """
        Initialisation of a CompoundBorder

        parameters:     border.Border the Border representing the inner part of the CompoundBorder
                        border.Border the Border representing the outer part of the CompoundBorder
        return values:  -
        """
        super(CompoundBorder, self).__init__((inner.left + outer.left, inner.width + outer.width),
                               (inner.top + outer.top, inner.height + outer.height))
        self.inner = inner
        self.outer = outer

    def getBorderedImage(self, surface):
        """
        Draw the CompoundBorder and return the bordered result

        parameters:     pygame.Surface the image to be bordered
        return values:  pygame.Surface the bordered result
        """
        if isinstance(surface, pygame.Surface) and not self.isEmptyBorder():
            return self.outer.getBorderedImage(self.inner.getBorderedImage(surface))
        return surface
