import sys

def bind_clipboard():
    """
    If the copy and paste functions are not bound this tries to bind them to appropriate functions.
    """
    global copy, paste
    if is_bound():
        return
    try:
        import pyperclip
        pyperclip.paste()
        paste = pyperclip.paste
        copy = pyperclip.copy
        return
    except:
        pass
    try:
        import pygame.scrap
        from pygame.locals import SCRAP_CLIPBOARD, SCRAP_TEXT
        pygame.scrap.init()
        default_encoding = "ascii"
        try:
            default_encoding = sys.getdefaultencoding()
        except:
            pass

        modes = ("strict", "replace", "ignore")

        def robust_paste():
            pygame.scrap.set_mode(SCRAP_CLIPBOARD)
            return_value = None
            encodings = ("utf8", "latin1", default_encoding)
            types = ("text/plain;charset=utf-8", "UTF8_STRING", "COMPOUND_TEXT", "TEXT", "STRING", SCRAP_TEXT)
            for mode in modes:
                for encoding in encodings:
                    for type in types:
                        try:
                            return_value = pygame.scrap.get(type)
                            if return_value:
                                return return_value.decode(encoding, mode)
                        except:
                            pass
            return return_value
        robust_paste.__doc__ = pygame.scrap.get.__doc__

        def robust_copy(text):
            pygame.scrap.set_mode(SCRAP_CLIPBOARD)
            return_value = None
            encodings = ("ascii", default_encoding, "latin1", "utf8")
            for mode in modes:
                for encoding in encodings:
                    try:
                        return_value = pygame.scrap.put(SCRAP_TEXT, text.encode(encoding, mode))
                        return return_value
                    except:
                        pass
            return return_value
        robust_copy.__doc__ = pygame.scrap.put.__doc__
        copy = robust_copy
        paste = robust_paste
        return
    except:
        pass

def is_bound():
    """
    Returns whether the copy and paste functions are bound to appropriate functions.
    """
    return copy != late_bind_copy and paste != late_bind_paste

def late_bind_copy(*args, **kwargs):
    """
    Try to copy a given text to the clipboard.

    This is a helper-funtion. While is_bound() is False this will return None.
    Otherwise an appropriate function has been found and it is executed.
    During the first successful execution (is_bound() is True) this function be replaced by
    the appropriate function.
    """
    bind_clipboard()
    if is_bound():
        return copy(*args, **kwargs)
    return None


def late_bind_paste(*args, **kwargs):
    """
    Try to paste a given text to the clipboard.

    This is a helper-funtion. While is_bound() is False this will return None.
    Otherwise an appropriate function has been found and it is executed.
    During the first successful execution (is_bound() is True) this function be replaced by
    the appropriate function.
    """
    bind_clipboard()
    if is_bound():
        return paste(*args, **kwargs)
    return None


copy = late_bind_copy
paste = late_bind_paste
