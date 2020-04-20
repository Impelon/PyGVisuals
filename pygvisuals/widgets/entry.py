# --- imports
# pygame imports
import pygame

# local imports
from .selection_text_widget import *
from ..designs import getDefaultDesign
from ..util import inherit_docstrings_from_superclass


class Entry(SelectionTextWidget):

    """
    Entry-fields that accept keyboard-input.
    """

    def __init__(self, x, y, width, height, text="", font=getDefaultDesign().font, editable=True, validation_function=(lambda *x: True), selection_overlay=getDefaultDesign().selection_overlay):
        """
        Initialisation of an Entry.

        Args:
            x: An integer specifing the x-coordinate of the widget.
                This is the horizontal distance from the left reference point.
            y: An integer specifing the y-coordinate of the widget.
                This is the vertical distance from the top reference point.
            width: An integer specifing the width of the widget.
            height: An integer specifing the height of the widget.
            text: A string specifing the content of the widget.
                The default value is an empty string.
            font: A font-like object that can be interpreted by pygame.font as a Font;
                this is used as the font for rendering text.
                The default value is the global default for fonts.
            editable: A boolean indicating whether the widget's content is editable by the user.
                The default value is True, meaning it can be edited by user-input.
            validation_function: A function that validates changed content.
                It will receive three arguments (the new content, the old content and the widget-object)
                and should return a boolean indicating whether the change is valid (True when valid).
                The old content can be None if it was not set before; the new content can be anything that is being passed to setText().
                The default value is a function that accepts every change.
            selection_overlay: A color-like object that can be interpreted as a color by pygame (such as a tuple with RGB values);
                this is used as an overlay for content that has been selected.
                The default value is the global default for the selection-color.
        """
        super(Entry, self).__init__(x, y, width, height, text, font, editable, validation_function, selection_overlay)

    def update(self, *args):
        """
        Additionally handles keyboard-input.

        inherit_doc::
        """
        if len(args) > 0 and self.isActive() and self.isFocused():
            event = args[0]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.moveCursor(-1)
                elif event.key == pygame.K_RIGHT:
                    self.moveCursor(1)
                elif self.isEditable():
                    if event.key not in (pygame.K_BACKSPACE, pygame.K_DELETE):
                        char = event.unicode
                        valid = False
                        if hasattr(char, "isprintable"):
                            valid = char.isprintable()
                        elif char == " " or not char.isspace():
                            valid = True
                        if char and valid:
                            s, c = self._sort(SELECTION, CURSOR)
                            if self.setText(self.text[:s] + char + self.text[c:], True):
                                self.setCursor(s + 1)

        super(Entry, self).update(*args)

    def _getAppearance(self, *args):
        """
        Additionally renders the entry's text, cursor and selection.

        inherit_doc::
        """
        surface = super(Entry, self)._getAppearance(*args)
        linesize = self.font.get_linesize()
        surface.blit(self._render(self.text), (0, (self.bounds.height - linesize) / 2))
        if self.isFocused():
            cursor_pos = self._indexToPos(CURSOR)[0]
            selection_pos = self._indexToPos(SELECTION)[0]
            cursor = pygame.Surface((2, linesize))
            cursor.fill(self.foreground)
            surface.blit(cursor, (cursor_pos, (self.bounds.height - linesize) / 2))
            selection = pygame.Surface((abs(cursor_pos - selection_pos), linesize), pygame.SRCALPHA, 32)
            selection.fill(self.selection_overlay)
            surface.blit(selection, (self._sort(cursor_pos, selection_pos, False)[0], (self.bounds.height - linesize) / 2))
        return surface


# inherit docs from superclass
Entry = inherit_docstrings_from_superclass(Entry)
