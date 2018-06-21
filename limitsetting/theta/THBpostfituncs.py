import os
import array
import glob
import math
import ROOT
import copy
import sys
#from ROOT import *
from array import *
from optparse import OptionParser
import WprimetoVlq_Functions
from WprimetoVlq_Functions import *

parser = OptionParser()

parser.add_option('-c', '--cuts', metavar='F', type='string', action='store',
                  default	=	'default',
                  dest		=	'cuts',
                  help		=	'Cuts type (ie default, rate, etc)')

parser.add_option('--batch', metavar='F', action='store_true',
                  default=False,
                  dest='batch',
                  help='batch')

(options, args) = parser.parse_args()

chans = ['h1t1b1']
chanstr = ''
for ch in chans:
	chanstr+='_'+ch
print chanstr

if options.batch:
	ROOT.gROOT.SetBatch(True)
	ROOT.PyConfig.IgnoreCommandLineOptions = True



fileloc = "TEST"+chanstr+options.cuts+"center.root"

Limitsettington = ROOT.TFile( fileloc)
print fileloc
D1 = Limitsettington.GetListOfKeys()

uncdictPF = {}
uncdict = {}
for i in range(0,len(D1)):
	a = D1[i].ReadObj()
	curname = a.GetName()

	if curname.find('plus') != -1:


		c1 = TCanvas('c1', '', 700, 600)
			
		main = ROOT.TPad("main" + curname, "main" + curname, 0, 0.3, 1, 1)
		sub = ROOT.TPad("sub" + curname, "sub" + curname, 0, 0, 1, 0.3)

	
		main.SetLeftMargin(0.16)
		main.SetRightMargin(0.05)
		main.SetTopMargin(0.11)
		main.SetBottomMargin(0.)


		sub.SetLeftMargin(0.16)
		sub.SetRightMargin(0.05)
		sub.SetTopMargin(0.)
		sub.SetBottomMargin(0.3)


		main.Draw()
		sub.Draw()

		main.cd()


		curnamedown = curname.replace('plus','minus')
		curnamenomarr = curname.split('__')
		curnamenom = curnamenomarr[0]+'__'+curnamenomarr[1]
		if curnamenom.find("mthb_h1t1b1__wp")!=-1:
			continue 
		if curnamenomarr[2]=="WEx":
			continue 
		nomhist = Limitsettington.Get(curnamenom)
		plushist = Limitsettington.Get(curname)
		minushist = Limitsettington.Get(curnamedown)
		print curnamenom
		print curnamenomarr[2]
		print "histos-mle/histos-mle_withsig"+fileloc.replace('.root','')+curnamenomarr[2]+"up.root"
		pfup = ROOT.TFile( "histos-mle/histos-mle_bkgonly"+fileloc.replace('.root','')+curnamenomarr[2]+"up.root")
		pfdown = ROOT.TFile( "histos-mle/histos-mle_bkgonly"+fileloc.replace('.root','')+curnamenomarr[2]+"down.root")
		pfnom = ROOT.TFile( "histos-mle/histos-mle_bkgonlyTEST_h1t1b1defaultcenterallnominal.root")
		histpfup = pfup.Get(curnamenom)
		histpfdown = pfdown.Get(curnamenom)
		histpfnom = pfnom.Get(curnamenom)

		histpfuprebin = copy.copy(nomhist)
		histpfdownrebin = copy.copy(nomhist)
		histpfnomrebin = copy.copy(nomhist)
		for xbin in xrange(nomhist.GetNbinsX()+1):
			histpfuprebin.SetBinContent(xbin,histpfup.GetBinContent(xbin))
			histpfdownrebin.SetBinContent(xbin,histpfdown.GetBinContent(xbin))
			histpfnomrebin.SetBinContent(xbin,histpfnom.GetBinContent(xbin))
		print curnamenom
		print curname
		print curnamedown
		unccur  =  0.5*abs(plushist.Integral()-minushist.Integral())
		pfunccur  =  0.5*abs(histpfuprebin.Integral()-histpfdownrebin.Integral())
		try:
			uncdict[curnamenom]+=unccur*unccur
			uncdictPF[curnamenom]+=pfunccur*pfunccur
		except:
			uncdict[curnamenom]=unccur*unccur
			uncdictPF[curnamenom]=pfunccur*pfunccur

		print "unc = ",0.5*abs((plushist.Integral()-minushist.Integral())/(nomhist.Integral()))
		print "up = ",(plushist.Integral()/nomhist.Integral())
		print "down = ",(minushist.Integral()/nomhist.Integral())

		plotmax = 1.4*max([plushist.GetMaximum(),minushist.GetMaximum()])
		

		leg = TLegend(0.55, 0.65, 0.84, 0.84)
		leg.SetFillColor(0)
		leg.SetBorderSize(0)

		nomhist.SetTitle(";;Events")

		nomhist.SetLineColor(1)
		plushist.SetLineColor(2)
		minushist.SetLineColor(3)

		leg.AddEntry( nomhist, 'nominal', 'l')
		leg.AddEntry( plushist, curnamenomarr[2]+' up', 'l')
		leg.AddEntry( minushist, curnamenomarr[2]+' down', 'l')

		nomhist.SetMaximum(plotmax)
		nomhist.SetStats(0)
		nomhist.Draw("hist")
		plushist.Draw("samehist")
		minushist.Draw("samehist")

		histpfuprebin.SetLineColor(2)
		histpfdownrebin.SetLineColor(3)
		histpfnomrebin.SetLineColor(1)

		histpfuprebin.SetLineStyle(2)
		histpfdownrebin.SetLineStyle(2)
		histpfnomrebin.SetLineStyle(2)


		histpfuprebin.Draw("samehist")
		histpfdownrebin.Draw("samehist")
		histpfnomrebin.Draw("samehist")
			
		leg.Draw()
		sub.cd()
		plusdevplot = copy.copy(plushist)
		minusdevplot = copy.copy(minushist)

		plusdevplot.Add(nomhist,-1)
		minusdevplot.Add(nomhist,-1)
		plusdevplot.Divide(nomhist)
		minusdevplot.Divide(nomhist)

		plusdevplot.GetYaxis().SetRangeUser(-1.0,1.0)
		plusdevplot.SetTitle(";M_{thb} GeV;#sigma/nominal")

		LS = .13




		plusdevplot.GetYaxis().SetTitleOffset(0.4)
		plusdevplot.GetXaxis().SetTitleOffset(0.9)
		plusdevplot.SetStats(0)
	    


		plusdevplot.GetYaxis().SetLabelSize(LS)
		plusdevplot.GetYaxis().SetTitleSize(LS)
		plusdevplot.GetYaxis().SetNdivisions(306)
		plusdevplot.GetXaxis().SetLabelSize(LS)
		plusdevplot.GetXaxis().SetTitleSize(LS)


		plusdevplot.Draw('hist')
		minusdevplot.Draw('samehist')
	
		line2=ROOT.TLine(500.,0.0,8000.,0.0)
		line2.SetLineColor(0)
		line1=ROOT.TLine(500.,0.0,8000.,0.0)
		line1.SetLineStyle(2)

		line2.Draw()
		line1.Draw()
		gPad.Update()
		print "uncdicts"
		print sqrt(uncdict[curnamenom])
		print sqrt(uncdictPF[curnamenom])
		print sqrt(uncdictPF[curnamenom])/sqrt(uncdict[curnamenom])
		c1.Print('plots/uncPFplot_'+curnamenomarr[1]+curnamenomarr[2]+'.root', 'root')
		c1.Print('plots/uncPFplot_'+curnamenomarr[1]+curnamenomarr[2]+'.pdf', 'pdf')
		c1.Print('plots/uncPFplot_'+curnamenomarr[1]+curnamenomarr[2]+'.png', 'png')


allpfnom = ROOT.TFile( "histos-mle/histos-mle_withsigTEST_h1t1b1defaultcenterallnominal.root")
allpfup = ROOT.TFile( "histos-mle/histos-mle_withsigTEST_h1t1b1defaultcenterallup.root")
allpfdown = ROOT.TFile( "histos-mle/histos-mle_withsigTEST_h1t1b1defaultcenteralldown.root")
for cunc in uncdict:
	print cunc
	print "Uncorr"
	print sqrt(uncdict[cunc])
	print sqrt(uncdictPF[cunc])
	print sqrt(uncdictPF[cunc])/sqrt(uncdict[cunc])
	print "Fullcorr"
	print allpfnom.Get(cunc).Integral()
	print allpfup.Get(cunc).Integral()
	print allpfdown.Get(cunc).Integral()
	histup = allpfup.Get(cunc)
	histdown = allpfdown.Get(cunc)
	print 0.5*abs(histup.Integral()-histdown.Integral())
	print 0.5*abs(histup.Integral()-histdown.Integral())/sqrt(uncdict[cunc])



