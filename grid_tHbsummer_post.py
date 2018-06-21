#! /usr/bin/env python
import re
import os
import subprocess
from os import listdir
from os.path import isfile, join
import glob
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
parser.add_option('-t', '--atype', metavar='F', type='string', action='store',
                  default	=	'analyzer',
                  dest		=	'atype',
                  help		=	'')
(options, args) = parser.parse_args()

cuts = options.cuts

import WprimetoVlq_Functions
from WprimetoVlq_Functions import *

WPF = WprimetoVlq_Functions(options.cuts)


#Load up cut values based on what selection we want to run 
Cons = WPF.LoadConstants
lumi = Cons['lumi']
kfac = Cons['kfac']
xsec_wpr = Cons['xsec_wpr']
#xsec_wpl = Cons['xsec_wpl']
#xsec_wplr = Cons['xsec_wplr']
xsec_ttbar = Cons['xsec_ttbar']
xsec_qcd = Cons['xsec_qcd']
xsec_st = Cons['xsec_st']
nev_wpr = Cons['nev_wpr']
nev_wpl = Cons['nev_wpl']
nev_wplr = Cons['nev_wplr']
nev_ttbar = Cons['nev_ttbar']
nev_qcd = Cons['nev_qcd']
nev_st = Cons['nev_st']

files = sorted(glob.glob("*job*of*.root"))


sigmassdict = WPF.sigmasses
sigbrdict = WPF.sigBR

j = []
for f in files:
	print f
	j.append(f.replace('_jo'+re.search('_jo(.+?)_PSET', f).group(1),""))

files_to_sum = list(set(j))

commands = []
commands.append('rm logs/output*.log')
commands.append('mv output*.log logs/')
commands.append('rm temprootfiles/*.root')
commands.append('rm -rf notneeded')
for f in files_to_sum:
	commands.append('rm '+f) 
	commands.append('hadd ' + f + " " + f.replace('_PSET','_job*_PSET') )
	commands.append('mv ' +  f.replace('_PSET','_job*_PSET') + ' temprootfiles/')
commands.append('mv THB'+options.atype+'data_*.root rootfiles/')


for s in commands :
    print 'executing ' + s
    subprocess.call( [s], shell=True )



print "Complete"


