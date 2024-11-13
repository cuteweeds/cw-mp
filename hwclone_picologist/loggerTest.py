import default-config
import machine
import utime
import os
"""Maintain rolling log file capped at LOG_FILESIZE_LIMIT bytes"""

# Drop the first line from a maxed-out LogFileName
def checkSize(LogFileName):
    """Checks LogFileName against maximum file size
    LOG_FILESIZE_MAX should be defined in main/config
    """
    global LOG_FILESIZE_MAX
    file_handle = open(LogFileName,"r")
    file_handle.seek(0,2)
    size = file_handle.tell()
    file_handle.close()

def dropFirst(LogFileName):
    """Rolls forward a specified file, dropping the first line and appending the last."""
    def wrapper(**args, **kwargs):
        tmpName = LogFileName + '.bak'
        with open (LogFileName, 'a') as readFrom, open (tmpName, 'w') as writeTo:
            readFrom.readline()
            for char in readFrom:
                writeTo.write(char)
                readFrom.close()
                writeTo.close()
                os.remove(LogFileName)
                os.rename(tmpName,LogFileName)
                #LED_FileWrite.value(0)
        return wrapper

def logLine():
    """appends line to LogFileName"""
    pass
    