# -*- coding: cp1252 -*-

import time

class StreamRedirector():

    """
    Manager for redirecting a stream to a insertable object
    """
    
    def __init__(self, stream, insertable, usePrefix = True):
        """
        Initialisation of a StreamRedirector

        parameters:     object the stream to redirect
                        object the object to insert the contents of the stream to
                        boolean should a prefix be used
        return values:  -
        """
        self._usePrefix     = usePrefix
        self._buffer        = ""
        self._stream        = stream
        self._insertable    = insertable
    
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
    
    def write(self, string):
        """
        Write to both the stream and the object

        parameters:     string data to write
        return values:  -
        """
        try:
            self._buffer += string
            if "\n" in string:
                prefix = ""
                if self._usePrefix:
                    prefix = "[" + self.getCurrentTime() + "] "
                self._insertable.insert(1, prefix + self._buffer)
                self._buffer = ""
        except:
            pass
        return self._stream.write(string)
