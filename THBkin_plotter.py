

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

parser.add_option('-z', '--histo', metavar='F', type='string', action='store',
                  default	=	'h1t1b1',
                  dest		=	'histo',
                  help		=	'')

parser.add_option('-e', '--etabin', metavar='F', type='string', action='store',
                  default	=	'True',
                  dest		=	'etabin',
                  help		=	'')

parser.add_option('-u', '--ptreweight', metavar='F', type='string', action='store',
                  default	=	'on',
                  dest		=	'ptreweight',
                  help		=	'on or off')


parser.add_option('--batch', metavar='F', action='store_true',
                  default=False,
                  dest='batch',
                  help='batch')

(options, args) = parser.parse_args()
extex = ""
if options.histo=='h1t1b0':
	extex = "Bfail"
if options.histo=='h1t0b1':
	extex = "Tfail"
cuts = options.cuts

if options.batch:
	ROOT.gROOT.SetBatch(True)
	ROOT.PyConfig.IgnoreCommandLineOptions = True




WPF = WprimetoVlq_Functions(options.cuts)

rwstr = ''
if options.ptreweight=='off':
	rwstr = '_PTRWoff'


rebin =5
plotdata = True
if options.set == 'data' and extex == "":
	#plotdata=False
	plotdata=True

etatext = ''
if options.etabin=='True':
	print "Etaparam"
	etatext = 'ebin'

histos = ['Mthb','Mth','Mbh','Mt','Mh','Ptt','Ptb','Pth','Etab','Etat','Etah']
histotitles = ['m_{thb} (GeV)','m_{th} (GeV)','m_{bh} (GeV)','m_{t} (GeV)','m_{h} (GeV)','top p_{T} (GeV)','b p_{T} (GeV)','Higgs p_{T} (GeV)','b #eta','top #eta','Higgs #eta']

#Kfac=1.2
arangel=[1000.0,0.0,0.0,110.0,0.0,350.,150.,150.,0.0,0.0,0.0]
arangeh=[6000.0,6000.,6000.,250.,400.,2000.,2000.,2000.,2.4,2.4,2.4]

rebins=[4,4,4,4,4,5,5,5,2,2,2,1,1]
sigfstringsBp = glob.glob("rootfiles/THBanalyzerweightedTHBWp2500*Bp*0__PSET_"+options.cuts+".root")
sigfstringsWp = glob.glob("rootfiles/THBanalyzerweightedTHBWp*Bp1500__PSET_"+options.cuts+".root")

sigf = [[
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp1500Tp1000__PSET_"+options.cuts+".root"),
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp1500Bp1000__PSET_"+options.cuts+".root")
],[
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp2000Tp1300__PSET_"+options.cuts+".root"),
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp2000Bp1300__PSET_"+options.cuts+".root")
],[
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp2500Tp1500__PSET_"+options.cuts+".root"),
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp2500Bp1500__PSET_"+options.cuts+".root")
],[
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp3000Tp1800__PSET_"+options.cuts+".root"),
ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp3000Bp1800__PSET_"+options.cuts+".root")
]]

masses = [['1500','1000'],['2000','1300'],['2500','1500'],['3000','1800']]

c2d = TCanvas('c2d', '', 700, 700)

c2d.SetLeftMargin(0.1)
c2d.SetRightMargin(0.15)
c2d.SetTopMargin(0.07)
c2d.SetBottomMargin(0.13)

#bkgparam = ['','mthb']
bkgparam = ['']

