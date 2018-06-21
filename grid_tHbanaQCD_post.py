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
sigbrdict = WPF.sigBR

j = []
for f in files:
	j.append(f.replace('_jo'+re.search('_jo(.+?)_PSET', f).group(1),""))

files_to_sum = list(set(j))

commands = []
commands.append('rm *.log') 
commands.append('rm temprootfiles/*.root')
commands.append('rm -rf notneeded')
for f in files_to_sum:
	commands.append('rm '+f) 
	commands.append('hadd ' + f + " " + f.replace('_PSET','_job*_PSET') )
	commands.append('mv ' +  f.replace('_PSET','_job*_PSET') + ' temprootfiles/')
#commands.append('mv THBanalyzerdata_*.root rootfiles/')



for s in commands :
    print 'executing ' + s
    subprocess.call( [s], shell=True )

commands = []

if True:	
	qcdfiles = sorted(glob.glob('THBanalyzerQCDHT*__PSET_'+cuts+'.root'))
	for f in qcdfiles:
		pt = f.lstrip('THBanalyzerQCDHT').rstrip('__PSET_'+cuts+'.root').replace('sjbtagHiggs','')
		print "QCD HT " + pt
		xsec_QCD = xsec_qcd['HT'+pt]
		nev_QCD = nev_qcd['HT'+pt]
		commands.append('rm ' + f.replace('THBanalyzerQCDHT','THBanalyzerweightedQCDHT'))	 
		commands.append('python HistoWeight.py -i '+f+' -o '+f.replace('THBanalyzerQCDHT','THBanalyzerweightedQCDHT')+' -n auto -w ' + str(lumi*xsec_QCD))
		commands.append('mv '+f+' temprootfiles/')
	commands.append('hadd THBanalyzerQCD__PSET_'+cuts+'.root THBanalyzerweightedQCDHT*__PSET_'+cuts+'.root')
	commands.append('mv THBanalyzerQCD__PSET_'+cuts+'.root rootfiles/')
	commands.append('mv THBanalyzerweightedQCDHT*__PSET_'+cuts+'.root rootfiles/')









for s in commands :
    print 'executing ' + s
    subprocess.call( [s], shell=True )




