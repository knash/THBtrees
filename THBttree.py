#! /usr/bin/env python

import os
import glob
import math
import copy
import random
import time
from math import sqrt
#import quickroot
#from quickroot import *
import ROOT 
from ROOT import TLorentzVector,TH1F,TH2F,TTree,TFile,gROOT

import sys
from DataFormats.FWLite import Events, Handle
from optparse import OptionParser

parser = OptionParser()

parser.add_option('-s', '--set', metavar='F', type='string', action='store',
                  default	=	'THB',
                  dest		=	'set',
                  help		=	'data or ttbar')

parser.add_option('-C', '--coll', metavar='F', type='string', action='store',
                  default	=	'Puppi',
                  dest		=	'coll',
                  help		=	'CHS or Puppi')

parser.add_option('-n', '--num', metavar='F', type='string', action='store',
                  default	=	'all',
                  dest		=	'num',
                  help		=	'job number')

parser.add_option('-j', '--jobs', metavar='F', type='string', action='store',
                  default	=	'1',
                  dest		=	'jobs',
                  help		=	'number of jobs')


parser.add_option('-t', '--tname', metavar='F', type='string', action='store',
                  default	=	'HLT_PFHT900,HLT_PFHT800,HLT_JET450',
                  dest		=	'tname',
                  help		=	'trigger name')
parser.add_option('-S', '--split', metavar='F', type='string', action='store',
                  default	=	'file',
                  dest		=	'split',
                  help		=	'split by event of file')

parser.add_option('-g', '--grid', metavar='F', type='string', action='store',
                  default	=	'off',
                  dest		=	'grid',
                  help		=	'running on grid off or on')

parser.add_option('-c', '--cuts', metavar='F', type='string', action='store',
                  default	=	'default',
                  dest		=	'cuts',
                  help		=	'Cuts type (ie default, rate, etc)')

(options, args) = parser.parse_args()

tname = options.tname.split(',')
tnamestr = ''
for iname in range(0,len(tname)):
	tnamestr+=tname[iname]
	if iname!=len(tname)-1:
		tnamestr+='OR'

if tnamestr=='HLT_PFHT900ORHLT_PFHT800ORHLT_JET450':
	tnameformat='nominal'
elif tnamestr=='':
	tnameformat='none'
else:
	tnameformat=tnamestr


print "Options summary"
print "=================="
for  opt,value in options.__dict__.items():
	#print str(option)+ ": " + str(options[option]) 
	print str(opt) +': '+ str(value)
print "=================="
print ""
di = ""
if options.grid == 'on':
	di = "tardir/"
	sys.path.insert(0, 'tardir/')

gROOT.Macro(di+"rootlogon.C")

import WprimetoVlq_Functions	
from WprimetoVlq_Functions import *



WPF = WprimetoVlq_Functions(options.cuts,options.coll,"")
#Load up cut values based on what selection we want to run 
Cuts = WPF.LoadCuts



####EDIT
ptmincut = Cuts['ptmincut']
pthcut = Cuts['pthcut']
pttcut = Cuts['pttcut']
ptbcut = Cuts['ptbcut']
tmass = Cuts['tmass']
tau32 = Cuts['tau32']
sjbtagt = Cuts['sjbtagt']
sjbtagh = Cuts['sjbtagh']
btag = Cuts['btag']
hmass = Cuts['hmass']
hmassinvert = Cuts['hmassinvert']
tau21 = Cuts['tau21']
####EDIT





#For large datasets we need to parallelize the processing
jobs=int(options.jobs)
if jobs != 1:
	num=int(options.num)
	jobs=int(options.jobs)
	print "Running over " +str(jobs)+ " jobs"
	print "This will process job " +str(num)
else:
	print "Running over all events"

#This section defines some strings that are used in naming the optput files


files = WPF.Load_Ntuples(options.set,di) 

jobiter = 0
splitfiles = []

if jobs != 1 and options.split=="file":
    for ifile in range(1,len(files)+1):
    	if (ifile-1) % jobs == 0:
		jobiter+=1
	count_index = ifile  - (jobiter-1)*jobs
	if count_index==num:
		splitfiles.append(files[ifile-1])

    events = Events(splitfiles)
    runs = Runs(splitfiles)

if options.split=="event" or jobs == 1:	  
	events = Events(files)
    	runs = Runs(files)

totnev = 0


for run in runs:

	run.getByLabel (WPF.nevLabel,WPF.nevHandle )
   	nev 		= 	WPF.nevHandle.product() 
		
	totnev+=nev[0]
print "Total unfiltered events in selection: ",totnev



