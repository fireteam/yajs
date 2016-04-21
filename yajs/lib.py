import os
import sys
import ctypes


if sys.platform == 'darwin':
    soname = 'libyajl.dylib'
else:
    soname = 'libyajl.so'


libpath = os.path.join(os.path.dirname(__file__), soname)
yajl = ctypes.CDLL(libpath)
