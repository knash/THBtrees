#! /usr/bin/env python
import os
from math import *

from optparse import OptionParser
parser = OptionParser()
parser.add_option('-p', '--plot', metavar='F', type='string', action='store',
                  default	=	'tmass',
                  dest		=	'plot',
                  help		=	'mtw or tmass')
(options, args) = parser.parse_args()

import ROOT
import array
import glob
import sys
from array import *
from ROOT import *
if options.plot == "tmass":
	title = ';M_{jet} (GeV);Counts / (8GeV)'
	xaxisrange = [140,350]
	string = ""
if options.plot == "mtw":
	title = ';M_{tW} (GeV);Counts'
	xaxisrange = [500,4000]
	string = "_mtw"
ROOT.gROOT.Macro("rootlogon.C")

st1= ROOT.THStack("st1", "st1")
st2= ROOT.THStack("st2", "st2")
st3= ROOT.THStack("st3", "st3")

leg = TLegend(0.45, 0.42, 0.84, 0.84)
leg.SetFillColor(0)
leg.SetBorderSize(0)

c1 = TCanvas('c1', 'Data Full selection vs b pt tagging background', 1400, 600)
c1.Divide(2,1)
c1.cd(1)

File = ROOT.TFile("TWPlotter_For_Plotting_ptuw_invtau21"+string+".root")

ttjets = File.Get("TTBAR")
ttjetssub = File.Get("TTBARSUB")
data = File.Get("DATA")
qcd = File.Get("QCD")
ttqcd = File.Get("ttQCD")

ttjets.SetFillColor(TROOT.kRed)



qcdcorr = qcd.Clone("qcdcorr")
qcdcorr.Add(ttQCD)
qcdcorr.Add(ttjetssub,-1)
qcdcorr.SetFillColor(TROOT.kYellow)


qcdcorrind = qcdcorr.Clone("qcdcorrind")
qcdcorrind.SetFillColor(TROOT.kYellow)
ttqcdcorr = qcdcorr.Clone("ttqcdcorr")
ttqcdcorr.SetFillColor(TROOT.kYellow-2)

leg.AddEntry( data, 'Data', 'P')
leg.AddEntry( qcdcorrind, 'Independent QCD Contribution', 'F')
leg.AddEntry( ttqcdcorr, 't#bar{t} dependent QCD Contribution', 'F')
leg.AddEntry( ttjets, 't#bar{t} Monte Carlo Prediction', 'F')

qcdcorrind.Scale(qcd.Integral()/(qcd.Integral()+ttqcd.Integral()))
ttqcdcorr.Scale(ttqcd.Integral()/(qcd.Integral()+ttqcd.Integral()))

st1.Add(qcdcorrind)
st1.Add(ttqcdcorr)
st1.Add(ttjets)
c1.cd(1)
st1.SetMaximum(data.GetMaximum() * 1.5)
st1.SetMinimum(1.0)
st1.SetTitle(title)
st1.Draw("hist")
st1.GetXaxis().SetRangeUser(xaxisrange[0],xaxisrange[1])
gPad.SetLeftMargin(0.12)
st1.GetYaxis().SetTitleOffset(0.98)
data.Draw("samep")
leg.Draw()
leg1 = leg.Clone()
prelim = TLatex()
prelim.SetNDC()
prelim.DrawLatex( 0.2, 0.91, "#scale[0.8]{CMS Preliminary, 8 TeV, 19.7 fb^{-1}  Pre Fitting}" )





c1.cd(2)
ttjetsscale = ttjets.Clone("ttjetsscale")
ttqcdscale = ttqcd.Clone("ttqcdscale")
ttjetssubscale = ttjetssub.Clone("ttjetssubscale")
ttjetsscaleup = ttjets.Clone("ttjetsscaleup")
ttjetsscaledown = ttjets.Clone("ttjetsscaledown")


