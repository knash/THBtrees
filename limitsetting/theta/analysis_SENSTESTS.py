# -*- coding: utf-8 -*-
import scipy.interpolate
import ROOT
from ROOT import *
def histogram_filter(hname):
    return True
def build_allhad_model():
    files = ['SENSTESTSdefault.root']
    model = build_model_from_rootfile(files, histogram_filter,  include_mc_uncertainties=True)
    model.fill_histogram_zerobins()
    model.set_signal_processes('wp*')
    for p in model.processes:
       	if p=='qcd': 
	       	model.add_lognormal_uncertainty('totqcd', math.log(1.1), p)
       	model.add_lognormal_uncertainty('lumi', math.log(1.027), p)
       	if p=='ttbar':
       		model.add_lognormal_uncertainty('topsf', math.log(1.02), p)
		continue
      	model.add_lognormal_uncertainty('generalsig', math.log(1.02), p)
    return model

def limits_allhad(model, step = 0):

   exp,obs = asymptotic_cls_limits(model,use_data=False)
   print exp
   exp.write_txt('testexp.txt')

model = build_allhad_model()


for p in model.distribution.get_parameters():
    d = model.distribution.get_distribution(p)
    if d['typ'] == 'gauss' and d['mean'] == 0.0 and d['width'] == 1.0:
        model.distribution.set_distribution_parameters(p, range = [-5.0, 5.0])
model_summary(model, True, True, True)

limits_allhad(model,0)

