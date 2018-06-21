#! /usr/bin/env python

###################################################################
##								 ##
## Name: TBanalyzer.py	   			                 ##
## Author: Kevin Nash 						 ##
## Date: 6/5/2012						 ##
## Purpose: This program performs the main analysis.  		 ##
##	    It takes the tagrates created by  	 		 ##
##          TBrate_Maker.py stored in fitdata, and uses 	 ##
##          them to weigh pre b tagged samples to create a 	 ##
##	    QCD background estimate along with the full event    ##
##	    selection to product Mtb inputs to Theta		 ##
##								 ##
###################################################################

import os
import glob
import math
import copy
import random
import time
from math import sqrt
#import quickroot
#from quickroot import *
import datetime
import ROOT 
from ROOT import TLorentzVector,TH1F,TH2F,TTree,TFile,gROOT

import sys
from DataFormats.FWLite import Events, Handle
from optparse import OptionParser

parser = OptionParser()

parser.add_option('-s', '--set', metavar='F', type='string', action='store',
                  default	=	'THB',
                  dest		=	'set',
                  help		=	'data or ttbar')

parser.add_option('-C', '--coll', metavar='F', type='string', action='store',
                  default	=	'Puppi',
                  dest		=	'coll',
                  help		=	'CHS or Puppi')

parser.add_option('-x', '--pileup', metavar='F', type='string', action='store',
                  default	=	'on',
                  dest		=	'pileup',
                  help		=	'If not data do pileup reweighting?')
parser.add_option('-n', '--num', metavar='F', type='string', action='store',
                  default	=	'all',
                  dest		=	'num',
                  help		=	'job number')

parser.add_option('-B', '--bkg', metavar='F', type='string', action='store',
                  default	=	'nominal',
                  dest		=	'bkg',
                  help		=	'cuts to use for rate file')

parser.add_option('-j', '--jobs', metavar='F', type='string', action='store',
                  default	=	'1',
                  dest		=	'jobs',
                  help		=	'number of jobs')


parser.add_option('-t', '--tname', metavar='F', type='string', action='store',
                  default	=	'HLT_PFHT900,HLT_PFHT800,HLT_JET450',
                  dest		=	'tname',
                  help		=	'trigger name')
parser.add_option('-S', '--split', metavar='F', type='string', action='store',
                  default	=	'file',
                  dest		=	'split',
                  help		=	'split by event of file')

#parser.add_option('-t', '--trigger', metavar='F', type='string', action='store',
#                  default	=	'none',
#                  dest		=	'trigger',
#                  help		=	'none, nominal, up, or down')

parser.add_option('-m', '--modulesuffix', metavar='F', type='string', action='store',
                  default	=	'none',
                  dest		=	'modulesuffix',
                  help		=	'ex. PtSmearUp')

parser.add_option('-g', '--grid', metavar='F', type='string', action='store',
                  default	=	'off',
                  dest		=	'grid',
                  help		=	'running on grid off or on')

parser.add_option('-u', '--ptreweight', metavar='F', type='string', action='store',
                  default	=	'on',
                  dest		=	'ptreweight',
                  help		=	'on or off')

parser.add_option('-p', '--pdfweights', metavar='F', type='string', action='store',
                  default	=	'nominal',
                  dest		=	'pdfweights',
                  help		=	'nominal, up, or down')

parser.add_option('-q', '--q2scale', metavar='F', type='string', action='store',
                  default	=	'nominal',
                  dest		=	'q2scale',
                  help		=	'nominal, up, or down')

parser.add_option('-a', '--alphas', metavar='F', type='string', action='store',
                  default	=	'nominal',
                  dest		=	'alphas',
                  help		=	'nominal, up, or down')

parser.add_option('-J', '--JES', metavar='F', type='string', action='store',
                  default	=	'nominal',
                  dest		=	'JES',
                  help		=	'nominal, up, or down')
parser.add_option('-R', '--JER', metavar='F', type='string', action='store',
                  default	=	'nominal',
                  dest		=	'JER',
                  help		=	'nominal, up, or down')
parser.add_option('-z', '--pdfset', metavar='F', type='string', action='store',
                  default	=	'',
                  dest		=	'pdfset',
                  help		=	'pdf set')
parser.add_option('--printEvents', metavar='F', action='store_true',
                  default=False,
                  dest='printEvents',
                  help='Print events that pass selection (run:lumi:event)')
