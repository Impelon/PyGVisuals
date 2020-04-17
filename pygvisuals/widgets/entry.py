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

    def __init__(self, x, y, width, height, text = "", font = getDefaultDesign().font, editable=True, selection_overlay=getDefaultDesign().selection_overlay, validation_function = (lambda *x: True)):
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
            selection_overlay: A color-like object that can be interpreted as a color by pygame (such as a tuple with RGB values);
                this is used as an overlay for content that has been selected.
                The default value is the global default for the selection-color.
            validation_function: A function that validates input.
                It will receive three arguments (the new content, the old content and the widget-object)
                and should return a boolean indicating whether the input is valid (True when valid).
                The old content can be None if it was not set before; the new content can be anything that is being passed to setText().
                The default value is a function that accepts every input.
        """
        self.validation_function = validation_function
        super(Entry, self).__init__(x, y, width, height, text, font, editable, selection_overlay)

    def setText(self, text):
        """
        Set the Entry's text; needs to be valid according to the Entry's validation-function

        parameters:     string the text to be set
        return values:  Entry Entry returned for convenience
        """
        if self.validation_function and callable(self.validation_function) and self.validation_function(text, getattr(self, "text", None), self):
            super(Entry, self).setText(text)
        return self

    def setValidation(self, validation_function):
        """
        Set the entry's validation-function.

        Args:
            validation_function: A function that validates input.
                It will receive three arguments (the new text, the old text and the entry-object)
                and should return a boolean indicating whether the input is valid (True when valid).

        Returns:
            Itsself (the widget) for convenience.
        """
        self._validation_function = validation_function
        return self

    def getValidation(self):
        """
        Return the entry's validation-function.

        Returns:
            A function that validates input.
            It receives three arguments (the new text, the old text and the entry-object)
            and returns a boolean indicating whether the input is valid (True when valid).
        """
        return self._validation_function

    def update(self, *args):
        """
        Handles the selection of content and keyboard-input.

        inherit_docstring::
        """
        if len(args) > 0 and self.isActive() and self.isFocused():
            event = args[0]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.moveCursor(-1)
                elif event.key == pygame.K_RIGHT:
                    self.moveCursor(1)
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    if self.selection_index == self.cursor:
                        if event.key == pygame.K_DELETE:
                            if self._validation_function(self.text[:self.selection_index] + self.text[self.selection_index + 1:], self.text, self):
                                self.delete(self.selection_index + 1, CURSOR)
                        else:
                            if self._validation_function(self.text[:self.selection_index - 1] + self.text[self.selection_index:], self.text, self):
                                self.delete(self.selection_index - 1, CURSOR)
                                self.moveCursor(-1)
                    else:
                        s, e = self._sort(SELECTION, CURSOR)
                        if self._validation_function(self.text[:s] + self.text[e:], self.text, self):
                            self.delete(SELECTION, CURSOR)
                            self.setCursor(s)
                else:
                    char = event.unicode
                    if char != "" and (char == " " or not char.isspace()):
                        s, e = self._sort(SELECTION, CURSOR)
                        if self._validation_function(self.text[:s] + char + self.text[e:], self.text, self):
                            self.delete(SELECTION, CURSOR)
                            self.insert(s, char)
                            self.setCursor(s + 1)
            elif event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos) and event.buttons[0]:
                    self.setSelection(SELECTION, self._posToIndex(event.pos[0] - self.rect.x))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos) and event.button != 2:
                    self.setCursor(self._posToIndex(event.pos[0] - self.rect.x))

        super(Entry, self).update(*args)

    def _getAppearance(self, *args):
        """
        Renders the entry's text, cursor and selection.

        inherit_docstring::
        """
        surface = super(Entry, self)._getAppearance(*args)
        linesize = self.font.get_linesize()
        surface.blit(self._render(str(self.text)), (0, (self.bounds.height - linesize) / 2))
        if self.isFocused():
            cursor = pygame.Surface((2, linesize))
            cursor.fill(self.foreground)
            surface.blit(cursor, (self._indexToPos(CURSOR), (self.bounds.height - linesize) / 2))
            selection = pygame.Surface((abs(self._indexToPos(CURSOR) - self._indexToPos(SELECTION)), linesize), pygame.SRCALPHA, 32)
            selection.fill(self.selection_overlay)
            surface.blit(selection, (self._sort(self._indexToPos(CURSOR), self._indexToPos(SELECTION))[0] , (self.bounds.height - linesize) / 2))
        return surface

    validation_function = property(lambda obj: obj.getValidation(), lambda obj, arg: obj.setValidation(arg), doc="""The widget's function used for validating input to its content.""")

# inherit docs from superclass
Entry = inherit_docstrings_from_superclass(Entry)
