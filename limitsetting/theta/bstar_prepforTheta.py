import ROOT, sys, os, re, string,copy
from ROOT import *
f_bs = TFile("BStar_tmass_forTheta.root", "RECREATE")
f_bsno = TFile("BStarCombinationHistos_Right_Allhadronic_noTTsub.root")
f_bsdub = TFile("BStarCombinationHistos_Right_Allhadronic_doubleTTsub.root")
print "keys"
f_bsno.cd()
for key in f_bsno.GetListOfKeys():
	print key



histosqcd = [
"mt_allhad__qcd",
"mt_allhad__qcd__Fit__plus",
"mt_allhad__qcd__Fit__minus",
"mt_allhad__qcd__Alt__plus",
"mt_allhad__qcd__Alt__minus",
"mt_allhad__qcd__modm__plus",
"mt_allhad__qcd__modm__minus"
]

histosttbar = [
"mt_allhad__ttbar"
]
f_bs.cd()

datahist  = f_bsno.Get("mt_allhad__DATA")
datahist.Write()
for hist in histosqcd:
	histno = f_bsno.Get(hist)
	histdub = f_bsdub.Get(hist)
	histdub.Write()
	histnom = copy.copy(histno)
	histnom.Add(histdub,-1)
	histnom.Scale(0.5)
	histnom.Write(hist.replace("mt_allhad__qcd","mt_allhad__ttqcd"))
for hist in histosttbar:
	histno = f_bsno.Get(hist)
	histno.Write()
f_bs.Write()
f_bs.Close()

