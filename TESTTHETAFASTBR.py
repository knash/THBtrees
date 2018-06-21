#! /usr/bin/env python
import re
import os
import subprocess
from os import listdir
from os.path import isfile, join
import glob
import copy
import math
import ROOT
from ROOT import *
import sys
from DataFormats.FWLite import Events, Handle
from optparse import OptionParser


#Load up cut values based on what selection we want to run 

commands = []

templ = "python TESTTHETA.py -S cslim -R center" 

for iii in xrange(1,11):
		commands.append(templ+" -B "+str(float(iii)/10.)+" -T "+str(1.0-float(iii)/10.)+" &")

for s in commands :
    print 'executing ' + s
    subprocess.call( [s], shell=True )





