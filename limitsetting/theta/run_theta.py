# !/bin/python
import subprocess
import glob
import copy
import re
import sys
import os
from optparse import OptionParser


parser = OptionParser()

parser.add_option('--file', metavar='F', type='string', action='store',
                  dest='file',
                  default='analysis_quick_limits.py',
                  help='analysis file')

(options, args) = parser.parse_args()

argv = []

commands = [
    'cp  ' + options.file +' ./analysis.py',
    './utils2/theta-auto.py',
    ]

for s in commands :
    print 'executing ' + s
    subprocess.call( [s], shell=True )
#os.chdir(retval )
