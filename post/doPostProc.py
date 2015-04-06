#!/usr/bin/python

if __name__=='__main__':
    from Sample import *
    from Plot import Plot
    from cuts import *
    from DataCard import *

import pickle

from ROOT import *
from tdrStyle import *
from sys import argv
from array import array
from numpy import linspace
import os

setTDRStyle()
gStyle.SetOptStat(False)
gROOT.SetBatch(1)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if len(argv)>1:
    outputDir=argv[1]
else:
    outputDir='plots'

if len(argv)>2:
    inputDir=argv[2]
else:
    inputDir='/eos/uscms/store/user/lpcmbja/noreplica/ntran/Zllstep4/112614'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#SETTINGS

DEBUG=True

fillEmptyBins=False
blind=False ###?###
applyNormSFs=True
unroll2D=False ###?###
normalizeByBinWidth=False ###?###

doBDT=True
do1stHalfBDT=False
do2ndHalfBDT=False

doCutTable=False
doTheta=False
makeDataCard=True

doAllSys=True ###?###
doJECSys=False
doJERSys=False
doBTagSys=False
doMisTagSys=False
doZJetsShapeSys=False
doTTbarShapeSys=False
doStatSys=False

doCuts=[
    'bdt',
    #'ZLF',
    #'ZHF',
    #'ttbar'
    ]

doVtypes=[
    0,
    1
    ]

doBoosts=[
    'med',
    'high'
    ]

showOverflow=True

doShapeComparison=False   #FIXME - not updated

doFormFactorWeighting=False ###?###
Lambda=10000

do13TeVestimate=False ###?###
lumi13TeV=300000

if not do13TeVestimate:
	elLumi=18940
	muLumi=18940
	
if do13TeVestimate:
	elLumi=lumi13TeV
	muLumi=lumi13TeV

sigmaFracUnc={}
sigmaFracUnc['VZ']=0.2
sigmaFracUnc['VV']=0.2
sigmaFracUnc['WJets']=0.2
sigmaFracUnc['ZJets']=0.2
sigmaFracUnc['ttbar']=0.15
sigmaFracUnc['singleTop']=0.15
sigmaFracUnc['QCD']=0.25
sigmaFracUnc['ggZh']=0.2
lumiFracUnc=.026   #2.6% for 8 TeV, 2.2% for 7 TeV (Jia Fu)

signalMagFrac=120

plotBackgrounds=['Z_light','Z_b','Z_bb','ttbar','VV','VZ','ggZh']
backgroundFillColors={'Z_light':ROOT.kYellow-7,'Z_b':ROOT.kYellow-3,'Z_bb':ROOT.kYellow+2,'WJets':ROOT.kGreen-3,'singleTop':ROOT.kCyan-7,'ttbar':ROOT.kBlue-7,'VV':ROOT.kGray+2,'VZ':ROOT.kRed-7,'ggZh':kOrange+1}
backgroundLineColors={'Z_light':ROOT.kYellow-6,'Z_b':ROOT.kYellow-2,'Z_bb':ROOT.kYellow+3,'WJets':ROOT.kGreen-2,'singleTop':ROOT.kCyan-3,'ttbar':ROOT.kBlue-3,'VV':ROOT.kGray+3,'VZ':ROOT.kRed-4,'ggZh':kOrange+2}


treeName='tree'
                
#---------------------------------------------------------------------------------------------------------------------------------------------
"""
if doTheta or makeDataCard:
    doVtypes=[2,3]
    doBoosts=['med','high']
    doCuts=['bdt']
    doCutTable=False
"""    
if doCutTable:
    doTheta=False
    makeDataCard=False

##################################################################################################################################################################

