""" This file contains source code for synchronize any windows """
""" Mutex object with Mutex object created in python. """
""" This code basically use the win32 kernel Mutex APIs using wintypes """ 
""" I have added code snippet to test the funtionality """

import ctypes
from ctypes import wintypes
import time


""" 
Following three APIs CreateMutex, ReleaseMutex, and CloseHandle
used to perform activities to synchronize between processes
whether process is from C++ or C# .NET/CLR or Python
"""

# Define CreateMutex API attributes from win32
_CreateMutex = ctypes.windll.kernel32.CreateMutexA
_CreateMutex.argtypes = [wintypes.LPCVOID, wintypes.BOOL, wintypes.LPCSTR]
_CreateMutex.restype = wintypes.HANDLE

# Define ReleaseMutex API attributes from win32
_ReleaseMutex = ctypes.windll.kernel32.ReleaseMutex
_ReleaseMutex.argtypes = [wintypes.HANDLE]
_ReleaseMutex.restype = wintypes.BOOL

#Define CloseHandle API attributes from win32
_CloseHandle = ctypes.windll.kernel32.CloseHandle
_CloseHandle.argtypes = [wintypes.HANDLE]
_CloseHandle.restype = wintypes.BOOL

""" Waitforsingle API is used to wait for an event to occur """
#Define waitforsingleobject attribute from win32 
_WaitForSingleObject = ctypes.windll.kernel32.WaitForSingleObject
_WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
_WaitForSingleObject.restype = wintypes.DWORD


class mutexAcrossProcess:
    """A named, system-wide mutex that can be acquired and released."""

    def __init__(self, name, acquired=False):
        """Create named mutex with given name, also acquiring mutex if acquired is True.
        Mutex names are case sensitive, and a filename (with backslashes in it) is not a
        valid mutex name. Raises WindowsError on error.
        
        """
        self.name = name
        self.acquired = acquired
        ret = _CreateMutex(None, False, name)
        if not ret:
            raise ctypes.WinError()
        self.handle = ret
        if acquired:
            self.acquire()

    def acquire(self, timeout=None):
        """Acquire ownership of the mutex, returning True if acquired. If a timeout
        is specified, it will wait a maximum of timeout seconds to acquire the mutex,
        returning True if acquired, False on timeout. Raises WindowsError on error.
        
        """
        if timeout is None:
            # Wait forever (INFINITE)
            timeout = 0xFFFFFFFF
        else:
            timeout = int(round(timeout * 1000))
        ret = _WaitForSingleObject(self.handle, timeout)
        if ret in (0, 0x80):
            # Note that this doesn't distinguish between normally acquired (0) and
            # acquired due to another owning process terminating without releasing (0x80)
            self.acquired = True
            return True
        elif ret == 0x102:
            # Timeout
            self.acquired = False
            return False
        else:
            # Waiting failed
            raise ctypes.WinError()

    def release(self):
        """Relase an acquired mutex. Raises WindowsError on error."""
        ret = _ReleaseMutex(self.handle)
        if not ret:
            raise ctypes.WinError()
        self.acquired = False

    def close(self):
        """Close the mutex and release the handle."""
        if self.handle is None:
            # Already closed
            return
        ret = _CloseHandle(self.handle)
        if not ret:
            raise ctypes.WinError()
        self.handle = None

    __del__ = close

    def __repr__(self):
        """Return the Python representation of this mutex."""
        return '{0}({1!r}, acquired={2})'.format(
                self.__class__.__name__, self.name, self.acquired)

    __str__ = __repr__

    # Make it a context manager so it can be used with the "with" statement
    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()


# =============================================================================
# """ 
# Test Above Mutex class here 
# along with this process there is one more python file present on root 
# to perform synchronization between these two files 
# """
# 
# 
# if __name__ == '__main__':
#  #Create object here
#  evMutex = MutexAcrossProcess(b"ChangeMutexName")
#  print("Start while loop")
#  while True:
#      #Acquire Mutex object
#      evMutex.acquire()
#      #perform activities 
#      fo = open("foo.txt", "ab")
#      fo.write(b"0- ")
#      print("Test Mutex 1")
#      fo.close()  
#      #Release Mutex Object
#      evMutex.release()
#      time.sleep(1)    
#  print("End of while loop")
# 
# =============================================================================
