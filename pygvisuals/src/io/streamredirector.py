# -*- coding: cp1252 -*-

import io, time

class StreamRedirector(io.IOBase):

    """
    Manager for redirecting a stream to a callback-function
    """
    
    def __init__(self, stream, callback, usePrefix = True):
        """
        Initialisation of a StreamRedirector

        parameters:     object the stream to redirect
                        function a callback that recieves data as a string (single parameter)
                        boolean should a prefix be used
        return values:  -
        """
        self._usePrefix     = usePrefix
        self._buffer        = ""
        self._stream        = stream
        self._callback      = callback
    
    def getCurrentDate(self):
        """
        Return the current date of the system

        parameters:     -
        return values:  string the date in dd.mm.yyyy format
        """
        t = time.localtime(time.time())
        day = str(t[2])
        if len(day) == 1:
            day = "0" + day
        month = str(t[1])
        if len(month) == 1:
            month = "0" + month
        year = str(t[0])
        return day + "." + month + "." + year

    def getCurrentTime(self):
        """
        Return the current time of the system

        parameters:     -
        return values:  string the time in hh:mm:ss format
        """
        t = time.localtime(time.time())
        hour = str(t[3])
        if len(hour) == 1:
            hour = "0" + hour
        minute = str(t[4])
        if len(minute) == 1:
            minute = "0" + minute
        second = str(t[5])
        if len(second) == 1:
            second = "0" + second
        return hour + ":" + minute + ":" + second
    
    def close(self):
        """
        Close all streams

        parameters:     -
        return values:  -
        """
        self._stream.close()
    
    
    def flush(self):
        """
        Flush all streams

        parameters:     -
        return values:  -
        """
        self._stream.flush()
    
    def write(self, string):
        """
        Write to both the stream and the callback

        parameters:     string data to write
        return values:  -
        """
        try:
            self._buffer += string
            if "\n" in string:
                prefix = ""
                if self._usePrefix:
                    prefix = "[" + self.getCurrentTime() + "] "
                self._callback(prefix + self._buffer)
                self._buffer = ""
        except:
            pass
        return self._stream.write(string)
