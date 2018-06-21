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
import glob
import math
from math import sqrt,exp
import ROOT
from ROOT import std,ROOT,TFile,TLorentzVector,TMath,gROOT, TF1,TH1F,TH1D,TH2F,TH2D
from ROOT import TVector
from ROOT import TFormula

import sys
from DataFormats.FWLite import Events, Handle
from optparse import OptionParser
from array import *

parser = OptionParser()

parser.add_option('-s', '--set', metavar='F', type='string', action='store',
                  default	=	'data',
                  dest		=	'set',
                  help		=	'dataset (ie data,ttbar etc)')

parser.add_option('-C', '--coll', metavar='F', type='string', action='store',
                  default	=	'Puppi',
                  dest		=	'coll',
                  help		=	'CHS or Puppi')

parser.add_option('-u', '--ptreweight', metavar='F', type='string', action='store',
                  default	=	'none',
                  dest		=	'ptreweight',
                  help		=	'on or off')

parser.add_option('-n', '--num', metavar='F', type='string', action='store',
                  default	=	'all',
                  dest		=	'num',
                  help		=	'job number')
parser.add_option('-j', '--jobs', metavar='F', type='string', action='store',
                  default	=	'1',
                  dest		=	'jobs',
                  help		=	'number of jobs')
parser.add_option('-g', '--grid', metavar='F', type='string', action='store',
                  default	=	'off',
                  dest		=	'grid',
                  help		=	'running on grid off or on')
parser.add_option('-S', '--split', metavar='F', type='string', action='store',
                  default	=	'file',
                  dest		=	'split',
                  help		=	'split by event of file')

parser.add_option('-b', '--bx', metavar='F', type='string', action='store',
                  default	=	'25ns',
                  dest		=	'bx',
                  help		=	'bunch crossing 50ns or 25ns')



parser.add_option('-J', '--JES', metavar='F', type='string', action='store',
                  default	=	'nominal',
                  dest		=	'JES',
                  help		=	'nominal, up, or down')
parser.add_option('-R', '--JER', metavar='F', type='string', action='store',
                  default	=	'nominal',
                  dest		=	'JER',
                  help		=	'nominal, up, or down')

parser.add_option('-t', '--tname', metavar='F', type='string', action='store',
                  default	=	'HLT_PFHT900,HLT_PFHT800,HLT_JET450',
                  dest		=	'tname',
                  help		=	'trigger name')

parser.add_option('-p', '--pretname', metavar='F', type='string', action='store',
                  default	=	'HLT_PFHT475,HLT_JET260',
                  dest		=	'pretname',
                  help		=	'prescaled trigger name')

parser.add_option('-c', '--cuts', metavar='F', type='string', action='store',
                  default	=	'default',
                  dest		=	'cuts',
                  help		=	'Cuts type (ie default, rate, etc)')

(options, args) = parser.parse_args()

tname = options.tname.split(',')
tnamestr = ''
for iname in range(0,len(tname)):
	tnamestr+=tname[iname]
	if iname!=len(tname)-1:
		tnamestr+='OR'
	


pretname = options.pretname.split(',')
pretnamestr = ''
for iname in range(0,len(pretname)):
	pretnamestr+=pretname[iname]
	if iname!=len(pretname)-1:
		pretnamestr+='OR'
	





gROOT.Macro("rootlogon.C")

import WprimetoVlq_Functions	
from WprimetoVlq_Functions import *
WPF = WprimetoVlq_Functions(options.cuts,options.coll)
#Load up cut values based on what selection we want to run 
Cuts = WPF.LoadCuts



gROOT.Macro("rootlogon.C")
#Load up cut values based on what selection we want to run 
ptmincut = Cuts['ptmincut']
pthcut = Cuts['pthcut']
pttcut = Cuts['pttcut']
ptbcut = Cuts['ptbcut']
tmass = Cuts['tmass']
tau32 = Cuts['tau32']
sjbtagt = Cuts['sjbtagt']
sjbtagh = Cuts['sjbtagh']
bmass = Cuts['bmass']
btag = Cuts['btag']
hmass = Cuts['hmass']
tau21 = Cuts['tau21']

print "Options summary"
print "=================="
for  opt,value in options.__dict__.items():
	#print str(option)+ ": " + str(options[option]) 
	print str(opt) +': '+ str(value)
print "=================="
print ""

#If running on the grid we access the script within a tarred directory
di = ""
if options.grid == 'on':
	di = "tardir/"
	sys.path.insert(0, 'tardir/')


#For large datasets we need to parallelize the processing
jobs=int(options.jobs)
if jobs != 1:
	num=int(options.num)
	jobs=int(options.jobs)
	print "Running over " +str(jobs)+ " jobs"
	print "This will process job " +str(num)
else:
	print "Running over all events"





