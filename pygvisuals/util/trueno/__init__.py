"""
Package with the Trueno font used as default font for PyGVisuals.

Note: Trueno is not licensed under PyGVisuals' license. You can find its license as a separate file in this directory.
"""

__all__ = ["create_font"]

import os.path
import pygame.font

__italic_suffix = "It"

TRUENO_REGULAR = "Rg"
TRUENO_REGULAR_ITALIC = TRUENO_REGULAR + __italic_suffix
TRUENO_BOLD = "Bd"
TRUENO_BOLD_ITALIC = TRUENO_BOLD + __italic_suffix
TRUENO_BOLD_OUTLINE = TRUENO_BOLD + "Ol"
TRUENO_BOLD_OUTLINE_ITALIC = TRUENO_BOLD_OUTLINE + __italic_suffix
TRUENO_SEMIBOLD = "S" + TRUENO_BOLD
TRUENO_SEMIBOLD_ITALIC = TRUENO_SEMIBOLD + __italic_suffix
TRUENO_EXTRABOLD = "Ex" + TRUENO_BOLD
TRUENO_EXTRABOLD_ITALIC = TRUENO_EXTRABOLD + __italic_suffix
TRUENO_EXTRABOLD_OUTLINE = TRUENO_EXTRABOLD + "Ol"
TRUENO_EXTRABOLD_OUTLINE_ITALIC = TRUENO_EXTRABOLD_OUTLINE + __italic_suffix
TRUENO_BLACK = "Blk"
TRUENO_BLACK_ITALIC = TRUENO_BLACK + __italic_suffix
TRUENO_BLACK_OUTLINE = TRUENO_BLACK + "Ol"
TRUENO_BLACK_OUTLINE_ITALIC = TRUENO_BLACK_OUTLINE + __italic_suffix
TRUENO_ULTRABLACK = "Ult" + TRUENO_BLACK
TRUENO_ULTRABLACK_ITALIC = TRUENO_ULTRABLACK + __italic_suffix
TRUENO_LIGHT = "Lt"
TRUENO_LIGHT_ITALIC = TRUENO_LIGHT + __italic_suffix
TRUENO_ULTRALIGHT = "Ult" + TRUENO_LIGHT
TRUENO_ULTRALIGHT_ITALIC = TRUENO_ULTRALIGHT + __italic_suffix

__all__.extend(filter(lambda x: x.startswith("TRUENO_"), vars().keys()))

pygame.font.init()


def create_font(size=11, type=TRUENO_REGULAR, italic=False, default=None):
    """
    Create a pygame.Font-object with a Truano-font.

    Args:
        size: An integer denoting the height of the font in pixels.
            This is 11 by default.
        type: A string denoting the type of Trueno-font. This should be a known fonttype-constant.
            The default value is TRUENO_REGULAR, meaning the font created will be `Trueno Regular`.
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