'''
confhisto = TH2F("confhisto","",3, -0.5, 1.5 ,3, -0.5, 1.5  )
ConfROOTBp = ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp2000Bp1300__PSET_default.root")


candidates = ["h","t","b"]
row=0
for cc in candidates:
	row+=1
	ConfROOThisto = ConfROOTBp.Get(cc+"match")
	ConfROOThisto.Scale(1./ConfROOThisto.Integral())
      	confhisto.GetYaxis().SetBinLabel(row,candidates[row-1]);
	for col in range(1,4):
		curcont = ConfROOThisto.GetBinContent(col)
		print col,row,curcont
		confhisto.SetBinContent(col,row,curcont)
      		confhisto.GetXaxis().SetBinLabel(col,candidates[col-1]);
confhisto.SetTitle(";tagged;matched")
confhisto.SetStats(0)
confhisto.SetContour(300);
confhisto.GetYaxis().SetTitleOffset(0.9)
confhisto.GetXaxis().SetTitleOffset(0.9)
confhisto.Draw('colztext0')
c2d.Update()
c2d.Print('plots/SigconfusionBp_PSET_'+options.cuts+'.root', 'root')
c2d.Print('plots/SigconfusionBp_PSET_'+options.cuts+'.pdf', 'pdf')
c2d.Print('plots/SigconfusionBp_PSET_'+options.cuts+'.png', 'png')










ConfROOTTp = ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp2000Tp1300__PSET_default.root")
candidates = ["h","t","b"]
row=0
for cc in candidates:
	row+=1
	ConfROOThisto = ConfROOTTp.Get(cc+"match")
	ConfROOThisto.Scale(1./ConfROOThisto.Integral())
      	confhisto.GetYaxis().SetBinLabel(row,candidates[row-1]);
	for col in range(1,4):
		curcont = ConfROOThisto.GetBinContent(col)
		print col,row,curcont
		confhisto.SetBinContent(col,row,curcont)
      		confhisto.GetXaxis().SetBinLabel(col,candidates[col-1]);
confhisto.SetTitle(";tagged;matched")
confhisto.SetStats(0)
confhisto.SetContour(300);
confhisto.GetYaxis().SetTitleOffset(0.9)
confhisto.GetXaxis().SetTitleOffset(0.9)
confhisto.Draw('colztext0')
c2d.Update()
c2d.Print('plots/SigconfusionTp_PSET_'+options.cuts+'.root', 'root')
c2d.Print('plots/SigconfusionTp_PSET_'+options.cuts+'.pdf', 'pdf')
c2d.Print('plots/SigconfusionTp_PSET_'+options.cuts+'.png', 'png')









ConfROOTBp3500 = ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp3500Bp2100__PSET_default.root")
ConfROOTTp3500 = ROOT.TFile("rootfiles/THBanalyzerweightedTHBWp3500Tp2100__PSET_default.root")





Bpthmatchedhisto = ConfROOTBp3500.Get('Mthmatched_h1t1b1')
Bpthunmatchedhisto = ConfROOTBp3500.Get('Mthunmatched_h1t1b1')

Tpthmatchedhisto = ConfROOTTp3500.Get('Mthmatched_h1t1b1')
Tpthunmatchedhisto = ConfROOTTp3500.Get('Mthunmatched_h1t1b1')


Bpbhmatchedhisto = ConfROOTBp3500.Get('Mbhmatched_h1t1b1')
Bpbhunmatchedhisto = ConfROOTBp3500.Get('Mbhunmatched_h1t1b1')

Tpbhmatchedhisto = ConfROOTTp3500.Get('Mbhmatched_h1t1b1')
Tpbhunmatchedhisto = ConfROOTTp3500.Get('Mbhunmatched_h1t1b1')





cmatchedTpth = TCanvas('cmatchedTpth', '', 700, 500)

Tpthmatchedhisto.Scale(1.0/Tpthmatchedhisto.Integral())
Tpthunmatchedhisto.Scale(1.0/Tpthunmatchedhisto.Integral())

Tpthmatchedhisto.SetLineColor(2)
Tpthunmatchedhisto.SetLineColor(3)

Tpthmatchedhisto.Draw('hist')
Tpthunmatchedhisto.Draw('histsame')

cmatchedTpth.Update()
cmatchedTpth.Print('plots/matchedTpth_PSET_'+options.cuts+'.root', 'root')
cmatchedTpth.Print('plots/matchedTpth_PSET_'+options.cuts+'.pdf', 'pdf')
cmatchedTpth.Print('plots/matchedTpth_PSET_'+options.cuts+'.png', 'png')








cmatchedBpbh = TCanvas('cmatchedBpbh', '', 700, 500)

Bpbhmatchedhisto.Scale(1.0/Bpbhmatchedhisto.Integral())
Bpbhunmatchedhisto.Scale(1.0/Bpbhunmatchedhisto.Integral())

Bpbhmatchedhisto.SetLineColor(2)
Bpbhunmatchedhisto.SetLineColor(3)

Bpbhmatchedhisto.Draw('hist')
Bpbhunmatchedhisto.Draw('histsame')

cmatchedBpbh.Update()
cmatchedBpbh.Print('plots/matchedBpbh_PSET_'+options.cuts+'.root', 'root')
cmatchedBpbh.Print('plots/matchedBpbh_PSET_'+options.cuts+'.pdf', 'pdf')
cmatchedBpbh.Print('plots/matchedBpbh_PSET_'+options.cuts+'.png', 'png')


'''


#THBanalyzerweightedttbar_PTRWoff__PSET_default.root
skipttbar=False
TTmc 	= ROOT.TFile("rootfiles/THBanalyzerweightedttbar"+rwstr+"__PSET_"+options.cuts+".root")
if options.set == 'data':
	setstring = '' 
	print "running on data"
	DataB11 = ROOT.TFile("rootfiles/THBanalyzerdata"+rwstr+"__PSET_"+options.cuts+".root")
	datapointcolor = 1	
elif options.set == 'QCD':
	setstring = 'QCD' 
	DataB11 = ROOT.TFile("rootfiles/THBanalyzerQCD_PSET_"+options.cuts+".root")
	datapointcolor = 4
elif options.set.find('QCDHT1000')!=-1:
	skipttbar=True
	setstring = options.set
	DataB11 = ROOT.TFile("rootfiles/THBanalyzer"+options.set+"_PSET_"+options.cuts+".root")
	datapointcolor = 4
elif options.set.find('QCDHT1500')!=-1:
	skipttbar=True
	setstring = options.set
	DataB11 = ROOT.TFile("rootfiles/THBanalyzer"+options.set+"_PSET_"+options.cuts+".root")
	datapointcolor = 4
elif options.set.find('QCDHT2000')!=-1:
	skipttbar=True
	setstring = options.set
	DataB11 = ROOT.TFile("rootfiles/THBanalyzer"+options.set+"_PSET_"+options.cuts+".root")
	datapointcolor = 4
else:
	print 'Error: Set selection invalid.'

