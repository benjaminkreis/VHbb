from copy import deepcopy
from glob import glob
from ROOT import *
from utils import *

class Sample:

    def __init__(self,name,sampleType=None,inputDir=None,fileIdentifier='',altName=None,channel=None,systematic=''):
        self.name=name;  self.inputDir=inputDir; self.fileIdentifier=fileIdentifier; self.altName=altName; self.channel=channel

        if name==sampleType: print "WARNING: sample name equals sample type:", sample.name

        self.setType(sampleType)

        self.systematic=systematic
        
        
    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def setType(self,sampleType):
        if type(sampleType)!=type(''): return

        self.type=sampleType

        self.isData=False; self.isMC=False; self.isSignal=False; self.isBackground=False;
        if isEqual(self.type,'data'):
            self.isData=True
        elif isEqual(self.type,'signal'):
            self.isMC=True
            self.isSignal=True
        else:
            self.isMC=True
            self.isBackground=True

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def setInputList(self,path):
        if not self.inputDir:
            print "No inputDir specified for sample:",self.name
            return

        path+='/'+self.inputDir+'/*'+self.fileIdentifier+'*.root'
        #if self.fileIdentifier.startswith("Merged") or self.fileIdentifier.startswith("Zee") or self.fileIdentifier.startswith("Zmm"): path ='/eos/uscms/store/user/ntran/VHbb/Zll_step4/102114/'+self.inputDir+'/*'+self.fileIdentifier+'*.root'
        self.inputList=glob(path)

        if len(self.inputList)==0:
            print "No input files found for sample:",self.name,"matching",path
            return

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def makeTChain(self,treeName):
        if not self.inputList:
            print "No inputList specified for sample:",self.name

        self.chain=TChain(treeName)
        for file in self.inputList:
            self.chain.Add(file)

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def clone(self,name):
        theClone=deepcopy(self)
        theClone.name=name
        return theClone

################################################################################################################################################

#name,sampleType,inputDir,fileIdentifier,altName,channel):

Zh_125p6_0P=Sample('Zh_125p6_0P','signal','/','ZHiggs0P_M-125p6_8TeV-JHUGenV4-private_nominal','Zh (CP = 0^{+})')
Zh_125p6_0M=Sample('Zh_125p6_0M','signal','/','ZHiggs0M_M-125p6_8TeV-JHUGenV4-private_nominal','Zh (CP = 0^{-})')

WZ=Sample('WZ','VZ','/','WZ_TuneZ2star_8TeV_pythia6_tauola_nominal')
ZZ=Sample('ZZ','VZ','/','ZZ_TuneZ2star_8TeV_pythia6_tauola_nominal')
WW=Sample('WW','VV','/','WW_TuneZ2star_8TeV_pythia6_tauola_nominal')

diboson=[WZ,ZZ,WW]

"""
DYJets_PtZ50to70=Sample('DYJetsToLL_PtZ-50To70','ZJets','/', 'DYJetsToLL_PtZ-50To70_TuneZ2star_8TeV-madgraph-tarball_nominal')
DYJets_PtZ70to100=Sample('DYJetsToLL_PtZ-70To100','ZJets','/', 'DYJetsToLL_PtZ-70To100_TuneZ2star_8TeV-madgraph-tarball_nominal')
DYJets_PtZ100=Sample('DYJetsToLL_PtZ-100','ZJets','/', 'DYJetsToLL_PtZ-100_TuneZ2star_8TeV-madgraph_nominal')
DYJets_HT200to400=Sample('DYJetsToLL_HT-200To400','ZJets','/', 'DYJetsToLL_HT-200To400_TuneZ2Star_8TeV-madgraph_nominal')
DYJets_HT400toInf=Sample('DYJetsToLL_HT-400ToInf','ZJets','/', 'DYJetsToLL_HT-400ToInf_TuneZ2Star_8TeV-madgraph_procV2_nominal')
DYJets_M50=Sample('DYJetsToLL_M-50','ZJets','/', 'DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball_nominal')
DY1Jets_M50=Sample('DY1JetsToLL_M-50','ZJets','/', 'DY1JetsToLL_M-50_TuneZ2Star_8TeV-madgraph_procV2_mergeV1V2_nominal')
DY2Jets_M50=Sample('DY2JetsToLL_M-50','ZJets','/', 'DY2JetsToLL_M-50_TuneZ2Star_8TeV-madgraph_nominal')
DY3Jets_M50=Sample('DY3JetsToLL_M-50','ZJets','/', 'DY3JetsToLL_M-50_TuneZ2Star_8TeV-madgraph_nominal')
DY4Jets_M50=Sample('DY4JetsToLL_M-50','ZJets','/', 'DY4JetsToLL_M-50_TuneZ2Star_8TeV-madgraph_mergeV1V2_nominal')

Zjets=[DYJets_PtZ50to70,DYJets_PtZ70to100,DYJets_PtZ100,DYJets_HT200to400,DYJets_HT400toInf,DYJets_M50,DY1Jets_M50,DY2Jets_M50,DY3Jets_M50,DY4Jets_M50]
"""
Zjets=[Sample('MergedDY','ZJets','/', 'Merged_DY_nominal')]

TTbar_FullLept=Sample('TTbar_FullLept','ttbar','/','TTJets_FullLeptMGDecays_8TeV-madgraph_nominal')
TTbar_SemiLept=Sample('TTbar_SemiLept','ttbar','/','TTJets_SemiLeptMGDecays_8TeV-madgraph_nominal')
TTbar_Hadronic=Sample('TTbar_Hadronic','ttbar','/','TTJets_HadronicMGDecays_8TeV-madgraph_nominal')

ttbar=[TTbar_FullLept,TTbar_SemiLept,TTbar_Hadronic]


