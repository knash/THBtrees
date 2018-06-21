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
commands.append('mv THBanalyzerdata_*.root rootfiles/')



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










#W'->tb is approx 1 to 1 with W'->tot in this model, W' to Bt+Tb = approx 50%, assume T->tH = 50%
WprimeConvo = (1.0)*(0.50)*(0.584)

sigfiles = sorted(glob.glob('THBanalyzerTHBW*_PSET_'+cuts+'.root'))

for f in sigfiles:
		mass = f.replace('THBanalyzerTHBWp','')
		print "full file",f
		mass = mass[0:4]
		print "mass", mass

		vlqmass = f.replace('THBanalyzerTHBWp'+mass,'').replace('sjbtagHiggs','')
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

		commands.append('rm ' + f.replace('THBanalyzerTHB','THBanalyzerweightedTHB'))	 
		commands.append('python HistoWeight.py -i '+f+' -o '+f.replace('THBanalyzerTHB','THBanalyzerweightedTHB')+'  -n auto -w ' + str(lumi*xsec_sig*CurWprimeConvo))
		commands.append('mv '+f+' temprootfiles/')
		commands.append('mv '+f.replace('THBanalyzerTHB','THBanalyzerweightedTHB')+' rootfiles/')


ttbarfiles = sorted(glob.glob('THBanalyzerttbar*_PSET_'+cuts+'.root'))

for ttbarfile in ttbarfiles:
	weightedname = ttbarfile.replace('THBanalyzerttbar','THBanalyzerweightedttbar')
	print weightedname
	csstring=ttbarfile.replace('THBanalyzerttbar_','')[0:7].replace('_','').replace('s','')
	print csstring
	crosssection=xsec_ttbar[csstring]
	print crosssection
	commands.append('rm rootfiles/'+weightedname) #removes old file with same name in /rootfiles/
	commands.append('python HistoWeight.py -i '+ ttbarfile +' -o '+weightedname+ ' -n auto -w ' + str(lumi*crosssection))
	commands.append('mv '+ ttbarfile +' temprootfiles/')


for s in commands :
    print 'executing ' + s
    subprocess.call( [s], shell=True )

commands = []


ttbarfilesweighted = sorted(glob.glob('THBanalyzerweightedttbar*_PSET_'+cuts+'.root'))
print "weightedttbar ",ttbarfilesweighted

for ttbarfilew in ttbarfilesweighted:
	if ttbarfilew.find("mtt700")!=-1:
		continue
	ttbarfilew700 = ttbarfilew.replace("mtt1000","mtt700")
	ttbarfilewhadd = ttbarfilew.replace("_mtt1000","")
	commands.append('rm rootfiles/'+ttbarfilewhadd)
	commands.append('hadd rootfiles/'+ttbarfilewhadd+' '+ttbarfilew700+' '+ttbarfilew)
	commands.append('mv '+ttbarfilew700+' '+ttbarfilew+' temprootfiles/')
	print "ttbar700 ",ttbarfilew700
	print "ttbar1000 ",ttbarfilew
	print "hadd command ",'hadd rootfiles/'+ttbarfilewhadd+" "+ttbarfilew700+" "+ttbarfilew


for s in commands :
    print 'executing ' + s
    subprocess.call( [s], shell=True )




