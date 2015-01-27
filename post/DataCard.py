from utils import printTable
import pickle

#defaultDistribution='hMass_v_VstarMass_bdt'
#defaultDistribution='allBDTs_v_VstarMass_bdt'
defaultDistribution='mainBDT_v_VstarMass_bdt'
#defaultDistribution='mainBDT_v_SMvPS_bdt'

#defaultDistribution='h_mass_mjj'
#defaultDistribution='x_mVH_mjj'
#defaultDistribution='h_mass_bdt'
#defaultDistribution='x_mVH_bdt'

defaultSignalNames=['Wh_125p6_0P','Wh_125p6_0M']
defaultBackgroundNames=['W_light','W_b','W_bb',
                        'Z_light','Z_b','Z_bb',
                        'ttbar','singleTop',
                        'VZ','VV',
                        'Zh_125p6_0P','ggZh']

none='-'
lumiSys='1.026'
leptonEffSys='1.03'
signalEWKSys0P='1.02'
signalEWKSys0M='1.10' # SS, 17 Oct 2014
signalQCDSys='1.05'
backgroundNormSys='1.1'
ZJetsSys='1.10'  #suggested by Seth
singleTopSys='1.15'
dibosonSys='1.15'
QCDSys='2'
QCDscale_VHSys='1.04'
QCDscale_VVSys='1.04'
QCDscale_ttbarSys='1.06'
qqbarPDFSys='1.01'
ggPDFSys='1.01'
METSys='1.03'
ggZHNormSys='.75/1.35'

flatSystematics=[('lumi_8TeV',{'Wh_125p6_0P':lumiSys,'Wh_125p6_0M':lumiSys,'Zh_125p6_0P':lumiSys,'Zh_125p6_0M':lumiSys,'ggZh':lumiSys,'singleTop':lumiSys,'QCD':lumiSys,'VZ':lumiSys,'VV':lumiSys}),
                 ('CMS_vhbb_eff_e',{'Wh_125p6_0P':leptonEffSys,'Wh_125p6_0M':leptonEffSys,'Zh_125p6_0P':leptonEffSys,'Zh_125p6_0M':leptonEffSys,'ggZh':leptonEffSys,'singleTop':leptonEffSys,'QCD':leptonEffSys,'VZ':leptonEffSys,'VV':leptonEffSys}),
                 ('CMS_vhbb_eff_m',{'Wh_125p6_0P':leptonEffSys,'Wh_125p6_0M':leptonEffSys,'Zh_125p6_0P':leptonEffSys,'Zh_125p6_0M':leptonEffSys,'ggZh':leptonEffSys,'singleTop':leptonEffSys,'QCD':leptonEffSys,'VZ':leptonEffSys,'VV':leptonEffSys}),
                 ('CMS_vhbb_MET',{'Wh_125p6_0P':METSys,'Wh_125p6_0M':METSys,'Zh_125p6_0P':METSys,'Zh_125p6_0M':METSys,'ggZh':METSys,'singleTop':METSys,'VZ':METSys,'VV':METSys}),
                 ('pdf_qqbar',{'Wh_125p6_0P':qqbarPDFSys,'Wh_125p6_0M':qqbarPDFSys,'Zh_125p6_0P':qqbarPDFSys,'Zh_125p6_0M':qqbarPDFSys,'VZ':qqbarPDFSys,'VV':qqbarPDFSys}),
                 ('pdf_gg',{'ggZh':ggPDFSys,'singleTop':ggPDFSys,'QCD':ggPDFSys}),
                 ('CMS_vhbb_boost_EWK',{'Wh_125p6_0P':signalEWKSys0P,'Wh_125p6_0M':signalEWKSys0M,'Zh_125p6_0P':signalEWKSys0P,'Zh_125p6_0M':signalEWKSys0M}),
                 ('CMS_vhbb_boost_QCD',{'Wh_125p6_0P':signalQCDSys,'Wh_125p6_0M':signalQCDSys,'Zh_125p6_0P':signalQCDSys,'Zh_125p6_0M':signalQCDSys}),
                 ('CMS_vhbb_wh_WlightNorm',{'W_light':backgroundNormSys}),
                 ('CMS_vhbb_wh_WbNorm',{'W_b':backgroundNormSys}),
                 ('CMS_vhbb_wh_WbbNorm',{'W_bb':backgroundNormSys}),
                 ('CMS_vhbb_wh_ZlightNorm',{'Z_light':ZJetsSys}),
                 ('CMS_vhbb_wh_ZbNorm',{'Z_b':ZJetsSys}),
                 ('CMS_vhbb_wh_ZbbNorm',{'Z_bb':ZJetsSys}),
                 ('CMS_vhbb_wh_ttbarNorm',{'ttbar':backgroundNormSys}),
                 ('CMS_vhbb_singleTopNorm',{'singleTop':singleTopSys}),
                 ('QCDscale_VH',{'Wh_125p6_0P':QCDscale_VHSys,'Wh_125p6_0M':QCDscale_VHSys,'Zh_125p6_0P':QCDscale_VHSys,'Zh_125p6_0M':QCDscale_VHSys}),
                 ('QCDscale_VV',{'VZ':QCDscale_VVSys,'VV':QCDscale_VVSys}),
                 ('QCDscale_ttbar',{'singleTop':QCDscale_ttbarSys}),
                 ('CMS_vhbb_dibosonNorm',{'VZ':dibosonSys,'VV':dibosonSys}),
                 ('CMS_vhbb_ggZhNorm',{'ggZh':ggZHNormSys}),
                 ]

