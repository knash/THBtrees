#! /usr/bin/env python

###################################################################
##								 ##
## Name: TBanalyzer.py	   			                 ##
## Author: Kevin Nash 						 ##
## Date: 6/5/2012						 ##
## Purpose: This program performs the main analysis.  		 ##
##	    It takes the tagrates created by  	 		 ##
##          TBrate_Maker.py stored in fitdata, and uses 	 ##
##          them to weigh pre b tagged samples to create a 	 ##
##	    QCD background estimate along with the full event    ##
##	    selection to product Mtb inputs to Theta		 ##
##								 ##
###################################################################

import os
import glob
import math
import copy
import time
import random
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


parser.add_option('-x', '--pileup', metavar='F', type='string', action='store',
                  default	=	'on',
                  dest		=	'pileup',
                  help		=	'If not data do pileup reweighting?')
parser.add_option('-n', '--num', metavar='F', type='string', action='store',
                  default	=	'all',
                  dest		=	'num',
                  help		=	'job number')

parser.add_option('-B', '--bkg', metavar='F', type='string', action='store',
                  default	=	'nominal',
                  dest		=	'bkg',
                  help		=	'cuts to use for rate file')

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

#parser.add_option('-t', '--trigger', metavar='F', type='string', action='store',
#                  default	=	'none',
#                  dest		=	'trigger',
#                  help		=	'none, nominal, up, or down')

parser.add_option('-m', '--modulesuffix', metavar='F', type='string', action='store',
                  default	=	'none',
                  dest		=	'modulesuffix',
                  help		=	'ex. PtSmearUp')

parser.add_option('-g', '--grid', metavar='F', type='string', action='store',
                  default	=	'off',
                  dest		=	'grid',
                  help		=	'running on grid off or on')

parser.add_option('-u', '--ptreweight', metavar='F', type='string', action='store',
                  default	=	'on',
                  dest		=	'ptreweight',
                  help		=	'on or off')

parser.add_option('-p', '--pdfweights', metavar='F', type='string', action='store',
                  default	=	'nominal',
                  dest		=	'pdfweights',
                  help		=	'nominal, up, or down')

parser.add_option('-q', '--q2scale', metavar='F', type='string', action='store',
                  default	=	'nominal',
                  dest		=	'q2scale',
                  help		=	'nominal, up, or down')

parser.add_option('-a', '--alphas', metavar='F', type='string', action='store',
                  default	=	'nominal',
                  dest		=	'alphas',
                  help		=	'nominal, up, or down')

parser.add_option('-J', '--JES', metavar='F', type='string', action='store',
                  default	=	'nominal',
                  dest		=	'JES',
                  help		=	'nominal, up, or down')
parser.add_option('-R', '--JER', metavar='F', type='string', action='store',
                  default	=	'nominal',
                  dest		=	'JER',
                  help		=	'nominal, up, or down')
parser.add_option('-z', '--pdfset', metavar='F', type='string', action='store',
                  default	=	'',
                  dest		=	'pdfset',
                  help		=	'pdf set')
parser.add_option('--printEvents', metavar='F', action='store_true',
                  default=False,
                  dest='printEvents',
                  help='Print events that pass selection (run:lumi:event)')
parser.add_option('-c', '--cuts', metavar='F', type='string', action='store',
                  default	=	'default',
                  dest		=	'cuts',
                  help		=	'Cuts type (ie default, rate, etc)')

parser.add_option('--bkgTree', metavar='F', action='store_true',
                  default=False,
                  dest='bkgTree',
                  help='bkgTree')


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
WPF = WprimetoVlq_Functions(options.cuts,options.coll)
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


tmassinvert = Cuts['tmassinvert']
tau32invert = Cuts['tau32invert']
sjbtagtinvert = Cuts['sjbtagtinvert']


sjbtagh = Cuts['sjbtagh']
#bmass = Cuts['bmass']
btag = Cuts['btag']
hmass = Cuts['hmass']
hmassinvert = Cuts['hmassinvert']
#htau32invert = Cuts['htau32invert']
#hsjbtagtinvert = Cuts['hsjbtagtinvert']
tau21 = Cuts['tau21']
####EDIT

print Cuts



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


mod = ''
post = ''
if options.JES!='nominal':
	mod = mod + 'JES_' + options.JES
	post='jes'+options.JES
