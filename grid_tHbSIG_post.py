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

#W'->tb is approx 1 to 1 with W'->tot in this model, W' to Bt+Tb = approx 50%, assume T->tH = 50%
WprimeConvo = (1.0)*(0.50)*(0.584)



sigfiles = sorted(glob.glob('THB'+options.atype+'THBWp*_PSET_'+cuts+'.root'))

for f in sigfiles:
		mass = f.replace('THB'+options.atype+'THBWp','')
		mass = mass[0:4]

		print "mass", mass

		vlqmass = f.replace('THB'+options.atype+'THBWp'+mass,'')
		vlqtype = vlqmass[0:2]
		vlqmass = (vlqmass).replace(vlqtype,'')
		vlqmass = (vlqmass[0:4]).replace('_','')
		print "vlqmass",vlqmass
		curVLQindex = sigmassdict[mass].index(vlqmass)
		print "index",curVLQindex

		print sigbrdict[mass]
		CurWprimeConvo = WprimeConvo*sigbrdict[mass][curVLQindex]*0.5
		print "BR",sigbrdict[mass][curVLQindex]
		print "CurWprimeConvo",CurWprimeConvo

		xsec_sig = xsec_wpr[mass]
		#nev_sig = 35546

		commands.append('rm ' + f.replace('THB'+options.atype+'THB','THB'+options.atype+'weightedTHB'))	 
		commands.append('python HistoWeight.py -i '+f+' -o '+f.replace('THB'+options.atype+'THB','THB'+options.atype+'weightedTHB')+'  -n auto -w ' + str(lumi*xsec_sig*CurWprimeConvo))
		commands.append('mv '+f+' temprootfiles/')
		commands.append('mv '+f.replace('THB'+options.atype+'THB','THB'+options.atype+'weightedTHB')+' rootfiles/')







for s in commands :
    print 'executing ' + s
    subprocess.call( [s], shell=True )

print "Complete"





