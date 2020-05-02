"""
A collection of designs for PyGVisuals.
"""

# --- imports
# pygame imports
import pygame
import pygame.font as fnt

# local imports
from ..borders import Border, BevelBorder, ColoredBorder, CompoundBorder, RoundedBorder
from .design import Design

fnt.init()


dark = Design(**{"border": CompoundBorder(ColoredBorder(1, 1, (200, 200, 200)), ColoredBorder(2, 2, (50, 50, 50))),
                 "foreground": (200, 200, 200),
                 "background": (30, 30, 30),
                 "disabeled_overlay": (255, 50, 50, 150),
                 "selection_overlay": (45, 255, 100, 120),
                 "hovered_overlay": (45, 255, 100, 60),
                 "pressed_overlay": (45, 255, 100, 120)})
"""
A dark design for PyGVisuals-widgets.
"""

hologram = Design(**{"border": CompoundBorder(RoundedBorder(2, 2, (50, 100, 255, 150), 4), RoundedBorder(4, 4, (50, 50, 50, 50), 4)),
                     "foreground": (50, 100, 255, 150),
                     "background": (50, 50, 50, 50),
                     "disabeled_overlay": (100, 100, 255, 150),
                     "selection_overlay": (100, 100, 255, 100),
                     "hovered_overlay": (100, 100, 255, 50),
                     "pressed_overlay": (100, 100, 255, 100)})
"""
A futuristic design for PyGVisuals-widgets; good for HUDs, etc.
"""

ice = Design(**{"border": CompoundBorder(RoundedBorder(3, 3, (150, 190, 255, 200), 8, True), RoundedBorder(2, 2, (30, 90, 150), 8)),
                "foreground": (255, 255, 255),
                "background": (120, 160, 200),
                "disabeled_overlay": (150, 150, 250, 150),
                "selection_overlay": (45, 110, 235, 120),
                "hovered_overlay": (150, 200, 250, 50),
                "pressed_overlay": (150, 200, 250, 100)})
"""
A design for PyGVisuals-widgets based around cold colors.
"""

classic = Design(**{"border": Border(0, 0),
                    "foreground": (255, 255, 255),
                    "background": (0, 0, 0),
                    "disabeled_overlay": (150, 150, 150, 150),
                    "scaling_function": pygame.transform.smoothscale,
                    "font": fnt.Font(None, 18),
                    "selection_overlay": (45, 110, 235, 120),
                    "hovered_overlay": (200, 200, 150, 50),
                    "pressed_overlay": (200, 200, 150, 100)})
"""
The default design hardcoded into PyGVisuals-widgets of older versions.
"""

aqua = Design(**{"border": CompoundBorder(CompoundBorder(ColoredBorder(1, 1, (235, 220, 190)), BevelBorder(4, 4, (215, 175, 145), (55, 125, 115))), ColoredBorder(1, 1, (235, 220, 190))),
                 "foreground": (135, 245, 235),
                 "background": (75, 155, 145),
                 "disabeled_overlay": (235, 220, 190, 220),
                 "selection_overlay": (45, 225, 100, 60),
                 "hovered_overlay": (235, 220, 190, 40),
                 "pressed_overlay": (235, 220, 190, 120)})
"""
A design working with turquoise and sandy colors.
"""

lavender = Design(**{"border": BevelBorder(4, 4, (215, 175, 245), (175, 125, 215), True),
                     "foreground": (255, 245, 255),
                     "background": (175, 155, 185),
                     "disabeled_overlay": (205, 145, 190, 220),
                     "selection_overlay": (255, 220, 190, 120),
                     "hovered_overlay": (255, 220, 190, 40),
                     "pressed_overlay": (255, 220, 190, 120)})
"""
A sleek design with a floral color-palette.
"""
