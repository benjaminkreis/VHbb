from utils import printTable
import pickle

#defaultDistribution='hMass_v_VstarMass_bdt'
#defaultDistribution='allBDTs_v_VstarMass_bdt'
defaultDistribution='mainBDT_v_VstarMass_bdt'

#defaultDistribution='h_mass_mjj'
#defaultDistribution='x_mVH_mjj'
#defaultDistribution='h_mass_bdt'
#defaultDistribution='x_mVH_bdt'

defaultSignalNames=['Zh_125p6_0P','Zh_125p6_0M']
defaultBackgroundNames=['Z_light','Z_b','Z_bb',
                 #'ZJets',
                 'ttbar',
                 #'singleTop',
                 #'QCD',
                 'VZ','VV','ggh']

none='-'
lumiSys='1.026'
leptonEffSys='1.03'
signalEWKSys0P='1.02'
signalEWKSys0M='1.10'
signalQCDSys='1.05'
backgroundNormSys='1.1'
#ZJetsSys='1.10'  #suggested by Seth
#singleTopSys='1.15'
dibosonSys='1.15'
#QCDSys='2'
qqbarPDFSys='1.01'
ggPDFSys='1.01'
METSys='1.03'  #FIX ME - should this be a shape uncertainty?
ggZhSys='1.2'

#FIX ME - Should there be QCD scale uncertainties?
flatSystematics=[('lumi',{'Zh_125p6_0P':lumiSys,'Zh_125p6_0M':lumiSys,'VZ':lumiSys,'VV':lumiSys}),
                 ('leptonEff',{'Zh_125p6_0P':leptonEffSys,'Zh_125p6_0M':leptonEffSys,'VZ':leptonEffSys,'VV':leptonEffSys}),
                 #('MET',{'Wh_OA125p6_0P':METSys,'Wh_125p6_0M':METSys,'ZJets':METSys,'singleTop':METSys,'QCD':METSys,'VZ':METSys,'VV':METSys}),
                 ('qqbarPDF',{'Zh_125p6_0P':qqbarPDFSys,'Zh_125p6_0M':qqbarPDFSys,'VZ':qqbarPDFSys,'VV':qqbarPDFSys}),
                 ('ggPDF',{'singleTop':ggPDFSys,'QCD':ggPDFSys}),
                 ('signalBoostEWK',{'Zh_125p6_0P':signalEWKSys0P,'Zh_125p6_0M':signalEWKSys0M}),
                 ('signalBoostQCD',{'Zh_125p6_0P':signalQCDSys,'Zh_125p6_0M':signalQCDSys}),
                 ('ZlightNorm',{'Z_light':backgroundNormSys}),
                 ('ZbNorm',{'Z_b':backgroundNormSys}),
                 ('ZbbNorm',{'Z_bb':backgroundNormSys}),
                 #('ZjetsNorm',{'ZJets':ZJetsSys}),
                 ('ttbarNorm',{'ttbar':backgroundNormSys}),
                 #('singleTopNorm',{'singleTop':singleTopSys}),
                 #('QCDNorm',{'QCD':QCDSys}),
                 ('dibosonNorm',{'VZ':dibosonSys,'VV':dibosonSys}),
                 ('ggZhSys',{'ggh':ggZhSys}),
                 ]

#FIX ME - we need systematic samples for signal
one='1'
shapeSystematics=[('JEC',{'Zh_125p6_0P':one,'Zh_125p6_0M':one,'Z_light':one,'Z_b':one,'Z_bb':one,'ttbar':one,'VZ':one,'VV':one}),
                  ('JER',{'Zh_125p6_0P':one,'Zh_125p6_0M':one,'Z_light':one,'Z_b':one,'Z_bb':one,'ttbar':one,'VZ':one,'VV':one}),
                  ('btag',{'Zh_125p6_0P':one,'Zh_125p6_0M':one,'Z_light':one,'Z_b':one,'Z_bb':one,'ttbar':one,'VZ':one,'VV':one}),
                  ('mistag',{'Zh_125p6_0P':one,'Zh_125p6_0M':one,'Z_light':one,'Z_b':one,'Z_bb':one,'ttbar':one,'VZ':one,'VV':one}),
                  #('stat_0P',{'Zh_125p6_0P':one}),
                  #('stat_0M',{'Zh_125p6_0M':one}),
                  #('stat_Z_light',{'Z_light':one}),
                  #('stat_Z_b',{'Z_b':one}),
                  #('stat_Z_bb',{'Z_bb':one}),
                  #('stat_ZJets',{'ZJets':one}),
                  #('stat_ttbar',{'ttbar':one}),
                  #('stat_singleTop',{'singleTop':one}),
                  #('stat_QCD',{'QCD':one}),
                  #('stat_VZ',{'VZ':one}),
                  #('stat_VV',{'VV':one}),
                  #('ttbarShape',{'ttbar':one}),
                  #('WJetsShape',{'W_light':one,'W_b':one,'W_bb':one}),
                  #('stat_ggZh',{'ggh':one}),
                  ]
                    
########################################################################

