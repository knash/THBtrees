# -*- coding: utf-8 -*-
import scipy.interpolate
import ROOT
from ROOT import *
def histogram_filter(hname):
    #if 'ttag' in hname: return False
    if 'WEx' in hname: return False
    
    return True



def makenuisanceplot(parlist,parVal,tstr=''):
   c1 = TCanvas('c1', 'NP', 1200, 700)
   c1.Divide(1,2)
   NPplot = ROOT.TH1F("NPplot",     "nuisanceplot",     	  	len(parVal.keys()), -0.5, len(parVal.keys())+0.5 )
   S95low  = TLine(-0.5,-2,len(parVal.keys())+0.5,-2)
   S95high = TLine(-0.5,2,len(parVal.keys())+0.5,2)
   zero = TLine(-0.5,0,len(parVal.keys())+0.5,0)
   zeroblank = TLine(-0.5,0,len(parVal.keys())+0.5,0)
   S68low = TLine(-0.5,-1,len(parVal.keys())+0.5,-1)
   S68high = TLine(-0.5,1,len(parVal.keys())+0.5,1)
   Pull = ROOT.TH1F("Pull",     "pullplot",     	  	len(parVal.keys()), -0.5, len(parVal.keys())+0.5 )
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
   		for p in nuisances:
			print p
			if p==nu:
				if n=='up':
   					parameter_values[p] = parVal[p][0][0]+parVal[p][0][1]
				if n=='down':
   					parameter_values[p] = parVal[p][0][0]-parVal[p][0][1]
			else:
   				parameter_values[p] = parVal[p][0][0]
		print parameter_values
   		histos = evaluate_prediction(model, parameter_values,include_signal=False)
   		write_histograms_to_rootfile(histos, 'plots/histos-mle'+nu+n+tstr+'.root')
   for par in nuisances:
	print par 
	i+=1
	NPplot.GetXaxis().SetBinLabel(i, par)
	print "setting",i,parVal[par][0][0],"pm",parVal[par][0][1]
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
   c1.Print('plots/nuisance'+tstr+'.root', 'root')
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

    return model

def limits_allhad(model, step = 0):
   fnamestr = "RFILE"
   #exp,obs = bayesian_limits(model,what='expected',input_expected='toys:0')
   exp,obs = bayesian_limits(model, 'all', n_toy = 2000, n_data = 20)
   #exp,obs = asymptotic_cls_limits(model,use_data=False)
   #print exp
   exp.write_txt('unblindedttsfnom_exp'+fnamestr.replace('.root','')+'.txt')
   obs.write_txt('unblindedttsfnom_obs'+fnamestr.replace('.root','')+'.txt')


   signal_process_groups1 = {'': []}
   myopts = Options()
   myopts.set('minimizer', 'strategy', 'robust')
   parVals = mle(model, input = 'data', n = 1,signal_process_groups=signal_process_groups1)
   print parVals
   for pv in parVals:
	print pv
	for pv1 in parVals[pv]:
		print pv1
		print parVals[pv][pv1]
   parlist = ['__nll','beta_signal']
   canvnuisanceplot = makenuisanceplot(parlist,parVals[''],"bkgttsfnom_data")


model = build_allhad_model()


for p in model.distribution.get_parameters():
    print "dists",p
    d = model.distribution.get_distribution(p)
    print d
    #if d['typ'] == 'gauss' and d['mean'] == 0.0 and d['width'] == 1.0:
        #model.distribution.set_distribution_parameters(p, range = [-5.0, 5.0])
model_summary(model, True, True, True)

limits_allhad(model,0)

