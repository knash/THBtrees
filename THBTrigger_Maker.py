
import os
import array
import glob
import math
import ROOT
import sys
from array import *
from ROOT import *
from optparse import OptionParser

parser = OptionParser()

parser.add_option('-s', '--set', metavar='F', type='string', action='store',
                  default	=	'singlemu',
                  dest		=	'set',
                  help		=	'dataset (ie data,ttbar etc)')

parser.add_option('-d', '--disc', metavar='F', type='string', action='store',
                  default	=	'',
                  dest		=	'disc',
                  help		=	'   ')

parser.add_option('-b', '--bx', metavar='F', type='string', action='store',
                  default	=	'25ns',
                  dest		=	'bx',
                  help		=	'bunch crossing 50ns or 25ns')


parser.add_option('--batch', metavar='F', action='store_true',
                  default=False,
                  dest='batch',
                  help='batch')

(options, args) = parser.parse_args()



if options.batch:
	ROOT.gROOT.SetBatch(True)
	ROOT.PyConfig.IgnoreCommandLineOptions = True


gROOT.Macro("rootlogon.C")
# Create the outfiles that will store fit and sigma data for use later
c1 = TCanvas('c1', 'Data Full selection vs b pt tagging background', 700, 500)

leg = TLegend(0.0, 0.0, 1.0, 1.0)
leg.SetFillColor(0)
leg.SetBorderSize(0)

trigs = [
"HLT_PFHT900ORHLT_PFHT800ORHLT_JET450_pre_HLT_IsoMu24",
]




histomajigs = ['Ht','Hthistwkinwhtcut','Mthbhistwkinwhtcut','Mthbhist']
#histomajigs = ['Ht']

