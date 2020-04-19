# --- imports
# pygame imports
import pygame
# local imports
from .border import Border
from ..util import inherit_docstrings_from_superclass


class DraggableBorder(Border):

    """
    Border ...
    """

    def __init__(self, widget, border):
        """
        Initialisation of a DraggableBorder.

        Args:
            border: ...
        """
        super(DraggableBorder, self).__init__((border.left, border.right), (border.top, border.bottom))
        self.widget = widget
        self.border = border

    def _drawBorder(self, surface, original_rect, bordered_rect, *args):
        if len(args) > 0 and self.widget.isActive():
            print(args)
            #widget_rect = original_rect
            #border_rect =
            event = args[0]
            pressed = None
            if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
                pressed = event.button == 1
            elif event.type == pygame.MOUSEMOTION:
                pressed = event.buttons[0]

            if pressed is not None:
                print("pressed maybe")
            if pressed is not None and bordered_rect.collidepoint(event.pos) and not original_rect.collidepoint(event.pos):
                print("clicked border")
        return self.border._drawBorder(surface, original_rect, bordered_rect, *args)

    def getBounds(self, rect):
        return self.border.getBounds(rect)

    def isEmptyBorder(self):
        return self.border.isEmptyBorder()

# inherit docs from superclass
DraggableBorder = inherit_docstrings_from_superclass(DraggableBorder)
