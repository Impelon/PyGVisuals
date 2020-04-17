# --- imports
# pygame imports
import pygame
import pygame.sprite

# local imports
from ..borders import ColoredBorder, Border
from ..designs import getDefaultDesign, getFallbackDesign

# set defaults
getFallbackDesign().border = ColoredBorder(2, 2, (50, 50, 50))
"""Border to be used by default."""
getFallbackDesign().foreground = (255, 255, 255)
"""Color to be used by default for the foreground of a widget."""
getFallbackDesign().background = (100, 100, 100)
"""Color to be used by default for the background of a widget."""
getFallbackDesign().disabeled_overlay = (200, 200, 200, 200)
"""Color used by default to overlay when a widget is disabled."""
getFallbackDesign().scaling_function = pygame.transform.smoothscale
"""Function used to scale background images to widget-size."""

def _getScalingFunctionForSmoothness(self, smooth):
    """
    Return an appropiate scaling-function for the smoothness given.

    This is an internal function.

    Args:
        smooth: A boolean indicating whether the returned function should scale smoothly or not.

    Returns:
        A corresponding scaling-function which transforms a given surface (see pygame.transform.scale).
    """
    if smooth:
        return pygame.transform.smoothscale
    return pygame.transform.scale

class Widget(pygame.sprite.DirtySprite):

    """
    Underlying class for interactive GUI-objects with pygame;
    intended for use together with pygame.sprite.LayeredDirty.

    Note: If you change any widget's visual characteristics (e.g. its background-color)
    via its methods or properties (e.g. setBackground()),
    its appearance will not change until it is redrawn.
    You can force this by calling widget.update() after you modified its characteristics.
    """

    def __init__(self, x, y, width, height):
        """
        Initialisation of a basic Widget.
        The units for the following lengths are pixel.

        Args:
            x: An integer specifing the x-coordinate of the widget.
                This is the horizontal distance from the left reference point.
            y: An integer specifing the y-coordinate of the widget.
                This is the vertical distance from the top reference point.
            width: An integer specifing the width of the widget.
            height: An integer specifing the height of the widget.
        """
        super(Widget, self).__init__()
        self._focused = False
        self._active = True
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self.bounds = self.image.get_rect().move(x, y)
        self.border = getDefaultDesign().border
        self.foreground = getDefaultDesign().foreground
        self.background = getDefaultDesign().background
        self.background_image = None
        self.disabeled_overlay = getDefaultDesign().disabeled_overlay
        self.scaling_function = getDefaultDesign().scaling_function
        self._updateRect()

    def markDirty(self, overwriteDirtyForever=False):
        """
        Mark the widget as dirty and therefore to be redrawn in the next draw-cycle.

        Args:
            overwriteDirtyForever: A boolean indicating whether this should overwrite the dirty-forever state.
                The default is False meaning that a widget which is marked as dirty-forever
                will not be clean after the next cycle when this method was called on it.
        """
        if not self.isDirtyForever() or overwriteDirtyForever:
            self.dirty = 1

    def markDirtyForever(self):
        """
        Mark the widget as constantly dirty and therefore to be redrawn periodically with every draw-cycle.
        """
        self.dirty = 2

    def markClean(self):
        """
        Mark the widget as clean and therefore not to be redrawn in the next draw-cycle.
        """
        self.dirty = 0

    def isDirty(self):
        """
        Return if the widget is dirty and will be redrawn in the next draw-cycle.
        """
        return self.dirty >= 1

    def isDirtyForever(self):
        """
        Return if the widget is constantly dirty and will be redrawn periodically with every draw-cycle.
        """
        return self.dirty >= 2

    def setVisible(self, visible):
        """
        Set the widget's visibility.
        Invisible widgets will not be drawn and are inactive.

        Args:
            visible: A boolean indicating whether the widget should be visible.

        Returns:
            Itsself (the widget) for convenience.
        """
        visible = bool(visible)
        if self.visible != visible:
            self.visible = visible
            self.setActive(visible)
        return self

    def isVisible(self):
        """
        Return whether the widget is visible.
        Invisible widgets will not be drawn and are inactive.

        Returns:
            A boolean indicating whether the widget is declared visible.
        """
        return self.visible

    def setFocused(self, focused):
        """
        Set whether the widget is focused.

        A widget will be focused automatically if it is clicked on.
        Although the default implementation does not process this information,
        subclasses may use this information to determine if the user-interaction
        was meant to be processed by them or not.

        Args:
            visible: A boolean indicating whether the widget should be focused.

        Returns:
            Itsself (the widget) for convenience.
        """
        focused = bool(focused)
        if self.focused != focused:
            self._focused = focused
            self.markDirty()
        return self

    def isFocused(self):
        """
        Return whether the widget is focused.
        A widget will be focused automatically if it is clicked on.

        Returns:
            A boolean indicating whether the widget is declared focused.
        """
        return self._focused

    def setActive(self, active):
        """
        Set the widget as active and therefore as interactive.
        An inactive widget should not be interactable and will have an overlay painted on.

        Args:
            active: A boolean indicating whether the widget should be active

        Returns:
            Itsself (the widget) for convenience.
        """
        active = bool(active)
        if self.active != active:
            self._active = active
            self.markDirty()
            self.update()
        return self

    def isActive(self):
        """
        Return whether the widget is active.
        An inactive widget should not be interactable and will have an overlay painted on.

        Returns:
            A boolean indicating whether the widget is active.
        """
        return self._active

    def setBounds(self, rect):
        """
        Set the widget's base bounds according to a pygame.Rect.
        This can be used to change the position of the widget or its size.

        Args:
            rect: A pygame.Rect with the according position and size.

        Returns:
            Itsself (the widget) for convenience.
        """
        self._bounds = rect
        self.markDirty()
        return self

    def getBounds(self):
        """
        Return the widget's base bounds (position and size).

        Returns:
            A pygame.Rect with the bounds of the widget.
        """
        return self._bounds

    def getActualBounds(self):
        """
        Return the widget's actual bounds (position and size).

        Returns:
            A pygame.Rect with the bounds of the widget.
        """
        return self._rect

    def setBorder(self, border):
        """
        Set the widget's border.

        Args:
            border: A PyGVisuals-border to be set.
                If this is a falsy value a empty border will be used.

        Returns:
            Itsself (the widget) for convenience.
        """
        if not border:
            border = Border(0, 0)
        if isinstance(border, Border):
            self._border = border
            self.markDirty()
        return self

    def getBorder(self):
        """
        Return the widget's border.

        Returns:
            A PyGVisuals-border belonging to the widget.
        """
        return self._border

    def setForeground(self, color):
        """
        Set the widget's foreground-color (not used by basic implementation).

        Args:
            color: A color-like object that can be interpreted as a color by pygame (such as a tuple with RGB values).

        Returns:
            Itsself (the widget) for convenience.
        """
        self._foreground = color
        self.markDirty()
        return self

    def setBackground(self, color):
        """
        Set the widget's background-color.

        Args:
            color: A color-like object that can be interpreted as a color by pygame (such as a tuple with RGB values).

        Returns:
            Itsself (the widget) for convenience.
        """
        self._background = color
        self.markDirty()
        return self

    def getForeground(self):
        """
        Return the widget's foreground-color (not used by basic implementation).

        Returns:
            A color-like object that represents the widget's foreground color.
        """
        return self._foreground

    def getBackground(self):
        """
        Return the widget's background-color.

        Returns:
            A color-like object that represents the widget's background color.
        """
        return self._background

    def setBackgroundImage(self, image, smooth=None, scale_immediately=False):
        """
        Set the widget's background-image.

        Args:
            image: A surface-like object (e.g. pygame.Surface) that should be rendered as the background.
                If this is a falsy value (e.g. None), there will be no background-image.
            smooth: A boolean indicating whether the image should be scaled smoothly or not.
                If this is None, the previous value will not be overwritten.
                The default value is None, so the previous configuration will be kept.
            scale_immediately: A boolean indicating whether the image should be scaled during this assignment.
                Usually the image is rescaled every time the widget is drawn.
                This is especially useful when the scaling-function is set to None
                since the image will only be resized once during this assignment therefore increasing performance.
                The default value is False, so the image will not be rescaled in this assignment which preserves image quality.

        Returns:
            Itsself (the widget) for convenience.
        """
        if image:
            self._background_image = image.convert_alpha(self._getAppearance())
            if smooth is None:
                smooth = self.smooth_scaling
            self.smooth_scaling = smooth
            if scale_immediately:
                scaling_function = self.scaling_function
                if not scaling_function:
                    scaling_function = _getScalingFunctionForSmoothness(smooth)
                self._background_image = scaling_function(self._background_image, self.bounds.size)
        else:
            self._background_image = image
        self.markDirty()
        return self

    def getBackgroundImage(self):
        """
        Return the widget's background-image.
        A falsy value (e.g. None) indicates that there is no background-image to be drawn.

        Returns:
            A surface-like object that is rendered in the background of the widget
            or a falsy value indicating that there is no such surface.
        """
        return self._background_image

    def setDisabeledOverlay(self, color):
        """
        Set the widget's color to overlay when it is disabled.

        Args:
            color: A color-like object that can be interpreted as a color by pygame (such as a tuple with RGB values).

        Returns:
            Itsself (the widget) for convenience.
        """
        self._disabeled_overlay = color
        self.markDirty()
        return self

    def getDisabeledOverlay(self):
        """
        Return the widget's color which is overlayed when it is disabled.

        Returns:
            A color-like object that represents the widget's disabeled color.
        """
        return self._disabeled_overlay

    def setSmoothScaling(self, smooth):
        """
        Set whether the widget's background-image will be scaled smoothly (with pygame.transform.smoothscale) or not.
        For more control see the widget's 'scaling_function' property.

        Args:
            smooth: A boolean indicating whether the image should be scaled smoothly or not.

        Returns:
            Itsself (the widget) for convenience.
        """
        smooth = bool(smooth)
        if smooth != self.smooth_scaling:
            self.scaling_function = _getScalingFunctionForSmoothness(smooth)
            self.markDirty()
        return self

    def hasSmoothScaling(self):
        """
        Return whether the background-image is known to be scaled smoothly or not.

        Returns:
            A boolean indicating whether the scaling-function is pygame.transform.smoothscale
            and the background-image is therefore scaled smoothly.
        """
        return self._scaling_function is pygame.transform.smoothscale

    def setScalingFunction(self, scaling_function):
        """
        Set the scaling-function used for scaling the background-image (to the widgets bounds).

        Args:
            scaling_function: A function that scales a given surface-like object
                to a given size. See for example pygame.transform.scale.
                If this is a falsy value (e.g. None), the image will not be rescaled when drawn.

        Returns:
            Itsself (the widget) for convenience.
        """
        self._scaling_function = scaling_function
        self.markDirty()
        return self

    def getScalingFunction(self):
        """
        Return the scaling-function used for scaling the background-image (to the widgets bounds).

        Returns:
            A function that scales a given surface-like object to a given size (like pygame.transform.scale)
            or a falsy value (e.g. None) if the background-image is not rescaled when drawn.
        """
        return self._scaling_function

    def update(self, *args):
        """
        Perform any updates on the widget if needed.

        This is a basic implementation of focus, active-state and border-rendering;
        used for interaction in more advanced widget-classes.

        Args:
            *args: Any argument needed for the update. This can include an optional pygame.event.Event to process.
        """
        if self.isActive() and len(args) > 0:
            event = args[0]
            if event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 2, 3):
                self.setFocused(self.rect.collidepoint(event.pos))
        if self.isDirty():
            self._updateRect(*args)
            self.image = self._getAppearance(*args)
            if not self.isActive():
                inactive = pygame.Surface(self.image.get_rect().size, 0, self.image)
                inactive.fill(self.disabeled_overlay)
                self.image.blit(inactive, (0, 0))
            self.image = self.border.getBorderedImage(self.image)

    def _updateRect(self, *args):
        """
        Update the actual position and size of the widget.
        This is an internal function.

        Args:
            *args: Any argument needed for the update. This can include an optional pygame.event.Event to process.
        """
        self._rect = self.border.getBounds(self.bounds)

    def _getAppearance(self, *args):
        """
        Return the underlying widget's appearance.

        This is an internal function.

        This includes a basic implementation of background-coloring and display of background-image.

        Args:
            *args: Any argument needed for the update. This can include an optional pygame.event.Event to process.

        Returns:
            The underlying widget's appearance as a pygame.Surface.
        """
        surface = pygame.Surface(self.bounds.size, pygame.SRCALPHA)
        surface.fill(self.background)
        if self.background_image:
            background_image = self.background_image
            if self._scaling_function:
                background_image = self._scaling_function(self.background_image, self.bounds.size)
            surface.blit(background_image, (0, 0))

        return surface

    foreground = property(lambda obj: obj.getForeground(), lambda obj, arg: obj.setForeground(arg), doc="The widget's foreground color.")
    background = property(lambda obj: obj.getBackground(), lambda obj, arg: obj.setBackground(arg), doc="The widget's background color.")
    background_image = property(lambda obj: obj.getBackgroundImage(), lambda obj, arg: obj.setBackgroundImage(arg), doc="""The widget's background-image.
        If this is a falsy value (e.g. None), no image will be drawn.""")
    disabeled_overlay = property(lambda obj: obj.getDisabeledOverlay(), lambda obj, arg: obj.setDisabeledOverlay(arg), doc="The widget's color to overlay when it is disabled.")
    smooth_scaling = property(lambda obj: obj.hasSmoothScaling(), lambda obj, arg: obj.setSmoothScaling(arg), doc="The widget' status as a boolean "
        """regarding whether the background-image will be scaled smoothly (with pygame.transform.smoothscale).
        Exact control of the scaling-function is given via the 'scaling_function' property.""")
    scaling_function = property(lambda obj: obj.getScalingFunction(), lambda obj, arg: obj.setScalingFunction(arg), doc="The widget's function used "
        """for scaling the background-image (to the widgets bounds).
        If this is a falsy value (e.g. None), the image will not be rescaled when drawn.""")
    border = property(lambda obj: obj.getBorder(), lambda obj, arg: obj.setBorder(arg), doc="The widget's border (a PyGVisuals' border).")
    bounds = property(lambda obj: obj.getBounds(), lambda obj, arg: obj.setBounds(arg), doc="The widget's base position and size as a pygame.Rect.")
    rect = property(lambda obj: obj.getActualBounds(), doc="The widget's actual position and size as a pygame.Rect.")
    active = property(lambda obj: obj.isActive(), lambda obj, arg: obj.setActive(arg),doc="""The widget's active status as a boolean.
        An inactive widget will should not respond to user-input and will have a grey overlay.""")
    focused = property(lambda obj: obj.isFocused(), lambda obj, arg: obj.setFocused(arg), doc="""The widget's focus status as a boolean.
        A widget will be focused automatically if it is clicked on.""")
