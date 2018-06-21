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
xsec_wpl = Cons['xsec_wpl']
xsec_wplr = Cons['xsec_wplr']
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
commands.append('mv THBanalyzerdata_*.root rootfiles/')



for s in commands :
    print 'executing ' + s
    subprocess.call( [s], shell=True )

commands = []

commands.append('rm rootfiles/THBanalyzerttbar_PSET_'+cuts+'weighted.root') #removes old file with same name in /rootfiles/
commands.append('python HistoWeight.py -i THBanalyzerttbar_PSET_'+cuts+'.root -o rootfiles/THBanalyzerttbar_PSET_'+cuts+'weighted.root -n auto -w ' + str(lumi*xsec_ttbar['PH']))
commands.append('mv THBanalyzerttbar_PSET_'+cuts+'.root temprootfiles/')

if True:	
	qcdfiles = sorted(glob.glob('THBanalyzerQCDHT*_PSET_'+cuts+'.root'))
	for f in qcdfiles:
		pt = f.lstrip('THBanalyzerQCDHT').rstrip('_PSET_'+cuts+'.root')
		print "QCD HT " + pt
		xsec_QCD = xsec_qcd['HT'+pt]
		nev_QCD = nev_qcd['HT'+pt]
		commands.append('rm ' + f.replace('THBanalyzerQCDHT','THBanalyzerweightedQCDHT'))	 
		commands.append('python HistoWeight.py -i '+f+' -o '+f.replace('THBanalyzerQCDHT','THBanalyzerweightedQCDHT')+' -n auto -w ' + str(lumi*xsec_QCD))
		commands.append('mv '+f+' temprootfiles/')
	commands.append('hadd THBanalyzerQCD_PSET_'+cuts+'.root THBanalyzerweightedQCDHT*_PSET_'+cuts+'.root')
	commands.append('mv THBanalyzerQCD_PSET_'+cuts+'.root rootfiles/')
	commands.append('mv THBanalyzerweightedQCDHT*_PSET_'+cuts+'.root temprootfiles/')






sigfiles = sorted(glob.glob('THBanalyzerTHBW*_PSET_'+cuts+'.root'))

#Take sigma_wpr->tb(all had) LO, correct to sigma_wpr->tb(all had), correct to sigma_wpr->tb, correct to sigma_wpr, correct to ~sigma_wpr->Tb, correct to ~sigma_wpr->Tb->tHb
#WprimeConvo = (1.2)*(1.0/0.676)*(1.0/0.24)*(0.22)*(0.50)
#W'->tb is approx 1 to 1 with W'->tot in this model, W' to Bt+Tb = approx 50%, assume T->tH = 50%
WprimeConvo = (1.0)*(0.25)*(0.50)
for f in sigfiles:
		mass = '2000'
		BPTP = copy.copy(f)
		BPTP = BPTP.replace('THBanalyzerTHBWp2000','').replace('1200_PSET_'+cuts+'.root','')

	#	if BPTP=='Bp':
	#		nev_sig = 36795
	#	if BPTP=='Tp':
	#		nev_sig = 35546
		xsec_sig = xsec_wpr[mass]


		commands.append('rm ' + f.replace('THBanalyzerTHB','THBanalyzerweightedTHB'))	 


		print "Wprime correcty factor ",WprimeConvo
		commands.append('python HistoWeight.py -i '+f+' -o '+f.replace('THBanalyzerTHB','THBanalyzerweightedTHB')+' -n auto -w ' + str(lumi*xsec_sig*WprimeConvo))
		commands.append('mv '+f+' temprootfiles/')
		commands.append('mv '+f.replace('THBanalyzerTHB','THBanalyzerweightedTHB')+' rootfiles/')







for s in commands :
    print 'executing ' + s
    subprocess.call( [s], shell=True )







