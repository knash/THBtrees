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

parser.add_option('--verbose', metavar='F', action='store_true',
                  default=False,
                  dest='verbose',
                  help='verbose debug mode')

parser.add_option('--qcdsetbkg', metavar='F', action='store_true',
                  default=False,
                  dest='qcdsetbkg',
                  help='qcdsetbkg')


parser.add_option('-c', '--cuts', metavar='F', type='string', action='store',
                  default	=	'default',
                  dest		=	'cuts',
                  help		=	'Cuts type (ie default, rate, etc)')
parser.add_option('-A', '--sjbtaghiggs', metavar='F', type='string', action='store',
                  default	=	'False',
                  dest		=	'sjbtaghiggs',
                  help		=	'use sjbtag b/c devdatta')

(options, args) = parser.parse_args()

tname = options.tname.split(',')
tnamestr = ''
for iname in range(0,len(tname)):
	tnamestr+=tname[iname]
	if iname!=len(tname)-1:
		tnamestr+='OR'

if tnamestr=='HLT_PFHT900ORHLT_PFHT800ORHLT_JET450':
	tnameformat='nominal'
elif tnamestr=='':
	tnameformat='none'
else:
	tnameformat=tnamestr


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
	mod = mod + 'JEC' + options.JES
	post='jes'+options.JES
if options.JER!='nominal':
	mod = mod + 'JER' + options.JER
	post='jer'+options.JER


AK4mod=""
if mod.find("M")==-1:
	AK4mod=mod



WPF = WprimetoVlq_Functions(options.cuts,options.coll,post)
Cuts = WPF.LoadCuts

####EDIT
ptmincut = Cuts['ptmincut']
pthcut = Cuts['pthcut']
pttcut = Cuts['pttcut']
ptbcut = Cuts['ptbcut']
tmass = Cuts['tmass']
tau32 = Cuts['tau32']
tau32tight = Cuts['tau32tight']
sjbtagt = Cuts['sjbtagt']
sjbtagh = Cuts['sjbtagh']
sjbtaghloose = Cuts['sjbtaghloose']
btag = Cuts['btag']
hmass = Cuts['hmass']
hmassinvert = Cuts['hmassinvert']
tau21 = Cuts['tau21']
####EDIT





#For large datasets we need to parallelize the processing
jobs=int(options.jobs)
if jobs != 1:
	num=int(options.num)
	jobs=int(options.jobs)
	print "Running over " +str(jobs)+ " jobs"
	print "This will process job " +str(num)
else:
	print "Running over all events"

#This section defines some strings that are used in naming the optput files


#files = WPF.Load_Ntuples(options.set,di) 
files = WPF.Load_Ntuples(options.set,di,True) 
#files = glob.glob("TTrees/THBttree"+options.set+"*.root")
files=sorted(files)

TFs = []

for fifi in files:
	TFs.append(TFile.Open(fifi))



TTree =  TFs[0].Get('Tree')


bkgset='data'
bkgsetqst = ''
if (options.set.find('QCD') != -1):
	if options.qcdsetbkg:
		bkgset='weighted'+options.set
		bkgsetqst = 'persetrate'
	else:
		bkgset='QCD'

jobiter = 0
splitfiles = []
totevents = 0
if jobs != 1 and options.split=="file":
    oldTFs = copy.copy(TFs)
    newTFs = []
    for infi in xrange(len(oldTFs)):
	remain = (infi)%jobs
	#print infi,jobs,(infi)%jobs
	if (remain+1)==num:
		newTFs.append(oldTFs[infi])
		totevents+=newTFs[-1].Get('Tree').GetEntries()

    TFs = newTFs
else:
    totevents+=TFs[0].Get('Tree').GetEntries()
print TFs
print len(TFs),"Files"




ptmod = ""
if post.find("M")==-1:
	ptmod=post	



rwstr = ''
if options.ptreweight=='off' and bkgset!="QCD":
	rwstr = '_PTRWoff'
sjstr = ''
if options.sjbtaghiggs=='True':
	sjstr = 'sjbtagHiggs'
#---------------------------------------------------------------------------------------------------------------------#

if jobs != 1:
	f = TFile( "THBanalyzer"+options.set+rwstr+bkgsetqst+sjstr+"_"+mod+"_job"+options.num+"of"+options.jobs+"_PSET_"+options.cuts+".root", "recreate" )
else:
	f = TFile( "THBanalyzer"+options.set+rwstr+bkgsetqst+sjstr+"_"+mod+"_PSET_"+options.cuts+".root", "recreate" )


ratestr = ""
if options.cuts!='default':
	ratestr = options.cuts+"_"
print "running on "+ratestr+"sidebandTT rates"

print "Loading ratefile",di+"THBrate_Maker"+rwstr+"_"+bkgset+"_PSET_default.root"
TagFile = ROOT.TFile(di+"THBrate_Maker"+rwstr+"_"+bkgset+"_PSET_default.root")
tagh = {}

if options.set.find('data')==-1:
	unclist = ['','PUup','PUdown','Trigup','Trigdown']
	if options.set.find('ttbar')!=-1:
		unclist.extend(['Alpup','Alpdown','Bup','Bdown','Bmisup','Bmisdown','Q2up','Q2down','Hmistagup','Hmistagdown','Tptup','Tptdown','PDFup','PDFdown'])	
	if options.set.find('THB')!=-1:
		unclist.extend(['Alpup','Alpdown','WExup','WExdown','Htagup','Htagdown','Hmistagup','Hmistagdown','Bup','Bdown','Bmisdown','Bmisup','Q2up','Q2down','PDFup','PDFdown'])	

else:
	unclist = ['','overlap']

bkguncs = ['','up','down','Mup','Mdown','ttup','ttdown','closup','closdown']
params = ['','mthb']
print "Creating histograms"

histosets = {}

Mthbbinning = [140, 500, 7500]
VLQbinning = [140, 200, 6000]
JMbinning = [200, 0, 400]
PTbinning = [300, 0, 3000]
ETAbinning = [24, 0, 2.4]
f.cd()
#---------------------------------------------------------------------------------------------------------------------#
#nev = TH1F("nev",	"nev",		1, 0, 1 )


t32nm1  = TH1F("t32nm1",		"",     	  	      	24, 0, 1.0 )
tmassnm1  = TH1F("tmassnm1",		"",     	  	      	200, 0, 400 )
sjbtagnm1  = TH1F("sjbtagnm1",		"",     	  	      	24, 0, 1.0 )

eventcounter = TH1F("eventcounter",		"",     	  	      	15, -0.5, 14.5 )

hdbtagnm1  = TH1F("hdbtagnm1",		"",     	  	      	48, -1.0, 1.0 )
hmassnm1  = TH1F("hmassnm1",		"",     	  	      	200, 0, 400 )

btagnm1  = TH1F("btagnm1",		"",     	  	      	24, 0, 1.0)

