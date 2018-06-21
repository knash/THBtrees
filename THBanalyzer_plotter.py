

import os
import array
import glob
import math
import ROOT
import sys
import copy
from ROOT import *
from array import *
from optparse import OptionParser
gROOT.Macro("rootlogon.C")
gROOT.LoadMacro("insertlogo.C+")
parser = OptionParser()

parser.add_option('-c', '--cuts', metavar='F', type='string', action='store',
                  default	=	'default',
                  dest		=	'cuts',
                  help		=	'Cuts type (ie default, rate, etc)')
parser.add_option('-s', '--set', metavar='F', type='string', action='store',
                  default	=	'data',
                  dest		=	'set',
                  help		=	'data or QCD')

parser.add_option('-z', '--histo', metavar='F', type='string', action='store',
                  default	=	'h1t1b1',
                  dest		=	'histo',
                  help		=	'')

parser.add_option('--batch', metavar='F', action='store_true',
                  default=False,
                  dest='batch',
                  help='batch')

(options, args) = parser.parse_args()
extex = ""
if options.histo=='h1t1b0':
	extex = "Bfail"

cuts = options.cuts

if options.batch:
	ROOT.gROOT.SetBatch(True)
	ROOT.PyConfig.IgnoreCommandLineOptions = True


import WprimetoVlq_Functions
from WprimetoVlq_Functions import *

WPF = WprimetoVlq_Functions(options.cuts)

st1= ROOT.THStack("st1", "st1")

leg = TLegend(0.45, 0.35, 0.84, 0.84)
leg.SetFillColor(0)
leg.SetBorderSize(0)

rebin =5
plotdata = True
if options.set == 'data' and extex == "":
	plotdata=False

#Kfac=1.2
arange=6000.0
amin=0.2

sigf = [
ROOT.TFile("rootfiles/THBanalyzerweightedTHB_PSET_"+options.cuts+".root")
]

sigh = [
sigf[0].Get("Mthb_"+options.histo)
]

sigh[0].Rebin(rebin)
sigh[0].SetLineStyle(5)
sigh[0].SetLineWidth(3)
sigh[0].SetLineColor(3)

TTmc 	= ROOT.TFile("rootfiles/THBanalyzerttbar_PSET_"+options.cuts+"weighted.root")
if options.set == 'data':
	setstring = '' 
	print "running on data"
	DataB11 = ROOT.TFile("rootfiles/THBanalyzerdata_PSET_"+options.cuts+".root")
	DataFS 	= DataB11.Get("Mthb_"+options.histo) 			
	DataBE 	= DataB11.Get("bkg_Mthb_"+options.histo) 		
	datapointcolor = 1	
elif options.set == 'QCD':
	setstring = 'QCD' 
	DataB11 = ROOT.TFile("rootfiles/THBanalyzerQCD_PSET_"+options.cuts+".root")
	DataFS 	= DataB11.Get("Mthb_"+options.histo) 			
	DataBE 	= DataB11.Get("bkg_Mthb_"+options.histo) 		
	DataFS.Add(TTmc.Get("Mthb_"+options.histo)) 
	datapointcolor = 4
else:
	print 'Error: Set selection invalid.'

c1 = TCanvas('c1', '', 700, 600)
main = ROOT.TPad("main", "main", 0, 0.3, 1, 1)
sub = ROOT.TPad("sub", "sub", 0, 0, 1, 0.3)

main.SetLeftMargin(0.16)
main.SetRightMargin(0.05)
main.SetTopMargin(0.11)
main.SetBottomMargin(0.0)

sub.SetLeftMargin(0.16)
sub.SetRightMargin(0.05)
sub.SetTopMargin(0)
sub.SetBottomMargin(0.3)

main.Draw()
sub.Draw()

main.cd()


output = ROOT.TFile( "THBanalyzer_output_PSET_"+options.cuts+".root", "recreate" )
output.cd()

TTmcFS = TTmc.Get("Mthb_"+options.histo)
TTmcBE = TTmc.Get("bkg_Mthb_"+options.histo)

TTmcFS.Rebin(rebin)
TTmcBE.Rebin(rebin)
DataBE.Rebin(rebin)
DataFS.Rebin(rebin)

unsubbkg = DataBE.Clone()

# Uncomment when using data -JL #
if options.set=='data':
	DataBE.Add(TTmcBE,-1)

output.cd()


DataBE.SetFillColor(kYellow)
TTmcFS.SetFillColor(kRed)

st1.Add(TTmcFS)
st1.Add(DataBE)

DataFS.SetLineColor(datapointcolor)
DataFS.SetMarkerColor(datapointcolor)

