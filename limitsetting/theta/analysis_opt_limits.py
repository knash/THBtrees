# -*- coding: utf-8 -*-
import scipy.interpolate
import ROOT
from ROOT import *
def histogram_filter(hname):
    #if 'ttag' in hname: return False
    if 'WEx' in hname: return False
    
    return True


def makenuisanceplot(parlist,parVal):
   c1 = TCanvas('c1', 'NP', 1200, 700)
   c1.Divide(1,2)
   NPplot = ROOT.TH1F("NPplot",     "nuisanceplot",     	  	len(parVal.keys())-2, -0.5, len(parVal.keys())-1.5 )
   S95low  = TLine(-0.5,-2,len(parVal.keys())-1.5,-2)
   S95high = TLine(-0.5,2,len(parVal.keys())-1.5,2)
   zero = TLine(-0.5,0,len(parVal.keys())-1.5,0)
   zeroblank = TLine(-0.5,0,len(parVal.keys())-1.5,0)
   S68low = TLine(-0.5,-1,len(parVal.keys())-1.5,-1)
   S68high = TLine(-0.5,1,len(parVal.keys())-1.5,1)
   Pull = ROOT.TH1F("Pull",     "pullplot",     	  	len(parVal.keys())-2, -0.5, len(parVal.keys())-1.5 )
   i=0
   nuisances = []
   for par in parVal.keys():
	if par in parlist:
		continue
	nuisances.append(par)
   #nuisances = ['','pile','pdf','modm','modtb','jer','q2','lumi','st_TW_xsec','ttbar_xsec','Fit','btag','pdf','Alt','lumi','trig','jes','ttag','AK8btag']
   #procs = [['ttbar','st','qcd'],['ttbar'],['ttbar'],['qcd'],['qcd'],['ttbar'],['ttbar'],['st'],['ttbar'],['qcd'],['ttbar'],['ttbar'],['qcd'],['ttbar','st'],['ttbar'],['ttbar'],['ttbar','st'],['ttbar']]
   hrange = (100, -3.0, 3.0)
   histogram_specs = {}
   
   for nu in nuisances:

	if nu=='':
		nudev=['']

	else:
		nudev=['up','down']

	for n in nudev:		
		parameter_values = {}
   		for p in model.get_parameters(['wp2000']):
			if p==nu:
				if n=='up':
   					parameter_values[p] = parVal[p][0][0]+parVal[p][0][1]
				if n=='down':
   					parameter_values[p] = parVal[p][0][0]-parVal[p][0][1]
			else:
   				parameter_values[p] = parVal[p][0][0]
   		histos = evaluate_prediction(model, parameter_values)
   		write_histograms_to_rootfile(histos, 'plots/histos-mle'+nu+n+'.root')
   for par in nuisances:
	print par 
	i+=1
	NPplot.GetXaxis().SetBinLabel(i, par)
	print parVal[par][0][0]
	print parVal[par][0][1]
	NPplot.SetBinContent(i, parVal[par][0][0])
	NPplot.SetBinError(i, parVal[par][0][1])
        Pull.GetXaxis().SetBinLabel(i, par)
        Pull.SetBinContent(i, parVal[par][0][0]/abs(parVal[par][0][1]))


	Pull.SetTitle(';Nuisance Parameter;Pull')
	Pull.SetStats(0)
	Pull.SetLineColor(1)


	NPplot.SetTitle(';Nuisance Parameter;\sigma')
	NPplot.SetStats(0)
	NPplot.SetLineColor(1)
	NPplot.SetMarkerStyle(21)

	LS=.10
	LS1 = 0.09
	NPplot.GetXaxis().SetTitleOffset(1.2)
	NPplot.GetXaxis().SetLabelSize(LS)
	NPplot.GetXaxis().SetTitleSize(LS1)

	S95low.SetLineWidth(4)
	S95high.SetLineWidth(4)
	S68low.SetLineWidth(4)
	S68high.SetLineWidth(4)
	S95low.SetLineColor(5)
	S95high.SetLineColor(5)
	S68low.SetLineColor(3)
	S68high.SetLineColor(3)
	zeroblank.SetLineColor(0)
	zero.SetLineColor(1)
	zero.SetLineStyle(2)
	zero.SetLineWidth(1)
	NPplot.GetXaxis().SetTickLength(0.0)

	NPplot.GetYaxis().SetRangeUser(-4,4)
	NPplot.GetYaxis().SetTitleOffset(0.4)

	Pull.GetXaxis().SetTickLength(0.0)

	Pull.GetYaxis().SetRangeUser(-1,1)
	Pull.GetYaxis().SetTitleOffset(0.4)


	c1.cd(1)
	gPad.SetLeftMargin(0.06)
	gPad.SetRightMargin(0.08)
	gPad.SetBottomMargin(0.31)
	NPplot.Draw()
	S95low.Draw()
	S95high.Draw()
	S68low.Draw()
	S68high.Draw()
	zero.Draw()
	NPplot.Draw("same")
        prelim = ROOT.TLatex()
        prelim.SetTextFont(42)
        prelim.SetNDC()
	prelim.DrawLatex( 0.15, 0.91, "#scale[1.0]{CMS Preliminary #sqrt{s} = 13 TeV}" )
	gPad.RedrawAxis()
	c1.cd(2)
	Pull.GetXaxis().SetTitleOffset(1.1)
	Pull.GetXaxis().SetLabelSize(LS)
	Pull.GetXaxis().SetTitleSize(LS1)
	gPad.SetLeftMargin(0.06)
	gPad.SetRightMargin(0.08)
	gPad.SetBottomMargin(0.3)
	Pull.SetFillColor(4)
	Pull.Draw('hist')
	zeroblank.Draw()
	zero.Draw()
	histogram_specs[par] = hrange
   c1.Update()

   c1.Print('plots/nuisance2000.root', 'root')
   c1.Print('plots/nuisance2000.pdf', 'pdf')

   return c1