mod = ''
post = ''
if options.JES!='nominal':
	mod = mod + 'JES_' + options.JES
	post='jes'+options.JES
if options.JER!='nominal':
	mod = mod + 'JER_' + options.JER
	post='jer'+options.JER

#Based on what set we want to analyze, we find all Ntuple root files 
files = WPF.Load_Ntuples(options.set,di) 
jobiter = 0
# We select all the events: 
splitfiles = []

if jobs != 1 and options.split=="file":
    for ifile in range(1,len(files)+1):
    	if (ifile-1) % jobs == 0:
		jobiter+=1
	count_index = ifile  - (jobiter-1)*jobs
	if count_index==num:
		splitfiles.append(files[ifile-1])

    events = Events (splitfiles)
if options.split=="event" or jobs == 1:	  
	events = Events (files)



############################################################################################



#events = ChainEvent(files)
#Here we load up handles and labels.
#These are used to grab entries from the Ntuples.
#To see all the current types in an Ntuple use edmDumpEventContent /PathtoNtuple/Ntuple.root



ptmod = ""
if post.find("M")==-1:
	ptmod=post	


AK8HL = WPF.Initlv("jetsAK8",ptmod,options.coll)
AK4HL = WPF.Initlv("jetsAK4",ptmod,options.coll)
#---------------------------------------------------------------------------------------------------------------------#

#Create the output file
if jobs != 1:
	f = TFile( "THBTrigger"+options.set+tnamestr+"_pre_"+options.pretname+"_job"+options.num+"of"+options.jobs+".root", "recreate" )
else:
	f = TFile( "triggerstudies/THBTrigger"+options.set+tnamestr+"_pre_"+pretnamestr+".root", "recreate" )




print "Creating histograms"

#Define Histograms
f.cd()
#---------------------------------------------------------------------------------------------------------------------#
Htpreuntrig          = TH1D("Htpreuntrig",           "",             400,  0,  4000 )
Htuntrig          = TH1D("Htuntrig",           "",             400,  0,  4000 )

Htpreuntrig.Sumw2()
Htuntrig.Sumw2()


Htpre          = TH1D("Htpre",           "",             400,  0,  4000 )
Ht          = TH1D("Ht",           "",             400,  0,  4000 )

Htpre.Sumw2()
Ht.Sumw2()



Mthbhistpre          = TH1D("Mthbhistpre",           "",             400,  0,  4000 )
Mthbhist          = TH1D("Mthbhist",           "",             400,  0,  4000 )


Mthbhistpre.Sumw2()
Mthbhist.Sumw2()



MthballAk8histpre          = TH1D("MthballAk8histpre",           "",             400,  0,  4000 )
MthballAk8hist          = TH1D("MthballAk8hist",           "",             400,  0,  4000 )


MthballAk8histpre.Sumw2()
MthballAk8hist.Sumw2()




Mthbhistwkinpre          = TH1D("Mthbhistwkinpre",           "",             400,  0,  4000 )
Mthbhistwkin          = TH1D("Mthbhistwkin",           "",             400,  0,  4000 )


Mthbhistwkinpre.Sumw2()
Mthbhistwkin.Sumw2()



MthballAk8histwkinpre          = TH1D("MthballAk8histwkinpre",           "",             400,  0,  4000 )
MthballAk8histwkin          = TH1D("MthballAk8histwkin",           "",             400,  0,  4000 )


MthballAk8histwkinpre.Sumw2()
MthballAk8histwkin.Sumw2()








Mthbhistuntrig          = TH1D("Mthbhistuntrig",           "",             400,  0,  4000 )
Mthbhistuntrig.Sumw2()

MthballAk8histuntrig          = TH1D("MthballAk8histuntrig",           "",             400,  0,  4000 )
MthballAk8histuntrig.Sumw2()

Mthbhistwkinuntrig          = TH1D("Mthbhistwkinuntrig",           "",             400,  0,  4000 )
Mthbhistwkinuntrig.Sumw2()

MthballAk8histwkinuntrig          = TH1D("MthballAk8histwkinuntrig",           "",             400,  0,  4000 )
MthballAk8histwkinuntrig.Sumw2()









#---------------------------------------------------------------------------------------------------------------------#

# loop over events
#---------------------------------------------------------------------------------------------------------------------#

count = 0

