"""
Package providing design templates for applications with widgets.
"""

__all__ = ["setDefaultDesign", "getDefaultDesign", "getFallbackDesign",
           "getDesignRegister", "registerDesign", "getRegisteredDesign"]

from .design import Design

__fallback_design = Design()
"""
The fallback-design to be used as fallback for all default-designs.
Widgets should define design-attributes with a default here by asigning a value to a new attribute.
"""
__default_design = Design(fallback=__fallback_design)
"""
The default-design to be used for defaults for all widgets.
"""
__design_register = {}

def setDefaultDesign(design):
    """
    Set the default-design to a copy of the given design.
    The fallback will be replaced by an internal fallback.

    Args:
        design: A PyGVisuals-design to set as default.
    """
    global __default_design
    design = design.copy()
    design.fallback = __fallback_design
    __default_design = design


def getDefaultDesign():
    """
    Return the default-design to be used for defaults for all widgets.

    Returns:
        A PyGVisuals-design that is being used as default.
    """
    return __default_design


def getFallbackDesign():
    """
    Return the fallback-design to be used as fallback for all default-designs.

    Widgets should define design-attributes with a default here by asigning a value to a new attribute.
    e.g.:
    getFallbackDesign().attribute = value

    Returns:
        A PyGVisuals-design that is being used as fallback.
    """
    return __fallback_design


def getDesignRegister():
    """
    Return a copy of the design-register.
    As the register is a dict, this can be used to list all available designs, e.g.:
    getDesignRegister().items()

    Returns:
        A dict which represents the design-register.
    """
    return __design_register.copy()

def registerDesign(name, design):
    """
    Register a design in the design-register.

    Args:
        name: A string to use as a reference/name for the design in the register.
        design: The design to register.
    """
    global __design_register
    __design_register[str(name)] = design

def getRegisteredDesign(name):
    """
    Return a design from the design-register by its reference.

    Args:
        name: A string used as a reference/name for the design in the register.
    """
    return __design_register[str(name)]

# register some hardcoded designs
registerDesign("default", __fallback_design)

from . import hardcoded_designs

for name, value in vars(hardcoded_designs).items():
    if isinstance(value, Design):
        registerDesign(name, value)