BPmass = TH1F("BPmass",		"",     	  	      	140, 500, 8000 )
TPmass = TH1F("TPmass",		"",     	  	      	140, 500, 8000 )
WPmass = TH1F("WPmass",		"",     	  	      	140, 500, 8000 )

bmatch = TH1F("bmatch",		"",     	  	      	4, -0.5, 3.5 )
tmatch = TH1F("tmatch",		"",     	  	      	4, -0.5, 3.5 )
hmatch = TH1F("hmatch",		"",     	  	      	4, -0.5, 3.5 )


for i in range(0,2):
	for j in range(0,2):
		for k in range(0,2):
			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)] = {}
			for curunc in unclist:
		
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Mthb"+curunc]  = TH1F("Mthb"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	Mthbbinning[0], Mthbbinning[1], Mthbbinning[2] )
				#histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Mthb_Mbh"+curunc]  = TH2F("Mthb_Mbh"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	24, 500, 6000 ,24, 200, 6000   )
				#histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Mthb_Mth"+curunc]  = TH2F("Mthb_Mth"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	24, 500, 6000 ,24, 200, 6000   )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Mthbmatched"+curunc]  = TH1F("Mthbmatched"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	Mthbbinning[0], Mthbbinning[1], Mthbbinning[2] )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Mthbunmatched"+curunc]  = TH1F("Mthbunmatched"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	Mthbbinning[0], Mthbbinning[1], Mthbbinning[2] )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["MthbGENmatched"+curunc]  = TH1F("MthbGENmatched"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	Mthbbinning[0], Mthbbinning[1], Mthbbinning[2] )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["MthbGENunmatched"+curunc]  = TH1F("MthbGENunmatched"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	Mthbbinning[0], Mthbbinning[1], Mthbbinning[2] )


				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Mth"+curunc]  = TH1F("Mth"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	VLQbinning[0], VLQbinning[1], VLQbinning[2] )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Mbh"+curunc]  = TH1F("Mbh"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	VLQbinning[0], VLQbinning[1], VLQbinning[2] )

				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Mthmatched"+curunc]  = TH1F("Mthmatched"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	VLQbinning[0], VLQbinning[1], VLQbinning[2])
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Mbhmatched"+curunc]  = TH1F("Mbhmatched"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	VLQbinning[0], VLQbinning[1], VLQbinning[2])
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Mthunmatched"+curunc]  = TH1F("Mthunmatched"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	VLQbinning[0], VLQbinning[1], VLQbinning[2] )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Mbhunmatched"+curunc]  = TH1F("Mbhunmatched"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	VLQbinning[0], VLQbinning[1], VLQbinning[2] )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["MthGENmatched"+curunc]  = TH1F("MthGENmatched"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	VLQbinning[0], VLQbinning[1], VLQbinning[2] )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["MbhGENmatched"+curunc]  = TH1F("MbhGENmatched"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	VLQbinning[0], VLQbinning[1], VLQbinning[2] )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["MthGENunmatched"+curunc]  = TH1F("MthGENunmatched"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	VLQbinning[0], VLQbinning[1], VLQbinning[2] )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["MbhGENunmatched"+curunc]  = TH1F("MbhGENunmatched"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      VLQbinning[0], VLQbinning[1], VLQbinning[2] )




				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Mminpair"+curunc]  = TH1F("Mminpair"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	VLQbinning[0], VLQbinning[1], VLQbinning[2] )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Mt"+curunc]  = TH1F("Mt"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	JMbinning[0], JMbinning[1], JMbinning[2] )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Mh"+curunc]  = TH1F("Mh"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	JMbinning[0], JMbinning[1], JMbinning[2] )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Mugb"+curunc]  = TH1F("Mugb"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	JMbinning[0], JMbinning[1], JMbinning[2] )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Mugt"+curunc]  = TH1F("Mugt"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	JMbinning[0], JMbinning[1], JMbinning[2])
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Mugh"+curunc]  = TH1F("Mugh"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	JMbinning[0], JMbinning[1], JMbinning[2] )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Ptb"+curunc]  = TH1F("Ptb"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	PTbinning[0], PTbinning[1], PTbinning[2] )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Ptt"+curunc]  = TH1F("Ptt"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	PTbinning[0], PTbinning[1], PTbinning[2] )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Pth"+curunc]  = TH1F("Pth"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	PTbinning[0], PTbinning[1], PTbinning[2] )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Etab"+curunc]  = TH1F("Etab"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	ETAbinning[0], ETAbinning[1], ETAbinning[2] )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Etat"+curunc]  = TH1F("Etat"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	ETAbinning[0], ETAbinning[1], ETAbinning[2]  )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Etah"+curunc]  = TH1F("Etah"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	ETAbinning[0], ETAbinning[1], ETAbinning[2]  )

				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bindex"+curunc]  = TH1F("bindex"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	5, -0.5, 4.5 )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["tindex"+curunc]  = TH1F("tindex"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	5, -0.5, 4.5 )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["hindex"+curunc]  = TH1F("hindex"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	5, -0.5, 4.5 )


				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["CSV"+curunc]  = TH1F("CSV"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	40, 0, 1 )


				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["SJcsvMAXt"+curunc]  = TH1F("SJcsvMAXt"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	24, 0, 1.0 )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["tau32t"+curunc]  = TH1F("tau32t"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	24, 0, 1.0 )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["SJcsv1h"+curunc]  = TH1F("SJcsv1h"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	24, 0, 1.0 )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["SJcsv2h"+curunc]  = TH1F("SJcsv2h"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	24, 0, 1.0 )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["tau21h"+curunc]  = TH1F("tau21h"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	24, 0, 1.0 )


				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["DRs"+curunc]  = TH1F("DRs"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	24, 0, 5.0 )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Drap1"+curunc]  = TH1F("Drap1"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	24, 0, 5.0 )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Drap2"+curunc]  = TH1F("Drap2"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	24, 0, 5.0 )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Drapmin"+curunc]  = TH1F("Drapmin_"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	24, 0, 5.0 )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["DRAK4"+curunc]  = TH1F("DRAK4_"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	24, 0, 5.0 )

				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["DRAK8min"+curunc]  = TH1F("DRAK8min_"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	24, 0, 5.0 )
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["DRAK4min"+curunc]  = TH1F("DRAK4min_"+curunc+"_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	24, 0, 5.0 )


			if i==1:
				tagh["t"+str(j)+"b"+str(k)] = TagFile.Get("t0b"+str(k))
				tagh["t"+str(j)+"b"+str(k)+"unsub"] = TagFile.Get("t0b"+str(k)+"unsub")

				tagh["t"+str(j)+"b"+str(k)+"mthb"] = TagFile.Get("t0b"+str(k)+"mthb")
				tagh["t"+str(j)+"b"+str(k)+"unsub"+"mthb"] = TagFile.Get("t0b"+str(k)+"unsub"+"mthb")

				tagh["t"+str(j)+"b"+str(k)+"e1"] = TagFile.Get("t0b"+str(k)+"e1")
				tagh["t"+str(j)+"b"+str(k)+"e2"] = TagFile.Get("t0b"+str(k)+"e2")
				tagh["t"+str(j)+"b"+str(k)+"e1unsub"] = TagFile.Get("t0b"+str(k)+"e1unsub")
				tagh["t"+str(j)+"b"+str(k)+"e2unsub"] = TagFile.Get("t0b"+str(k)+"e2unsub")

				for pp in params:			
					for eb in ['','ebin']:
						if eb!='' and pp=='mthb':
							continue 
						for unc in bkguncs:
							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Mthb"+pp+eb+unc]  = TH1F("bkg_Mthb_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	Mthbbinning[0], Mthbbinning[1], Mthbbinning[2] )
							if unc =='up' or unc=='down':
								if eb=='ebin':
									nbins = TagFile.Get("t0b1e1").GetNbinsX()+TagFile.Get("t0b1e2").GetNbinsX()+2
									ebinstart = TagFile.Get("t0b1e1").GetNbinsX()+1

								else:
									nbins = TagFile.Get("t0b1").GetNbinsX()+1

								histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Mthb2d"+pp+eb+unc]  = TH2F("bkg_Mthb2d_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	nbins,0,nbins,Mthbbinning[0], Mthbbinning[1], Mthbbinning[2] )
								histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Mth2d"+pp+eb+unc]  = TH2F("bkg_Mth2d_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	nbins,0,nbins,VLQbinning[0], VLQbinning[1], VLQbinning[2] )
								histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Mbh2d"+pp+eb+unc]  = TH2F("bkg_Mbh2d_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	nbins,0,nbins,VLQbinning[0], VLQbinning[1], VLQbinning[2] )
								histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Mt2d"+pp+eb+unc]  = TH2F("bkg_Mt2d_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	nbins,0,nbins,JMbinning[0], JMbinning[1], JMbinning[2] )
								histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Mh2d"+pp+eb+unc]  = TH2F("bkg_Mh2d_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	nbins,0,nbins,JMbinning[0], JMbinning[1], JMbinning[2] )
								histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Ptb2d"+pp+eb+unc]  = TH2F("bkg_Ptb2d_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	nbins,0,nbins,PTbinning[0], PTbinning[1], PTbinning[2] )
								histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Ptt2d"+pp+eb+unc]  = TH2F("bkg_Ptt2d_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	nbins,0,nbins,PTbinning[0], PTbinning[1], PTbinning[2] )
								histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Pth2d"+pp+eb+unc]  = TH2F("bkg_Pth2d_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	nbins,0,nbins,PTbinning[0], PTbinning[1], PTbinning[2] )
								histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Etab2d"+pp+eb+unc]  = TH2F("bkg_Etab2d_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	nbins,0,nbins,ETAbinning[0], ETAbinning[1], ETAbinning[2]  )
								histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Etat2d"+pp+eb+unc]  = TH2F("bkg_Etat2d_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	nbins,0,nbins,ETAbinning[0], ETAbinning[1], ETAbinning[2]  )
								histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Etah2d"+pp+eb+unc]  = TH2F("bkg_Etah2d_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	nbins,0,nbins,ETAbinning[0], ETAbinning[1], ETAbinning[2]  )




							#histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Mthb_Mbh"+pp+eb+unc]  = TH2F("bkg_Mthb_Mbh_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	24, 500, 6000 ,24, 200, 6000   )
							#histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Mthb_Mth"+pp+eb+unc]  = TH2F("bkg_Mthb_Mth_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	24, 500, 6000 ,24, 200, 6000   )
							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Mth"+pp+eb+unc]  = TH1F("bkg_Mth_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	VLQbinning[0], VLQbinning[1], VLQbinning[2] )
							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Mbh"+pp+eb+unc]  = TH1F("bkg_Mbh_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	VLQbinning[0], VLQbinning[1], VLQbinning[2] )
							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Mminpair"+pp+eb+unc]  = TH1F("bkg_Mminpair_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	VLQbinning[0], VLQbinning[1], VLQbinning[2] )

							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Mb"+pp+eb+unc]  = TH1F("bkg_Mb_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	JMbinning[0], JMbinning[1], JMbinning[2] )
							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Mt"+pp+eb+unc]  = TH1F("bkg_Mt_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	JMbinning[0], JMbinning[1], JMbinning[2] )
							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Mh"+pp+eb+unc]  = TH1F("bkg_Mh_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	JMbinning[0], JMbinning[1], JMbinning[2])
							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Mugb"+pp+eb+unc]  = TH1F("bkg_Mugb_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	JMbinning[0], JMbinning[1], JMbinning[2])
							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Mugt"+pp+eb+unc]  = TH1F("bkg_Mugt_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	JMbinning[0], JMbinning[1], JMbinning[2] )
							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Mugh"+pp+eb+unc]  = TH1F("bkg_Mugh_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	JMbinning[0], JMbinning[1], JMbinning[2] )
						
							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Ptb"+pp+eb+unc]  = TH1F("bkg_Ptb_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	PTbinning[0], PTbinning[1], PTbinning[2] )
							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Ptt"+pp+eb+unc]  = TH1F("bkg_Ptt_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	PTbinning[0], PTbinning[1], PTbinning[2] )
							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Pth"+pp+eb+unc]  = TH1F("bkg_Pth_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	PTbinning[0], PTbinning[1], PTbinning[2] )
							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Etab"+pp+eb+unc]  = TH1F("bkg_Etab_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	ETAbinning[0], ETAbinning[1], ETAbinning[2]  )
							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Etat"+pp+eb+unc]  = TH1F("bkg_Etat_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	ETAbinning[0], ETAbinning[1], ETAbinning[2]  )
							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_Etah"+pp+eb+unc]  = TH1F("bkg_Etah_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	ETAbinning[0], ETAbinning[1], ETAbinning[2]  )

							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_bindex"+pp+eb+unc]  = TH1F("bkg_bindex_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	5, -0.5, 4.5 )
							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_tindex"+pp+eb+unc]  = TH1F("bkg_tindex_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	5, -0.5, 4.5 )
							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_hindex"+pp+eb+unc]  = TH1F("bkg_hindex_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	5, -0.5, 4.5 )


							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_DRAK8min"+pp+eb+unc]  = TH1F("bkg_DRAK8min_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	24, 0, 5.0 )
							histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bkg_DRAK4min"+pp+eb+unc]  = TH1F("bkg_DRAK4min_"+"h"+str(i)+"t"+str(j)+"b"+str(k)+pp+eb+unc,		"",     	  	      	24, 0, 5.0 )



			for ih in histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]:
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)][ih].Sumw2()

