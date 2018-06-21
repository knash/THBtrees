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

parser.add_option('-t', '--cot', metavar='F', type='string', action='store',
                  default	=	'default',
                  dest		=	'cot',
                  help		=	'cottheta2')

parser.add_option('-S', '--sigscale', metavar='F', type='string', action='store',
                  default	=	'1.0',
                  dest		=	'sigscale',
                  help		=	'sigscale')
parser.add_option('-R', '--region', metavar='F', type='string', action='store',
                  default	=	'all',
                  dest		=	'region',
                  help		=	'sigscale')

parser.add_option('-u', '--ptreweight', metavar='F', type='string', action='store',
                  default	=	'on',
                  dest		=	'ptreweight',
                  help		=	'on or off')


parser.add_option('-B', '--Bbranch', metavar='F', type='string', action='store',
                  default	=	'0.5',
                  dest		=	'Bbranch',
                  help		=	'Wp to Bt BR')

parser.add_option('-T', '--Tbranch', metavar='F', type='string', action='store',
                  default	=	'0.5',
                  dest		=	'Tbranch',
                  help		=	'Wp to Tb BR')



(options, args) = parser.parse_args()

Tstr = options.Tbranch.replace('.','p')
Tstr += options.Bbranch.replace('.','p')

if Tstr == "0p50p5":
	Tstr=""

Tbrratio = float(options.Tbranch)/0.5
Bbrratio = float(options.Bbranch)/0.5

def Zero(hist):
	for ibin in range(0,hist.GetXaxis().GetNbins()+1):
		hist.SetBinContent(ibin,max(0.0,hist.GetBinContent(ibin)))
	
cuts = options.cuts
gROOT.Macro("rootlogon.C")

WPF = WprimetoVlq_Functions(options.cuts)

if options.region=='all':
	regions = ['center','high','low']
else:
	if not (options.region not in ['center','high','low']):
		print "bad region"
		sys.exit
	regions = [options.region]
ptrwstr = '' 
if options.ptreweight == "off":
	print "No pt reweighting!"
	ptrwstr = '_PTRWoff' 