#AK8HL = WPF.Initlv("jetsAK8",ptmod,options.coll)
#AK4HL = WPF.Initlv("jetsAK4",ptmod,options.coll)

#---------------------------------------------------------------------------------------------------------------------#

if jobs != 1:
	f = TFile( "THBttree"+options.set+"_job"+options.num+"of"+options.jobs+".root", "recreate" )
else:
	f = TFile( "THBttree"+options.set+".root", "recreate" )

unclist = []
if options.set.find('data')==-1:
	unclist = ['PUup','PUdown']
	if options.set.find('ttbar')!=-1:
		unclist.extend(['Alpup','Alpdown','Q2up','Q2down','Tptup','Tptdown','PDFup','PDFdown'])	
	if options.set.find('THB')!=-1:
		unclist.extend(['Alpup','Alpdown','Q2up','Q2down','PDFup','PDFdown'])	

print "Creating histograms"

histosets = {}

f.cd()
#---------------------------------------------------------------------------------------------------------------------#
nev = TH1F("nev",	"nev",		1, 0, 1 )


#---------------------------------------------------------------------------------------------------------------------#

# loop over events
#---------------------------------------------------------------------------------------------------------------------#

count = 0

print "Start looping"
#initialize the ttree variables







tree_vars = {
	"AK8_pt":array('d',[-100.]*7),
	"AK8_eta":array('d',[-100.]*7),
	"AK8_phi":array('d',[-100.]*7),
	"AK8_M":array('d',[-100.]*7),
	"AK8_SDMtop":array('d',[-100.]*7),
	"AK8_SDMhiggs":array('d',[-100.]*7),
	"AK8_tau21":array('d',[-100.]*7),
	"AK8_tau32":array('d',[-100.]*7),
	"AK8_sjbtag":array('d',[-100.]*7),
	"AK8_dbtag":array('d',[-100.]*7),
	"AK4_pt":array('d',[-100.]*7),
	"AK4_eta":array('d',[-100.]*7),
	"AK4_phi":array('d',[-100.]*7),
	"AK4_M":array('d',[-100.]*7),
	"AK4_btag":array('d',[-100.]*7),
	"AK4_ht":array('d',[-100.]),
	"run":array('d',[-100.]),
	"lumi":array('d',[-100.]),
	"event":array('d',[-100.]),
	}

if  options.set.find('data')==-1:

	tree_vars.update({
		"AK8_JECup":array('d',[1.]*7),
		"AK8_JECdown":array('d',[1.]*7),
		"AK8_JERup":array('d',[1.]*7),
		"AK8_JERdown":array('d',[1.]*7),
		"AK8_JECMup":array('d',[1.]*7),
		"AK8_JECMdown":array('d',[1.]*7),
		"AK8_JERMup":array('d',[1.]*7),
		"AK8_JERMdown":array('d',[1.]*7),
		"AK8_weight_Htag":array('d',[1.]*7),
		"AK8_weight_Htagup":array('d',[1.]*7),
		"AK8_weight_Htagdown":array('d',[1.]*7),
		"AK8_weight_Hmistag":array('d',[1.]*7),
		"AK8_weight_Hmistagup":array('d',[1.]*7),
		"AK8_weight_Hmistagdown":array('d',[1.]*7),
		"AK8_weight_WExup":array('d',[1.]*7),
		"AK8_weight_WExdown":array('d',[1.]*7),
		"AK8_flav":array('d',[-100.]*7),
		"AK4_weight_Bup":array('d',[1.]*7),
		"AK4_weight_B":array('d',[1.]*7),
		"AK4_weight_Bdown":array('d',[1.]*7),
		"AK4_weight_Bmisup":array('d',[1.]*7),
		"AK4_weight_Bmis":array('d',[1.]*7),
		"AK4_weight_Bmisdown":array('d',[1.]*7),
		"AK4_JECup":array('d',[1.]*7),
		"AK4_JECdown":array('d',[1.]*7),
		"AK4_JERup":array('d',[1.]*7),
		"AK4_JERdown":array('d',[1.]*7),
		"AK4_flav":array('d',[-100.]*7),
		"AK4_htJECup":array('d',[-100.]),
		"AK4_htJECdown":array('d',[-100.]),
		"AK4_htJERup":array('d',[-100.]),
		"AK4_htJERdown":array('d',[-100.]),
		})













for unc in unclist:
	tree_vars["weight_"+unc]=array('d',[1.])
	if unc.find('up')!=-1 and (unc.find('PU')!=-1 or unc.find('Trig')!=-1 or unc.find('Tpt')!=-1):
		tree_vars["weight_"+unc.replace('up','')]=array('d',[1.])

