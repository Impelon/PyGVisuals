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
                if a attribute was not found for this design.
                This will also be used when applying the design to widgets.
                If this is a falsy value (e.g. None), there will be no fallback-design.
            **kwargs: Any key-value-pairs to add to this design's attributes.
        """
        super(Design, self).__init__()
        self._fallback = fallback
        self.__dict__.update(kwargs)

    def __getattr__(self, name):
        """
        In case there is a fallback-design defined,
        ask it for an undefinded attribute (by calling getattr() on it).
        Otherwise behaves like the base implementation.

        inherit_doc::
        """
        if self._fallback:
            return getattr(self._fallback, name)
        return getattr(super(Design, self), name)

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
        for source in (self, self._fallback):
            for name, value in vars(source).items():
                try:
                    if hasattr(widget, name):
                        setattr(widget, name, value)
                except:
                    pass


# inherit docs from superclass
Design = inherit_docstrings_from_superclass(Design)