if options.set == 'QCD':
	leg.AddEntry( DataFS, 'QCD FS + t#bar{t}', 'P')
	leg.AddEntry( DataBE, 'QCD Background', 'F')
elif options.set == 'data':
	if plotdata:
		leg.AddEntry( DataFS, 'data', 'P')
	leg.AddEntry( DataBE, 'QCD', 'F')
leg.AddEntry( TTmcFS, 't#bar{t}', 'F')



leg.AddEntry( sigh[0], 'W`_{R} at 2000 GeV -> Tp at 1200 GeV', 'L')


#c1.cd()
#c1.SetLeftMargin(0.17)

st1.SetMaximum(DataFS.GetMaximum() * 1.3)
st1.SetMinimum(1.0)
st1.SetTitle(';M_{thb} (GeV);Counts per 100 GeV')
st1.Draw("hist")
gPad.SetLeftMargin(.16)
st1.GetYaxis().SetTitleOffset(0.9)
#DataTOTALBEH.Draw("histsame")
#DataTOTALBEL.Draw("histsame")
sigh[0].Draw("samehist")

DataFS1	    = TH1D("DataFS1",     "mass W' in b+1",     	  	      140, 500, 4000 )
DataFS1.Rebin(rebin)
for ibin in range(1,DataFS.GetNbinsX()+1):
	DataFS1.SetBinContent(ibin,DataFS.GetBinContent(ibin))

DataFS1.SetBinErrorOption(DataFS1.kPoisson)
DataFS1 = DataFS
if plotdata:
	DataFS1.Draw("samepE")

leg.Draw()
prelim = TLatex()
prelim.SetNDC()


#insertlogo( main, 2, 11 )


#prelim.DrawLatex( 0.5, 0.91, "#scale[0.8]{CMS Preliminary, 13 TeV, 2553 pb^{-1}}" )
#prelim.DrawLatex( 0.2, 0.83, "#scale[0.8]{"+text+"}" )
insertlogo( main, 4, 11 )
st1.GetXaxis().SetRangeUser(500.0,arange)
sub.cd()
gPad.SetLeftMargin(.16)
totalH = st1.GetStack().Last().Clone("totalH")
#totalH.Add(TTmcFS)
pull = WPF.Make_Pull_plot( DataFS1,totalH,totalH,totalH )


	
#pull.GetXaxis().SetRangeUser(0,3000)
pull.SetFillColor(kBlue)
pull.SetTitle(';M_{tb} (GeV);(Data-Bkg)/#sigma')
pull.SetStats(0)


pull.GetYaxis().SetRangeUser(-2.9,2.9)
pull.GetXaxis().SetLabelSize(0.05)
pull.GetYaxis().SetLabelSize(0.05)


LS = .13

pull.GetYaxis().SetTitleOffset(0.4)
pull.GetXaxis().SetTitleOffset(0.9)
pull.SetStats(0)
    

pull.GetYaxis().SetLabelSize(LS)
pull.GetYaxis().SetTitleSize(LS)
pull.GetYaxis().SetNdivisions(306)
pull.GetXaxis().SetLabelSize(LS)
pull.GetXaxis().SetTitleSize(LS)
if plotdata:
	pull.Draw("hist")
pull.GetXaxis().SetRangeUser(500.0,arange)

line2=ROOT.TLine(500.0,0.0,arange,0.0)
line2.SetLineColor(0)
line1=ROOT.TLine(500.0,0.0,arange,0.0)
line1.SetLineStyle(2)

line2.Draw()
line1.Draw()
gPad.Update()

main.RedrawAxis()

c1.Print('plots/MthbvsBkg_BifPoly_fit_'+extex+setstring+'PSET_'+options.cuts+'.root', 'root')
c1.Print('plots/MthbvsBkg_BifPoly_fit_'+extex+setstring+'PSET_'+options.cuts+'.pdf', 'pdf')
c1.Print('plots/MthbvsBkg_BifPoly_fit_'+extex+setstring+'PSET_'+options.cuts+'.png', 'png')
main.SetLogy()
st1.SetMaximum( DataFS.GetMaximum() * 6000 )
st1.SetMinimum( amin)
main.RedrawAxis()

c1.Print('plots/MthbvsBkgsemilog_BifPoly_fit_'+extex+setstring+'PSET_'+options.cuts+'.root', 'root')
c1.Print('plots/MthbvsBkgsemilog_BifPoly_fit_'+extex+setstring+'PSET_'+options.cuts+'.pdf', 'pdf')
c1.Print('plots/MthbvsBkgsemilog_BifPoly_fit_'+extex+setstring+'PSET_'+options.cuts+'.png', 'png')