parser.add_option('-c', '--cuts', metavar='F', type='string', action='store',
                  default	=	'default',
                  dest		=	'cuts',
                  help		=	'Cuts type (ie default, rate, etc)')


(options, args) = parser.parse_args()

print "Options summary"
print "=================="
for  opt,value in options.__dict__.items():
	#print str(option)+ ": " + str(options[option]) 
	print str(opt) +': '+ str(value)
print "=================="
print ""
di = ""
if options.grid == 'on':
	di = "tardir/"
	sys.path.insert(0, 'tardir/')

gROOT.Macro(di+"rootlogon.C")

import WprimetoVlq_Functions	
from WprimetoVlq_Functions import *


mod = ''
post = ''
if options.JES!='nominal':
	mod = mod + 'JES_' + options.JES
	post='jes'+options.JES
if options.JER!='nominal':
	mod = mod + 'JER_' + options.JER
	post='jer'+options.JER




WPF = WprimetoVlq_Functions(options.cuts,options.coll,post)
#Load up cut values based on what selection we want to run 
Cuts = WPF.LoadCuts


#files = WPF.Load_Ntuples(options.set,di) 


#events = Events(files)
if options.set=='QCDHT1500':
	b2ganafwf = 	[
			"root://cmsxrootd.fnal.gov///store/group/phys_b2g/B2GAnaFW_80X_V2p4/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1_B2GAnaFW_80X_V2p4/170103_191052/0000/B2GEDMNtuple_1.root",
			"root://cmsxrootd.fnal.gov///store/group/phys_b2g/B2GAnaFW_80X_V2p4/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1_B2GAnaFW_80X_V2p4/170103_191052/0000/B2GEDMNtuple_2.root",
			#"root://cmsxrootd.fnal.gov///store/group/phys_b2g/B2GAnaFW_80X_V2p4/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1_B2GAnaFW_80X_V2p4/170103_191052/0000/B2GEDMNtuple_3.root",
			#"root://cmsxrootd.fnal.gov///store/group/phys_b2g/B2GAnaFW_80X_V2p4/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1_B2GAnaFW_80X_V2p4/170103_191052/0000/B2GEDMNtuple_4.root",
			#"root://cmsxrootd.fnal.gov///store/group/phys_b2g/B2GAnaFW_80X_V2p4/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1_B2GAnaFW_80X_V2p4/170103_191052/0000/B2GEDMNtuple_5.root"		
			]

if options.set=='QCDHT500':
	b2ganafwf = 	[
			"root://cmsxrootd.fnal.gov///store/group/phys_b2g/B2GAnaFW_80X_V2p4/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1_B2GAnaFW_80X_V2p4/170103_194958/0000/B2GEDMNtuple_1.root",
			"root://cmsxrootd.fnal.gov///store/group/phys_b2g/B2GAnaFW_80X_V2p4/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1_B2GAnaFW_80X_V2p4/170103_194958/0000/B2GEDMNtuple_2.root"
			]


if options.set=='ttbar':
	b2ganafwf = 	[
			"root://cmsxrootd.fnal.gov///store/group/phys_b2g/B2GAnaFW_80X_V2p4/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1_B2GAnaFW_80X_V2p4/161222_110143/0000/B2GEDMNtuple_1.root",
			"root://cmsxrootd.fnal.gov///store/group/phys_b2g/B2GAnaFW_80X_V2p4/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1_B2GAnaFW_80X_V2p4/161222_110143/0000/B2GEDMNtuple_2.root"
			]




if options.set=='dataB':
	b2ganafwf = 	[
			"root://cmsxrootd.fnal.gov///store/group/phys_b2g/B2GAnaFW_80X_V2p3/JetHT/Run2016B/JetHT/Run2016B-23Sep2016-v3_B2GAnaFW_80X_V2p3/161216_214635/0000/B2GEDMNtuple_1.root",
			"root://cmsxrootd.fnal.gov///store/group/phys_b2g/B2GAnaFW_80X_V2p3/JetHT/Run2016B/JetHT/Run2016B-23Sep2016-v3_B2GAnaFW_80X_V2p3/161216_214635/0000/B2GEDMNtuple_2.root"
			]

