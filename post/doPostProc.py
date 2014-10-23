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
    inputDir='/eos/uscms/store/user/ntran/VHbb/Zll_step4/102214'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#SETTINGS

DEBUG=True#False

fillEmptyBins=False
blind=True
applyNormSFs=True
unroll2D=False#True

doBDT=True
do1stHalfBDT=False
do2ndHalfBDT=False

doCutTable=False
doTheta=False
makeDataCard=True

doAllSys=False#True
doJECSys=False
doJERSys=False
doBTagSys=False
doMisTagSys=False
doWJetsShapeSys=False
doTTbarShapeSys=False
doStatSys=False

doCuts=[
    'bdt',
    #'ZLight',
    #'Zbb',
    #'TTbar'
    ]

doVtypes=[
    0,
    1,
    #2,
    #3
    ]

doBoosts=[
    #'low',
    'med',
    'high'
    ]
'''
# Cascading BDT implementation 1
offset=1; cutTTbar=-0.35; cutWJet=0.0; cutVV=0.2
BDTMin=-1+offset
BDTMax=-1+offset+8
BDTStitching="""(({3}+BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4)*(BDT_8TeV_H125Sig_NewTTbarBkg_newCuts4<{0}))+\
((2+{3}+BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4)*((BDT_8TeV_H125Sig_NewTTbarBkg_newCuts4>{0})*(BDT_8TeV_H125Sig_0b1b2bWjetsBkg_newCuts4<{1})))+\
((4+{3}+BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4)*((BDT_8TeV_H125Sig_NewTTbarBkg_newCuts4>{0})*(BDT_8TeV_H125Sig_0b1b2bWjetsBkg_newCuts4>{1})*(BDT_8TeV_H125Sig_VVBkg_newCuts4<{2})))+\
((6+{3}+BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4)*((BDT_8TeV_H125Sig_NewTTbarBkg_newCuts4>{0})*(BDT_8TeV_H125Sig_0b1b2bWjetsBkg_newCuts4>{1})*(BDT_8TeV_H125Sig_VVBkg_newCuts4>{2})))\
""".format(cutTTbar,cutWJet,cutVV,offset)

medBoostBDTBins =linspace(-1+offset, -1+offset+0.7, 15).tolist() + [-1+offset+2] + linspace(-1+offset+2+0.45,-1+offset+2+0.9, 10).tolist() +[-1+offset+4] + linspace(-1+offset+4+0.55,-1+offset+4+1, 10).tolist() + [-1+offset+6] + linspace(-1+offset+6+0.6, -1+offset+6+1.1, 11).tolist() + [BDTMax]
highBoostBDTBins=linspace(-1+offset, -1+offset+0.7, 15).tolist() + [-1+offset+2] + linspace(-1+offset+2+0.45,-1+offset+2+1, 12).tolist() +[-1+offset+4] + linspace(-1+offset+4+0.55,-1+offset+4+1.05, 11).tolist() + [-1+offset+6] + linspace(-1+offset+6+0.6, -1+offset+6+1.2, 13).tolist() + [BDTMax]
'''
# Cascading BDT implementation 2
offset=1; cutTTbar=-0.35; cutWJet=0.0; cutVV=0.2
BDTMin=-1+offset
BDTMax=-1+offset+4
BDTStitching="""(({3}+BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4)*(BDT_8TeV_H125Sig_NewTTbarBkg_newCuts4<{0}))+\
((1+0.4+BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4)*((BDT_8TeV_H125Sig_NewTTbarBkg_newCuts4>{0})*(BDT_8TeV_H125Sig_0b1b2bWjetsBkg_newCuts4<{1})))+\
((2+BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4)*((BDT_8TeV_H125Sig_NewTTbarBkg_newCuts4>{0})*(BDT_8TeV_H125Sig_0b1b2bWjetsBkg_newCuts4>{1})*(BDT_8TeV_H125Sig_VVBkg_newCuts4<{2})))+\
((2+0.65+BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4)*((BDT_8TeV_H125Sig_NewTTbarBkg_newCuts4>{0})*(BDT_8TeV_H125Sig_0b1b2bWjetsBkg_newCuts4>{1})*(BDT_8TeV_H125Sig_VVBkg_newCuts4>{2})))\
""".format(cutTTbar,cutWJet,cutVV,offset)

medBoostBDTBins =linspace(0, 3, 49).tolist()
highBoostBDTBins=linspace(0, 3, 49).tolist()

kPSlow=4722955.231 #After averaging over e/mu and 0P/0M for lowBoost
kHOlow=1862001.840 #After averaging over e/mu and 0P/0M for lowBoost
kPSmed=7131743.071 #After averaging over e/mu and 0P/0M for medBoost
kHOmed=2410258.959 #After averaging over e/mu and 0P/0M for medBoost
kPShigh=13499645.703 #After averaging over e/mu and 0P/0M for highBoost
kHOhigh=3883419.8068 #After averaging over e/mu and 0P/0M for highBoost
MELA_SMvPSlow='MELA_PS/(({0}*MELA_SM) + MELA_PS)'.format(kPSlow)  #This arbitrary factor needs to be optimized
MELA_SMvHOlow='MELA_HO/(({0}*MELA_SM) + MELA_HO)'.format(kHOlow)
MELA_SMvPSmed='MELA_PS/(({0}*MELA_SM) + MELA_PS)'.format(kPSmed)
MELA_SMvHOmed='MELA_HO/(({0}*MELA_SM) + MELA_HO)'.format(kHOmed)
MELA_SMvPShigh='MELA_PS/(({0}*MELA_SM) + MELA_PS)'.format(kPShigh)
MELA_SMvHOhigh='MELA_HO/(({0}*MELA_SM) + MELA_HO)'.format(kHOhigh)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

