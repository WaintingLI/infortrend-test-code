import sys
import os



#獲得當前工作路徑
print( os.getcwd())

print('sys.argv[0] =', sys.argv[0])
pathname = os.path.dirname(sys.argv[0])
print('path =', pathname,bool(pathname))
print('full path =', os.path.abspath(pathname))