if __name__=='__main__':
    
    print 'Welcome to doPostProc!'
    logFile = open(outputDir + '/log.txt','w')
    logFile.close()

    if makeDataCard:
        dataCard=DataCard()
        cardFile=outputDir+'/dataCard.txt'

    yields={}
    plots=[]
    for cuts in doCuts:
        yields[cuts]={}
        for Vtype in doVtypes:
            yields[cuts][Vtype]={}
            for boost in doBoosts:
                yields[cuts][Vtype][boost]={}
	print cuts
    if makeDataCard:
    	for cuts in doCuts:
			plots+=[
				
				#Plot(name='V_pT',distribution='V.pt',nBinsX=25,xMin=0,xMax=500,xTitle='p_{T}(V) [GeV]',yLog=False,cuts=cuts,Vtype=1,boost='high'),
				
				#Plot(name='h_mass',distribution='H.mass',binsX=[0]+linspace(40,240,21).tolist()+[500],xTitle='m(h) [GeV]',yLog=True,cuts=cuts,Vtype=Vtype,boost='med'),  
				#Plot(name='h_mass',distribution='H.mass',binsX=[0]+linspace(60,240,19).tolist()+[500],xTitle='m(h) [GeV]',yLog=True,cuts=cuts,Vtype=Vtype,boost='high'),

				# mVh uniform binning
				#Plot(name='x_mVh',distribution='h_MVHCorr',nBinsX=30,xMin=0,xMax=1200,xTitle='m(Vh) [GeV]',yLog=True,cuts=cuts,Vtype=0,boost='med'),
				#Plot(name='x_mVh',distribution='h_MVHCorr',nBinsX=30,xMin=0,xMax=1200,xTitle='m(Vh) [GeV]',yLog=True,cuts=cuts,Vtype=1,boost='med'),
				#Plot(name='x_mVh',distribution='h_MVHCorr',nBinsX=30,xMin=0,xMax=1200,xTitle='m(Vh) [GeV]',yLog=True,cuts=cuts,Vtype=0,boost='high'),
				#Plot(name='x_mVh',distribution='h_MVHCorr',nBinsX=30,xMin=0,xMax=1200,xTitle='m(Vh) [GeV]',yLog=True,cuts=cuts,Vtype=1,boost='high'),

				# mVh uniform binning
				Plot(name='x_mVh',distribution='h_MVHCorr',nBinsX=100,xMin=0,xMax=2000,xTitle='m(Vh) [GeV]',yLog=False,cuts=cuts,Vtype=0,boost='med'),
				Plot(name='x_mVh',distribution='h_MVHCorr',nBinsX=100,xMin=0,xMax=2000,xTitle='m(Vh) [GeV]',yLog=False,cuts=cuts,Vtype=1,boost='med'),
				Plot(name='x_mVh',distribution='h_MVHCorr',nBinsX=100,xMin=0,xMax=2000,xTitle='m(Vh) [GeV]',yLog=False,cuts=cuts,Vtype=0,boost='high'),
				Plot(name='x_mVh',distribution='h_MVHCorr',nBinsX=100,xMin=0,xMax=2000,xTitle='m(Vh) [GeV]',yLog=False,cuts=cuts,Vtype=1,boost='high'),
			
				# BDT uniform binning
				#Plot(name='h_bdtCorr',distribution='h_bdtmCorr',binsX=linspace(-1,1,16).tolist(),xTitle='BDT',yLog=False,cuts=cuts,Vtype=0,boost='med'),
				#Plot(name='h_bdtCorr',distribution='h_bdtmCorr',binsX=linspace(-1,1,16).tolist(),xTitle='BDT',yLog=False,cuts=cuts,Vtype=1,boost='med'),			
				#Plot(name='h_bdtCorr',distribution='h_bdttCorr',binsX=linspace(-1,1,16).tolist(),xTitle='BDT',yLog=False,cuts=cuts,Vtype=0,boost='high'),
				#Plot(name='h_bdtCorr',distribution='h_bdttCorr',binsX=linspace(-1,1,16).tolist(),xTitle='BDT',yLog=False,cuts=cuts,Vtype=1,boost='high'),

				# mVh hypothesis testing binning
				#Plot(name='x_mVh',distribution='h_MVHCorr',binsX=[0.0, 200.0, 250.0, 300.0, 350.0, 400.0, 450.0, 500.0, 1200.0],xTitle='m(Vh) [GeV]',yLog=True,cuts=cuts,Vtype=0,boost='med'),
				#Plot(name='x_mVh',distribution='h_MVHCorr',binsX=[0.0, 200.0, 250.0, 300.0, 350.0, 1200.0],xTitle='m(Vh) [GeV]',yLog=True,cuts=cuts,Vtype=1,boost='med'),
				#Plot(name='x_mVh',distribution='h_MVHCorr',binsX=[0.0, 350.0, 400.0, 450.0, 500.0, 550.0, 1200.0],xTitle='m(Vh) [GeV]',yLog=True,cuts=cuts,Vtype=0,boost='high'),
				#Plot(name='x_mVh',distribution='h_MVHCorr',binsX=[0.0, 300.0, 350.0, 400.0, 450.0, 500.0, 550.0, 600.0, 1200.0],xTitle='m(Vh) [GeV]',yLog=True,cuts=cuts,Vtype=1,boost='high'),
			
				# BDT hypothesis testing binning
				#Plot(name='h_bdtCorr',distribution='h_bdtmCorr',binsX=[-1.0, -0.75, -0.6666666666666666, -0.5833333333333334, -0.5, -0.4166666666666667, -0.33333333333333337, -0.25, -0.16666666666666674, -0.08333333333333337, 0.0, 1.0],xTitle='BDT',yLog=True,cuts=cuts,Vtype=0,boost='med'),
				#Plot(name='h_bdtCorr',distribution='h_bdtmCorr',binsX=[-1.0, -0.75, -0.6666666662151164, -0.5833333324302327, -0.499999998645349, -0.41666666486046533, -0.33333333107558166, -0.249999997290698, -0.16666666350581427, -0.08333332972093066, 4.063952951938177e-09, 0.08333333784883667, 0.1666666716337204, 1.0],xTitle='BDT',yLog=True,cuts=cuts,Vtype=1,boost='med'),			
				#Plot(name='h_bdtCorr',distribution='h_bdttCorr',binsX=[-1.0, -0.5833333134651184, -0.49999998103488574, -0.4166666486046531, -0.33333331617442047, -0.2499999837441878, -0.16666665131395514, -0.08333331888372253, 1.3546510135853396e-08, 0.0833333459767428, 0.16666667840697547, 0.25000001083720813, 0.3333333432674408, 1.0],xTitle='BDT',yLog=True,cuts=cuts,Vtype=0,boost='high'),
				#Plot(name='h_bdtCorr',distribution='h_bdttCorr',binsX=[-1.0, -0.5833333134651184, -0.4999999821186066, -0.41666665077209475, -0.33333331942558286, -0.24999998807907103, -0.1666666567325592, -0.08333332538604732, 5.960464455334602e-09, 0.08333333730697634, 0.16666666865348823, 0.25, 1.0],xTitle='BDT',yLog=True,cuts=cuts,Vtype=1,boost='high'),


				# BDT for significance, etc
				#Plot(name='h_bdtCorr',distribution='h_bdtmCorr',binsX=[-1]+linspace(-0.7,0.25,11).tolist()+[1],xTitle='BDT',yLog=True,cuts=cuts,Vtype=0,boost='med'),
				#Plot(name='h_bdtCorr',distribution='h_bdtmCorr',binsX=[-1]+linspace(-0.7,0.25,11).tolist()+[1],xTitle='BDT',yLog=True,cuts=cuts,Vtype=1,boost='med'),			
				#Plot(name='h_bdtCorr',distribution='h_bdttCorr',binsX=[-1]+linspace(-0.85,0.45,14).tolist()+[1],xTitle='BDT',yLog=True,cuts=cuts,Vtype=0,boost='high'),
				#Plot(name='h_bdtCorr',distribution='h_bdttCorr',binsX=[-1]+linspace(-0.85,0.45,14).tolist()+[1],xTitle='BDT',yLog=True,cuts=cuts,Vtype=1,boost='high'),

				#Plot(name='Z_mass',distribution='V.mass',nBinsX=20,xMin=75,xMax=105,xTitle='m(Vh) [GeV]',yLog=True,cuts=cuts,Vtype=0,boost='med'),
				#Plot(name='Z_mass',distribution='V.mass',nBinsX=20,xMin=75,xMax=105,xTitle='m(Vh) [GeV]',yLog=True,cuts=cuts,Vtype=1,boost='med'),
				#Plot(name='Z_mass',distribution='V.mass',nBinsX=20,xMin=75,xMax=105,xTitle='m(Vh) [GeV]',yLog=True,cuts=cuts,Vtype=0,boost='high'),
				#Plot(name='Z_mass',distribution='V.mass',nBinsX=20,xMin=75,xMax=105,xTitle='m(Vh) [GeV]',yLog=True,cuts=cuts,Vtype=1,boost='high'),

				#uniform binning - JS
                                #Plot(name='mainBDT_v_VstarMass', distribution='h_bdtmCorr:h_MVHCorr',nBinsX=12,xMin=0,xMax=1200,xTitle='m(Vh) [GeV]',nBinsY=10,yMin=-1,yMax=1,yTitle='BDT',yLog=False,cuts=cuts,Vtype=0,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='h_bdtmCorr:h_MVHCorr',nBinsX=12,xMin=0,xMax=1200,xTitle='m(Vh) [GeV]',nBinsY=10,yMin=-1,yMax=1,yTitle='BDT',yLog=False,cuts=cuts,Vtype=1,boost='med'),


				#Plot(name='mainBDT_v_VstarMass', distribution='h_bdttCorr:h_MVHCorr',binsX=[0]+linspace(280,560,7).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.6, 0.0, 12).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=0,boost='high'),
				#Plot(name='mainBDT_v_VstarMass', distribution='h_bdttCorr:h_MVHCorr',binsX=[0]+linspace(270,515,8).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.65, 0.1, 15).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=1,boost='high'),

				#uniform mVh, Coarser
				#Plot(name='mainBDT_v_VstarMass', distribution='h_bdtmCorr:h_MVHCorr',binsX=linspace(0,1200,25).tolist(),xTitle='m(Vh) [GeV]',binsY=linspace(-1,1,25).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=0,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='h_bdtmCorr:h_MVHCorr',binsX=linspace(0,1200,25).tolist(),xTitle='m(Vh) [GeV]',binsY=linspace(-1,1,25).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=1,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='h_bdttCorr:h_MVHCorr',binsX=linspace(0,1200,25).tolist(),xTitle='m(Vh) [GeV]',binsY=linspace(-1,1,25).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=0,boost='high'),
				#Plot(name='mainBDT_v_VstarMass', distribution='h_bdttCorr:h_MVHCorr',binsX=linspace(0,1200,25).tolist(),xTitle='m(Vh) [GeV]',binsY=linspace(-1,1,25).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=1,boost='high'),

				#Zll mVh uniformCoarser global box rebinned
				#Plot(name='mainBDT_v_VstarMass', distribution='h_bdtmCorr:h_MVHCorr',binsX=[0.0, 200.0, 250.0, 300.0, 350.0, 400.0, 450.0, 500.0, 1200.0],xTitle='m(Vh) [GeV]',binsY=[-1.0, -0.75, -0.6666666666666666, -0.5833333333333334, -0.5, -0.4166666666666667, -0.33333333333333337, -0.25, -0.16666666666666674, -0.08333333333333337, 0.0, 1.0],yTitle='BDT',yLog=False,cuts=cuts,Vtype=0,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='h_bdtmCorr:h_MVHCorr',binsX=[0.0, 200.0, 250.0, 300.0, 350.0, 400.0, 450.0, 1200.0],xTitle='m(Vh) [GeV]',binsY=[-1.0, -0.75, -0.6666666666666666, -0.5833333333333334, -0.5, -0.4166666666666667, -0.33333333333333337, -0.25, -0.16666666666666674, -0.08333333333333337, 0.0, 1.0],yTitle='BDT',yLog=False,cuts=cuts,Vtype=1,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='h_bdttCorr:h_MVHCorr',binsX=[0.0, 250.0, 300.0, 350.0, 400.0, 450.0, 500.0, 550.0, 600.0, 650.0, 700.0, 750.0, 850.0, 1200.0],xTitle='m(Vh) [GeV]',binsY=[-1.0, -0.5833333134651184, -0.4999999829701015, -0.4166666524750846, -0.33333332198006765, -0.24999999148505075, -0.16666666099003385, -0.0833333304950169, 0.0, 1.0],yTitle='BDT',yLog=False,cuts=cuts,Vtype=0,boost='high'),
				#Plot(name='mainBDT_v_VstarMass', distribution='h_bdttCorr:h_MVHCorr',binsX=[0.0, 250.0, 300.0, 350.0, 400.0, 450.0, 500.0, 550.0, 600.0, 650.0, 1200.0],xTitle='m(Vh) [GeV]',binsY=[-1.0, -0.5833333134651184, -0.4999999823048711, -0.41666665114462376, -0.33333331998437643, -0.2499999888241291, -0.16666665766388178, -0.08333332650363445, 4.6566128730773926e-09, 0.0833333358168602, 1.0],yTitle='BDT',yLog=False,cuts=cuts,Vtype=1,boost='high'),

				#Zll mVh uniformCoarser global box rebinned2 (the real deal)
                #Plot(name='mainBDT_v_VstarMass', distribution='h_bdtmCorr:h_MVHCorr',binsX=[0.0, 200.0, 250.0, 300.0, 350.0, 400.0, 450.0, 500.0, 1200.0],xTitle='m(Vh) [GeV]',binsY=[-1.0, -0.75, -0.6666666666666666, -0.5833333333333334, -0.5, -0.4166666666666667, -0.33333333333333337, -0.25, -0.16666666666666674, -0.08333333333333337, 0.0, 1.0],yTitle='BDT',yLog=False,cuts=cuts,Vtype=0,boost='med'),
                #Plot(name='mainBDT_v_VstarMass', distribution='h_bdtmCorr:h_MVHCorr',binsX=[0.0, 200.0, 250.0, 300.0, 350.0, 1200.0],xTitle='m(Vh) [GeV]',binsY=[-1.0, -0.75, -0.6666666662151164, -0.5833333324302327, -0.499999998645349, -0.41666666486046533, -0.33333333107558166, -0.249999997290698, -0.16666666350581427, -0.08333332972093066, 4.063952951938177e-09, 0.08333333784883667, 0.1666666716337204, 1.0],yTitle='BDT',yLog=False,cuts=cuts,Vtype=1,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='h_bdttCorr:h_MVHCorr',binsX=[0.0, 350.0, 400.0, 450.0, 500.0, 550.0, 1200.0],xTitle='m(Vh) [GeV]',binsY=[-1.0, -0.5833333134651184, -0.49999998103488574, -0.4166666486046531, -0.33333331617442047, -0.2499999837441878, -0.16666665131395514, -0.08333331888372253, 1.3546510135853396e-08, 0.0833333459767428, 0.16666667840697547, 0.25000001083720813, 0.3333333432674408, 1.0],yTitle='BDT',yLog=False,cuts=cuts,Vtype=0,boost='high'),
				#Plot(name='mainBDT_v_VstarMass', distribution='h_bdttCorr:h_MVHCorr',binsX=[0.0, 300.0, 350.0, 400.0, 450.0, 500.0, 550.0, 600.0, 1200.0],xTitle='m(Vh) [GeV]',binsY=[-1.0, -0.5833333134651184, -0.4999999821186066, -0.41666665077209475, -0.33333331942558286, -0.24999998807907103, -0.1666666567325592, -0.08333332538604732, 5.960464455334602e-09, 0.08333333730697634, 0.16666666865348823, 0.25, 1.0],yTitle='BDT',yLog=False,cuts=cuts,Vtype=1,boost='high'),
							
			]
    else:
        for Vtype in doVtypes:
            for cuts in doCuts:
                yields[cuts][Vtype]={}
                for boost in doBoosts:
                    yields[cuts][Vtype][boost]={}

                    if doCutTable:
                        plots+=[Plot(name='dummy',distribution='H.pt',nBinsX=1,xMin=0,xMax=500000,cuts=cuts,Vtype=Vtype,boost=boost)]
                    else:
                        plots+=[

                            #Plot(name='h_mass',distribution='H.mass',nBinsX=25,xMin=0,xMax=500,xTitle='m(h) [GeV]',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='x_mVH',distribution='x_mVH',nBinsX=40,xMin=0,xMax=1200,xTitle='m(VH) [GeV]',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),

                            #Plot(name='hMass_v_VstarMass',distribution='H.mass:x_mVH',binsX=[0]+range(300,700,25)+range(700,1001,100)+[1200],xTitle='m(Vh) [GeV]',binsY=[0,50]+range(75,175,10)+range(175,251,25),yTitle='m(h) [GeV]',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='hMass_v_VstarMass',distribution='H.mass:x_mVH',nBinsX=20,xMin=0,xMax=1000,xTitle='m(Vh) [GeV]',nBinsY=20,yMin=0,yMax=500,yTitle='m(h) [GeV]',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost)                    

                            #Plot(name='BDT_8TeV_H125Sig_NewTTbarBkg',distribution='BDT_8TeV_H125Sig_NewTTbarBkg_newCuts4',nBinsX=25,xMin=-1,xMax=1,xTitle='BDT',yLog=True,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='BDT_8TeV_H125Sig_0b1b2bWjetsBkg',distribution='BDT_8TeV_H125Sig_0b1b2bWjetsBkg_newCuts4',nBinsX=25,xMin=-1,xMax=1,xTitle='BDT',yLog=True,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='BDT_8TeV_H125Sig_VVBkg',distribution='BDT_8TeV_H125Sig_VVBkg_newCuts4',nBinsX=25,xMin=-1,xMax=1,xTitle='BDT',yLog=True,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4',nBinsX=25,xMin=-1,xMax=1,xTitle='BDT',yLog=True,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='allBDTs',distribution=BDTStitching,nBinsX=60,xMin=BDTMin,xMax=BDTMax,xTitle='BDT',yLog=True,cuts=cuts,Vtype=Vtype,boost=boost),

                            #Plot(name='mainBDT_v_VstarMass',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[200,400,450,500,550,600,700,850,1200],xTitle='m(Vh) [GeV]',binsY=[-1,-0.4,-0.2,0,0.1,0.2,1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='mainBDT_v_VstarMass',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',nBinsX=15,xMin=200,xMax=1200,xTitle='m(Vh) [GeV]',nBinsY=25,yMin=-1,yMax=1,yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='allBDTs_v_VstarMass',distribution=BDTStitching+':x_mVH',                                   nBinsX=15,xMin=200,xMax=1200,xTitle='m(Vh) [GeV]',nBinsY=40,yMin=0,yMax=BDTMax,yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='BDT_8TeV_H125Sig_NewTTbarBkg',distribution='BDT_8TeV_H125Sig_NewTTbarBkg_newCuts4',nBinsX=25,xMin=-1,xMax=1,xTitle='BDT',yLog=True,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='BDT_8TeV_H125Sig_0b1b2bWjetsBkg',distribution='BDT_8TeV_H125Sig_0b1b2bWjetsBkg_newCuts4',nBinsX=25,xMin=-1,xMax=1,xTitle='BDT',yLog=True,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='BDT_8TeV_H125Sig_VVBkg',distribution='BDT_8TeV_H125Sig_VVBkg_newCuts4',nBinsX=25,xMin=-1,xMax=1,xTitle='BDT',yLog=True,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4',nBinsX=25,xMin=-1,xMax=1,xTitle='BDT',yLog=True,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='allBDTs',distribution=BDTStitching,nBinsX=60,xMin=BDTMin,xMax=BDTMax,xTitle='BDT',yLog=True,cuts=cuts,Vtype=Vtype,boost=boost),

                            #Plot(name='MELA_SM',          distribution='MELA_SM',nBinsX=25,xMin=0,xMax=.015, xTitle='L(0^{+})',     yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='MELA_SM_smallXMax',distribution='MELA_SM',nBinsX=25,xMin=0,xMax=.003, xTitle='L(0^{+})',     yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='MELA_PS',          distribution='MELA_PS',nBinsX=25,xMin=0,xMax=50000,xTitle='L(0^{-})',     yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='MELA_HO_smallXMax',distribution='MELA_HO',nBinsX=25,xMin=0,xMax=10000,xTitle='L(0^{+}_{HO})',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='MELA_HO',          distribution='MELA_HO',nBinsX=25,xMin=0,xMax=20000,xTitle='L(0^{+}_{HO})',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),

                            #Plot(name='MELA_SMvPS',distribution=MELA_SMvPSmed,nBinsX=25,xMin=0,xMax=1, xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',          yLog=False,cuts=cuts,Vtype=Vtype,boost='med'),
                            #Plot(name='MELA_SMvPS',distribution=MELA_SMvPShigh,nBinsX=25,xMin=0,xMax=1, xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',          yLog=False,cuts=cuts,Vtype=Vtype,boost='high'),
                            #Plot(name='MELA_SMvHO',distribution=MELA_SMvHOmed,nBinsX=25,xMin=0,xMax=1, xTitle='L(0^{+}_{HO})/(L(0^{+})+L(0^{+}_{HO}))',yLog=False,cuts=cuts,Vtype=Vtype,boost='med'),
                            #Plot(name='MELA_SMvHO',distribution=MELA_SMvHOhigh,nBinsX=25,xMin=0,xMax=1, xTitle='L(0^{+}_{HO})/(L(0^{+})+L(0^{+}_{HO}))',yLog=False,cuts=cuts,Vtype=Vtype,boost='high'),

                            #Plot(name='hMass_v_VstarMass',distribution='H.mass:x_mVH',nBinsX=25,xMin=0,xMax=1000,xTitle='m(Vh) [GeV]',nBinsY=25,yMin=0,yMax=500,yTitle='m(h) [GeV]',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='hMass_v_VstarMass',distribution='H.mass:x_mVH',binsX=[0]+range(300,700,25)+range(700,1001,100),xTitle='m(Vh) [GeV]',binsY=[0,50]+range(75,175,10)+range(175,251,25),yTitle='m(h) [GeV]',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),

                            #Plot(name='hMass_v_VstarMass',distribution='H.mass:x_mVH',nBinsX=20,xMin=0,xMax=1000,xTitle='m(Vh) [GeV]',nBinsY=20,yMin=0,yMax=500,yTitle='m(h) [GeV]',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost)
                            #Plot(name='mainBDT_v_VstarMass',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',nBinsX=15,xMin=200,xMax=1200,xTitle='m(Vh) [GeV]',nBinsY=25,yMin=-1,yMax=1,yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='allBDTs_v_VstarMass',distribution=BDTStitching+':x_mVH',                                   nBinsX=15,xMin=200,xMax=1200,xTitle='m(Vh) [GeV]',nBinsY=40,yMin=0,yMax=BDTMax,yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='allBDTs_v_MELA_SMvPS',distribution=BDTStitching+':'+MELA_SMvPS,nBinsX=15,xMin=0,xMax=1, xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',nBinsY=40,yMin=0,yMax=BDTMax,yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),

                            #Plot(name='nPVs',distribution='nPVs',nBinsX=60,xMin=0,xMax=60,xTitle='nPVs',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='h_pT',distribution='H.pt',nBinsX=25,xMin=0,xMax=500,xTitle='p_{T}(h) [GeV]',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='h_mass',distribution='H.mass',nBinsX=25,xMin=0,xMax=500,xTitle='m(h) [GeV]',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='h_eta',distribution='H.eta',nBinsX=20,xMin=-4,xMax=4,xTitle='#eta(h)',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='h_dRjj',distribution='H.dR',nBinsX=20,xMin=0,xMax=10,xTitle='#deltaR(j_{1},j_{2})',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='hJet1_ptCorr',distribution='hJet_ptCorr[0]',nBinsX=25,xMin=0,xMax=500,xTitle='p_{T}(j_{1}) [GeV]',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='hJet2_ptCorr',distribution='hJet_ptCorr[1]',nBinsX=25,xMin=0,xMax=500,xTitle='p_{T}(j_{2}) [GeV]',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='hJet1_csv',distribution='hJet_csv[0]',nBinsX=25,xMin=0,xMax=1,xTitle='csv(j_{1}) [GeV]',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='hJet2_csv',distribution='hJet_csv[1]',nBinsX=25,xMin=0,xMax=1,xTitle='csv(j_{2}) [GeV]',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='V_pT',distribution='V.pt',nBinsX=25,xMin=0,xMax=500,xTitle='p_{T}(V) [GeV]',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='METtype1corr_et',distribution='METtype1corr.et',nBinsX=25,xMin=0,xMax=500,xTitle='E_{T}^{miss} [GeV]',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='METtype1corr_sig',distribution='METtype1corr.sig',nBinsX=25,xMin=0,xMax=10,xTitle='E_{T}^{miss} significance',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='naJets',distribution='naJets',nBinsX=20,xMin=0,xMax=30,xTitle='N_{aj}',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='nalep',distribution='nalep',nBinsX=20,xMin=0,xMax=20,xTitle='N_{al}',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='hVdPhi',distribution='HVdPhi',nBinsX=20,xMin=0,xMax=3.3,xTitle='#Delta#phi(V,h)',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='lMETdPhi',distribution='lMETdPhi',nBinsX=20,xMin=-3.3,xMax=3.3,xTitle='#Delta#phi(E_{T}^{miss},l)',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='x_costheta1',distribution='x_costheta1',nBinsX=20,xMin=-1,xMax=1,xTitle='Cos(#theta_{1})',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='x_costheta2',distribution='x_costheta2',nBinsX=20,xMin=-1,xMax=1,xTitle='Cos(#theta_{2})',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='x_phi',distribution='x_phi',nBinsX=20,xMin=-3.3,xMax=3.3,xTitle='#phi',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='x_costhetastar',distribution='x_costhetastar',nBinsX=20,xMin=0,xMax=1,xTitle='Cos(#theta*)',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='x_phi1',distribution='x_phi1',nBinsX=20,xMin=-3.3,xMax=3.3,xTitle='#phi_{1}',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='x_mVh',distribution='x_mVH',nBinsX=25,xMin=0,xMax=1200,xTitle='m(Vh) [GeV]',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            #Plot(name='x_rapidityVh',distribution='x_rapidityVH',nBinsX=20,xMin=-3,xMax=3,xTitle='y(Vh)',yLog=False,cuts=cuts,Vtype=Vtype,boost=boost),
                            ]

    for plot in plots:
        if not plot.cuts in  yields.keys():                        yields[plot.cuts]={}
        if not plot.Vtype in yields[plot.cuts].keys():             yields[plot.cuts][plot.Vtype]={}
        if not plot.boost in yields[plot.cuts][plot.Vtype].keys(): yields[plot.cuts][plot.Vtype][plot.boost]={}

        y=plot.Prepare()
        print plot.cuts, plot.Vtype, plot.boost
        try: yields[plot.cuts][plot.Vtype][plot.boost]=y
        except: pass
        plot.Draw()
        #plot.Write()
        
        if makeDataCard:
            dataCard.appendChannel('Vtype'+str(plot.Vtype)+'_'+plot.boost+'Boost',y)
    pickle.dump(yields,open(outputDir+'/yields.p','wb'))

    stdout_old = sys.stdout
    logFile = open(outputDir + '/log.txt','a')
    sys.stdout = logFile

    cWidth=15; nameWidth=30
    for Vtype in doVtypes:
        for cuts in doCuts:
            print ("VTYPE:"+str(Vtype)).ljust(nameWidth+(2*cWidth+1))
            print ("CUTS:"+cuts).ljust(nameWidth+(2*cWidth+1))
            print "".ljust(nameWidth),
            for boost in doBoosts: print boost.ljust(cWidth),
            print
            for histName in ['Z_light','Z_b','Z_bb','ttbar','VZ','VV']:
                print histName.ljust(nameWidth),
                try:
                    for boost in doBoosts:
                        print str(round(yields[cuts][Vtype][boost][histName],2)).ljust(cWidth),
                except: pass
                print
            for sample in allSamples:
                #if sample.isData: continue
                print sample.name.ljust(nameWidth),
                try:
                    for boost in doBoosts:
                        print str(round(yields[cuts][Vtype][boost][sample.name],2)).ljust(cWidth),
                except: pass
                print
            for sample in ['Total Background','Data']:
                print sample.replace(' ','_').ljust(nameWidth),
                try:
                    for boost in doBoosts:
                        print str(round(yields[cuts][Vtype][boost][sample],2)).ljust(cWidth),
                    print
                except: pass
            print 'Data/Background'.ljust(nameWidth),
            for boost in doBoosts:
                try: print str(round(yields[cuts][Vtype][boost]['Data']/yields[cuts][Vtype][boost]['Total Background'],3)).ljust(cWidth),
                except: pass
            print 3*'\n'

    sys.stdout = stdout_old
    logFile.close()

    if makeDataCard:
        #sys.stdout=open(cardFile,'w')
        #dataCard.construct(sys.stdout)
        dataCard.distribution='_'.join(plots[0].name.split('_')[:-2])
        dataCard.construct()
        dataCard.toTxt(cardFile)
             



    