datamass = DataB11.Get("Mugh"+"_"+options.histo)
cmugh = TCanvas('cmugh', '', 700, 700)
datamass.SetStats(0)
datamass.GetYaxis().SetTitleOffset(0.9)
datamass.GetXaxis().SetTitleOffset(0.9)
datamass.Rebin(4)
datamass.SetMinimum(0)
datamass.Draw()
cmugh.Update()
cmugh.Print('plots/cmugh_PSET_'+options.cuts+'.root', 'root')
cmugh.Print('plots/cmugh_PSET_'+options.cuts+'.pdf', 'pdf')
cmugh.Print('plots/cmugh_PSET_'+options.cuts+'.png', 'png')
saveeta = etatext
cols = [3,4,6,7]
for ih in range(0,len(histos)):
    for bkgstr in bkgparam:
	#badname#
	nomname = histos[ih]
	if histos[ih].find('DRAK')!=-1:
		nomname = histos[ih]+'_'
	leg = TLegend(0.6, 0.6, 0.84, 0.84)
	if histos[ih]=="Mthb":
		
		leg = TLegend(0.5, 0.4, 0.84, 0.84)
		bins=[900,1100]
		for ixabin in xrange(1,14):
			bins.append(bins[-1]+200)
		bins.append(bins[-1]+400)
		bins.append(6000)

		bins2=array('d',bins)
		print bins2
		#neta1r = neta1.Rebin(len(bins2)-1,"neta1r",bins2)

	leg.SetFillColor(0)
	leg.SetBorderSize(0)

	if bkgstr == 'mthb':
		etatext=''
	else:
		etatext=saveeta

	if options.set == 'data':
		print "sample is data"
		DataFS 	= DataB11.Get(nomname+"_"+options.histo) 			
		DataBE 	= DataB11.Get("bkg_"+histos[ih]+"_"+options.histo+bkgstr+etatext) 
		#DataBEUP 	= DataB11.Get("bkg_"+histos[ih]+"_"+options.histo+bkgstr+etatext+"up") 		
		#DataBEDOWN 	= DataB11.Get("bkg_"+histos[ih]+"_"+options.histo+bkgstr+etatext+"down") 		
	elif options.set.find('QCD')!=-1:
		print "sample is QCD"
		DataFS 	= DataB11.Get(nomname+"_"+options.histo) 			
		DataBE 	= DataB11.Get("bkg_"+histos[ih]+"_"+options.histo+bkgstr+etatext) 
		

		errDataFS = ROOT.Double()
		errDataBE = ROOT.Double()


		
		print DataFS.IntegralAndError(0, -1, errDataFS),errDataFS
		print DataBE.IntegralAndError(0, -1, errDataBE),errDataBE
	
		QCDcorr = DataFS.Integral()/DataBE.Integral()
		if histos[ih]=="Mthb":
			QCDcorrbinned = [] 
			corrf = ROOT.TFile( "THBcorr_"+options.set+extex+"__PSET_"+options.cuts+".root", "recreate" )
			corrf.cd()
		        QCDcorrhistN = copy.copy(DataFS)
		        QCDcorrhistD = copy.copy(DataBE)
			binsclos=array('d',[500,1300,2000,8000])
			QCDcorrhistN = QCDcorrhistN.Rebin(len(binsclos)-1,QCDcorrhistN.GetName()+"_R",binsclos)
			QCDcorrhistD = QCDcorrhistD.Rebin(len(binsclos)-1,QCDcorrhistD.GetName()+"_R",binsclos)
			
			QCDcorrhistN.Divide(QCDcorrhistD)
			#QCDcorrhistN.Fit("pol1")
			QCDcorrhistN.Write("QCDCorrFactor")
			corrf.Write()

			c1corr = TCanvas('c1corr' + str(ih), '', 700, 600)
			xg,yg = array('d'),array('d')
			for icontin in range(500,8000):
				xg.append(icontin)
				yg.append(QCDcorrhistN.Interpolate(icontin))
			TG = TGraph(len(xg),xg,yg)
			QCDcorrhistN.SetTitle(';'+histotitles[ih]+';QCD FS/BKG')
			QCDcorrhistN.GetYaxis().SetRangeUser(0,2)
			QCDcorrhistN.SetStats(0)
			c1corr.SetLeftMargin(0.16)
			QCDcorrhistN.Draw("hist")

			TG.SetLineWidth(2)
			TG.SetLineColor(3)
			TG.Draw('same')


			c1corr.Print('plots/QCDcorr'+histos[ih]+'vsBkg'+rwstr+'semilog_BifPoly_fit_'+extex+setstring+bkgstr+etatext+'PSET_'+options.cuts+'.root', 'root')
			c1corr.Print('plots/QCDcorr'+histos[ih]+'vsBkg'+rwstr+'semilog_BifPoly_fit_'+extex+setstring+bkgstr+etatext+'PSET_'+options.cuts+'.pdf', 'pdf')
			c1corr.Print('plots/QCDcorr'+histos[ih]+'vsBkg'+rwstr+'semilog_BifPoly_fit_'+extex+setstring+bkgstr+etatext+'PSET_'+options.cuts+'.png', 'png')
			suint =0
			for iiibin in xrange(DataBE.GetNbinsX()+1):
				suint+=DataBE.GetBinContent(iiibin)
				#print DataBE.GetBinCenter(iiibin),suint

			qb1 = DataFS.FindBin(1999.0)
			#print DataBE.Integral(0,qb1)
			QCDcorrbinned.append(DataFS.Integral(0,qb1)/DataBE.Integral(0,qb1))
			QCDcorrbinned.append(DataFS.Integral(qb1+1,-1)/DataBE.Integral(qb1+1,-1))
			print "QCDcorrbinned",QCDcorrbinned
			

		DataBEperr = errDataBE/DataBE.Integral()
		DataFSperr = errDataFS/DataFS.Integral()
		QCDcorrerror = QCDcorr*sqrt(DataBEperr*DataBEperr + DataFSperr*DataFSperr)



		skipttbar=True
		#DataBEUP 	= DataB11.Get("bkg_"+histos[ih]+"_"+options.histo+bkgstr+etatext+"up") 
		#DataBEDOWN 	= DataB11.Get("bkg_"+histos[ih]+"_"+options.histo+bkgstr+etatext+"down") 
		if not skipttbar:							
			DataFS.Add(TTmc.Get(nomname+"_"+options.histo)) 
 
	#ovrname = histos[ih]+"overlap"+"_"+(options.histo).replace("t1","t0")
	#print ovrname
	#DataOVR = DataB11.Get(ovrname) 			
	#print DataOVR.Integral()/DataFS.Integral()
	sigharray = []
	
	for sig in sigf:
		sigh = [
		sig[0].Get(nomname+"_"+options.histo),
		sig[1].Get(nomname+"_"+options.histo)
		]
		sigharray.append(copy.copy(sigh[0]))
		sigharray[-1].Add(sigh[1])
		if bkgstr == '':
			if histos[ih]=="Mthb":
				sigharray[-1] = sigharray[-1].Rebin(len(bins2)-1,sigharray[-1].GetName()+"_R",bins2)
			else:
				sigharray[-1].Rebin(rebins[ih])

		sigharray[-1].SetLineStyle(5)
		sigharray[-1].SetLineWidth(3)
		sigharray[-1].SetLineColor(cols[len(sigharray)-1])


	#sigh[1].Rebin(rebins[ih])
	#sigh[1].SetLineStyle(5)
	#sigh[1].SetLineWidth(3)
	#sigh[1].SetLineColor(4)

	st1= ROOT.THStack("st1" + str(ih), "st1" + str(ih))
	c1 = TCanvas('c1' + str(ih), '', 700, 600)
	main = ROOT.TPad("main" + str(ih), "main" + str(ih), 0, 0.3, 1, 1)
	sub = ROOT.TPad("sub" + str(ih), "sub" + str(ih), 0, 0, 1, 0.3)

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

	print histos[ih]
	output = ROOT.TFile( "THBanalyzer_output__PSET_"+options.cuts+".root", "recreate" )
	output.cd()

	TTmcFS = TTmc.Get(nomname+"_"+options.histo)
	print TTmc
	print "getting","bkg_"+histos[ih]+"_"+options.histo+bkgstr+etatext
	TTmcBE = TTmc.Get("bkg_"+histos[ih]+"_"+options.histo+bkgstr+etatext)
	if bkgstr == '':


		if histos[ih]=="Mthb":
			TTmcFS = TTmcFS.Rebin(len(bins2)-1,TTmcFS.GetName()+"_R",bins2)
			DataFS = DataFS.Rebin(len(bins2)-1,DataFS.GetName()+"_R",bins2)
		else:
			TTmcFS.Rebin(rebins[ih])
			DataFS.Rebin(rebins[ih])


	if histos[ih]=="Mthb":
		print "pRebin"
		print DataBE.Integral()
		print TTmcBE.Integral()
		TTmcBE = TTmcBE.Rebin(len(bins2)-1,TTmcBE.GetName()+"_R",bins2)
		DataBE = DataBE.Rebin(len(bins2)-1,DataBE.GetName()+"_R",bins2)
		print "poRebin"
		print DataBE.Integral()
		print TTmcBE.Integral()
	else:
		TTmcBE.Rebin(rebins[ih])
		DataBE.Rebin(rebins[ih])

	#DataBEUP.Rebin(rebins[ih])
	#DataBEDOWN.Rebin(rebins[ih])


	unsubbkg = DataBE.Clone()



	ttuncs = ['PU','Trig','Alp','B','Bmis','Q2','Hmistag','PDF','JERM','JECM','JER','JEC']
	ttuphistos = []
	ttdownhistos = []

	sigmattuphisto = copy.copy(DataBE)
	sigmattdownhisto = copy.copy(DataBE)
	upttf = []
	downttf = []
	if not skipttbar:							
		for ttunc in ttuncs:

			if (ttunc.find('JER')!=-1) or (ttunc.find('JEC')!=-1):

				histnameup = nomname+"_"+options.histo
				histnamedown = nomname+"_"+options.histo
				upttf.append(TFile('rootfiles/THBanalyzerweightedttbar_'+ttunc+'up_PSET_'+options.cuts+'.root'))
				downttf.append(TFile('rootfiles/THBanalyzerweightedttbar_'+ttunc+'down_PSET_'+options.cuts+'.root'))
				#print upttf[-1]
				#print downttf[-1]
			
				curtthistup =upttf[-1].Get(histnameup)
				curtthistdown =downttf[-1].Get(histnamedown)

		
			else:

				histnameup = nomname+ttunc+"up"+"_"+options.histo
				histnamedown = nomname+ttunc+"down"+"_"+options.histo

				#print histnameup
				#print histnamedown

				curtthistup =TTmc.Get(histnameup)
				curtthistdown =TTmc.Get(histnamedown)

			#print "totunc ",  100.0*(abs(curtthistup.Integral()-curtthistdown.Integral()))*(1.0/TTmcFS.Integral()),"%"
			#print curtthistup
			if bkgstr == '':
	

				if histos[ih]=="Mthb":
					curtthistup = curtthistup.Rebin(len(bins2)-1,curtthistup.GetName()+"_R",bins2)
					curtthistdown = curtthistdown.Rebin(len(bins2)-1,curtthistdown.GetName()+"_R",bins2)
				else:
					curtthistup.Rebin(rebins[ih])
					curtthistdown.Rebin(rebins[ih])






			#print curtthistup,ttunc
			#print "ttuncup",curtthistup.Integral()-TTmcFS.Integral()
			#print "ttuncdown",curtthistdown.Integral()-TTmcFS.Integral()
			ttuphistos.append(copy.copy(curtthistup))
			ttdownhistos.append(copy.copy(curtthistdown))
													
		for binx in range(0,TTmcFS.GetNbinsX()+1):
			downdelta = 0.0
			updelta = 0.0
			nomcont = TTmcFS.GetBinContent(binx)
			for nhist in range(0,len(ttuphistos)):
				deltaup = (ttuphistos[nhist].GetBinContent(binx)-nomcont)
				deltadown = (ttdownhistos[nhist].GetBinContent(binx)-nomcont)
				downdelta += min(deltaup,deltadown,0.0)*min(deltaup,deltadown,0.0)
				updelta += max(deltaup,deltadown,0.0)*max(deltaup,deltadown,0.0)
				#print ttuphistos[nhist]
				#print deltaup
				#print deltadown

			#ttsf
			updelta+=(0.1*nomcont)*(0.1*nomcont)
			downdelta+=(0.04*nomcont)*(0.04*nomcont)


			#lumi
			updelta+=(0.025*nomcont)*(0.025*nomcont)
			downdelta+=(0.025*nomcont)*(0.025*nomcont)

			#xsec
			updelta+=(0.055*nomcont)*(0.055*nomcont)
			downdelta+=(0.048*nomcont)*(0.048*nomcont)

			#stat 
			updelta+=(TTmcFS.GetBinErrorUp(binx))*(TTmcFS.GetBinErrorUp(binx))
			downdelta+=(TTmcFS.GetBinErrorLow(binx))*(TTmcFS.GetBinErrorLow(binx))

			sigmattuphisto.SetBinContent(binx,sqrt(updelta))
			sigmattdownhisto.SetBinContent(binx,sqrt(downdelta))
	print "updownint"
	print "ttbar unc up",sigmattuphisto.Integral()
	print "ttbar unc down",sigmattdownhisto.Integral()

	#sum because abs value
	tttotunc = 0.5*(sigmattuphisto.Integral()+sigmattdownhisto.Integral())

	bkguncs = ['','M','tt']
	if options.set=='data':
		bkguncs.append('clos')


	bkguphistos = []
	bkgdownhistos = []



	sigmabkguphisto = copy.copy(DataBE)
	sigmabkgdownhisto = copy.copy(DataBE)



	sigmatotuphisto = copy.copy(DataBE)
	sigmatotdownhisto = copy.copy(DataBE)


	for bkgunc in bkguncs:
		histnameup = "bkg_"+histos[ih]+"_"+options.histo+bkgstr+etatext+bkgunc+"up"
		histnamedown = "bkg_"+histos[ih]+"_"+options.histo+bkgstr+etatext+bkgunc+"down"
		print "unc",bkgunc,"str",bkgstr
		if bkgunc=='' and bkgstr=='':
			print "2d Projection"
			print histos[ih]

			hist2dnameup = "bkg_"+histos[ih]+"2d_"+options.histo+bkgstr+etatext+bkgunc+"up"
			hist2dnamedown = "bkg_"+histos[ih]+"2d_"+options.histo+bkgstr+etatext+bkgunc+"down"
			

			cur2dbkghistup =DataB11.Get(hist2dnameup)
			cur2dbkghistdown =DataB11.Get(hist2dnamedown)


			histupuncorrup = WPF.projectquadrature(cur2dbkghistup)
			histupuncorrdown = WPF.projectquadrature(cur2dbkghistdown)





			#histupuncorrup = cur2dbkghistup.ProjectionY()
			#histupuncorrdown = cur2dbkghistdown.ProjectionY()

			curbkghistup =  copy.copy(DataBE)
			curbkghistdown =  copy.copy(DataBE)



			if histos[ih]=="Mthb":
					histupuncorrup = histupuncorrup.Rebin(len(bins2)-1,histupuncorrup.GetName()+"_R",bins2)
					histupuncorrdown = histupuncorrdown.Rebin(len(bins2)-1,histupuncorrdown.GetName()+"_R",bins2)
			else:
					histupuncorrup.Rebin(rebins[ih])
					histupuncorrdown.Rebin(rebins[ih])



			curbkghistup.Add(histupuncorrup,1)
			curbkghistdown.Add(histupuncorrdown,-1)





		else:

			curbkghistup =DataB11.Get(histnameup)
			curbkghistdown =DataB11.Get(histnamedown)



			if histos[ih]=="Mthb":
					curbkghistup = curbkghistup.Rebin(len(bins2)-1,curbkghistup.GetName()+"_R",bins2)
					curbkghistdown = curbkghistdown.Rebin(len(bins2)-1,curbkghistdown.GetName()+"_R",bins2)
			else:
					curbkghistup.Rebin(rebins[ih])
					curbkghistdown.Rebin(rebins[ih])

			if bkgunc=='tt' and (not skipttbar):
				#template needs one extra tt subtract factor
				print "tt pre sub",curbkghistdown.Integral()
				curbkghistdown.Add(TTmcBE,-1)
				print "tt post sub",curbkghistdown.Integral()
				print "standard bkg",DataBE.Integral()
				 

		print
		print "current QCD background ",bkgunc
		print histnameup , curbkghistup.Integral()
		print DataBE , DataBE.Integral()
		print histnamedown  , curbkghistdown.Integral()
		print "perror",0.5*(curbkghistup.Integral()-curbkghistdown.Integral())/DataBE.Integral()

		bkguphistos.append(copy.copy(curbkghistup))
		bkgdownhistos.append(copy.copy(curbkghistdown))


        for binx in range(0,DataBE.GetNbinsX()+1):
		downdelta = 0.0
		updelta = 0.0
		nomcont =DataBE.GetBinContent(binx)
		for nhist in range(0,len(bkguphistos)):
			deltaup = (bkguphistos[nhist].GetBinContent(binx)-nomcont)
			deltadown = (bkgdownhistos[nhist].GetBinContent(binx)-nomcont)
			downdelta += min(deltaup,deltadown,0.0)*min(deltaup,deltadown,0.0)
			updelta += max(deltaup,deltadown,0.0)*max(deltaup,deltadown,0.0)
			
		updelta+=(DataBE.GetBinErrorUp(binx))*(DataBE.GetBinErrorUp(binx))
		downdelta+=(DataBE.GetBinErrorLow(binx))*(DataBE.GetBinErrorLow(binx))

		
		####NONCLOSURE
		#if options.set=='data':
		#	updelta+=(0.12*nomcont)*(0.12*nomcont)
		#	downdelta+=(0.12*nomcont)*(0.12*nomcont)
		####NONCLOSURE

		

		sigmabkguphisto.SetBinContent(binx,sqrt(updelta))
		sigmabkgdownhisto.SetBinContent(binx,sqrt(downdelta))



		if not skipttbar:							

			#print "bin centers ",binx
			#print sigmabkguphisto.GetBinCenter(binx)
			#print sigmabkgdownhisto.GetBinCenter(binx)
			#print sigmattuphisto.GetBinCenter(binx)
			#print sigmattdownhisto.GetBinCenter(binx)
			#print DataBE.GetBinCenter(binx)

			quadcontup = sigmabkguphisto.GetBinContent(binx)*sigmabkguphisto.GetBinContent(binx)    +     sigmattuphisto.GetBinContent(binx)*sigmattuphisto.GetBinContent(binx)
			quadcontdown = sigmabkgdownhisto.GetBinContent(binx)*sigmabkgdownhisto.GetBinContent(binx)    +     sigmattdownhisto.GetBinContent(binx)*sigmattdownhisto.GetBinContent(binx)


			sigmatotuphisto.SetBinContent(binx,sqrt(quadcontup))
			sigmatotdownhisto.SetBinContent(binx,sqrt(quadcontdown))
		else:

			sigmatotuphisto.SetBinContent(binx,sigmabkguphisto.GetBinContent(binx))
			sigmatotdownhisto.SetBinContent(binx,sigmabkgdownhisto.GetBinContent(binx))

	qcdtotunc = 0.5*(sigmabkguphisto.Integral()+sigmabkgdownhisto.Integral())

	if options.set=='data':
		print "ttbar contamination ",100.*(TTmcBE.Integral()/DataBE.Integral()),"%"
		print DataBE.Integral()
		print TTmcBE.Integral()
		DataBE.Add(TTmcBE,-1)

	print "total unc up",sigmatotuphisto.Integral()
	print "total unc down",sigmatotdownhisto.Integral()

	DataBEUP = copy.copy(DataBE)
	DataBEDOWN = copy.copy(DataBE)
	DataBEUP.Add(sigmatotuphisto)
	DataBEDOWN.Add(sigmatotdownhisto,-1)

	print "Total bkg uncertainty",100*(0.5*(DataBEUP.Integral()-DataBEDOWN.Integral())/DataBE.Integral()),"%"



	output.cd()


	DataBE.SetFillColor(kYellow)
	DataBEUP.SetLineColor(kBlue)
	DataBEDOWN.SetLineColor(kBlue)
	DataBEUP.SetLineStyle(2)
	DataBEDOWN.SetLineStyle(2)
	DataBEUP.SetLineWidth(2)
	DataBEDOWN.SetLineWidth(2)
	TTmcFS.SetFillColor(kRed)
	print "data",DataFS.Integral()
	print "QCD",DataBE.Integral()
	print "TTmcFS",TTmcFS.Integral()

	if histos[ih]=='Mt':
		st1.Add(DataBE)
		if not skipttbar:							
			st1.Add(TTmcFS)


		thetafile = ROOT.TFile( "Thetafile"+extex+rwstr+"__PSET_"+options.cuts+".root", "recreate" )

		TTmcFStowrite = copy.copy(TTmcFS)
		DataFStowrite = copy.copy(DataFS)
		DataBEtowrite = copy.copy(DataBE)

		TTmcFStowrite.GetXaxis().SetRangeUser(110,200)
		DataFStowrite.GetXaxis().SetRangeUser(110,200)
		DataBEtowrite.GetXaxis().SetRangeUser(110,200)

		TTmcFStowrite.SetName("mthb__ttbar")
		TTmcFStowrite.SetTitle("mthb__ttbar")
		TTmcFStowrite.Write("mthb__ttbar")


		DataFStowrite.SetName("mthb__DATA")
		DataFStowrite.SetTitle("mthb__DATA")
		DataFStowrite.Write("mthb__DATA")
		
		
		DataBEtowrite.SetName("mthb__QCD")
		DataBEtowrite.SetTitle("mthb__QCD")
		DataBEtowrite.Write("mthb__QCD")

		thetafile.Write()
		output.cd()
		#dcops = copy.copy(DataFS)
		#dcops.GetXaxis().SetRangeUser(130.,190.)
		#stack.GetXaxis().SetRangeUser(130.,190.)
		#print "TMASSCHI2",dcops.Chi2Test(stack,'UWCHI2/NDF')
	else:
		if not skipttbar:
			print "ttbar",TTmcFS.Integral(),"\\pm",tttotunc							
			st1.Add(TTmcFS)
		print "qcd",DataBE.Integral(),"\\pm",qcdtotunc						
		st1.Add(DataBE)

	if not skipttbar:							
		DataBEUP.Add(TTmcFS)
		DataBEDOWN.Add(TTmcFS)



	stack = st1.GetStack().Last()

	stack2forchi = copy.copy(stack)
	#for ibin in xrange(stack2forchi.GetNbinsX()+1):
	#	print stack2forchi.GetBinContent(ibin),stack2forchi.GetBinError(ibin)
	if histos[ih]=="Mthb":
		DataFSforchi = copy.copy(DataFS)

		DataFSforchi.GetXaxis().SetRangeUser(1200.,4000.)
		stack2forchi.GetXaxis().SetRangeUser(1200.,4000.)




	yvmin = array('d')
	yvmax = array('d')
	xv = array('d')

	totbins = DataBEUP.GetNbinsX()
	for xbin in range(0,totbins+1):
		xv.append(DataBEUP.GetBinLowEdge(xbin))	
		xv.append(DataBEUP.GetBinLowEdge(xbin)+DataBEUP.GetBinWidth(xbin))	

		yvmax.append(DataBEUP.GetBinContent(xbin))
		yvmax.append(DataBEUP.GetBinContent(xbin))
		yvmin.append(DataBEDOWN.GetBinContent(xbin))
		yvmin.append(DataBEDOWN.GetBinContent(xbin))



	totpoints = len(xv)
   	grshade = TGraph(2*totpoints);
	for xpoint in range(0,totpoints):
     		grshade.SetPoint(xpoint,xv[xpoint],yvmax[xpoint])
      		grshade.SetPoint(totpoints+xpoint,xv[totpoints-xpoint-1],yvmin[totpoints-xpoint-1])



	grmin = TGraph(len(xv),xv,yvmin)
	grmax = TGraph(len(xv),xv,yvmax)




	DataFS.SetLineColor(datapointcolor)
	DataFS.SetMarkerColor(datapointcolor)

	if options.set == 'QCD':
		leg.AddEntry( DataFS, 'QCD MC', 'P')
		leg.AddEntry( DataBE, 'QCD MC estimate', 'F')


	elif options.set == 'data':
		if plotdata:
			leg.AddEntry( DataFS, 'data', 'PE')
		leg.AddEntry( DataBE, 'QCD estimate', 'F')
	if not skipttbar:							
		leg.AddEntry( TTmcFS, 't#bar{t} MC', 'F')

	#leg.AddEntry( sigh[1], 'W`_{R} at 2000 GeV -> Bp at 1200 GeV', 'L')

	#c1.cd()
	#c1.SetLeftMargin(0.17)

	st1.SetMaximum(DataFS.GetMaximum() * 1.3)
	st1.SetMinimum(0.1)
	st1.SetTitle(';'+histotitles[ih]+';Events / bin')



	st1.Draw("hist")


	LS = .08

	st1.GetYaxis().SetTitleOffset(0.4)
	st1.GetXaxis().SetTitleOffset(0.9)
	    


	st1.GetYaxis().SetLabelSize(LS)
	st1.GetYaxis().SetTitleSize(LS)
	st1.GetYaxis().SetNdivisions(306)
	st1.GetXaxis().SetLabelSize(LS)
	st1.GetXaxis().SetTitleSize(LS)

	gPad.SetLeftMargin(.16)
	st1.GetYaxis().SetTitleOffset(0.9)
	#DataTOTALBEH.Draw("histsame")
	#DataTOTALBEL.Draw("histsame")
	if not skipttbar:							
		ish = 0
		for sighist in sigharray:
			leg.AddEntry( sighist, 'W`_{R} at '+masses[ish][0]+' GeV -> VLQ at '+masses[ish][1]+' GeV', 'L')
			sighist.Draw("samehist")
			ish +=1
	#DataBEUP.Draw("samehist")
	#DataBEDOWN.Draw("samehist")

	#grshade.SetFillStyle(3245)
	#grshade.SetFillColor(1)
	grshade.Draw("f")
	#grshade.SetFillStyle(3245)
   	grshade.SetFillStyle(3013);
   	grshade.SetFillColor(1);
	leg.AddEntry( grshade, '1#sigma background uncertainty', 'F')

	#grmin.Draw("l")
	#grmax.Draw("l")

	#sigh[1].Draw("samehist")



	#DataFS1	    = TH1D("DataFS1",     "mass W' in b+1",     	  	      140, 500, 4000 )


	#DataFS1.Rebin(rebins[ih])
	#for ibin in range(1,DataFS.GetNbinsX()+1):
	#	DataFS1.SetBinContent(ibin,DataFS.GetBinContent(ibin))

	#DataFS1.SetBinErrorOption(DataFS1.kPoisson)
	DataFS1 = DataFS
	if plotdata:
		DataFS1.Draw("samepE")

	leg.Draw()
	prelim = TLatex()
	prelim.SetNDC()


	#insertlogo( main, 2, 11 )


	#prelim.DrawLatex( 0.5, 0.91, "#scale[0.8]{CMS Preliminary, 13 TeV, 2553 pb^{-1}}" )
	#prelim.DrawLatex( 0.2, 0.83, "#scale[0.8]{"+text+"}" )
	CMS_lumi.CMS_lumi(main, 4, 11)
	#insertlogo( main, 4, 11 )
	st1.GetXaxis().SetRangeUser(arangel[ih],arangeh[ih])
	sub.cd()
	gPad.SetLeftMargin(.16)
	totalH = st1.GetStack().Last().Clone("totalH")
	#totalH.Add(TTmcFS)
	pull = WPF.Make_Pull_plot( DataFS1,totalH,DataBEUP,DataBEDOWN )

	if histos[ih]=="Mthb":
		chi2full = WPF.calcchi2( DataFS1,totalH,DataBEUP,DataBEDOWN )
		chi2stat = WPF.calcchi2stat( DataFSforchi,stack2forchi )
		print DataFSforchi.Chi2Test(stack2forchi,"UW P CHI2/NDF")
	
	#pull.GetXaxis().SetRangeUser(0,3000)
	pull.SetFillColor(kBlue)
	pull.SetTitle(';'+histotitles[ih]+';(Data-Bkg)/#sigma')
	pull.SetStats(0)


	pull.GetYaxis().SetRangeUser(-2.9,2.9)
	pull.GetXaxis().SetLabelSize(0.05)
	pull.GetYaxis().SetLabelSize(0.05)


	LS = .15

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
	else:
		pull.Draw("AXIS")
	pull.GetXaxis().SetRangeUser(arangel[ih],arangeh[ih])

	line2=ROOT.TLine(arangel[ih],0.0,arangeh[ih],0.0)
	line2.SetLineColor(0)
	line1=ROOT.TLine(arangel[ih],0.0,arangeh[ih],0.0)
	line1.SetLineStyle(2)

	line2.Draw()
	line1.Draw()
	gPad.Update()

	main.RedrawAxis()

	c1.Print('plots/'+histos[ih]+'vsBkg'+rwstr+'_BifPoly_fit_'+extex+setstring+bkgstr+etatext+'PSET_'+options.cuts+'.root', 'root')
	c1.Print('plots/'+histos[ih]+'vsBkg'+rwstr+'_BifPoly_fit_'+extex+setstring+bkgstr+etatext+'PSET_'+options.cuts+'.pdf', 'pdf')
	c1.Print('plots/'+histos[ih]+'vsBkg'+rwstr+'_BifPoly_fit_'+extex+setstring+bkgstr+etatext+'PSET_'+options.cuts+'.png', 'png')
	main.SetLogy()
	st1.SetMaximum( DataFS.GetMaximum() * 6000 )
	st1.SetMinimum( 0.1)
	main.RedrawAxis()

	c1.Print('plots/'+histos[ih]+'vsBkg'+rwstr+'semilog_BifPoly_fit_'+extex+setstring+bkgstr+etatext+'PSET_'+options.cuts+'.root', 'root')
	c1.Print('plots/'+histos[ih]+'vsBkg'+rwstr+'semilog_BifPoly_fit_'+extex+setstring+bkgstr+etatext+'PSET_'+options.cuts+'.pdf', 'pdf')
	c1.Print('plots/'+histos[ih]+'vsBkg'+rwstr+'semilog_BifPoly_fit_'+extex+setstring+bkgstr+etatext+'PSET_'+options.cuts+'.png', 'png')
	if options.set=="QCD":
		DataBEsysterror = abs(DataBEUP.Integral()-DataBE.Integral())/DataBE.Integral()
		#print "QCDCORR",QCDcorr,"+/-",QCDcorrerror,"+/-",DataBEsysterror
		QCDcorrerrorfull = QCDcorr*sqrt(DataBEperr*DataBEperr + DataBEsysterror*DataBEsysterror + DataFSperr*DataFSperr)
		#print "QCDCORR",QCDcorr,"+/-",QCDcorrerrorfull," -- full error"
		#print QCDcorrbinned
