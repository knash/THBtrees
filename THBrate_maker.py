



###################################################################
##								 ##
## Name: Tagrate_Maker_B.py				         ##
## Author: Kevin Nash 						 ##
## Date: 6/5/2012						 ##
## Purpose: This program takes the root files created by  	 ##
##          TBrate.py and creates the average b-tagging rate, 	 ##
##	    then fits the average b-tagging rates		 ##
##          tagrates with a several functions 			 ##
##	    which are stored in the fitdata folder to be used    ##
##	    to weight the pre b tagged sample and create	 ##
##	    QCD background estimates				 ##
##								 ##
###################################################################

import os
import array
import glob
import math
import ROOT
import sys
from array import *
from optparse import OptionParser
import CMS_lumi
parser = OptionParser()

parser.add_option('-s', '--set', metavar='F', type='string', action='store',
                  default	=	'data',
                  dest		=	'set',
                  help		=	'data or QCD')

parser.add_option('-c', '--cuts', metavar='F', type='string', action='store',
                  default	=	'default',
                  dest		=	'cuts',
                  help		=	'Cuts type (ie default, rate, etc)')

parser.add_option('-u', '--ptreweight', metavar='F', type='string', action='store',
                  default	=	'on',
                  dest		=	'ptreweight',
                  help		=	'on or off')

parser.add_option('--batch', metavar='F', action='store_true',
                  default=False,
                  dest='batch',
                  help='batch')
(options, args) = parser.parse_args()

if options.batch:
	ROOT.gROOT.SetBatch(True)
	ROOT.PyConfig.IgnoreCommandLineOptions = True

ROOT.gROOT.Macro("rootlogon.C")

import WprimetoVlq_Functions	
from WprimetoVlq_Functions import *


rwstr = ''
if options.ptreweight=='off':
	rwstr = '_PTRWoff'


print "Running on "+options.set
fttbar = TFile("rootfiles/THBrateweightedttbar"+rwstr+"_PSET_"+options.cuts+".root")
#fst = TFile(rootdir+"TBratefileST_PSET_"+options.cuts+".root")

fdata = TFile("rootfiles/THBrate"+options.set+"_PSET_"+options.cuts+".root")
fsig0 = TFile("rootfiles/THBrateweightedTHBWp1500Tp1000_PSET_"+options.cuts+".root")
fsig1 = TFile("rootfiles/THBrateweightedTHBWp1500Bp1000_PSET_"+options.cuts+".root")

toprint = []

