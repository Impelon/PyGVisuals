# --- imports
# pygame imports
import pygame

# local imports
from .border import Border


class BevelBorder(Border):

    """
    Border with two colored lines, creating a simple bevel-effect.
    """

    def __init__(self, width, height, upper, lower, lower_has_right_side = False):
        """
        Initialisation of a BevelBorder.

        Args:
            width: The width of the BevelBorder.
                This can either be an integer for the width of both the left and right side
                or a tuple for each side specifically (left, right).
            height: The height of the BevelBorder.
                This can either be an integer for the height of both the top and bottom side
                or a tuple for each side specifically (top, bottom).
            upper: A color-like object that can be interpreted as a color by pygame (such as a tuple with RGB values).
                This will be used as the color for the upper (and left) side of the border.
            lower: A color-like object that can be interpreted as a color by pygame (such as a tuple with RGB values).
                This will be used as the color for the lower (and right) side of the border.
        """
        super(BevelBorder, self).__init__(width, height)
        self.upper = upper
        self.lower = lower
        self.lower_has_right_side = lower_has_right_side

    def getBorderedImage(self, surface):
        """
        Draw the border surrounding a given surface and return the bordered result.

        parameters:     pygame.Surface the image to be bordered
        return values:  pygame.Surface the bordered result
        """
        try:
            if not self.isEmptyBorder():
                rect = surface.get_rect()
                size = self.getBounds(rect)
                bordered = pygame.Surface(size.size, 0, surface)
                bordered.fill(self.upper)
                lower_size = size.move(self.width + self.left, self.height + self.top)
                if self.lower_has_right_side:
                    lower_size.width -= self.width
                    lower_size.left -= self.width
                bordered.fill(self.lower, lower_size)
                bordered.fill((0, 0, 0, 0), rect.move(self.left, self.top))
                bordered.blit(surface, (self.left, self.top))
                return bordered
        except:
            return surface
