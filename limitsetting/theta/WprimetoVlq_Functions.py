
###################################################################
##								 ##
## Name: WPrime_Functions.py	   			         ##
## Author: Kevin Nash 						 ##
## Date: 5/13/2015						 ##
## Purpose: This contains all functions used by the              ##
##	    analysis.  A method is generally placed here if 	 ##
##	    it is called more than once in reproducing all	 ##
##	    analysis results.  The functions contained here 	 ##
##	    Are capable of tuning the analysis - such as changing##
##	    cross sections, updating lumi, changing file	 ##
##	    locations, etc. with all changes propegating 	 ##
##	    to all relevant files automatically.  		 ##
##								 ##
###################################################################

import cppyy
import copy
import os
import array
import glob
import math
import ROOT
import sys
import math
import random
random.seed(123456) 
from math import sqrt
from array import *

from ROOT import TLorentzVector,TH1F,TH1D,TH2F,TLine,TArrow,TTree,TFile,gROOT,TLegend,TCanvas,kYellow,kRed,kBlue,kGreen,gPad,TLatex,TFormula,TGraph,gROOT,TF1
from DataFormats.FWLite import Events, Handle, Runs
#This is the most impostant Function.  Correct information here is essential to obtaining valid results.
#In order we have Luminosity, top tagging scale factor, cross sections for wprime right,left,mixed,ttbar,qcd, and singletop and their corresponding event numbers
#If I wanted to access the left handed W' cross section at 1900 GeV I could do Xsecl1900 = LoadConstants()['xsec_wpl']['1900']
class WprimetoVlq_Functions:
	def __init__(self,TYPE,jetcoll='Puppi',module=''):
		self.LoadConstants =  {	
				'lumi':35867.1,
				'kfac':1.0,
				#---EVAL AS 23*EXP(0.00237x)--- 'xsec_wpr':{'1500':0.710,'2000':0.190,'2500':0.0570,'3000':0.019,'3500':0.006},
				'xsec_wpr':{'1500':0.56,'2000':0.135,'2500':0.0389,'3000':0.0123,'3500':0.00416,'4000':0.00144},
				#'xsec_wpl':{'1400': 0.},
				#'xsec_wplr':{'1400': 0.},
				'xsec_ttbar':{'PH':831.76,'PHscaleup':831.76,'PHscaledown':831.76,'mtt700':76.61,'mtt1000':20.58 },
				'xsec_qcd':{'HT500':31630,'HT700':6802,'HT1000':1206,'HT1500':120.4,'HT2000':25.25},
				'xsec_st':{'TW':35.85,'TWB':35.85},
				'xsec_wjets':{'HT600':95.14},
				'nev_wpr':{'1000':1},
				'nev_wpl':{'2000':1},
				'nev_wplr':{'2000':1},
				'nev_wjets':{'HT600':1008034},
				'nev_ttbar':{'PH':180037820,'PHscaleup':9933327,'PHscaledown':9942427},
				'nev_qcd':{'HT500':44058594,'HT700':15020802,'HT1000':4980387,'HT1500':3846616,'HT2000':1680210},
				'nev_st':{'TW':998400 ,'TWB':985000},
				}



	 	self.LoadCuts =  {
				'ptmincut':[300.,float("inf")],
				'pthcut':[300.,float("inf")],
				'pttcut':[400.,float("inf")],
				'ptbcut':[200.,float("inf")],
				'tmass':[105.0,210.0],
				'tau32':[0.0,0.8],
				'tau32tight':[0.0,0.54],
				'sjbtagt':[0.5426,1.0],
				'tmassinvert':[30.0,105.0],
				'tau32invert':[0.65,1.0],
				'sjbtagtinvert':[0.5426,1.0],
				'sbtmass':[30.0,105.0],
				'sbtau32':[0.65,1.0],
				'sbsjbtagt':[0.5426,1.0],
				'sjbtagh':[0.8,1.0],
				'sjbtaghloose':[0.3,1.0],
				'bmass':[0.0,80.0],
				'btag':[0.5426,1.0],
				'hmass':[105.0,135.0],
				'hmassinvert':[0.0,30.0],
				'tau21':[0.0,1.0]
				}

		if TYPE=='tau32_3':
			self.LoadCuts['tau32']=[0.0,0.65]

		if TYPE=='tau32_2':
			self.LoadCuts['tau32']=[0.0,0.54]

		if TYPE=='tau32_1':
			self.LoadCuts['tau32']=[0.0,0.46]

		if TYPE=='sjbtagt_0':
			self.LoadCuts['sjbtagt']=[-1*float("inf"),float("inf")]

		if TYPE=='sjbtagt_2':
			self.LoadCuts['sjbtagt']=[0.8484,1.0]


		if TYPE=='sjbtagh_1':
			self.LoadCuts['sjbtagt']=[0.3,1.0]

		if TYPE=='sjbtagh_2':
			self.LoadCuts['sjbtagt']=[0.6,1.0]

		if TYPE=='sjbtagh_4':
			self.LoadCuts['sjbtagt']=[0.9,1.0]




		if TYPE=='btag_2':
			self.LoadCuts['btag']=[0.8484,1.0]

		if TYPE=='btag_3':
			self.LoadCuts['btag']=[0.9535,1.0]


		self.sigmasses = 	{
				'1500':['800','1000','1300'],
				'2000':['1000','1300','1500'],
				'2500':['1300','1500','1800'],
				'3000':['1500','1800','2100'],
				'3500':['1800','2100','2500'],
				'4000':['2100','2500','3000']
				}

		self.sigmasses = 	{
					'1500':['800','1000','1300'],
					'2000':['1000','1300','1500'],
					'2500':['1300','1500','1800'],
					'3000':['1500','1800','2100'],
					'3500':['1800','2100','2500'],
					'4000':['2100','2500','3000']
					}

		self.sigBR = 		{
					'1500':[0.169757,0.430023,0.145605],
					'2000':[0.154239,0.446878,0.329075],
					'2500':[0.161456,0.491523,0.368732],
					'3000':[0.154239,0.491523,0.393075],
					'3500':[0.158903,0.491523,0.375857],
					'4000':[0.164126,0.470263,0.329075]
					}

		massmod = ""
		ptmod = ""
		if module.find("M")!=-1:
			massmod=module.replace("M","")
		else:	
			ptmod=module	

		self.elPtHandle 	= 	Handle (  "vector<float> "  )
		self.elPtLabel  	= 	( "electrons" , "elPt")
	
		self.muIsMediumMuonHandle 	= 	Handle (  "vector<float> "  )
		self.muIsMediumMuonLabel  	= 	( "muons" , "muIsMediumMuon")


		self.muPtHandle 	= 	Handle (  "vector<float> "  )
		self.muPtLabel  	= 	( "muons" , "muPt")

		#self.metFullPtHandle 	= 	Handle (  "vector<float> "  )
		#self.metFullPtLabel  	= 	( "metFull" , "metFullPt")


		self.DijetBitHandle 	= 	Handle (  "vector<bool>"  )
		self.DijetBitLabel  	= 	( "Filter" , "DijetBit")


		self.JET260bitHandle 	= 	Handle (  "vector<bool>"  )
		self.JET260bitLabel  	= 	( "Filter" , "JET260bit")

		self.JET450bitHandle 	= 	Handle (  "vector<bool>"  )
		self.JET450bitLabel  	= 	( "Filter" , "JET450bit")

		self.HT475bitHandle 	= 	Handle (  "vector<bool>"  )
		self.HT475bitLabel  	= 	( "Filter" , "HT475bit")

		self.HT800bitHandle 	= 	Handle (  "vector<bool>"  )
		self.HT800bitLabel  	= 	( "Filter" , "HT800bit")

		self.HT900bitHandle 	= 	Handle (  "vector<bool>"  )
		self.HT900bitLabel  	= 	( "Filter" , "HT900bit")


		self.Triggermap = {}
		self.Triggermap['HLT_PFHT900'] = [self.HT900bitLabel,self.HT900bitHandle]
		self.Triggermap['HLT_PFHT800'] = [self.HT800bitLabel,self.HT800bitHandle]
		self.Triggermap['HLT_PFHT475'] = [self.HT475bitLabel,self.HT475bitHandle]
		self.Triggermap['HLT_JET450'] = [self.JET450bitLabel,self.JET450bitHandle]
		self.Triggermap['HLT_JET260'] = [self.JET260bitLabel,self.JET260bitHandle]


		self.PtnomHandle 	= 	Handle (  "vector<float> "  )
		self.PtnomLabel  	= 	( "jetsAK8"  , "jetAK8"+jetcoll+"Pt")


		self.EtanomHandle 	= 	Handle (  "vector<float> "  )
		self.EtanomLabel  	= 	( "jetsAK8"  , "jetAK8"+jetcoll+"Eta")


		self.PhinomHandle 	= 	Handle (  "vector<float> "  )
		self.PhinomLabel  	= 	( "jetsAK8"  , "jetAK8"+jetcoll+"Phi")


		self.MassnomHandle 	= 	Handle (  "vector<float> "  )
		self.MassnomLabel  	= 	( "jetsAK8"  , "jetAK8"+jetcoll+"Mass")




		self.PtAK4nomHandle 	= 	Handle (  "vector<float> "  )
		self.PtAK4nomLabel  	= 	( "jetsAK4"  , "jetAK4"+jetcoll+"Pt")


		self.EtaAK4nomHandle 	= 	Handle (  "vector<float> "  )
		self.EtaAK4nomLabel  	= 	( "jetsAK4"  , "jetAK4"+jetcoll+"Eta")


		self.PhiAK4nomHandle 	= 	Handle (  "vector<float> "  )
		self.PhiAK4nomLabel  	= 	( "jetsAK4"  , "jetAK4"+jetcoll+"Phi")


		self.MassAK4nomHandle 	= 	Handle (  "vector<float> "  )
		self.MassAK4nomLabel  	= 	( "jetsAK4"  , "jetAK4"+jetcoll+"Mass")






		self.BDiscHandle 	= 	Handle (  "vector<float> "  )
		self.BDiscLabel  	= 	( "jetsAK8"  , "jetAK8"+jetcoll+"CSV")



		self.PtjesupHandle 	= 	Handle (  "vector<float> "  )
		self.PtjesupLabel  	= 	( "jetsAK8jesup"  , "jetAK8"+jetcoll+"Pt")

		self.PtjesdownHandle 	= 	Handle (  "vector<float> "  )
		self.PtjesdownLabel  	= 	( "jetsAK8jesdown"  , "jetAK8"+jetcoll+"Pt")




		self.PtjerupHandle 	= 	Handle (  "vector<float> "  )
		self.PtjerupLabel  	= 	( "jetsAK8jerup"  , "jetAK8"+jetcoll+"Pt")

		self.PtjerdownHandle 	= 	Handle (  "vector<float> "  )
		self.PtjerdownLabel  	= 	( "jetsAK8jerdown"  , "jetAK8"+jetcoll+"Pt")






		self.PtAK4jesupHandle 	= 	Handle (  "vector<float> "  )
		self.PtAK4jesupLabel  	= 	( "jetsAK4jesup"  , "jetAK4"+jetcoll+"Pt")

		self.PtAK4jesdownHandle 	= 	Handle (  "vector<float> "  )
		self.PtAK4jesdownLabel  	= 	( "jetsAK4jesdown"  , "jetAK4"+jetcoll+"Pt")




		self.PtAK4jerupHandle 	= 	Handle (  "vector<float> "  )
		self.PtAK4jerupLabel  	= 	( "jetsAK4jerup"  , "jetAK4"+jetcoll+"Pt")

		self.PtAK4jerdownHandle 	= 	Handle (  "vector<float> "  )
		self.PtAK4jerdownLabel  	= 	( "jetsAK4jerdown"  , "jetAK4"+jetcoll+"Pt")







		self.BDiscAK4Handle 	= 	Handle (  "vector<float> "  )
		self.BDiscAK4Label  	= 	( "jetsAK4"  , "jetAK4"+jetcoll+"CSV")


		self.GeneratorHandle 	= 	Handle (  "GenEventInfoProduct")
		self.GeneratorLabel  	= 	( "generator" , "")

		self.puHandle    	= 	Handle("int")
		self.puLabel     	= 	( "eventUserData", "puNtrueInt" )


		self.pdfHandleNOM 	= 	Handle (  "vector<float> "  )
		self.pdfLabelNOM  	= 	( "weights" , "pdfWeights")

		self.pdfHandleNNPDF 	= 	Handle (  "vector<float>"  )
		self.pdfLabelNNPDF  	= 	( "weights" , "pdfWeightsNNPDF")

		self.partonFlavourHandle 	= 	Handle (  "vector<float> "  )
		self.partonFlavourLabel  	= 	( "jetsAK8"  , "jetAK8"+jetcoll+"PartonFlavour")


		self.partonFlavourAK4Handle 	= 	Handle (  "vector<float> "  )
		self.partonFlavourAK4Label  	= 	( "jetsAK4"  , "jetAK4"+jetcoll+"PartonFlavour")



		self.hadronFlavourAK4Handle 	= 	Handle (  "vector<float> "  )
		self.hadronFlavourAK4Label  	= 	( "jetsAK4"  , "jetAK4"+jetcoll+"HadronFlavour")





		self.softDropMassHandle 	= 	Handle (  "vector<float> "  )
		self.softDropMassLabel  	= 	( "jetsAK8" +  massmod , "jetAK8"+jetcoll+"CorrectedsoftDropMass")




		self.softDropMassjerupHandle 	= 	Handle (  "vector<float> "  )
		self.softDropMassjerupLabel  	= 	( "jetsAK8jerup" +  massmod , "jetAK8"+jetcoll+"CorrectedsoftDropMass")



		self.softDropMassjerdownHandle 	= 	Handle (  "vector<float> "  )
		self.softDropMassjerdownLabel  	= 	( "jetsAK8jerdown" +  massmod , "jetAK8"+jetcoll+"CorrectedsoftDropMass")



		self.softDropMassjesupHandle 	= 	Handle (  "vector<float> "  )
		self.softDropMassjesupLabel  	= 	( "jetsAK8jesup" +  massmod , "jetAK8"+jetcoll+"CorrectedsoftDropMass")



		self.softDropMassjesdownHandle 	= 	Handle (  "vector<float> "  )
		self.softDropMassjesdownLabel  	= 	( "jetsAK8jesdown" +  massmod , "jetAK8"+jetcoll+"CorrectedsoftDropMass")






		self.tau1Handle 	= 	Handle (  "vector<float> "  )
		self.tau1Label  	= 	( "jetsAK8"  , "jetAK8"+jetcoll+"tau1")

		self.tau2Handle 	= 	Handle (  "vector<float> "  )
		self.tau2Label  	= 	( "jetsAK8"  , "jetAK8"+jetcoll+"tau2")

		self.tau3Handle 	= 	Handle (  "vector<float> "  )
		self.tau3Label  	= 	( "jetsAK8"  , "jetAK8"+jetcoll+"tau3")

		self.topMassHandle 	= 	Handle (  "vector<float> "  )
		self.topMassLabel  	= 	( "jetsAK8"  , "jetAK8"+jetcoll+"topMass")

		self.subjetsCSVHandle 	= 	Handle (  "vector<float> "  )
		self.subjetsCSVLabel  	= 	( "subjetsCmsTopTag" , "subjetCmsTopTagCSV")


		self.softDropMassuncorrHandle 	= 	Handle (  "vector<float> "  )
		self.softDropMassuncorrLabel  	= 	( "jetsAK8" +  ptmod , "jetAK8"+jetcoll+"softDropMassForTopPUPPIAK8JEC")

		self.vsubjets0indexHandle 	= 	Handle (  "vector<float> "  )
		self.vsubjets0indexLabel  	= 	( "jetsAK8"  , "jetAK8"+jetcoll+"vSubjetIndex0")

		self.vsubjets1indexHandle 	= 	Handle (  "vector<float> "  )
		self.vsubjets1indexLabel  	= 	( "jetsAK8"  , "jetAK8"+jetcoll+"vSubjetIndex1")

		self.jetAK8DoubleBAK8Handle 	= 	Handle (  "vector<float> "  )
		self.jetAK8DoubleBAK8Label  	= 	("jetsAK8"  , "jetAK8"+jetcoll+"DoubleBAK8")




		self.subjetsAK8CSVHandle 	= 	Handle (  "vector<float> "  )
		self.subjetsAK8CSVLabel  	= 	( "subjetsAK8"+jetcoll+"" ,"subjetAK8"+jetcoll+"CSVv2")


		self.nevHandle 	= 	Handle (  "vector<int> "  )
		self.nevLabel  	= 	( "counter" , "nevr")


		self.filtersbitHandle 	= 	Handle (  "vector<bool>"  )
		self.filtersbitLabel  	= 	( "Filter" , "filtersbit")



		self.TightHandle 	= 	Handle ( "vector<float>"  )
		self.TightLabel  	= 	( "jetsAK8" , "jetAK8"+jetcoll+"Tight")


		self.LooseHandle 	= 	Handle ( "vector<float>"  )
		self.LooseLabel  	= 	( "jetsAK8" , "jetAK8"+jetcoll+"Loose")





		self.TightAK4Handle 	= 	Handle ( "vector<float>"  )
		self.TightAK4Label  	= 	( "jetsAK4" , "jetAK4"+jetcoll+"Tight")


		self.LooseAK4Handle 	= 	Handle ( "vector<float>"  )
		self.LooseAK4Label  	= 	( "jetsAK4" , "jetAK4"+jetcoll+"Loose")




		self.GenHandle 	= 	Handle (  "vector<reco::GenParticle>")
		self.GenLabel  	= 	( "filteredPrunedGenParticles" , "")
	

		self.Q2Handle 	= 	Handle (  "vector<float>")
		self.Q2Label  	= 	( "weights" , "Q2Weights")
	
	

		self.AsHandle 	= 	Handle (  "vector<float>")
		self.AsLabel  	= 	( "weights" , "alphasWeights")
	






	def select(self,indices):
		hrems = []
		trems = []
		

		newindices = [copy.copy(indices[0]),copy.copy(indices[1])]
		if len(indices[0])>0 and len(indices[1])>0:
			for i in range(0,len(indices[0])):
				for j in range(0,len(indices[1])):
					if indices[0][i]==indices[1][j]:
						trems.append(indices[1][j])
						

			for h in hrems:
				newindices[0].remove(h)
			for t in trems:
				newindices[1].remove(t)
	
		return newindices[0],newindices[1]
	


	def Inittree(self,curTree):		

		treedict = {}
		for leaf in curTree.GetListOfLeaves():		
			treedict[leaf.GetName()]=array('d', [0]*leaf.GetLen())
			curTree.SetBranchAddress(str(leaf.GetName()), treedict[leaf.GetName()])
		return treedict



	def Load_Ntuples(self,string,di='',istree=False):
		print 'running on ' + string 
		treestring = ''
		if istree:
			treestring = 'TTree'
		if di!='':
			files=open(di+'Files_'+treestring+string+'.txt').readlines()
			for i in range(0,len(files)):
				files[i] = files[i].replace('/eos/uscms','root://cmsxrootd.fnal.gov//').replace('\n','')

			try:
				print 'A total of ' + str(len(files)) + ' files'
			except:
				print 'Bad files option'
			return files
		if istree:
			files = glob.glob("/eos/uscms//store/user/knash/TTrees/THBttree"+string+"*.root")

		else:

			if string == 'ttbar':
				files = glob.glob("/eos/uscms/store/group/lpcrutgers/knash/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/crab_TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_Slim_V12/*/*/*.root")

			if string == 'ttbar_mtt700':
				files = glob.glob("/eos/uscms/store/group/lpcrutgers/knash/TT_Mtt-700to1000_TuneCUETP8M2T4_13TeV-powheg-pythia8/crab_TT_Mtt-700to1000_TuneCUETP8M2T4_13TeV-powheg-pythia8_Slim_V14/*/*/*.root")
			if string == 'ttbar_mtt1000':
				files = glob.glob("/eos/uscms/store/group/lpcrutgers/knash/TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8/crab_TT_Mtt-1000toInf_TuneCUETP8M2T4_13TeV-powheg-pythia8_Slim_V14/*/*/*.root")

			if string == 'ttbarscaleup':
				files = glob.glob("")
			if string == 'ttbarscaledown':
				files = glob.glob("")

			if string == 'QCDHT500':
				files = glob.glob("/eos/uscms/store/group/lpcrutgers/knash/QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_Slim_V12/*/*/*.root")
			if string == 'QCDHT700':
				files = glob.glob("/eos/uscms/store/group/lpcrutgers/knash/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_Slim_V12/*/*/*.root")
				files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT700to1000_EXT1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_Slim_V12/*/*/*.root")
			if string == 'QCDHT1000':
				files = glob.glob("/eos/uscms/store/group/lpcrutgers/knash/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_Slim_V12/*/*/*.root")
				files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT1000to1500_EXT1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_Slim_V12/171031_212316/0000/*.root")

			if string == 'QCDHT1500':
				files = glob.glob("/eos/uscms/store/group/lpcrutgers/knash/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_Slim_V12/*/*/*.root")
				files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT1500to2000_EXT1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_Slim_V12/171031_211529/0000/*.root")

			if string == 'QCDHT2000':
				files = glob.glob("/eos/uscms/store/group/lpcrutgers/knash/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_Slim_V12/*/*/*.root")
				files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_QCD_HT2000toInf_EXT1_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_Slim_V12/171031_211559/0000/*.root")

			if string == 'data':

				files = glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016B-03Feb2017-v3_B2GAnaFW_80X_V2p3_Slim_V12/*/*/*.root")
				files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016C-03Feb2017-v1_B2GAnaFW_80X_V2p3_Slim_V12/*/*/*.root")
				files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016D-03Feb2017-v1_B2GAnaFW_80X_V2p3_Slim_V12/*/*/*.root")
				files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016E-03Feb2017-v1_B2GAnaFW_80X_V2p3_Slim_V12/*/*/*.root")
				files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016F-03Feb2017-v1_B2GAnaFW_80X_V2p3_Slim_V12/*/*/*.root")
				files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016G-03Feb2017-v1_B2GAnaFW_80X_V2p3_Slim_V12/*/*/*.root")
				files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016H-03Feb2017_ver2-v1_B2GAnaFW_80X_V2p3_Slim_V12/*/*/*.root")
				files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016H-03Feb2017_ver3-v1_B2GAnaFW_80X_V2p3_Slim_V12/*/*/*.root")



			if string == 'datanoH':

				files = glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016B-03Feb2017-v3_B2GAnaFW_80X_V2p3_Slim_V12/*/*/*.root")
				files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016C-03Feb2017-v1_B2GAnaFW_80X_V2p3_Slim_V12/*/*/*.root")
				files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016D-03Feb2017-v1_B2GAnaFW_80X_V2p3_Slim_V12/*/*/*.root")
				files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016E-03Feb2017-v1_B2GAnaFW_80X_V2p3_Slim_V12/*/*/*.root")
				files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016F-03Feb2017-v1_B2GAnaFW_80X_V2p3_Slim_V12/*/*/*.root")
				files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016G-03Feb2017-v1_B2GAnaFW_80X_V2p3_Slim_V12/*/*/*.root")




			if string == 'dataH':
				files = glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016H-03Feb2017_ver2-v1_B2GAnaFW_80X_V2p3_Slim_V12/*/*/*.root")
				files += glob.glob("/eos/uscms/store/group/lpcrutgers/knash/JetHT/crab_JetHT_Run2016H-03Feb2017_ver3-v1_B2GAnaFW_80X_V2p3_Slim_V12/*/*/*.root")

			if string.find('THBWp')!=-1:
				
			
			

				print "str ", string
				fstring = string.replace('THBWp','')
				print "fstr ", fstring
				strWPM = fstring[0:4]
				print "WPm ", strWPM

				strTPM = fstring.replace(strWPM,'')
				VLQ = strTPM[0]+strTPM[1]

				print "TPT ", VLQ

				if VLQ=="Tp":
					AQ = "B"
				if VLQ=="Bp":
					AQ = "T"

				strTPM = strTPM.replace(VLQ,'')

				print "AQ ", AQ
				print "TPM ", strTPM

				Recons_name = "WpTo"+VLQ+AQ+"_Wp"+strWPM+"Nar_"+VLQ+strTPM+"NarLH"
				print "reco name " , Recons_name
				full_name = "/eos/uscms/store/group/lpcrutgers/knash/"+Recons_name+"_Ht_HTobb_TuneCUETP8M2T4_13TeV-madgraphMLM-pythia8/crab_"+Recons_name+"_Slim_V14/*/*/*.root"
				print "full name " , full_name 
		 		files = glob.glob(full_name)



		for i in range(0,len(files)):
			files[i] = files[i].replace('/eos/uscms','root://cmsxrootd.fnal.gov//')

		try:
			print 'A total of ' + str(len(files)) + ' files'
		except:
			print 'Bad files option'
		return files




	#This function initializes the average b tagging rates used for QCD determination
	#It tages the type of functional form as an argument.  The default fit is Bifpoly





	def BTR_Init(self,ST,CUT,di,setval):

		if setval.find("QCD")==-1:
			setval = "data"


		if ST == 'Bifpoly':
			TRBPE1 = open("./"+di+"fitdata/bpinput"+setval+"eta1_PSET_"+CUT+".txt")
			TRBPE1.seek(0)
			TRBPE2 = open("./"+di+"fitdata/bpinput"+setval+"eta2_PSET_"+CUT+".txt")
			TRBPE2.seek(0)
			TRBPE3 = open("./"+di+"fitdata/bpinput"+setval+"eta3_PSET_"+CUT+".txt")
			TRBPE3.seek(0)
			eta1fit = TF1("eta1fit",BifPoly,0,2000,5)
			eta2fit = TF1("eta2fit",BifPoly,0,2000,5)
			eta3fit = TF1("eta3fit",BifPoly,0,2000,5)
			Params = 5
		if ST == 'Bifpoly_err':
			TRBPE1 = open("./"+di+"fitdata/bperrorinput"+setval+"eta1_PSET_"+CUT+".txt")
			TRBPE1.seek(0)
			TRBPE2 = open("./"+di+"fitdata/bperrorinput"+setval+"eta2_PSET_"+CUT+".txt")
			TRBPE2.seek(0)
			TRBPE3 = open("./"+di+"fitdata/bperrorinput"+setval+"eta3_PSET_"+CUT+".txt")
			TRBPE3.seek(0)
			eta1fit=TF1("eta1fit",BifPolyErr,0,2000,10)
			eta2fit=TF1("eta2fit",BifPolyErr,0,2000,10)
			eta3fit=TF1("eta3fit",BifPolyErr,0,2000,10)
			Params = 10

		if ST == 'pol0':
			TRBPE1 = open("./"+di+"fitdata/pol0input"+setval+"eta1_PSET_"+CUT+".txt")
			TRBPE1.seek(0)
			TRBPE2 = open("./"+di+"fitdata/pol0input"+setval+"eta2_PSET_"+CUT+".txt")
			TRBPE2.seek(0)
			TRBPE3 = open("./"+di+"fitdata/pol0input"+setval+"eta3_PSET_"+CUT+".txt")
			TRBPE3.seek(0)
			eta1fit = TF1("eta1fit",'pol0',0,2000)
			eta2fit = TF1("eta2fit",'pol0',0,2000)
			eta3fit = TF1("eta3fit",'pol0',0,2000)
			Params = 1

		if ST == 'pol2':
			TRBPE1 = open("./"+di+"fitdata/pol2input"+setval+"eta1_PSET_"+CUT+".txt")
			TRBPE1.seek(0)
			TRBPE2 = open("./"+di+"fitdata/pol2input"+setval+"eta2_PSET_"+CUT+".txt")
			TRBPE2.seek(0)
			TRBPE3 = open("./"+di+"fitdata/pol2input"+setval+"eta3_PSET_"+CUT+".txt")
			TRBPE3.seek(0)
			eta1fit = TF1("eta1fit",'pol2',0,2000)
			eta2fit = TF1("eta2fit",'pol2',0,2000)
			eta3fit = TF1("eta3fit",'pol2',0,2000)
			Params = 3

		if ST == 'pol3':
			TRBPE1 = open("./"+di+"fitdata/pol3input"+setval+"eta1_PSET_"+CUT+".txt")
			TRBPE1.seek(0)
			TRBPE2 = open("./"+di+"fitdata/pol3input"+setval+"eta2_PSET_"+CUT+".txt")
			TRBPE2.seek(0)
			TRBPE3 = open("./"+di+"fitdata/pol3input"+setval+"eta3_PSET_"+CUT+".txt")
			TRBPE3.seek(0)
			eta1fit = TF1("eta1fit",'pol3',0,2000)
			eta2fit = TF1("eta2fit",'pol3',0,2000)
			eta3fit = TF1("eta3fit",'pol3',0,2000)
			Params = 4
		if ST == 'FIT':
			TRBPE1 = open("./"+di+"fitdata/newfitinput"+setval+"eta1_PSET_"+CUT+".txt")
			TRBPE1.seek(0)
			TRBPE2 = open("./"+di+"fitdata/newfitinput"+setval+"eta2_PSET_"+CUT+".txt")
			TRBPE2.seek(0)
			TRBPE3 = open("./"+di+"fitdata/newfitinput"+setval+"eta3_PSET_"+CUT+".txt")
			TRBPE3.seek(0)
			eta1fit = TF1("eta1fit",'[0]*([1]+x)/([2]+x)+[3]*x',0,2000)
			eta2fit = TF1("eta2fit",'[0]*([1]+x)/([2]+x)+[3]*x',0,2000)
			eta3fit = TF1("eta3fit",'[0]*([1]+x)/([2]+x)+[3]*x',0,2000)
			Params = 4
		if ST == 'expofit':
			TRBPE1 = open("./"+di+"fitdata/expoconinput"+setval+"eta1_PSET_"+CUT+".txt")
			TRBPE1.seek(0)
			TRBPE2 = open("./"+di+"fitdata/expoconinput"+setval+"eta2_PSET_"+CUT+".txt")
			TRBPE2.seek(0)
			TRBPE3 = open("./"+di+"fitdata/expoconinput"+setval+"eta3_PSET_"+CUT+".txt")
			TRBPE3.seek(0)
			eta1fit = TF1("eta1fit",'expo(0) + pol0(2)',0,2000)
			eta2fit = TF1("eta2fit",'expo(0) + pol0(2)',0,2000)
			eta3fit = TF1("eta3fit",'expo(0) + pol0(2)',0,2000)
			Params = 3

		TBP1 = TRBPE1.read()
		TBP2 = TRBPE2.read()
		TBP3 = TRBPE3.read()
	
		for i in range(0,Params):

			eta1fit.SetParameter(i,float(TBP1.split('\n')[i]) )
			eta2fit.SetParameter(i,float(TBP2.split('\n')[i]) )
			eta3fit.SetParameter(i,float(TBP3.split('\n')[i]) )

		return [eta1fit.Clone(),eta2fit.Clone(),eta3fit.Clone()] 

	#This takes the average b tagging rates that are initialized in the above function and produces 
	#A QCD background estimate based on them 
	def bkg_weight(self,blv, funcs, etabins):
		for ibin in range(0,len(etabins)):
			if (etabins[ibin][0] <= abs(blv.Eta()) < etabins[ibin][1]) :
				tagratept = funcs[ibin].Eval(blv.Perp())	

		try :
			return tagratept
		except :
			print blv.Eta()
			tagratept=0.0	

	#This is the bifurcated polynomial function and its associated uncertainty 
	def BifPoly(self, x, p ):
		xx=x[0]
		if xx<p[4]:
	      		return p[0]+p[1]*xx+p[2]*(xx-p[4])**2
		else:
			return p[0]+p[1]*xx+p[3]*(xx-p[4])**2
	def BifPolyErr(self, x, p ):
		xx=x[0]
		if xx<p[9]:
	      		return p[0]+p[1]*xx**2+p[2]*(xx-p[9])**4+p[3]*xx+p[4]*(xx-p[9])**2+p[5]*xx*(xx-p[9])**2
		else:
			return p[0]+p[1]*xx**2+p[6]*(xx-p[9])**4+p[3]*xx+p[7]*(xx-p[9])**2+p[8]*xx*(xx-p[9])**2

	#This is the first in a series of functions used to extract Monte Carlo to data scale factors and their uncertainty 
	#This looks up the b tagging scale factor 
	def SFB_Lookup(self, Y,HF ):


		weightSFb,weightSFb_down,weightSFb_up  =  1.0,1.0,1.0
		#print [weightSFb,weightSFb_down,weightSFb_up]
		ptminsfb = [100.0,140.0,200.0,300.0,600.0,]
		ptmaxsfb = [140.0,200.0,300.0,600.0,1000.0,]
	

		if HF==5:

			SFb = TFormula("SFb","0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x)))")
			SFb_down =	[
					TFormula("SFb_down_1","(0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x))))-0.010811596177518368"),	 				TFormula("SFb_down_2","(0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x))))-0.010882497765123844"), 	 				TFormula("SFb_down_3","(0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x))))-0.013456921093165874"), 	 				TFormula("SFb_down_4","(0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x))))-0.017094610258936882"), 	 				TFormula("SFb_down_5","(0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x))))-0.02186630479991436") 
					]

			SFb_up =	[	 				TFormula("SFb_up_1","(0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x))))+0.010811596177518368"), 	 				TFormula("SFb_up_2","(0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x))))+0.010882497765123844"), 	 				TFormula("SFb_up_3","(0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x))))+0.013456921093165874"), 	 				TFormula("SFb_up_4","(0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x))))+0.017094610258936882"), 	 				TFormula("SFb_up_5","(0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x))))+0.02186630479991436") 
					]
		elif HF==4:
			SFb = TFormula("SFb","0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x)))")
			SFb_down =	[
					TFormula("SFb_down_1","(0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x))))-0.027028990909457207"),	 				TFormula("SFb_down_2","(0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x))))-0.027206243947148323"), 	 				TFormula("SFb_down_3","(0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x))))-0.033642303198575974"), 	 				TFormula("SFb_down_4","(0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x))))-0.04273652657866478"), 	 				TFormula("SFb_down_5","(0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x))))-0.054665762931108475") 
					]


			SFb_up =	[	 				TFormula("SFb_up_1","(0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x))))+0.027028990909457207"), 	 				TFormula("SFb_up_2","(0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x))))+0.027206243947148323"), 	 				TFormula("SFb_up_3","(0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x))))+0.033642303198575974"), 	 				TFormula("SFb_up_4","(0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x))))+0.04273652657866478"), 	 				TFormula("SFb_up_5","(0.887973*((1.+(0.0523821*x))/(1.+(0.0460876*x))))+0.054665762931108475") 
					]

		else:
			SFb = TFormula("SFb","1.13904+-0.000594946*x+1.97303e-06*x*x+-1.38194e-09*x*x*x")
			SFb_down =	[
					TFormula("SFb_down_1","(1.13904+-0.000594946*x+1.97303e-06*x*x+-1.38194e-09*x*x*x)*(1-(0.0996438+-8.33354e-05*x+4.74359e-08*x*x))"),	 				TFormula("SFb_down_2","(1.13904+-0.000594946*x+1.97303e-06*x*x+-1.38194e-09*x*x*x)*(1-(0.0996438+-8.33354e-05*x+4.74359e-08*x*x))"), 	 				TFormula("SFb_down_3","(1.13904+-0.000594946*x+1.97303e-06*x*x+-1.38194e-09*x*x*x)*(1-(0.0996438+-8.33354e-05*x+4.74359e-08*x*x))"), 	 				TFormula("SFb_down_4","(1.13904+-0.000594946*x+1.97303e-06*x*x+-1.38194e-09*x*x*x)*(1-(0.0996438+-8.33354e-05*x+4.74359e-08*x*x))"), 	 				TFormula("SFb_down_5","(1.13904+-0.000594946*x+1.97303e-06*x*x+-1.38194e-09*x*x*x)*(1-(0.0996438+-8.33354e-05*x+4.74359e-08*x*x))") 
					]


			SFb_up =	[	 				TFormula("SFb_up_1","(1.13904+-0.000594946*x+1.97303e-06*x*x+-1.38194e-09*x*x*x)*(1+(0.0996438+-8.33354e-05*x+4.74359e-08*x*x))"), 	 				TFormula("SFb_up_2","(1.13904+-0.000594946*x+1.97303e-06*x*x+-1.38194e-09*x*x*x)*(1+(0.0996438+-8.33354e-05*x+4.74359e-08*x*x))"), 	 				TFormula("SFb_up_3","(1.13904+-0.000594946*x+1.97303e-06*x*x+-1.38194e-09*x*x*x)*(1+(0.0996438+-8.33354e-05*x+4.74359e-08*x*x))"), 	 				TFormula("SFb_up_4","(1.13904+-0.000594946*x+1.97303e-06*x*x+-1.38194e-09*x*x*x)*(1+(0.0996438+-8.33354e-05*x+4.74359e-08*x*x))"), 	 				TFormula("SFb_up_5","(1.13904+-0.000594946*x+1.97303e-06*x*x+-1.38194e-09*x*x*x)*(1+(0.0996438+-8.33354e-05*x+4.74359e-08*x*x))") 
					]

		#print "Checking b tag SF"
		#print "at pt ",Y
		if Y <= 1000.0:
			weightSFb  = SFb.Eval(Y)
			for iptrange in range(0,len(ptminsfb)):
				if ptminsfb[iptrange]<Y<=ptmaxsfb[iptrange]:
					weightSFb_down = SFb_down[iptrange].Eval(Y)
					weightSFb_up = SFb_up[iptrange].Eval(Y)	
					#print "eval at i=",iptrange
					#print "pr range ",ptminsfb[iptrange]," - ",ptmaxsfb[iptrange]
					break
		else: 
			weightSFb  = SFb.Eval(1000.0)

			deltaSFb_down = SFb_down[-1].Eval(1000.0) - weightSFb
			deltaSFb_up = SFb_up[-1].Eval(1000.0) - weightSFb

			weightSFb_down = SFb.Eval(1000.0) + 2*deltaSFb_down
			weightSFb_up = SFb.Eval(1000.0) + 2*deltaSFb_up

		#print [weightSFb,weightSFb_down,weightSFb_up]
		return [weightSFb,weightSFb_down,weightSFb_up]
	#This looks up the PDF uncertainty
	def SFT_Lookup(self, pttop ):

		ttagsf = [[0.88,0.11],[1.00,0.23]]
		ttagsfregions = [[0,550],[550,float("inf")]]

		for ipttop in range(0,len(ttagsfregions)):
			if ttagsfregions[ipttop][0]<pttop<=ttagsfregions[ipttop][1]:
				return [ttagsf[ipttop][0],ttagsf[ipttop][0]-ttagsf[ipttop][1],ttagsf[ipttop][0]+ttagsf[ipttop][1]]

	def SFH_Lookup(self, higgslv, GPs ):
		#print
		#print "New Event"
		Nparts = []
		Nsfs = []
		#if setstr.find('THB')!=-1:
		#	parts = [25,6]
		#if setstr.find('ttbar')!=-1:
		#	parts = [-6,6]
		for GP in GPs:
			#print GP.pdgId()
			if abs(GP.pdgId())==25 or abs(GP.pdgId())==6:

				GPlv = TLorentzVector()
				GPlv.SetPtEtaPhiM(GP.pt(),GP.eta(),GP.phi(),GP.mass())

				if (abs(GP.pdgId())==25) and (GP.numberOfDaughters()>1) and not (GP.pdgId() in Nparts):
					#print GP.pdgId()
					#print GP.numberOfDaughters()
					Nparts.append(GP.pdgId())
 					if GP.numberOfDaughters()>1:
						#print "ID",GP.pdgId()
						#print "daughters "
						minDR = -1.0
						for idaughter in range(0,GP.numberOfDaughters()):
	
							daughter = GP.daughter(idaughter)
							#print "ID",daughter.pdgId()
							daughterlv = TLorentzVector()
							daughterlv.SetPtEtaPhiM(daughter.pt(),daughter.eta(),daughter.phi(),daughter.mass())
							currentDR = higgslv.DeltaR(daughterlv)
							#print "DR",currentDR

							maxDR=max(minDR,currentDR)
						#print "maxDR",maxDR
						#print maxDR
						if maxDR<0.8:
							#print "ApplySF"
							if 250.0<higgslv.Perp()<=350.0:
								Nsfs.append([0.92,0.92+0.042,0.92-0.042,'eff'])
							if 350.0<higgslv.Perp()<=430.0:
								Nsfs.append([1.01,1.01+0.05,1.01-0.05,'eff'])
							if 430.0<higgslv.Perp()<=840.0:
								Nsfs.append([0.92,0.92+0.058,0.92-0.058,'eff'])
							if 840.0<higgslv.Perp():
								Nsfs.append([0.92,0.92+0.117,0.92-0.117,'eff'])
				if (abs(GP.pdgId())==6)  and not (GP.pdgId() in Nparts):
					Nparts.append(GP.pdgId())
					#print "ID",GP.pdgId()
					currentDR = higgslv.DeltaR(GPlv)
					#print "currentDR",currentDR
					if currentDR<1.2:
						#print "ApplyTOPSF"
						if 350.0<higgslv.Perp()<700.0:
							Nsfs.append([1.086,1.086+0.078,1.086-0.078,'mistag'])
	
						if 700.0<higgslv.Perp():
							Nsfs.append([1.086,1.086+0.156,1.086-0.156,'mistag'])
			if len(Nparts)>=2:

				if len(Nsfs)>0:
					for Nsf in Nsfs:
						if Nsf[-1]=='eff':
							return Nsf
					return Nsf

				break
		#print Nparts
		return [1.0,1.0,1.0,'none']
	#def PDF_Lookup( pdfs , pdfOP ):
		#print pdfs
		#for pd in pdfs:
	#		print pd
	#	iweight = 0.0

	 #       if pdfOP == "up" :
	  #     		for pdf in pdfs[1::2] :
	   #           		iweight = iweight + pdf*pdf
	    #    else :
	     #   	for pdf in pdfs[2::2] :
	      #  		iweight = iweight + pdf*pdf
		##print sqrt((iweight) / (len(pdfs)-1) * 2.0)
		#return sqrt((iweight) / (len(pdfs)-1) * 2.0)
	def PDF_LookupMAX(self, pdfs , pdfOP ):
		#print pdfs
		#for pd in pdfs:
	#		print pd
		iweight=1.0
		if pdfOP == "up" :
	       		for pdf in pdfs :
		      		iweight = max(iweight,pdf)

		else :
			for pdf in pdfs :
		      		iweight = min(iweight,pdf)

		return iweight

	def PDF_LookupAVE(self, pdfs , pdfOP ):
		iweight = 0.0
		if pdfOP == "up" :
	       		for pdf in pdfs[1::2] :
		      		iweight = iweight + pdf
		else :
			for pdf in pdfs[2::2] :
				iweight = iweight + pdf
		return (iweight) / (len(pdfs)-1) * 2.0
	def PDF_Lookup(self, pdfs , pdfOP ):
		

		ilimweight = 0.0

		limitedpdf = []

		#rmshist = TH1F("rms",  "",   	  	      	200, -100., 100 )

		#print 
		#print pdfs
		for curpdf in pdfs:
			if 0.00001<abs(curpdf)<1000.0:
				#rmshist.Fill(curpdf)
				limitedpdf.append(curpdf)

		#print "RMS", rmshist.GetRMS()
		#print "RMSE", rmshist.GetRMSError()


		limave =  limitedpdf
		limave =  reduce(lambda x, y: x + y, limitedpdf) / len(limitedpdf)

	       	for limpdf in limitedpdf :
			#print limpdf
		     	ilimweight = ilimweight + (limpdf-limave)*(limpdf-limave)
		
		if pdfOP == "up" :
			return min(13.0,1.0+sqrt((ilimweight) / (len(limitedpdf))))
		else :
		  	return max(-12.0,1.0-sqrt((ilimweight) / (len(limitedpdf))))

	def Q2_Lookup(self, Q2 , q2scale):
		Q2array = []
		for iQ2 in range(0,len(Q2)):
			print
			print Q2[iQ2]		
			print iQ2

			if iQ2 not in [0,5,7]:
				Q2array.append(Q2[iQ2])
				print Q2array
		if q2scale == "up" :
			return max(Q2array)
		if q2scale == "down" :
			return min(Q2array)
		print "INCORRECT OPTION"
	
	def as_Lookup(self, alphas ):
		uncs = []
		for calp in alphas:
			uncs.append((calp-1)*.75 + 1)
		returnas = [min(uncs),max(uncs)]
		return returnas
	#This looks up the b tagging scale factor or uncertainty
	def Trigger_Lookup(self, H , TRP):
		TrigWeight = 1.0
		TrigWeightup = 1.0
		TrigWeightdown = 1.0
		if H < 1600.0:
		        bin0 = TRP.FindBin(H) 
		        jetTriggerWeight = TRP.GetBinContent(bin0)
		        TrigWeight = jetTriggerWeight

			deltaTriggerEff  = 0.5*(1.0-jetTriggerWeight)
		        TrigWeightup  =   min(1.0,jetTriggerWeight + deltaTriggerEff)
		        TrigWeightdown  =   max(0.0,jetTriggerWeight - deltaTriggerEff)
		
		return [TrigWeight,TrigWeightup,TrigWeightdown]



	def Trigger_Pass(self,tnamestr,trigs,bits):
		###TAKE OUT!
		#tnamestr = ['HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV0p45_v3','HLT_PFHT800_v2']
		foundname=False
		for t in range(0,len(trigs)):
			for tname in tnamestr:	
				if trigs[t]==tname :
					foundname=True
				if trigs[t]==tname and bits[t] :
					return True
		if foundname==False:
			print "TRIGGER NOT IN FILE"
		return False



	def PU_Lookup(self, PU , PUP):
		PUWeight = 1.0
		PUWeightup = 1.0
		PUWeightdown = 1.0

		bin1 = PUP[0].FindBin(float(PU)) 

		PUWeight = PUP[0].GetBinContent(bin1)
		PUWeightup = PUP[1].GetBinContent(bin1)
		PUWeightdown = PUP[2].GetBinContent(bin1)

		return [PUWeight,PUWeightup,PUWeightdown]

	def PTW_Lookup( self, GP ):
		genTpt = -100.
		genTBpt = -100	
		for ig in GP :
			isT = ig.pdgId() == 6 and ig.status() == 22
			isTB = ig.pdgId() == -6 and ig.status() == 22
			if isT:
				genTpt = ig.pt()
			if isTB:
				genTBpt = ig.pt()

		if (genTpt<0) or (genTBpt<0):
			print "ERROR"

		# wTPt = exp(0.156-0.00137*genTpt)
		# wTbarPt = exp(0.156-0.00137*genTBpt)
		#print 	genTBpt , genTpt
		wTPt = math.exp(0.0615-0.0005*genTpt)
		wTbarPt = math.exp(0.0615-0.0005*genTBpt)
		#print wTPt,wTbarPt,sqrt(wTPt*wTbarPt)
		return sqrt(wTPt*wTbarPt)


	def Orthogonalize(self,orthopass,event):




	    	event.getByLabel (orthopass[0][1] , orthopass[0][0] )
	    	elPt 		= 	orthopass[0][0].product() 

	    	event.getByLabel (orthopass[1][1] , orthopass[1][0] )
	    	muIsMediumMuon 		= 	orthopass[1][0].product() 

	    	event.getByLabel (orthopass[2][1] , orthopass[2][0] )
	    	muPt 		= 	orthopass[2][0].product() 

	    	#event.getByLabel (orthopass[3][1] , orthopass[3][0] )
	    	#metFullPt 		= 	orthopass[3][0].product() 



		MedmuPt = []
	


		for im in range(0,len(muIsMediumMuon)):
			if muIsMediumMuon[im]:
				MedmuPt.append(muPt[im])

		if len(MedmuPt)!=0:

			if MedmuPt[0]>100.0:
				return False
			elif len(elPt)!=0:
				if elPt[0]>100.0:
					return False 

		if len(elPt)!=0:
				if elPt[0]>100.0:
					return False 
		#if len(metFullPt)!=0:
		#		if metFullPt[0]>150.0:
		#			return False 
		 
		return True


	#This is just a quick function to automatically make a tree
	#This is used right now to automatically output branches used to validate the cuts used in a run
	def Make_Trees(self,Floats,name="Tree"):
		t = TTree(name, name);
		print "Booking " + name
		for F in Floats.keys():
			extex = ''
			if len(Floats[F])>1:
				extex = "["+str(len(Floats[F]))+"]"
	    		t.Branch(F, Floats[F], F+extex+"/D")
		return t

	#This takes all of the alternative fit forms for the average b tagging rate and 
	#Compares them to the chosen nominal fit (bifpoly).  It outputs the mean squared error uncertainty from this comparison 
	def Fit_Uncertainty(self,List):
		sigmah	    = List[0]
		fits=len(List)-1
		for ihist in range(0,len(List)):
			print List[ihist].GetName()
			if List[ihist].GetName().find('Bifpoly') != -1:
				nominalhist = List[ihist]
		for ibin in range(0,nominalhist.GetXaxis().GetNbins()+1):

			mse=0.0
			sigma=0.0
			sumsqdiff = 0.0
			for ihist in range(0,len(List)):
				if List[ihist].GetName().find('Bifpoly') == -1:
					sumsqdiff+=(List[ihist].GetBinContent(ibin)-nominalhist.GetBinContent(ibin))*(List[ihist].GetBinContent(ibin)-nominalhist.GetBinContent(ibin))
			mse = sumsqdiff/fits
			sigma = sqrt(mse)
			sigmah.SetBinContent(ibin,sigma)
	
		return sigmah


	def calcchi2( self,DATA,BKG,BKGUP,BKGDOWN ):
		sigma = 0.0
		FScont = 0.0
		BKGcont = 0.0
		chi2tot = 0.
		ndf = 0
		for ibin in range(1,DATA.GetNbinsX()+1):
			FScont = DATA.GetBinContent(ibin)
			BKGcont = BKG.GetBinContent(ibin)
			if FScont>=BKGcont:
				FSerr = DATA.GetBinErrorLow(ibin)
				BKGerr = abs(BKGUP.GetBinContent(ibin)-BKG.GetBinContent(ibin))
			if FScont<BKGcont:
				FSerr = DATA.GetBinErrorUp(ibin)
				BKGerr = abs(BKGDOWN.GetBinContent(ibin)-BKG.GetBinContent(ibin))
				
			sigma = sqrt(FSerr*FSerr + BKGerr*BKGerr)
			if sigma>0. and BKGcont>0. and FScont>0.:
				chi2tot += ((FScont-BKGcont)/sigma)*((FScont-BKGcont)/sigma)
				ndf+=1
				#print "FScont,BKGcont",FScont,BKGcont
				#print "FSerr,BKGerr,sigma",FSerr,BKGerr,sigma
				#print "chi2tot,ndf",chi2tot,ndf
		print "CHI2TEST", chi2tot,ndf, chi2tot/float(ndf)
		return chi2tot/float(ndf)



	def calcchi2stat( self,DATA,BKG ):
		sigma = 0.0
		FScont = 0.0
		BKGcont = 0.0
		chi2tot = 0.
		ndf = 0
		for ibin in range(2,DATA.GetNbinsX()):
			FScont = DATA.GetBinContent(ibin)
			BKGcont = BKG.GetBinContent(ibin)
		
			print DATA.GetBinCenter(ibin)
			FSerr = DATA.GetBinError(ibin)
			BKGerr = BKG.GetBinError(ibin)
			sigma = sqrt(FSerr*FSerr + BKGerr*BKGerr)
			if sigma>0.:
				chi2tot += ((FScont-BKGcont)/sigma)*((FScont-BKGcont)/sigma)
				ndf+=1
		print "CHI2TESTstat", chi2tot,ndf, chi2tot/float(ndf)
		return chi2tot/float(ndf)



	#Makes the blue pull plots
	def Make_Pull_plot( self,DATA,BKG,BKGUP,BKGDOWN ):
		pull = DATA.Clone("pull")
		pull.Add(BKG,-1)
		sigma = 0.0
		FScont = 0.0
		BKGcont = 0.0
		for ibin in range(1,pull.GetNbinsX()+1):
			FScont = DATA.GetBinContent(ibin)
			BKGcont = BKG.GetBinContent(ibin)
			if FScont>=BKGcont:
				FSerr = DATA.GetBinErrorLow(ibin)
				BKGerr = abs(BKGUP.GetBinContent(ibin)-BKG.GetBinContent(ibin))
			if FScont<BKGcont:
				FSerr = DATA.GetBinErrorUp(ibin)
				BKGerr = abs(BKGDOWN.GetBinContent(ibin)-BKG.GetBinContent(ibin))
			sigma = sqrt(FSerr*FSerr + BKGerr*BKGerr)
			if FScont == 0.0:
				pull.SetBinContent(ibin, 0.0 )	
			else:
				if sigma != 0 :
					pullcont = (pull.GetBinContent(ibin))/sigma
					pull.SetBinContent(ibin, pullcont)
				else :
					pull.SetBinContent(ibin, 0.0 )
		return pull

	def Initlv(self,string,post='',jetcoll='Puppi'):
		PtHandle 	= 	Handle (  "vector<float> "  )
		PtLabel  	= 	( string+post , string.replace("jets","jet")+jetcoll+"Pt")

		EtaHandle 	= 	Handle (  "vector<float> "  )
		EtaLabel  	= 	( string+post , string.replace("jets","jet")+jetcoll+"Eta")

		PhiHandle 	= 	Handle (  "vector<float> "  )
		PhiLabel  	= 	( string+post , string.replace("jets","jet")+jetcoll+"Phi")

		MassHandle 	= 	Handle (  "vector<float> "  )
		MassLabel  	= 	( string+post , string.replace("jets","jet")+jetcoll+"Mass")

		return [[PtHandle,PtLabel],[EtaHandle,EtaLabel],[PhiHandle,PhiLabel],[MassHandle,MassLabel]]

	def Makelv(self,vector,event):

	    	event.getByLabel (vector[0][1], vector[0][0])
	    	Pt 		= 	vector[0][0].product()

	    	event.getByLabel (vector[1][1], vector[1][0])
	    	Eta 		= 	vector[1][0].product()

	    	event.getByLabel (vector[2][1], vector[2][0])
	    	Phi 		= 	vector[2][0].product()

	    	event.getByLabel (vector[3][1], vector[3][0])
	    	Mass 		= 	vector[3][0].product()

		lvs = []
		for i in range(0,len(Pt)):

			#lvs.append(ROOT.Math.LorentzVector('ROOT::Math::PtEtaPhiM4D<double>')(Pt[i],Eta[i],Phi[i],Mass[i]))
			lvs.append(TLorentzVector())
			lvs[i].SetPtEtaPhiM(Pt[i],Eta[i],Phi[i],Mass[i])
		return lvs









	#Temporary -- to update
	def InitAK4lv(self,string,post='',jetcoll='Puppi'):
		PtHandle 	= 	Handle (  "vector<float> "  )
		PtLabel  	= 	( string+post , string.replace("jets","jet")+jetcoll+"Pt")

		EtaHandle 	= 	Handle (  "vector<float> "  )
		EtaLabel  	= 	( string+post , string.replace("jets","jet")+jetcoll+"Eta")

		PhiHandle 	= 	Handle (  "vector<float> "  )
		PhiLabel  	= 	( string+post , string.replace("jets","jet")+jetcoll+"Phi")

		EnergyHandle 	= 	Handle (  "vector<float> "  )
		EnergyLabel  	= 	( string+post , string.replace("jets","jet")+jetcoll+"E")

		return [[PtHandle,PtLabel],[EtaHandle,EtaLabel],[PhiHandle,PhiLabel],[EnergyHandle,EnergyLabel]]

	def MakeAK4lv(self,vector,event):

	    	event.getByLabel (vector[0][1], vector[0][0])
	    	Pt 		= 	vector[0][0].product()

	    	event.getByLabel (vector[1][1], vector[1][0])
	    	Eta 		= 	vector[1][0].product()

	    	event.getByLabel (vector[2][1], vector[2][0])
	    	Phi 		= 	vector[2][0].product()

	    	event.getByLabel (vector[3][1], vector[3][0])
	    	Energy 		= 	vector[3][0].product()

		lvs = []
		for i in range(0,len(Pt)):

			#lvs.append(ROOT.Math.LorentzVector('ROOT::Math::PtEtaPhiM4D<double>')(Pt[i],Eta[i],Phi[i],Mass[i]))
			lvs.append(TLorentzVector())
			lvs[i].SetPtEtaPhiE(Pt[i],Eta[i],Phi[i],Energy[i])
		return lvs





	def Nonclosure(self,cmthb,histo):
		
		reunc = 1.0-histo.Interpolate(cmthb)
		#if cmthb<1300:
		#print reunc
		return reunc





	def Hemispherize(self,LV1,LV2):
		tjets = [[],[]]
		bjets = [[],[]]

		for iLV1 in range(0,len(LV1)):

			if abs(Math.VectorUtil.DeltaPhi(LV1[0],LV1[iLV1]))> TMath.Pi()/2.0:
				tjets[1].append(iLV1)
			else:
				tjets[0].append(iLV1)

		for iLV2 in range(0,len(LV2)):
			if abs(Math.VectorUtil.DeltaPhi(LV1[0],LV2[iLV2]))> TMath.Pi()/2.0:
				bjets[1].append(iLV2)
			else:
				bjets[0].append(iLV2)
		return tjets,bjets


	def projectquadrature(self, hist2d ):
		Projquad = hist2d.ProjectionY()
		for ybin in xrange(hist2d.GetNbinsY()+1):
			quadcont=0.0		
			for xbin in xrange(hist2d.GetNbinsX()+1):
				curcont = hist2d.GetBinContent(xbin,ybin)
				quadcont+=curcont*curcont
	
			quadcont=sqrt(quadcont)
			Projquad.SetBinContent(ybin,quadcont)
		return Projquad


	#Some lazy string formatting functions 
	def strf(self, x ):
		return '%.2f' % x

	def strf1(self, x ):
		return '%.0f' % x
	def strf2(self, x ):
		return '%.1f' % x

	def strfSF(self, x , nsf ):
		ndigs = int(math.log10(10*x))
		newnsf =nsf
		if ndigs<newnsf:
			dps = "."+str(min(newnsf,abs(ndigs-newnsf)))+"f"
			return '%{0}'.format(dps) % x
		else:
			return '%.0f' % x









