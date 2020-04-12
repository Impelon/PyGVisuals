"""
Package for useful functionalities not belonging to any other cathegory.
"""

__all__ = ["inherit_docstrings_from_superclass"]


import types

def inherit_docstrings_from_superclass(cls, doc_inheritance_specifier = "inherit_doc::"):
    """
    Add docstrings for methods of the class from its superclasses and return it.

    Every function from the given class without a __doc__-attribute or with
    a __doc__-attribute containing the given specifier will get a copy of
    a __doc__-attribute from a function with the same name from one of its superclasses.

    This can be used as a decorator.

    This function was taken and modified from the 'Stack Overflow' network.
    The original author is Raymond Hettinger.
    - original source: https://stackoverflow.com/a/8101598
        answered by: Raymond Hettinger (https://stackoverflow.com/users/1001643/raymond-hettinger)
    - original question: https://stackoverflow.com/q/8100166
        asked by: Fred Foo (https://stackoverflow.com/users/166749/fred-foo)

    The original is licensed under Creative Commons Attribution-Share Alike.
    This function and its documentation are therefore licensed under the same license (Adapter's License).
    You can find a copy of this license here: https://creativecommons.org/licenses/by-sa/4.0/legalcode
    And a more readable summary here: https://creativecommons.org/licenses/by-sa/4.0/

    Args:
        cls: A class to modify.
        doc_inheritance_specifier: A string to search for in the __doc__-attributes of functions.
            If this string is found, it will be replaced with the found __doc__ from a superclass;
            the rest of the __doc__ attribute remains as before.
            If this is a falsy value (e.g. None), no such specifier will be searched for;
            instead only functions without a __doc__ attribute will inherit docstrings from superclasses.

    Returns:
        The class supplied (with the modifications made).
    """
    for name, func in vars(cls).items():
        if isinstance(func, types.FunctionType):
            if func.__doc__ and (not doc_inheritance_specifier or doc_inheritance_specifier not in func.__doc__):
                continue
            try:
                superclasses = cls.__mro__[1:]
            except:
                superclasses = cls.__bases__
            for supercls in superclasses:
                superfunc = getattr(supercls, name, None)
                if superfunc and getattr(superfunc, "__doc__", None):
                    if func.__doc__:
                        func.__doc__ = func.__doc__.replace(doc_inheritance_specifier, superfunc.__doc__)
                    else:
                        func.__doc__ = superfunc.__doc__
                    break
            else:
                if func.__doc__:
                    func.__doc__ = func.__doc__.replace(doc_inheritance_specifier, "")
    return cls
