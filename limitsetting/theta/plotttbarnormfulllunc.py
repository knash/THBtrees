#! /usr/bin/env python
import os
from math import *

from optparse import OptionParser


import ROOT
import copy
import array
import glob
import sys
from array import *
from ROOT import *

title = ';M_{jet} (GeV);Counts / (8GeV)'
xaxisrange = [120,350]

ROOT.gROOT.Macro("rootlogon.C")

st1= ROOT.THStack("st1", "st1")

st2= ROOT.THStack("st2", "st2")

leg = TLegend(0.45, 0.42, 0.84, 0.84)
leg.SetFillColor(0)
leg.SetBorderSize(0)

c1 = TCanvas('c1', 'Data Full selection vs b pt tagging background', 1400, 600)
c1.Divide(2,1)
c1.cd(1)
indir = ""
pre = ROOT.TFile("BStar_tmass_forTheta.root")
post = ROOT.TFile(indir+"histos-bstar-mle_syst.root")

ttjets = pre.Get("mt_allhad__ttbar")
ttjetssub = copy.copy(ttjets)
data = pre.Get("mt_allhad__DATA")
qcd = pre.Get("mt_allhad__qcd")
ttqcd = pre.Get("mt_allhad__ttqcd")

ttjets.SetFillColor(ROOT.kRed)

ttjetssub.Scale(0.0)


qcdcorr = qcd.Clone("qcdcorr")
qcdcorr.Add(ttqcd)
qcdcorr.Add(ttjetssub,-1)

qcdcorrind = qcdcorr.Clone("qcdcorrind")
qcdcorrind.SetFillColor(ROOT.kYellow)
ttqcdcorr = qcdcorr.Clone("ttqcdcorr")
ttqcdcorr.SetFillColor(ROOT.kYellow-2)

leg.AddEntry( data, 'Data', 'P')
leg.AddEntry( qcdcorrind, 't#bar{t} Independent QCD Contribution', 'F')
leg.AddEntry( ttqcdcorr, 't#bar{t} Dependent QCD Contribution', 'F')
leg.AddEntry( ttjets, 't#bar{t} Monte Carlo Prediction', 'F')

qcdcorrind.Scale(qcd.Integral()/(qcd.Integral()+ttqcd.Integral()))
ttqcdcorr.Scale(ttqcd.Integral()/(qcd.Integral()+ttqcd.Integral()))

st1.Add(qcdcorrind)
st1.Add(ttqcdcorr)
st1.Add(ttjets)
c1.cd(1)
st1.SetMaximum(data.GetMaximum() * 2.5)
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
ttjetssubscale = ttjetssub.Clone("ttjetssubscale")
ttjetsscaleup = ttjets.Clone("ttjetsscaleup")
ttjetsscaledown = ttjets.Clone("ttjetsscaledown")
qcdpost = post.Get("mt_allhad__qcd")
ttqcdpost = post.Get("mt_allhad__ttqcd")

factor = 0.994206693679
#factor1 = 0.97
unc = 0.146995985743

ttjetsscale.Scale(factor)
ttjetssubscale.Scale(factor)
ttjetsscaleup.Scale(factor+unc)
ttjetsscaledown.Scale(factor-unc)

qcdpostcorrind2 = qcdpost.Clone("qcdpostcorrind2")
ttsub1 = ttjetssubscale.Clone("ttsub1")
ttsub1.Scale(qcdpost.Integral()/(qcdpost.Integral()+ttqcdpost.Integral()))
qcdpostcorrind2.Add(ttsub1,-1)

ttqcdpostcorr2 = ttqcdpost.Clone("ttqcdpostcorr2")
ttsub2 = ttjetssubscale.Clone("ttsub2")
ttsub2.Scale(ttqcdpost.Integral()/(qcd.Integral()+ttqcdpost.Integral()))
ttqcdpostcorr2.Add(ttsub2,-1)


qcdpostcorrind2.SetFillColor(ROOT.kYellow)
ttqcdpostcorr2.SetFillColor(ROOT.kYellow-2)






ttjetsscaleup.Add(qcdpostcorrind2)
ttjetsscaleup.Add(ttqcdpostcorr2)
ttjetsscaledown.Add(qcdpostcorrind2)
ttjetsscaledown.Add(ttqcdpostcorr2)

st2.Add(qcdpostcorrind2)
st2.Add(ttqcdpostcorr2)
st2.Add(ttjetsscale)

st2.SetMaximum(data.GetMaximum() * 2.5)
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

c1.Print('plots/ttbarfittingfromtheta.root', 'root')
c1.Print('plots/ttbarfittingfromtheta.pdf', 'pdf')

