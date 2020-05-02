"""
Package with the Trueno font used as default font for PyGVisuals.

Note: Trueno is not licensed under PyGVisuals' license. You can find its license as a separate file in this directory.
"""

__all__ = ["create_font"]

import os.path
import pygame.font

__italic_suffix = "It"

FONT_REGULAR = "Rg"
FONT_REGULAR_ITALIC = FONT_REGULAR + __italic_suffix
FONT_BOLD = "Bd"
FONT_BOLD_ITALIC = FONT_BOLD + __italic_suffix
FONT_BOLD_OUTLINE = FONT_BOLD + "Ol"
FONT_BOLD_OUTLINE_ITALIC = FONT_BOLD_OUTLINE + __italic_suffix
FONT_SEMIBOLD = "S" + FONT_BOLD
FONT_SEMIBOLD_ITALIC = FONT_SEMIBOLD + __italic_suffix
FONT_EXTRABOLD = "Ex" + FONT_BOLD
FONT_EXTRABOLD_ITALIC = FONT_EXTRABOLD + __italic_suffix
FONT_EXTRABOLD_OUTLINE = FONT_EXTRABOLD + "Ol"
FONT_EXTRABOLD_OUTLINE_ITALIC = FONT_EXTRABOLD_OUTLINE + __italic_suffix
FONT_BLACK = "Blk"
FONT_BLACK_ITALIC = FONT_BLACK + __italic_suffix
FONT_BLACK_OUTLINE = FONT_BLACK + "Ol"
FONT_BLACK_OUTLINE_ITALIC = FONT_BLACK_OUTLINE + __italic_suffix
FONT_ULTRABLACK = "Ult" + FONT_BLACK
FONT_ULTRABLACK_ITALIC = FONT_ULTRABLACK + __italic_suffix
FONT_LIGHT = "Lt"
FONT_LIGHT_ITALIC = FONT_LIGHT + __italic_suffix
FONT_ULTRALIGHT = "Ult" + FONT_LIGHT
FONT_ULTRALIGHT_ITALIC = FONT_ULTRALIGHT + __italic_suffix

__all__.extend(filter(lambda x: x.startswith("FONT_"), vars().keys()))

pygame.font.init()


def create_font(size, type=FONT_REGULAR, italic=False, default=None):
    """
    Create a pygame.Font-object with a Truano-font.

    Args:
        size: An integer denoting the height of the font in pixels.
        type: A string denoting the type of Trueno-font. This should be a known fonttype-constant.
            The default value is FONT_REGULAR, meaning the font created will be `Trueno Regular`.
        italic: A boolean indicating whether to create italic font. This will try to use italic font provided by the font-software.
            The default value is False, meaning the font will not be italic.
        default: A default-value to return in case an exception occurs when creating the font.
            This is None by default.

    Returns:
        A pygame.Font-object with the specified configuration.
    """
    suffix = ""
    if italic and not type.endswith(__italic_suffix):
        suffix = __italic_suffix
    try:
        return pygame.font.Font(os.path.join(os.path.dirname(__file__), "Trueno{}{}.otf".format(type, suffix)), size)
    except:
        return default