print "Start looping"
#initialize the ttree variables
#totevents = events.size()
#print str(totevents)  +  ' Events total'
PFIRST = True
numpass = 0
trigdict = {}
prestrig = options.pretname 
nfail=0
for event in events:

    count	= 	count + 1
    

    if count % 100000 == 0 :
      print  '--------- Processing Event ' + str(count) #+'   -- percent complete ' + str(100*count/totevents) + '% -- '


   # if count>200000:
	#break

    if jobs != 1 and options.split=="event":
    	if (count - 1) % jobs == 0:
		jobiter+=1
	count_index = count - (jobiter-1)*jobs
	if count_index!=num:
		continue 


    AK8LV = WPF.Makelv(AK8HL,event)
    AK4LV = WPF.Makelv(AK4HL,event)
    kinak8 = False
    if len(AK8LV)>2:
	if AK8LV[0].Perp()>400 and AK8LV[1].Perp()>300 and AK8LV[2].Perp()>200:
    		kinak8 = True
    # We load up the relevant handles and labels and create collections
    nak4 = 0
    AK4ht=0.0

    event.getByLabel (WPF.LooseAK4Label, WPF.LooseAK4Handle)
    LooseAK4 	= 	WPF.LooseAK4Handle.product()
    AK43rdindex = None
    for iak4j in range(0,len(AK4LV)):
	isloose = LooseAK4[iak4j]>0.5
	if not isloose:
		continue 
	if len(AK8LV)>1 and AK43rdindex==None:
		if (AK4LV[iak4j].DeltaR(AK8LV[0])>1.2) and (AK4LV[iak4j].DeltaR(AK8LV[1])>1.2):
			AK43rdindex=iak4j
	
	AK4ht+=AK4LV[iak4j].Perp()

	kinak4 = False
	if len(AK8LV)>1 and AK43rdindex!=None:
		if AK8LV[0].Perp()>400 and AK8LV[1].Perp()>300 and AK4LV[AK43rdindex].Perp()>200:
	    		kinak4 = True


	nak4+=1
    if  nak4>=3:


	trigbools = []
	pretrigbools = []
	PASS = False
	prePASS = False

	for curTrig in tname:

		TrigH = WPF.Triggermap[curTrig][1]
		TrigL = WPF.Triggermap[curTrig][0]
		event.getByLabel(TrigL,TrigH )
		try:
			if TrigH.product()[-1]:
				PASS = True
		except:
			#print curTrig
			continue 

	for curTrig in pretname:
		TrigH = WPF.Triggermap[curTrig][1]
		TrigL = WPF.Triggermap[curTrig][0]
		event.getByLabel(TrigL,TrigH )
		try:
			if TrigH.product()[-1]:
					prePASS = True
		except:
			#print curTrig
			continue 

	Htpreuntrig.Fill(AK4ht)











	if len(AK8LV)>1 and AK43rdindex!=None:
		Mthbhistuntrig.Fill((AK4LV[AK43rdindex]+AK8LV[0]+AK8LV[1]).M())
	if len(AK8LV)>2:
		MthballAk8histuntrig.Fill((AK8LV[0]+AK8LV[1]+AK8LV[2]).M())
	if len(AK8LV)>1 and AK43rdindex!=None and kinak4:
		Mthbhistwkinuntrig.Fill((AK4LV[AK43rdindex]+AK8LV[0]+AK8LV[1]).M())
	if len(AK8LV)>2 and kinak8:
		MthballAk8histwkinuntrig.Fill((AK8LV[0]+AK8LV[1]+AK8LV[2]).M())





	if PASS:
		Htuntrig.Fill(AK4ht)


	if not prePASS:
		continue 

	Htpre.Fill(AK4ht)

	if len(AK8LV)>1 and AK43rdindex!=None:
		Mthbhistpre.Fill((AK4LV[AK43rdindex]+AK8LV[0]+AK8LV[1]).M())
	if len(AK8LV)>2:
		MthballAk8histpre.Fill((AK8LV[0]+AK8LV[1]+AK8LV[2]).M())

	if len(AK8LV)>1 and AK43rdindex!=None and kinak4:
		Mthbhistwkinpre.Fill((AK4LV[AK43rdindex]+AK8LV[0]+AK8LV[1]).M())
	if len(AK8LV)>2 and kinak8:
		MthballAk8histwkinpre.Fill((AK8LV[0]+AK8LV[1]+AK8LV[2]).M())





	#print 
	#print count

	#print [ event.object().id().run(), event.object().id().luminosityBlock(), event.object().id().event() ]
	#print "pre"
	#print totht
	if PASS:
	#	print "post"
	#	print totht
		Ht.Fill(AK4ht)
		if len(AK8LV)>1 and AK43rdindex!=None:
			Mthbhist.Fill((AK4LV[AK43rdindex]+AK8LV[0]+AK8LV[1]).M())
		if len(AK8LV)>2:
			MthballAk8hist.Fill((AK8LV[0]+AK8LV[1]+AK8LV[2]).M())
		if len(AK8LV)>1 and AK43rdindex!=None and kinak4:
			Mthbhistwkin.Fill((AK4LV[AK43rdindex]+AK8LV[0]+AK8LV[1]).M())
		if len(AK8LV)>2 and kinak8:
			MthballAk8histwkin.Fill((AK8LV[0]+AK8LV[1]+AK8LV[2]).M())





f.cd()
f.Write()
f.Close()


print "number of events: " + str(count)
