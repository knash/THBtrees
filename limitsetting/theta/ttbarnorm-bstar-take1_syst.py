#! /usr/bin/env python
import os
from math import *

import ROOT
import array
import glob
import sys
from array import *
from ROOT import *




#ttbarunc = 0.2443423375338506
#rawnorm = -0.76153685090179923

ttonlyFile1 = ROOT.TFile("histos-bstar-ttbarrate_syst.root")

subfrac =  0.0

File1 = ROOT.TFile("histos-bstar-ttbarrate_syst.root")
File2 = ROOT.TFile("BStar_tmass_forTheta.root")
File3 = ROOT.TFile("histos-bstar-ttbarrateup_syst.root")
File4 = ROOT.TFile("histos-bstar-ttbarratedown_syst.root")

ttonlyttbar = ttonlyFile1.Get("mt_allhad__ttbar")
ttonlyttqcd = ttonlyFile1.Get("mt_allhad__ttqcd")

data = File2.Get("mt_allhad__DATA")

ttbarpostfit = File1.Get("mt_allhad__ttbar")
ttbarprefit = File2.Get("mt_allhad__ttbar")

qcdpostfit = File1.Get("mt_allhad__qcd")
qcdprefit = File2.Get("mt_allhad__qcd")

ttqcdpostfit = File1.Get("mt_allhad__ttqcd")
ttqcdprefit = File2.Get("mt_allhad__ttqcd")

ttbarpostfitup = File3.Get("mt_allhad__ttbar")
ttbarpostfitdown = File4.Get("mt_allhad__ttbar")

print "Consistency Check for tt scale variation only:"
print "ttbar post / ttbar pre " + str(ttonlyttbar.Integral()/ttbarprefit.Integral())
print "qcd post / qcd pre " + str(ttonlyttqcd.Integral()/ttqcdprefit.Integral())
print "qcd post predict " + str((ttqcdprefit.Integral())*(ttbarprefit.Integral()/ttonlyttbar.Integral()))
print "qcd post " + str(ttonlyttqcd.Integral())
print "qcd pre " + str(ttqcdprefit.Integral())
print ""

qcdpostfit.Add(ttqcdpostfit)
qcdprefit.Add(ttqcdprefit)


ttbarsubpre =  ttbarprefit.Integral()*subfrac
ttbarsubpost =  ttbarpostfit.Integral()*subfrac

print ttbarpostfitup.Integral()/ttbarpostfit.Integral()
print ttbarpostfitdown.Integral()/ttbarpostfit.Integral()
FracUnc = (ttbarpostfitup.Integral()/ttbarpostfit.Integral())-1
print "Symmetry " + str((ttbarpostfitup.Integral()/ttbarpostfit.Integral() + ttbarpostfitdown.Integral()/ttbarpostfit.Integral())*.5)
print "pre fit"
print "total bkg " + str(qcdprefit.Integral() - ttbarsubpre + ttbarprefit.Integral())
print "data " + str(data.Integral())
print ""
print "Un-corrected numbers"
print "qcd scaled by " + str(qcdpostfit.Integral()/qcdprefit.Integral())
print "ttbar scaled by " + str(ttbarpostfit.Integral()/ttbarprefit.Integral()) + " +/- " + str(FracUnc)
print "total bkg " + str(qcdpostfit.Integral() + ttbarpostfit.Integral())
print "data " + str(data.Integral())
print "ttbar " + str(ttbarpostfit.Integral())
print ""
print "Corrected numbers"
print "qcd scaled by " + str((qcdpostfit.Integral()-ttbarsubpost)/(qcdprefit.Integral()-ttbarsubpre))
#print "ttbar scaled by " + str(ttbarpostfit.Integral()/ttbarprefit.Integral()*(1+subfrac)) + " +/- " + str(newuncertainty*(1+subfrac))
#print "ttbar impact " + str(newuncertainty*(1+subfrac)/(ttbarpostfit.Integral()/ttbarprefit.Integral()*(1+subfrac)))
print "ttbar scaled by " + str(ttbarpostfit.Integral()/ttbarprefit.Integral()*(1+subfrac)) + " +/- " + str(FracUnc*(1+subfrac))
print "ttbar impact " + str(FracUnc*(1+subfrac)/(ttbarpostfit.Integral()/ttbarprefit.Integral()*(1+subfrac)))
print "total bkg " + str(qcdpostfit.Integral()-ttbarsubpost + ttbarpostfit.Integral()*(1+subfrac))
print "data " + str(data.Integral())
print ""
print "ttbar in the end " + str(ttbarpostfit.Integral()*(1+subfrac))
