from ROOT import *

from Sample import *
#samples=samplesForPlotting
samples=allSamples
from cuts import *
from doPostProc import *
from scaleFactors import *
from utils import *

import os,sys

from array import array

d=os.environ['CMSSW_BASE']
gROOT.ProcessLine('.L '+d+'/src/VHbb/post/weightSignalNLO.C+')

PUWeight='PUweight'
#trigWeightEl='weightTrig2012SingleEle'
#trigWeightMu='weightTrig2012SingleMuon'
trigWeightEl='weightTrig2012'
trigWeightMu='weightTrig2012'

if not os.path.isdir(outputDir): os.system("mkdir -p "+outputDir)
output=TFile(outputDir+'/plots.root',"RECREATE")

TH1.SetDefaultSumw2(True)
TGaxis.SetMaxDigits(3)

class Plot:

    def __init__(self,name,distribution,binsX=None,nBinsX=100,xMin=0,xMax=100,xTitle='',binsY=None,nBinsY=100,yMin=0,yMax=100,yTitle='',yLog=True,cuts="bdt",Vtype=3,boost='med'):
        self.name=name; self.distribution=distribution; self.binsX=binsX; self.nBinsX=nBinsX; self.xMin=xMin; self.xMax=xMax; self.xTitle=xTitle; self.binsY=binsY; self.nBinsY=nBinsY; self.yMin=yMin; self.yMax=yMax; self.yTitle=yTitle; self.yLog=yLog; self.cuts=cuts; self.Vtype=Vtype; self.boost=boost

        self.is2D=(':' in self.distribution)
        self.is1D=not self.is2D

        if self.binsX:
            self.nBinsX=len(self.binsX)-1
            self.xMin=self.binsX[0]
            self.xMax=self.binsX[-1]

            if self.is2D:
                self.nBinsY=len(self.binsY)-1
                self.yMin=self.binsY[0]
                self.yMax=self.binsY[-1]
        else:
            self.binsX=[]
            for n in range(self.nBinsX+1):
                self.binsX.append(self.xMin+n*(float(self.xMax-self.xMin)/self.nBinsX))

            if self.is2D:
                self.binsY=[]
                for n in range(self.nBinsY+1):
                    self.binsY.append(self.yMin+n*(float(self.yMax-self.yMin)/self.nBinsY))

        self.binsX=array('f',self.binsX)
        if self.is2D: self.binsY=array('f',self.binsY)

        self.extraHists={}   #For Combine

        #make name unique
        self.name+='_'+self.cuts+'_Vtype'+str(self.Vtype)+'_'+self.boost+'Boost'
        
        if (self.Vtype==0 or self.Vtype==2):
            self.lumi=muLumi
            self.trigWeight=trigWeightMu
        elif (self.Vtype==1 or self.Vtype==3):
            self.lumi=elLumi
            self.trigWeight=trigWeightEl

        for sample in reversed(samples):

            if (((sample.systematic=='JECDown' or sample.systematic=='JECUp') and not (doAllSys or doJECSys)) or 
                ((sample.systematic=='JERDown' or sample.systematic=='JERUp') and not (doAllSys or doJERSys)) or 
                ((sample.systematic=='btagDown' or sample.systematic=='btagUp') and not (doAllSys or doBTagSys)) or 
                ((sample.systematic=='mistagDown' or sample.systematic=='mistagUp') and not (doAllSys or doMisTagSys))): samples.remove(sample)

    #---------------------------------------------------------------------------------------------------------------------------------------------------------            

    def newHist(self, name, Sumw2=True):

        if self.is1D:
            result=TH1F(self.name+'__'+name,";"+self.xTitle,self.nBinsX,self.binsX)
            if Sumw2: result.Sumw2()
            return result
        else:
            result=TH2F(self.name+'__'+name,";"+self.xTitle+";"+self.yTitle,self.nBinsX,self.binsX,self.nBinsY,self.binsY)
            if Sumw2: result.Sumw2()
            return result

    #---------------------------------------------------------------------------------------------------------------------------------------------------------

    def allHists(self):
        return [sample.h for sample in allSamples] + self.extraHists.values()

    #---------------------------------------------------------------------------------------------------------------------------------------------------------

    def skip(self, sample):
        if (self.Vtype==0 or self.Vtype==2) and sample.channel=='el': return True
        if (self.Vtype==1 or self.Vtype==3) and sample.channel=='mu': return True
        if (not doZJetsShapeSys and not doAllSys) and isEqual(sample.type,'ZJets') and 'shape' in sample.name: return True
        if (not doTTbarShapeSys and not doAllSys) and isEqual(sample.type,'ttbar') and 'shape' in sample.name: return True
        else: return False
                    
    #---------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def Prepare(self):
        yields={}
        
        #get histograms with proper normalization
        for sample in samples:
            print sample.name
            
            if self.skip(sample): continue

            sample.setInputList(inputDir)
            sample.makeTChain(treeName)
                        
            #hName=self.name+'__'+sample.name
            sample.h=self.newHist(sample.name)

            theCuts=cuts[self.Vtype][self.cuts]+' && Vtype=='+str(self.Vtype)
            #if self.boost=='low': theCuts+=' && 100<V.pt && V.pt<130'
            if self.boost=='med' and self.cuts=='bdt': theCuts+=' && V.pt > 50. && V.pt < 100. && h_HmCorr > 40. && h_HmCorr < 250.'
            if self.boost=='high' and self.cuts=='bdt': theCuts+=' && V.pt > 100. && h_HmCorr < 250.'
            
            weight='1'
            if sample.isMC:
                #theCuts = theCuts.replace('((EVENT.run<193834 && (triggerFlags[22]>0 || triggerFlags[23]>0)) || (EVENT.run>=193834 && (triggerFlags[14]>0 ||triggerFlags[21]>0)))','1')
                #theCuts = theCuts.replace('(triggerFlags[44]>0)','1')
                theCuts = theCuts.replace('(!(207883<=EVENT.run && EVENT.run<=208307))','1')
                weight+=' * '+PUWeight 
                weight+=' * '+self.trigWeight
                weight+=' * weightMueEff'
                if sample.name=='ZJets_shapeSys' or sample.name=='ttbar_shapeSys': weight+=' * 1'
                else: 
                	weight+=' * lheWeight'
                	weight+=' * weightDYZpT'
                weight+=' * weightSignalQCD'
                weight+=' * weightEWKSignalATLAS'
                weight+=' / effectiveLumi'

                #if isEqual(sample.type,'WJets'): weight+=' * weightWpt_WJets'
                #if isEqual(sample.type,'ttbar'): weight+=' * weightWpt_TTbar'
                #weight+=' * weightEleTrigger'  #Why are we applying this weight to muon channel? JS

                if doBDT and not sample.isSignal and not (sample.name=='ZJets_shapeSys' or sample.name=='ttbar_shapeSys'):
                    weight+=' * 2'
                    theCuts+=' && EventForTraining==0'#' && EVENT.event%2==0'

                if do1stHalfBDT:
                    weight+=' * 4'
                    theCuts+=' && EVENT.event%4==1'
                    
                if do2ndHalfBDT:
                    weight+=' * 4'
                    theCuts+=' && EVENT.event%2!=0 && EVENT.event%4!=1'

                if sample.isSignal:
                    weight+=' * weightSignalNLO(genZ.pt)' # SS, 17 Oct 2014                                                                                                                                                                       
            if isEqual(sample.type,'ZJets'):
                Z_light='Z_light'
                Z_b='Z_b'
                Z_bb='Z_bb'
                if sample.systematic:
                    Z_light+='_'+sample.systematic
                    Z_b+='_'+sample.systematic
                    Z_bb+='_'+sample.systematic

                self.extraHists[Z_light]=self.newHist(Z_light)
                self.extraHists[Z_b]=self.newHist(Z_b)
                self.extraHists[Z_bb]=self.newHist(Z_bb)

                if not applyNormSFs:
                    scaleFactors[self.boost]['Z_light'] = 1
                    scaleFactors[self.boost]['Z_b'] = 1
                    scaleFactors[self.boost]['Z_bb'] = 1
                
                #sample.chain.Draw(self.distribution+'>>'+self.extraHists[Z_light].GetName(),weight+' * '+str(scaleFactors[self.boost]['Z_light'])+' * ('+theCuts+' && ((abs(hJet_flavour[0])==5)+(abs(hJet_flavour[1])==5))==0)','GOFF')
                #sample.chain.Draw(self.distribution+'>>'+self.extraHists[Z_b].GetName(),weight+' * '+str(scaleFactors[self.boost]['Z_b'])    +' * ('+theCuts+' && ((abs(hJet_flavour[0])==5)+(abs(hJet_flavour[1])==5))==1)','GOFF')
                #sample.chain.Draw(self.distribution+'>>'+self.extraHists[Z_bb].GetName(),weight+' * '+str(scaleFactors[self.boost]['Z_bb'])   +' * ('+theCuts+' && ((abs(hJet_flavour[0])==5)+(abs(hJet_flavour[1])==5))==2)','GOFF')
                sample.chain.Draw(self.distribution+'>>'+self.extraHists[Z_light].GetName(),weight+' * '+str(scaleFactors[self.boost]['Z_light'])+' * ('+theCuts+' && ((eventFlav != 5 && eventFlav != 4) || eventFlav == 4))','GOFF')
                sample.chain.Draw(self.distribution+'>>'+self.extraHists[Z_b].GetName(),weight+' * '+str(scaleFactors[self.boost]['Z_b'])    +' * ('+theCuts+' && eventFlav == 5 && !(abs(hJet_flavour[0]) == 5 && abs(hJet_flavour[1]) == 5))','GOFF')
                sample.chain.Draw(self.distribution+'>>'+self.extraHists[Z_bb].GetName(),weight+' * '+str(scaleFactors[self.boost]['Z_bb'])   +' * ('+theCuts+' && eventFlav == 5 && abs(hJet_flavour[0]) == 5 && abs(hJet_flavour[1]) == 5)','GOFF')
                
                if showOverflow:   #if we fix the overflow when drawing all histograms, then all the "extraHists" will automatically have overflow taken care of
                    for hName in [Z_light,Z_b,Z_bb]:
                        self.overflow(self.extraHists[hName])
                
                if normalizeByBinWidth:
                    for hName in [Z_light,Z_b,Z_bb]:
                        self.extraHists[hName]=normByBinWidth(self.extraHists[hName])

                sample.h.Add(self.extraHists[Z_light])
                sample.h.Add(self.extraHists[Z_b])
                sample.h.Add(self.extraHists[Z_bb])

                #Inclusive W sample will be scaled below
                self.extraHists[Z_light].Scale(self.lumi)
                self.extraHists[Z_b].Scale(self.lumi)
                self.extraHists[Z_bb].Scale(self.lumi)

                if DEBUG:
                    print '=============================='
                    print weight+' * '+scaleFactor
                    print '=============================='
                    print weight+' * '+str(scaleFactors[self.boost]['Z_light'])+' * ('+theCuts+' && ((eventFlav != 5 && eventFlav != 4) || eventFlav == 4))'
                    print weight+' * '+str(scaleFactors[self.boost]['Z_b'])    +' * ('+theCuts+' && eventFlav == 5 && !(abs(hJet_flavour[0]) == 5 && abs(hJet_flavour[1]) == 5))'
                    print weight+' * '+str(scaleFactors[self.boost]['Z_bb'])   +' * ('+theCuts+' && eventFlav == 5 && abs(hJet_flavour[0]) == 5 && abs(hJet_flavour[1]) == 5)'
                    print '=============================='

                stdout_old = sys.stdout
                logFile = open(outputDir + '/log.txt','a')
                sys.stdout = logFile                    
                if DEBUG:
                    print "Draw:",sample.name, self.Vtype, self.cuts, self.boost, sample.h.Integral()#, sample.h.Integral(0,sample.h.GetNbinsX()+1, 0,sample.h.GetNbinsY()+1)
                sys.stdout = stdout_old
                logFile.close()
            else:
                if isEqual(sample.type,'ttbar') and applyNormSFs: scaleFactor=str(scaleFactors[self.boost]['ttbar'])
                else: scaleFactor='1'

                if DEBUG:
                    print '=============================='
                    print weight+' * '+scaleFactor
                    print '=============================='
                    print theCuts
                    print '=============================='

                if not blind or not contains(sample.type,'data'):
                    val = sample.chain.Draw(self.distribution+">>"+sample.h.GetName(),weight+' * '+scaleFactor+' * ('+theCuts+')','GOFF')
                
                stdout_old = sys.stdout
                logFile = open(outputDir + '/log.txt','a')
                sys.stdout = logFile
                if DEBUG:
                    print "Draw:",sample.name, self.Vtype, self.cuts, self.boost, sample.h.Integral()#, sample.h.Integral(0,sample.h.GetNbinsX()+1, 0,sample.h.GetNbinsY()+1)
                sys.stdout = stdout_old
                logFile.close()

            #output.cd()
            if sample.isMC: sample.h.Scale(self.lumi)
            if showOverflow: self.overflow(sample.h)
            if normalizeByBinWidth: sample.h=normByBinWidth(sample.h)
            if fillEmptyBins and sample.isBackground: fillBins(sample.h)

            #Make histograms for background combinations and fill yield table
            name=sample.type
            if sample.systematic: name+='_'+sample.systematic
            if not name in self.extraHists.keys(): self.extraHists[name]=self.newHist(name)
            self.extraHists[name].Add(sample.h)

        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #Systematics
        """
        #Statistical
        if doStatSys or doAllSys:
            for sample in samples:
                try: histName=sample.h.GetName()
                except: continue
                if contains(histName,'data') or contains(histName,'total back') or contains(histName,'up') or contains(histName,'down') or contains(histName,'shape'): continue   #Only calculate for nominal backgrounds - this is dangerous, 'up' could accidentally match a lot of things
                if sample.isSignal: ID=sample.name.split('_')[-1]
                else: ID=sample.name
                self.makeStat(sample.h,ID)

            for histName in self.extraHists.keys():
                
                if contains(histName,'data') or contains(histName,'total back') or contains(histName,'up') or contains(histName,'down') or contains(histName,'shape'): continue   #Only calculate for nominal backgrounds - this is dangerous, 'up' could accidentally match a lot of things
                ID=histName
                self.makeStat(self.extraHists[histName],ID)
        """
        #Z+Jets and ttbar shape
        if doZJetsShapeSys or doTTbarShapeSys or doAllSys:
            shapeSamples=[]
            if doZJetsShapeSys or doAllSys and self.extraHists.has_key('ZJets'):
                shapeSamples+=['Z_light','Z_b','Z_bb']
            if doTTbarShapeSys or doAllSys and self.extraHists.has_key('ttbar'):
                shapeSamples+=['ttbar']
                    
            for sampleName in shapeSamples:
                nominal=self.extraHists[sampleName]
                print sampleName
                if sampleName=='ttbar': up=self.extraHists[sampleName+'_ttbarShape_ZHUp']
                else: up=self.extraHists[sampleName+'_ZJetsShapeUp']
                down=up.Clone(up.GetName().replace('Up','Down'))

                #Force Z+Jets and ttbar systematic integrals to nominal values
                up.Scale(self.integral(nominal)/self.integral(up))

                #symmeterize
                if self.is1D:
                    for xBin in range(0,self.nBinsX+2):
                        down.SetBinContent(xBin,max(0,nominal.GetBinContent(xBin)-(up.GetBinContent(xBin)-nominal.GetBinContent(xBin))))
                else:
                    for xBin in range(0,self.nBinsX+2):
                        for yBin in range(0,self.nBinsY+2):
                            down.SetBinContent(xBin,yBin,max(0,nominal.GetBinContent(xBin,yBin)-(up.GetBinContent(xBin,yBin)-nominal.GetBinContent(xBin,yBin))))
                if sampleName=='ttbar': self.extraHists[sampleName+'_ttbarShape_ZHDown']=down
                else: self.extraHists[sampleName+'_ZJetsShapeDown']=down
        """                    
        #Force Z+Jets and ttbar systematic integrals to nominal values
        for histName in self.extraHists.keys():
            try:
				if self.extraHists.has_key('ZJets'):  #Sometimes I skip WJets for speed - JS
					if contains(histName,'Z_light_'):
						self.extraHists[histName].Scale(self.integral(self.extraHists['Z_light'])/self.integral(self.extraHists[histName]))
					elif contains(histName,'Z_b_'):
						self.extraHists[histName].Scale(self.integral(self.extraHists['Z_b'])/self.integral(self.extraHists[histName]))
					elif contains(histName,'Z_bb_'):
						self.extraHists[histName].Scale(self.integral(self.extraHists['Z_bb'])/self.integral(self.extraHists[histName]))
				if self.extraHists.has_key('ttbar'):
					if contains(histName,'ttbar_'):
						self.extraHists[histName].Scale(self.integral(self.extraHists['ttbar'])/self.integral(self.extraHists[histName]))
            except:
				print histName, self.extraHists[histName], self.integral(self.extraHists[histName])
        """                                                                                           
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #Signals and total background - yes it shouldn't really be here but I want to return the total background yield - JS

        self.signals=[]
        for sample in samples:
            if self.skip(sample): continue
            
            sample.h.SetLineWidth(4)
            if sample.isSignal and not sample.systematic:
            	print sample.name
                sample.h.SetLineColor(1)
                sample.h.SetLineStyle(2+len(self.signals))
                self.signals.append(sample)
                
        self.backgroundStack=THStack()
        for background in plotBackgrounds:
            try:
                self.extraHists[background].SetFillColor(backgroundFillColors[background])
                self.extraHists[background].SetLineColor(backgroundLineColors[background])
                self.backgroundStack.Add(self.extraHists[background])
            except: print "No",background,"background found!"
        self.extraHists['Total Background']=self.backgroundStack.GetStack().Last().Clone(self.name+'__totalBackground'); self.extraHists['Total Background'].Sumw2()
        
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        #Yields

        for sample in samples:
            if self.skip(sample): continue
            yields[sample.name]=self.integral(sample.h)
        for histName in self.extraHists.keys():
            yields[histName]=self.integral(self.extraHists[histName])
        return yields

    #---------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def Draw(self):
        self.canvas=TCanvas(self.name,"",1000,800)

        gStyle.SetErrorX(0.5)

        yDiv=0.35
        if blind == True:
            yDiv=0.1
            
        uMargin = 0
        if blind == True:
            uMargin = 0.15
             
        rMargin=.13
        
        self.uPad=TPad("uPad","",0,yDiv,1,1) #for actual plots
        self.uPad.SetTopMargin(0.07)
        self.uPad.SetBottomMargin(uMargin)
        self.uPad.SetRightMargin(rMargin)
        self.uPad.SetLeftMargin(.18)
        self.uPad.Draw()

        if blind == False:                                    
            self.lPad=TPad("lPad","",0,0,1,yDiv) #for sigma runner
            self.lPad.SetTopMargin(0)
            self.lPad.SetBottomMargin(.4)
            self.lPad.SetRightMargin(rMargin)
            self.lPad.SetLeftMargin(.18)
            self.lPad.SetGridy()
            self.lPad.Draw()

        #self.extraHists['Data'].SetMaximum(2*self.extraHists['Data'].GetMaximum())
        self.extraHists['Data'].SetMaximum(2*max(self.extraHists['Data'].GetMaximum(),self.extraHists['Total Background'].GetMaximum()))
        self.extraHists['Data'].SetMinimum(0.025)

        #binWidth=round(self.extraHists['Data'].GetBinWidth(1),5)
        #if binWidth-round(binWidth)<.001*binWidth: binWidth=int(round(binWidth))
        
        yTitle="Events"
        if normalizeByBinWidth:
            yTitle+=' / 1'
        if  '[' in self.xTitle and ']' in self.xTitle: #get units from x axis title
            begin=self.xTitle.find('[')+1
            end=self.xTitle.find(']')
            yTitle+=self.xTitle[begin:end]
        self.extraHists['Data'].GetYaxis().SetTitle(yTitle)
        
        self.formatUpperHist(self.extraHists['Data'])

        self.uPad.cd()
        self.extraHists['Data'].Draw("E1 X0") #draw data first because its easier to format a TH1 than a THStack
        self.backgroundStack.Draw("SAME HIST")
        for signal in self.signals:
            if signal in samplesForPlotting:
                signal.h.Scale(signalMagFrac)
                signal.h.Draw("SAME HIST")
                #signal.h.Scale(1./signalMagFrac)

        self.extraHists['Data'].Draw("SAME E1 X0") #redraw data so its not hidden
        self.uPad.RedrawAxis()

        if self.is1D:
        
            #calculate stat+sys uncertainty band
            self.uncBand=self.extraHists['Total Background'].Clone("unc")
            #for binNo in range(0,self.nBinsX+2):
            #    lumiUnc=0
            #    statUnc=0
            #    sigmaUnc=0
            #    for sample in samples:
            #        if sample.systematic or (not sample.isBackground) or self.skip(sample): continue
            #        lumiUnc+=(sample.h.GetBinContent(binNo)*lumiFracUnc)**2
            #        sigmaUnc+=(sample.h.GetBinContent(binNo)*sigmaFracUnc[sample.type])**2
            #        statUnc+=sample.h.GetBinError(binNo)**2
            #    totalUnc=sqrt(lumiUnc+sigmaUnc+statUnc)
            #    self.uncBand.SetBinError(binNo,totalUnc)
            #    self.extraHists['Total Background'].SetBinError(binNo,totalUnc)
            self.uncBand.SetFillStyle(3344)
            self.uncBand.SetFillColor(1)
            self.uncBand.SetLineColor(1)
            self.uncBand.SetMarkerSize(0)
            gStyle.SetHatchesLineWidth(1)
            self.uncBand.Draw("SAME E2")

            legend=TLegend(0.43,0.64,0.84,0.90)
            SetOwnership( legend, 0 )   # 0 = release (not keep), 1 = keep
            legend.SetNColumns(2)
            legend.SetShadowColor(0)
            legend.SetFillColor(0)
            legend.SetFillStyle(0)
            legend.SetLineColor(0)
            legend.SetTextFont(42)
            if blind == False:
                legend.AddEntry(self.extraHists['Data'],"Data")
            for bName,bLabel in zip(reversed(['QCD','ZJets','WJets','singleTop','ttbar','VV','VZ','ggh']),reversed(['QCD','Z+jets','W+jets','single top','ttbar','VV','VZ','ggZh'])):
                try: legend.AddEntry(self.extraHists[bName],bLabel,"f")
                except: pass

            for signal in self.signals:
                if signal in samplesForPlotting:
                    legend.AddEntry(signal.h, signal.altName + " x" + str(signalMagFrac), "l")

            legend.AddEntry(self.uncBand , "MC uncert. (stat.)" , "f")
            legend.Draw("SAME")

            prelimTex=TLatex()
            prelimTex.SetNDC()
            prelimTex.SetTextSize(0.04)
            prelimTex.SetTextAlign(31) # align right
            prelimTex.SetTextFont(42)
            lumi=self.lumi/1000.
            lumi=round(lumi,2)
            prelimTex.DrawLatex(0.88, 0.95, "CMS Preliminary, "+str(lumi)+" fb^{-1} at #sqrt{s} = 8 TeV");

            channelTex = TLatex()
            channelTex.SetNDC()
            channelTex.SetTextSize(0.08)
            channelTex.SetTextAlign(31)
            channelTex.SetTextFont(42)
            if self.Vtype==0: text='Z #rightarrow #mu#mu'
            elif self.Vtype==1: text='Z #rightarrow ee'
            elif self.Vtype==2: text='W #rightarrow #mu#nu'
            else: text='W #rightarrow e#nu'
            channelTex.DrawLatex(0.38, 0.81, text);

            if blind == False:
                self.lPad.cd()
                self.pull=self.extraHists['Data'].Clone("pull")
                self.pull.Divide(self.extraHists['Data'], self.extraHists['Total Background'])
                #I think this would be correct - JS
                #for binNo in range(0,self.nBinsX+2):
                #    if self.extraHists['Total Background'].GetBinContent(binNo)!=0:
                #        self.pullUncBand.SetBinErorr(binNo,self.extraHists['Total Background'].GetBinError(binNo)/self.extraHists['Total Background'].GetBinContent(binNo)))
                self.pull.SetMaximum(3)
                self.pull.SetMinimum(0)
                self.pull.SetFillColor(1)
                self.pull.SetLineColor(1)
                self.formatLowerHist(self.pull)
                self.pull.GetYaxis().SetTitle('Data/Bkgd')
                #self.pull.Draw("HIST")
                self.pull.Draw("E1")
                
                self.pullUncBand=self.pull.Clone("pullunc")
                self.pullUncBand.Divide(self.extraHists['Total Background'], self.extraHists['Total Background'])
                #I think this would be correct - JS
                #for binNo in range(0,self.nBinsX+2):
                #    if self.extraHists['Total Background'].GetBinContent(binNo)!=0:
                #        self.pullUncBand.SetBinErorr(binNo,self.extraHists['Total Background'].GetBinError(binNo)/self.extraHists['Total Background'].GetBinContent(binNo)))
                self.pullUncBand.SetFillStyle(3344)
                self.pullUncBand.SetFillColor(1)
                self.pullUncBand.SetLineColor(1)
                self.pullUncBand.SetMarkerSize(0)
                gStyle.SetHatchesLineWidth(1)
                self.pullUncBand.Draw("SAME E2")
                
                pullLegend=TLegend(0.19,0.92,0.37,0.99)
                SetOwnership( pullLegend, 0 )   # 0 = release (not keep), 1 = keep
                pullLegend.SetShadowColor(0)
                pullLegend.SetFillColor(0)
                pullLegend.SetLineColor(0)
                pullLegend.SetTextFont(42)
                pullLegend.AddEntry(self.pullUncBand , "MC uncert. (stat.)" , "f")
                pullLegend.Draw("SAME")

            self.canvas.Write()
            self.canvas.SaveAs(outputDir+'/'+self.name+'.pdf')
            self.canvas.SaveAs(outputDir+'/'+self.name+'.eps')
            self.canvas.SaveAs(outputDir+'/'+self.name+'.png')
            
        for signal in self.signals:
        	if signal in samplesForPlotting:
        		signal.h.Scale(1./signalMagFrac)

        if unroll2D:
            for sample in allSamples:
                if self.skip(sample): continue
                #print sample.name,sample.h.Integral()
                sample.h=unroll(sample.h)
            for key,value in self.extraHists.items():
                #print key, self.extraHists[key].Integral()
                self.extraHists[key]=unroll(value)

        #Write histograms
        for sample in samples:
            if self.skip(sample): continue
            sample.h.Write()
                        
        for histName in self.extraHists.keys():
            self.extraHists[histName].Write()

    #---------------------------------------------------------------------------------------------------------------------------------------------------------

    def makeStat(self, h, ID):
        statUp=h.Clone(h.GetName()+'_stat_'+ID+'Up')
        statDown=h.Clone(h.GetName()+'_stat_'+ID+'Down')
        
        if self.is1D:
            for xBin in range(0,self.nBinsX+2):
                nominal=h.GetBinContent(xBin)
                unc=h.GetBinError(xBin)
                statUp.SetBinContent(xBin,nominal+unc)
                statDown.SetBinContent(xBin,max(0,nominal-unc))
        else:
            for xBin in range(0,self.nBinsX+2):
                for yBin in range(0,self.nBinsY+2):
                    nominal=h.GetBinContent(xBin,yBin)
                    unc=h.GetBinError(xBin,yBin)
                    statUp.SetBinContent(xBin,yBin,nominal+unc)
                    statDown.SetBinContent(xBin,yBin,max(0,nominal-unc))
        self.extraHists[ID+'_statUp']=statUp
        self.extraHists[ID+'_statDown']=statDown

    #---------------------------------------------------------------------------------------------------------------------------------------------------------
                        
    def overflow(self, h):

        if self.is1D:
            content=h.GetBinContent(self.nBinsX)+h.GetBinContent(self.nBinsX+1)
            error=sqrt(h.GetBinError(self.nBinsX)**2+h.GetBinError(self.nBinsX+1)**2)
            h.SetBinContent(self.nBinsX,content)
            h.SetBinError(self.nBinsX,error)
            h.SetBinContent(self.nBinsX+1,0)
            h.SetBinError(self.nBinsX+1,0)
        else:
            for yBin in range(0,self.nBinsY+2):
                content=h.GetBinContent(self.nBinsX,yBin)+h.GetBinContent(self.nBinsX+1,yBin)
                error=sqrt(h.GetBinError(self.nBinsX,yBin)**2+h.GetBinError(self.nBinsX+1,yBin)**2)
                h.SetBinContent(self.nBinsX,yBin,content)
                h.SetBinError(self.nBinsX,yBin,error)
                h.SetBinContent(self.nBinsX+1,yBin,0)
                h.SetBinError(self.nBinsX+1,yBin,0)
            for xBin in range(0,self.nBinsX+2):
                content=h.GetBinContent(xBin,self.nBinsY)+h.GetBinContent(xBin,self.nBinsY+1)
                error=sqrt(h.GetBinError(xBin,self.nBinsY)**2+h.GetBinError(xBin,self.nBinsY+1)**2)
                h.SetBinContent(xBin,self.nBinsY,content)
                h.SetBinError(xBin,self.nBinsY,error)
                h.SetBinContent(xBin,self.nBinsY+1,0)
                h.SetBinError(xBin,self.nBinsY+1,0)

    #---------------------------------------------------------------------------------------------------------------------------------------------------------
        
    def integral(self, h):
        if type(h)==type(TH1F()): return h.Integral(0,h.GetNbinsX()+1)
        else: return h.Integral(0,h.GetNbinsX()+1,0,h.GetNbinsY()+1)
        
    #---------------------------------------------------------------------------------------------------------------------------------------------------------
            
    def formatUpperHist(self,histogram):
        histogram.GetXaxis().SetLabelSize(0)

        if blind == True:
            histogram.GetXaxis().SetLabelSize(0.08)
            histogram.GetXaxis().SetTitleSize(0.08)
            histogram.GetXaxis().SetTitle(self.xTitle)
            histogram.GetYaxis().SetLabelSize(0.08)
            histogram.GetYaxis().SetTitleSize(0.08)
            histogram.GetYaxis().SetTitleOffset(1.2)
        else:
            histogram.GetYaxis().SetLabelSize(0.08)
            histogram.GetYaxis().SetTitleSize(0.12)
            histogram.GetYaxis().SetTitleOffset(.75)

        histogram.GetYaxis().CenterTitle()
        if self.yLog:
            self.uPad.SetLogy()
            histogram.SetMaximum(500*histogram.GetMaximum())
            
    #---------------------------------------------------------------------------------------------------------------------------------------------------------

    def formatLowerHist(self,histogram):
        histogram.GetXaxis().SetLabelSize(.15)
        histogram.GetXaxis().SetTitleSize(0.18)
        histogram.GetXaxis().SetTitleOffset(0.95)
        histogram.GetXaxis().SetTitle(self.xTitle)

        histogram.GetYaxis().SetLabelSize(0.125)
        histogram.GetYaxis().SetTitleSize(0.1)
        histogram.GetYaxis().SetTitleOffset(.55)
        histogram.GetYaxis().SetNdivisions(5);