for cregion in regions:

	LabelsU=[]
	mass = []


	bins=[500,1100]
	for ixabin in xrange(1,14):
		bins.append(bins[-1]+200)
	bins.append(bins[-1]+400)
	bins.append(8000)
	bins2=array('d',bins)
	print bins2



	#chans = ['h1t1b1','h1t0b1','h1t1b0']
	chans = ['h0t0b1']
	#chans = ['h1t1b1']
	chanstr = ''
	for ch in chans:
		chanstr+='_'+ch
	print chanstr

	if cregion=='center':
		mindex=1
	if cregion=='high':
		mindex=2
	if cregion=='low':
		mindex=0

	sigarray = WPF.sigmasses
	sigpoints = []
	for awpmass in sigarray:
		#if int(awpmass)>3100:
		#	continue
		sigpoints.append([awpmass,sigarray[awpmass][mindex]])
	#sigpoints = [['1500','1000'],['2000','1300'],['2500','1500'],['3000','1800']]
	#sigpoints = [['1500',''],['2000','1300'],['2500','1500'],['3000','1800']]

	sigscstr = ""
	foldstr = ""
	setstr ="weighted" 
	sigscale=1.0
	if options.sigscale=="cslim":
		print "using 1pb scale"
		sigscstr="sigscale_1pb"	 
		foldstr = "limitscale/"
		setstr ="limitscale" 
	elif options.sigscale!="1.0":
		print "using "+options.sigscale+" scale"
		sigscstr="sigscale_"+options.sigscale.replace(".","p")
		sigscale = float(options.sigscale)

	syststrings = ["JERMup","JERMdown","JECMup","JECMdown","JERup","JERdown","JECup","JECdown"]
	QCDuncs = ["up","down","Mup","Mdown","ttup","ttdown","closup","closdown"]

	for coup in ['right']:
		outputtmp = ROOT.TFile( "tmp.root", "recreate" )
		output = ROOT.TFile( "limitsetting/theta/TEST"+ptrwstr+chanstr+options.cuts+sigscstr+cregion+Tstr+".root", "recreate" )
		outputtmp.cd()

		Data = ROOT.TFile("rootfiles/THBanalyzerdata"+ptrwstr+"__PSET_"+options.cuts+".root")
		TTmc 	= ROOT.TFile("rootfiles/THBanalyzerweightedttbar"+ptrwstr+"__PSET_"+options.cuts+".root")

		sigfiles = []
		systfiles = {}
		efftable = {}

		for sigpoint in sigpoints:



			sigfiles.append([])
			#sigfiles[-1].append(ROOT.TFile("rootfiles/limitscale/THBanalyzerlimitscaleTHBWp"+sigpoint[0]+"Bp"+sigpoint[1]+"__PSET_"+options.cuts+".root"))
			#sigfiles[-1].append(ROOT.TFile("rootfiles/limitscale/THBanalyzerlimitscaleTHBWp"+sigpoint[0]+"Tp"+sigpoint[1]+"__PSET_"+options.cuts+".root"))
			sigfiles[-1].append(ROOT.TFile("rootfiles/"+foldstr+"THBanalyzer"+setstr+"THBWp"+sigpoint[0]+"Bp"+sigpoint[1]+"__PSET_"+options.cuts+".root"))
			sigfiles[-1].append(ROOT.TFile("rootfiles/"+foldstr+"THBanalyzer"+setstr+"THBWp"+sigpoint[0]+"Tp"+sigpoint[1]+"__PSET_"+options.cuts+".root"))



			reweight0 = array('d',[0.])
			wtree0 = sigfiles[-1][0].Get('Weight')
			wtree0.SetBranchAddress("weightv",reweight0)
			wtree0.GetEntry(0)


			reweight1 = array('d',[0.])
			wtree1 = sigfiles[-1][1].Get('Weight')
			wtree1.SetBranchAddress("weightv",reweight1)
			wtree1.GetEntry(0)




			noentries = sigfiles[-1][0].Get("Mthb_h1t1b1").GetEntries()+sigfiles[-1][1].Get("Mthb_h1t1b1").GetEntries()
			nointentries = sigfiles[-1][0].Get("Mthb_h1t1b1").Integral()*(1.0/reweight0[0])+sigfiles[-1][1].Get("Mthb_h1t1b1").Integral()*(1.0/reweight1[0])
			nototentries = sigfiles[-1][0].Get("nev").Integral()*(1.0/reweight0[0])+sigfiles[-1][1].Get("nev").Integral()*(1.0/reweight1[0])

			print sigfiles[-1]
			print "pass",noentries
			print "pass int",nointentries
			print "tot",nototentries
			print "eff",100*noentries/nototentries,"%"
			print "effint",100*nointentries/nototentries,"%"
			efftable[sigpoint[0]+sigpoint[1]] = noentries/nototentries
			for syststring in syststrings:
				#print syststring
				name = sigpoint[0]+"_"+sigpoint[1]+"_"+syststring.replace("_M","M_").replace("down","__minus").replace("up","__plus")
				#print  name
				systfiles[name] = []
				systfiles[name].append(ROOT.TFile("rootfiles/"+foldstr+"THBanalyzer"+setstr+"THBWp"+sigpoint[0]+"Bp"+sigpoint[1]+"_"+syststring+"_PSET_"+options.cuts+".root"))
				systfiles[name].append(ROOT.TFile("rootfiles/"+foldstr+"THBanalyzer"+setstr+"THBWp"+sigpoint[0]+"Tp"+sigpoint[1]+"_"+syststring+"_PSET_"+options.cuts+".root"))
			#print systfiles



	   	for ch in chans:

			TTmcFS = TTmc.Get("Mthb_"+ch)
			DataFS = Data.Get("Mthb_"+ch)


			#DataFS 	= DataB11.Get("Mthb_"+ch) 

			if ch.find('h1')!=-1:

				TTmcQCD = TTmc.Get("bkg_Mthb_"+ch+'ebin')

				DataQCD = Data.Get("bkg_Mthb_"+ch+'ebin')
				print "DATAQCDPRE",DataQCD.Integral()
				TTmcQCD = TTmcQCD.Rebin(len(bins2)-1,TTmcQCD.GetName(),bins2)

				QCDsysthists = []
				for QCDunc in QCDuncs:

					if QCDunc=="up" or QCDunc=="down":
						hist2dname = "bkg_Mthb2d_"+ch+"ebin"+QCDunc
			

						cur2dbkghist =Data.Get(hist2dname)
						#cur2dbkghist.RebinY(rebin)
						print "2dHname",hist2dname



						histupuncorr = WPF.projectquadrature(cur2dbkghist)
					

						#histupuncorrup = cur2dbkghistup.ProjectionY()
						#histupuncorrdown = cur2dbkghistdown.ProjectionY()

						DataQCDsysthist =  copy.copy(DataQCD)
						DataQCDsysthist = DataQCDsysthist.Rebin(len(bins2)-1,DataQCDsysthist.GetName(),bins2)
						histupuncorr = histupuncorr.Rebin(len(bins2)-1,histupuncorr.GetName(),bins2)
						print "ADDING"
						if QCDunc=="up":
							DataQCDsysthist.Add(histupuncorr,1)
						if QCDunc=="down":
							DataQCDsysthist.Add(histupuncorr,-1)
						print "Done"
					else:
						DataQCDsysthist = Data.Get("bkg_Mthb_"+ch+'ebin'+QCDunc)
					QCDsysthists.append(DataQCDsysthist)
					if not (QCDunc=="up" or QCDunc=="down"):
						QCDsysthists[-1] = QCDsysthists[-1].Rebin(len(bins2)-1,QCDsysthists[-1].GetName(),bins2)

					#print QCDunc
					#print "preintegral",QCDsysthists[-1].Integral()
					if QCDunc=="ttdown":
						print "ttdown d-d-d-d-double subtract"
						QCDsysthists[-1].Add(TTmcQCD,-2)
						print QCDsysthists[-1].Integral()
					elif QCDunc!="ttup":
						#print "nominal subtract"
						QCDsysthists[-1].Add(TTmcQCD,-1)
					else:
						print QCDunc
						print "ttup no subtract"
						print QCDsysthists[-1].Integral()
					#print "postintegral",QCDsysthists[-1].Integral()

					syststringappend = QCDunc.replace('down','__minus').replace('up','__plus')
					print syststringappend
					QCDsysthists[-1].SetName("mthb_"+ch+"__qcd__Fit"+syststringappend)
					QCDsysthists[-1].SetTitle("mthb_"+ch+"__qcd__Fit"+syststringappend)
				output.cd()

				for QCDsys in QCDsysthists:
					QCDsys.Write(QCDsys.GetName())
					print "Writing",QCDsys.GetName()
				outputtmp.cd()
				DataQCD = DataQCD.Rebin(len(bins2)-1,DataQCD.GetName(),bins2)
				DataQCD.Add(TTmcQCD,-1)
				print "DATAQCDPOST",DataQCD.Integral()
				print

				output.cd()
				DataQCD.SetName("mthb_"+ch+"__qcd")
				DataQCD.SetTitle("mthb_"+ch+"__qcd")
				DataQCD.Write("mthb_"+ch+"__qcd")
				print "Writing","mthb_"+ch+"__qcd"

			DataFS = DataFS.Rebin(len(bins2)-1,DataFS.GetName(),bins2)
			DataFS.SetName("mthb_"+ch+"__DATA")
			DataFS.SetTitle("mthb_"+ch+"__DATA")
			DataFS.Write("mthb_"+ch+"__DATA")
			print "Writing","mthb_"+ch+"__DATA"
			outputtmp.cd()



			alltthistos = []		
			allttsighistos = []

			for syststring in syststrings: 

					systname = syststring.replace("_M","M_").replace("down","__minus").replace("up","__plus")
					#print systname
					allttsighistos.append(ROOT.TFile("rootfiles/THBanalyzerweightedttbar_"+syststring+"_PSET_"+options.cuts+".root"))

					ttsyshisto = allttsighistos[-1].Get("Mthb_"+ch)


					ttsyshisto = ttsyshisto.Rebin(len(bins2)-1,ttsyshisto.GetName(),bins2)
					reconamesys = "mthb_"+ch+"__ttbar__"+systname





					print "writing ",reconamesys
					output.cd()
				
					ttsyshisto.SetName(reconamesys)
					ttsyshisto.SetTitle(reconamesys)
					ttsyshisto.Write(reconamesys)
					outputtmp.cd()



			TTmcFS.SetName("mthb_"+ch+"__ttbar")

			D1 = TTmc.GetListOfKeys()
			ttpdfasminus = {}
			ttpdfasplus = {}

			for i in range(0,len(D1)):
					a = D1[i].ReadObj()
					try:
						currentname = a.GetName()
						if currentname[0:4]!="Mthb":
							continue 
						TThisto = TTmc.Get(a.GetName())
					except:
						print "skipping ",a.GetName()
					if True:
			
						if currentname[-6:]!=ch:
							continue
						if str(type(a)) != "<class 'ROOT.TH1F'>":
							continue 
						#print currentname
						#print "Mthb=",currentname[0:4]
						#print "channel=",currentname[-6:]
						syststring = currentname[4:-7]
						#print  type(a) 
						print syststring,"downfind ",syststring.find('down')
						if syststring.find('matched')!=-1:
							continue 
						#if syststring.find('Tpt')!=-1:
						#	continue
						print syststring

						TThisto = TThisto.Rebin(len(bins2)-1,TThisto.GetName(),bins2)
						if syststring.find('down')!=-1:
						#	print "isdown"
							reconame="mthb_"+ch+"__ttbar__"+syststring.replace('down','')+"__minus"
						elif syststring.find('up')!=-1:
							reconame="mthb_"+ch+"__ttbar__"+syststring.replace('up','')+"__plus"
						else:
							reconame="mthb_"+ch+"__ttbar"
							nomhist = TThisto

						#print "writing",a.GetName()
						#print "Using name",reconame



						alltthistos.append(copy.copy(TThisto))
						if syststring.find('PDF')!=-1 or syststring.find('Alp')!=-1 :
							#print "INTHEIF"
							#print reconame
							if reconame.find("minus")!=-1:
								#print "isminus"
								ttpdfasminus[syststring]=alltthistos[-1]
								if len(ttpdfasminus)<2:
									#print "comtineu"
									continue 

								if len(ttpdfasminus)==2:

									#print "MINUS ",ttpdfasminus
							
									print "zeroint "+str(ttpdfasminus['PDFdown'].Integral())
									print "oneint "+str(ttpdfasminus['Alpdown'].Integral())
									print "nomint "+str(nomhist.Integral())



									ttnewpdfminus = copy.copy(nomhist)
							

									ttpdfasminus['PDFdown'].Add(nomhist,-1)
									ttpdfasminus['Alpdown'].Add(nomhist,-1)

									for bin in range(0,ttnewpdfminus.GetNbinsX()+1):	
										nhcont = nomhist.GetBinContent(bin)
										mncont0 = ttpdfasminus['PDFdown'].GetBinContent(bin)
										mncont1 = ttpdfasminus['Alpdown'].GetBinContent(bin)
										#print "nom",nhcont,"zero",mncont0,"one",mncont1
										ttnewpdfminus.SetBinContent(bin,nhcont-sqrt(mncont0*mncont0+mncont1*mncont1))
										ttnewpdfminus.SetBinError(bin,nomhist.GetBinError(bin))
										#print "cont",nhcont-sqrt(mncont0*mncont0+mncont1*mncont1)
									reconame="mthb_"+ch+"__ttbar__PDF__minus"

									alltthistos[-1]= ttnewpdfminus 
									print "fullpdf "+str(alltthistos[-1].Integral())


							if reconame.find("plus")!=-1 and len(ttpdfasplus)<2:
								print "isplus"
								ttpdfasplus[syststring]=alltthistos[-1]
								print ttpdfasplus
								if len(ttpdfasplus)<2:
									#print "comtineu"
									continue 


								if len(ttpdfasplus)==2:
									#print "PLUS ",ttpdfasplus

									ttnewpdfplus = copy.copy(nomhist)
							
							
									print "zeroint "+str(ttpdfasplus['PDFup'].Integral())
									print "oneint "+str(ttpdfasplus['Alpup'].Integral())
									print "nomint "+str(nomhist.Integral())

							
									ttpdfasplus['PDFup'].Add(nomhist,-1)
									ttpdfasplus['Alpup'].Add(nomhist,-1)




									#print "SUBBED"
									#print "zeroint ",pdfasplus['PDFup'].Integral()
									#print "oneint ",pdfasplus['Alpup'].Integral()
									#print "nomint ",nomhist.Integral()
									for bin in range(0,ttnewpdfplus.GetNbinsX()+1):	
										#print bin
										nhcont = nomhist.GetBinContent(bin)
										plcont0 = ttpdfasplus['PDFup'].GetBinContent(bin)
										plcont1 = ttpdfasplus['Alpup'].GetBinContent(bin)
										#print "nom",nhcont,"zero",plcont0,"one",plcont1
										ttnewpdfplus.SetBinContent(bin,nhcont+sqrt(plcont0*plcont0+plcont1*plcont1))
										ttnewpdfplus.SetBinError(bin,nomhist.GetBinError(bin))
										#print "cont",nhcont+sqrt(plcont0*plcont0+plcont1*plcont1)
									reconame="mthb_"+ch+"__ttbar__PDF__plus"
									alltthistos[-1]= ttnewpdfplus 
									print "fullpdf "+str(alltthistos[-1].Integral())













						output.cd()
						print "writing ",reconame
						alltthistos[-1].SetName(reconame)
						alltthistos[-1].SetTitle(reconame)
						alltthistos[-1].Write(reconame)
						print "Keep it!"
						outputtmp.cd()





			isig = 0
			allsighists = []
			allsyssighists = []
			pdffraction = {}
			for sigpoint in sigpoints:
				for syststring in syststrings: 
		
					name = sigpoint[0]+"_"+sigpoint[1]+"_"+syststring.replace("_M","M_").replace("down","__minus").replace("up","__plus")
					#print name

					systname = syststring.replace("_M","M_").replace("down","__minus").replace("up","__plus")
					#print systname
					#print sigpoint 
					#print systfiles[name]
					syshisto0 = systfiles[name][0].Get("Mthb_"+ch)
					syshisto1 = systfiles[name][1].Get("Mthb_"+ch)





					syshisto0 = syshisto0.Rebin(len(bins2)-1,syshisto0.GetName(),bins2)
					syshisto1 = syshisto1.Rebin(len(bins2)-1,syshisto1.GetName(),bins2)
					#print "histo1-Bp ",syshisto0.Integral()
					#print "histo2-Tp ",syshisto1.Integral()


					syshisto0.Scale(Bbrratio)
					syshisto1.Scale(Tbrratio)

					allsyssighists.append(copy.copy(syshisto0))
					allsyssighists[-1].Add(syshisto1)

					#print "summed ",allsyssighists[-1].Integral()
					reconamesys = "mthb_"+ch+"__wp"+sigpoint[0]+"__"+systname
					#print reconamesys
					output.cd()
					print "writing ",reconamesys
					allsyssighists[-1].SetName(reconamesys)
					allsyssighists[-1].SetTitle(reconamesys)
					allsyssighists[-1].Write(reconamesys)
					outputtmp.cd()
				sigintegrals = {}
				D = sigfiles[isig][0].GetListOfKeys()
				pdfasminus = {}
				pdfasplus = {}

				nomhistsig = None
				for i in range(0,len(D)):
					a = D[i].ReadObj()
					try:
						currentname = a.GetName()
						if currentname[0:4]!="Mthb":
							continue 
						histo0 = sigfiles[isig][0].Get(a.GetName())
						histo1 = sigfiles[isig][1].Get(a.GetName())
					except:
						print "skipping ",a.GetName()
					if True:

						if currentname[-6:]!=ch:
							continue
						if str(type(a)) != "<class 'ROOT.TH1F'>":
							continue 
						#print currentname
						#print "Mthb=",currentname[0:4]
						#print "channel=",currentname[-6:]
						syststring = currentname[4:-7]

						if syststring.find('matched')!=-1:
							continue 

						#print  type(a) 
						#print syststring

						
					
						if syststring.find('down')!=-1:
						#	print "isdown"
							reconame="mthb_"+ch+"__wp"+sigpoint[0]+"__"+syststring.replace('down','')+"__minus"
						elif syststring.find('up')!=-1:
							reconame="mthb_"+ch+"__wp"+sigpoint[0]+"__"+syststring.replace('up','')+"__plus"
						else:
							reconame="mthb_"+ch+"__wp"+sigpoint[0]

						#print "writing",a.GetName()
						#print "Using name",reconame

						histo0 = sigfiles[isig][0].Get(a.GetName())
						histo1 = sigfiles[isig][1].Get(a.GetName())
						#print "adding ",histo0,histo0.Integral()
						#print "and ",histo1,histo1.Integral()



						#print "histo1-Bp ",histo0.Integral()
						#print "histo2-Tp ",histo1.Integral()

						histo0 = histo0.Rebin(len(bins2)-1,histo0.GetName(),bins2)
						histo1 = histo1.Rebin(len(bins2)-1,histo1.GetName(),bins2)

						histo0.Scale(Bbrratio)
						histo1.Scale(Tbrratio)

						allsighists.append(copy.copy(histo0))
						allsighists[-1].Add(histo1)
						#print "summed ",allsighists[-1].Integral()

						if syststring=='':
							sigintegrals["wp"+sigpoint[0]] = allsighists[-1].Integral()
							#print sigintegrals["wp"+sigpoint[0]]

						if reconame=="mthb_"+ch+"__wp"+sigpoint[0]:
							nomhistsig = allsighists[-1]


						if syststring.find('Q2')!=-1:
							print "Q2"
							print "nom ",str(nomhistsig.Integral()),"cur ",str(allsighists[-1].Integral())
							if allsighists[-1].Integral()>0:
								allsighists[-1].Scale(nomhistsig.Integral()/allsighists[-1].Integral())	
							print allsighists[-1].Integral()
						if syststring.find('Alp')!=-1 :
							print syststring
							print "SKIPIT"
							continue

						if syststring.find('PDF')!=-1:
							print "PDF"
							print "nom ",str(nomhistsig.Integral()),"cur ",str(allsighists[-1].Integral())
							if allsighists[-1].Integral()>0:
								allsighists[-1].Scale(nomhistsig.Integral()/allsighists[-1].Integral())	
							print "pre",reconame
							reconame=reconame.replace("PDF","PDFsig")
							print "post",reconame



						output.cd()
						print "writing ",reconame
						allsighists[-1].SetName(reconame)
						allsighists[-1].SetTitle(reconame)
						allsighists[-1].Write(reconame)
						print "Keep it!"
						outputtmp.cd()


				isig += 1
	print pdffraction
	for pdff in pdffraction :
		print pdff,pdffraction[pdff]
	print cregion
	for eff in efftable:
		print eff,100.0*efftable[eff]
	print "writing",output
	output.Write()
	output.ls()
	output.Close()
	print "Done!"
sys.exit
