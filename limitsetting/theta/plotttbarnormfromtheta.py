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
xaxisrange = [100,210]

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

data = pre.Get("mt_allhad__DATA")

ttjetspre = pre.Get("mt_allhad__ttbar")
qcdpre = pre.Get("mt_allhad__qcd")
ttqcdpre = pre.Get("mt_allhad__ttqcd")


data = pre.Get("mt_allhad__DATA")

ttjetspost = post.Get("mt_allhad__ttbar")
qcdpost = post.Get("mt_allhad__qcd")
ttqcdpost = post.Get("mt_allhad__ttqcd")


ttjetspre.SetFillColor(ROOT.kRed)
ttjetspost.SetFillColor(ROOT.kRed)

qcdpre.SetFillColor(ROOT.kYellow)
qcdpost.SetFillColor(ROOT.kYellow)

ttqcdpre.SetFillColor(ROOT.kYellow-2)
ttqcdpost.SetFillColor(ROOT.kYellow-2)

leg.AddEntry( data, 'Data', 'P')
leg.AddEntry( qcdpre, 't#bar{t} Independent QCD Contribution', 'F')
leg.AddEntry( ttqcdpre, 't#bar{t} Dependent QCD Contribution', 'F')
leg.AddEntry( ttjetspre, 't#bar{t} Monte Carlo Prediction', 'F')

st1.Add(qcdpre)
st1.Add(ttqcdpre)
st1.Add(ttjetspre)
c1.cd(1)
st1.SetMaximum(data.GetMaximum() * 2.5)
st1.SetMinimum(1.0)
st1.SetTitle(title)
st1.Draw("hist")
st1.GetXaxis().SetRangeUser(xaxisrange[0],xaxisrange[1])
gPad.SetLeftMargin(0.12)
st1.GetYaxis().SetTitleOffset(0.98)
data.Draw("samep")

leg1 = leg.Clone()
prelim = TLatex()
prelim.SetNDC()
prelim.DrawLatex( 0.2, 0.91, "#scale[0.8]{CMS Preliminary, 8 TeV, 19.7 fb^{-1}  Pre Fitting}" )





c1.cd(2)

st2.Add(qcdpost)
st2.Add(ttqcdpost)
st2.Add(ttjetspost)

st2.SetMaximum(data.GetMaximum() * 2.5)
st2.SetMinimum(1.0)
st2.SetTitle(title)

st2.Draw("hist")
gPad.SetLeftMargin(0.12)
st2.GetYaxis().SetTitleOffset(0.98)
data.Draw("samep")
st2.GetXaxis().SetRangeUser(xaxisrange[0],xaxisrange[1])

data.Draw("samep")

prelim.DrawLatex( 0.2, 0.91, "#scale[0.8]{CMS Preliminary, 8 TeV, 19.7 fb^{-1}  Post Fitting}" )

c1.Print('plots/ttbarfittingfromtheta.root', 'root')
c1.Print('plots/ttbarfittingfromtheta.pdf', 'pdf')

