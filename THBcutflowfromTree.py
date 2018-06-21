

import os
import array
import glob
import math
import ROOT
import sys
import copy

from array import *
from optparse import OptionParser
import WprimetoVlq_Functions
from WprimetoVlq_Functions import *
gROOT.Macro("rootlogon.C")
gROOT.LoadMacro("insertlogo.C+")
parser = OptionParser()

parser.add_option('-c', '--cuts', metavar='F', type='string', action='store',
                  default	=	'default',
                  dest		=	'cuts',
                  help		=	'Cuts type (ie default, rate, etc)')

parser.add_option('--batch', metavar='F', action='store_true',
                  default=False,
                  dest='batch',
                  help='batch')

(options, args) = parser.parse_args()

cuts = options.cuts

if options.batch:
	ROOT.gROOT.SetBatch(True)
	ROOT.PyConfig.IgnoreCommandLineOptions = True




WPF = WprimetoVlq_Functions(options.cuts)



leg = TLegend(0.45, 0.35, 0.84, 0.84)
leg.SetFillColor(0)
leg.SetBorderSize(0)

sigf = [[
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp1500Tp1000__PSET_"+options.cuts+".root"),
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp1500Bp1000__PSET_"+options.cuts+".root")
],[
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp2000Tp1300__PSET_"+options.cuts+".root"),
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp2000Bp1300__PSET_"+options.cuts+".root")
],[
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp2500Tp1500__PSET_"+options.cuts+".root"),
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp2500Bp1500__PSET_"+options.cuts+".root")
],[
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp3000Tp1800__PSET_"+options.cuts+".root"),
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp3000Bp1800__PSET_"+options.cuts+".root")
]]


sigratef = [[
ROOT.TFile("rootfiles/THBrateweightedTHBWp1500Tp1000_PSET_"+options.cuts+".root"),
ROOT.TFile("rootfiles/THBrateweightedTHBWp1500Bp1000_PSET_"+options.cuts+".root")
],[
ROOT.TFile("rootfiles/THBrateweightedTHBWp2000Tp1300_PSET_"+options.cuts+".root"),
ROOT.TFile("rootfiles/THBrateweightedTHBWp2000Bp1300_PSET_"+options.cuts+".root")
],[
ROOT.TFile("rootfiles/THBrateweightedTHBWp2500Tp1500_PSET_"+options.cuts+".root"),
ROOT.TFile("rootfiles/THBrateweightedTHBWp2500Bp1500_PSET_"+options.cuts+".root")
],[
ROOT.TFile("rootfiles/THBrateweightedTHBWp3000Tp1800_PSET_"+options.cuts+".root"),
ROOT.TFile("rootfiles/THBrateweightedTHBWp3000Bp1800_PSET_"+options.cuts+".root")
]]




masses = [['1500','1000'],['2000','1300'],['2500','1500'],['3000','1800']]
histos = ['Mthb']
arangel=[1000.0]
arangeh=[6000.0]

rebins=[4]

TTmc 	= ROOT.TFile("rootfiles/THBanalyzerweightedttbar__PSET_"+options.cuts+".root")
DataB11 = ROOT.TFile("rootfiles/THBanalyzerdata__PSET_"+options.cuts+".root")

TTratemc 	= ROOT.TFile("rootfiles/THBrateweightedttbar_PSET_"+options.cuts+".root")
DatarateB11 = ROOT.TFile("rootfiles/THBratedata_PSET_"+options.cuts+".root")


regions = ['SR','SB1','SB2','SB3','SB4','SB5','SB6','SB7']
histonames = ['h1t1b1','h0t0b1','h1t0b1','h0t1b1','h1t1b0','h0t0b0','h1t0b0','h0t1b0']
integraldict = {}
histodict = {}

for iregion in xrange(len(regions)):
	histodict[regions[iregion]]=histonames[iregion]

for iset in ['Data','ttbar','QCD','signal1500','signal2000','signal2500','signal3000']:
	integraldict[iset] = {}
	for region in regions:
		integraldict[iset][str(region)]=0.0