one='1'
shapeSystematics=[('CMS_vhbb_scale_j',{'Wh_125p6_0P':one,'Wh_125p6_0M':one,'Zh_125p6_0P':one,'Zh_125p6_0M':one,'ggZh':one,'W_light':one,'W_b':one,'W_bb':one,'Z_light':one,'Z_b':one,'Z_bb':one,'ttbar':one,'singleTop':one,'QCD':one,'VZ':one,'VV':one}),
                  ('CMS_vhbb_res_j',{'Wh_125p6_0P':one,'Wh_125p6_0M':one,'Zh_125p6_0P':one,'Zh_125p6_0M':one,'ggZh':one,'W_light':one,'W_b':one,'W_bb':one,'Z_light':one,'Z_b':one,'Z_bb':one,'ttbar':one,'singleTop':one,'QCD':one,'VZ':one,'VV':one}),
                  ('CMS_vhbb_eff_b',{'Wh_125p6_0P':one,'Wh_125p6_0M':one,'Zh_125p6_0P':one,'Zh_125p6_0M':one,'ggZh':one,'W_light':one,'W_b':one,'W_bb':one,'Z_light':one,'Z_b':one,'Z_bb':one,'ttbar':one,'singleTop':one,'QCD':one,'VZ':one,'VV':one}),
                  ('CMS_vhbb_FakeRate_b',{'Wh_125p6_0P':one,'Wh_125p6_0M':one,'Zh_125p6_0P':one,'Zh_125p6_0M':one,'ggZh':one,'W_light':one,'W_b':one,'W_bb':one,'Z_light':one,'Z_b':one,'Z_bb':one,'ttbar':one,'singleTop':one,'QCD':one,'VZ':one,'VV':one}),
                  ('CMS_vhbb_wh_ttbar_shape',{'ttbar':one}),
                  ('CMS_vhbb_wh_W_light_shape',{'W_light':one}),
                  ('CMS_vhbb_wh_W_b_shape',{'W_b':one}),
                  ('CMS_vhbb_wh_W_bb_shape',{'W_bb':one}),
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
                    try: self.appendChannel('Vtype'+str(Vtype)+'_'+boost+'Boost',yields[SR][Vtype][boost])
                    except: print "Busted channel:",'Vtype'+str(Vtype)+'_'+boost+'Boost'
        
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
            type='lnN'
            #if 'ggZh' in systematic: type='gmN'
            row=[systematic,type]
            
            for channel in self.channels:
                for process in self.processNames:
                    if systematic == 'CMS_vhbb_eff_e' and channel.name.startswith('Vtype3'):
                    	try: row.append(values[process])
                    	except: row.append(none)
                    elif systematic == 'CMS_vhbb_eff_e' and channel.name.startswith('Vtype2'):
                    	row.append(none)
                    elif systematic == 'CMS_vhbb_eff_m' and channel.name.startswith('Vtype2'):
                    	try: row.append(values[process])
                    	except: row.append(none)
                    elif systematic == 'CMS_vhbb_eff_m' and channel.name.startswith('Vtype3'):
                    	row.append(none)
                    else:
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