if options.set=='dataD':
	b2ganafwf = 	[
			"root://cmsxrootd.fnal.gov///store/group/phys_b2g/B2GAnaFW_80X_V2p3/JetHT/Run2016D/JetHT/Run2016D-23Sep2016-v1_B2GAnaFW_80X_V2p3/170117_200913/0000/B2GEDMNtuple_1.root",
			"root://cmsxrootd.fnal.gov///store/group/phys_b2g/B2GAnaFW_80X_V2p3/JetHT/Run2016D/JetHT/Run2016D-23Sep2016-v1_B2GAnaFW_80X_V2p3/170117_200913/0000/B2GEDMNtuple_2.root"
			]

if options.set=='dataH':
	b2ganafwf = 	[
			"root://cmsxrootd.fnal.gov///store/group/phys_b2g/B2GAnaFW_80X_V2p3/JetHT/Run2016H/JetHT/Run2016H-PromptReco-v2_B2GAnaFW_80X_V2p3/161216_223421/0000/B2GEDMNtuple_1.root",
			"root://cmsxrootd.fnal.gov///store/group/phys_b2g/B2GAnaFW_80X_V2p3/JetHT/Run2016H/JetHT/Run2016H-PromptReco-v2_B2GAnaFW_80X_V2p3/161216_223421/0000/B2GEDMNtuple_2.root"

			]



events = Events(b2ganafwf)

PDFup = 0.0
PDFdown = 0.0
PDFnom = 0.0
count = 0




reconpvHandle 	= 	Handle (  "int"  )
reconpvLabel  	= 	( "vertexInfo" , "npv")


truenpvHandle 	= 	Handle (  "int"  )
truenpvLabel  	= 	( "eventUserData" , "puNtrueInt")

f = TFile( "THBnpvtester"+options.set+".root", "recreate" )



truenpvhistpre  = TH1F("truenpvhistpre",		"",     	  	      	100, 0, 100.0 )
truenpvhistpost  = TH1F("truenpvhistpost",		"",     	  	      	100, 0, 100.0 )
truenpvhistpostup  = TH1F("truenpvhistpostup",		"",     	  	      	100, 0, 100.0 )
truenpvhistpostdown  = TH1F("truenpvhistpostdown",		"",     	  	      	100, 0, 100.0 )

reconpvhistpre  = TH1F("reconpvhistpre",		"",     	  	      	100, 0, 100.0 )
reconpvhistpost  = TH1F("reconpvhistpost",		"",     	  	      	100, 0, 100.0 )
reconpvhistpostup  = TH1F("reconpvhistpostup",		"",     	  	      	100, 0, 100.0 )
reconpvhistpostdown  = TH1F("reconpvhistpostdown",		"",     	  	      	100, 0, 100.0 )



truenpvhistpre.Sumw2()
truenpvhistpost.Sumw2()
truenpvhistpostup.Sumw2()
truenpvhistpostdown.Sumw2()

reconpvhistpre.Sumw2()
reconpvhistpost.Sumw2()
reconpvhistpostup.Sumw2()
reconpvhistpostdown.Sumw2()





	

PUFile = TFile(di+"PileUp_Ratio_ttbar.root")
PUplotvec = [PUFile.Get("Pileup_Ratio"),PUFile.Get("Pileup_Ratio_up"),PUFile.Get("Pileup_Ratio_down")]
		

for event in events:
  	count+=1
    	if count % 1000 == 0 :
      		print  '--------- Processing Event ' + str(count) #+'   -- percent complete ' + str(100*count/totevents) + '% -- '

	event.getByLabel (reconpvLabel, reconpvHandle)
	reconpv 	= 	reconpvHandle.product()
			
	puweight = 1.0
	if (options.set).find('data')==-1:
		event.getByLabel (truenpvLabel, truenpvHandle)
		truenpv 	= 	truenpvHandle.product()
		#print truenpv[0]



		puweightvec = WPF.PU_Lookup(truenpv[0],PUplotvec)
			
		puweight = puweightvec[0]
		puweightup = puweightvec[1]
		puweightdown = puweightvec[2]

		reconpvhistpre.Fill(reconpv[0])
		reconpvhistpostup.Fill(reconpv[0],puweightup)
		reconpvhistpostdown.Fill(reconpv[0],puweightdown)

	
		truenpvhistpre.Fill(truenpv[0])
		truenpvhistpost.Fill(truenpv[0],puweight)
		truenpvhistpostup.Fill(truenpv[0],puweightup)
		truenpvhistpostdown.Fill(truenpv[0],puweightdown)



	reconpvhistpost.Fill(reconpv[0],puweight)

	#print reconpv[0]


f.cd()
f.Write()
f.Close()