if options.JER!='nominal':
	mod = mod + 'JER_' + options.JER
	post='jer'+options.JER





#files = WPF.Load_Ntuples(options.set,di) 
files = WPF.Load_Ntuples(options.set,di,True) 
#files = glob.glob("TTrees/THBttree"+options.set+"*.root")
files=sorted(files)

TFs = []

for fifi in files:
	TFs.append(TFile.Open(fifi))



TTree =  TFs[0].Get('Tree')

bkgset='data'
if (options.set.find('QCD') != -1):
	bkgset='QCD'

jobiter = 0
splitfiles = []
totevents = 0



if jobs != 1 and options.split=="file":
    oldTFs = copy.copy(TFs)
    newTFs = []
    for infi in xrange(len(oldTFs)):
	remain = (infi)%jobs
	#print infi,jobs,(infi)%jobs
	if (remain+1)==num:
		newTFs.append(oldTFs[infi])
		totevents+=newTFs[-1].Get('Tree').GetEntries()

    TFs = newTFs
else:
    totevents+=TFs[0].Get('Tree').GetEntries()
print TFs
print len(TFs),"Files"
rwstr = ''
if options.ptreweight=='off':
	rwstr = '_PTRWoff'
#---------------------------------------------------------------------------------------------------------------------#

if jobs != 1:
	f = TFile( "THBrate"+options.set+rwstr+"_job"+options.num+"of"+options.jobs+"_PSET_"+options.cuts+".root", "recreate" )
else:
	f = TFile( "THBrate"+options.set+rwstr+"_PSET_"+options.cuts+".root", "recreate" )



print "Creating histograms"

histosets = {}

f.cd()
#---------------------------------------------------------------------------------------------------------------------#


topt32loose = TH1F("topt32loose","",     	  	      	30, 0, 1 )
topmassloose = TH1F("topmassloose","",     	  	      	100, 0, 400 )
topsjbtagloose = TH1F("topsjbtagloose","",     	  	      	30, 0, 1  )

