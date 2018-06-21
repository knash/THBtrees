import os
import array
import glob
import math
import ROOT
import copy
import sys
#from ROOT import *
from array import *
from optparse import OptionParser
import WprimetoVlq_Functions
from WprimetoVlq_Functions import *

parser = OptionParser()

parser.add_option('-c', '--cuts', metavar='F', type='string', action='store',
                  default	=	'default',
                  dest		=	'cuts',
                  help		=	'Cuts type (ie default, rate, etc)')

parser.add_option('-t', '--cot', metavar='F', type='string', action='store',
                  default	=	'default',
                  dest		=	'cot',
                  help		=	'cottheta2')

parser.add_option('-S', '--sigscale', metavar='F', type='string', action='store',
                  default	=	'1.0',
                  dest		=	'sigscale',
                  help		=	'sigscale')

(options, args) = parser.parse_args()


def Zero(hist):
	for ibin in range(0,hist.GetXaxis().GetNbins()+1):
		hist.SetBinContent(ibin,max(0.0,hist.GetBinContent(ibin)))
	

def writeslices(curhist,output,reconame):
	output.cd()
	print "writing",a.GetName()
	print "Total Integral",curhist[0].Integral()
	print "number of bins ",curhist[0].GetNbinsX()
	intsum = 0.0
	for binbin in range(0,curhist[0].GetNbinsX()+1):
		print binbin
		curhist.append(curhist[0].ProjectionY("bin"+str(binbin),binbin,binbin))

		curhist[-1].SetName("bin"+str(binbin)+reconame)
		curhist[-1].SetTitle("bin"+str(binbin)+reconame)
		curhist[-1].Write("bin"+str(binbin)+reconame)

		print "Using name","bin"+str(binbin)+reconame
		print curhist[-1].Integral()
		print "bin",binbin,curhist[-1].Integral()
		intsum+=curhist[-1].Integral()
	print "totsum",intsum



cuts = options.cuts
gROOT.Macro("rootlogon.C")

WPF = WprimetoVlq_Functions(options.cuts)

LabelsU=[]
mass = []
rebin =2
#chans = ['h1t1b1','h1t0b1','h1t1b0']
chans = ['h1t1b1']
#chans = ['h1t1b1']
chanstr = ''
for ch in chans:
	chanstr+='_'+ch
print chanstr
sigpoints = [['1500','1000'],['2000','1300'],['2500','1500'],['3000','1800']]
#sigpoints = [['1500',''],['2000','1300'],['2500','1500'],['3000','1800']]

sigscstr = ""
foldstr = ""
setstr ="weighted" 
sigscale=1.0
if options.sigscale=="cslim":
	print "using 1pb scale"
	sigscstr="sigscale_1pb"	 
	foldstr = "limitscale/"
	setstr ="limitscale" 
elif options.sigscale!="1.0":
	print "using "+options.sigscale+" scale"
	sigscstr="sigscale_"+options.sigscale.replace(".","p")
	sigscale = float(options.sigscale)

