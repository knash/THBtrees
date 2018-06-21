

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

parser.add_option('-s', '--set', metavar='F', type='string', action='store',
                  default	=	'ttbarfulltuple',
                  dest		=	'set',
                  help		=	'data or QCD')

(options, args) = parser.parse_args()

leg = TLegend(0.5, 0.5, 0.84, 0.84)
leg.SetFillColor(0)
leg.SetBorderSize(0)

ROOT.gROOT.Macro("rootlogon.C")

fdata = ROOT.TFile("Pileup_2016_69200mb.root")
fdataup = ROOT.TFile("Pileup_2016_72383mb.root")
fdatadown = ROOT.TFile("Pileup_2016_66017mb.root")






fttbar  = ROOT.TFile("THBPileup"+options.set+".root")


output = ROOT.TFile( "PileUp_Ratio_"+options.set+".root", "recreate" )

output.cd()

# Get numerators and denominators for each eta region

ndata = fdata.Get("pileup")
ndataup = fdataup.Get("pileup")
ndatadown = fdatadown.Get("pileup")

ndata.Sumw2()
ndataup.Sumw2()
ndatadown.Sumw2()


ndata.Scale(1./ndata.Integral())
ndataup.Scale(1./ndataup.Integral())
ndatadown.Scale(1./ndatadown.Integral())

dttbar = fttbar.Get("npvtruehistUW")
dttbar.Scale(1./dttbar.Integral())

ttbar_pileup_reweight = ndata.Clone("Pileup_Ratio")
ttbar_pileup_reweight.Divide(dttbar)
ttbar_pileup_reweight.Write()

ttbar_pileup_reweight_up = ndataup.Clone("Pileup_Ratio_up")
ttbar_pileup_reweight_up.Divide(dttbar)
ttbar_pileup_reweight_up.Write()

ttbar_pileup_reweight_down = ndatadown.Clone("Pileup_Ratio_down")
ttbar_pileup_reweight_down.Divide(dttbar)
ttbar_pileup_reweight_down.Write()











'''

files = [
ROOT.TFile("TBPileupsignalright2000fulltuple.root")

]

names = [
"PileUp_Ratio_signal.root"
]

















files = [

ROOT.TFile("TBPileupsignalright1200.root"),
ROOT.TFile("TBPileupsignalright1300.root"),
ROOT.TFile("TBPileupsignalright1400.root"),
ROOT.TFile("TBPileupsignalright1500.root"),
ROOT.TFile("TBPileupsignalright1600.root"),
ROOT.TFile("TBPileupsignalright1700.root"),
ROOT.TFile("TBPileupsignalright1800.root"),
ROOT.TFile("TBPileupsignalright1900.root"),
ROOT.TFile("TBPileupsignalright2000.root"),
ROOT.TFile("TBPileupsignalright2100.root"),
ROOT.TFile("TBPileupsignalright2200.root"),
ROOT.TFile("TBPileupsignalright2300.root"),
ROOT.TFile("TBPileupsignalright2400.root"),
ROOT.TFile("TBPileupsignalright2500.root"),
ROOT.TFile("TBPileupsignalright2600.root"),
ROOT.TFile("TBPileupsignalright2700.root"),
ROOT.TFile("TBPileupsignalright2800.root"),
ROOT.TFile("TBPileupsignalright2900.root")
]

names = [
"PileUp_Ratio_signal1200.root",
"PileUp_Ratio_signal1300.root",
"PileUp_Ratio_signal1400.root",
"PileUp_Ratio_signal1500.root",
"PileUp_Ratio_signal1600.root",
"PileUp_Ratio_signal1700.root",
"PileUp_Ratio_signal1800.root",
"PileUp_Ratio_signal1900.root",
"PileUp_Ratio_signal2000.root",
"PileUp_Ratio_signal2100.root",
"PileUp_Ratio_signal2200.root",
"PileUp_Ratio_signal2300.root",
"PileUp_Ratio_signal2400.root",
"PileUp_Ratio_signal2500.root",
"PileUp_Ratio_signal2600.root",
"PileUp_Ratio_signal2700.root",
"PileUp_Ratio_signal2800.root",
"PileUp_Ratio_signal2900.root"
]

dhists = []
dhistsalt = []
for ifile in range(0,len(files)):
	outputsig = ROOT.TFile(names[ifile] , "recreate" )
	outputsig.cd()



	dhists.append(files[ifile].Get("npvtruehistUW"))
	dhists[ifile].Scale(1./dhists[ifile].Integral())

	Pileup_Ratio = ndata.Clone("Pileup_Ratio")
	Pileup_Ratio_up = ndataup.Clone("Pileup_Ratio_up")
	Pileup_Ratio_down = ndatadown.Clone("Pileup_Ratio_down")

	Pileup_Ratio.Divide(dhists[ifile])
	Pileup_Ratio_up.Divide(dhists[ifile])
	Pileup_Ratio_down.Divide(dhists[ifile])

	Pileup_Ratio.Write()
	Pileup_Ratio_up.Write()
	Pileup_Ratio_down.Write()

	#outputsig.Write()
	outputsig.Close()
'''