Pthfailb= TH1F("Pthfailb","",     	  	      	300, 0, 3000  )
Pthfailbpasst = TH1F("Pthfailbpasst","",     	  	      	300, 0, 3000  )
Pthfailbpasstpassh = TH1F("Pthfailbpasstpassh","",     	  	      	300, 0, 3000  )
Pthfailbpasstfailh = TH1F("Pthfailbpasstfailh","",     	  	      	300, 0, 3000  )
Pthfailbpasstfailhpostinvert = TH1F("Pthfailbpasstfailhpostinvert","",     	  	      	300, 0, 3000  )
T21doublebDen  = TH2F("T21doublebDen",		"",     	  	      	40, 0., 1.,60, -2, 2  )
T21doublebNum  = TH2F("T21doublebNum",		"",     	  	      	40, 0., 1.,60, -2, 2  )
hflavall  = TH1F("hflavall",		"",     	  	      	22, -0.5, 21.5 )
hflavallbfail  = TH1F("hflavallbfail",		"",     	  	      	22, -0.5, 21.5 )
for i in range(0,2):
	for j in range(0,2):
		for k in range(0,2):

			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)] = {}
			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Mthb"]  = TH1F("Mthb_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	140, 500, 8000 )
			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Etah"]  = TH1F("Etah_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	20, 0, 2.4 )
			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Mh"]  = TH1F("Mh_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	200, 0, 400 )
			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Pth"]  = TH1F("Pth_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	300, 0, 3000 )
			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Pthe1"]  = TH1F("Pthe1_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	300, 0, 3000 )
			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["Pthe2"]  = TH1F("Pthe2_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	300, 0, 3000 )
			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["PtEtah"]  = TH2F("PtEtah_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	300, 0, 3000,20, 0, 2.4  )

			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["DRs"]  = TH1F("DRs_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	24, 0, 5.0 )
			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["DRAK4"]  = TH1F("DRAK4_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	24, 0, 5.0 )

			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bindex"]  = TH1F("bindex_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	5, -0.5, 4.5 )
			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["tindex"]  = TH1F("tindex_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	5, -0.5, 4.5 )
			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["hindex"]  = TH1F("hindex_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	5, -0.5, 4.5 )


			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["bflav"]  = TH1F("bflav_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	        22, -0.5, 21.5 )
			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["tflav"]  = TH1F("tflav_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	22, -0.5, 21.5 )
			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["hflav"]  = TH1F("hflav_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	22, -0.5, 21.5 )
			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]["ntrub"]  = TH1F("ntrub_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	7, -0.5, 6.5 )

			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]['ttau32']  = TH1F("ttau32_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	24, 0, 1.0 )
			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]['htau21']  = TH1F("htau21_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	24, 0, 1.0 )
			histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]['hdbtag']  = TH1F("hDoubleB_"+"h"+str(i)+"t"+str(j)+"b"+str(k),		"",     	  	      	24, -1.0, 1.0 )

			for ih in histosets["h"+str(i)+"t"+str(j)+"b"+str(k)]:
				histosets["h"+str(i)+"t"+str(j)+"b"+str(k)][ih].Sumw2()

#---------------------------------------------------------------------------------------------------------------------#

# loop over events
#---------------------------------------------------------------------------------------------------------------------#

count = 0

print "Start looping"
#initialize the ttree variables

bkgTree_vars = {"b_pt":array('d',[0.]),"b_btag":array('d',[0.]),"t_pt":array('d',[0.]),"t_mass":array('d',[0.]),"t_sjbtag":array('d',[0.]),"t_tau32":array('d',[0.]),"h_pt":array('d',[0.]),"h_mass":array('d',[0.]),"h_dbtag":array('d',[0.]),"h_tau21":array('d',[0.]), "m_thb":array('d',[0.]), "m_bh":array('d',[0.]), "m_th":array('d',[0.]), "hpass":array('d',[0.]), "bpass":array('d',[0.])}
bkgTree = WPF.Make_Trees(bkgTree_vars,"bkgTree")

tree_vars = {"b_pt":array('d',[0.]),"b_btag":array('d',[0.]),"t_pt":array('d',[0.]),"t_mass":array('d',[0.]),"t_sjbtag":array('d',[0.]),"t_tau32":array('d',[0.]),    "h_pt":array('d',[0.]),"h_mass":array('d',[0.]),"h_dbtag":array('d',[0.]),"h_tau21":array('d',[0.]),  "weight":array('d',[0.])}
fullselTree = WPF.Make_Trees(tree_vars,"srTree")

Histoname = "TriggerWeight_"+tnamestr+"_pre_HLT_IsoMu24"

TrigFile = TFile(di+"Triggerweight_singlemu.root")
TrigPlot = TrigFile.Get(Histoname)


PUFile = TFile(di+"PileUp_Ratio_ttbar.root")
PUplotvec = [PUFile.Get("Pileup_Ratio"),PUFile.Get("Pileup_Ratio_up"),PUFile.Get("Pileup_Ratio_down")]
		



goodEvents = []

nfail = 0 
npass = 0

filtereffN = 0
filtereffD = 0

npasspresel = 0
ntpass = 0
nhpass = 0
nbpass = 0

jetidAK8effD = 0
jetidAK8effN = 0
jetidAK4effD = 0
jetidAK4effN = 0

numtottag=0
numdubtag=0
numoverlaptag=0
NevPre=0		


#print treedict
n11=0

treearr = []
numtree = 0
for curf in TFs:

    if numtree==0:
    	fullnev = curf.Get('nev')
    else:
    	curnev = curf.Get('nev')
	fullnev.Add(curnev)
    treearr.append(curf.Get('Tree'))
    treedict = WPF.Inittree(treearr[-1])	
    for event in  treearr[-1]:

	    weightSFb = 1.0
	    errorSFb = 0.0
	    weightsubjetSFb = 1.0
	    errorsubjetSFb = 0.0

	    weight = 1.0

	    count	= 	count + 1
	    
	    m = 0
	    t = 0
	    #if count > 2000:
		#break

	    if count % 100000 == 0 :
	      print  '--------- Processing Event ' + str(count) +' (' + str(100*count/totevents) + '%)  --  dataset:', options.set

	    #Here we split up event processing based on number of jobs 
	    #This is set up to have jobs range from 1 to the total number of jobs (ie dont start at job 0)

	    if jobs != 1 and options.split=="event":
	    	if (count - 1) % jobs == 0:
			jobiter+=1
		count_index = count - (jobiter-1)*jobs
		if count_index!=num:
			continue 

	    # We load up the relevant handles and labels and create collections



	    if  True:


		AK4_ht 	= 	treedict["AK4_ht"][0]
	   
	    	if AK4_ht<1000.:
			continue


	    	hJetMass 	= 	treedict["AK8_SDMhiggs"]
	    	topJetMassuncorr 	= 	treedict["AK8_SDMtop"]
	    	AK8CSVMAX 	= 	treedict["AK8_sjbtag"]
	    	jetAK8DoubleBAK8	= 	treedict["AK8_dbtag"]
		#jetAK8DoubleBAK8	= 	[0.9,0.9,0.9,0.9,0.9]
		tau21val	= 	treedict["AK8_tau21"]
		tau32val	= 	treedict["AK8_tau32"]
	    	bJetBDiscAK4 	= 	treedict["AK4_btag"]
	
		bind = []
		hind = []
		ahind = []
		tind = [] 
		atind = [] 
		npasspresel += 1



		puweight = 1.0
		puweightup = 1.0
		puweightdown = 1.0
	
		ptw=1.0
		htagw=1.0



		uncweight = {}
		if options.set.find('data')==-1:
			
			if options.ptreweight!='off' and options.set.find('ttbar')!=-1:
				#ptw = WPF.PTW_Lookup( gplist )
				ptw = treedict["weight_Tpt"][0]

			if options.set.find('ttbar')!=-1 or options.set.find('THB')!=-1:
				if len(hind)!=0:
					flavvec = treedict["AK8_flav"]

					if abs(flavvec[defs['h']])==25:
							AK8_Hweight = treedict["AK8_weight_Hmistag"]	

							htagw=AK8_Hweight[defs['h']]
					if abs(flavvec[defs['h']])==6:
							AK8_Hweight = treedict["AK8_weight_Hmistag"]	
							htagw=AK8_Hweight[defs['h']]





			if options.pileup!='off':
			

				puweight = treedict["weight_PU"][0]
				puweightup = treedict["weight_PUup"][0]
				puweightdown = treedict["weight_PUdown"][0]
				uncweight['']=puweight
				uncweight['PUup']=puweightup
				uncweight['PUdown']=puweightdown

		AK8_pt 	= 	treedict["AK8_pt"]

		AK8_eta = 	treedict["AK8_eta"]
		AK8_phi = 	treedict["AK8_phi"]
		AK8_M 	= 	treedict["AK8_M"]
		AK8LV = []


		#start = time.time()



		for ijet in xrange(len(AK8_pt)):

			if AK8_pt[ijet]<0.:
				AK8LV.append(None)
				break
			AK8LV.append(TLorentzVector())
			AK8LV[-1].SetPtEtaPhiM(AK8_pt[ijet],AK8_eta[ijet],AK8_phi[ijet],AK8_M[ijet])

	    	




			if tmassinvert[0]<topJetMassuncorr[ijet]<tmassinvert[1]:
				if pttcut[0]<AK8LV[ijet].Perp()<pttcut[1]:
					SJ_csvmax = AK8CSVMAX[ijet]
					if sjbtagtinvert[0]<SJ_csvmax<=sjbtagtinvert[1]:
						tau32_cut =  tau32invert[0]<=tau32val[ijet]<tau32invert[1]
						if tau32_cut:
							atind.append(ijet)





			if tmass[0]<topJetMassuncorr[ijet]<tmass[1]:
				if pttcut[0]<AK8LV[ijet].Perp()<pttcut[1]:
					SJ_csvmax = AK8CSVMAX[ijet]
					if sjbtagt[0]<SJ_csvmax<=sjbtagt[1]:
						tau32_cut =  tau32[0]<=tau32val[ijet]<tau32[1]
						if tau32_cut:
							tind.append(ijet)


			if hmassinvert[0]<hJetMass[ijet]<hmassinvert[1]:
				tau21_cut =  tau21[0]<=tau21val[ijet]<tau21[1]
				if tau21_cut:
					if pthcut[0]<AK8LV[ijet].Perp()<pthcut[1]:
						ahind.append(ijet)
				if pthcut[0]<AK8LV[ijet].Perp()<pthcut[1]:
					T21doublebDen.Fill(tau21val[ijet],jetAK8DoubleBAK8[ijet])
			if hmass[0]<hJetMass[ijet]<hmass[1]:
				if pthcut[0]<AK8LV[ijet].Perp()<pthcut[1]:
					T21doublebNum.Fill(tau21val[ijet],jetAK8DoubleBAK8[ijet])
					if sjbtagh[0]<jetAK8DoubleBAK8[ijet]<=sjbtagh[1]:
						tau21_cut =  tau21[0]<=tau21val[ijet]<tau21[1]
						if tau21_cut:
							hind.append(ijet)


		hind,tind  =  WPF.select([hind,tind])
		ahind,tind  =  WPF.select([ahind,tind])
		hind,atind  =  WPF.select([hind,atind])
		ahind,atind  =  WPF.select([ahind,atind])
		

		#end = time.time()
		#print end - start

		defs = {}

		random.seed(treedict["event"][0]) 

		if len(hind)>0:
			random.shuffle(hind)
			hind=[hind[0]]
			defs['h']=hind[0]
		if len(tind)>0:
			random.shuffle(tind)
			tind=[tind[0]]
			defs['t']=tind[0]

		if len(tind)==0 and len(atind)>0:
			random.shuffle(atind)
			atind=[atind[0]]
			defs['t']=atind[0]

		if len(hind)==0 and len(ahind)>0:
			random.shuffle(ahind)
			ahind = [ahind[0]]
			defs['h']=ahind[0]
		if len(hind)==0 and len(ahind)==0:
			continue
		if len(tind)==0 and len(atind)==0:
			continue


		AK4LV = []
		AK4array = []


		AK4_pt 		= 	treedict["AK4_pt"]
		AK4_eta 	= 	treedict["AK4_eta"]
		AK4_phi 	= 	treedict["AK4_phi"]
		AK4_M 		= 	treedict["AK4_M"]

		#print AK4_pt
		for iAK4 in xrange(len(AK4_pt)):

			if AK4_pt[iAK4]<0.:
				AK4LV.append(None)
				continue

			AK4LV.append(TLorentzVector())
			AK4LV[-1].SetPtEtaPhiM(AK4_pt[iAK4],AK4_eta[iAK4],AK4_phi[iAK4],AK4_M[iAK4])

			if (ptbcut[0]<AK4LV[iAK4].Perp()<ptbcut[1]) and abs(AK4LV[iAK4].Eta())<2.4:
				overlap=False
				for key in defs:
					if AK4LV[iAK4].DeltaR(AK8LV[defs[key]])<1.2:
						overlap=True
				if not overlap:
					AK4array.append(iAK4)



		correctindex = 9999
		bind= []
		abind= []
		AK4_btag 	= 	treedict["AK4_btag"]
		for AK4index in AK4array:

			if btag[0]<AK4_btag[AK4index]<btag[1]:
				bind.append(AK4index)
			else:
				abind.append(AK4index)
			


		if len(bind)>0:
			random.shuffle(bind)
			bind=[bind[0]]
			defs['b']=bind[0]
		if len(bind)==0 and len(abind)>0:
			random.shuffle(abind)
			abind=[abind[0]]
			defs['b']=abind[0]

		#print defs

		if len(defs)<3:
			continue 

		thb =  AK8LV[defs['t']] + AK8LV[defs['h']] + AK4LV[defs['b']]

		CurrTrigPlot  =  TrigPlot
		triggerweight = 1.0
		if options.set.find('data')==-1 and tnamestr!='none':


			triggerweight = WPF.Trigger_Lookup(AK4_ht,CurrTrigPlot)
			

			triggerweight = triggerweight[0]
			weight = weight*triggerweight*ptw*puweight*htagw

		if options.set.find('data')!=-1:
			if weight!=1.0:
				print "DATA WITH NON UNITY WEIGHT ", weight




		mindr = 999.0
		AK8defs = {}
		AK8defs['t'] = defs['t']
		AK8defs['h'] = defs['h']



		for aa in AK8defs:
			for bb in AK8defs:
				if aa!=bb:
					curdr = AK8LV[AK8defs[aa]].DeltaR(AK8LV[AK8defs[bb]])
					mindr = min(curdr,mindr)
					histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['DRs'].Fill(AK8LV[defs[aa]].DeltaR(AK8LV[defs[bb]]),weight)
		if mindr<1.8:
			continue 




		for aa in AK8defs:
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['DRAK4'].Fill(AK4LV[defs['b']].DeltaR(AK8LV[AK8defs[aa]]),weight)

		histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Mthb'].Fill(thb.M(),weight)
		histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Mh'].Fill(hJetMass[defs['h']],weight)
		histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Pth'].Fill(AK8LV[defs['h']].Perp(),weight)



		if options.set.find('QCD')!=-1:



	   			pflavsAK4 	= 	treedict["AK4_flav"]
	   			pflavsAK8 	= 	treedict["AK8_flav"]

				hflav = abs(pflavsAK8[defs['h']])
				tflav = abs(pflavsAK8[defs['t']])
				bflav = abs(pflavsAK4[defs['b']])
				#if len(hind)==1 and len(tind)==1 and len(bind)==0:

				

				histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['hflav'].Fill(hflav)
				histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['tflav'].Fill(tflav)
				histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['bflav'].Fill(bflav)

		if abs(AK8LV[defs['h']].Eta())<1.0:
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Pthe1'].Fill(AK8LV[defs['h']].Perp(),weight)
		else:
			histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Pthe2'].Fill(AK8LV[defs['h']].Perp(),weight)

		histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['Etah'].Fill(AK8LV[defs['h']].Eta(),weight)
		histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['PtEtah'].Fill(AK8LV[defs['h']].Perp(),AK8LV[defs['h']].Eta(),weight)

		histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]["bindex"].Fill(defs['b'],weight)
		histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]["tindex"].Fill(defs['t'],weight)
		histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]["hindex"].Fill(defs['h'],weight)

		#THE REST JUST FILLS THE DEBUG TREE

		ttau32 = tau32val[defs['t']]

		tmaxsjcsv = AK8CSVMAX[defs['t']]



		htau21 = tau21val[defs['h']]

		histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['ttau32'].Fill(ttau32,weight)
		histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['htau21'].Fill(htau21,weight)
		histosets["h"+str(len(hind))+"t"+str(len(tind))+"b"+str(len(bind))]['hdbtag'].Fill(jetAK8DoubleBAK8[defs['h']],weight)
		#if len(hind)==1 and len(tind)==1 and len(tind)==1:
		#	print "later ",jetAK8DoubleBAK8[defs['h']]


		if bkgTree and len(tind)==1:
		

			bkgtemp_variables = {
						"b_pt":AK4LV[defs['b']].Perp(),
						"m_thb":thb.M(),
						"m_bh":(AK8LV[defs['h']]+AK4LV[defs['b']]).M(),
						"m_th":(AK8LV[defs['h']]+AK8LV[defs['t']]).M(),
						"b_btag":bJetBDiscAK4[defs['b']],
						"t_pt":AK8LV[defs['t']].Perp(),
						"t_mass":topJetMassuncorr[defs['t']],
						"t_sjbtag":tmaxsjcsv,
						"t_tau32":ttau32,    
						"h_pt":AK8LV[defs['h']].Perp(),
						"h_mass":hJetMass[defs['h']],
						"h_dbtag":jetAK8DoubleBAK8[defs['h']],
						"h_tau21":htau21,    
						"hpass":len(hind),
						"bpass":len(bind)
					}



			for tv in bkgTree_vars.keys():
				bkgTree_vars[tv][0] = bkgtemp_variables[tv]
			bkgTree.Fill()



		#THE REST JUST FILLS THE DEBUG TREE
		if (len(hind) == 1) and (len(tind) == 1) and (len(bind)==1):


			#n11+=1
			#print, n11 , 	treedict["event"]

			temp_variables = {
						"b_pt":AK4LV[defs['b']].Perp(),
						"b_btag":bJetBDiscAK4[defs['b']],
						"t_pt":AK8LV[defs['t']].Perp(),
						"t_mass":topJetMassuncorr[defs['t']],
						"t_sjbtag":tmaxsjcsv,
						"t_tau32":ttau32,    
						"h_pt":AK8LV[defs['h']].Perp(),
						"h_mass":hJetMass[defs['h']],
						"h_dbtag":jetAK8DoubleBAK8[defs['h']],
						"h_tau21":htau21,    
						"weight":weight
					}


			for tv in tree_vars.keys():
				tree_vars[tv][0] = temp_variables[tv]
			fullselTree.Fill()



    numtree += 1

f.cd()
fullnev.Write()
f.Write()
f.Close()

print "number of events: " + str(count)


