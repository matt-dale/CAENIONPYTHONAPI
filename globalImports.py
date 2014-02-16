"""Setup and imports for all files"""

import os
import sys
import time
import datetime
import urllib
THISDIR = os.path.abspath(os.path.dirname(__file__))

sys.path.append(THISDIR)
sys.path.append(r'C:\Program Files\IronPython 2.7\Lib')
sys.path.append(os.path.join(THISDIR, 'resources'))

import clr
import System
