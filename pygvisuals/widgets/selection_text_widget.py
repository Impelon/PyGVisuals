# --- imports
# pygame imports
import pygame

# local imports
from .text_widget import TextWidget
from ..designs import getDefaultDesign, getFallbackDesign
from ..util import inherit_docstrings_from_superclass


# constants
START = 0
"""A index-constant for the first index of a widget's content."""
END = 'e'
"""A index-constant for the last index of a widget's content."""
CURSOR = 'c'
"""A index-constant for the cursor of a widget."""
INSERT = CURSOR
"""A index-constant alias for CURSOR."""
CURRENT = CURSOR
"""A index-constant alias for CURSOR."""
SELECTION = 's'
"""A index-constant for the selection-index of a widget."""

# set defaults
getFallbackDesign().selection_overlay = (45, 110, 235, 120)
"""Color to be overlayed by default for content that has been selected in a widget."""


class SelectionTextWidget(TextWidget):

    """
    Underlying class for widgets using selectable content.
    """

    def __init__(self, x, y, width, height, text="", font=getDefaultDesign().font, editable=False, validation_function=(lambda *x: True), selection_overlay=getDefaultDesign().selection_overlay):
        """
        Initialisation of a SelectionTextWidget.

        Args:
            inherit_doc:: arguments
            editable: A boolean indicating whether the widget's content is editable by the user.
                The default value is False, meaning it can not be edited by user-input.
            validation_function: A function that validates changed content.
                It will receive three arguments (the new content, the old content and the widget-object)
                and should return a boolean indicating whether the change is valid (True when valid).
                The old content can be None if it was not set before;
                the new content can be anything that is being passed to setText().
                The default value is a function that accepts every change.
            selection_overlay: A color-like object that can be interpreted as a color by pygame (such as a tuple with RGB values);
                this is used as an overlay for content that has been selected.
                The default value is the global default for the selection-color.
        """
        self.validation_function = validation_function
        super(SelectionTextWidget, self).__init__(x, y, width, height, text, font)
        self._cursor = 0
        self._selection_index = 0
        self.editable = editable
        self.selection_overlay = selection_overlay

    def setEditable(self, editable):
        """
        Set whether the widget's content is editable by the user (via user-input).

        Args:
            editable: A boolean indicating whether the widget's content is editable by the user.

        Returns:
            Itsself (the widget) for convenience.
        """
        self._editable = bool(editable)
        return self

    def isEditable(self):
        """
        Return whether the widget's content is editable by the user (via user-input).

        Returns:
            A boolean indicating whether the widget's content is editable by the user.
        """
        return self._editable

    def setValidation(self, validation_function):
        """
        Set the widget's validation-function.

        Args:
            validation_function: A function that validates changed content.
                It will receive three arguments (the new content, the old content and the widget-object)
                and should return a boolean indicating whether the change is valid (True when valid).
                The old content can be None if it was not set before; the new content can be anything that is being passed to setText().

        Returns:
            Itsself (the widget) for convenience.
        """
        self._validation_function = validation_function
        return self

    def getValidation(self):
        """
        Return the widget's validation-function.

        Returns:
            A function that validates changed content.
            It will receive three arguments (the new content, the old content and the widget-object)
            and should return a boolean indicating whether the change is valid (True when valid).
            The old content can be None if it was not set before; the new content can be anything that is being passed to setText().
        """
        return self._validation_function

    def setText(self, text, return_success_boolean=False):
        """
        Additionally validate the change of content.

        inherit_doc::
        """
        if self.validation_function and callable(self.validation_function) and self.validation_function(text, getattr(self, "text", None), self):
            super(SelectionTextWidget, self).setText(text)
            if return_success_boolean:
                return True
        if return_success_boolean:
            return False
        return self

    def insert(self, index, text):
        """
        Insert a given text at the given index.

        Args:
            index: An integer (or known constant) representing the position the text should be insterted at.
            text: A string specifing the content to add to the content of the widget.

        Returns:
            A boolean indicating whether the change was successful.
        """
        index = self.getActualIndex(index)
        return self.setText(self.text[:index] + text + self.text[index:], True)

    def delete(self, start, end):
        """
        Deletes the widget's content between the two given indices.

        Args:
            start: An integer representing the index from which the content should be deleted.
            end: An integer representing the index until which the content should be deleted.

        Returns:
            A boolean indicating whether the change was successful.
        """
        start, end = self._sort(start, end)
        return self.setText(self.text[:start] + self.text[end:], True)

    def setSelectionOverlay(self, color):
        """
        Set the widget's color to overlay for content that has been selected.

        Args:
            color: A color-like object that can be interpreted as a color by pygame (such as a tuple with RGB values).

        Returns:
            Itsself (the widget) for convenience.
        """
        self._selection_overlay = color
        self.markDirty()
        return self

    def getSelectionOverlay(self):
        """
        Return the widget's color to overlay for content that has been selected.

        Returns:
            A color-like object that represents the widget's color to overlay for content that has been selected.
        """
        return self._selection_overlay

    def setCursor(self, index):
        """
        Set the widget's cursor-position.

        Args:
            index: An integer (or known constant) representing the index the cursor should be set to.

        Returns:
            Itsself (the widget) for convenience.
        """
        return self.setSelection(index, index)

    def moveCursor(self, amount):
        """
        Move the widget's cursor-position by the given amount.

        Args:
            amount: An integer representing the amount the cursor should be moved by.

        Returns:
            Itsself (the widget) for convenience.
        """
        return self.setCursor(self.cursor + int(amount))

    def getCursor(self):
        """
        Return the widget's cursor-position.

        Returns:
            An integer representing the index the cursor is at.
        """
        return self._cursor

    def setSelectionIndex(self, index):
        """
        Set the widget' selection-index.

        Args:
            index: An integer (or known constant) representing the index the selection-index should be set to.

        Returns:
            Itsself (the widget) for convenience.
        """
        return self.setSelection(index, CURSOR)

    def moveSelectionIndex(self, amount):
        """
        Move the widget's cursor-position by the given amount.

        Args:
            amount: An integer representing the amount the cursor should be moved by.

        Returns:
            Itsself (the widget) for convenience.
        """
        return self.setSelectionIndex(self.selection_index + int(amount))

    def getSelectionIndex(self):
        """
        Return the widget' selection-index.

        Returns:
            An integer representing the index the selection-index is at.
        """
        return self._selection_index

    def setSelection(self, selection_index, cursor):
        """
        Set the widget' selection between the given bounds.

        Args:
            selection_index: An integer (or known constant) representing the index the selection should start.
                This will be the position of the selection-index.
            cursor: An integer (or known constant) representing the index the selection should end.
                This will be the position of the cursor.
                The indices can actually be reversed (meaning the start-index is larger than the end-index)
                so that the cursor is at the start of the selection.

        Returns:
            Itsself (the widget) for convenience.
        """
        self._selection_index = self.getActualIndex(selection_index)
        self._cursor = self.getActualIndex(cursor)
        self.markDirty()
        return self

    def getSelection(self):
        """
        Return the widget' selection-range.

        Returns:
            A tuple (start, end) with the start- and end-index of the selection.
            This is not the selected content, only the indices of the range!
        """
        return self._sort(self.selection_index, self.cursor)

    def getActualIndex(self, index, constrain=True):
        """
        Return the actual index corresponding to the given representation.
        This converts known constants (e.g. END, CURSOR) to the corresponding integers.

        Args:
            index: An integer (or known constant) to be converted.
            constrain: A boolean indicating whether the given index should be constrained to
                valid indices for the content or not.
                The default value is True, meaning that the returned index is constrained.

        Returns:
            An integer representing the actual index the given value corresponds to.
        """
        if index == CURSOR:
            return self.cursor
        if index == END:
            return len(self.text)
        if index == SELECTION:
            return self.selection_index
        if constrain:
            return min(max(int(index), START), self.getActualIndex(END))
        return index

    def _indexToPos(self, index):
        """
        Return the relative coordinate (x, y) corresponding to the given index.

        This is an internal function.

        Args:
            index: An integer (or known constant) to be converted.

        Returns:
            A pair of integers (x, y) representing a relative coordinate.
        """
        return self.font.size(self.text[:self.getActualIndex(index)])[0], 0

    def _posToIndex(self, x, y):
        """
        Return the index corresponding to the given relative coordinate (x, y).

        This is an internal function.

        Args:
            x: An integer representing a relative x-coordinate.
            y: An integer representing a relative y-coordinate.

        Returns:
            An integer representing the index corresponding to the given relative coordinate.
        """
        length = len(self.text)
        x = min(float(x), (self.font.size(self.text[:-1])[0]
                           + self.font.size(self.text[-1:])[0] * 1.5))
        index = 0
        n = 0
        if self.text:
            for n in range(max(min(int(x / (self.font.size(self.text)[0] / length)), length - 1), 0), 0, -1):
                if self.font.size(self.text[:n])[0] + self.font.size(self.text[n])[0] < x:
                    break
            for index in range(n, length):
                if self.font.size(self.text[:index])[0] + (self.font.size(self.text[index])[0] * 1.5) > x:
                    break
            else:
                index += 1
        return index

    def _sort(self, i, j, constrain=True):
        """
        Return the indices in ascending order.

        This is an internal function.

        Args:
            i: An integer (or known constant) to sort.
            j: Another integer (or known constant) to sort.
            constrain: A boolean indicating whether the given indices should be constrained to
                valid indices for the content or not.
                The default value is True, meaning that the returned index is constrained.

        Returns:
            A tuple (min, max) of the numbers which have been sorted.
        """
        i = self.getActualIndex(i, constrain)
        j = self.getActualIndex(j, constrain)
        if i > j:
            return j, i
        return i, j

    def update(self, *args):
        """
        Additionally handles the selection and deletion of content.

        inherit_doc::
        """
        if len(args) > 0 and self.isActive() and self.isFocused():
            event = args[0]
            if event.type == pygame.KEYDOWN and self.isEditable():
                if event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                    if self.selection_index == self.cursor:
                        if event.key == pygame.K_DELETE:
                            self.delete(self.selection_index + 1, CURSOR)
                        else:
                            if self.delete(self.selection_index - 1, CURSOR):
                                self.moveCursor(-1)
                    else:
                        s, c = self._sort(SELECTION, CURSOR)
                        if self.delete(s, c):
                            self.setCursor(s)
            elif event.type == pygame.MOUSEMOTION:
                if (event.buttons[0] or event.buttons[2]) and self.rect.collidepoint(event.pos):
                    self.setSelection(SELECTION, self._posToIndex(event.pos[0] - self.rect.x, event.pos[1] - self.rect.y))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 3) and self.rect.collidepoint(event.pos):
                    self.setCursor(self._posToIndex(event.pos[0] - self.rect.x, event.pos[1] - self.rect.y))

        super(SelectionTextWidget, self).update(*args)

    editable = property(lambda obj: obj.isEditable(), lambda obj, arg: obj.setEditable(arg), doc="""The widget' status as a boolean whether its content is editable by the user.""")
    validation_function = property(lambda obj: obj.getValidation(), lambda obj, arg: obj.setValidation(arg), doc="""The widget's function used for validating change of its content.""")
    selection_overlay = property(lambda obj: obj.getSelectionOverlay(), lambda obj, arg: obj.setSelectionOverlay(arg), doc="""The widget's color to overlay for content that has been selected.""")
    selection_index = property(lambda obj: obj.getSelectionIndex(), lambda obj, arg: obj.setSelectionIndex(arg), doc="""The widget's index representing an endpoint for the range of selected content.""")
    cursor = property(lambda obj: obj.getCursor(), lambda obj, arg: obj.setCursor(arg), doc="""The widget's position of the cursor as a index. This is another endpoint for the range of selected content.""")
    selection = property(lambda obj: obj.getSelection(), lambda obj, tuple: obj.setSelection(*tuple), doc="""The widget's indices spanning the range of selected content.""")


# inherit docs from superclass
SelectionTextWidget = inherit_docstrings_from_superclass(SelectionTextWidget)
