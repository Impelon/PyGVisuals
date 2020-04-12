import pygame.font as fnt
from ..borders import Border, ColoredBorder, CompoundBorder, RoundedBorder
from .design import Design


fnt.init()

"""
A collection of designs for PyGVisuals.
"""

dark = Design(**{"border": CompoundBorder(ColoredBorder(1, 1, (200, 200, 200)), ColoredBorder(2, 2, (50, 50, 50))),
                 "foreground": (200, 200, 200),
                 "background": (30, 30, 30),
                 "disabeled_overlay": (255, 50, 50, 150),
                 "font": fnt.Font(None, 20),
                 "selection_color": (45, 255, 100, 120),
                 "hovered_color": (45, 255, 100, 60),
                 "pressed_color": (45, 255, 100, 120)})
"""
A dark design for PyGVisuals-widgets.
"""

hologram = Design(**{"border": CompoundBorder(RoundedBorder(2, 2, (50, 100, 255, 150), 4), RoundedBorder(4, 4, (50, 50, 50, 50), 4)),
                     "foreground": (50, 100, 255, 150),
                     "background": (50, 50, 50, 50),
                     "disabeled_overlay": (100, 100, 255, 150),
                     "font": fnt.Font(None, 18),
                     "selection_color": (100, 100, 255, 100),
                     "hovered_color": (100, 100, 255, 50),
                     "pressed_color": (100, 100, 255, 100)})
"""
A futuristic design for PyGVisuals-widgets; good for HUDs, etc.
"""

ice = Design(**{"border": CompoundBorder(RoundedBorder(3, 3, (150, 190, 255, 200), 8), RoundedBorder(2, 2, (30, 90, 150), 8)),
                "foreground": (255, 255, 255),
                "background": (120, 160, 200),
                "disabeled_overlay": (150, 150, 250, 150),
                "font": fnt.Font(None, 18),
                "selection_color": (45, 110, 235, 120),
                "hovered_color": (150, 200, 250, 50),
                "pressed_color": (150, 200, 250, 100)})
"""
A design for PyGVisuals-widgets based around cold colors.
"""

classic = Design(**{"border": Border(0, 0),
                    "foreground": (255, 255, 255),
                    "background": (0, 0, 0),
                    "disabeledOverlay": (150, 150, 150, 150),
                    "font": fnt.Font(None, 18),
                    "selection_color": (45, 110, 235, 120),
                    "hovered_color": (200, 200, 150, 50),
                    "pressed_color": (200, 200, 150, 100)})
"""
The default design hardcoded into PyGVisuals-widgets of older versions.
"""
