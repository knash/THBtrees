

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
import CMS_lumi
parser = OptionParser()

parser.add_option('-c', '--cuts', metavar='F', type='string', action='store',
                  default	=	'default',
                  dest		=	'cuts',
                  help		=	'Cuts type (ie default, rate, etc)')
parser.add_option('-s', '--set', metavar='F', type='string', action='store',
                  default	=	'data',
                  dest		=	'set',
                  help		=	'data or QCD')
parser.add_option('--batch', metavar='F', action='store_true',
                  default=False,
                  dest='batch',
                  help='batch')

(options, args) = parser.parse_args()

if options.batch:
	ROOT.gROOT.SetBatch(True)
	ROOT.PyConfig.IgnoreCommandLineOptions = True




WPF = WprimetoVlq_Functions(options.cuts)




histos = ['t32nm1','tmassnm1','sjbtagnm1','hdbtagnm1','hmassnm1']#,'btagnm1']
titles = ['top #tau3/#tau2','top m_{SD} (GeV)','top  SJ_{csvmax}','Higgs Dbtag','Higgs m_{SD} (GeV)']
cutvals = [[0.8],[105,210],[0.5426],[0.8],[105,135]]
arrowvals = [["L"],["G","L"],["G"],["G"],["G","L"]]
arrdisps = [0.2,0.2,0.2,0.2,0.13]

arangel=[0.0,0.0,0.0,-1.0,0.0,0.0]
arangeh=[1.0,400.,1.0,1.0,250.,1.0]

rebins=[1,4,1,2,4,2]

QCDF = ROOT.TFile("rootfiles/THBanalyzerQCD_PSET_"+options.cuts+".root")
TTmc 	= ROOT.TFile("rootfiles/THBanalyzerweightedttbar__PSET_"+options.cuts+".root")

sigf = {}
sigf['1500'] = [
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp1500Tp1000__PSET_"+options.cuts+".root"),
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp1500Bp1000__PSET_"+options.cuts+".root")
]

sigf['2000'] = [
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp2000Tp1300__PSET_"+options.cuts+".root"),
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp2000Bp1300__PSET_"+options.cuts+".root")
]

sigf['2500'] = [
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp2500Tp1500__PSET_"+options.cuts+".root"),
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp2500Bp1500__PSET_"+options.cuts+".root")
]

canvs = []

cols = [3,4,6,7]
ihist=0

legx=[0.3,0.54,0.3,0.4,0.54,0.4]

for hist in histos:


	leg = TLegend(legx[ihist], 0.57, legx[ihist] + 0.30, 0.84)
	leg.SetFillColor(0)
	leg.SetBorderSize(0)
	canvs.append(TCanvas(hist))
	canvs[-1].cd()
	QCDFhist = QCDF.Get(hist)
	TTmchist = TTmc.Get(hist)
	firsthist = True
	isig = 0
	maxes = []
	sighs = []
	for sss in sigf:
		sigh = sigf[sss][0].Get(hist)		
		sigh1 = sigf[sss][0].Get(hist)
		sigh.Add(sigh1)	
		sigh.Rebin(rebins[ihist])
		sigh.Scale(1./sigh.Integral())
		sigh.SetLineColor(cols[isig])
		

		maxes.append(sigh.GetMaximum())
		leg.AddEntry( sigh, 'Signal (W`_{R} at ' + sss+' GeV)', 'l')


		sighs.append(sigh)

		isig+=1		

	QCDFhist.Rebin(rebins[ihist])
	TTmchist.Rebin(rebins[ihist])


	QCDFhist.Scale(1./QCDFhist.Integral())
	TTmchist.Scale(1./TTmchist.Integral())


	maxes.append(QCDFhist.GetMaximum())
	maxes.append(TTmchist.GetMaximum())
	for sigg in sighs:
		if firsthist:
			sigg.SetMaximum(max(maxes)*1.7)
			sigg.SetTitle(';'+titles[ihist]+';Fraction / bin')
			sigg.GetYaxis().SetTitleOffset(1.2)
			sigg.SetStats(0)

			sigg.GetXaxis().SetRangeUser(arangel[ihist],arangeh[ihist])

			sigg.Draw('hist')
		else:
			sigg.Draw('histsame')
		firsthist=False





	sigh.Scale(1./sigh.Integral())
	QCDFhist.SetLineColor(1)
	TTmchist.SetLineColor(2)

	leg.AddEntry( QCDFhist, 'QCD MC', 'l')
	leg.AddEntry( TTmchist, 't#bar{t} MC', 'l')


	QCDFhist.Draw('histsame')
	TTmchist.Draw('histsame')

	#cutvals = [[0.8],[105,210],[0.5426],[0.8],[105,135]]
	#arrowvals = ["L","B","G","G","B"]
	Lines = []
	Arrows = []
	arrdisp = arrdisps[ihist]
	totdisp = cutvals[ihist][0]


	nhh=0
	for cutval in cutvals[ihist]:

		Lines.append(TLine(cutval, 0.0, cutval, max(maxes)*1.2))
																											
		Lines[-1].SetLineColor(kRed)
		Lines[-1].SetLineWidth(2)
		Lines[-1].SetLineStyle(2)
		Lines[-1].Draw()


		curarrv = arrowvals[ihist][nhh]
		if curarrv=="L":
			Arrows.append(TArrow(cutval, max(maxes)*0.9, cutval - totdisp*arrdisp, max(maxes)*0.9,0.03,"|>"))
		if curarrv=="G":
			Arrows.append(TArrow(cutval, max(maxes)*0.9, cutval + totdisp*arrdisp, max(maxes)*0.9,0.03,"|>"))
		if curarrv=="L" or curarrv=="G":
			Arrows[-1].SetLineColor(kRed)
			Arrows[-1].SetFillColor(0)
			Arrows[-1].SetLineWidth(2)
			Arrows[-1].SetLineStyle(2)
			Arrows[-1].Draw()
		nhh+=1
	CMS_lumi.CMS_lumi(canvs[-1], 4, 11)
	leg.Draw()
	canvs[-1].Print('plots/NM1'+hist+'_Wprime_PSET_'+options.cuts+'.root', 'root')
	canvs[-1].Print('plots/NM1'+hist+'_Wprime_PSET_'+options.cuts+'.pdf', 'pdf')
	canvs[-1].Print('plots/NM1'+hist+'_Wprime_PSET_'+options.cuts+'.png', 'png')

	ihist+=1
	
