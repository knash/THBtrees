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
parser.add_option('-S', '--split', metavar='F', type='string', action='store',
                  default	=	'file',
                  dest		=	'split',
                  help		=	'split by event of file')

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

(options, args) = parser.parse_args()


gROOT.Macro("rootlogon.C")


import WprimetoVlq_Functions	
from WprimetoVlq_Functions import *
WPF = WprimetoVlq_Functions("default")



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


#Based on what set we want to analyze, we find all Ntuple root files 
files = WPF.Load_Ntuples(options.set,di)
jobiter = 0
splitfiles = []
# We select all the events:    
if jobs != 1 and options.split=="file":
    for ifile in range(1,len(files)+1):
    	if (ifile-1) % jobs == 0:
		jobiter+=1
	count_index = ifile  - (jobiter-1)*jobs
	if count_index==num:
		splitfiles.append(files[ifile-1])

    events = Events(splitfiles)
if options.split=="event" or jobs == 1:	  
	events = Events(files)
print "Event array created"
#Here we load up handles and labels.
#These are used to grab entries from the Ntuples.
#To see all the current types in an Ntuple use edmDumpEventContent /PathtoNtuple/Ntuple.root

AK8HL = WPF.Initlv("jetsAK8")


puHandle    	= 	Handle("int")
puLabel     	= 	(  "eventUserData", "puNtrueInt" )




npvHandle = Handle( "vector<int>" )
npvLabel = ( "eventUserData", "puNInt" )
#---------------------------------------------------------------------------------------------------------------------#

#Create the output file
if jobs != 1:
	f = TFile( "THBPileup"+options.set+"_job"+options.num+"of"+options.jobs+".root", "recreate" )
else:
	f = TFile( "THBPileup"+options.set+".root", "recreate" )




print "Creating histograms"

#Define Histograms
f.cd()
#---------------------------------------------------------------------------------------------------------------------#



npvtruehistUW	    = ROOT.TH1F("npvtruehistUW",     "mass W' in b+1",     	  	      80, 0, 80 )
npvtruehistUW.Sumw2()

npvhistUW	    = ROOT.TH1F("npvhistUW",     "mass W' in b+1",     	  	      80, 0, 80 )
npvhist	    = ROOT.TH1F("npvhist",     "mass W' in b+1",     	  	      80, 0, 80 )

npvhistUW.Sumw2()
npvhist.Sumw2()

#---------------------------------------------------------------------------------------------------------------------#

# loop over events
#---------------------------------------------------------------------------------------------------------------------#

count = 0

print "Start looping"
#initialize the ttree variables
totevents = events.size()
print str(totevents)  +  ' Events total'
#PFIRST = True
for event in events:
    count	= 	count + 1

    if count % 100000 == 0 :
      print  '--------- Processing Event ' + str(count) #+'   -- percent complete ' + str(100*count/totevents) + '% -- '

    #if count > 500000 :
	#break


    #Here we split up event processing based on number of jobs 
    #This is set up to have jobs range from 1 to the total number of jobs (ie dont start at job 0)
    if jobs != 1 and options.split=="event":
    	if (count - 1) % jobs == 0:
		jobiter+=1
	count_index = count - (jobiter-1)*jobs
	if count_index!=num:
		continue 
	




    event.getByLabel (npvLabel, npvHandle)
    npv = npvHandle.product()

    event.getByLabel (puLabel, puHandle)
    npvtrue = puHandle.product()

    npvhistUW.Fill(npv[0])  
    npvtruehistUW.Fill(float(npvtrue[0]))
    #npvhist.Fill(npv[0],weight)


f.cd()
f.Write()
f.Close()

print "number of events: " + str(count)
