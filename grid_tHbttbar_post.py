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




ttbarfiles = sorted(glob.glob('THB'+options.atype+'ttbar*_PSET_'+cuts+'.root'))

for ttbarfile in ttbarfiles:
	weightedname = ttbarfile.replace('THB'+options.atype+'ttbar','THB'+options.atype+'weightedttbar')
	print weightedname
	csstring=ttbarfile.replace('THB'+options.atype+'ttbar_','')[0:7].replace('_','').replace('s','')
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


ttbarfilesweighted = sorted(glob.glob('THB'+options.atype+'weightedttbar*_PSET_'+cuts+'.root'))
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



print "Complete"