def build_allhad_model():
    files = ["RFILE"]
    model = build_model_from_rootfile(files, histogram_filter,  include_mc_uncertainties=True)
    model.fill_histogram_zerobins()
    model.set_signal_processes('wp*')


    for p in model.processes:
	print p
       	if p=='qcd': 
       		model.add_lognormal_uncertainty('nonclosure', math.log(1.12), p)
		continue
       	model.add_lognormal_uncertainty('lumi', math.log(1.025), p)
    	model.add_asymmetric_lognormal_uncertainty('topsf',math.log(1.04),math.log(1.1), p)
       	if p=='ttbar':
    		model.add_asymmetric_lognormal_uncertainty('ttbar_xsec',math.log(1.048),math.log(1.055), p)
       		model.add_lognormal_uncertainty('ttbar_guess', math.log(1.15), p)
	else:
       		model.add_lognormal_uncertainty('sig_guess', math.log(1.15), p)
    return model

def limits_allhad(model, step = 0):
   fnamestr = "RFILE"
   exp,obs = bayesian_limits(model,what='expected',input_expected='toys:0', n_toy = 1200)
   #exp,obs = asymptotic_cls_limits(model,use_data=False)
   print exp
   exp.write_txt('OPT_exp'+fnamestr.replace('.root','')+'.txt')
   
   print "running discovery"
   discvector = {}
   for masses in ['1500','2500','3500']:
   	discvector['wp'+masses] = discovery(model, spid = 'wp'+masses, use_data = False, maxit = 20)
   print discvector

   text_file = open('discvector'+fnamestr.replace('.root','')+'.txt', "w") 
   for key in sorted(discvector):
  	 text_file.write(key + " "+str(discvector[key])+"\n")

   
model = build_allhad_model()


for p in model.distribution.get_parameters():
    d = model.distribution.get_distribution(p)
    if d['typ'] == 'gauss' and d['mean'] == 0.0 and d['width'] == 1.0:
        model.distribution.set_distribution_parameters(p, range = [-5.0, 5.0])
model_summary(model, True, True, True)

limits_allhad(model,0)

