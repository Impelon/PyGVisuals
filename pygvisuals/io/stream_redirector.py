# --- imports
# preinstalled python libraries
import io
import time


class StreamRedirector(io.IOBase):

    """
    Class for redirecting a stream to a callback-function.
    Whenever a new line is written into the underlying stream, the callback-function will be called with the input.
    Any write-operation applied to a StreamRedirector will still also be fully applied to the underlying stream.
    """

    def __init__(self, stream, callback, timestampFormat="[%x %X] "):
        """
        Initialisation of a StreamRedirector.

        Args:
            stream: A stream-like object to redirect from.
            callback: A callback-function that recieves data as a string (single parameter).
            timestampFormat: A string for formating a timestamp that will be prefixed to each data-string for the callback-function only.
                The format will be interpreted via time.strftime(timestampFormat); default is '[%x %X] '.
                If an empty string or any falsy expression is supplied, no prefix will be produced.
        """
        super(StreamRedirector, self).__init__()
        self._timestampFormat = timestampFormat
        self._buffer = ""
        self._stream = stream
        self._callback = callback

    @property
    def closed(self):
        """
        True if the underlying stream is closed.
        """
        return self._stream.closed

    def close(self):
        """
        Close the underlying stream and flush the current buffer.
        """
        self.flush()
        self._stream.close()

    def flush(self):
        """
        Flush the underlying stream and the current buffer.
        """
        while "\n" in self._buffer:
            self._writeline()
        self._writeline()
        if not self.closed:
            self._stream.flush()

    def read(self, *args):
        """
        Raise io.UnsupportedOperation as this stream-like object can not be read from.
        """
        raise io.UnsupportedOperation("read")

    def writable(self):
        """
        Return True as this stream-like object is writable.
        """
        return True

    def write(self, input):
        """
        Write to the underlying stream.
        If a new line is found also call the callback-function with every line.

        Args:
            input: An appropiate object for the underlying stream to write.
        """
        try:
            self._buffer += input
            while "\n" in self._buffer:
                self._writeline()
        except:
            pass
        return self._stream.write(input)

    def _writeline(self):
        """
        Call the callback-function with a single line from the buffer.
        If the buffer has no line-endings the entire content of the buffer will be supplied as data to the callback-function.
        This also prepends the timestamp-prefix if needed.
        This is an internal function.
        """
        if self._buffer:
            splitted = self._buffer.split("\n", 1)
            data = splitted[0]
            if len(splitted) > 1:
                self._buffer = splitted[1]
            else:
                self._buffer = ""
            if self._timestampFormat:
                data = time.strftime(self._timestampFormat) + data
            self._callback(data)