class Channel:

    def __init__(self, name, yields, signalNames, backgroundNames):
        self.name=name

        self.data=yields['Data']

        self.signals={}
        for key in signalNames:
            self.signals[key]=yields[key]
            
        self.backgrounds={}
        for key in backgroundNames:
            try: self.backgrounds[key]=yields[key]
            except: pass

        self.allProcesses=self.signals
        self.allProcesses.update(self.backgrounds)
        
########################################################################

class DataCard:

    def __init__(self, distribution=defaultDistribution, signalNames=defaultSignalNames, backgroundNames=defaultBackgroundNames):
        self.channels=[]
        self.data=[]

        self.distribution=distribution
        self.signalNames=signalNames
        self.backgroundNames=backgroundNames
        self.processNames=signalNames+backgroundNames

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def toTxt(self, fileName):
        out=open(fileName,'w')
        printTable(self.data,out)
        
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def fromDict(self, yields):
        for SR in yields.keys():
            for Vtype in yields[SR].keys():
                for boost in yields[SR][Vtype].keys():
                    self.appendChannel('Vtype'+str(Vtype)+'_'+boost+'Boost',yields[SR][Vtype][boost])
        
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def fromPickle(self,fileName='yields.p'):
        yields=pickle.load(open(fileName,'rb'))
        self.fromDict(yields)
        
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        
    def appendChannel(self, name, yields):

        channel=Channel(name, yields, self.signalNames, self.backgroundNames)
        self.channels.append(channel)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def nChannels(self): return len(self.channels)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    """
    imax 4
    jmax 1
    kmax *
    ----------------------------------------------------------------
    shapes *        * HGG_SM_WITHSYS_140_4cat.root $PROCESS_$CHANNEL  $PROCESS_$SYSTEMATIC_$CHANNEL
    shapes data_obs * HGG_SM_WITHSYS_140_4cat.root datmc_$CHANNEL
    ----------------------------------------------------------------
    bin          cat0   cat1   cat2  cat3
    observation  1718   2335   1765  2227
    ----------------------------------------------------------------
    bin                      cat0       cat0       cat1      cat1       cat2       cat2      cat3      cat3
    process                  sig        bkg        sig       bkg        sig        bkg       sig       bkg
    process                    0          1          0         1          0          1         0         1
    rate                     3.711     1710.59     3.266    2336.53     1.949     1792.63    1.624    2235.41
    ----------------------------------------------------------------
    lumi            lnN      1.04         -        1.04        -        1.04         -       1.04        -  #
    """

    def construct(self):
        line=['break']

        self.data.append(['imax',str(self.nChannels())])
        self.data.append(['jmax','*'])   #str(len(self.backgroundNames))])
        self.data.append(['kmax','*'])

        self.data.append(line)

        row=['Observation','','','']
        for channel in self.channels: row.append(str(channel.data))
        self.data.append(row)

        self.data.append(line)

        self.data.append(['shapes','','','','data_obs','*','plots.root',self.distribution+'_$CHANNEL__Data'])
        self.data.append(['shapes','','','','*',       '*','plots.root',self.distribution+'_$CHANNEL__$PROCESS',self.distribution+'_$CHANNEL__$PROCESS_$SYSTEMATIC'])
        
        self.data.append(line)

        row=['bin','']
        for channel in self.channels:
            for i in range(len(self.signalNames)+len(self.backgroundNames)):
                row.append(channel.name)
        self.data.append(row)

        row=['process','']
        for channelNo in range(self.nChannels()):
            for process in self.processNames:
                row.append(str(process))
        self.data.append(row)

        row=['process','']
        for channelNo in range(self.nChannels()):
            for processNo in range(1-len(self.signalNames),1+len(self.backgroundNames)):
                row.append(str(processNo))
        self.data.append(row)

        row=['rate','']
        for channel in self.channels:
            for process in self.processNames:
                try: row.append(str(channel.allProcesses[process]))
                except: row.append(0)
        self.data.append(row)

        self.data.append(line)

        for systematic,values in flatSystematics:
            row=[systematic,'lnN']
            for channel in self.channels:
                for process in self.processNames:
                    try: row.append(values[process])
                    except: row.append(none)
            self.data.append(row)

        self.data.append(line)
                
        for systematic,values in shapeSystematics:
            row=[systematic,'shape']
            for channel in self.channels:
                for process in self.processNames:
                    try: row.append(values[process])
                    except: row.append(none)
            self.data.append(row)

        """
        #Dummy systematics
        row=['1 lnN']
        for n in range(len(self.channels)): row+=['1.15','-','-','-']
        self.data.append(row)
        row=['2 lnN']
        for n in range(len(self.channels)): row+=['-','1.3','-','-']
        self.data.append(row)
        row=['3 lnN']
        for n in range(len(self.channels)): row+=['-','-','1.3','-']
        self.data.append(row)
        row=['4 lnN']
        for n in range(len(self.channels)): row+=['-','-','-','1.25']
        self.data.append(row)
        """



if __name__=='__main__':
    
    theCard=DataCard()
    theCard.fromPickle('forCombine/yields.p')
    theCard.construct()
    theCard.toTxt('test.txt')