for coup in ['right']:

	output = ROOT.TFile( "limitsetting/theta/TEST2Dbins"+chanstr+options.cuts+sigscstr+".root", "recreate" )
	output.cd()

	Data = ROOT.TFile("rootfiles/THBanalyzerdata__PSET_"+options.cuts+".root")
	TTmc 	= ROOT.TFile("rootfiles/THBanalyzerweightedttbar__PSET_"+options.cuts+".root")
	sigfiles = []


	for sigpoint in sigpoints:


		sigfiles.append([])
		#sigfiles[-1].append(ROOT.TFile("rootfiles/limitscale/THBanalyzerlimitscaleTHBWp"+sigpoint[0]+"Bp"+sigpoint[1]+"__PSET_"+options.cuts+".root"))
		#sigfiles[-1].append(ROOT.TFile("rootfiles/limitscale/THBanalyzerlimitscaleTHBWp"+sigpoint[0]+"Tp"+sigpoint[1]+"__PSET_"+options.cuts+".root"))
		sigfiles[-1].append(ROOT.TFile("rootfiles/"+foldstr+"THBanalyzer"+setstr+"THBWp"+sigpoint[0]+"Bp"+sigpoint[1]+"__PSET_"+options.cuts+".root"))
		sigfiles[-1].append(ROOT.TFile("rootfiles/"+foldstr+"THBanalyzer"+setstr+"THBWp"+sigpoint[0]+"Tp"+sigpoint[1]+"__PSET_"+options.cuts+".root"))




   	for ch in chans:




		#DataFS 	= DataB11.Get("Mthb_"+ch) 			
		DataQCD = Data.Get("bkg_Mthb_Mth_"+ch)
		print DataQCD
		DataQCDUp = Data.Get("bkg_Mthb_Mth_"+ch+"up")
		DataQCDDown = Data.Get("bkg_Mthb_Mth_"+ch+"down")
		TTmcQCD = TTmc.Get("bkg_Mthb_Mth_"+ch)

		DataQCD.Add(TTmcQCD,-1)
		DataQCDUp.Add(TTmcQCD,-1)
		DataQCDDown.Add(TTmcQCD,-1)

		DataQCD.RebinX(rebin)
		DataQCDUp.RebinX(rebin)
		DataQCDDown.RebinX(rebin)



		alltthistos = []

		D1 = TTmc.GetListOfKeys()
		for i in range(0,len(D1)):
				a = D1[i].ReadObj()
				try:
					currentname = a.GetName()
					TThisto = TTmc.Get(a.GetName())
					if currentname[0:8]!="Mthb_Mth":
						continue 
					if currentname[-6:]!=ch:
						continue
					if str(type(a)) != "<class 'ROOT.TH2F'>":
						continue 
					#print currentname
					#print "Mthb=",currentname[0:4]
					#print "channel=",currentname[-6:]
					syststring = currentname[8:-7]
					#print  type(a) 
					#print syststring,"downfind ",syststring.find('down')
					if syststring.find('Tpt')!=-1:
						continue
					if syststring.find('down')!=-1:
					#	print "isdown"

						reconame="Mthb_Mth"+ch+"__ttbar__"+syststring.replace('down','')+"__minus"
					elif syststring.find('up')!=-1:
						reconame="Mthb_Mth"+ch+"__ttbar__"+syststring.replace('up','')+"__plus"
					else:
						reconame="Mthb_Mth"+ch+"__ttbar"

					print "writing",a.GetName()
					print "Using name",reconame
					TThisto.RebinX(rebin)
					alltthistos.append(copy.copy(TThisto))
					output.cd()
					writeslices([alltthistos[-1]],output,reconame)
					
					print "Keep it!"
				except:
					print "skipping ",a.GetName()


		output.cd()

		writeslices([DataQCD],output,"Mthb_Mth"+ch+"__qcd")
		writeslices([DataQCDUp],output,"Mthb_Mth"+ch+"__qcd__Fit__plus")
		writeslices([DataQCDDown],output,"Mthb_Mth"+ch+"__qcd__Fit__minus")
		
		isig = 0
		allsighists = []

		for sigpoint in sigpoints:

			D = sigfiles[isig][0].GetListOfKeys()
			for i in range(0,len(D)):
				a = D[i].ReadObj()
				if True:#try:
					currentname = a.GetName()
					histo0 = sigfiles[isig][0].Get(a.GetName())
					histo1 = sigfiles[isig][1].Get(a.GetName())
					#print currentname
					#print currentname[0:8]
					if currentname[0:8]!="Mthb_Mth":
						continue 
					if currentname[-6:]!=ch:
						continue
					if str(type(a)) != "<class 'ROOT.TH2F'>":
						continue 
					#print currentname
					#print "Mthb=",currentname[0:4]
					#print "channel=",currentname[-6:]
					syststring = currentname[8:-7]
					#print  type(a) 
					#print syststring,"downfind ",syststring.find('down')
					
					if syststring.find('down')!=-1:
					#	print "isdown"
						reconame="Mthb_Mth"+ch+"__wp"+sigpoint[0]+"__"+syststring.replace('down','')+"__minus"
					elif syststring.find('up')!=-1:
						reconame="Mthb_Mth"+ch+"__wp"+sigpoint[0]+"__"+syststring.replace('up','')+"__plus"
					else:
						reconame="Mthb_Mth"+ch+"__wp"+sigpoint[0]


					histo0 = sigfiles[isig][0].Get(a.GetName())
					histo1 = sigfiles[isig][1].Get(a.GetName())
					#print "adding ",histo0,histo0.Integral()
					#print "and ",histo1,histo1.Integral()
					histo0.RebinX(rebin)
					histo1.RebinX(rebin)
					allsighists.append([])
					allsighists[-1].append(copy.copy(histo0))
					allsighists[-1][0].Add(histo1)
					
					writeslices(allsighists[-1],output,reconame)
					
				#except:
				#	print "skipping ",a.GetName()

			isig += 1



