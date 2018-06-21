
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


files =[
'limits_outputlim_theta_unblind_AllHadronicTEST_h1t1b1defaultcenter0p01p0_logcenter.root',
'limits_outputlim_theta_unblind_AllHadronicTEST_h1t1b1defaultcenter0p10p9_logcenter.root', 
'limits_outputlim_theta_unblind_AllHadronicTEST_h1t1b1defaultcenter0p20p8_logcenter.root', 
'limits_outputlim_theta_unblind_AllHadronicTEST_h1t1b1defaultcenter0p30p7_logcenter.root', 
'limits_outputlim_theta_unblind_AllHadronicTEST_h1t1b1defaultcenter0p40p6_logcenter.root', 
'limits_outputlim_theta_unblind_AllHadronic_logcenter.root',
'limits_outputlim_theta_unblind_AllHadronicTEST_h1t1b1defaultcenter0p60p4_logcenter.root', 
'limits_outputlim_theta_unblind_AllHadronicTEST_h1t1b1defaultcenter0p70p3_logcenter.root', 
'limits_outputlim_theta_unblind_AllHadronicTEST_h1t1b1defaultcenter0p80p2_logcenter.root',
'limits_outputlim_theta_unblind_AllHadronicTEST_h1t1b1defaultcenter0p90p1_logcenter.root', 
'limits_outputlim_theta_unblind_AllHadronicTEST_h1t1b1defaultcenter1p00p0_logcenter.root', 
]

legz =[
'BR T=0.0, BR B=1.0', 
'BR T=0.1, BR B=0.9', 
'BR T=0.2, BR B=0.8', 
'BR T=0.3, BR B=0.7', 
'BR T=0.4, BR B=0.6', 
'BR T=0.5, BR B=0.5', 
'BR T=0.6, BR B=0.4', 
'BR T=0.7, BR B=0.3', 
'BR T=0.8, BR B=0.2', 
'BR T=0.9, BR B=0.1', 
'BR T=1.0, BR B=0.0', 
]

cmugh = TCanvas('cmugh', '', 1000, 800)
obss,exps = [],[]
cols = [2,3,4,6,7,8,9,10,11,12,13,14,15]

iii=0
leg = TLegend(0.2, 0.5, 0.84, 0.84)

leg.SetFillColor(0)
leg.SetBorderSize(0)

for curfilestr in files:
	curfile=TFile(curfilestr)


	obss.append(curfile.Get('obs'))
	exps.append(curfile.Get('exp'))
	leg.AddEntry(obss[-1],"Limit at "+str(legz[iii]),"l")
	#leg.AddEntry(exps[-1],"observed limit at "+str(legz[iii]))
	obss[-1].SetLineColor(cols[iii])
	exps[-1].SetLineColor(cols[iii])
	obss[-1].SetLineWidth(1)
	exps[-1].SetLineWidth(1)
	if iii==0:
		exps[-1].SetMinimum(5.e-4)
		exps[-1].SetMaximum(2000.)
		cmugh.SetLogy()
    #g_mclimit.GetXaxis().SetTitle("m_{W'} (TeV)")
    #g_mclimit.GetYaxis().SetTitle("Upper Limit #sigma_{W'} #times #bf{#it{#Beta}}( W' #rightarrow (Tb,tB) #rightarrow tHb) (pb)")

    #g_mclimit.GetYaxis().SetTitleSize(0.03)
    #g_mclimit.GetYaxis().SetTitleOffset(1.9)
		exps[-1].Draw()
	else:
		exps[-1].Draw('same')
	obss[-1].Draw('same')
	iii+=1
WPh = curfile.Get('WP')
WPh.SetLineColor(4)
WPh.Draw('same')
leg.Draw()
cmugh.Print('plots/limitcombined_center.root', 'root')
cmugh.Print('plots/limitcombined_center.pdf', 'pdf')
cmugh.Print('plots/limitcombined_center.png', 'png')
