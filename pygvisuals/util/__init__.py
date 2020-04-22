"""
Package for useful functionalities not belonging to any other cathegory.
"""

__all__ = ["inherit_docstrings_from_superclass"]


import types
import re


def inherit_docstrings_from_superclass(cls, doc_inheritance_specifier="inherit_doc::"):
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
    This function, the functions it relies on included this file and
    its documentation are therefore licensed under the same license (Adapter's License).
    You can find a copy of this license here: https://creativecommons.org/licenses/by-sa/4.0/legalcode
    And a more readable summary here: https://creativecommons.org/licenses/by-sa/4.0/

    The doc_inheritance_specifier will be interpreted similar to a reStructuredText-directive.
    It will accept *one* the following parameters:
        description: Instead of replacing the specifier and this parameter with all of the superclass'
            __doc__-attribute, only the description above the sections ``Args`` and ``Returns`` will be copied.
        arguments: Instead of replacing the specifier and this parameter with all of the superclass'
            __doc__-attribute, only the section ``Args`` will be copied.
        return_values: Instead of replacing the specifier and this parameter with all of the superclass'
            __doc__-attribute, only the section ``Returns`` will be copied.
        all: Replaces the specifier and this parameter with all of the superclass' __doc__-attribute,
            same as if no parameter was given.
    Any replacement string from a superclass will have leading and trailing whitespace stripped off
    so it integrates seamlessly into existing docstrings.

    Args:
        cls: A class to modify.
        doc_inheritance_specifier: A string to search for in the __doc__-attributes of functions.
            If this string is found, it will be replaced with the found __doc__ from a superclass;
            the rest of the __doc__-attribute remains as before.
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
                        matches = _extract_inheritance_parameters_from_doc(func.__doc__, doc_inheritance_specifier)
                        sections = extract_sections_from_doc(superfunc.__doc__)
                        replaced_all = True
                        for match in matches:
                            parameter = match.group(1)
                            if not parameter:
                                parameter = "all"
                            if parameter in sections:
                                func.__doc__ = func.__doc__[:match.start()] + sections[parameter].strip() + func.__doc__[match.end():]
                            else:
                                replaced_all = False
                        if not replaced_all:
                            continue
                    else:
                        func.__doc__ = superfunc.__doc__
                    break
            else:
                if func.__doc__:
                    func.__doc__ = func.__doc__.replace(doc_inheritance_specifier, "")
    return cls


def extract_sections_from_doc(doc):
    """
    Extract sections from a given docstring.
    It will search for the following sections:
        description: the description above the sections ``Args`` and ``Returns``
        arguments: the section ``Args``
        return_values: the section ``Returns``
        all: all of the given docstring

    Args:
        doc: A (doc-)string to extract sections from.

    Returns:
        A dict with section-names as keys and their content as values.
    """
    sections = {"all": doc}
    index = 0

    def section_generator():
        last_index = -1
        possible = ("description", "arguments", "return_values")
        while index < len(possible):
            if last_index != index:
                sections[possible[index]] = []
                last_index = index
            yield possible[index]

    lines = doc.split("\n")
    for line, section in zip(lines, section_generator()):
        if line.strip() in ("Args:", "Returns:"):
            index += 1
        else:
            sections[section].append(line)

    return {key: "\n".join(value) if isinstance(value, list) else value for key, value in sections.items()}


def _extract_inheritance_parameters_from_doc(doc, doc_inheritance_specifier=None):
    """
    Return a iterator of Match-objects (from module re) with the span equal to the span of the "doc_inheritance-directive"
    and the group equal to the parameter. (If there was no parameter, the group is None.)

    This is an internal function.

    Args:
        doc: A (doc-)string to extract matches from.
        doc_inheritance_specifier: A string to search for in the doc-attribute.
            If this is a falsy value (e.g. None), the default value
            'inherit_doc::' will be used.

    Returns:
        The iterator with the Match-objects.
    """
    if not doc_inheritance_specifier:
        doc_inheritance_specifier = "inherit_doc::"
    pattern = re.compile("".join(map(lambda s: "[" + s + "]", doc_inheritance_specifier)) + "(?:[ ](\\S*))?", re.MULTILINE)
    return re.finditer(pattern, doc)
