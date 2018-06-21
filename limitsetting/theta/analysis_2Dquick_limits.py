# -*- coding: utf-8 -*-
import scipy.interpolate
import ROOT
from ROOT import *
def histogram_filter(hname):
    if 'ttag' in hname: return False
    if 'WEx' in hname: return False
    #if 'bin6' in hname: return False
    #if 'bin0' in hname: return False
    #if 'bin1' in hname: return False
    #if 'bin2' in hname: return False
    #if 'bin4' in hname: return False
    #if 'bin5' in hname: return False
    #if 'bin6' in hname: return False
    return True
def build_allhad_model():
    files = ["RFILE"]
    model = build_model_from_rootfile(files, histogram_filter,  include_mc_uncertainties=True)
    model.fill_histogram_zerobins()
    model.set_signal_processes('wp*')


    #model.scale_predictions(0.91, "wp1500", "*")
    #model.scale_predictions(0.91, "wp2000", "*")
    #model.scale_predictions(0.91, "wp2500", "*")
    #model.scale_predictions(0.91, "wp3000", "*")

    model.scale_predictions(.58/.5, "wp1500", "*")
    model.scale_predictions(.58/.5, "wp2000", "*")
    model.scale_predictions(.58/.5, "wp2500", "*")
    model.scale_predictions(.58/.5, "wp3000", "*")

    for p in model.processes:
	print p
       	if p=='qcd': 
		continue
       	model.add_lognormal_uncertainty('lumi', math.log(1.027), p)
    	model.add_asymmetric_lognormal_uncertainty('topsf',math.log(1.1),math.log(1.04), p)
       	if p=='ttbar':
    		model.add_asymmetric_lognormal_uncertainty('ttbar_xsec',math.log(1.055),math.log(1.048), p)
		continue

    return model

def limits_allhad(model, step = 0):
   fnamestr = "RFILE"
   exp,obs = asymptotic_cls_limits(model,use_data=False)
   print exp
   exp.write_txt('test2Dexp'+fnamestr.replace('.root','')+'.txt')



   #bexp,bobs = bayesian_limits(model,what='expected',input_expected='toys:0')
   #print "BAYES",bexp
   #bexp.write_txt('cslimBAYESexp'+fnamestr.replace('.root','')+'.txt')




model = build_allhad_model()


for p in model.distribution.get_parameters():
    d = model.distribution.get_distribution(p)
    if d['typ'] == 'gauss' and d['mean'] == 0.0 and d['width'] == 1.0:
        model.distribution.set_distribution_parameters(p, range = [-5.0, 5.0])
model_summary(model, True, True, True)

limits_allhad(model,0)

