from distutils.core import setup # Need this to handle modules
import py2exe 
import os
import sqlite3
from sqlite3 import Error
import win32con
import win32file
import xml.etree.ElementTree as ET


setup(console=['parser.py'],
      options={"py2exe":{"includes":["win32con","win32file"]}})