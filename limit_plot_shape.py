import array, math
import CMS_lumi
def Inter(g1,g2):
	xaxisrange = g1.GetXaxis().GetXmax()-g1.GetXaxis().GetXmin()
	xaxismin = g1.GetXaxis().GetXmin()
	inters = []
	for x in range(0,10000):
		xpoint = xaxismin + (float(x)/1000.0)*xaxisrange
		xpoint1 = xaxismin + (float(x+1)/1000.0)*xaxisrange
		Pr1 = g1.Eval(xpoint)
		Pr2 = g2.Eval(xpoint)
		Po1 = g1.Eval(xpoint1)
		Po2 = g2.Eval(xpoint1)
		if (Pr1-Pr2)*(Po1-Po2)<0:
			inters.append(0.5*(xpoint+xpoint1))
		
	return inters
			
def strf( x ):
	return '%.3f' % x

def strf1( x ):
	return '%.0f' % x
	

from optparse import OptionParser


parser = OptionParser()

parser.add_option('--inputFileExp', metavar='H', type='string', action='store',
                  default='limits_shape_exp.txt',
                  dest='inputFileExp',
                  help='Expected limits from theta')

parser.add_option('--inputFileObs', metavar='H', type='string', action='store',
                  default='limits_shape_obs.txt',
                  dest='inputFileObs',
                  help='Observed limits from theta')

parser.add_option('--outputName', metavar='D', type='string', action='store',
                  default='comb',
                  dest='outputName',
                  help='Directory to plot')

parser.add_option('--title', metavar='D', type='string', action='store',
                  default='narrow',
                  dest='title',
                  help='Titles to use, options are narrow, wide, kkg')

parser.add_option('--showNarrowTheory', action='store_true',
                  default=False,
                  dest='showNarrowTheory',
                  help='Show theory prediction for 1% width')

parser.add_option('--showWideTheory', action='store_true',
                  default=False,
                  dest='showWideTheory',
                  help='Show theory prediction for 3% width')

parser.add_option('--showKKGTheory', action='store_true',
                  default=False,
                  dest='showKKGTheory',
                  help='Show theory prediction for KK Gluon')

parser.add_option('--useLog', metavar='L', action='store_true',
                  default=False,
                  dest='useLog',
                  help='use log y-axis')

parser.add_option('--noTheory', metavar='T', action='store_true',
                  default=False,
                  dest='noTheory',
                  help='do not plot theory curves')

parser.add_option('-R', '--region', metavar='F', type='string', action='store',
                  default	=	'center',
                  dest		=	'region',
                  help		=	'sigscale')


(options, args) = parser.parse_args()

argv = []



import WprimetoVlq_Functions	
from WprimetoVlq_Functions import *


gROOT.Macro("rootlogon.C")
#VLQbuddy = {'1500':'1000','2000':'1300','2500':'1500','3000':'1800'}
VLQbuddy = {}
Outf   =   open("pdfw.csv", "r")
Outfr = Outf.read()
Outspl = Outfr.split('\n')
csunc = {}
for outl in Outspl:
	tempoutspl = outl.split(',')
	if len(tempoutspl)<3:
		continue 
	tempoutspl = outl.split(',')
	string = tempoutspl[0].replace("THBWp","").replace("Tp","").replace("Bp","")
	csunc[string+"__PDF__plus"]=float(tempoutspl[1])
	csunc[string+"__PDF__minus"]=float(tempoutspl[2])

print "extracted pdf uncertatainty:   "+str(csunc)
#WprimeConvo = (1.0)*(0.25)*(0.50)



WPF = WprimetoVlq_Functions('default')
Cons = WPF.LoadConstants
sigbrdict = WPF.sigBR


#Load up cut values based on what selection we want to run 

lumi = Cons['lumi']
kfac = Cons['kfac']
xsec_wpr = Cons['xsec_wpr']
xsec_ttbar = Cons['xsec_ttbar']
xsec_qcd = Cons['xsec_qcd']
xsec_st = Cons['xsec_st']
nev_wpr = Cons['nev_wpr']
nev_ttbar = Cons['nev_ttbar']
nev_qcd = Cons['nev_qcd']
nev_st = Cons['nev_st']


if options.region=='low':
	mindex=0
if options.region=='center':
	mindex=1
if options.region=='high':
	mindex=2



sigarray = WPF.sigmasses