showOverflow=True

doShapeComparison=False   #FIXME - not updated

elLumi=19040
muLumi=19040

sigmaFracUnc={}
sigmaFracUnc['VZ']=0.2
sigmaFracUnc['VV']=0.2
sigmaFracUnc['WJets']=0.2
sigmaFracUnc['ZJets']=0.2
sigmaFracUnc['ttbar']=0.15
sigmaFracUnc['singleTop']=0.15
sigmaFracUnc['QCD']=0.25
lumiFracUnc=.026   #2.6% for 8 TeV, 2.2% for 7 TeV (Jia Fu)

signalMagFrac=20

plotBackgrounds=['ZJets','ttbar','VV','VZ']
backgroundFillColors={'QCD':ROOT.kMagenta,'ZJets':ROOT.kYellow-7,'WJets':ROOT.kGreen-3,'singleTop':ROOT.kCyan-7,'ttbar':ROOT.kBlue-7,'VV':ROOT.kGray+2,'VZ':ROOT.kRed-7}
backgroundLineColors={'QCD':ROOT.kMagenta+1,'ZJets':ROOT.kYellow-4,'WJets':ROOT.kGreen-2,'singleTop':ROOT.kCyan-3,'ttbar':ROOT.kBlue-3,'VV':ROOT.kGray+3,'VZ':ROOT.kRed-4}

treeName='tree'
                
