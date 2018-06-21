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
                  help		=	'Cuts type (ie default, analyzer, etc)')
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

commands = []

#1pb for sigma T' + B' for scaling 
#samples generated with H decay, so this needs to be taken into account 
WprimeConvo = (0.584)*(0.5)

#sigfiles = sorted(glob.glob('THBanalyzerTHBW*_PSET_'+cuts+'.root'))

sigfiles = sorted(glob.glob('rootfiles/THBanalyzerweightedTHBWp*_PSET_'+cuts+'.root'))

for f in sigfiles:
		mass = f.replace('THBanalyzerTHBWp','')
		mass = mass[0:4]
		print mass
		
		#xsec_sig = xsec_wpr[mass]
		#nev_sig = 35546
		commands.append('rm '+f.replace('THBanalyzerweightedTHB','limitscale/THBanalyzerlimitscaleTHB'))
		commands.append('python HistoWeight.py -i '+f+' -o '+f.replace('THBanalyzerweightedTHB','limitscale/THBanalyzerlimitscaleTHB')+'  -n auto -w ' + str(lumi*1.0*WprimeConvo)+"  ")


for s in commands :
    print 'executing ' + s
    subprocess.call( [s], shell=True )







