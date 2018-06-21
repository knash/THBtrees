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

files = sorted(glob.glob("*job*of*.root"))

sigmassdict = WPF.sigmasses

j = []
for f in files:
	j.append(f.replace('_jo'+re.search('_jo(.+?)_PSET', f).group(1),""))

files_to_sum = list(set(j))

commands = []
commands.append('rm *.log') 
commands.append('rm temprootfiles/*.root')
commands.append('rm -rf notneeded')





#W'->tb is approx 1 to 1 with W'->tot in this model, W' to Bt+Tb = approx 50%, assume T->tH = 50%
WprimeConvo = (1.0)*(0.50)*(0.584)

sigfiles = sorted(glob.glob('THBanalyzerTHBW*_PSET_'+cuts+'.root'))

for f in sigfiles:
		mass = f.replace('THBanalyzerTHBWp','')
		print "full file",f
		mass = mass[0:4]
		print "mass", mass

		vlqmass = f.replace('THBanalyzerTHBWp'+mass,'')
		vlqtype = vlqmass[0:2]
		vlqmass = (vlqmass).replace(vlqtype,'')
		vlqmass = (vlqmass[0:4]).replace('_','')
		print "vlqmass",vlqmass
		curVLQindex = sigmassdict[mass].index(vlqmass)
		print "index",curVLQindex
		if curVLQindex==0:
			CurWprimeConvo = (0.25)*WprimeConvo
		elif curVLQindex==1:
			CurWprimeConvo = (0.1225)*WprimeConvo
		elif curVLQindex==2:
			CurWprimeConvo = (0.075)*WprimeConvo
		print "CurWprimeConvo",CurWprimeConvo

		xsec_sig = xsec_wpr[mass]
		#nev_sig = 35546

		commands.append('rm ' + f.replace('THBanalyzerTHB','THBanalyzerweightedTHB'))	 
		commands.append('python HistoWeight.py -i '+f+' -o '+f.replace('THBanalyzerTHB','THBanalyzerweightedTHB')+'  -n auto -w ' + str(lumi*xsec_sig*CurWprimeConvo))
		commands.append('mv '+f+' temprootfiles/')
		commands.append('mv '+f.replace('THBanalyzerTHB','THBanalyzerweightedTHB')+' rootfiles/')


for s in commands :
    print 'executing ' + s
    subprocess.call( [s], shell=True )