for awpmass in sigarray:
	#sigpoints.append([awpmass,sigarray[awpmass][mindex]])
	VLQbuddy[awpmass]=sigarray[awpmass][mindex]




gROOT.Macro("rootlogon.C")

def make_smooth_graph(h2,h3):
    h2 = TGraph(h2)
    h3 = TGraph(h3)
    npoints = h3.GetN()
    h3.Set(2*npoints+2)
    for b in range(npoints+2):
        x1, y1 = (ROOT.Double(), ROOT.Double())
        if b == 0:
            h3.GetPoint(npoints-1, x1, y1)
        elif b == 1:
            h2.GetPoint(npoints-b, x1, y1)
        else:
            h2.GetPoint(npoints-b+1, x1, y1)
        h3.SetPoint(npoints+b, x1, y1)
    return h3

if __name__ == "__main__":
    ROOT.gROOT.Macro("rootlogon.C")
    TPT = ROOT.TPaveText(.20, .65, .45, .73,"NDC")
 
    if options.region=="low":
    	TPT.AddText("Low VLQ mass (~1/2m_{W'})")
    if options.region=="center":
    	TPT.AddText("Central VLQ mass (~2/3m_{W'})")
    if options.region=="high":
    	TPT.AddText("High VLQ mass (~3/4m_{W'})")



    TPT.SetFillColor(0)
    TPT.SetBorderSize(0)
    TPT.SetTextAlign(12)



    xsec_wpr = Cons['xsec_wpr']
    masses = [1500,2000,2500,3000,3500,4000] 

    x_mass = array('d')
    y_limit = array('d')
    y_mclimit  = array('d')
    y_mclimitlow68 = array('d')
    y_mclimitup68 = array('d')
    y_mclimitup95 = array('d')
    y_mclimitlow95 = array('d')
    

    logScale = options.useLog

    f1 = file(options.inputFileExp, "r")
    if (not options.noTheory) :
    	f2 = file(options.inputFileObs, "r")

    # i = 0
    expvals = []
    for line in f1:

        data = map(float,line.split())
        x_mass.append( data[0]/1000.0  )    # mass
        rt_xsec = xsec_wpr[str(int(data[0]))]
        #print data
        # data is an array along the line, has 8 entries

        #y_limit.append( data[1] )

    	if (not options.noTheory) :
		y_mclimit.append( data[1]*rt_xsec )

		y_mclimitlow95.append( data[2]*rt_xsec )
		y_mclimitup95.append( data[3]*rt_xsec )
		y_mclimitlow68.append( data[4]*rt_xsec )
		y_mclimitup68.append( data[5]*rt_xsec )
	else:
		print "noscale"
		y_mclimit.append( data[1])
		expvals.append(data[1])
		y_mclimitlow95.append( data[2])
		y_mclimitup95.append( data[3] )
		y_mclimitlow68.append( data[4] )
		y_mclimitup68.append( data[5] )
    print y_mclimit
    # i = 0
    if (not options.noTheory) :
	    for line in f2:

		data = map(float,line.split())
		rt_xsec = xsec_wpr[str(int(data[0]))]

		y_limit.append( data[1]*rt_xsec )
	 
    if (not options.noTheory) :
	    print "Limit Table"
	    for imass in range(0,len(x_mass)):    
			print "\hline"
			print strf1(x_mass[imass]*1000.0) +" & "+strf(y_limit[imass])+" & "+strf(y_mclimit[imass])+" & "+strf(y_mclimitlow68[imass])+","+strf(y_mclimitup68[imass])+" & "+strf(y_mclimitlow95[imass])+","+strf(y_mclimitup95[imass])
		  
    cv = TCanvas("cv", "cv",700, 600)
    #cv = TCanvas("cv", "cv")
    if logScale:
        cv.SetLogy(True)
    cv.SetLeftMargin(.18)
    cv.SetBottomMargin(.18)   

    if (not options.noTheory) : 
	    g_limit = TGraph(len(x_mass), x_mass, y_limit)	

	    g_limit.SetTitle("")
	    g_limit.SetMarkerStyle(0)
	    g_limit.SetMarkerColor(1)
	    g_limit.SetLineColor(1)
	    g_limit.SetLineWidth(3)
	    g_limit.SetMarkerSize(0.5) #0.5
	    g_limit.GetXaxis().SetTitle("M_{W'_{R}} (TeV)")
	    g_limit.GetYaxis().SetTitle("Upper Limit #sigma_{W'_{R}} #times B(W'_{R}#rightarrowtb) [pb]")

	    g_limit.Draw("alp")
	    g_limit.GetYaxis().SetRangeUser(0., 80.)
	    g_limit.GetXaxis().SetRangeUser(1.0, 2.9)
	    if logScale:
		g_limit.SetMinimum(1.0e-2) #0.005
		g_limit.SetMaximum(4000.) #10000
	    else:
		# g_limit.SetMaximum(80.)
		g_limit.SetMaximum(0.5)#20.)

	    g_limit.Draw("al")		#uncomm later
	    
    g_mclimit = TGraph(len(x_mass), x_mass, y_mclimit)
    g_mclimit.SetTitle("")
    g_mclimit.SetMarkerStyle(21)
    g_mclimit.SetMarkerColor(1)
    g_mclimit.SetLineColor(1)
    g_mclimit.SetLineStyle(2)
    g_mclimit.SetLineWidth(3)
    g_mclimit.SetMarkerSize(0.)
    g_mclimit.GetXaxis().SetTitle("m_{W'} (TeV)")
    g_mclimit.GetYaxis().SetTitle("Upper Limit #sigma_{W'} #times #bf{#it{#Beta}}( W' #rightarrow (Tb,tB) #rightarrow tHb) (pb)")

    g_mclimit.GetYaxis().SetTitleSize(0.03)
    g_mclimit.GetYaxis().SetTitleOffset(1.9)
    g_mclimit.Draw("al")
    g_mclimit.GetYaxis().SetRangeUser(0., 80.)
    if logScale:
		g_mclimit.SetMinimum(1.0e-3) #0.005
		g_mclimit.SetMaximum(300.) #10000
    else:
		# g_limit.SetMaximum(80.)
		g_mclimit.SetMaximum(0.5)#20.)


    g_mcplus = TGraph(len(x_mass), x_mass, y_mclimitup68)
    g_mcminus = TGraph(len(x_mass), x_mass, y_mclimitlow68)
    
    g_mc2plus = TGraph(len(x_mass), x_mass, y_mclimitup95)
    g_mc2minus = TGraph(len(x_mass), x_mass, y_mclimitlow95)

    graphWP = ROOT.TGraph()
    graphWP.SetTitle("")
    graphWP.SetMarkerStyle(23)
    graphWP.SetMarkerColor(4)
    graphWP.SetLineColor(4)
    graphWP.SetLineWidth(2)
    graphWP.SetMarkerSize(0.5)

    graphWPup = ROOT.TGraph()
    graphWPup.SetTitle("")
    graphWPup.SetMarkerStyle(23)
    graphWPup.SetMarkerColor(4)
    graphWPup.SetLineColor(4)
    graphWPup.SetLineWidth(1)
    graphWPup.SetLineStyle(2)
    graphWPup.SetMarkerSize(0.5)

    graphWPdown = ROOT.TGraph()
    graphWPdown.SetTitle("")
    graphWPdown.SetMarkerStyle(23)
    graphWPdown.SetMarkerColor(4)
    graphWPdown.SetLineColor(4)
    graphWPdown.SetLineWidth(1)
    graphWPdown.SetLineStyle(2)
    graphWPdown.SetMarkerSize(0.5)
    q = 0
    print "Theory lines"
    sigstr = []
    for wpmass in masses:

        rt_xsec = xsec_wpr[str(int(wpmass))]
	
	WprimeConvo = (1.0)*(0.50)
	WprimeConvo*=sigbrdict[str(int(wpmass))][mindex]
	
	print str(wpmass)+VLQbuddy[str(wpmass)]
	print "xsec",rt_xsec,"BR",sigbrdict[str(int(wpmass))][mindex],'WprimeConvo',WprimeConvo
	print rt_xsec*WprimeConvo
	print rt_xsec*csunc[str(wpmass)+VLQbuddy[str(wpmass)]+"__PDF__plus"]*WprimeConvo
	print rt_xsec*csunc[str(wpmass)+VLQbuddy[str(wpmass)]+"__PDF__minus"]*WprimeConvo 
	sigstr.append(rt_xsec*WprimeConvo)
    	graphWP.SetPoint(q,    wpmass/1000. ,   rt_xsec*WprimeConvo    )
    	graphWPup.SetPoint(q,    wpmass/1000. ,   rt_xsec*csunc[str(wpmass)+VLQbuddy[str(wpmass)]+"__PDF__plus"]*WprimeConvo    )
    	graphWPdown.SetPoint(q,    wpmass/1000. ,   rt_xsec*csunc[str(wpmass)+VLQbuddy[str(wpmass)]+"__PDF__minus"]*WprimeConvo   )
	q+=1
    graphWP.SetLineWidth(3)
    graphWP.SetLineColor(4 )

    print "expvals",expvals
    print "sigstr",sigstr
    print "sig strength"
    for xxx in xrange(len(expvals)):
	print expvals[xxx]/sigstr[xxx]

    g_error95 = make_smooth_graph(g_mc2minus, g_mc2plus)
    g_error95.SetFillColor(kYellow)
    g_error95.SetLineColor(0)
    g_error95.Draw("lf")
    g_error95.Draw("lf")
    
    g_error = make_smooth_graph(g_mcminus, g_mcplus)
    g_error.SetFillColor( kGreen)
    g_error.SetLineColor(0)
    g_error.Draw("lf")
    g_error.Draw("lf")
   

 

    g_mclimit.Draw("l")
    #g_limit.Draw("l")		#uncomm later
    if True:#(not options.noTheory) :
    	#g_limit.Draw("l")		#uncomm later
   	graphWP.Draw("l")
    	graphWPup.Draw("l")
    	graphWPdown.Draw("l")
	
    legLabel = ""
    if logScale:
	  legend = TLegend(0.47, 0.45, 0.86, 0.84, legLabel)
    else:
	  legend = TLegend(0.47, 0.35, 0.86, 0.75, legLabel)
    
    #legend.SetTextFont(42)
    if (not options.noTheory) :
   	 legend.AddEntry(g_limit, "Observed limit (95% CL)","l")		#uncomm later
    legend.AddEntry(g_mclimit, "Expected limit (95% CL)","l")
    legend.AddEntry(g_error, "68% Expected", "f")
    legend.AddEntry(g_error95, "95% Expected", "f")
    if True:
    	legend.AddEntry(graphWP, "W' signal", "l")
    	legend.AddEntry(graphWPup, "W' signal PDF uncertainty", "l")   
	#g_mclimit.GetYaxis().SetTitleOffset(1.9) 
	if (not options.noTheory) :
	    	g_limit.GetYaxis().SetTitleOffset(1.4)


    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetLineColor(0)
    
    text1 = ROOT.TLatex()
    text1.SetNDC()
    text1.SetTextFont(42)
    #text1.DrawLatex(0.2,0.84, "#scale[1.0]{CMS, L = 2.55 fb^{-1} at  #sqrt{s} = 13 TeV}")
    
    text11 = ROOT.TLatex()
    text11.SetTextFont(42)
    text11.SetNDC()

    label = "temp"
  
    text2 = ROOT.TLatex(3.570061, 23.08044, label)
    text2.SetNDC()
    text2.SetTextAlign(13)
    text2.SetX(0.4) #0.32
    text2.SetY(0.8) #0.87
    #text2.SetW(0.5)
    text2.SetTextFont(42)
    #text2.SetTextSizePixels(24)
    #text2.SetTextSizePixels(17)
    #text2.Draw()

    CMS_lumi.CMS_lumi(cv, 4, 11)
	
    legend.Draw("same")

    if (not options.noTheory) :
    	g_limit.Draw("p same")

    postpend = options.outputName
    if logScale:
        postpend = postpend + "_log"
    if options.noTheory :
        postpend = postpend + "_notheory"
    TPT.Draw()		
    cv.RedrawAxis()
    print "name is limits_theta_"+postpend+options.region
    cv.SaveAs("plots/limits_theta_"+postpend+options.region+".pdf")
    cv.SaveAs("plots/limits_theta_"+postpend+options.region+".gif")
    cv.SaveAs("plots/limits_theta_"+postpend+options.region+".png")
    cv.SaveAs("plots/limits_theta_"+postpend+options.region+".root")
    if (not options.noTheory) :
	    obs = Inter(g_limit,graphWP)
	    exp = Inter(g_mclimit,graphWP)


	    print "intersections:"
	    print "Observed"
	    for i in range(0,len(obs)): 
	    	print str(obs[i]) 
	    print "Experimental"
	    for i in range(0,len(exp)): 
	    	print str(exp[i]) 

   
