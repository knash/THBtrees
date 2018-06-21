#! /usr/bin/env python

###################################################################
##								 ##
## Name: TBrate.py						 ##
## Author: Kevin Nash 						 ##
## Date: 5/28/2015						 ##
## Purpose: This program creates the numerator and denominator 	 ##
##          used by TBTrigger_Maker.py to create trigger  	 ##
##          Efficiency curves.					 ##
##								 ##
###################################################################

import os
import sys
from DataFormats.FWLite import Events, Handle
from optparse import OptionParser
from array import *


import WprimetoVlq_Functions	
from WprimetoVlq_Functions import *
WPF = WprimetoVlq_Functions('default','Puppi')


from DataFormats.FWLite import Events, Handle
from optparse import OptionParser

parser = OptionParser()

parser.add_option('--istree', metavar='F', action='store_true',
                  default=False,
                  dest='istree',
                  help='istree')

(options, args) = parser.parse_args()


saveout = sys.stdout
#Based on what set we want to analyze, we find all Ntuple root files 
#arr = ['QCDHT500','QCDHT700','QCDHT1000','QCDHT1500','QCDHT2000','data','dataH','datanoH','ttbar','ttbar_mtt700','ttbar_mtt1000']

arr = ['QCDHT1000','QCDHT1500','QCDHT2000','data','ttbar_mtt700','ttbar_mtt1000']



import os, shutil, subprocess

siglist = []

for VLQ in ['Tp','Bp']:
	FinalStates = ["Ht"]
	Chiralities =["LH","RH"]
	Masses = [[1500,[700,900,1200]],[2000,[900,1200,1500]],[2500,[1200,1500,1900]]]
	Zwidths = [[0.03,'Nar'],[0.1,'Wid'],[0.3,'ExWid']]
	Twidths = [[0,'Nar'],[0.1,'Wid'],[0.3,'ExWid']]
	FinalStates = ["Ht"]
	Chiralities =["LH","RH"]
	Masses = [[1500,[800,1000,1300]],[2000,[1000,1300,1500]],[2500,[1300,1500,1800]],[3000,[1500,1800,2100]],[3500,[1800,2100,2500]],[4000,[2100,2500,3000]]]
	Zwidths = [[0.03,'Nar'],[0.3,'Wid']]
	Twidths = [[0.03,'Nar'],[0.3,'Wid']]


	for state in FinalStates:
		for hand in Chiralities:
			for zmass in Masses:
				for tmass in zmass[1]:
					for zwidth in Zwidths:
						for twidth in Twidths:
							#if zmass[0]==1500 and tmass==zmass[1][0]:
							#	continue 
							if hand=='RH' and not (tmass==zmass[1][1]):
								continue
							#if (zwidth[1]!=twidth[1]) and not (tmass==zmass[1][1]):
							#	continue
						
							if (twidth[1]=='Wid') :
								print  twidth[1]	 
								if hand=='RH' :
									continue
								if hand=='LH' :
									if tmass!=zmass[1][1]:
										continue
									if zmass[0]!=2000 and zmass[0]!=3000:
										print zmass[0]
										continue 
							
							if hand=='RH' :
								if (zwidth[1]!=twidth[1]):
									continue
								#if zmass[0]!=1500 and zmass[0]!=2500 and zmass[0]!=3500:
								#	continue




							WpM = str(zmass[0])
							WpW = str(zwidth[1])
							QpT = str(VLQ)
							QpM = str(tmass)
							QpW = str(twidth[1])
							Hand = str(hand)
							
							#BLACKLIST
							#if int(WpM)>3100:
							#	continue	
							#if WpW!='Nar':
							#	continue
							#if QpW!='Nar':
							#	continue
							#if Hand!='LH':
							#	continue

							arr.append('THBWp'+WpM+QpT+QpM)
							print  'WpTo'+QpT+'_Wp' + WpM+ WpW + '_'+ QpT + QpM + QpW + Hand+'_Ht_HTobb_TuneCUETP8M2T4_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM'



treestring = ''
if options.istree:
	treestring = 'TTree'

for i in arr:
	Outf1   =   open("Files_"+treestring+i+".txt", "w")
	files = WPF.Load_Ntuples(i,'',options.istree)
	sys.stdout = Outf1
	for file1 in files:
		if file1.find("root")!=-1:
			print file1
	sys.stdout = saveout


