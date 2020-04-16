# --- imports
# local imports
from .text_widget import TextWidget
from ..designs import getDefaultDesign, getFallbackDesign


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

    def __init__(self, x, y, width, height, text="", font=getDefaultDesign().font, selection_overlay=getDefaultDesign().selection_overlay):
        """
        Initialisation of a SelectionTextWidget.

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
            selection_overlay: A color-like object that can be interpreted as a color by pygame (such as a tuple with RGB values);
                this is used as an overlay for content that has been selected.
                The default value is the global default for the selection-color.
        """
        super(SelectionTextWidget, self).__init__(x, y, width, height, text, font)
        self._cursor = 0
        self._selection_index = 0
        self.selection_overlay = selection_overlay

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
        Set the widget's selection-index.

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
        Return the widget's selection-index.

        Returns:
            An integer representing the index the selection-index is at.
        """
        return self._selection_index

    def setSelection(self, selection_index, cursor):
        """
        Set the widget's selection between the given bounds.

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
        Return the widget's selection-range.

        Returns:
            A tuple (start, end) with the start- and end-index of the selection.
            This is not the selected content, only the indices of the range!
        """
        return self._sort(self.selection_index, self.cursor)

    def getActualIndex(self, index):
        """
        Return the actual index corresponding to the given representation.
        This converts known constants (e.g. END, CURSOR) to the corresponding integers.

        Args:
            index: An integer (or known constant) to be converted.

        Returns:
            An integer representing the actual index the given value corresponds to.
        """
        if index == CURSOR:
            return self.cursor
        if index == END:
            return len(self.text)
        if index == SELECTION:
            return self.selection_index
        return abs(int(index))

    def _indexToPos(self, index):
        """
        Return the relative x-coordinate corresponding to the given index

        This is an internal function.

        parameters:     int index given
        return values:  int relative x-coordinate
        """
        return self.font.size(self.text[:self.getActualIndex(index)])[0]

    def _posToIndex(self, x):
        """
        Return the index corresponding to the given relative x-coordinate

        This is an internal function.

        parameters:     int relative x-coordinate
        return values:  int index given
        """
        length = len(self.text)
        x = min(float(x), (self.font.size(self.text[:-1])[0] +
                           self.font.size(self.text[-1:])[0] * 1.5))
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

    def _sort(self, i, j):
        """
        Return the indices in ascending order.

        This is an internal function.

        Args:
            i: An integer (or known constant) to sort.
            j: Another integer (or known constant) to sort.

        Returns:
            A tuple (min, max) of the numbers which have been sorted.
        """
        i = self.getActualIndex(i)
        j = self.getActualIndex(j)
        if i > j:
            return j, i
        return i, j

    selection_overlay = property(getSelectionOverlay, setSelectionOverlay, doc="""The widget's color to overlay for content that has been selected.""")
    selection_index = property(getSelectionIndex, setSelectionIndex, doc="""The widget's index representing an endpoint for the range of selected content.""")
    cursor = property(getCursor, setCursor, doc="""The widget's position of the cursor as a index. This is another endpoint for the range of selected content.""")
    selection = property(getSelection, lambda obj, tuple: obj.setSelection(*tuple), doc="""The widget's indicies spanning the range of selected content.""")