#Wh_125p6_0P=Sample('Wh_125p6_0P','signal','Ntuple_Step1V42_Step2Tag_EDMV42_Step2_V6_MC_varsAddedSummed_v19/nominal','WHiggs0P_M-125p6','Wh (CP = 0^{+})')
#Wh_125p6_0PH=Sample('Wh_125p6_0PH','signal','Ntuple_Step1V42_Step2Tag_EDMV42_Step2_V6_MC_varsAddedSummed_v19/nominal','WHiggs0PH_M-125p6')
#Wh_125p6_0M=Sample('Wh_125p6_0M','signal','Ntuple_Step1V42_Step2Tag_EDMV42_Step2_V6_MC_varsAddedSummed_v19/nominal','WHiggs0M_M-125p6','Wh (CP = 0^{-})')
#Wh_125p6_0Mf05ph0=Sample('Wh_125p6_0Mf05ph0','signal','Ntuple_Step1V42_Step2Tag_EDMV42_Step2_V6_MC_varsAddedSummed_v19/nominal','WHiggs0Mf05ph0_M-125p6','Wh (CP mixed 50/50)')
#signals=[Wh_125p6_0P,Wh_125p6_0PH,Wh_125p6_0M,Wh_125p6_0Mf05ph0]

#WJets=Sample('WJetsInclusive','WJets','Ntuple_Step1V42_Step2Tag_EDMV42_Step2_V6_MC_varsAddedSummed_v19/nominal/WJets_boostedMG_lumiWeighted')#not in ZH

#singleTop_sChannel=Sample('singleTop_sChannel','singleTop','Ntuple_Step1V42_Step2Tag_EDMV42_Step2_V6_MC_varsAddedSummed_v19/nominal/SingleTop_sChannel_lumiWeighted')
#singleTop_tChannel=Sample('singleTop_tChannel','singleTop','Ntuple_Step1V42_Step2Tag_EDMV42_Step2_V6_MC_varsAddedSummed_v19/nominal/SingleTop_tChannel_lumiWeighted')
#singleTop_tW=Sample('singleTop_tW','singleTop','Ntuple_Step1V42_Step2Tag_EDMV42_Step2_V6_MC_varsAddedSummed_v19/nominal/SingleTop_tW_lumiWeighted')

#singleTop=[singleTop_sChannel,singleTop_tChannel,singleTop_tW]

#QCD_BCtoE=Sample('QCD_BCtoE','QCD','Ntuple_Step1V42_Step2Tag_EDMV42_Step2_V6_MC_varsAddedSummed_v19/nominal/QCD_BCtoE_80toInf_lumiWeighted',channel='el')
#QCD_Inclusive=Sample('QCD_Inclusive','QCD','Ntuple_Step1V42_Step2Tag_EDMV42_Step2_V6_MC_varsAddedSummed_v19/nominal/QCD_Inclusive_50toInf_lumiWeighted',channel='el')   #FIXME - Is this correct?
#QCD_MuEnriched=Sample('QCD_MuEnriched','QCD','Ntuple_Step1V42_Step2Tag_EDMV42_Step2_V6_MC_varsAddedSummed_v19/nominal/QCD_MuEnrichedPt5_80toInf_lumiWeighted',channel='mu')

#QCD=[QCD_BCtoE,QCD_MuEnriched]

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

dataEl=Sample('DataEl','Data','/','Zee_nominal',channel='el')
dataMu=Sample('DataMu','Data','/','Zmm_nominal',channel='mu')

data=[dataEl,dataMu]

#-----------------------------------------------------------------------------------------------------------------------------------------------

samplesForPlotting=[Zh_125p6_0P,Zh_125p6_0M]+diboson+Zjets+ttbar+data

#samplesForPlotting=[Wh_125p6_0P,Wh_125p6_0M,Wh_125p6_0Mf05ph0]+diboson+[WJets,ZJets]+ttbar+singleTop+QCD+data
#samplesForPlotting=[Wh_125p6_0P,Wh_125p6_0M,Wh_125p6_0Mf05ph0]+diboson+[ZJets]+ttbar+singleTop+QCD+data   #no W+Jets

allSamples=samplesForPlotting
#allSamples=samplesForPlotting+[Wh_125p6_0PH]


#-----------------------------------------------------------------------------------------------------------------------------------------------

#BEN FIXME blindly assuming there are none of these
#WJetsHW=Sample('WJets_shapeSys','WJets','Ntuple_Step1V42_Step2Tag_EDMV42_Step2_V6_MC_varsAddedSummed_v19/nominal/WJets_boostedHW_lumiWeighted',systematic='WJetsShapeUp')
#ttbarMCatNLO=Sample('ttbar_shapeSys','ttbar','Ntuple_Step1V42_Step2Tag_EDMV42_Step2_V6_MC_varsAddedSummed_v19/nominal/TTbar_mcAtNLO_lumiWeighted',systematic='ttbarShapeUp')
#systematicSamples=[WJetsHW,ttbarMCatNLO]
systematicSamples=[]

systematics=['JECDown','JECUp','JERDown','JERUp','btagDown','btagUp','mistagDown','mistagUp']
for sample in allSamples:
    if sample.isMC and not sample.systematic:
        for systematic in systematics:
            s=sample.clone(sample.name+'_'+systematic)
            s.systematic=systematic
            s.fileIdentifier=s.fileIdentifier.replace('nominal',systematic)
            #s.inputDir=s.inputDir.replace('nominal',systematic.replace('Up','_up').replace('Down','_down'))
            #if s.isSignal: s.inputDir+='/'+s.fileIdentifier+'_lumiWeighted'
            systematicSamples.append(s)

allSamples+=systematicSamples

