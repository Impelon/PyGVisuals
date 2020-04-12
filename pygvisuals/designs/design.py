# --- imports
# local imports
from ..util import inherit_docstrings_from_superclass


class Design(object):

    """
    Class implementing a design template for applications with widgets.
    """

    def __init__(self, fallback=None, **kwargs):
        """
        Initialisation of a Design.
        Designs bundle named attributes (just like any object) which can be accessed directly.

        It includes methods to 'apply' the design to widgets.
        For any defined attribute in the design it will try to write it to given widgets,
        if the widget has that attribute (via hasattr(), setattr()).

        Args:
            fallback: An object with readable attributes to be used,
                if an attribute was not found for this design.
                This will also be used when applying the design to widgets.
                If this is a falsy value (e.g. None), there will be no fallback-design.
            **kwargs: Any key-value-pairs to add to this design's attributes.
        """
        super(Design, self).__init__()
        self.fallback = fallback
        self.__dict__.update(kwargs)

    def __getattr__(self, name):
        """
        In case there is a fallback-design defined,
        ask it for an undefinded attribute (by calling getattr() on it).
        Otherwise behaves like the base implementation.

        inherit_doc::
        """
        if self.fallback:
            return getattr(self.fallback, name)
        return getattr(super(Design, self), name)

    def __copy__(self):
        """
        Create a shallow copy of this design.

        Returns:
            A new design-instance with the same attributes and fallback as this design.
        """
        return type(self)(self.fallback, **vars(self))

    def copy(self):
        """
        This calls the underlying __copy__-function.
        """
        return self.__copy__()
    # copy doc from __copy__-function
    copy.__doc__ += __copy__.__doc__

    def applyToWidgets(self, widgets):
        """
        Apply this design to the supplied widgets.
        For any defined attribute in the design, this will try to write it to given widgets,
        if the widget has that attribute (via hasattr(), setattr()).

        Args:
            widgets: An iterable of widgets to apply the designs to.
        """
        for widget in widgets:
            self.applyToWidget(widget)

    def applyToWidget(self, widget):
        """
        Apply this design to the supplied widget.
        For any defined attribute in the design, this will try to write it to given widget,
        if the widget has that attribute (via hasattr(), setattr()).

        Args:
            widgets: A widgets to apply the design to.
        """
        for source in (self, self.fallback):
            try:
                for name, value in vars(source).items():
                    try:
                        if hasattr(widget, name):
                            setattr(widget, name, value)
                    except: pass
            except: pass


# inherit docs from superclass
Design = inherit_docstrings_from_superclass(Design)
