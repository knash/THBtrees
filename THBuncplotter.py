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



fileloc = "limitsetting/theta/TEST"+chanstr+options.cuts+"center.root"

Limitsettington = ROOT.TFile( fileloc)
print fileloc
D1 = Limitsettington.GetListOfKeys()
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



		nomhist = Limitsettington.Get(curnamenom)
		plushist = Limitsettington.Get(curname)
		minushist = Limitsettington.Get(curnamedown)

		print curnamenom
		print curname
		print curnamedown

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



		c1.Print('plots/uncplot_'+curnamenomarr[1]+curnamenomarr[2]+'.root', 'root')
		c1.Print('plots/uncplot_'+curnamenomarr[1]+curnamenomarr[2]+'.pdf', 'pdf')
		c1.Print('plots/uncplot_'+curnamenomarr[1]+curnamenomarr[2]+'.png', 'png')












