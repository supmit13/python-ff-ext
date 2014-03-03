# This file defines the constants used in savewhatyoulookedat server side python code. The files that use the 
# constants defined here are handlers.py and forms.py (as on 11th Dec, 2009). The constants defined here are 
# grouped on the basis of the type of data they represent. At present, there are 4 groups (more may be added
# later on). These are "Path related constants", "Database related constants" ,"Filetype/File extension related
# constants" and "Logging/Error messages related constants". More constants may be added to each group later on.
#
# -- Supriyo.


import os
import sys
import re
# Path related constants:
USER_ROOT_DIR = "/home/supmit/work/odesk/PythonFirefoxExtn/users/"
LOG_PATH = "logs" # Can be relative. If the path starts with a forward slash or a character followed by a colon, then it is absolute path. Otherwise it is relative to the location of the caller file.
WEB_HOST = "192.168.228.1:8000"

# Database related constants:
DB_USERID = "root"
DB_PASSWD = "spmprx"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_SCHEMA_NAME = "urldb"
DB_DRIVER = "MySQLdb"

# Image file type patterns:
JPGPAT = re.compile("\.jpe?g$")
GIFPAT = re.compile("\.gif$")
PNGPAT = re.compile("\.png$")
BMPPAT = re.compile("\.bmp$")
TIFFPAT = re.compile("\.tiff?$")

EMAILPAT = re.compile("\s(\w+[\.\w]*\@\w+\.\w+[\.\w]{0,})")

# Error/Logging related constants:
DEBUG = 1
LOG_LEVEL = 5