output = TFile( "THBrate_Maker"+rwstr+"_"+options.set+"_PSET_"+options.cuts+".root", "recreate" )
output.cd()
for i in range(0,2):
	for j in range(0,2):
		for k in range(0,2):
			for hname in  ['','e1','e2']:
				for ttsub in  ['','unsub','sigsub']:#,'e1','e2']:
					if i!=1:
						continue 

					neta1 = fdata.Get("Pth"+hname+"_h1t"+str(j)+"b"+str(k))
					deta1 = fdata.Get("Pth"+hname+"_h0t"+str(j)+"b"+str(k))
					#print "DATA"



					signeta1 = fsig0.Get("Pth"+hname+"_h1t"+str(j)+"b"+str(k))
					sigdeta1 = fsig0.Get("Pth"+hname+"_h0t"+str(j)+"b"+str(k))


					signeta1.Add(fsig1.Get("Pth"+hname+"_h1t"+str(j)+"b"+str(k)))
					sigdeta1.Add(fsig1.Get("Pth"+hname+"_h0t"+str(j)+"b"+str(k)))


					ttneta1 = fttbar.Get("Pth"+hname+"_h1t"+str(j)+"b"+str(k))
					ttdeta1 = fttbar.Get("Pth"+hname+"_h0t"+str(j)+"b"+str(k))




					#if hname=='':
						#print "TT"
						#print ttneta1.Integral()
						#print ttdeta1.Integral()

						#print "TTFrac"
						#print ttneta1.Integral()/(ttneta1.Integral()+neta1.Integral())*100.0,"%"
						#print ttdeta1.Integral()/(ttdeta1.Integral()+deta1.Integral())*100.0,"%"


					if hname=='':
						bins= [300,350,400,450,500,600,800,3000]

						mthbneta1 = fdata.Get("Mthb"+hname+"_h1t"+str(j)+"b"+str(k))
						mthbdeta1 = fdata.Get("Mthb"+hname+"_h0t"+str(j)+"b"+str(k))

						mthbsigneta1 = fsig0.Get("Mthb"+hname+"_h1t"+str(j)+"b"+str(k))
						mthbsigdeta1 = fsig0.Get("Mthb"+hname+"_h0t"+str(j)+"b"+str(k))


						mthbsigneta1.Add(fsig1.Get("Mthb"+hname+"_h1t"+str(j)+"b"+str(k)))
						mthbsigdeta1.Add(fsig1.Get("Mthb"+hname+"_h0t"+str(j)+"b"+str(k)))

						mthbttneta1 = fttbar.Get("Mthb"+hname+"_h1t"+str(j)+"b"+str(k))
						mthbttdeta1 = fttbar.Get("Mthb"+hname+"_h0t"+str(j)+"b"+str(k))

						if options.set=='QCD':
							mthbbins= [1000,2200,3000,7000]
						else:
							mthbbins= [1000,1500,2000,3000,7000]

						mthbbins2=array('d',mthbbins)

						mthbneta1r = mthbneta1.Rebin(len(mthbbins2)-1,"mthbneta1r",mthbbins2)
						mthbdeta1r = mthbdeta1.Rebin(len(mthbbins2)-1,"mthbdeta1r",mthbbins2)




						mthbsigneta1r = mthbsigneta1.Rebin(len(mthbbins2)-1,"mthbsigneta1r",mthbbins2)
						mthbsigdeta1r = mthbsigdeta1.Rebin(len(mthbbins2)-1,"mthbsigdeta1r",mthbbins2)



						mthbttneta1r = mthbttneta1.Rebin(len(mthbbins2)-1,"mthbttneta1r",mthbbins2)
						mthbttdeta1r = mthbttdeta1.Rebin(len(mthbbins2)-1,"mthbttdeta1r",mthbbins2)



						if options.set=='data' and ttsub!='unsub':
							print "subtracting ttbar"
							mthbneta1r.Add(mthbttneta1r,-1)
							mthbdeta1r.Add(mthbttdeta1r,-1)


						mthbtagrateeta1 = mthbneta1r.Clone("mthbtagrateeta1")
						mthbtagrateeta1.Divide(mthbdeta1r)
						mthbtagrateeta1.Write("t"+str(j)+"b"+str(k)+hname+ttsub+"mthb")

					if hname=='e1':
						bins= [300,350,400,500,750,3000]
					if hname=='e2':
						bins= [300,400,500,650,3000]





					bins2=array('d',bins)

					neta1r = neta1.Rebin(len(bins2)-1,"neta1r",bins2)
					deta1r = deta1.Rebin(len(bins2)-1,"deta1r",bins2)


					signeta1r = signeta1.Rebin(len(bins2)-1,"signeta1r",bins2)
					sigdeta1r = sigdeta1.Rebin(len(bins2)-1,"sigdeta1r",bins2)

					ttneta1r = ttneta1.Rebin(len(bins2)-1,"ttneta1r",bins2)
					ttdeta1r = ttdeta1.Rebin(len(bins2)-1,"ttdeta1r",bins2)

					if options.set=='data' and ttsub!='unsub':
						print "subtracting ttbar"
						neta1r.Add(ttneta1r,-1)
						deta1r.Add(ttdeta1r,-1)

					if options.set=='data' and ttsub == 'sigsub':
						print "subtracting signal"
						print "sigsubn",signeta1r.Integral(),neta1r.Integral(),signeta1r.Integral()/neta1r.Integral()
						print "sigsubd",sigdeta1r.Integral(),deta1r.Integral(),sigdeta1r.Integral()/deta1r.Integral()
						print "rate pre",neta1r.Integral()/deta1r.Integral()
						neta1r.Add(signeta1r,-1)
						deta1r.Add(sigdeta1r,-1)
						print "rate post",neta1r.Integral()/deta1r.Integral()


					if ttsub != 'unsub':
						totnormN = neta1r.Integral()+ttneta1r.Integral()
						totnormD = deta1r.Integral()+ttdeta1r.Integral()
						toprint.append("h1t"+str(j)+"b"+str(k))
						toprint.append("Rate "+hname+" "+str(neta1r.Integral()/deta1r.Integral()))
						toprint.append("Subbed N "+str(100*ttneta1r.Integral()/totnormN)+"% D "+str(100*ttdeta1r.Integral()/totnormD)+"%")
					#if hname=='':
						#print "num ",neta1r.Integral()
						#print "den",deta1r.Integral()

						#print "sig num ",signeta1.Integral()
						#print "sig den ",sigdeta1.Integral()

					tagrateeta1 = neta1r.Clone("tagrateeta1")
					tagrateeta1.Divide(deta1r)
					tagrateeta1.Write("t"+str(j)+"b"+str(k)+hname+ttsub)

					c1 = TCanvas('c1', '', 700, 600)
				
					c1.SetLeftMargin(0.16)
					c1.SetRightMargin(0.05)
					c1.SetTopMargin(0.11)
					c1.SetBottomMargin(0.16)

					tagrateeta1.GetYaxis().SetRangeUser(min(0.0,0.25*tagrateeta1.GetMinimum()),max(0.0,1.6*tagrateeta1.GetMaximum()))
					tagrateeta1.SetStats(0)
					legstr = "N/D"

					if j==0:
						if k==0:
							legstr = "CR6/CR5"
						if k==1:
							legstr = "CR2/CR1"
					else:
							legstr = "Err"
					
					tagrateeta1.SetTitle(";Higgs candidate p_{T};"+legstr)
					ROOT.gStyle.SetErrorX()
					tagrateeta1.Draw('pe1')



					if ttsub == '':
						TEMPHIST = copy.copy(tagrateeta1)

					if ttsub == 'unsub' or ttsub == 'sigsub':


						leg = TLegend(0.55, 0.65, 0.84, 0.84)
						leg.SetFillColor(0)
						leg.SetBorderSize(0)

						TEMPHIST.SetLineColor(2)
						TEMPHIST.SetMarkerColor(2)
						CMS_lumi.CMS_lumi(c1, 4, 11)
    						TPT = ROOT.TPaveText(.65, .55, .75, .65,"NDC")
						if hname == 'e1':
    							TPT.AddText("|#eta|<1")
						if hname == 'e2':
    							TPT.AddText("|#eta|>1")
						leg.AddEntry( TEMPHIST, 't#bar{t} MC subtracted', 'lpe')
						leg.AddEntry( tagrateeta1, 't#bar{t} MC unsubtracted', 'lpe')
						TEMPHIST.Draw('pe1same')

						TPT.SetFillColor(0)
						TPT.SetBorderSize(0)
						TPT.SetTextAlign(12)

						TPT.Draw()
						leg.Draw()

					c1.Print('plots/Hrate'+ttsub+'_'+hname+"_h1t"+str(j)+"b"+str(k)+'PSET_'+options.cuts+'.root', 'root')
					c1.Print('plots/Hrate'+ttsub+'_'+hname+"_h1t"+str(j)+"b"+str(k)+'PSET_'+options.cuts+'.pdf', 'pdf')
					c1.Print('plots/Hrate'+ttsub+'_'+hname+"_h1t"+str(j)+"b"+str(k)+'PSET_'+options.cuts+'.png', 'png')

for pr in toprint:
	print pr
output.Write()
output.Close()

