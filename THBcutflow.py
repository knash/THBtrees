

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

masses = [['1500','1000'],['2000','1300'],['2500','1500'],['3000','1800']]
histos = ['Mthb']
arangel=[1000.0]
arangeh=[6000.0]

rebins=[4]

TTmc 	= ROOT.TFile("rootfiles/THBanalyzerweightedttbar__PSET_"+options.cuts+".root")
DataB11 = ROOT.TFile("rootfiles/THBanalyzerdata__PSET_"+options.cuts+".root")
QCD = ROOT.TFile("rootfiles/THBanalyzerQCD__PSET_"+options.cuts+".root")

regions = [[''],['t1'],['h1'],['b1'],['t1','h1'],['t1','b1'],['h1','b1'],['h1','b1','t1']]

integraldict = {}
for iset in ['Data','ttbar','QCD','signal1500','signal2000','signal2500','signal3000']:
	integraldict[iset] = {}
	for region in regions:
		integraldict[iset][str(region).replace("[","").replace("]","").replace(",","")]=0.0
for ih in range(0,len(histos)):


	D = DataB11.GetListOfKeys()
	pdfasminus = {}
	pdfasplus = {}

	nomhist = None
	for region in regions:
		regionstr = str(region).replace("[","").replace("]","").replace(",","")

		for i in range(0,len(D)):
					a = D[i].ReadObj()
					currentname = a.GetName()
					if currentname[0:4]!="Mthb" or len(currentname)!=11:
						continue 

					try:

						datahisto = DataB11.Get(a.GetName())

						#print "bkg_"+a.GetName()
						if currentname[-6:].find('h1')!=-1:
							QCDhisto = copy.copy(DataB11.Get("bkg_"+a.GetName()))
							ttbarbkghisto = TTmc.Get("bkg_"+a.GetName())
							QCDhisto.Add(ttbarbkghisto,-1)
						ttbarhisto = TTmc.Get(a.GetName())
						signal1500histo = copy.copy(sigf[0][0].Get(a.GetName()))
						signal1500histotosum = sigf[0][1].Get(a.GetName())
						signal1500histo.Add(signal1500histotosum)
					except:
						continue
					signal2000histo = copy.copy(sigf[1][0].Get(a.GetName()))
					signal2000histotosum = sigf[1][1].Get(a.GetName())
					signal2000histo.Add(signal2000histotosum)

					signal2500histo = copy.copy(sigf[2][0].Get(a.GetName()))
					signal2500histotosum =  sigf[2][1].Get(a.GetName())
					signal2500histo.Add(signal2500histotosum)

					signal3000histo = copy.copy(sigf[3][0].Get(a.GetName()))
					signal3000histotosum = sigf[3][1].Get(a.GetName())
					signal3000histo.Add(signal3000histotosum)
					#histo0 = sigfiles[isig][0].Get(a.GetName())
					#histo1 = sigfiles[isig][1].Get(a.GetName())

					#print "skipping ",a.GetName()
					#print currentname
					#print len(currentname)
			


					notfoundstr=True
					for ss in region:
						#print currentname[-6:] 
						#print ss
						if currentname[-6:].find(ss)==-1:
							#print "NF"
							notfoundstr=False
					if notfoundstr:
						#if currentname[-6:]=='h1t1b1' :
						#	print currentname[-6:]
						#	print regionstr
						#	print integraldict['signal2000'][regionstr],signal2000histo.Integral()
						integraldict['Data'][regionstr]+=datahisto.Integral()	
						print regionstr
						print integraldict['Data'][regionstr]
						integraldict['ttbar'][regionstr]+=ttbarhisto.Integral()
						if currentname[-6:].find('h1')!=-1:
							integraldict['QCD'][regionstr]+=QCDhisto.Integral()
									
						integraldict['signal1500'][regionstr]+=signal1500histo.Integral()

						integraldict['signal2000'][regionstr]+=signal2000histo.Integral()

						integraldict['signal2500'][regionstr]+=signal2500histo.Integral()
						integraldict['signal3000'][regionstr]+=signal3000histo.Integral()



					#if str(type(a)) != "<class 'ROOT.TH1F'>":
					#	continue 

order = ["''","'b1'","'h1'","'t1'","'t1' 'b1'","'h1' 'b1'","'t1' 'h1'","'h1' 'b1' 't1'"]

print integraldict

print "Region & Data & QCD & ttbar & signal 1500 & signal 2000& signal 2500 &  signal 3000"
for iord in order:
	QCDcontstring = "---" 
	Datacontstring = "---" 
	if  iord=="'t1' 'h1'" or  iord=="'h1' 'b1' 't1'":
		QCDcontstring = WPF.strf1(integraldict['QCD'][iord])
	if  iord!="'h1' 'b1' 't1'":
		Datacontstring = WPF.strf1(integraldict['Data'][iord])
	print iord , "&" , Datacontstring, "&" , QCDcontstring, "&" , WPF.strf1(integraldict['ttbar'][iord]), "&" , WPF.strf1(integraldict['signal1500'][iord]), "&" , WPF.strf1(integraldict['signal2000'][iord]), "&" , WPF.strf1(integraldict['signal2500'][iord]), "&" , WPF.strf1(integraldict['signal3000'][iord])
print 