factor = 0.79
factor1 = 0.97
unc = 0.17

ttjetsscale.Scale(factor)
ttjetssubscale.Scale(factor)
ttqcdscale.Scale(factor1)
ttjetsscaleup.Scale(factor+unc)
ttjetsscaledown.Scale(factor-unc)

qcdcorr2 = qcd.Clone("qcdcorr2")
qcdcorr2.Add(ttqcdscale)
qcdcorr2.Add(ttjetssubscale,-1)

qcdcorrind2 = qcdcorr2.Clone("qcdcorrind2")
qcdcorrind2.SetFillColor(TROOT.kYellow)
ttqcdcorr2 = qcdcorr2.Clone("ttqcdcorr2")
ttqcdcorr2.SetFillColor(TROOT.kYellow-2)

qcdcorrind2.Scale(qcd.Integral()/(qcd.Integral()+ttqcdscale.Integral()))
ttqcdcorr2.Scale(ttqcdscale.Integral()/(qcd.Integral()+ttqcdscale.Integral()))






ttjetsscaleup.Add(qcdcorr2)
ttjetsscaledown.Add(qcdcorr2)

st2.Add(qcdcorrind2)
st2.Add(ttqcdcorr2)
st2.Add(ttjetsscale)

st2.SetMaximum(data.GetMaximum() * 1.5)
st2.SetMinimum(1.0)
st2.SetTitle(title)

st2.Draw("hist")
gPad.SetLeftMargin(0.12)
st2.GetYaxis().SetTitleOffset(0.98)
data.Draw("samep")
st2.GetXaxis().SetRangeUser(xaxisrange[0],xaxisrange[1])
ttjetsscaleup.SetLineStyle(2)
ttjetsscaledown.SetLineStyle(2)
ttjetsscaleup.SetLineWidth(2)
ttjetsscaledown.SetLineWidth(2)
ttjetsscaleup.SetFillColor(0)
ttjetsscaledown.SetFillColor(0)
ttjetsscaleup.SetLineColor(4)
ttjetsscaledown.SetLineColor(4)
ttjetsscaleup.Draw("hist same")
ttjetsscaledown.Draw("hist same")
leg1.AddEntry( ttjetsscaleup, '1#sigma uncertainty', 'l')
leg1.Draw()
prelim.DrawLatex( 0.2, 0.91, "#scale[0.8]{CMS Preliminary, 8 TeV, 19.7 fb^{-1}  Post Fitting}" )

c1.Print('plots/ttbarfittingfromtheta_normonly_'+options.plot+'.root', 'root')
c1.Print('plots/ttbarfittingfromtheta_normonly_'+options.plot+'.pdf', 'pdf')


leg = TLegend(0.45, 0.42, 0.84, 0.84)
leg.SetFillColor(0)
leg.SetBorderSize(0)

st3.Add(qcdcorr)
st3.Add(ttjetsscale)

leg.AddEntry( data, 'Data', 'P')
leg.AddEntry( qcdcorr, 'QCD', 'F')
leg.AddEntry( ttjetsscale, 't#bar{t}', 'F')


st3.SetMaximum(data.GetMaximum() * 1.5)
st3.SetMinimum(1.0)
st3.SetTitle(title)

st3.Draw("hist")
gPad.SetLeftMargin(0.12)
st3.GetYaxis().SetTitleOffset(0.98)
data.Draw("samep")
st3.GetXaxis().SetRangeUser(xaxisrange[0],xaxisrange[1])
leg.Draw()
prelim.DrawLatex( 0.2, 0.91, "#scale[0.8]{CMS Preliminary, 8 TeV, 19.7 fb^{-1}  Post Fitting}" )

c1.Print('plots/ttbarfittingfromthetafullqcd_normonly_'+options.plot+'.root', 'root')
c1.Print('plots/ttbarfittingfromthetafullqcd_normonly_'+options.plot+'.pdf', 'pdf')


