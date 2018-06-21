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


files = WPF.Load_Ntuples(options.set,di) 


events = Events(files)
runs = Runs(files)
PDFup = 0.0
PDFdown = 0.0
PDFnom = 0.0

Q2up = 0.0
Q2down = 0.0
Q2nom = 0.0

count = 0
for event in events:
  	count+=1
    	if count % 10000 == 0 :
      		print  '--------- Processing Event ' + str(count) #+'   -- percent complete ' + str(100*count/totevents) + '% -- '
	if count>90000:
		break
	event.getByLabel (WPF.pdfLabelNOM, WPF.pdfHandleNOM)
	pdfweightNOM 	= 	WPF.pdfHandleNOM.product()


	PDFup += WPF.PDF_Lookup(pdfweightNOM , "up" )
	PDFdown += WPF.PDF_Lookup(pdfweightNOM , "down" )
	PDFnom += 1.0
	
	event.getByLabel (WPF.Q2Label, WPF.Q2Handle)
	Q2weight 	= 	WPF.Q2Handle.product()

	Q2up+=max(Q2weight)
	Q2down+=min(Q2weight)
	Q2nom+=1			



strwpmassp = options.set

print PDFup/PDFnom
print PDFdown/PDFnom

print Q2up/Q2nom
print Q2down/Q2nom

Outf   =   open("pdfw.csv", "r")
Outfr = Outf.read()
Outspl = Outfr.split('\n')
Outfwrite   =   open("pdfw.csv", "w")
foundpdf = False
now = datetime.datetime.now()
timestr = str(now.month)+'_'+str(now.day)

pdfup = PDFup/PDFnom
pdfdown = PDFdown/PDFnom
q2up = Q2up/Q2nom
q2down = Q2down/Q2nom
uquad = str(1.0+sqrt((pdfup-1.)*(pdfup-1.) + (q2up-1.)*(q2up-1.)))
dquad = str(1.0-sqrt((pdfdown-1.)*(pdfdown-1.) + (q2down-1.)*(q2down-1.)))
print "up quad ",uquad
print "down quad ",dquad
for outl in Outspl:
	tempoutspl = outl.split(',')
	if len(tempoutspl)<3:
		continue 
	if tempoutspl[0] == strwpmassp:
		print "this one"
		foundpdf = True
		tempoutspl[1] = str(uquad)
		tempoutspl[2] = str(dquad)
	Outspl = str(tempoutspl[0])+','+str(tempoutspl[1])+','+str(tempoutspl[2])+','+timestr+'\n'
	Outfwrite.write(str(Outspl))
if not foundpdf:
	Outfwrite.write(str(str(strwpmassp)+','+str(uquad)+','+str(dquad)+','+timestr+'\n'))


Outfwrite.close()

		
#f.cd()
#f.Write()
#f.Close()



