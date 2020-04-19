# --- imports
# pygame imports
import pygame

# local imports
from .colored_border import ColoredBorder
from ..util import inherit_docstrings_from_superclass


class RoundedBorder(ColoredBorder):

    """
    Border with rounded corners, which can be colored.
    """

    def __init__(self, width, height, color, radius, surface_above_border = False):
        """
        Initialisation of a RoundedBorder.
        The rounded rectangle is produced by placing 4 circles on the side of the rectangle as described here:
        https://github.com/pygame/pygame/issues/1120

        Args:
            inherit_doc:: arguments
            radius: An integer denoting the radius in pixels of the circles on the corners of the RoundedBorder.
            surface_above_border: A boolean controling whether the border will be drawn behind the surface
                or on top of it. The default value is False, meaning the border will be drawn on top of the surface.
        """
        super(RoundedBorder, self).__init__(width, height, color)
        self.radius = radius
        self.remove_background_after_draw = surface_above_border
        self.draw_surface_above_border = surface_above_border

    def _drawBorder(self, surface, original_rect, bordered_rect, *args):
        surface.blit(self._getRoundRect(bordered_rect, self.color), (0, 0))
        if not self.remove_background_after_draw:
            surface.blit(self._getRoundRect(original_rect, (255, 255, 255, 255)), (self.left, self.top), special_flags=pygame.BLEND_RGBA_SUB)
        return surface

    def _getRoundRect(self, rect, color):
        """
        Draw a rectangle with rounded corners and return the result.

        This is an internal function.

        Args:
            rect: A rect-like object (e.g. pygame.Rect)
                denoting the bounds of the rectangle to be drawn.
            color: A color-like object that can be interpreted as a color by pygame (such as a tuple with RGB values).
                This will be used as the color for the rectable.
        Returns:
            A pygame.Surface with the result.
        """
        rect = rect.copy()
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


# inherit docs from superclass
RoundedBorder = inherit_docstrings_from_superclass(RoundedBorder)
