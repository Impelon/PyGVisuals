# --- imports
# pygame imports
import pygame


class Border(object):

    """
    Underlying class for borders compatible with pygame's surfaces.
    Intended to be used together with PyGVisuals' widgets.
    A border will have four sides, surrounding a provided surface.
    """

    def __init__(self, width, height):
        """
        Initialisation of a Border.

        Args:
            width: The width of the border.
                This can either be an integer for the width of both the left and right side
                or a tuple for each side specifically (left, right).
            height: The height of the border.
                This can either be an integer for the height of both the top and bottom side
                or a tuple for each side specifically (top, bottom).
        """
        super(Border, self).__init__()
        self.remove_background_after_draw = True
        self.draw_surface_above_border = True
        try:
            self.left = width[0]
            self.right = width[1]
        except:
            self.left = width
            self.right = width
        try:
            self.top = height[0]
            self.bottom = height[1]
        except:
            self.top = height
            self.bottom = height

    def getBorderedImage(self, surface, *args):
        """
        Draw the border surrounding the given surface and return the bordered result.

        Args:
            surface: A surface-like object (e.g. pygame.Surface) that should be bordered.
            *args: Any arguments provided for the update. This can include an optional pygame.event.Event to process.

        Returns:
            A pygame.Surface with the bordered result.
        """
        try:
            if not self.isEmptyBorder():
                rect = surface.get_rect()
                size = self.getBounds(rect)
                result = pygame.Surface(size.size, 0, surface)
                border = result.copy()
                border = self._drawBorder(border, rect, size, *args)
                if self.remove_background_after_draw:
                    border.fill((0, 0, 0, 0), rect.move(self.left, self.top))
                blit_sequence = [(border, (0, 0)), (surface, (self.left, self.top))]
                if not self.draw_surface_above_border:
                    blit_sequence.reverse()
                result.blits(blit_sequence)
                return result
        except:
            pass
        return surface

    def _drawBorder(self, surface, original_rect, bordered_rect, *args):
        """
        Draw the border on the given surface and return the result.

        This is an internal function.
        It will be called internally from getBorderedImage(...) and
        the appropiate space will be painted over with the original surface.
        This should not leave a hole, as the space for the original surface will be cleared by getBorderedImage(...),
        except when the border's remove_background_after_draw-attribute is set to False.

        Args:
            surface: A surface-like object (e.g. pygame.Surface) that will have the border drawn on.
                It should be able to fit the border.
                This is the case if its size is equal to the size bordered_size.
            original_size: A rect-like object (e.g. pygame.Rect)
                denoting the bounds of the original surface without the border.
            bordered_size: A rect-like object (e.g. pygame.Rect)
                denoting the bounds of the original surface with the border drawn on it.
            *args: Any arguments provided for the update. This can include an optional pygame.event.Event to process.

        Returns:
            A surface-like object with the same size as the provided one, but with the border painted on top of it.
        """
        surface.fill((0, 0, 0))
        return surface

    def getBounds(self, rect):
        """
        Return the new size of a rect if it was to be bordered with this border.

        Args:
            A rect-like object (e.g. pygame.Rect) to calculate the new bounds from.

        Returns:
            A rect-like object (e.g. pygame.Rect) with the size if it was to be bordered with this border.
        """
        try:
            bordered = rect.inflate(self.right + self.left, self.bottom + self.top)
            bordered.top = rect.top - self.top
            bordered.left = rect.left - self.left
            return bordered
        except:
            return rect

    def isEmptyBorder(self):
        """
        Return whether the border is empty and therefore of zero size.
        An empty border needs not to be drawn.

        Returns:
            A boolean indicating whether all sides of the border have zero width.
        """
        return (self.left + self.top + self.right + self.bottom) == 0