#---------------------------------------------------------------------------------------------------------------------#

# loop over events
#---------------------------------------------------------------------------------------------------------------------#

count = 0

print "Start looping"
#initialize the ttree variables



tree_vars = {"b_pt":array('d',[0.]),"b_btag":array('d',[0.]),"t_pt":array('d',[0.]),"t_mass":array('d',[0.]),"t_sjbtag":array('d',[0.]),"t_tau32":array('d',[0.]),"h_pt":array('d',[0.]),"h_mass":array('d',[0.]),"h_dbtag":array('d',[0.]),"h_tau21":array('d',[0.]), "m_thb":array('d',[0.]), "m_bh":array('d',[0.]), "m_th":array('d',[0.]), "tpart":array('d',[0.])  , "hpart":array('d',[0.])  , "bpart":array('d',[0.])  ,  "run":array('d',[0.]),"lumi":array('d',[0.]),"event":array('d',[0.]),"weight":array('d',[0.])}




for unc in unclist:
	tree_vars["weight_"+unc]=array('d',[0.])
	if unc.find('up')!=-1:
		tree_vars["weight_"+unc.replace('up','nom')]=array('d',[0.])

Tree = WPF.Make_Trees(tree_vars,"srTree")
	
Histoname = "TriggerWeight_"+tnamestr+"_pre_HLT_IsoMu24"