###Should be moved


c2 = TCanvas('c2', '', 700, 600)

c2.SetLeftMargin(0.16)
c2.SetRightMargin(0.05)
c2.SetTopMargin(0.11)
c2.SetBottomMargin(0.32)


sighists = []
sigfiles = []
ibp = 0
for sbp in sigfstringsBp:
	print sbp
	sigfiles.append(ROOT.TFile(sbp))
	sighists.append(sigfiles[-1].Get("Mbh_h1t1b1"))
	sighists[-1].SetLineColor(ibp+1)
	sighists[-1].Scale(1.0/sighists[-1].Integral())
	if len(sighists)>1:
		sighists[-1].Draw("samehist")
	else:
		sighists[-1].SetTitle(";Mbh;Fraction")
		sighists[-1].Draw("hist")
	ibp+=1
c2.Print('plots/Sigcomp_Bprime'+rwstr+'_PSET_'+options.cuts+'.root', 'root')
c2.Print('plots/Sigcomp_Bprime'+rwstr+'_PSET_'+options.cuts+'.pdf', 'pdf')
c2.Print('plots/Sigcomp_Bprime'+rwstr+'_PSET_'+options.cuts+'.png', 'png')




sighists = []
sigfiles = []
iwp = 0
for swp in sigfstringsWp:
	print swp

	sigfiles.append(ROOT.TFile(swp))
	sighists.append(sigfiles[-1].Get("Mthb_h1t1b1"))
	sighists[-1].SetLineColor(iwp+1)
	sighists[-1].Scale(1.0/sighists[-1].Integral())
	if len(sighists)>1:

		sighists[-1].Draw("samehist")
	else:
		sighists[-1].SetTitle(";Mthb;Fraction")
		sighists[-1].Draw("hist")
	iwp+=1
c2.Print('plots/Sigcomp_Wprime'+rwstr+'_PSET_'+options.cuts+'.root', 'root')
c2.Print('plots/Sigcomp_Wprime'+rwstr+'_PSET_'+options.cuts+'.pdf', 'pdf')
c2.Print('plots/Sigcomp_Wprime'+rwstr+'_PSET_'+options.cuts+'.png', 'png')



