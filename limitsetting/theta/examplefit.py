# -*- coding: utf-8 -*-
import scipy.interpolate


def histogram_filter(hname):
    return True

def build_allhad_model():
    files = ['example_tmass_forTheta.root']
    model = build_model_from_rootfile(files, histogram_filter,include_mc_uncertainties=True)
    model.fill_histogram_zerobins()
    model.add_lognormal_uncertainty('ttbar_rate', math.log(2.5), 'ttbar')
    return model


model = build_allhad_model()


for p in model.distribution.get_parameters():
    d = model.distribution.get_distribution(p)
    if d['typ'] == 'gauss' and d['mean'] == 0.0 and d['width'] == 1.0:
        model.distribution.set_distribution_parameters(p, range = [-5.0, 5.0])
	if p=='ttbar_rate':
		model.distribution.set_distribution(p, typ = "gauss",mean = 0.0,width = inf, range = [-inf,inf])


signal_process_groups = {'': []}
parVals = mle(model, input = 'data', n=1, signal_process_groups = signal_process_groups)
print "Fit result: ", parVals

print 

parameter_values = {}
for p in model.get_parameters([]):
    parameter_values[p] = parVals[''][p][0][0]
histos = evaluate_prediction(model, parameter_values, include_signal = False)
write_histograms_to_rootfile(histos, 'histos-bstar-mle_syst.root')
print "post fit full: ",parameter_values


parameter_values1 = {}
for p in model.get_parameters([]):
    parameter_values1[p] = parVals[''][p][0][0]+parVals[''][p][0][1]
histos1 = evaluate_prediction(model, parameter_values1, include_signal = False)
write_histograms_to_rootfile(histos1, 'histos-bstar-mleup_syst.root')
print "post fit full up: ",parameter_values1


parameter_values2 = {}
for p in model.get_parameters([]):
    parameter_values2[p] = parVals[''][p][0][0]-parVals[''][p][0][1]
histos2 = evaluate_prediction(model, parameter_values2, include_signal = False)
write_histograms_to_rootfile(histos2, 'histos-bstar-mledown_syst.root')
print "post fit full down: ",parameter_values2


parameter_values3 = {}
for p in model.get_parameters([]):
    if p=='ttbar_rate':
    	parameter_values3[p] = parVals[''][p][0][0]+parVals[''][p][0][1]
    else:
    	parameter_values3[p] = 0.0
histos3 = evaluate_prediction(model, parameter_values3, include_signal = False)
write_histograms_to_rootfile(histos3, 'histos-bstar-ttbarrateup_syst.root')
print "post fit rate up: ",parameter_values3


parameter_values4 = {}
for p in model.get_parameters([]):
    if p=='ttbar_rate':
    	parameter_values4[p] = parVals[''][p][0][0]-parVals[''][p][0][1]
    else:
    	parameter_values4[p] = 0.0
histos4 = evaluate_prediction(model, parameter_values4, include_signal = False)
write_histograms_to_rootfile(histos4, 'histos-bstar-ttbarratedown_syst.root')
print "post fit rate down: ",parameter_values4


parameter_values5 = {}
for p in model.get_parameters([]):
    if p=='ttbar_rate':
    	parameter_values5[p] = parVals[''][p][0][0]
    else:
    	parameter_values5[p] = 0.0
histos5 = evaluate_prediction(model, parameter_values5, include_signal = False)
write_histograms_to_rootfile(histos5, 'histos-bstar-ttbarrate_syst.root')
print "post fit rate: ",parameter_values5

print
model_summary(model)
report.write_html('htmlout')