print integraldict
print histodict
for ih in range(0,len(histos)):
	for region in regions:
		print region
		print histodict[region]
		curhist = histos[ih]+"_"+histodict[region]
		userate=False
		print curhist
		if histodict[region].find("t0")!=-1:
			print "USE RATE REGION"
			userate=True
		
		TTmchist = TTmc.Get(curhist) 
		Datahist = DataB11.Get(curhist) 
		if userate:
	
			TTmchist = TTratemc.Get(curhist) 
			Datahist = DatarateB11.Get(curhist) 
			

		integraldict['Data'][region]=Datahist.Integral()
		integraldict['ttbar'][region]=TTmchist.Integral()

		if histodict[region]=='h1t1b0' or  histodict[region]=='h1t1b1':
			QCDhist = DataB11.Get("bkg_"+curhist+"ebin")
			TTmcQCDhist = TTmc.Get("bkg_"+curhist+"ebin") 
			print QCDhist.Integral()
			print TTmcQCDhist.Integral()
			integraldict['QCD'][region]=QCDhist.Integral()
			integraldict['QCD'][region]-=TTmcQCDhist.Integral()
			print region,integraldict

		sig1500 = sigf[0][0].Get(curhist) 
		sig1500.Add(sigf[0][1].Get(curhist))



		sig2000 = sigf[1][0].Get(curhist) 
		sig2000.Add(sigf[1][1].Get(curhist))



		sig2500 = sigf[2][0].Get(curhist) 
		sig2500.Add(sigf[2][1].Get(curhist))



		sig3000 = sigf[3][0].Get(curhist) 
		sig3000.Add(sigf[3][1].Get(curhist))


		if userate:



			sig1500 = sigratef[0][0].Get(curhist) 
			sig1500.Add(sigratef[0][1].Get(curhist))



			sig2000 = sigratef[1][0].Get(curhist) 
			sig2000.Add(sigratef[1][1].Get(curhist))



			sig2500 = sigratef[2][0].Get(curhist) 
			sig2500.Add(sigratef[2][1].Get(curhist))



			sig3000 = sigratef[3][0].Get(curhist) 
			sig3000.Add(sigratef[3][1].Get(curhist))





		integraldict['signal1500'][region]=sig1500.Integral()
		integraldict['signal2000'][region]=sig2000.Integral()
		integraldict['signal2500'][region]=sig2500.Integral()
		integraldict['signal3000'][region]=sig3000.Integral()


print integraldict

print "Region & Data & QCD & ttbar & signal 1500 & signal 2000& signal 2500 &  signal 3000"
for ireg in xrange(len(regions)):
	QCDcontstring = "---" 
	Datacontstring = "---" 
	if  histodict[regions[ireg]]=='h1t1b0' or  histodict[regions[ireg]]=='h1t1b1':
		QCDcontstring = WPF.strf1(integraldict['QCD'][regions[ireg]])
	if  histodict[regions[ireg]]!='h1t1b1':
		Datacontstring = WPF.strf1(integraldict['Data'][regions[ireg]])
	print regions[ireg] , "&" , Datacontstring, "&" , QCDcontstring, "&" , WPF.strf1(integraldict['ttbar'][regions[ireg]]), "&" , WPF.strf1(integraldict['signal1500'][regions[ireg]]), "&" , WPF.strf1(integraldict['signal2000'][regions[ireg]]), "&" , WPF.strf1(integraldict['signal2500'][regions[ireg]]), "&" , WPF.strf1(integraldict['signal3000'][regions[ireg]])
print 
print 
print "Region & Data & QCD & ttbar & signal 1500 & signal 2000& signal 2500 &  signal 3000"
for ireg in xrange(len(regions)):
	QCDcontstring = "---" 
	Datacontstring = "---" 
	if  histodict[regions[ireg]]=='h1t1b0' or  histodict[regions[ireg]]=='h1t1b1':
		QCDcontstring = WPF.strfSF(integraldict['QCD'][regions[ireg]],2)
	#if  histodict[regions[ireg]]!='h1t1b1':
	Datacontstring = WPF.strfSF(integraldict['Data'][regions[ireg]],2)
	print regions[ireg] , "&" , Datacontstring, "&" , QCDcontstring, "&" , WPF.strfSF(integraldict['ttbar'][regions[ireg]],2), "&" , WPF.strfSF(integraldict['signal1500'][regions[ireg]],2), "&" , WPF.strfSF(integraldict['signal2000'][regions[ireg]],2), "&" , WPF.strfSF(integraldict['signal2500'][regions[ireg]],2), "&" , WPF.strfSF(integraldict['signal3000'][regions[ireg]],2)
print 
