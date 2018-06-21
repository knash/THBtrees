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
parser = OptionParser()
parser.add_option('-c', '--cuts', metavar='F', type='string', action='store',
                  default	=	'default',
                  dest		=	'cuts',
                  help		=	'Cuts type (ie default, rate, etc)')
(options, args) = parser.parse_args()

cuts = options.cuts

import WprimetoVlq_Functions	
from WprimetoVlq_Functions import *
WPF = WprimetoVlq_Functions(options.cuts)
Cons = WPF.LoadConstants
#Load up cut values based on what selection we want to run 

lumi = Cons['lumi']
kfac = Cons['kfac']
xsec_wpr = Cons['xsec_wpr']
xsec_ttbar = Cons['xsec_ttbar']
xsec_qcd = Cons['xsec_qcd']
xsec_st = Cons['xsec_st']
nev_wpr = Cons['nev_wpr']
nev_ttbar = Cons['nev_ttbar']
nev_qcd = Cons['nev_qcd']
nev_st = Cons['nev_st']


commands = []

commands.append('rm logs/o*.log')
commands.append('mv o*.log logs/')
commands.append('rm TTrees/*.root')  
commands.append('mv THBttree*.root TTrees/')  
commands.append('rm /eos/uscms/store/user/knash/TTrees/*.root')  
commands.append('xrdcp -r --force TTrees/ root://cmseos.fnal.gov///store/user/knash/TTrees') 
for s in commands :
    print 'executing ' + s
    subprocess.call( [s], shell=True )

print "Complete"