Trigfile = ROOT.TFile( "Triggerweight_"+options.set+".root", "recreate" )
#Trigfile = ROOT.TFile( "Triggertestington.root", "recreate" )
njig=0																									
for hjig in histomajigs:

	leg1 = TLegend(0.4, 0.4, 0.8, 0.8)
	leg1.SetFillColor(0)
	leg1.SetBorderSize(0)


	print 
	print hjig 
	TR = []
	fvec = []
	for ifile in range(0,len(trigs)) :
		fname="triggerstudies/THBTrigger"+options.set+trigs[ifile]+".root"
		sigfs = [ROOT.TFile("triggerstudies/THBTriggerTHBWp1500Bp1000HLT_PFHT900ORHLT_PFHT800ORHLT_JET450_pre_HLT_IsoMu24.root"),ROOT.TFile("triggerstudies/THBTriggerTHBWp2000Bp1300HLT_PFHT900ORHLT_PFHT800ORHLT_JET450_pre_HLT_IsoMu24.root")]
		sigfstr = ["1500","2000"]
		print "name",fname
		fvec.append(ROOT.TFile(fname))
		#fvec.append(ROOT.TFile("THBTriggerdataFHLT_PFHT900ORHLT_PFHT800ORHLT_JET450_pre_HLT_PFHT475,HLT_JET260_job1of100.root"))
		HT = fvec[ifile].Get(hjig)
		HTpre = fvec[ifile].Get(hjig+'pre')

		print "HTI",HT.Integral()
		print "HTpre",HTpre.Integral()
		if hjig == 'Hthistwkinwhtcut':
			HT.Rebin(10)
			HTpre.Rebin(10)
	
		else:
			HT.Rebin(5)
			HTpre.Rebin(5)
	
		print trigs[ifile]
		#print HT.Integral()/HTpre.Integral()
		#print HT.Integral(HT.FindBin(550),HT.FindBin(2000))/HTpre.Integral(HT.FindBin(550),HT.FindBin(2000))
		TR.append(HT.Clone())

		g_efficiency = ROOT.TGraphAsymmErrors()
		g_efficiency.Divide(TR[ifile],HTpre,"cl=0.683 b(1,1) mode")



		TR[ifile].Divide(TR[ifile],HTpre,1.0,1.0,'B')

		TR[ifile].SetLineColor(ifile+1)
		TR[ifile].SetMarkerColor(ifile+1)

		if ifile >= 4:
			TR[ifile].SetLineColor(ifile+2)
			TR[ifile].SetMarkerColor(ifile+2)

		
		leg.AddEntry(TR[ifile] , trigs[ifile].replace('OR',' OR '), 'p')

		Tline = TLine(1000.0, 0.0, 1000.0, 1.01)
		Tline.SetLineColor(kRed)
		Tline.SetLineStyle(2)
		c1.cd()

		g_efficiency.SetMaximum(1.01)
		g_efficiency.SetMinimum(0.0)
		g_efficiency.GetXaxis().SetRangeUser(600,2000)
		#g_efficiency.SetStats(0)
		if hjig.find('Mthb')!=-1:
			g_efficiency.SetTitle(';m_{tHb} (GeV);Efficiency / 50 GeV')					
		else:
			g_efficiency.SetTitle(';#sum pT (GeV);Efficiency / 50 GeV')		


		TR[ifile].SetMaximum(1.01)
		TR[ifile].SetMinimum(0.2)
		TR[ifile].GetXaxis().SetRangeUser(600,2000)
		TR[ifile].SetStats(0)
		TR[ifile].SetTitle('; (GeV);Efficiency / 50 GeV')



		if ifile ==0:

			g_efficiency.SetMarkerStyle(8)
			g_efficiency.Draw("pe")
			leg1.AddEntry( g_efficiency, 'data', 'ple')

		else:
			g_efficiency.Draw("pesame")

		gPad.SetLeftMargin(.15)
		gPad.SetBottomMargin(.45) 
		TR[ifile].GetXaxis().SetTitleOffset(0.8)
		g_efficiency.GetXaxis().SetTitleOffset(1.2)
		TR[ifile].GetYaxis().SetTitleOffset(0.8)
		g_efficiency.GetYaxis().SetTitleOffset(0.8)
		Trigfile.cd()
		if hjig	=='Ht':	
			TR[ifile].Write("TriggerWeight_"+trigs[ifile])
		if hjig == 'Hthistwkinwhtcut':
			TR[ifile].SetMinimum(0.0)
			print "writing", trigs[ifile]
			TR[ifile].Write("TriggerWeight_Hthistwkinwhtcut"+trigs[ifile])
		c3 = TCanvas('c3', 'Data Full selection vs b pt tagging background', 700, 500)
		leg.AddEntry( g_efficiency, 'Data', 'lpe')
		g_efficiency.Draw("AP")
		#if hjig == 'Hthistwkinwhtcut':
		#	continue 
		signu = 0
		for sigsig in sigfs:

			print 	hjig+'preuntrig'
			if hjig == "Ht":
				sigsigf = sigsig.Get(hjig+'preuntrig')

			else:
				sigsigf = sigsig.Get(hjig+'untrig')
			
			if hjig == 'Hthistwkinwhtcut':
				sigsigf.Rebin(10)
			else:
				sigsigf.Rebin(5)
			sigsigf.Scale(3.0/sigsigf.Integral())
			sigsigf.SetLineWidth(2)
			sigsigf.SetLineColor(signu+2)
			leg1.AddEntry( sigsigf, 'Signal (W`_{R} at ' + sigfstr[signu]+' GeV)', 'l')
			sigsigf.Draw("samehist")
			signu +=1
		if hjig == "Ht":
			Tline.Draw()
			leg1.Draw()
		gPad.SetBottomMargin(.15) 
		gPad.Update()
		c3.Print('plots/Trigger'+hjig+'_'+trigs[ifile]+options.disc+'.root', 'root')
		c3.Print('plots/Trigger'+hjig+'_'+trigs[ifile]+options.disc+'.pdf', 'pdf')
		njig+=1																									
#Tline.Draw()
#c1.Print('plots/Trigger_TEMP'+options.disc+'.root', 'root')
#c1.Print('plots/Trigger_TEMP'+options.disc+'.pdf', 'pdf')

#c2 = TCanvas('c2', 'Data Full selection vs b pt tagging background', 700, 200)
#leg.Draw()
#c2.Print('plots/Trigger_TEMP_legend.pdf'+options.disc, 'pdf')

print "write"
Trigfile.Write()
Trigfile.Close()
print "wrote"



