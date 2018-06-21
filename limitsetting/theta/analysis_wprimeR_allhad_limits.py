# -*- coding: utf-8 -*-
import scipy.interpolate
import ROOT
from ROOT import *
def histogram_filter(hname):
    if 'ttag' in hname: return False
    if 'TwoD' in hname: return False
    return True
 
def build_allhad_model():
    files = ['Limits_allhadronic_right_PSET_default.root']
    #files = ['allhadronic_mttbar.root']
    model = build_model_from_rootfile(files, histogram_filter,  include_mc_uncertainties=True)
    model.fill_histogram_zerobins()
    model.set_signal_processes('wp*')
    for p in model.processes:
       	if p=='qcd': continue
       	if p=='ttbar':
       		#model.add_lognormal_uncertainty('ttbar_xsec', math.log(1.058), p)
    		model.add_asymmetric_lognormal_uncertainty('ttbar_xsec',math.log(1.055),math.log(1.048), p)
       	if p=='st': 
       		model.add_lognormal_uncertainty('st_TW_xsec', math.log(1.054), p)
      # 	model.add_lognormal_uncertainty('topsf', math.log(1.15), p)
       	model.add_lognormal_uncertainty('lumi', math.log(1.027), p)
       	model.add_lognormal_uncertainty('ttag', math.log(1.23), p)
       	model.add_lognormal_uncertainty('AK8btag', math.log(1.03), p)
    return model

def limits_allhad(model, step = 0):
   if step==0:

       runs = bayesian_quantiles(model,'toys:0',2000, run_theta=False)
       print runs
       for point in runs:
		runs[point].get_configfile(Options())
       return
   expected_limits = bayesian_quantiles(model, 'toys:0', 2000, run_theta=True)
   plot_expected = limit_band_plot(expected_limits, True)
   observed_limits = bayesian_quantiles(model, 'data', 10)
   plot_observed = limit_band_plot(observed_limits, False)
   report_limit_band_plot(plot_expected, plot_observed, 'Bayesian', 'bayesian')

   plot_expected.write_txt('bayesian_expected_allhad_limits_WprimeR.txt')
   plot_observed.write_txt('bayesian_observed_allhad_limits_WprimeR.txt')
   
   myopts = Options()
   myopts.set('minimizer', 'strategy', 'robust')
   myopts.set('minimizer', 'minuit_tolerance_factor', '100000')
   hrange = (100, -3.0, 3.0)
   histogram_specs = {}

   parVals = mle(model, input = 'data', n=1, with_error=True, with_covariance=False,options = myopts)


   #parVals = mle(model, input='data', n=1, options = options)



   parlist = ['__nll','beta_signal']
   c1 = TCanvas('c1', 'NP', 1200, 700)
   c1.Divide(1,2)
   NPplot = ROOT.TH1F("NPplot",     "nuisanceplot",     	  	len(parVals['wp1800'].keys())-2, -0.5, len(parVals['wp1800'].keys())-1.5 )
   S95low  = TLine(-0.5,-2,len(parVals['wp1800'].keys())-1.5,-2)
   S95high = TLine(-0.5,2,len(parVals['wp1800'].keys())-1.5,2)
   zero = TLine(-0.5,0,len(parVals['wp1800'].keys())-1.5,0)
   zeroblank = TLine(-0.5,0,len(parVals['wp1800'].keys())-1.5,0)
   S68low = TLine(-0.5,-1,len(parVals['wp1800'].keys())-1.5,-1)
   S68high = TLine(-0.5,1,len(parVals['wp1800'].keys())-1.5,1)
   Pull = ROOT.TH1F("Pull",     "pullplot",     	  	len(parVals['wp1800'].keys())-2, -0.5, len(parVals['wp1800'].keys())-1.5 )
   i=0

   print parVals

   nuisances = ['','pile','pdf','modm','modtb','jer','q2','lumi','st_TW_xsec','ttbar_xsec','Fit','btag','pdf','Alt','lumi','trig','jes','ttag','AK8btag']
   procs = [['ttbar','st','qcd'],['ttbar'],['ttbar'],['qcd'],['qcd'],['ttbar'],['ttbar'],['st'],['ttbar'],['qcd'],['ttbar'],['ttbar'],['qcd'],['ttbar','st'],['ttbar'],['ttbar'],['ttbar','st'],['ttbar']]

   for nu in nuisances:

	if nu=='':
		nudev=['']

	else:
		nudev=['up','down']
	for n in nudev:		
		parameter_values = {}
   		for p in model.get_parameters(['wp1800']):
			if p==nu:
				if n=='up':
   					parameter_values[p] = parVals['wp1800'][p][0][0]+parVals['wp1800'][p][0][1]
				if n=='down':
   					parameter_values[p] = parVals['wp1800'][p][0][0]-parVals['wp1800'][p][0][1]
			else:
   				parameter_values[p] = parVals['wp1800'][p][0][0]
   		histos = evaluate_prediction(model, parameter_values)
   		write_histograms_to_rootfile(histos, 'histos-mle'+nu+n+'.root')

   for par in parVals['wp1800'].keys():
	if par in parlist:
		continue 
	print par 
	i+=1
	NPplot.GetXaxis().SetBinLabel(i, par)
	NPplot.SetBinContent(i, parVals['wp1800'][par][0][0])
	NPplot.SetBinError(i, parVals['wp1800'][par][0][1])
        Pull.GetXaxis().SetBinLabel(i, par)
        Pull.SetBinContent(i, parVals['wp1800'][par][0][0]/abs(parVals['wp1800'][par][0][1]))


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
   c1.Print('nuisance1800.root', 'root')
   c1.Print('nuisance1800.pdf', 'pdf')


   print model.signal_process_groups 
   histograms1 = bayesian_posteriors(model, input = 'data', n=1, histogram_specs = histogram_specs,signal_process_groups={'wp1800':['wp1800']})
   write_histograms_to_rootfile(histograms1, 'histos_posteriors.root')
   histograms2 = bayesian_posterior_model_prediction(model, input = 'data', n=1,signal_process_groups={'wp1800':['wp1800']})
   write_histograms_to_rootfile(histograms2, 'histos_posterior_model_prediction.root')
   posteriors = ROOT.TFile("histos_posteriors.root")
   setstr = 'wp1800'

   for n in range(0,len(nuisances)):
	if nuisances[n]=='':
		continue
	print nuisances[n]
	histo = posteriors.Get(setstr + '__'  +nuisances[n] + '__0')
        c2 = TCanvas('c2', 'post', 600, 400)
	gPad.SetLeftMargin(0.1)
	gPad.SetRightMargin(0.06)
	histo.GetYaxis().SetTitleOffset(1.2)

	histo.Scale(1./histo.Integral())
	histo.SetStats(0)
	histo.SetTitle(';'+nuisances[n]+';Normalized')
	histo.Draw('hist')
	c2.Print(setstr + '__'  +nuisances[n]+'.root','root' )
	c2.Print(setstr + '__'  +nuisances[n]+'.pdf','pdf' )
   
   report.write_html('htmlout_WprimeR_allhad')



model = build_allhad_model()


for p in model.distribution.get_parameters():
    d = model.distribution.get_distribution(p)
    if d['typ'] == 'gauss' and d['mean'] == 0.0 and d['width'] == 1.0:
        model.distribution.set_distribution_parameters(p, range = [-5.0, 5.0])
model_summary(model, True, True, True)

limits_allhad(model,0)