print "Loading ",Histoname, "from", di+"Triggerweight_singlemu.root"
TrigFile = TFile(di+"Triggerweight_singlemu.root")
TrigPlot = TrigFile.Get(Histoname)
	
QCDClosFile = TFile(di+"THBcorr_QCD__PSET_default.root")
QCDClosPlot = QCDClosFile.Get("QCDCorrFactor")



goodEvents = []



#btottestnom = 0 
#btottest = 0 

treearr = []
numtree = 0
for curf in TFs:

    if numtree==0:
    	fullnev = curf.Get('nev')
    else:
    	curnev = curf.Get('nev')
	fullnev.Add(curnev)
    treearr.append(curf.Get('Tree'))
    treedict = WPF.Inittree(treearr[-1])	
    for event in  treearr[-1]:





	    eventcountvar = 0.
	    eventcounter.Fill(eventcountvar)

	    normweight = 1.0
	    count	= 	count + 1
	    
	    # m = 0
	    # t = 0

	    #if count > 100000:
		#break

	    if count % 10000 == 0 :
	      print  '--------- Processing Event ' + str(count) +' (' + str(100*count/totevents) + '%)  --  dataset:', options.set

	    #Here we split up event processing based on number of jobs 
	    #This is set up to have jobs range from 1 to the total number of jobs (ie dont start at job 0)

	    if jobs != 1 and options.split=="event":
	    	if (count - 1) % jobs == 0:
			jobiter+=1
		count_index = count - (jobiter-1)*jobs
		if count_index!=num:
			continue 


	    eventcountvar += 1.
	    eventcounter.Fill(eventcountvar)
	    if True:

		AK4_ht 	= 	treedict["AK4_ht"+AK4mod][0]
	   
	    	if AK4_ht<1000.:
			continue


	    	hJetMass 	= 	treedict["AK8_SDMhiggs"]

		AK8_sdmassscale 	= 	[1.0]*len(hJetMass)
		if mod!="" and mod.find("M")!=-1 :
			AK8_sdmassscale 	= 	treedict["AK8_"+mod]


	   	hJetMass = array('d',[hJetMass[nn]*AK8_sdmassscale[nn] for nn in xrange(len(hJetMass))])

	    	topJetMassuncorr 	= 	treedict["AK8_SDMtop"]
	    	AK8CSVMAX 	= 	treedict["AK8_sjbtag"]
	    	jetAK8DoubleBAK8	= 	treedict["AK8_dbtag"]
		#jetAK8DoubleBAK8	= 	[0.9,0.9,0.9,0.9,0.9]
		tau21val	= 	treedict["AK8_tau21"]
		tau32val	= 	treedict["AK8_tau32"]
	    	bJetBDiscAK4 	= 	treedict["AK4_btag"]

		eventcountvar += 1.
		eventcounter.Fill(eventcountvar)

		bind = []
		hind = []
		ahind = []
		tind = [] 
		atind = [] 


		NM1 = []

		AK8_pt 	= 	treedict["AK8_pt"]
		AK8_ptscale 	= 	[1.0]*len(AK8_pt)
		if mod!="" and mod.find("M")==-1 :
			AK8_ptscale 	= 	treedict["AK8_"+mod]
			#print AK8_ptscale
			#print treedict["AK8_"+mod]
		#print "pr",AK8_pt
	   	AK8_pt = array('d',[AK8_pt[nn]*AK8_ptscale[nn] for nn in xrange(len(AK8_pt))])
		#print "po",AK8_pt

		AK8_eta = 	treedict["AK8_eta"]
		AK8_phi = 	treedict["AK8_phi"]

		AK8_M 	= 	treedict["AK8_M"]
	   	AK8_M = array('d',[AK8_M[nn]*AK8_ptscale[nn] for nn in xrange(len(AK8_M))])
		AK8LV = []



		#start = time.time()




		for ijet in xrange(len(AK8_pt)):
		
	    	
			NM1.append({})
			NM1[-1]['hmass'] = False
			NM1[-1]['ahmass'] = False
			NM1[-1]['hdbtag'] = False
			NM1[-1]['htau21'] = False
			NM1[-1]['tmass'] = False
			NM1[-1]['tbtag'] = False
			NM1[-1]['ttau32'] = False

			if AK8_pt[ijet]<0.:

				AK8LV.append(None)
				continue
			AK8LV.append(TLorentzVector())
			AK8LV[-1].SetPtEtaPhiM(AK8_pt[ijet],AK8_eta[ijet],AK8_phi[ijet],AK8_M[ijet])

			if abs(AK8LV[ijet].Eta())>2.4:
				continue 


			SJ_csvmax = AK8CSVMAX[ijet]

			if pttcut[0]<AK8LV[ijet].Perp()<pttcut[1]:
				if tmass[0]<topJetMassuncorr[ijet]<tmass[1]:
					NM1[-1]['tmass'] = True
				if sjbtagt[0]<SJ_csvmax<=sjbtagt[1]:
					NM1[-1]['tbtag'] = True
				if tau32[0]<=tau32val[ijet]<tau32[1]:
					NM1[-1]['ttau32'] = True

				if tau32tight[0]<=tau32val[ijet]<tau32tight[1]:
					NM1[-1]['ttau32tight'] = True

				if NM1[-1]['tmass'] and NM1[-1]['tbtag'] and NM1[-1]['ttau32']:
					tind.append(ijet)

				
			if pthcut[0]<AK8LV[ijet].Perp()<pthcut[1]:


				if hmassinvert[0]<hJetMass[ijet]<hmassinvert[1]:
					NM1[-1]['ahmass'] = True
		

				if hmass[0]<hJetMass[ijet]<hmass[1] :
					NM1[-1]['hmass'] = True
				hdbbool= (sjbtagh[0]<jetAK8DoubleBAK8[ijet]<=sjbtagh[1])
				if hdbbool:
					NM1[-1]['hdbtag'] = True

				hdbboolloose= (sjbtaghloose[0]<jetAK8DoubleBAK8[ijet]<=sjbtaghloose[1])
				if hdbboolloose:
					NM1[-1]['hdbtagloose'] = True

				tau21_cut =  tau21[0]<=tau21val[ijet]<tau21[1]
				if tau21_cut:
					NM1[-1]['htau21'] = True

	
				if NM1[-1]['hmass'] and NM1[-1]['hdbtag'] and NM1[-1]['htau21']:
					hind.append(ijet)


				if NM1[-1]['ahmass'] and NM1[-1]['htau21']:
					ahind.append(ijet)


		if len(NM1)<3:
			continue
		for NM in range(0,2):
			if NM==0:
				ind0 = 0
				ind1 = 1
			if NM==1:
				ind0 = 1
				ind1 = 0
			if NM1[ind0]['hmass'] and NM1[ind0]['hdbtag']  and not (NM1[ind1]['hmass'] and NM1[ind1]['hdbtag'] and NM1[ind1]['htau21']):
				if NM1[ind1]['tmass'] and NM1[ind1]['tbtag']:
					#print tau32val
					#print tau32val[ind1]
					t32nm1.Fill(tau32val[ind1])
				if NM1[ind1]['ttau32'] and NM1[ind1]['tbtag']:
					tmassnm1.Fill(topJetMassuncorr[ind1])
				if NM1[ind1]['tmass'] and NM1[ind1]['ttau32']:
					sjbtagnm1.Fill(AK8CSVMAX[ind1])
			

			if NM1[ind0]['tmass'] and NM1[ind0]['tbtag'] and NM1[ind0]['ttau32'] and not (NM1[ind0]['hmass'] and NM1[ind0]['hdbtag'] and NM1[ind0]['htau21']):
				if NM1[ind1]['hdbtag']:
					hmassnm1.Fill(hJetMass[ind1])
				if NM1[ind1]['hmass']:
					hdbtagnm1.Fill(jetAK8DoubleBAK8[ind1])
			


		preort,poort,overlapht = False,False,False
		if len(tind)>=1:
			temptind = tind
			temphind = hind
			tempahind = ahind
			preort = True
		
		hind,tind  =  WPF.select([hind,tind])
		ahind,tind  =  WPF.select([ahind,tind])
		hind,atind  =  WPF.select([hind,atind])
		ahind,atind  =  WPF.select([ahind,atind])


		
		
		if len(tind)>=1:
			poort = True

		if preort and not poort:
			overlapht = True


		eventcountvar += 1.
		eventcounter.Fill(eventcountvar)

	
		defs = {}


		random.seed(treedict["event"][0]) 
		if len(hind)>0:
			random.shuffle(hind)
			hind=[hind[0]]
			defs['h']=hind[0]
		if len(tind)>0:
			random.shuffle(tind)
			tind=[tind[0]]
			defs['t']=tind[0]

		if len(tind)==0 and len(atind)>0:
			random.shuffle(atind)
			atind=[atind[0]]
			defs['t']=atind[0]

		if len(hind)==0 and len(ahind)>0:
			random.shuffle(ahind)
			ahind = [ahind[0]]
			defs['h']=ahind[0]
		if len(hind)==0 and len(ahind)==0:
			continue
		
		if len(tind)==0 and len(atind)==0:
			continue





		AK4LV = []
		AK4array = []
		AK4_pt 	= 	treedict["AK4_pt"]
		AK4_ptscale 	= 	[1.0]*len(AK4_pt)
		if AK4mod!="":
			AK4_ptscale 	= 	treedict["AK4_"+AK4mod]



	   	AK4_pt = array('d',[AK4_pt[nn]*AK4_ptscale[nn] for nn in xrange(len(AK4_pt))])


		AK4_eta 	= 	treedict["AK4_eta"]
		AK4_phi 	= 	treedict["AK4_phi"]
		AK4_M 		= 	treedict["AK4_M"]
	   	AK4_M = array('d',[AK4_M[nn]*AK4_ptscale[nn] for nn in xrange(len(AK4_M))])



		for iAK4 in xrange(len(AK4_pt)):

			if AK4_pt[iAK4]<0.:
				AK4LV.append(None)
				continue 

			AK4LV.append(TLorentzVector())
			AK4LV[-1].SetPtEtaPhiM(AK4_pt[iAK4],AK4_eta[iAK4],AK4_phi[iAK4],AK4_M[iAK4])

			if (ptbcut[0]<AK4LV[iAK4].Perp()<ptbcut[1]) and abs(AK4LV[iAK4].Eta())<2.4:
				overlap=False
				for key in defs:
					if AK4LV[iAK4].DeltaR(AK8LV[defs[key]])<1.2:
						overlap=True
				if not overlap:
					AK4array.append(iAK4)



		correctindex = 9999
		bind= []
		abind= []
		AK4_btag 	= 	treedict["AK4_btag"]
		for AK4index in AK4array:

			if btag[0]<AK4_btag[AK4index]<btag[1]:
				bind.append(AK4index)
			else:
				abind.append(AK4index)
			


		if len(bind)>0:
			#if len(defs)==2:

			#	btottest += 1 
				#if len(bind)>1:	
				#	btottestnom += 1 
				#	print "defs",defs
				#	print "len(bind)",len(bind)
				#	print 100.*float(btottestnom)/float(btottest)
			random.shuffle(bind)
			bind=[bind[0]]
			defs['b']=bind[0]
		if len(bind)==0 and len(abind)>0:

			random.shuffle(abind)
			abind=[abind[0]]
			defs['b']=abind[0]

	
		if len(defs)<3:
			continue 


		eventcountvar += 1.
		eventcounter.Fill(eventcountvar)



		if NM1[defs['t']]['tmass'] == True:
			eventcountvar += 1.
			eventcounter.Fill(eventcountvar)
			if NM1[defs['t']]['tbtag'] == True:
				eventcountvar += 1.
				eventcounter.Fill(eventcountvar)
				if NM1[defs['t']]['ttau32'] == True:
					eventcountvar += 1.
					eventcounter.Fill(eventcountvar)
					if NM1[defs['h']]['hmass'] == True:
						eventcountvar += 1.
						eventcounter.Fill(eventcountvar)
						if NM1[defs['h']]['hdbtag'] == True:
							eventcountvar += 1.
							eventcounter.Fill(eventcountvar)
							if NM1[defs['h']]['htau21'] == True:
								eventcountvar += 1.
								eventcounter.Fill(eventcountvar)
								if len(bind)==1:
									eventcountvar += 1.
									eventcounter.Fill(eventcountvar)	


							
		thb =  AK8LV[defs['t']] + AK8LV[defs['h']] + AK4LV[defs['b']]

		triggerweight = 1.0


		uncweight={}
		nomweight={}
		for unc in unclist:
			uncweight[unc]=1.0
			if unc.find('up')!=-1:
				nomweight[unc.replace('up','nom')]=1.0
	

		puweight = 1.0
		puweightup = 1.0
		puweightdown = 1.0
	
		ptw=1.0
		tpart,hpart,bpart = -1,-1,-1
		if options.set.find('data')==-1:



	   			pflavsAK4 	= 	treedict["AK4_flav"]
	   			pflavsAK8 	= 	treedict["AK8_flav"]

				tpart = pflavsAK8[defs['t']]
				hpart = pflavsAK8[defs['h']]
				bpart = pflavsAK4[defs['b']]

				if options.set.find('THB')!=-1 and ( (len(tind)==1) and (len(hind)==1) and (len(bind)==1) ): 
					genmatches = {}
					genmatchedlvs = {}
					convo = {'25':'h','5':'b','6':'t'}
					
					genmatches['h']=hpart
					genmatches['t']=tpart
					genmatches['b']=bpart
					for genmatch in genmatches:
						if str(abs(int(genmatches[genmatch]))) not in convo:
							continue
						if genmatch=='h':
							entry=0
						if genmatch=='t':
							entry=1
						if genmatch=='b':
							entry=2
						if convo[str(abs(int(genmatches[genmatch])))]=='h':
							hmatch.Fill(entry)
						if convo[str(abs(int(genmatches[genmatch])))]=='t':
							tmatch.Fill(entry)
						if convo[str(abs(int(genmatches[genmatch])))]=='b':
							bmatch.Fill(entry)
							
				if options.ptreweight!='off' and options.set.find('ttbar')!=-1:
					ptw = treedict["weight_Tpt"][0]
				


				#CHECK (pu dist correct)
				if options.pileup!='off':
			

					puweight = treedict["weight_PU"][0]
					puweightup = treedict["weight_PUup"][0]
					puweightdown = treedict["weight_PUdown"][0]
					nomweight['PUnom']=puweight
					uncweight['PUup']=puweightup
					uncweight['PUdown']=puweightdown


		CurrTrigPlot  =  TrigPlot
		if options.set.find('data')==-1:
			if tnamestr!='none':
				triggerweight = WPF.Trigger_Lookup(AK4_ht,CurrTrigPlot)
			
				uncweight['Trigup'] = triggerweight[1]
				uncweight['Trigdown'] =  triggerweight[2]
				nomweight['Trignom'] =  triggerweight[0]	
	
			#Here, apply top/W sf
			if options.set.find('ttbar')!=-1 or options.set.find('THB')!=-1:

				if len(tind)!=0:
					normweight*=1.07



				uncweight['PDFup'] = treedict["weight_PDFup"][0]	
				uncweight['PDFdown'] = treedict["weight_PDFdown"][0]	

				uncweight['Q2up'] = treedict["weight_Q2up"][0]
				uncweight['Q2down'] = treedict["weight_Q2down"][0]
				

				if len(bind)!=0:
				


					uncweight['Bup']=treedict["AK4_weight_Bup"][defs['b']]
					uncweight['Bdown']=treedict["AK4_weight_Bdown"][defs['b']]
					nomweight['Bnom']=treedict["AK4_weight_B"][defs['b']]
				

					uncweight['Bmisup']=treedict["AK4_weight_Bmisup"][defs['b']]
					uncweight['Bmisdown']=treedict["AK4_weight_Bmisdown"][defs['b']]
					nomweight['Bmisnom']=treedict["AK4_weight_Bmis"][defs['b']]

					
				#Should do differently
				Asweights_proc = WPF.as_Lookup([treedict["weight_Alpup"][0],treedict["weight_Alpdown"][0]])


				uncweight['Alpup']=Asweights_proc[1]
				uncweight['Alpdown']=Asweights_proc[0]

	
				if len(hind)!=0:
					
					nomweight['Htagnom']=treedict["AK8_weight_Htag"][defs['h']]
	       	 			uncweight['Htagup']=treedict["AK8_weight_Htagup"][defs['h']]
	       	 			uncweight['Htagdown']=treedict["AK8_weight_Htagdown"][defs['h']]

					nomweight['Hmistagnom']=treedict["AK8_weight_Hmistag"][defs['h']]
	       	 			uncweight['Hmistagup']=treedict["AK8_weight_Hmistagup"][defs['h']]
	       	 			uncweight['Hmisdown']=treedict["AK8_weight_Hmistagdown"][defs['h']]
				

					#print 
					#print treedict["AK8_weight_Htag"][defs['h']]
	       	 			#print treedict["AK8_weight_Htagup"][defs['h']]
	       	 			#print treedict["AK8_weight_Htagdown"][defs['h']]

					#print treedict["AK8_weight_Hmistag"][defs['h']]
	       	 			#print treedict["AK8_weight_Hmistagup"][defs['h']]
	       	 			#print treedict["AK8_weight_Hmistagdown"][defs['h']]
				

					if options.set.find('THB')!=-1: 
							Hpt = AK8LV[defs['h']].Perp()
							delta=0.054*math.log(Hpt/200.0)
	       	 					uncweight['WExup']+=delta
							uncweight['WExdown']-=delta
						
				if options.set.find('ttbar')!=-1:
					uncweight['Tptdown']=1.0
					nomweight['Tptnom']=ptw
					uncweight['Tptup']=max(0.0,(1.0-2.0*(1.0-ptw)))

		isinvertedtop=False


		#CHECK
		flatnomweight = normweight
		for nom in nomweight:
			flatnomweight*=nomweight[nom]
		
		

		mindr = 999.0
		AK8defs = {}
		AK8defs['t'] = defs['t']
		AK8defs['h'] = defs['h']
		for aa in AK8defs:
			for bb in AK8defs:
				if aa!=bb:
					curdr = AK8LV[AK8defs[aa]].DeltaR(AK8LV[AK8defs[bb]])
					mindr = min(curdr,mindr)
					histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['DRs'].Fill(AK8LV[defs[aa]].DeltaR(AK8LV[defs[bb]]),flatnomweight)
		if mindr<1.8:
			continue 
		mindrak4 = 999.0
		for aa in AK8defs:
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['DRAK4'].Fill(AK4LV[defs['b']].DeltaR(AK8LV[AK8defs[aa]]),flatnomweight)
			mindrak4 = min(AK4LV[defs['b']].DeltaR(AK8LV[AK8defs[aa]]),mindrak4)



		if len(hind)==0 and (hmassinvert[0]<hJetMass[defs['h']]<hmassinvert[1]):
			for pp in params:		
				for etar in ['','e1','e2']:
					if etar!='' and pp=='mthb':
						continue 
					for unc in bkguncs:
						if etar == 'e1':
							if abs(AK8LV[defs['h']].Eta())>=1.0:
								continue
						if etar == 'e2':
							if abs(AK8LV[defs['h']].Eta())<1.0:
								continue


						fakehiggsmass = 128.
						bkgfakehiggs = copy.copy(AK8LV[defs['h']])
						bkgfakehiggs.SetPtEtaPhiM(AK8LV[defs['h']].Perp(),AK8LV[defs['h']].Eta(),AK8LV[defs['h']].Phi(),fakehiggsmass)

						thbfake =  AK8LV[defs['t']] + bkgfakehiggs + AK4LV[defs['b']]


						if pp=='mthb':
							hvar = thbfake.M()
						else:
							hvar = AK8LV[defs['h']].Perp()
						TP = tagh["t"+str(len(tind))+"b"+str(len(bind)) + etar+pp]

						etab = ""
						if etar!='':
							etab = "ebin"

						hrate = TP.GetBinContent(TP.FindBin(hvar))
						if unc == 'up':
							#if len(tind)==1 and len(bind)==1:
							#	print 
							#	print hrate
							#	print AK8LV[defs['h']].Perp()
							#	print TP.GetBinErrorUp(TP.FindBin(AK8LV[defs['h']].Perp()))/hrate
							hrate += TP.GetBinErrorUp(TP.FindBin(hvar))

						if unc == 'down':
							hrate -= TP.GetBinErrorLow(TP.FindBin(hvar))
						if unc == 'Mup':
							fakehiggsmass = 141.
						if unc == 'Mdown':
							fakehiggsmass = 115.
						if unc == 'ttup':
							TPu = tagh["t"+str(len(tind))+"b"+str(len(bind)) + etar+"unsub"+pp]
							hrateu = TPu.GetBinContent(TP.FindBin(hvar))
							hrate += (hrateu-hrate)

						if unc == 'ttdown':
							TPu = tagh["t"+str(len(tind))+"b"+str(len(bind)) + etar+"unsub"+pp]
							hrate = TP.GetBinContent(TP.FindBin(hvar))
							hrate -= (hrateu-hrate)
						closunc = WPF.Nonclosure(thbfake.M(),QCDClosPlot)
						if unc == 'closup':
							hrate *= (1+closunc)
							
						if unc == 'closdown':
							hrate *= (1-closunc)

						hratebin = TP.FindBin(hvar)
						if etar=='e2':
							hratebin+=ebinstart

						#if  len(tind)==0 and len(bind)==1 and unc=='':
						#	print "t",tind,"h",hind,"b",bind
						#	print TP
						#	print hrate
						#	print hvar
						hrate = max(0.0,hrate)
						histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Mthb'+pp+etab+unc].Fill(thbfake.M(),hrate*flatnomweight)
						if unc=='up':
							hrateunc = TP.GetBinErrorUp(TP.FindBin(hvar))




						if unc=='down':
							hrateunc = TP.GetBinErrorLow(TP.FindBin(hvar))


						if unc=='up' or unc=='down':
							#print hrateunc
							#print flatnomweight
							#print hrateunc*flatnomweight
							histosets["h1t"+str(len(tind))+"b"+str(len(bind))]["bkg_Mthb2d"+pp+etab+unc].Fill(hratebin,thbfake.M(),hrateunc*flatnomweight)

							histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Mbh2d'+pp+etab+unc].Fill(hratebin,(bkgfakehiggs+AK4LV[defs['b']]).M(),hrateunc*flatnomweight)
							histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Mth2d'+pp+etab+unc].Fill(hratebin,(bkgfakehiggs+AK8LV[defs['t']]).M(),hrateunc*flatnomweight)
							histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Mh2d'+pp+etab+unc].Fill(hratebin,hJetMass[defs['h']],hrateunc*flatnomweight)
							histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Mt2d'+pp+etab+unc].Fill(hratebin,topJetMassuncorr[defs['t']],hrateunc*flatnomweight)
							histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Pth2d'+pp+etab+unc].Fill(hratebin,bkgfakehiggs.Perp(),hrateunc*flatnomweight)
							histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Ptb2d'+pp+etab+unc].Fill(hratebin,AK4LV[defs['b']].Perp(),hrateunc*flatnomweight)
							histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Ptt2d'+pp+etab+unc].Fill(hratebin,AK8LV[defs['t']].Perp(),hrateunc*flatnomweight)
							histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Etah2d'+pp+etab+unc].Fill(hratebin,abs(bkgfakehiggs.Eta()),hrateunc*flatnomweight)
							histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Etab2d'+pp+etab+unc].Fill(hratebin,abs(AK4LV[defs['b']].Eta()),hrateunc*flatnomweight)
							histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Etat2d'+pp+etab+unc].Fill(hratebin,abs(AK8LV[defs['t']].Eta()),hrateunc*flatnomweight)


						#histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Mthb_Mbh'+pp+etab+unc].Fill(thbfake.M(),(bkgfakehiggs+AK4LV[defs['b']]).M(),hrate*flatnomweight)
						#histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Mthb_Mth'+pp+etab+unc].Fill(thbfake.M(),(bkgfakehiggs+AK8LV[defs['t']]).M(),hrate*flatnomweight)
						histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Mbh'+pp+etab+unc].Fill((bkgfakehiggs+AK4LV[defs['b']]).M(),hrate*flatnomweight)
						histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Mth'+pp+etab+unc].Fill((bkgfakehiggs+AK8LV[defs['t']]).M(),hrate*flatnomweight)
						histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Mminpair'+pp+etab+unc].Fill(min((AK8LV[defs['h']]+AK8LV[defs['t']]).M(),(AK8LV[defs['h']]+AK4LV[defs['b']]).M()),hrate*flatnomweight)
				


						histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Mh'+pp+etab+unc].Fill(hJetMass[defs['h']],hrate*flatnomweight)
						histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Mt'+pp+etab+unc].Fill(topJetMassuncorr[defs['t']],hrate*flatnomweight)


						histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Mugh'+pp+etab+unc].Fill(bkgfakehiggs.M(),hrate*flatnomweight)
						histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Mugb'+pp+etab+unc].Fill(AK4LV[defs['b']].M(),hrate*flatnomweight)
						histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Mugt'+pp+etab+unc].Fill(AK8LV[defs['t']].M(),hrate*flatnomweight)


						histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Pth'+pp+etab+unc].Fill(bkgfakehiggs.Perp(),hrate*flatnomweight)
						histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Ptb'+pp+etab+unc].Fill(AK4LV[defs['b']].Perp(),hrate*flatnomweight)
						histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Ptt'+pp+etab+unc].Fill(AK8LV[defs['t']].Perp(),hrate*flatnomweight)
						histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Etah'+pp+etab+unc].Fill(abs(bkgfakehiggs.Eta()),hrate*flatnomweight)
						histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Etab'+pp+etab+unc].Fill(abs(AK4LV[defs['b']].Eta()),hrate*flatnomweight)
						histosets["h1t"+str(len(tind))+"b"+str(len(bind))]['bkg_Etat'+pp+etab+unc].Fill(abs(AK8LV[defs['t']].Eta()),hrate*flatnomweight)




						histosets["h1t"+str(len(tind))+"b"+str(len(bind))]["bkg_bindex"+pp+etab+unc].Fill(defs['b'],hrate*flatnomweight)
						histosets["h1t"+str(len(tind))+"b"+str(len(bind))]["bkg_tindex"+pp+etab+unc].Fill(defs['t'],hrate*flatnomweight)
						histosets["h1t"+str(len(tind))+"b"+str(len(bind))]["bkg_hindex"+pp+etab+unc].Fill(defs['h'],hrate*flatnomweight)



						histosets["h1t"+str(len(tind))+"b"+str(len(bind))]["bkg_DRAK8min"+pp+etab+unc].Fill(mindr,hrate*flatnomweight)
						histosets["h1t"+str(len(tind))+"b"+str(len(bind))]["bkg_DRAK4min"+pp+etab+unc].Fill(mindrak4,hrate*flatnomweight)






			#print "applying weights"
			#print "h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))
			#print "uncweight",uncweight
			#print "nomweight",nomweight

		#print "bind,tind,hind",bind,tind,hind
		for unc in unclist:
			curweight = normweight
			for nom in nomweight:
				#if unc == '':
					#print nom,nomweight[nom]
				if (unc==nom.replace('nom','up')) or (unc==nom.replace('nom','down')):

					curweight*=uncweight[unc]
					continue 
				curweight*=nomweight[nom]
			#if unc == '':
				#print curweight
			weightFull=curweight

			#print unc,weightFull

			if options.set.find('data')!=-1:
				if weightFull!=1.0:
					print "DATA WITH NON UNITY WEIGHT ", weight



			if unc == "overlap":
				if not overlapht:		
					continue


			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Mthb'+unc].Fill(thb.M(),weightFull)
			#histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Mthb_Mbh'+unc].Fill(thb.M(),(AK8LV[defs['h']]+AK4LV[defs['b']]).M(),weightFull)
			#histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Mthb_Mth'+unc].Fill(thb.M(),(AK8LV[defs['h']]+AK8LV[defs['t']]).M(),weightFull)
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Mbh'+unc].Fill((AK8LV[defs['h']]+AK4LV[defs['b']]).M(),weightFull)
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Mth'+unc].Fill((AK8LV[defs['h']]+AK8LV[defs['t']]).M(),weightFull)
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]["Mminpair"+unc].Fill(min((AK8LV[defs['h']]+AK8LV[defs['t']]).M(),(AK8LV[defs['h']]+AK4LV[defs['b']]).M()),weightFull)

			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Mh'+unc].Fill(hJetMass[defs['h']],weightFull)
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Mt'+unc].Fill(topJetMassuncorr[defs['t']],weightFull)

			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Mugh'+unc].Fill(AK8LV[defs['h']].M(),weightFull)
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Mugb'+unc].Fill(AK4LV[defs['b']].M(),weightFull)
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Mugt'+unc].Fill(AK8LV[defs['t']].M(),weightFull)

			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['CSV'+unc].Fill(bJetBDiscAK4[defs['b']],weightFull)


			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Pth'+unc].Fill(AK8LV[defs['h']].Perp(),weightFull)
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Ptb'+unc].Fill(AK4LV[defs['b']].Perp(),weightFull)
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Ptt'+unc].Fill(AK8LV[defs['t']].Perp(),weightFull)
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Etah'+unc].Fill(abs(AK8LV[defs['h']].Eta()),weightFull)
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Etab'+unc].Fill(abs(AK4LV[defs['b']].Eta()),weightFull)
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Etat'+unc].Fill(abs(AK8LV[defs['t']].Eta()),weightFull)


			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]["DRAK8min"+unc].Fill(mindr,weightFull)
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]["DRAK4min"+unc].Fill(mindrak4,weightFull)



			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]["bindex"+unc].Fill(defs['b'],weightFull)
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]["tindex"+unc].Fill(defs['t'],weightFull)
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]["hindex"+unc].Fill(defs['h'],weightFull)




			Drap1 = abs((AK8LV[defs['t']]+AK8LV[defs['h']]).Rapidity() - AK4LV[defs['b']].Rapidity())
			Drap2 = abs((AK4LV[defs['b']]+AK8LV[defs['h']]).Rapidity() - AK8LV[defs['t']].Rapidity())
			Drapmin = min(Drap1,Drap2)
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]["Drap1"+unc].Fill(Drap1,weightFull)
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]["Drap2"+unc].Fill(Drap2,weightFull)
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]["Drapmin"+unc].Fill(Drapmin,weightFull)

			ttau32 = tau32val[defs['t']]

			tmaxsjcsv = AK8CSVMAX[defs['t']]
			htau21 = tau21val[defs['h']]


			try:
				histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]["SJcsvMAXt"+unc].Fill(tmaxsjcsv,weightFull)
			except:
				print "no subjet"

			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]["tau32t"+unc].Fill(ttau32,weightFull)
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]["tau21h"+unc].Fill(htau21,weightFull)  	  	 



		#THE REST JUST FILLS THE DEBUG TREE
		if (len(hind) == 1) and (len(tind) == 1) and (len(bind)==1):


			#n11+=1
			#print n11 , 	treedict["event"]

			temp_variables = {
					"b_pt":AK4LV[defs['b']].Perp(),
					"m_thb":thb.M(),
					"m_bh":(AK8LV[defs['h']]+AK4LV[defs['b']]).M(),
					"m_th":(AK8LV[defs['h']]+AK8LV[defs['t']]).M(),
					"b_btag":bJetBDiscAK4[defs['b']],
					"t_pt":AK8LV[defs['t']].Perp(),
					"t_mass":topJetMassuncorr[defs['t']],
					"t_sjbtag":tmaxsjcsv,
					"t_tau32":ttau32,    
					"h_pt":AK8LV[defs['h']].Perp(),
					"h_mass":hJetMass[defs['h']],
					"h_dbtag":jetAK8DoubleBAK8[defs['h']],
					"h_tau21":htau21,    
					"bpart":bpart,
					"hpart":hpart,
					"tpart":tpart,
					"run":treedict["run"][0],
					"lumi":treedict["lumi"][0],
					"event":treedict["event"][0],
					"weight":flatnomweight
				}

			for var in tree_vars:
				#print var
				if var.find("weight_")!=-1:
					#print "found ",var
					if var.find('nom')!=-1:
						#print "nominal = ", nomweight[var.replace("weight_","")]
						temp_variables[var]=nomweight[var.replace("weight_","")]
					else:	
						#print "NOT nominal = ", uncweight[var.replace("weight_","")]
						temp_variables[var]=uncweight[var.replace("weight_","")]

			#print temp_variables
			for tv in tree_vars.keys():
				#print tv
				tree_vars[tv][0] = temp_variables[tv]
			#print tree_vars
			Tree.Fill()


    numtree += 1

f.cd()
fullnev.Write()
f.Write()
f.Close()
print "number of events: " + str(count)


