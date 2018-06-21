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


sigmassdict = WPF.sigmasses
sigbrdict = WPF.sigBR

commands = []


qcdfiles = sorted(glob.glob('THB'+options.atype+'QCDHT*_PSET_'+cuts+'.root'))
for f in qcdfiles:
	pt = f.lstrip('THB'+options.atype+'QCDHT').rstrip('_PSET_'+cuts+'.root')
	print "QCD HT " + pt
	xsec_QCD = xsec_qcd['HT'+pt]
	nev_QCD = nev_qcd['HT'+pt]
	commands.append('rm ' + f.replace('THB'+options.atype+'QCDHT','THB'+options.atype+'weightedQCDHT'))	 
	commands.append('python HistoWeight.py -i '+f+' -o '+f.replace('THB'+options.atype+'QCDHT','THB'+options.atype+'weightedQCDHT')+' -n auto -w ' + str(lumi*xsec_QCD))
	commands.append('mv '+f+' temprootfiles/')
commands.append('hadd THB'+options.atype+'QCD_PSET_'+cuts+'.root THB'+options.atype+'weightedQCDHT*_PSET_'+cuts+'.root')
commands.append('mv THB'+options.atype+'QCD_PSET_'+cuts+'.root rootfiles/')
commands.append('mv THB'+options.atype+'weightedQCDHT*_PSET_'+cuts+'.root rootfiles/')



for s in commands :
    print 'executing ' + s
    subprocess.call( [s], shell=True )

print "Complete"





