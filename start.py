import os
import sys
PATH =os.path.dirname(sys.modules['__main__'].__file__) # Get the path of the current file
if(PATH==""):
    PATH = "."
try:
    os.mkdir(PATH+"/.users")
except:
    pass
try:
    os.mkdir(PATH+"/.tmp")
except:
    pass
try:
    os.mkdir(PATH+"/.user/admin")
except:
    pass