#---------------------------------------------------------------------------------------------------------------------------------------------
"""
if doTheta or makeDataCard:
    doVtypes=[2,3]
    doBoosts=['med','high']
    doCuts=['bdt']
    doCutTable=False
    
if doCutTable:
    doTheta=False
    makeDataCard=False
"""
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
				#Plot(name='h_mass',distribution='H.mass',binsX=[0]+linspace(40,240,21).tolist()+[500],xTitle='m(h) [GeV]',yLog=True,cuts=cuts,Vtype=Vtype,boost='med'),  
				#Plot(name='h_mass',distribution='H.mass',binsX=[0]+linspace(60,240,19).tolist()+[500],xTitle='m(h) [GeV]',yLog=True,cuts=cuts,Vtype=Vtype,boost='high'),

				#Plot(name='MELA_SMvPS_before',distribution=MELA_SMvPShigh,nBinsX=25,xMin=0,xMax=1, xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))', yLog=False,cuts=cuts,Vtype=Vtype,boost='med'),                
				#Plot(name='MELA_SMvPS_after',distribution=MELA_SMvPSmed,nBinsX=25,xMin=0,xMax=1, xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))', yLog=False,cuts=cuts,Vtype=Vtype,boost='med'),
				#Plot(name='MELA_SMvPS',distribution=MELA_SMvPSlow,nBinsX=25,xMin=0,xMax=1, xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))', yLog=False,cuts=cuts,Vtype=Vtype,boost='low'),
				#Plot(name='MELA_SMvPS',distribution=MELA_SMvPSmed,nBinsX=25,xMin=0,xMax=1, xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))', yLog=False,cuts=cuts,Vtype=Vtype,boost='med'),
				#Plot(name='MELA_SMvPS',distribution=MELA_SMvPShigh,nBinsX=25,xMin=0,xMax=1, xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))', yLog=False,cuts=cuts,Vtype=Vtype,boost='high'),
				#Plot(name='MELA_SMvHO',distribution=MELA_SMvHOmed,nBinsX=25,xMin=0,xMax=1, xTitle='L(0^{+}_{HO})/(L(0^{+})+L(0^{+}_{HO}))',yLog=False,cuts=cuts,Vtype=Vtype,boost='med'),
				#Plot(name='MELA_SMvHO',distribution=MELA_SMvHOhigh,nBinsX=25,xMin=0,xMax=1, xTitle='L(0^{+}_{HO})/(L(0^{+})+L(0^{+}_{HO}))',yLog=False,cuts=cuts,Vtype=Vtype,boost='high'),

				# mVh for AN
				#Plot(name='x_mVh',distribution='x_mVH',nBinsX=50,xMin=0,xMax=1200,xTitle='m(Vh) [GeV]',yLog=True,cuts=cuts,Vtype=2,boost='low'),	
				#Plot(name='x_mVh',distribution='x_mVH',nBinsX=50,xMin=0,xMax=1200,xTitle='m(Vh) [GeV]',yLog=True,cuts=cuts,Vtype=3,boost='low'),					
				#Plot(name='x_mVh',distribution='h_MVHCorr',nBinsX=30,xMin=0,xMax=1200,xTitle='m(Vh) [GeV]',yLog=True,cuts=cuts,Vtype=0,boost='med'),
				#Plot(name='x_mVh',distribution='h_MVHCorr',nBinsX=30,xMin=0,xMax=1200,xTitle='m(Vh) [GeV]',yLog=True,cuts=cuts,Vtype=1,boost='med'),
				#Plot(name='x_mVh',distribution='h_MVHCorr',nBinsX=30,xMin=0,xMax=1200,xTitle='m(Vh) [GeV]',yLog=True,cuts=cuts,Vtype=0,boost='high'),
				#Plot(name='x_mVh',distribution='h_MVHCorr',nBinsX=30,xMin=0,xMax=1200,xTitle='m(Vh) [GeV]',yLog=True,cuts=cuts,Vtype=1,boost='high'),
			
				# BDT for AN
				#Plot(name='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4',binsX=linspace(-1,-0.76,4).tolist()+linspace(-0.72,0.04,20).tolist()+[1],xTitle='BDT',yLog=True,cuts=cuts,Vtype=2,boost='low'),
				#Plot(name='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4',binsX=linspace(-1,-0.76,4).tolist()+linspace(-0.72,0.04,20).tolist()+[1],xTitle='BDT',yLog=True,cuts=cuts,Vtype=3,boost='low'),
				#Plot(name='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4',binsX=linspace(-1,-0.76,4).tolist()+linspace(-0.72,0.04,20).tolist()+[1],xTitle='BDT',yLog=True,cuts=cuts,Vtype=2,boost='med'),
				#Plot(name='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4',binsX=linspace(-1,-0.76,4).tolist()+linspace(-0.72,0.04,20).tolist()+[1],xTitle='BDT',yLog=True,cuts=cuts,Vtype=3,boost='med'),			
				#Plot(name='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4',binsX=linspace(-1,-0.76,4).tolist()+linspace(-0.72,0.2,24).tolist()+[1],xTitle='BDT',yLog=True,cuts=cuts,Vtype=2,boost='high'),
				#Plot(name='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4',binsX=linspace(-1,-0.76,4).tolist()+linspace(-0.72,0.2,24).tolist()+[1],xTitle='BDT',yLog=True,cuts=cuts,Vtype=3,boost='high'),

				# For Significance, nominal prime binning
				#Plot(name='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4',binsX=[-1]+linspace(-0.75, -0.15, 7).tolist()+[1],xTitle='BDT',yLog=True,cuts=cuts,Vtype=2,boost='med'),
				#Plot(name='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4',binsX=[-1]+linspace(-0.75, -0.15, 7).tolist()+[1],xTitle='BDT',yLog=True,cuts=cuts,Vtype=3,boost='med'),			
				#Plot(name='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4',binsX=[-1]+linspace(-0.75, 0.05, 9).tolist()+[1],xTitle='BDT',yLog=True,cuts=cuts,Vtype=2,boost='high'),
				#Plot(name='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4',binsX=[-1]+linspace(-0.75, 0.05, 9).tolist()+[1],xTitle='BDT',yLog=True,cuts=cuts,Vtype=3,boost='high'),

				# For Significance, uniform' global box mVH, rebinned
				#Plot(name='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4',binsX=[-1, -0.795918345451355, -0.7551020201709535, -0.714285694890552, -0.6734693696101507, -0.6326530443297492, -0.5918367190493478, -0.5510203937689464, -0.5102040684885449, -0.46938774320814347, -0.428571417927742, -0.3877550926473406, -0.3469387673669392, -0.3061224420865377, -0.26530611680613625, -0.2244897915257349, -0.18367346624533343, -0.14285714096493196, -0.1020408156845305, -0.06122449040412903, -0.020408162847161293, 1],xTitle='BDT',yLog=True,cuts=cuts,Vtype=2,boost='med'),
				#Plot(name='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4',binsX=[-1, -0.7551020383834839, -0.7142857313156128, -0.6734694038828214, -0.63265307645003, -0.5918367490172386, -0.5510204215844472, -0.5102040941516558, -0.46938776671886445, -0.42857143928607305, -0.38775511185328165, -0.34693878442049025, -0.30612245698769885, -0.26530612955490745, -0.2244898021221161, -0.1836734746893247, -0.1428571472565333, -0.10204081982374191, -0.06122449040412903, 1],xTitle='BDT',yLog=True,cuts=cuts,Vtype=3,boost='med'),			
				#Plot(name='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4',binsX=[-1, -0.7551020383834839, -0.7142857119441033, -0.6734693855047226, -0.632653059065342, -0.5918367326259613, -0.5510204061865807, -0.5102040797472001, -0.4693877533078194, -0.42857142686843874, -0.3877551004290581, -0.34693877398967743, -0.30612244755029683, -0.26530612111091617, -0.22448979467153551, -0.1836734682321549, -0.1428571417927742, -0.1020408153533936, -0.061224488914013, -0.020408162474632285, 0.020408163964748316, 0.06122449040412903, 1],xTitle='BDT',yLog=True,cuts=cuts,Vtype=2,boost='high'),
				#Plot(name='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4',binsX=[-1, -0.7551020383834839, -0.7142857120029236, -0.6734693856223634, -0.632653059241803, -0.5918367328612428, -0.5510204064806825, -0.5102040801001222, -0.469387753719562, -0.4285714273390017, -0.38775510095844146, -0.3469387745778812, -0.30612244819732093, -0.2653061218167606, -0.2244897954362004, -0.18367346905564008, -0.14285714267507987, -0.10204081629451955, -0.061224489913959235, -0.020408163533399026, 0.020408162847161293, 0.10204081982374191, 1],xTitle='BDT',yLog=True,cuts=cuts,Vtype=3,boost='high'),

				# SM search BDT binning (not exactly the same)
				#Plot(name='allBDTs',distribution=BDTStitching,binsX=medBoostBDTBins,xTitle='BDT',yLog=True,cuts=cuts,Vtype=2,boost='med'), 
				#Plot(name='allBDTs',distribution=BDTStitching,binsX=medBoostBDTBins,xTitle='BDT',yLog=True,cuts=cuts,Vtype=3,boost='med'), 
				#Plot(name='allBDTs',distribution=BDTStitching,binsX=highBoostBDTBins,xTitle='BDT',yLog=True,cuts=cuts,Vtype=2,boost='high'),
				#Plot(name='allBDTs',distribution=BDTStitching,binsX=highBoostBDTBins,xTitle='BDT',yLog=True,cuts=cuts,Vtype=3,boost='high'),
			
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(325,450,6).tolist()+[550,1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.75, -0.15, 7).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(400,900,11).tolist()+[1050,1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.75, 0.05, 9).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='high'),

				#First binning
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPSmed+')',binsX=[0]+linspace(0.1,0.8,11).tolist()+[0.85,1],xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=[-1]+linspace(-0.75, -0.15, 7).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='med'),
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPShigh+')',binsX=[0]+linspace(0.1,0.8,11).tolist()+[0.85,1],xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=[-1]+linspace(-0.75, -0.15, 7).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='high'),

				#Second binning
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPS+')',binsX=[0]+linspace(0.25,0.45,11).tolist()+[0.5,1],xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=[-1]+linspace(-0.75, -0.15, 7).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='med'),
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPS+')',binsX=[0]+linspace(0.35,0.75,11).tolist()+[0.85,1],xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=[-1]+linspace(-0.75, -0.15, 7).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='high'),

				#uniform
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPSmed+')',binsX=linspace(0,1,49).tolist(),xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=[-1]+linspace(-0.75, -0.15, 7).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='med'),
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPShigh+')',binsX=linspace(0,1,25).tolist(),xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=[-1]+linspace(-0.75, 0.05, 9).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='high'),

				#uniform : fine binning
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPSlow+')',binsX=linspace(0,1,50).tolist(),xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=linspace(-1, 1, 50).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='low'),
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPSmed+')',binsX=linspace(0,1,50).tolist(),xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=linspace(-1, 1, 50).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='med'),
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPShigh+')',binsX=linspace(0,1,50).tolist(),xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=linspace(-1, 1, 50).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='high'),

				#uniform modified for empty bins
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPSlow+')',binsX=linspace(0, 0.95,47).tolist()+[1],xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=[-1]+linspace(-0.75, -0.15, 7).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='low'),
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPSmed+')',binsX=linspace(0, 0.95,47).tolist()+[1],xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=[-1]+linspace(-0.75, -0.15, 7).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='med'),
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPShigh+')',binsX=[0]+linspace(0.083,1,23).tolist(),xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=[-1]+linspace(-0.75, 0.05, 9).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='high'),

				#nominal prime for KD
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPSmed+')',binsX=[0]+linspace(450./1200,575./1200,6).tolist()+[675./1200,1200./1200],xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=[-1]+linspace(-0.75, -0.15, 7).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='med'),
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPShigh+')',binsX=[0]+linspace(250./1200,750./1200,11).tolist()+[800./1200,1200./1200],xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=[-1]+linspace(-0.75, 0.05, 9).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='high'),

				#nominal prime KD from mVH
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPSmed+')',binsX=[0]+linspace(325./1200,450./1200,6).tolist()+[550./1200,1200./1200],xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=[-1]+linspace(-0.75, -0.15, 7).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='med'),
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPShigh+')',binsX=[0]+linspace(400./1200,900./1200,11).tolist()+[1050./1200,1200./1200],xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=[-1]+linspace(-0.75, 0.05, 9).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='high'),

				#nominal KD from mVH
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPSmed+')',binsX=[0]+linspace((266+2./3)/1200,(733+1./3)/1200,8).tolist()+[1200./1200],xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=[-1]+linspace(-0.76, -0.2, 8).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='med'),
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPShigh+')',binsX=[0]+linspace(400./1200,(933+1./3)/1200,9).tolist()+[(1066.+2./3)/1200,1200./1200],xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=[-1]+linspace(-0.76, 0.04, 11).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='high'),

				#larger floor KD from mVH
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPSmed+')',binsX=[0]+linspace((333+1./3)/1200,(666+2./3)/1200,6).tolist()+[1200./1200],xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=[-1]+linspace(-0.68, -0.28, 5).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='med'),
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPShigh+')',binsX=[0]+linspace((466+2./3)/1200,1000./1200,9).tolist()+[1200./1200],xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=[-1]+linspace(-0.68, -0.04, 9).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='high'),

				#course KD from mVH
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPSmed+')',binsX=[0]+linspace((266+2./3)/1200,(733+1./3)/1200,4).tolist()+[1200./1200],xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=[-1]+linspace(-0.76, -0.2, 4).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='med'),
				#Plot(name='mainBDT_v_SMvPS', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:('+MELA_SMvPShigh+')',binsX=[0]+linspace(400./1200,(933+1./3)/1200,5).tolist()+[(1066+2./3)/1200,1200./1200],xTitle='L(0^{-})/(L(0^{+})+L(0^{-}))',binsY=[-1]+linspace(-0.76, 0.04, 6).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='high'),

				#uniform mVH
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=linspace(0,1200,50).tolist(),xTitle='m(Vh) [GeV]',binsY=linspace(-1, 1, 50).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='low'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=linspace(0,1200,50).tolist(),xTitle='m(Vh) [GeV]',binsY=linspace(-1, 1, 50).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='low'),
				#Plot(name='mainBDT_v_VstarMass', distribution='h_bdtmCorr:h_MVHCorr',binsX=linspace(0,1200,50).tolist(),xTitle='m(Vh) [GeV]',binsY=linspace(-1, 1, 50).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=0,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='h_bdtmCorr:h_MVHCorr',binsX=linspace(0,1200,50).tolist(),xTitle='m(Vh) [GeV]',binsY=linspace(-1, 1, 50).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=1,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='h_bdttCorr:h_MVHCorr',binsX=linspace(0,1200,50).tolist(),xTitle='m(Vh) [GeV]',binsY=linspace(-1, 1, 50).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=0,boost='high'),
				#Plot(name='mainBDT_v_VstarMass', distribution='h_bdttCorr:h_MVHCorr',binsX=linspace(0,1200,50).tolist(),xTitle='m(Vh) [GeV]',binsY=linspace(-1, 1, 50).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=1,boost='high'),

				#uniform mVH, Coarser
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=linspace(0,1200,24).tolist(),xTitle='m(Vh) [GeV]',binsY=linspace(-1, 1, 24).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='low'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=linspace(0,1200,24).tolist(),xTitle='m(Vh) [GeV]',binsY=linspace(-1, 1, 24).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='low'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=linspace(0,1200,24).tolist(),xTitle='m(Vh) [GeV]',binsY=linspace(-1, 1, 24).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=linspace(0,1200,24).tolist(),xTitle='m(Vh) [GeV]',binsY=linspace(-1, 1, 24).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=linspace(0,1200,24).tolist(),xTitle='m(Vh) [GeV]',binsY=linspace(-1, 1, 24).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='high'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=linspace(0,1200,24).tolist(),xTitle='m(Vh) [GeV]',binsY=linspace(-1, 1, 24).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='high'),

				#uniformCoarser' global box mVH, rebinned
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=linspace(0,1200,24).tolist(),xTitle='m(Vh) [GeV]',binsY=linspace(-1, 1, 24).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='low'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=linspace(0,1200,24).tolist(),xTitle='m(Vh) [GeV]',binsY=linspace(-1, 1, 24).tolist(),yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='low'),
				Plot(name='mainBDT_v_VstarMass', distribution='h_bdtmCorr:h_MVHCorr',binsX=[0]+linspace(185,500,9).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.7, 0.05, 15).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=0,boost='med'),
				Plot(name='mainBDT_v_VstarMass', distribution='h_bdtmCorr:h_MVHCorr',binsX=[0]+linspace(175,525,10).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.7, 0.05, 15).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=1,boost='med'),
				Plot(name='mainBDT_v_VstarMass', distribution='h_bdttCorr:h_MVHCorr',binsX=[0]+linspace(200,560,9).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.65, 0.0, 14).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=0,boost='high'),
				Plot(name='mainBDT_v_VstarMass', distribution='h_bdttCorr:h_MVHCorr',binsX=[0]+linspace(235,515,9).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.65, 0.1, 15).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=1,boost='high'),

				#uniform' local box mVH
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(269.388,587.755,12).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.795918, -0.265306, 12).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='low'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(269.388,514.286,9).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.836735, -0.265306, 13).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='low'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(293,661,14).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.79, -0.1, 16).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(293,612,12).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.79, -0.06, 17).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(391.837,881.633,19).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.755102, -0.0204082, 16).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='high'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(367,906,21).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.71, 0.06, 18).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='high'),

				#uniform' global box mVH, single bin outside
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(293.877563477 , 587.755126953 , 11).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.795918345451 , -0.142857149243 , 15).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='low'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(269.387756348 , 636.734680176 , 14).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.795918345451 , -0.26530611515 , 12).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='low'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(293.877563477 , 636.734680176 , 13).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.795918345451 , -0.0612244904041 , 17).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(293.877563477 , 661.224487305 , 14).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.755102038383 , -0.102040819824 , 15).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(391.836730957 , 832.653076172 , 17).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.755102038383 , 0.0612244904041 , 19).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='high'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(367.346923828 , 906.122436523 , 21).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.755102038383 , 0.0612244904041 , 19).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='high'),

				#uniform' global box mVH, rebinned
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0, 293.8775634765625, 318.3673583984375, 342.8571533203125, 367.3469482421875, 391.8367431640625, 416.3265380859375, 440.8163330078125, 465.3061279296875, 489.7959228515625, 514.2857177734375, 538.7755126953125, 1200],xTitle='m(Vh) [GeV]',binsY=[-1, -0.9591836929321289, -0.918367326259613, -0.8367347121238708, -0.795918345451355, -0.7551020201709535, -0.714285694890552, -0.6734693696101507, -0.6326530443297492, -0.5918367190493478, -0.5510203937689464, -0.5102040684885449, -0.46938774320814347, -0.428571417927742, -0.3877550926473406, -0.3469387673669392, -0.3061224420865377, -0.26530611680613625, -0.2244897915257349, -0.18367346624533343, -0.14285714096493196, -0.1020408156845305, -0.06122449040412903, 1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='low'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0, 293.8775634765625, 318.36735916137695, 342.8571548461914, 367.34695053100586, 391.8367462158203, 416.32654190063477, 440.8163375854492, 465.3061332702637, 489.7959289550781, 563.2653198242188, 1200],xTitle='m(Vh) [GeV]',binsY=[-1, -0.9591836929321289, -0.8367347121238708, -0.795918345451355, -0.7551020201709535, -0.714285694890552, -0.6734693696101507, -0.6326530443297492, -0.5918367190493478, -0.5510203937689464, -0.5102040684885449, -0.46938774320814347, -0.428571417927742, -0.3877550926473406, -0.3469387673669392, -0.3061224420865377, -0.26530611680613625, -0.2244897915257349, -0.18367346624533343, -0.14285714096493196, -0.1020408156845305, -0.06122449040412903, 1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='low'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0, 318.3673400878906, 342.85713547926684, 367.346930870643, 391.8367262620192, 416.32652165339545, 440.8163170447716, 465.3061124361478, 489.79590782752405, 514.2857032189003, 538.7754986102764, 563.2652940016526, 587.7550893930288, 612.244884784405, 636.7346801757812, 1200],xTitle='m(Vh) [GeV]',binsY=[-1, -0.795918345451355, -0.7551020201709535, -0.714285694890552, -0.6734693696101507, -0.6326530443297492, -0.5918367190493478, -0.5510203937689464, -0.5102040684885449, -0.46938774320814347, -0.428571417927742, -0.3877550926473406, -0.3469387673669392, -0.3061224420865377, -0.26530611680613625, -0.2244897915257349, -0.18367346624533343, -0.14285714096493196, -0.1020408156845305, -0.06122449040412903, -0.020408162847161293, 1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0, 293.8775634765625, 318.3673565204327, 342.85714956430286, 367.3469426081731, 391.8367356520433, 416.32652869591345, 440.8163217397837, 465.30611478365387, 489.79590782752405, 514.2857008713943, 538.7754939152644, 563.2652869591346, 587.7550800030049, 612.244873046875, 661.2244873046875, 710.2041015625, 759.1836547851562, 1200],xTitle='m(Vh) [GeV]',binsY=[-1, -0.7551020383834839, -0.7142857313156128, -0.6734694038828214, -0.63265307645003, -0.5918367490172386, -0.5510204215844472, -0.5102040941516558, -0.46938776671886445, -0.42857143928607305, -0.38775511185328165, -0.34693878442049025, -0.30612245698769885, -0.26530612955490745, -0.2244898021221161, -0.1836734746893247, -0.1428571472565333, -0.10204081982374191, -0.06122449040412903, 1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0, 391.83673095703125, 416.32652646019346, 440.8163219633557, 465.3061174665179, 489.79591296968005, 514.2857084728423, 538.7755039760045, 563.2652994791666, 587.7550949823288, 612.244890485491, 636.7346859886533, 661.2244814918155, 685.7142769949777, 710.2040724981399, 734.693868001302, 759.1836635044642, 783.6734590076264, 808.1632545107886, 832.6530500139509, 857.1428455171131, 881.6326410202753, 906.1224365234375, 955.10205078125, 1200],xTitle='m(Vh) [GeV]',binsY=[-1, -0.7551020383834839, -0.7142857119441033, -0.6734693855047226, -0.632653059065342, -0.5918367326259613, -0.5510204061865807, -0.5102040797472001, -0.4693877533078194, -0.42857142686843874, -0.3877551004290581, -0.34693877398967743, -0.30612244755029683, -0.26530612111091617, -0.22448979467153551, -0.1836734682321549, -0.1428571417927742, -0.1020408153533936, -0.061224488914013, -0.020408162474632285, 0.020408163964748316, 0.06122449040412903, 1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='high'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0, 391.83673095703125, 416.32652791341144, 440.8163248697917, 465.3061218261719, 489.79591878255206, 514.2857157389323, 538.7755126953125, 563.2653096516926, 587.7551066080729, 612.2449035644531, 636.7347005208333, 661.2244974772135, 685.7142944335938, 710.2040913899739, 734.6938883463541, 759.1836853027344, 783.6734822591145, 808.1632792154948, 832.653076171875, 881.6326293945312, 930.6122436523438, 979.5918579101562, 1200],xTitle='m(Vh) [GeV]',binsY=[-1, -0.7551020383834839, -0.7142857120029236, -0.6734693856223634, -0.632653059241803, -0.5918367328612428, -0.5510204064806825, -0.5102040801001222, -0.469387753719562, -0.4285714273390017, -0.38775510095844146, -0.3469387745778812, -0.30612244819732093, -0.2653061218167606, -0.2244897954362004, -0.18367346905564008, -0.14285714267507987, -0.10204081629451955, -0.061224489913959235, -0.020408163533399026, 0.020408162847161293, 0.10204081982374191, 1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='high'),

				#uniform' global box mVH, rebinned, 2nd trial
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0, 293.8775634765625, 318.3673583984375, 342.8571533203125, 367.3469482421875, 391.8367431640625, 465.3061279296875, 514.2857177734375, 1200],xTitle='m(Vh) [GeV]',binsY=[-1, -0.918367326259613, -0.8367347121238708, -0.795918345451355, -0.7551020201709535, -0.714285694890552, -0.6734693696101507, -0.6326530443297492, -0.5918367190493478, -0.5510203937689464, -0.5102040684885449, -0.46938774320814347, -0.428571417927742, -0.3877550926473406, -0.3469387673669392, -0.3061224420865377, -0.26530611680613625, -0.2244897915257349, -0.18367346624533343, -0.14285714096493196, -0.1020408156845305, -0.06122449040412903, 1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='low'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0, 293.8775634765625, 318.36735916137695, 342.8571548461914, 367.34695053100586, 391.8367462158203, 416.32654190063477, 440.8163375854492, 465.3061332702637, 489.7959289550781, 563.2653198242188, 1200],xTitle='m(Vh) [GeV]',binsY=[-1, -0.9591836929321289, -0.8367347121238708, -0.795918345451355, -0.7551020201709535, -0.714285694890552, -0.6734693696101507, -0.6326530443297492, -0.5918367190493478, -0.5510203937689464, -0.5102040684885449, -0.46938774320814347, -0.428571417927742, -0.3877550926473406, -0.3469387673669392, -0.3061224420865377, -0.26530611680613625, -0.2244897915257349, -0.18367346624533343, -0.14285714096493196, -0.1020408156845305, -0.06122449040412903, 1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='low'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0, 318.3673400878906, 342.85713547926684, 367.346930870643, 391.8367262620192, 416.32652165339545, 440.8163170447716, 465.3061124361478, 489.79590782752405, 514.2857032189003, 538.7754986102764, 563.2652940016526, 587.7550893930288, 612.244884784405, 636.7346801757812, 1200],xTitle='m(Vh) [GeV]',binsY=[-1, -0.795918345451355, -0.7551020201709535, -0.714285694890552, -0.6734693696101507, -0.6326530443297492, -0.5918367190493478, -0.5510203937689464, -0.5102040684885449, -0.46938774320814347, -0.428571417927742, -0.3877550926473406, -0.3469387673669392, -0.3061224420865377, -0.26530611680613625, -0.2244897915257349, -0.18367346624533343, -0.14285714096493196, -0.1020408156845305, -0.06122449040412903, -0.020408162847161293, 1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0, 293.8775634765625, 318.3673565204327, 342.85714956430286, 367.3469426081731, 391.8367356520433, 416.32652869591345, 440.8163217397837, 465.30611478365387, 489.79590782752405, 514.2857008713943, 538.7754939152644, 563.2652869591346, 587.7550800030049, 612.244873046875, 661.2244873046875, 710.2041015625, 759.1836547851562, 1200],xTitle='m(Vh) [GeV]',binsY=[-1, -0.7551020383834839, -0.7142857313156128, -0.6734694038828214, -0.63265307645003, -0.5918367490172386, -0.5510204215844472, -0.5102040941516558, -0.46938776671886445, -0.42857143928607305, -0.38775511185328165, -0.34693878442049025, -0.30612245698769885, -0.26530612955490745, -0.2244898021221161, -0.1836734746893247, -0.1428571472565333, -0.10204081982374191, -0.06122449040412903, 1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0, 391.83673095703125, 416.32652646019346, 440.8163219633557, 465.3061174665179, 489.79591296968005, 514.2857084728423, 538.7755039760045, 563.2652994791666, 587.7550949823288, 612.244890485491, 636.7346859886533, 661.2244814918155, 685.7142769949777, 710.2040724981399, 734.693868001302, 759.1836635044642, 783.6734590076264, 808.1632545107886, 857.1428455171131, 906.1224365234375, 955.10205078125, 1200],xTitle='m(Vh) [GeV]',binsY=[-1, -0.7551020383834839, -0.7142857119441033, -0.6734693855047226, -0.632653059065342, -0.5918367326259613, -0.5510204061865807, -0.5102040797472001, -0.4693877533078194, -0.42857142686843874, -0.3877551004290581, -0.34693877398967743, -0.30612244755029683, -0.26530612111091617, -0.22448979467153551, -0.1836734682321549, -0.1428571417927742, -0.1020408153533936, -0.061224488914013, -0.020408162474632285, 0.020408163964748316, 0.06122449040412903, 1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='high'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0, 416.32652791341144, 440.8163248697917, 465.3061218261719, 489.79591878255206, 514.2857157389323, 538.7755126953125, 563.2653096516926, 587.7551066080729, 612.2449035644531, 636.7347005208333, 661.2244974772135, 685.7142944335938, 710.2040913899739, 734.6938883463541, 759.1836853027344, 783.6734822591145, 808.1632792154948, 832.653076171875, 881.6326293945312, 930.6122436523438, 979.5918579101562, 1200],xTitle='m(Vh) [GeV]',binsY=[-1, -0.7551020383834839, -0.7142857120029236, -0.6734693856223634, -0.632653059241803, -0.5918367328612428, -0.5510204064806825, -0.5102040801001222, -0.469387753719562, -0.4285714273390017, -0.38775510095844146, -0.3469387745778812, -0.30612244819732093, -0.2653061218167606, -0.2244897954362004, -0.18367346905564008, -0.14285714267507987, -0.10204081629451955, -0.061224489913959235, -0.020408163533399026, 0.020408162847161293, 0.10204081982374191, 1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='high'),

				#uniform' 20% stat mVH
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(293.878,465.306,6).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.795918,-0.0612245,17).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='low'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(244.898,465.306,8).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.795918,-0.428571,8).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='low'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0, 318.3673400878906, 342.8571350097656, 367.3469299316406, 391.83672485351565, 416.32651977539064, 440.8163146972656, 489.7959289550781, 514.2857055664062, 612.244873046875, 1200],xTitle='m(Vh) [GeV]',binsY=[-1, -0.9591836929321289, -0.7551020383834839, -0.7142857313156128, -0.6734693646430969, -0.6326530575752258, -0.5918367306391398, -0.5510204037030538, -0.5102040767669678, -0.4693877498308817, -0.4285714228947957, -0.3877550959587097, -0.34693876902262366, -0.30612244208653766, -0.26530611515045166, -0.22448979318141937, -0.18367347121238708, -0.1428571492433548, -0.10204081982374191, -0.06122449040412903, 0.020408162847161293, 1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0, 293.8775634765625, 318.3673400878906, 342.85713958740234, 367.34693908691406, 391.8367385864258, 416.3265380859375, 440.8163146972656, 465.3061218261719, 489.7959289550781, 538.7755126953125, 636.7346801757812, 1200],xTitle='m(Vh) [GeV]',binsY=[-1, -0.795918345451355, -0.7142857313156128, -0.6734693646430969, -0.6326530396938324, -0.5918367147445679, -0.5510203897953033, -0.5102040648460389, -0.4693877398967743, -0.4285714149475097, -0.3877550899982452, -0.3469387650489807, -0.3061224400997162, -0.26530611515045166, -0.22448979318141937, -0.18367347121238708, -0.1428571492433548, -0.10204081982374191, -0.020408162847161293, 1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0, 416.3265380859375, 440.8163350423177, 465.30613199869794, 489.7959289550781, 514.2857055664062, 538.7755126953125, 563.2653198242188, 587.755126953125, 612.244873046875, 661.2244873046875, 734.69384765625, 832.653076171875, 1126.5306396484375, 1200],xTitle='m(Vh) [GeV]',binsY=[-1, -0.8367347121238708, -0.6734693646430969, -0.6326530575752258, -0.5918367334774562, -0.5510204093796867, -0.5102040852819171, -0.46938776118414743, -0.42857143708637785, -0.3877551129886082, -0.3469387888908386, -0.30612245202064514, -0.26530611515045166, -0.22448979318141937, -0.18367347121238708, -0.10204081982374191, -0.020408162847161293, 0.1428571492433548, 1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='high'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0, 391.83673095703125, 416.3265380859375, 440.8163146972656, 465.3061157226563, 489.79591674804686, 514.2857177734375, 538.7755187988281, 563.2653198242188, 612.244873046875, 661.2244873046875, 734.69384765625, 808.1632690429688, 1200],xTitle='m(Vh) [GeV]',binsY=[-1, -0.7142857313156128, -0.6326530575752258, -0.5510203838348389, -0.4693877696990967, -0.4285714402794838, -0.3877551108598709, -0.346938781440258, -0.30612245202064514, -0.22448979318141937, -0.1428571492433548, -0.020408162847161293, 1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='high'),

				#nominal prime
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(275,450,8).tolist()+[550,1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.75, -0.15, 7).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='low'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(275,450,8).tolist()+[550,1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.75, -0.15, 7).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='low'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(300,500,9).tolist()+[550,1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.75, -0.15, 7).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(300,500,9).tolist()+[550,1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.75, -0.15, 7).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='med'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(400,900,11).tolist()+[1050,1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.75, 0.05, 9).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=2,boost='high'),
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(400,900,11).tolist()+[1050,1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.75, 0.05, 9).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=3,boost='high'),

				#nominal
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(266+2./3,733+1./3,8).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.76, -0.2, 8).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='med'),
				#Plot(name='mainBDT_v_VstarMass',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(400,933+1./3,9).tolist()+[1066+2./3,1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.76, 0.04, 11).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='high'),   

				#larger floor
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(333+1./3,666+2./3,6).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.68, -0.28, 5).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='med'),
				#Plot(name='mainBDT_v_VstarMass',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(466+2./3,1000,9).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.68, -0.04, 9).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='high'),   

				#coarse
				#Plot(name='mainBDT_v_VstarMass', distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(266+2./3,733+1./3,4).tolist()+[1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.76, -0.2, 4).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='med'),
				#Plot(name='mainBDT_v_VstarMass',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4:x_mVH',binsX=[0]+linspace(400,933+1./3,5).tolist()+[1066+2./3,1200],xTitle='m(Vh) [GeV]',binsY=[-1]+linspace(-0.76, 0.04, 6).tolist()+[1],yTitle='BDT',yLog=False,cuts=cuts,Vtype=Vtype,boost='high'), 
			
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
                        	# for AN, use makeDataCard version
							Plot(name='x_mVh',distribution='x_mVH',nBinsX=50,xMin=0,xMax=1200,xTitle='m(Vh) [GeV]',yLog=True,cuts=cuts,Vtype=Vtype,boost=boost),	
							Plot(name='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg',distribution='BDT_8TeV_H125Sig_LFHFWjetsNewTTbarVVBkg_newCuts4',binsX=linspace(-1,-0.76,4).tolist()+linspace(-0.72,0.04,20).tolist()+[1],xTitle='BDT',yLog=True,cuts=cuts,Vtype=Vtype,boost=boost),

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
             



    