Tree = WPF.Make_Trees(tree_vars)
Histoname = "TriggerWeight_"+tnamestr+"_pre_HLT_PFHT475,HLT_JET260"

print "Loading ",Histoname, "from", di+"Triggerweight_data.root"
TrigFile = TFile(di+"Triggerweight_data.root")
TrigPlot = TrigFile.Get(Histoname)
	

PUFile = TFile(di+"PileUp_Ratio_ttbar.root")
PUplotvec = [PUFile.Get("Pileup_Ratio"),PUFile.Get("Pileup_Ratio_up"),PUFile.Get("Pileup_Ratio_down")]
		


goodEvents = []
nev.SetBinContent(1,totnev)
jetidAK8effD = 0
jetidAK8effN = 0
jetidAK4effD = 0
jetidAK4effN = 0


filtereffN = 0
filtereffD = 0
print options 

for event in events:
    normweight = 1.0
    count	= 	count + 1
    
    m = 0
    t = 0
    #if count > 5000:
	#break


    if count % 10000 == 0 :
      print  '--------- Processing Event ' + str(count) #+'   -- percent complete ' + str(100*count/totevents) + '% -- '

    #Here we split up event processing based on number of jobs 
    #This is set up to have jobs range from 1 to the total number of jobs (ie dont start at job 0)

    if jobs != 1 and options.split=="event":
    	if (count - 1) % jobs == 0:
		jobiter+=1
	count_index = count - (jobiter-1)*jobs
	if count_index!=num:
		continue 

    #AK8LV = WPF.Makelv(AK8HL,event)
    #AK4LV = WPF.Makelv(AK4HL,event)




    event.getByLabel (WPF.PtnomLabel, WPF.PtnomHandle)
    Ptnom		= 	WPF.PtnomHandle.product()


    event.getByLabel (WPF.EtanomLabel, WPF.EtanomHandle)
    Etanom		= 	WPF.EtanomHandle.product()


    # We load up the relevant handles and labels and create collections
    hptjets = 0
    #totht=0.0
    for iAKJ in xrange(len(Ptnom)):
	if ptmincut[0] < Ptnom[iAKJ] < ptmincut[1]:
		if abs(Etanom[iAKJ]) < 2.4:
			hptjets+=1


    event.getByLabel (WPF.LooseAK4Label, WPF.LooseAK4Handle)
    LooseAK4 	= 	WPF.LooseAK4Handle.product()




    event.getByLabel (WPF.PtAK4nomLabel, WPF.PtAK4nomHandle)
    PtAK4nom		= 	WPF.PtAK4nomHandle.product()


    if  hptjets>=2:


    	event.getByLabel (WPF.softDropMassLabel, WPF.softDropMassHandle)
    	topJetMass 	= 	WPF.softDropMassHandle.product()



    	event.getByLabel (WPF.PhinomLabel, WPF.PhinomHandle)
    	Phinom		= 	WPF.PhinomHandle.product()


    	event.getByLabel (WPF.MassnomLabel, WPF.MassnomHandle)
    	Massnom		= 	WPF.MassnomHandle.product()





    	event.getByLabel (WPF.softDropMassLabel, WPF.softDropMassHandle)
    	topJetMass 	= 	WPF.softDropMassHandle.product()



    	event.getByLabel (WPF.softDropMassuncorrLabel, WPF.softDropMassuncorrHandle)
    	topJetMassuncorr 	= 	WPF.softDropMassuncorrHandle.product()

   	event.getByLabel (WPF.BDiscAK4Label,WPF.BDiscAK4Handle)
    	bJetBDiscAK4	= 	WPF.BDiscAK4Handle.product()

    	event.getByLabel (WPF.vsubjets0indexLabel,WPF.vsubjets0indexHandle )
    	vsubjets0index 		= 	WPF.vsubjets0indexHandle.product() 

    	event.getByLabel (WPF.vsubjets1indexLabel,WPF.vsubjets1indexHandle )
    	vsubjets1index 		= 	WPF.vsubjets1indexHandle.product() 

    	event.getByLabel (WPF.subjetsAK8CSVLabel,WPF.subjetsAK8CSVHandle )
    	subjetsAK8CSV		= 	WPF.subjetsAK8CSVHandle.product() 
 

    	event.getByLabel (WPF.jetAK8DoubleBAK8Label,WPF.jetAK8DoubleBAK8Handle )
    	jetAK8DoubleBAK8		= 	WPF.jetAK8DoubleBAK8Handle.product() 
 

    	event.getByLabel (WPF.tau1Label, WPF.tau1Handle)
    	tau1 		= 	WPF.tau1Handle.product()  


    	event.getByLabel (WPF.tau2Label, WPF.tau2Handle)
    	tau2 		= 	WPF.tau2Handle.product()  


    	event.getByLabel (WPF.tau3Label, WPF.tau3Handle)
    	tau3 		= 	WPF.tau3Handle.product()  
	
	
	if  options.set.find('data')==-1:

	    	event.getByLabel (WPF.PtjesupLabel, WPF.PtjesupHandle)
		Ptjesup		= 	WPF.PtjesupHandle.product()


	    	event.getByLabel (WPF.PtjesdownLabel, WPF.PtjesdownHandle)
		Ptjesdown		= 	WPF.PtjesdownHandle.product()

	


	    	event.getByLabel (WPF.PtjerupLabel, WPF.PtjerupHandle)
		Ptjerup		= 	WPF.PtjerupHandle.product()


	    	event.getByLabel (WPF.PtjerdownLabel, WPF.PtjerdownHandle)
		Ptjerdown		= 	WPF.PtjerdownHandle.product()




	    	event.getByLabel (WPF.softDropMassjesupLabel, WPF.softDropMassjesupHandle)
		softDropMassjesup		= 	WPF.softDropMassjesupHandle.product()


	    	event.getByLabel (WPF.softDropMassjesdownLabel, WPF.softDropMassjesdownHandle)
		softDropMassjesdown		= 	WPF.softDropMassjesdownHandle.product()

	


	    	event.getByLabel (WPF.softDropMassjerupLabel, WPF.softDropMassjerupHandle)
		softDropMassjerup		= 	WPF.softDropMassjerupHandle.product()


	    	event.getByLabel (WPF.softDropMassjerdownLabel, WPF.softDropMassjerdownHandle)
		softDropMassjerdown		= 	WPF.softDropMassjerdownHandle.product()








	if  options.set.find('data')!=-1 and tnamestr!='none':

		PASS = False
		for curTrig in tname:
			TrigH = WPF.Triggermap[curTrig][1]
			TrigL = WPF.Triggermap[curTrig][0]
			event.getByLabel(TrigL,TrigH )
			try:
				if TrigH.product()[-1]:
					PASS = True
			except:
				#print "Trig Warning!"
				continue 
		if (not PASS):
			continue 




    	event.getByLabel (WPF.LooseLabel, WPF.LooseHandle)
    	Loose 	= 	WPF.LooseHandle.product()




	temp_vars ={
	"AK8_pt":array('d',[-100.]*7),
	"AK8_eta":array('d',[-100.]*7),
	"AK8_phi":array('d',[-100.]*7),
	"AK8_M":array('d',[-100.]*7),
	"AK8_SDMtop":array('d',[-100.]*7),
	"AK8_SDMhiggs":array('d',[-100.]*7),
	"AK8_tau21":array('d',[-100.]*7),
	"AK8_tau32":array('d',[-100.]*7),
	"AK8_sjbtag":array('d',[-100.]*7),
	"AK8_dbtag":array('d',[-100.]*7),
	"AK4_pt":array('d',[-100.]*7),
	"AK4_eta":array('d',[-100.]*7),
	"AK4_phi":array('d',[-100.]*7),
	"AK4_M":array('d',[-100.]*7),
	"AK4_btag":array('d',[-100.]*7),
	"AK4_ht":array('d',[-100.]),
	"run":array('d',[-100.]),
	"lumi":array('d',[-100.]),
	"event":array('d',[-100.]),
	}

	if  options.set.find('data')==-1:


		temp_vars.update({
		"AK8_JECup":array('d',[1.]*7),
		"AK8_JECdown":array('d',[1.]*7),
		"AK8_JERup":array('d',[1.]*7),
		"AK8_JERdown":array('d',[1.]*7),
		"AK8_JECMup":array('d',[1.]*7),
		"AK8_JECMdown":array('d',[1.]*7),
		"AK8_JERMup":array('d',[1.]*7),
		"AK8_JERMdown":array('d',[1.]*7),
		"AK8_weight_Htag":array('d',[1.]*7),
		"AK8_weight_Htagup":array('d',[1.]*7),
		"AK8_weight_Htagdown":array('d',[1.]*7),
		"AK8_weight_Hmistag":array('d',[1.]*7),
		"AK8_weight_Hmistagup":array('d',[1.]*7),
		"AK8_weight_Hmistagdown":array('d',[1.]*7),
		"AK8_weight_WExup":array('d',[1.]*7),
		"AK8_weight_WExdown":array('d',[1.]*7),
		"AK8_flav":array('d',[-100.]*7),
		"AK4_weight_Bup":array('d',[1.]*7),
		"AK4_weight_B":array('d',[1.]*7),
		"AK4_weight_Bdown":array('d',[1.]*7),
		"AK4_weight_Bmisup":array('d',[1.]*7),
		"AK4_weight_Bmis":array('d',[1.]*7),
		"AK4_weight_Bmisdown":array('d',[1.]*7),
		"AK4_htJECup":array('d',[-100.]),
		"AK4_htJECdown":array('d',[-100.]),
		"AK4_htJERup":array('d',[-100.]),
		"AK4_htJERdown":array('d',[-100.]),
		"AK4_JECup":array('d',[1.]*7),
		"AK4_JECdown":array('d',[1.]*7),
		"AK4_JERup":array('d',[1.]*7),
		"AK4_JERdown":array('d',[1.]*7),
		"AK4_flav":array('d',[-100.]*7),
		})


	AK8LV = []

	for ijet in xrange(min([7,hptjets])):	
		if abs(Etanom[ijet])>2.4:
			continue 

		try:
    			SJ_csvvals = [subjetsAK8CSV[int(vsubjets0index[ijet])],subjetsAK8CSV[int(vsubjets1index[ijet])]]
		except:
			SJ_csvvals=[0.,0.] 
			print "no subjet"

		isloose = Loose[ijet]>0.5
		
		jetidAK8effD +=1
		if isloose:
			jetidAK8effN += 1

		AK8LV.append(TLorentzVector())
		AK8LV[-1].SetPtEtaPhiM(Ptnom[ijet],Etanom[ijet],Phinom[ijet],Massnom[ijet])

		if  options.set.find('data')!=-1:
			maxAK8pt = AK8LV[ijet].Perp()
		else:
			maxAK8pt = max(Ptjesup[ijet],Ptjesdown[ijet],Ptjerup[ijet],Ptjerdown[ijet],AK8LV[ijet].Perp())
		if isloose and (ptmincut[0] < maxAK8pt < ptmincut[1]):
	

			temp_vars["AK8_sjbtag"][ijet] = max(SJ_csvvals)

			if tau2[ijet]>0.:
				tau32val =  tau3[ijet]/tau2[ijet]
			else:
				tau32val =  1.0


			temp_vars["AK8_tau32"][ijet] = tau32val




			temp_vars["AK8_pt"][ijet] = AK8LV[ijet].Perp()
			temp_vars["AK8_eta"][ijet] = AK8LV[ijet].Eta()
			temp_vars["AK8_phi"][ijet] = AK8LV[ijet].Phi()
			temp_vars["AK8_M"][ijet] = AK8LV[ijet].M()

			if  options.set.find('data')==-1:
				if AK8LV[ijet].Perp()>0.:
					temp_vars["AK8_JECup"][ijet] = Ptjesup[ijet]/AK8LV[ijet].Perp()
					temp_vars["AK8_JECdown"][ijet] = Ptjesdown[ijet]/AK8LV[ijet].Perp()
					temp_vars["AK8_JERup"][ijet] = Ptjerup[ijet]/AK8LV[ijet].Perp()
					temp_vars["AK8_JERdown"][ijet] = Ptjerdown[ijet]/AK8LV[ijet].Perp()
				if topJetMass[ijet]>0.:
					temp_vars["AK8_JECMup"][ijet] = softDropMassjesup[ijet]/topJetMass[ijet]
					temp_vars["AK8_JECMdown"][ijet] = softDropMassjesdown[ijet]/topJetMass[ijet]
					temp_vars["AK8_JERMup"][ijet] = softDropMassjerup[ijet]/topJetMass[ijet]
					temp_vars["AK8_JERMdown"][ijet] = softDropMassjerdown[ijet]/topJetMass[ijet]




			temp_vars["AK8_SDMtop"][ijet] = topJetMassuncorr[ijet]

			if tau1[ijet]>0.:
				tau21val =  tau2[ijet]/tau1[ijet]
			else:
				tau21val =  1.0
			temp_vars["AK8_tau21"][ijet] = tau21val
			temp_vars["AK8_SDMhiggs"][ijet] = topJetMass[ijet]
			temp_vars["AK8_dbtag"][ijet] = jetAK8DoubleBAK8[ijet]
	if len(AK8LV)<2:
		continue







    	event.getByLabel (WPF.filtersbitLabel, WPF.filtersbitHandle)
    	filters 	= 	WPF.filtersbitHandle.product()


	filtereffD += 1
	evpass = True
	for filt in filters:
		if (not filt):
			evpass=False
	if (not evpass):
		continue 




    	event.getByLabel (WPF.EtaAK4nomLabel, WPF.EtaAK4nomHandle)
    	EtaAK4nom		= 	WPF.EtaAK4nomHandle.product()



    	event.getByLabel (WPF.PhiAK4nomLabel, WPF.PhiAK4nomHandle)
    	PhiAK4nom		= 	WPF.PhiAK4nomHandle.product()


    	event.getByLabel (WPF.MassAK4nomLabel, WPF.MassAK4nomHandle)
    	MassAK4nom		= 	WPF.MassAK4nomHandle.product()




	if  options.set.find('data')==-1:

	    	event.getByLabel (WPF.PtAK4jesupLabel, WPF.PtAK4jesupHandle)
		PtAK4jesup		= 	WPF.PtAK4jesupHandle.product()

	    	event.getByLabel (WPF.PtAK4jesdownLabel, WPF.PtAK4jesdownHandle)
		PtAK4jesdown		= 	WPF.PtAK4jesdownHandle.product()

	    	event.getByLabel (WPF.PtAK4jerupLabel, WPF.PtAK4jerupHandle)
		PtAK4jerup		= 	WPF.PtAK4jerupHandle.product()

	    	event.getByLabel (WPF.PtAK4jerdownLabel, WPF.PtAK4jerdownHandle)
		PtAK4jerdown		= 	WPF.PtAK4jerdownHandle.product()

	

	AK4LV = []

        for iAK4 in xrange(min([7,len(PtAK4nom)])):

		
		AK4LV.append(TLorentzVector())
		AK4LV[-1].SetPtEtaPhiM(PtAK4nom[iAK4],EtaAK4nom[iAK4],PhiAK4nom[iAK4],MassAK4nom[iAK4])


		if  options.set.find('data')!=-1:
			maxAK4pt = AK4LV[iAK4].Perp()
		else:
			maxAK4pt = max(PtAK4jesup[iAK4],PtAK4jesdown[iAK4],PtAK4jerup[iAK4],PtAK4jerdown[iAK4],AK4LV[iAK4].Perp())


		isloose= LooseAK4[iAK4]>0.5

		jetidAK4effD +=1
		if isloose:
			jetidAK4effN += 1
		if isloose and (ptbcut[0] < maxAK4pt < ptbcut[1]) and abs(AK4LV[iAK4].Eta())<2.4:
		
			temp_vars["AK4_pt"][iAK4] = AK4LV[iAK4].Perp()
			temp_vars["AK4_eta"][iAK4] = AK4LV[iAK4].Eta()
			temp_vars["AK4_phi"][iAK4] = AK4LV[iAK4].Phi()
			temp_vars["AK4_M"][iAK4] = AK4LV[iAK4].M()
			temp_vars["AK4_btag"][iAK4] = bJetBDiscAK4[iAK4]
			if  options.set.find('data')==-1:
				if AK4LV[iAK4].Perp()>0.:
					temp_vars["AK4_JECup"][iAK4] = PtAK4jesup[iAK4]/AK4LV[iAK4].Perp()
					temp_vars["AK4_JECdown"][iAK4] = PtAK4jesdown[iAK4]/AK4LV[iAK4].Perp()
					temp_vars["AK4_JERup"][iAK4] = PtAK4jerup[iAK4]/AK4LV[iAK4].Perp()
					temp_vars["AK4_JERdown"][iAK4] = PtAK4jerdown[iAK4]/AK4LV[iAK4].Perp()



	
	CurrTrigPlot  =  TrigPlot
	triggerweight = 1.0


	uncweight={}
	nomweight={}
	for unc in unclist:
		uncweight[unc]=1.0
		if unc.find('up')!=-1:
			nomweight[unc.replace('up','nom')]=1.0
	

	puweight = 1.0
	puweightup = 1.0
	puweightdown = 1.0
	
	ptw=1.0
	tpart,hpart,bpart = -1,-1,-1
	if options.set.find('data')==-1:

			event.getByLabel (WPF.partonFlavourLabel, WPF.partonFlavourHandle)
	    		pflavs 		= 	WPF.partonFlavourHandle.product()

			event.getByLabel (WPF.partonFlavourAK4Label, WPF.partonFlavourAK4Handle)
	    		pflavsAK4 		= 	WPF.partonFlavourAK4Handle.product()


			event.getByLabel (WPF.GenLabel, WPF.GenHandle)
	    		gplist 		= 	WPF.GenHandle.product()
			if options.set.find('THB')!=-1: 
				genmatches = {}
				genmatchedlvs = {}
				fhigs,fbot,ftop = False,False,False
				for tgp in gplist:

					tempGPlv = TLorentzVector()
					tempGPlv.SetPtEtaPhiM(tgp.pt(),tgp.eta(),tgp.phi(),tgp.mass())

					tempdrval = 999.
					if abs(tgp.pdgId())==25 and (not fhigs):
						#print tgp.mass()
						matchind = None
						for iclv in  xrange(len(AK8LV)):
							curgdr = AK8LV[iclv].DeltaR(tempGPlv)
							curlv = AK8LV[iclv]
							tempdrval = min(tempdrval,curgdr)
							#print curgdr
							if (curgdr == tempdrval) and curgdr<0.6:
								matchind = iclv
						if matchind!=None:
							temp_vars["AK8_flav"][matchind] = tgp.pdgId()

						fhigs = True

					if abs(tgp.pdgId())==6 and (not ftop):
						matchind = None
						for iclv in  xrange(len(AK8LV)):
							curgdr = AK8LV[iclv].DeltaR(tempGPlv)
							curlv = AK8LV[iclv]
							tempdrval = min(tempdrval,curgdr)
							if (curgdr == tempdrval) and curgdr<0.6:
								matchind = iclv
						if matchind!=None:
							temp_vars["AK8_flav"][matchind] = tgp.pdgId()

						ftop = True




					if abs(tgp.pdgId())==5 and ((abs(tgp.mother().pdgId())==6000024) or (abs(tgp.mother().pdgId())==6000007)) and (not fbot):
						matchind = None
						for iclv in  xrange(len(AK4LV)):
							curgdr = AK4LV[iclv].DeltaR(tempGPlv)
							curlv = AK4LV[iclv]
							tempdrval = min(tempdrval,curgdr)
							if (curgdr == tempdrval) and curgdr<0.2:
								matchind = iclv
						if matchind!=None:
							temp_vars["AK4_flav"][matchind] = tgp.pdgId()

						fbot = True
					
					

					
					if ftop and fbot and fhigs:
						break
			#CHECK (optimize?)
			if options.set.find('ttbar')!=-1:
				ptw = WPF.PTW_Lookup( gplist )


				





			event.getByLabel (WPF.puLabel, WPF.puHandle)
		    	PileUp 		= 	WPF.puHandle.product()

			puweightvec = WPF.PU_Lookup(PileUp[0],PUplotvec)
			
			puweight = puweightvec[0]
			puweightup = puweightvec[1]
			puweightdown = puweightvec[2]
			temp_vars['weight_PU']=puweight
			temp_vars['weight_PUup']=puweightup
			temp_vars['weight_PUdown']=puweightdown


	#CHECK
	AK4ht=0.0
	for iak4j in xrange(len(PtAK4nom)):
		isloose = LooseAK4[iak4j]>0.5
		if not isloose:
			continue 

		AK4ht+=PtAK4nom[iak4j]
	temp_vars['AK4_ht']=AK4ht
	if options.set.find('data')==-1 and tnamestr!='none':


	    	AK4htjesup=0.0
	    	AK4htjesdown=0.0
	    	AK4htjerup=0.0
	    	AK4htjerdown=0.0
	    	for iak4j in xrange(len(PtAK4nom)):
			isloose = LooseAK4[iak4j]>0.5
			if not isloose:
				continue 


		    	AK4htjesup+=PtAK4jesup[iak4j]
		    	AK4htjesdown+=PtAK4jesdown[iak4j]
		    	AK4htjerup+=PtAK4jerup[iak4j]
		    	AK4htjerdown+=PtAK4jerdown[iak4j]


		temp_vars['AK4_htJECup']=AK4htjesup
		temp_vars['AK4_htJECdown']=AK4htjesdown
		temp_vars['AK4_htJERup']=AK4htjerup
		temp_vars['AK4_htJERdown']=AK4htjerdown

		#triggerweight = WPF.Trigger_Lookup(AK4ht,CurrTrigPlot)[0]
		#temp_vars['weight_Trigup'] = WPF.Trigger_Lookup(AK4ht,CurrTrigPlot)[1]
		#temp_vars['weight_Trigdown'] =  WPF.Trigger_Lookup(AK4ht,CurrTrigPlot)[2]
		#temp_vars['weight_Trig']=triggerweight	


		#print temp_vars['weight_Trig']
		#Here, apply top/W sf
		if options.set.find('ttbar')!=-1 or options.set.find('THB')!=-1:

			event.getByLabel (WPF.pdfLabelNOM, WPF.pdfHandleNOM)
			pdfweightNOM 	= 	WPF.pdfHandleNOM.product()


			temp_vars['weight_PDFup'] = WPF.PDF_Lookup(pdfweightNOM , "up" )
			temp_vars['weight_PDFdown'] = WPF.PDF_Lookup(pdfweightNOM , "down" )

			event.getByLabel (WPF.Q2Label, WPF.Q2Handle)
			Q2weight 	= 	WPF.Q2Handle.product()

			temp_vars['weight_Q2up']=max(Q2weight)
			temp_vars['weight_Q2down']=min(Q2weight)
				

			event.getByLabel (WPF.hadronFlavourAK4Label, WPF.hadronFlavourAK4Handle)
	    		hflavsAK4 		= 	WPF.hadronFlavourAK4Handle.product()
			for iAK4clv in  xrange(len(AK4LV)):

					HF = abs(hflavsAK4[iAK4clv])

					bweights = WPF.SFB_Lookup( AK4LV[iAK4clv].Perp(),HF )
					if abs(HF)==5 or abs(HF)==4:
						temp_vars['AK4_weight_Bup'][iAK4clv] = bweights[2]
						temp_vars['AK4_weight_Bdown'][iAK4clv] = bweights[1]
						temp_vars['AK4_weight_B'][iAK4clv] = bweights[0]
				

						temp_vars['AK4_weight_Bmisup'][iAK4clv] = 1.0
						temp_vars['AK4_weight_Bmisdown'][iAK4clv] = 1.0
						temp_vars['AK4_weight_Bmis'][iAK4clv] = 1.0

					else:
						temp_vars['AK4_weight_Bmisup'][iAK4clv] = bweights[2]
						temp_vars['AK4_weight_Bmisdown'][iAK4clv] = bweights[1]
						temp_vars['AK4_weight_Bmis'][iAK4clv] = bweights[0]
				

						temp_vars['AK4_weight_Bup'][iAK4clv] = 1.0
						temp_vars['AK4_weight_Bdown'][iAK4clv] = 1.0
						temp_vars['AK4_weight_B'][iAK4clv] = 1.0


					
					#weight*=bweights[0]
	
			event.getByLabel (WPF.AsLabel, WPF.AsHandle)
			Asweight 	= 	WPF.AsHandle.product()
		
			temp_vars['weight_Alpup']=max(Asweight)
			temp_vars['weight_Alpdown']=min(Asweight)
			#CHECK (optimize?)
			iAK8clv = 0

			for ak8jet in AK8LV:
				Htagweightvec = WPF.SFH_Lookup(ak8jet, gplist )
				
				if Htagweightvec[-1]=='eff':
						temp_vars['AK8_weight_Htag'][iAK8clv] = Htagweightvec[0]
       	 					temp_vars['AK8_weight_Htagup'][iAK8clv] = Htagweightvec[1]
       	 					temp_vars['AK8_weight_Htagdown'][iAK8clv] = Htagweightvec[2]
				if Htagweightvec[-1]=='mistag':
						temp_vars['AK8_weight_Hmistag'][iAK8clv] = Htagweightvec[0]
       	 					temp_vars['AK8_weight_Hmistagup'][iAK8clv] = Htagweightvec[1]
       	 					temp_vars['AK8_weight_Hmistagdown'][iAK8clv] = Htagweightvec[2]
				
				if options.set.find('THB')!=-1: 
						Hpt = ak8jet.Perp()
						delta=0.054*math.log(Hpt/200.0)
       	 					temp_vars['AK8_weight_WExup'][iAK8clv] = 1+delta
        					temp_vars['AK8_weight_WExdown'][iAK8clv] = 1-delta
				iAK8clv += 1
						
		        #CHECK
			if options.set.find('ttbar')!=-1:
				temp_vars['weight_Tptdown']=1.0
				temp_vars['weight_Tpt']=ptw
				temp_vars['weight_Tptup']=max(0.0,(1.0-2.0*(1.0-ptw)))

	temp_vars['run']=event.object().id().run()
	temp_vars['lumi']=event.object().id().luminosityBlock()
	temp_vars['event']=event.object().id().event()

	for tv in tree_vars.keys():
	
        	if type(temp_vars[tv])==array: 
			for i in range(0,len(temp_vars[tv])):
				try:
		             		tree_vars[tv][i] = temp_vars[tv][i]
		      		except:
		                   	print 
		                     	print "BREAK!",tv,i
		                       	print "tree_vars",tree_vars
		                     	print "temp_vars",temp_vars
		                    	print 
		                	break

		else:
		        tree_vars[tv][0] = temp_vars[tv]
	#print tree_vars
	Tree.Fill()




f.cd()
f.Write()
f.Close()
print "AK4 JetId ",float(jetidAK4effN)/float(jetidAK4effD)
print "AK8 JetId ",float(jetidAK8effN)/float(jetidAK8effD)
print "number of events: " + str(count)


