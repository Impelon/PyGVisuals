# --- imports
# preinstalled python libraries
import unittest
from unittest.mock import Mock
import types

# pygame imports
import pygame
from pygame.locals import *

# local imports
from pygvisuals.widgets import Widget


def record_success(func):
    def record_result(self, *args, **kwargs):
        self._test_successful = False
        func(self, *args, **kwargs)
        self._test_successful = True
    return record_result


def record_successful_tests(cls):
    for name, func in vars(cls).items():
        if name.startswith("test") and isinstance(func, types.FunctionType):
            setattr(cls, name, record_success(func))
    return cls


@record_successful_tests
class TestWidget(unittest.TestCase):

    def mockClickAt(self, pos, button=1):
        """
        Return a Mock-object of an MOUSEBUTTONDOWN-event for the specified position and button.
        """
        return Mock(**{"type": MOUSEBUTTONDOWN,
                       "button": button,
                       "pos": pos})

    def mockBorder(self):
        """
        Return a Mock-object of an empty border.
        """
        return Mock(**{"getBorderedImage.side_effect": lambda x, *args: x,
                       "getBounds.side_effect": lambda x, *args: x,
                       "isEmptyBorder.return_value": True})

    def assertColorsIn(self, colors, surface, rect, should_check=None):
        """
        Assert that all colors of the surface in the given rect are in the given container.

        Args:
            colors: A sequence/container containing all colors that are allowed.
            surface: A pygame-Surface to check the colors on.
            rect: A pygame-Rect which specifies the bounds to check for colors.
            should_check: A function that takes two arguments x, y which are coordinates on the surface,
                and returns True if the corresponding pixel should be checked, False otherwise.
                If this is a falsy value (e.g. None), all pixels will be checked.
                The default value for this is None.
        """
        if not should_check:
            def should_check(x, y): return True
        for x in range(rect.left, rect.right):
            for y in range(rect.top, rect.bottom):
                if should_check(x, y):
                    self.assertIn(self.surface.get_at((x, y)), colors)

    @property
    def surface_color(self):
        return (128, 128, 128, 255)

    @property
    def surface_size(self):
        return (50, 50)

    @property
    def widget_type(self):
        return Widget

    @property
    def widget_x(self):
        return 1

    @property
    def widget_y(self):
        return 1

    @property
    def widget_width(self):
        return 1

    @property
    def widget_height(self):
        return 1

    def setUp(self):
        self.border_mock = self.mockBorder()
        self.surface = pygame.Surface(self.surface_size)
        self.surface.fill(self.surface_color)
        self.widget = self.widget_type(self.widget_x, self.widget_y, self.widget_width, self.widget_height)
        self.widget.setBorder(self.border_mock)
        self.group = pygame.sprite.LayeredDirty(self.widget)

    def tearDown(self):
        if not getattr(self, "_test_successful", True):
            pygame.display.init()
            screen = pygame.display.set_mode(self.surface_size, DOUBLEBUF, 32)
            screen.blit(self.surface, (0, 0))
            pygame.display.update()
            going = True
            while going:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        going = False
                pygame.time.wait(100)
            pygame.display.quit()

    def test_border_called(self):
        self.widget.markDirty()
        self.widget.update()
        self.group.draw(self.surface)
        self.border_mock.getBorderedImage.assert_called_once()

    def test_background(self):
        color = (255, 0, 128, 255)
        self.widget.background = color
        self.widget.update()
        self.group.draw(self.surface)
        self.assertEqual(color, self.surface.get_at((self.widget_x, self.widget_y)))

    def test_move_bounds(self):
        color = (255, 255, 255, 255)
        move_x = 5
        move_y = 3
        asserted_bounds = pygame.Rect(self.widget_x + move_x, self.widget_y + move_y, self.widget_width, self.widget_height)
        self.widget.background = color
        self.widget.bounds.move_ip((move_x, move_y))
        self.widget.update()
        self.group.draw(self.surface)
        self.assertEqual(color, self.surface.get_at(asserted_bounds.topleft))
        self.assertColorsIn([self.surface_color], self.surface, asserted_bounds.inflate(2, 2),
                            should_check=lambda x, y: not asserted_bounds.collidepoint(x, y))

    def test_change_bounds(self):
        color = (255, 255, 255, 255)
        asserted_bounds = pygame.Rect(self.widget_x, self.widget_y, self.widget_width + 4, self.widget_height + 1)
        self.widget.background = color
        self.widget.bounds = asserted_bounds
        self.widget.update()
        self.group.draw(self.surface)
        self.assertEqual(color, self.surface.get_at(asserted_bounds.topleft))
        self.assertColorsIn([self.surface_color], self.surface, asserted_bounds.inflate(2, 2),
                            should_check=lambda x, y: not asserted_bounds.collidepoint(x, y))

    def test_invisibility(self):
        self.widget.visible = False
        self.widget.update()
        self.group.draw(self.surface)
        self.assertColorsIn([self.surface_color], self.surface, self.surface.get_rect())

    def test_focus(self):
        self.assertFalse(self.widget.focused)
        self.widget.update(self.mockClickAt((self.widget_x, self.widget_y)))
        self.assertTrue(self.widget.focused)
        self.widget.update(self.mockClickAt((self.widget_x - 1, self.widget_y)))
        self.assertFalse(self.widget.focused)

    def test_active(self):
        color = (12, 89, 172, 255)
        self.widget.disabeled_overlay = color
        self.widget.active = False
        self.assertFalse(self.widget.focused)
        self.widget.update(self.mockClickAt((self.widget_x, self.widget_y)))
        self.assertFalse(self.widget.focused)
        self.widget.update(self.mockClickAt((self.widget_x - 1, self.widget_y)))
        self.assertFalse(self.widget.focused)
        self.group.draw(self.surface)
        self.assertEqual(color, self.surface.get_at((self.widget_x, self.widget_y)))


if __name__ == "__main__":
    unittest.main()
