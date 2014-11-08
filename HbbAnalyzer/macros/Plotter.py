import math,ROOT, sys
from ROOT import gStyle

ROOT.gROOT.SetStyle('Plain')
ROOT.gROOT.SetBatch(ROOT.kTRUE)
gStyle.SetOptStat(1110)
gStyle.SetOptTitle(0)
gStyle.SetPadTickY(1)
gStyle.SetPadTickX(1)

doAK4 = False
dofat = False
dofatmult = True
doZ = False
dogen = False
doZeff = False
dofateff = False
dofateffZ = False
doungr = False

fat = ['AK8', 'AK10', 'AK12', 'AK15']
algo = ['AK4']
groom = ['_filtered', '_pruned', '_trimmed', '_mdt', '_bdrs']
var = ['HiggsM_', 'HiggsM_nocuts_', 'HiggsPt_', 'ZBosonPt_', 'HiggsPt_nocuts_', 'HiggsM_bdtcuts_', 'HiggsPt_bdtcuts_', 'HiggsEta_', 'deltaRbb_', 'deltaRbb_nocuts_', 'deltaRbb_bdtcuts_', 'j1Pt_', 'j1Pt_nocuts_', 'j2Pt_', 'j2Pt_nocuts_', 'j1Eta_', 'j1Eta_nocuts_', 'j2Eta_', 'j2Eta_nocuts_', 'j1Pt_bdtcuts_', 'j2Pt_bdtcuts_', 'j1Eta_bdtcuts_', 'j2Eta_bdtcuts_', 'HiggsM_200cuts_', 'HiggsPt_200cuts_', 'ZBosonPt_200cuts_', 'j1Pt_200cuts_', 'j2Pt_200cuts_', 'deltaRbb_200cuts_', 'HiggsM_300cuts_', 'HiggsPt_300cuts_', 'ZBosonPt_300cuts_', 'j1Pt_300cuts_', 'j2Pt_300cuts_', 'deltaRbb_300cuts_', 'HiggsM_150masscuts_', 'HiggsPt_150masscuts_', 'ZBosonPt_150masscuts_', 'j1Pt_150masscuts_', 'j2Pt_150masscuts_', 'deltaRbb_150masscuts_', 'HiggsM_200masscuts_', 'HiggsPt_200masscuts_', 'ZBosonPt_200masscuts_', 'j1Pt_200masscuts_', 'j2Pt_200masscuts_', 'deltaRbb_200masscuts_', 'HiggsM_300masscuts_', 'HiggsPt_300masscuts_', 'ZBosonPt_300masscuts_', 'j1Pt_300masscuts_', 'j2Pt_300masscuts_', 'deltaRbb_300masscuts_']
Zvar = ['ZM', 'ZPt', 'ZPt_150', 'ZPt_onlymcut', 'ZEta', 'muon1Pt', 'muon2Pt', 'muon1Eta', 'muon2Eta']
genvar = ['genHPt', 'genHPt_allcuts', 'genHPt_hcuts', 'genHEta', 'genbPt', 'genbEta', 'gendeltaRbb',  'gendeltaRbb_cuts', 'gendeltaRbb_cuts150', 'gendeltaRbb_cuts300', 'gendeltaPhiZH', 'genZPt', 'genZPt_allcuts', 'genZPt_goodZcuts', 'genZEta', 'genmuonPt', 'genmuonEta']
effvar = ['genHPt_recoH_150_', 'genHPt_recoH_200_', 'genHPt_recoH_300_', 'genHPt_recoH_tightm150_', 'genHPt_recoH_tightm200_', 'genHPt_recoH_tightm300_']
Zeffvar = ['ZBosonPt_', 'ZBosonPt_200cuts_', 'ZBosonPt_300cuts_', 'ZBosonPt_150masscuts_', 'ZBosonPt_200masscuts_', 'ZBosonPt_300masscuts_']
ungr = ['HiggsM_nocuts_ungr_', 'HiggsPt_nocuts_ungr_', 'HiggsM_150cut_ungr_', 'HiggsPt_150cut_ungr_', 'HiggsM_150masscut_ungr_', 'HiggsPt_150masscut_ungr_', 'HiggsM_200cut_ungr_', 'HiggsPt_200cut_ungr_', 'HiggsM_200masscut_ungr_', 'HiggsPt_200masscut_ungr_', 'HiggsM_150cut_ungr_', 'HiggsPt_150cut_ungr_', 'HiggsM_150masscut_ungr_', 'HiggsPt_150masscut_ungr_', 'HiggsM_300cut_ungr_', 'HiggsPt_300cut_ungr_', 'HiggsM_300masscut_ungr_', 'HiggsPt_300masscut_ungr_']
tau = ['tau1_nocuts_', 'tau2_nocuts_', 'tau3_nocuts_', 'tau1_150cut_', 'tau2_150cut_', 'tau3_150cut_', 'tau1_150masscut_', 'tau2_150masscut_', 'tau3_150masscut_', 'tau1_200cut_', 'tau2_200cut_', 'tau3_200cut_', 'tau1_200masscut_', 'tau2_200masscut_', 'tau3_200masscut_', 'tau1_300cut_', 'tau2_300cut_', 'tau3_300cut_', 'tau1_300masscut_', 'tau2_300masscut_', 'tau3_300masscut_']

rbn=1
xmin=0
xmax=100
title = 'title'


zh = ROOT.TFile('/eos/uscms/store/user/ingabu/Higgs/CSA14/Anatuples/Hbb__ZH_HToBB_ZToLL_M-125_13TeV_PU40bx50_Moreplots.root')
#zh = ROOT.TFile('/eos/uscms/store/user/ingabu/Higgs/CSA14/Anatuples/Hbb__DYJetsToLL_M-50_13TeV_PU40bx50_Moreplots.root')
#zh = ROOT.TFile('/eos/uscms/store/user/ingabu/Higgs/CSA14/Anatuples/Hbb__TTJets_13TeV_PU40bx50_Moreplots.root')

#nbins = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160]
nbins = [25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800] 
def RebinHist(h,theBins,divideByBinWidth=True):
##
## Rebin histogram with variable width bins 
## pass histogram and python list containing bin lower edges and upper edge of last bin
##
##
    from array import array

    newbins=array("d",theBins)

    n=len(newbins)
    hname=h.GetName()
    hname=hname + " -- Rebinned"
    hnew=h.Rebin(n-1,hname,newbins)

    if divideByBinWidth:
        ## divide by the bin width
        for i in range(hnew.GetNbinsX()):
            bw=hnew.GetXaxis().GetBinWidth(i+1)
            # print bw
            cont=hnew.GetBinContent(i+1)
            err=hnew.GetBinError(i+1)

            cont=cont/bw
            err=err/bw
            hnew.SetBinContent(i+1,cont)
            hnew.SetBinError(i+1,err)

    #print hnew
    return hnew


#******** Z plots ****************
if doZ:
    for v in Zvar:
        hist_zh_var = zh.Get('HbbAnalyzer/ZBoson/' + v)
        
        if v == 'ZM':
            rbn=2; xmin=0.; xmax=260.; title='Z Mass (GeV)'
        if v == 'ZPt' or v == 'ZPt_150' or v == 'ZPt_300' or v == 'ZPt_onlymcut':
            rbn=2; xmin=0.; xmax=500.; title='Z Pt (GeV)'
        if v == 'ZEta':
            rbn=1; xmin=-5.; xmax=5.; title='Z Eta'
        if v == 'muon1Pt':
            rbn=2; xmin=0.; xmax=500.; title='muon_1 Pt (GeV)'
        if v == 'muon2Pt':
            rbn=2; xmin=0.; xmax=500.; title='muon_2 Pt (GeV)'
        if v == 'muon1Eta':
            rbn=1; xmin=-5.; xmax=5.; title='muon_1 Eta'
        if v == 'muon2Eta':
            rbn=1; xmin=-5.; xmax=5.; title='muon_2 Eta'

        hist_zh_var.Rebin(rbn)
        hist_zh_var.SetLineColor(ROOT.kBlack)
        hist_zh_var.SetMarkerStyle(20)
        hist_zh_var.SetMarkerColor(ROOT.kBlack)
        hist_zh_var.SetStats(1)

        canvas = ROOT.TCanvas()
        #canvas.SetLogy()
        hist_zh_var.GetXaxis().SetRangeUser(xmin, xmax)
        hist_zh_var.GetXaxis().SetTitleSize(0.05)
        hist_zh_var.GetXaxis().SetTitleOffset(0.8)
        hist_zh_var.GetXaxis().SetTitle(title)
        hist_zh_var.Draw()


        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.06)
        #latex.DrawLatex(0.10, 0.94, '#color[' + str(4) + ']{' + 'Z Boson' + '}')
        canvas.Update()

        canvas.SaveAs('/uscms_data/d3/ingabu/CSA14/CMSSW_7_1_0_pre9/src/VHbb/HbbAnalyzer/macros/Gifs/MorePlots/'+ v + '.gif')

#******** Gen plots *************
if dogen:
    for v in genvar:
        hist_zh_var = zh.Get('HbbAnalyzer/genParticles/' + v)

        if v == 'genHPt' or v == 'genHPt_allcuts' or v == 'genHPt_hcuts':
            rbn=2; xmin=0.; xmax=500.; title='Gen Higgs Pt (GeV)'
        if v == 'genZPt' or v == 'genZPt_allcuts' or v == 'genZPt_goodZcuts':
            rbn=2; xmin=0.; xmax=500.; title='Gen Z Pt (GeV)'
        if v == 'genHEta':
            rbn=1; xmin=-5.; xmax=5.; title='Gen Higgs Eta'
        if v == 'genZEta':
            rbn=1; xmin=-5.; xmax=5.; title='Gen Z Eta'
        if v == 'genbPt':
            rbn=2; xmin=0.; xmax=500.; title='Gen b Pt (GeV)'
        if v == 'genmuonPt':
            rbn=2; xmin=0.; xmax=500.; title='Gen muon Pt (GeV)'
        if v == 'genbEta':
            rbn=1; xmin=-5.; xmax=5.; title='Gen b Eta'
        if v == 'genmuonEta':
            rbn=1; xmin=-5.; xmax=5.; title='Gen muon Eta'
        if v == 'gendeltaRbb' or v == 'gendeltaRbb_cuts':
            rbn=1; xmin=0.; xmax=5.; title='Gen DeltaR(bb)'
        if v == 'gendeltaRbb_cuts150':
            rbn=1; xmin=0.; xmax=5.; title='Gen DeltaR(bb), Z Pt > 150 GeV'
        if v == 'gendeltaRbb_cuts300':
            rbn=1; xmin=0.; xmax=5.; title='Gen DeltaR(bb), Z Pt > 300 GeV'
        if v == 'gendeltaPhiZH':
            rbn=1; xmin=0.; xmax=5.; title='Gen DeltaPhi(ZH)'

        hist_zh_var.Rebin(rbn)
        hist_zh_var.SetLineColor(ROOT.kBlack)
        hist_zh_var.SetMarkerStyle(20)
        hist_zh_var.SetMarkerColor(ROOT.kBlack)
        hist_zh_var.SetStats(1)

        canvas = ROOT.TCanvas()
        #canvas.SetLogy()
        hist_zh_var.GetXaxis().SetRangeUser(xmin, xmax)
        hist_zh_var.GetXaxis().SetTitleSize(0.05)
        hist_zh_var.GetXaxis().SetTitleOffset(0.8)
        hist_zh_var.GetXaxis().SetTitle(title)
        hist_zh_var.Draw()


        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.06)
        latex.DrawLatex(0.10, 0.94, '#color[' + str(4) + ']{' + 'GEN' + '}')
        canvas.Update()

        canvas.SaveAs('/uscms_data/d3/ingabu/CSA14/CMSSW_7_1_0_pre9/src/VHbb/HbbAnalyzer/macros/Gifs/MorePlots/'+ v + '.gif')

#******** AK4 Jet plots **************
if doAK4:
    for v in var:
        if v == 'HiggsM_' or v == 'HiggsM_nocuts_' or v == 'HiggsM_bdtcuts_':
            rbn=4; xmin=0.; xmax=260.; title='Higgs Mass (GeV)'
        if v == 'HiggsPt_' or v == 'HiggsPt_nocuts_' or v == 'HiggsPt_bdtcuts_':
            rbn=2; xmin=0.; xmax=500.; title='Higgs Pt (GeV)'
        if v == 'HiggsEta_' or v == 'HiggsEta_nocuts_':
            rbn=2; xmin=-4.; xmax=4.; title='Higgs Eta'
        if v == 'deltaRbb_' or v == 'deltaRbb_nocuts_' or v == 'deltaRbb_bdtcuts_':
            rbn=10; xmin=0.; xmax=2.; title='DeltaR(bb)'
        if v == 'j1Pt_' or v == 'j1Pt_nocuts_' or v == 'j1Pt_bdtcuts_':
            rbn=2; xmin=0.; xmax=500.; title='jet_1 Pt (GeV)'
        if v == 'j2Pt_' or v == 'j2Pt_nocuts_' or v == 'j2Pt_bdtcuts_':
            rbn=2; xmin=0.; xmax=300.; title='jet_2 Pt (GeV)'
        if v == 'j1Eta_' or v == 'j1Eta_nocuts_' or v == 'j1Eta_bdtcuts_':
            rbn=2; xmin=-4.; xmax=4.; title='jet_1 Eta'
        if v == 'j2Eta_' or v == 'j2Eta_nocuts_' or v == 'j2Eta_bdtcuts_':
            rbn=2; xmin=-4.; xmax=4.; title='jet_2 Eta'
        for a in algo:
            hist_zh_var = zh.Get('HbbAnalyzer/AK4/' + v + a)

            hist_zh_var.Rebin(rbn)
            hist_zh_var.SetLineColor(ROOT.kBlack)
            hist_zh_var.SetLineWidth(3)
            hist_zh_var.SetMarkerStyle(20)
            hist_zh_var.SetMarkerColor(ROOT.kBlack)
            hist_zh_var.SetStats(1)

            canvas = ROOT.TCanvas()
            #canvas.SetLogy()
            hist_zh_var.GetXaxis().SetRangeUser(xmin, xmax)
            hist_zh_var.GetXaxis().SetTitleSize(0.05)
            hist_zh_var.GetXaxis().SetTitleOffset(0.8)
            hist_zh_var.GetXaxis().SetTitle(title)
            hist_zh_var.Draw()


            latex = ROOT.TLatex()
            latex.SetNDC()
            latex.SetTextSize(0.06)
            #latex.DrawLatex(0.14, 0.92, 'L = 5 fb^{-1}')
            latex.DrawLatex(0.10, 0.94, '#color[' + str(4) + ']{' + a + '}')
            canvas.Update()

            canvas.SaveAs('/uscms_data/d3/ingabu/CSA14/CMSSW_7_1_0_pre9/src/VHbb/HbbAnalyzer/macros/Gifs/MorePlots/'+ v + a + '.gif')


#******** Fat Jet plots **************
if dofat:
    for v in var:
        if v == 'HiggsM_' or v == 'HiggsM_nocuts_':
            rbn=4; xmin=0.; xmax=260.; title='Higgs Mass (GeV)'
        if v == 'HiggsPt_' or v == 'HiggsPt_nocuts_':
            rbn=2; xmin=0.; xmax=500.; title='Higgs Pt (GeV)'
        if v == 'HiggsEta_' or v == 'HiggsEta_nocuts_':
            rbn=1; xmin=-5.; xmax=5.; title='Higgs Eta'
        if v == 'deltaRbb_' or v == 'deltaRbb_nocuts_':
            rbn=10; xmin=0.; xmax=6.; title='DeltaR(bb)'
        if v == 'j1Pt_' or v == 'j1Pt_nocuts_':
            rbn=2; xmin=0.; xmax=500.; title='jet_1 Pt (GeV)'
        if v == 'j2Pt_' or v == 'j2Pt_nocuts_':
            rbn=2; xmin=0.; xmax=300.; title='jet_2 Pt (GeV)'
        if v == 'j1Eta_' or v == 'j1Eta_nocuts_':
            rbn=1; xmin=-5.; xmax=5.; title='jet_1 Eta'
        if v == 'j2Eta_' or v == 'j2Eta_nocuts_':
            rbn=1; xmin=-5.; xmax=5.; title='jet_2 Eta'
        for a in fat:
            for g in groom:
                hist_zh_var = zh.Get('HbbAnalyzer/' + a + '/' + g + '/' + v + a + g)

                hist_zh_var.Rebin(rbn)
                hist_zh_var.SetLineColor(ROOT.kBlack)
                hist_zh_var.SetMarkerStyle(20)
                hist_zh_var.SetMarkerColor(ROOT.kBlack)
                hist_zh_var.SetStats(1)

                canvas = ROOT.TCanvas()
                #canvas.SetLogy()
                hist_zh_var.GetXaxis().SetRangeUser(xmin, xmax)
                hist_zh_var.GetXaxis().SetTitleSize(0.05)
                hist_zh_var.GetXaxis().SetTitleOffset(0.8)
                hist_zh_var.GetXaxis().SetTitle(title)
                hist_zh_var.Draw()


                latex = ROOT.TLatex()
                latex.SetNDC()
                latex.SetTextSize(0.06)
                #latex.DrawLatex(0.14, 0.92, 'L = 5 fb^{-1}')
                latex.DrawLatex(0.10, 0.94, '#color[' + str(4) + ']{' + a + g + '}')
                canvas.Update()

                canvas.SaveAs('/uscms_data/d3/ingabu/CSA14/CMSSW_7_1_0_pre9/src/VHbb/HbbAnalyzer/macros/Gifs/MorePlots/'+ v + a + g + '.gif')

#******** Mult Fat Jet plots **************
if dofatmult:
    for v in var:
        if v == 'HiggsM_' or v == 'HiggsM_nocuts_' or v == 'HiggsM_bdtcuts_' or v == 'HiggsM_200cuts_' or v == 'HiggsM_300cuts_' or v == 'HiggsM_150masscuts_' or v == 'HiggsM_200masscuts_' or v == 'HiggsM_300masscuts_':
            rbn=10; xmin=0.; xmax=260.; title='Higgs Mass (GeV)'
        if v == 'HiggsPt_' or v == 'HiggsPt_nocuts_' or v == 'HiggsPt_bdtcuts_' or v == 'HiggsPt_200cuts_' or v == 'HiggsPt_300cuts_' or v == 'HiggsPt_150masscuts_' or v == 'HiggsPt_200masscuts_' or v == 'HiggsPt_300masscuts_':
            rbn=2; xmin=0.; xmax=500.; title='Higgs Pt (GeV)'
        if v == 'ZBosonPt_' or v == 'ZBosonPt_200cuts_' or v == 'ZBosonPt_300cuts_' or v == 'ZBosonPt_150masscuts_' or v == 'ZBosonPt_200masscuts_' or v == 'ZBosonPt_300masscuts_':
            rbn=2; xmin=0.; xmax=500.; title='Z Boson Pt (GeV)'
        if v == 'HiggsEta_' or v == 'HiggsEta_nocuts_':
            rbn=2; xmin=-4.; xmax=4.; title='Higgs Eta'
        if v == 'deltaRbb_' or v == 'deltaRbb_nocuts_' or v == 'deltaRbb_bdtcuts_' or v == 'deltaRbb_200cuts_' or v == 'deltaRbb_300cuts_' or v == 'deltaRbb_150masscuts_' or v == 'deltaRbb_200masscuts_' or v == 'deltaRbb_300masscuts_':
            rbn=5; xmin=0.; xmax=2.; title='DeltaR(bb)'
        if v == 'j1Pt_' or v == 'j1Pt_nocuts_' or v == 'j1Pt_bdtcuts_' or v == 'j1Pt_200cuts_' or v == 'j1Pt_300cuts_' or v == 'j1Pt_150masscuts_' or v == 'j1Pt_200masscuts_' or v == 'j1Pt_300masscuts_':
            rbn=2; xmin=0.; xmax=500.; title='jet_1 Pt (GeV)'
        if v == 'j2Pt_' or v == 'j2Pt_nocuts_' or v == 'j2Pt_bdtcuts_' or v == 'j2Pt_200cuts_' or v == 'j2Pt_300cuts_' or v == 'j2Pt_150masscuts_' or v == 'j2Pt_200masscuts_' or v == 'j2Pt_300masscuts_':
            rbn=2; xmin=0.; xmax=300.; title='jet_2 Pt (GeV)'
        if v == 'j1Eta_' or v == 'j1Eta_nocuts_' or v == 'j1Eta_bdtcuts_':
            rbn=2; xmin=-4.; xmax=4.; title='jet_1 Eta'
        if v == 'j2Eta_' or v == 'j2Eta_nocuts_' or v == 'j2Eta_bdtcuts_':
            rbn=2; xmin=-4.; xmax=4.; title='jet_2 Eta'

        hist_zh_var_AK4 = zh.Get('HbbAnalyzer/AK4/' + v + 'AK4')
        hist_zh_var_AK4.Rebin(rbn)
        hist_zh_var_AK4.SetLineColor(ROOT.kMagenta)
        hist_zh_var_AK4.SetLineWidth(3)
        hist_zh_var_AK4.SetFillColor(ROOT.kMagenta)
        hist_zh_var_AK4.SetFillStyle(3022)
        #hist_zh_var_AK4.SetMarkerStyle(20)
        #hist_zh_var_AK4.SetMarkerColor(ROOT.kMagenta)
        hist_zh_var_AK4.SetStats(0)

        if doungr and not (v == 'HiggsPt_') and not (v == 'HiggsPt_200cuts_') and not (v == 'HiggsPt_300cuts_') and not (v == 'HiggsPt_150masscuts_') and not (v == 'HiggsPt_200masscuts_') and not (v == 'HiggsPt_300masscuts_') and not (v == 'HiggsM_') and not (v == 'HiggsM_200cuts_') and not (v == 'HiggsM_300cuts_'): continue

        for a in fat:
            hist_zh_var_filt = zh.Get('HbbAnalyzer/' + a + '/_filtered/' + v + a + '_filtered')
            hist_zh_var_prun = zh.Get('HbbAnalyzer/' + a + '/_pruned/' + v + a + '_pruned')
            hist_zh_var_trim = zh.Get('HbbAnalyzer/' + a + '/_trimmed/' + v + a + '_trimmed')
            hist_zh_var_mdt = zh.Get('HbbAnalyzer/' + a + '/_mdt/' + v + a + '_mdt')
            hist_zh_var_bdrs = zh.Get('HbbAnalyzer/' + a + '/_bdrs/' + v + a + '_bdrs')
            if doungr and (v == 'HiggsM_' or v == 'HiggsM_200cuts_' or v == 'HiggsM_300cuts_'):
                if v == 'HiggsM_': hist_zh_var_ungr = zh.Get('HbbAnalyzer/' + a + '/HiggsM_150cut_ungr_' + a)
                if v == 'HiggsM_200cuts_': hist_zh_var_ungr = zh.Get('HbbAnalyzer/' + a + '/HiggsM_200cut_ungr_' + a)
                if v == 'HiggsM_300cuts_': hist_zh_var_ungr = zh.Get('HbbAnalyzer/' + a + '/HiggsM_300cut_ungr_' + a)
            if doungr and (v == 'HiggsPt_' or v == 'HiggsPt_200cuts_' or v == 'HiggsPt_300cuts_' or v == 'HiggsPt_150masscuts_' or v == 'HiggsPt_200masscuts_' or v == 'HiggsPt_300masscuts_'):
                if v == 'HiggsPt_': hist_zh_var_ungr = zh.Get('HbbAnalyzer/' + a + '/HiggsPt_150cut_ungr_' + a)
                if v == 'HiggsPt_200cuts_': hist_zh_var_ungr = zh.Get('HbbAnalyzer/' + a + '/HiggsPt_200cut_ungr_' + a)
                if v == 'HiggsPt_300cuts_': hist_zh_var_ungr = zh.Get('HbbAnalyzer/' + a + '/HiggsPt_300cut_ungr_' + a)
                if v == 'HiggsPt_150masscuts_': hist_zh_var_ungr = zh.Get('HbbAnalyzer/' + a + '/HiggsPt_150masscut_ungr_' + a)
                if v == 'HiggsPt_200masscuts_': hist_zh_var_ungr = zh.Get('HbbAnalyzer/' + a + '/HiggsPt_200masscut_ungr_' + a)
                if v == 'HiggsPt_300masscuts_': hist_zh_var_ungr = zh.Get('HbbAnalyzer/' + a + '/HiggsPt_300masscut_ungr_' + a)

            hist_zh_var_filt.Rebin(rbn)
            hist_zh_var_filt.SetLineColor(ROOT.kBlack)
            hist_zh_var_filt.SetLineWidth(3)
            hist_zh_var_filt.SetFillColor(ROOT.kBlack)
            hist_zh_var_filt.SetFillStyle(3012)
            #hist_zh_var_filt.SetMarkerStyle(20)
            #hist_zh_var_filt.SetMarkerColor(ROOT.kBlack)
            hist_zh_var_filt.SetStats(0)
            hist_zh_var_prun.Rebin(rbn)
            hist_zh_var_prun.SetLineColor(ROOT.kRed)
            hist_zh_var_prun.SetLineWidth(3)
            hist_zh_var_prun.SetFillColor(ROOT.kRed)
            hist_zh_var_prun.SetFillStyle(3003)
            #hist_zh_var_prun.SetMarkerStyle(20)
            #hist_zh_var_prun.SetMarkerColor(ROOT.kRed)
            hist_zh_var_prun.SetStats(0)
            hist_zh_var_trim.Rebin(rbn)
            hist_zh_var_trim.SetLineColor(ROOT.kBlue)
            hist_zh_var_trim.SetLineWidth(3)
            hist_zh_var_trim.SetFillColor(ROOT.kBlue)
            hist_zh_var_trim.SetFillStyle(3244)
            #hist_zh_var_trim.SetMarkerStyle(20)
            #hist_zh_var_trim.SetMarkerColor(ROOT.kBlue)
            hist_zh_var_trim.SetStats(0)
            hist_zh_var_mdt.Rebin(rbn)
            hist_zh_var_mdt.SetLineColor(7)
            hist_zh_var_mdt.SetLineWidth(3)
            hist_zh_var_mdt.SetFillColor(7)
            hist_zh_var_mdt.SetFillStyle(3004)
            #hist_zh_var_mdt.SetMarkerStyle(20)
            #hist_zh_var_mdt.SetMarkerColor(3)
            hist_zh_var_mdt.SetStats(0)
            hist_zh_var_bdrs.Rebin(rbn)
            hist_zh_var_bdrs.SetLineColor(ROOT.kGreen)
            hist_zh_var_bdrs.SetLineWidth(3)
            hist_zh_var_bdrs.SetFillColor(ROOT.kGreen)
            hist_zh_var_bdrs.SetFillStyle(3020)
            #hist_zh_var_bdrs.SetMarkerStyle(20)
            #hist_zh_var_bdrs.SetMarkerColor(ROOT.kGreen)
            hist_zh_var_bdrs.SetStats(0)
            if doungr:
                hist_zh_var_ungr.SetLineColor(ROOT.kOrange+7)
                hist_zh_var_ungr.SetLineWidth(3)
                hist_zh_var_ungr.SetFillColor(ROOT.kOrange+7)
                hist_zh_var_ungr.SetFillStyle(3019)
                hist_zh_var_ungr.SetStats(0)

            canvas = ROOT.TCanvas()
            #canvas.SetLogy()

            ymax = hist_zh_var_trim.GetMaximum()
            if ymax < hist_zh_var_AK4.GetMaximum(): ymax = hist_zh_var_AK4.GetMaximum()
            if ymax < hist_zh_var_filt.GetMaximum(): ymax = hist_zh_var_filt.GetMaximum()
            if ymax < hist_zh_var_prun.GetMaximum(): ymax = hist_zh_var_prun.GetMaximum()
            if ymax < hist_zh_var_bdrs.GetMaximum(): ymax = hist_zh_var_bdrs.GetMaximum()
            if ymax < hist_zh_var_mdt.GetMaximum(): ymax = hist_zh_var_mdt.GetMaximum()
            if doungr and ymax < hist_zh_var_ungr.GetMaximum(): ymax = hist_zh_var_ungr.GetMaximum()
            ymin = hist_zh_var_trim.GetMinimum()
            #print "ymax ", ymax
            ymaxim = ymax + 0.1*ymax
            if v == 'deltaRbb_' or v == 'deltaRbb_nocuts_' or v == 'deltaRbb_bdtcuts_' or v == 'deltaRbb_200cuts_' or v == 'deltaRbb_300cuts_' or v == 'deltaRbb_150masscuts_' or v == 'deltaRbb_200masscuts_' or v == 'deltaRbb_300masscuts_': ymaxim = ymax
            if v == 'HiggsM_' or v == 'HiggsM_nocuts_' or v == 'HiggsM_bdtcuts_' or v == 'HiggsM_200cuts_' or v == 'HiggsM_300cuts_' or v == 'HiggsM_150masscuts_' or v == 'HiggsM_200masscuts_' or v == 'HiggsM_300masscuts_': ymaxim = ymax - 0.1*ymax
            hist_zh_var_trim.GetXaxis().SetRangeUser(xmin, xmax)
            hist_zh_var_trim.GetYaxis().SetRangeUser(ymin, ymaxim)
            hist_zh_var_trim.GetXaxis().SetTitleSize(0.05)
            hist_zh_var_trim.GetXaxis().SetTitleOffset(0.8)
            hist_zh_var_trim.GetXaxis().SetTitle(title)
            hist_zh_var_filt.GetXaxis().SetRangeUser(xmin, xmax)
            hist_zh_var_filt.GetYaxis().SetRangeUser(ymin, ymaxim)
            hist_zh_var_filt.GetXaxis().SetTitleSize(0.05)
            hist_zh_var_filt.GetXaxis().SetTitleOffset(0.8)
            hist_zh_var_filt.GetXaxis().SetTitle(title)
            hist_zh_var_prun.GetXaxis().SetRangeUser(xmin, xmax)
            hist_zh_var_prun.GetYaxis().SetRangeUser(ymin, ymaxim)
            hist_zh_var_prun.GetXaxis().SetTitleSize(0.05)
            hist_zh_var_prun.GetXaxis().SetTitleOffset(0.8)
            hist_zh_var_prun.GetXaxis().SetTitle(title)
            hist_zh_var_bdrs.GetXaxis().SetRangeUser(xmin, xmax)
            hist_zh_var_bdrs.GetYaxis().SetRangeUser(ymin, ymaxim)
            hist_zh_var_bdrs.GetXaxis().SetTitleSize(0.05)
            hist_zh_var_bdrs.GetXaxis().SetTitleOffset(0.8)
            hist_zh_var_bdrs.GetXaxis().SetTitle(title)
            hist_zh_var_mdt.GetXaxis().SetRangeUser(xmin, xmax)
            hist_zh_var_mdt.GetYaxis().SetRangeUser(ymin, ymaxim)
            hist_zh_var_mdt.GetXaxis().SetTitleSize(0.05)
            hist_zh_var_mdt.GetXaxis().SetTitleOffset(0.8)
            hist_zh_var_mdt.GetXaxis().SetTitle(title)
            hist_zh_var_AK4.GetXaxis().SetRangeUser(xmin, xmax)
            hist_zh_var_AK4.GetYaxis().SetRangeUser(ymin, ymaxim)
            hist_zh_var_AK4.GetXaxis().SetTitleSize(0.05)
            hist_zh_var_AK4.GetXaxis().SetTitleOffset(0.8)
            hist_zh_var_AK4.GetXaxis().SetTitle(title)
            if doungr: 
                hist_zh_var_ungr.GetXaxis().SetRangeUser(xmin, xmax)
                hist_zh_var_ungr.GetYaxis().SetRangeUser(ymin, ymaxim)
                hist_zh_var_ungr.GetXaxis().SetTitleSize(0.05)
                hist_zh_var_ungr.GetXaxis().SetTitleOffset(0.8)
                hist_zh_var_ungr.GetXaxis().SetTitle(title)
                
            hist_zh_var_bdrs.Draw()
            if doungr: hist_zh_var_ungr.Draw("same")
            hist_zh_var_filt.Draw("same")
            hist_zh_var_AK4.Draw("same")
            hist_zh_var_prun.Draw("same")
            hist_zh_var_mdt.Draw("same")
            hist_zh_var_trim.Draw("same")

            latex = ROOT.TLatex()
            latex.SetNDC()
            latex.SetTextSize(0.06)
            #latex.DrawLatex(0.14, 0.92, 'L = 5 fb^{-1}')
            latex.DrawLatex(0.10, 0.94, '#color[' + str(4) + ']{' + a + '}')

            xl1=.73; yl1=.63 
            if doungr: xl1=.68
            xl2=xl1+.15; yl2=yl1+.25
            leg =ROOT.TLegend(xl1,yl1,xl2,yl2);
            leg.SetFillColor(0);
            leg.SetLineColor(0);
            leg.SetShadowColor(0);
            leg.AddEntry(hist_zh_var_filt,"filtered","l");
            leg.AddEntry(hist_zh_var_prun,"pruned","l");
            leg.AddEntry(hist_zh_var_trim,"trimmed","l");
            leg.AddEntry(hist_zh_var_mdt,"mdt","l");
            leg.AddEntry(hist_zh_var_bdrs,"bdrs","l");
            if doungr: leg.AddEntry(hist_zh_var_ungr,"ungroomed","l");
            leg.AddEntry(hist_zh_var_AK4,"AK4","l");
            leg.SetTextSize(0.045);    
            leg.Draw();

            canvas.Update()

            if not doungr: canvas.SaveAs('/uscms_data/d3/ingabu/CSA14/CMSSW_7_1_0_pre9/src/VHbb/HbbAnalyzer/macros/Gifs/MorePlots/'+ v + a + 'multwAK4.gif')
            if doungr: canvas.SaveAs('/uscms_data/d3/ingabu/CSA14/CMSSW_7_1_0_pre9/src/VHbb/HbbAnalyzer/macros/Gifs/MorePlots/'+ v + a + 'multwAK4_ungr.gif')

#******** Efficiency plots **************
if doZeff:
    hist_zh_genZ = zh.Get('HbbAnalyzer/ZBoson/genZPt_goodZcuts')
    hist_zh_genZ.Sumw2()
    
    hist_zh_recoZ = zh.Get('HbbAnalyzer/ZBoson/genZPt_recoZ')
    hist_zh_recoZ.Sumw2()
    rbn=2; xmin=0.; xmax=500.; title='gen Z Pt (GeV)'

    hist_zh_recoZ.Rebin(rbn)
    hist_zh_genZ.Rebin(rbn)
    hist_zh_recoZ.SetLineColor(ROOT.kBlack)
    hist_zh_recoZ.SetStats(0)

    hist_zh_recoZ_rat = hist_zh_recoZ.Clone()
    hist_zh_recoZ_rat.Divide(hist_zh_recoZ,hist_zh_genZ,1.,1.,"b");

    canvas = ROOT.TCanvas()
    #canvas.SetLogy()
    hist_zh_recoZ_rat.GetXaxis().SetRangeUser(xmin, xmax)
    hist_zh_recoZ_rat.GetXaxis().SetTitleSize(0.05)
    hist_zh_recoZ_rat.GetXaxis().SetTitleOffset(0.8)
    hist_zh_recoZ_rat.GetXaxis().SetTitle(title)
    hist_zh_recoZ_rat.Draw()

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.06)
    #latex.DrawLatex(0.14, 0.92, 'L = 5 fb^{-1}')
    latex.DrawLatex(0.10, 0.94, '#color[' + str(4) + ']{' + 'Z Boson' + '}')
    canvas.Update()

    canvas.SaveAs('/uscms_data/d3/ingabu/CSA14/CMSSW_7_1_0_pre9/src/VHbb/HbbAnalyzer/macros/Gifs/MorePlots/'+ 'Zeff' + '.gif')

#**********fat eff **********
if dofateff:

    hist_zh_genH = zh.Get('HbbAnalyzer/genParticles/genHPt_hcuts')
    hist_zh_genH.Sumw2()

    rbn=5; xmin=0.; xmax=600.; title='gen H Pt (GeV)'
    #hist_zh_genH.Rebin(rbn)
    hist_zh_genH = RebinHist(hist_zh_genH, nbins, False)

    for v in effvar:
        if v == 'genHPt_recoH_300_' or v == 'genHPt_recoH_tightm300_': xmax = 800.
        hist_zh_var_AK4 = zh.Get('HbbAnalyzer/AK4/' + v + 'AK4')
        hist_zh_var_AK4.Sumw2()
        hist_zh_var_AK4.SetLineColor(ROOT.kMagenta)
        hist_zh_var_AK4.SetLineWidth(3)
        hist_zh_var_AK4.SetMarkerStyle(21)
        hist_zh_var_AK4.SetMarkerColor(ROOT.kMagenta)
        hist_zh_var_AK4.SetStats(0)
        #hist_zh_var_AK4.Rebin(rbn)
        hist_zh_var_AK4 = RebinHist(hist_zh_var_AK4, nbins, False)
        for a in fat:
            hist_zh_var_filt = zh.Get('HbbAnalyzer/' + a + '/' + '_filtered/' + v + a + '_filtered')
            hist_zh_var_filt.Sumw2()
            hist_zh_var_prun = zh.Get('HbbAnalyzer/' + a + '/' + '_pruned/' + v + a + '_pruned')
            hist_zh_var_prun.Sumw2()
            hist_zh_var_trim = zh.Get('HbbAnalyzer/' + a + '/' + '_trimmed/' + v + a + '_trimmed')
            hist_zh_var_trim.Sumw2()
            hist_zh_var_mdt = zh.Get('HbbAnalyzer/' + a + '/' + '_mdt/' + v + a + '_mdt')
            hist_zh_var_mdt.Sumw2()
            hist_zh_var_bdrs = zh.Get('HbbAnalyzer/' + a + '/' + '_bdrs/' + v + a + '_bdrs')
            hist_zh_var_bdrs.Sumw2()

            #hist_zh_var_filt.Rebin(rbn)
            hist_zh_var_filt = RebinHist(hist_zh_var_filt, nbins, False)
            hist_zh_var_filt.SetLineColor(ROOT.kBlack)
            hist_zh_var_filt.SetLineWidth(3)
            hist_zh_var_filt.SetMarkerStyle(20)
            hist_zh_var_filt.SetMarkerColor(ROOT.kBlack)
            hist_zh_var_filt.SetStats(0)
            #hist_zh_var_prun.Rebin(rbn)
            hist_zh_var_prun = RebinHist(hist_zh_var_prun, nbins, False)
            hist_zh_var_prun.SetLineColor(ROOT.kRed)
            hist_zh_var_prun.SetLineWidth(3)
            hist_zh_var_prun.SetMarkerStyle(22)
            hist_zh_var_prun.SetMarkerColor(ROOT.kRed)
            hist_zh_var_prun.SetStats(0)
            #hist_zh_var_trim.Rebin(rbn)
            hist_zh_var_trim = RebinHist(hist_zh_var_trim, nbins, False)
            hist_zh_var_trim.SetLineColor(ROOT.kBlue)
            hist_zh_var_trim.SetLineWidth(3)
            hist_zh_var_trim.SetMarkerStyle(34)
            hist_zh_var_trim.SetMarkerColor(ROOT.kBlue)
            hist_zh_var_trim.SetStats(0)
            #hist_zh_var_mdt.Rebin(rbn)
            hist_zh_var_mdt = RebinHist(hist_zh_var_mdt, nbins, False)
            hist_zh_var_mdt.SetLineColor(7)
            hist_zh_var_mdt.SetLineWidth(3)
            hist_zh_var_mdt.SetMarkerStyle(29)
            hist_zh_var_mdt.SetMarkerColor(7)
            hist_zh_var_mdt.SetStats(0)
            #hist_zh_var_bdrs.Rebin(rbn)
            hist_zh_var_bdrs = RebinHist(hist_zh_var_bdrs, nbins, False)
            hist_zh_var_bdrs.SetLineColor(ROOT.kGreen)
            hist_zh_var_bdrs.SetLineWidth(3)
            hist_zh_var_bdrs.SetMarkerStyle(23)
            hist_zh_var_bdrs.SetMarkerColor(ROOT.kGreen)
            hist_zh_var_bdrs.SetStats(0)

            hist_zh_var_AK4_rat = hist_zh_var_AK4.Clone()
            hist_zh_var_AK4_rat.Divide(hist_zh_var_AK4,hist_zh_genH,1.,1.,"b");
            hist_zh_var_filt_rat = hist_zh_var_filt.Clone()
            hist_zh_var_filt_rat.Divide(hist_zh_var_filt,hist_zh_genH,1.,1.,"b");
            hist_zh_var_prun_rat = hist_zh_var_prun.Clone()
            hist_zh_var_prun_rat.Divide(hist_zh_var_prun,hist_zh_genH,1.,1.,"b");
            hist_zh_var_trim_rat = hist_zh_var_trim.Clone()
            hist_zh_var_trim_rat.Divide(hist_zh_var_trim,hist_zh_genH,1.,1.,"b");
            hist_zh_var_mdt_rat = hist_zh_var_mdt.Clone()
            hist_zh_var_mdt_rat.Divide(hist_zh_var_mdt,hist_zh_genH,1.,1.,"b");
            hist_zh_var_bdrs_rat = hist_zh_var_bdrs.Clone()
            hist_zh_var_bdrs_rat.Divide(hist_zh_var_bdrs,hist_zh_genH,1.,1.,"b");

            canvas = ROOT.TCanvas()
            #canvas.SetLogy()
            hist_zh_var_trim_rat.GetXaxis().SetRangeUser(xmin, xmax)
            hist_zh_var_trim_rat.GetXaxis().SetTitleSize(0.05)
            hist_zh_var_trim_rat.GetXaxis().SetTitleOffset(0.8)
            hist_zh_var_trim_rat.GetXaxis().SetTitle(title)
            hist_zh_var_trim_rat.Draw()
            hist_zh_var_filt_rat.Draw("same")
            hist_zh_var_prun_rat.Draw("same")
            hist_zh_var_AK4_rat.Draw("same")
            hist_zh_var_mdt_rat.Draw("same")
            hist_zh_var_bdrs_rat.Draw("same")

            latex = ROOT.TLatex()
            latex.SetNDC()
            latex.SetTextSize(0.06)
            #latex.DrawLatex(0.14, 0.92, 'L = 5 fb^{-1}')
            latex.DrawLatex(0.10, 0.94, '#color[' + str(4) + ']{' + a + '}')

            xl1=.13; yl1=.6 
            xl2=xl1+.15; yl2=yl1+.23
            leg =ROOT.TLegend(xl1,yl1,xl2,yl2);
            leg.SetFillColor(0);
            leg.SetLineColor(0);
            leg.SetShadowColor(0);
            leg.AddEntry(hist_zh_var_filt,"filtered","l");
            leg.AddEntry(hist_zh_var_prun,"pruned","l");
            leg.AddEntry(hist_zh_var_trim,"trimmed","l");
            leg.AddEntry(hist_zh_var_mdt,"mdt","l");
            leg.AddEntry(hist_zh_var_bdrs,"bdrs","l");
            leg.AddEntry(hist_zh_var_AK4,"AK4","l");
            leg.SetTextSize(0.045);    
            leg.Draw();

            canvas.Update()

            canvas.SaveAs('/uscms_data/d3/ingabu/CSA14/CMSSW_7_1_0_pre9/src/VHbb/HbbAnalyzer/macros/Gifs/MorePlots/Eff_' + v + a + '.gif')

#**********fat eff **********
if dofateffZ:

    hist_zh_Z = zh.Get('HbbAnalyzer/ZBoson/ZPt')
    hist_zh_Z.Sumw2()

    rbn=5; xmin=0.; xmax=600.; title='reco Z Pt (GeV)'
    #hist_zh_Z.Rebin(rbn)
    hist_zh_Z = RebinHist(hist_zh_Z, nbins, False)
    
    for v in Zeffvar:
        if v == 'ZBosonPt_300cuts_' or v == 'ZBosonPt_300masscuts_': xmax = 800.
        hist_zh_var_AK4 = zh.Get('HbbAnalyzer/AK4/' + v + 'AK4')
        hist_zh_var_AK4.Sumw2()
        hist_zh_var_AK4.SetLineColor(ROOT.kMagenta)
        hist_zh_var_AK4.SetLineWidth(3)
        hist_zh_var_AK4.SetMarkerStyle(21)
        hist_zh_var_AK4.SetMarkerColor(ROOT.kMagenta)
        hist_zh_var_AK4.SetStats(0)
        #hist_zh_var_AK4.Rebin(rbn)
        hist_zh_var_AK4 = RebinHist(hist_zh_var_AK4, nbins, False)
        for a in fat:
            hist_zh_var_filt = zh.Get('HbbAnalyzer/' + a + '/' + '_filtered/' + v + a + '_filtered')
            hist_zh_var_filt.Sumw2()
            hist_zh_var_prun = zh.Get('HbbAnalyzer/' + a + '/' + '_pruned/' + v + a + '_pruned')
            hist_zh_var_prun.Sumw2()
            hist_zh_var_trim = zh.Get('HbbAnalyzer/' + a + '/' + '_trimmed/' + v + a + '_trimmed')
            hist_zh_var_trim.Sumw2()
            hist_zh_var_mdt = zh.Get('HbbAnalyzer/' + a + '/' + '_mdt/' + v + a + '_mdt')
            hist_zh_var_mdt.Sumw2()
            hist_zh_var_bdrs = zh.Get('HbbAnalyzer/' + a + '/' + '_bdrs/' + v + a + '_bdrs')
            hist_zh_var_bdrs.Sumw2()

            #hist_zh_var_filt.Rebin(rbn)
            hist_zh_var_filt = RebinHist(hist_zh_var_filt, nbins, False)
            hist_zh_var_filt.SetLineColor(ROOT.kBlack)
            hist_zh_var_filt.SetLineWidth(3)
            hist_zh_var_filt.SetMarkerStyle(20)
            hist_zh_var_filt.SetMarkerColor(ROOT.kBlack)
            hist_zh_var_filt.SetStats(0)
            #hist_zh_var_prun.Rebin(rbn)
            hist_zh_var_prun = RebinHist(hist_zh_var_prun, nbins, False)
            hist_zh_var_prun.SetLineColor(ROOT.kRed)
            hist_zh_var_prun.SetLineWidth(3)
            hist_zh_var_prun.SetMarkerStyle(22)
            hist_zh_var_prun.SetMarkerColor(ROOT.kRed)
            hist_zh_var_prun.SetStats(0)
            #hist_zh_var_trim.Rebin(rbn)
            hist_zh_var_trim = RebinHist(hist_zh_var_trim, nbins, False)
            hist_zh_var_trim.SetLineColor(ROOT.kBlue)
            hist_zh_var_trim.SetLineWidth(3)
            hist_zh_var_trim.SetMarkerStyle(34)
            hist_zh_var_trim.SetMarkerColor(ROOT.kBlue)
            hist_zh_var_trim.SetStats(0)
            #hist_zh_var_mdt.Rebin(rbn)
            hist_zh_var_mdt = RebinHist(hist_zh_var_mdt, nbins, False)
            hist_zh_var_mdt.SetLineColor(7)
            hist_zh_var_mdt.SetLineWidth(3)
            hist_zh_var_mdt.SetMarkerStyle(29)
            hist_zh_var_mdt.SetMarkerColor(7)
            hist_zh_var_mdt.SetStats(0)
            #hist_zh_var_bdrs.Rebin(rbn)
            hist_zh_var_bdrs = RebinHist(hist_zh_var_bdrs, nbins, False)
            hist_zh_var_bdrs.SetLineColor(ROOT.kGreen)
            hist_zh_var_bdrs.SetLineWidth(3)
            hist_zh_var_bdrs.SetMarkerStyle(23)
            hist_zh_var_bdrs.SetMarkerColor(ROOT.kGreen)
            hist_zh_var_bdrs.SetStats(0)

            hist_zh_var_AK4_rat = hist_zh_var_AK4.Clone()
            hist_zh_var_AK4_rat.Divide(hist_zh_var_AK4,hist_zh_Z,1.,1.,"b");
            hist_zh_var_filt_rat = hist_zh_var_filt.Clone()
            hist_zh_var_filt_rat.Divide(hist_zh_var_filt,hist_zh_Z,1.,1.,"b");
            hist_zh_var_prun_rat = hist_zh_var_prun.Clone()
            hist_zh_var_prun_rat.Divide(hist_zh_var_prun,hist_zh_Z,1.,1.,"b");
            hist_zh_var_trim_rat = hist_zh_var_trim.Clone()
            hist_zh_var_trim_rat.Divide(hist_zh_var_trim,hist_zh_Z,1.,1.,"b");
            hist_zh_var_mdt_rat = hist_zh_var_mdt.Clone()
            hist_zh_var_mdt_rat.Divide(hist_zh_var_mdt,hist_zh_Z,1.,1.,"b");
            hist_zh_var_bdrs_rat = hist_zh_var_bdrs.Clone()
            hist_zh_var_bdrs_rat.Divide(hist_zh_var_bdrs,hist_zh_Z,1.,1.,"b");

            canvas = ROOT.TCanvas()
            #canvas.SetLogy()
            hist_zh_var_trim_rat.GetXaxis().SetRangeUser(xmin, xmax)
            hist_zh_var_trim_rat.GetXaxis().SetTitleSize(0.05)
            hist_zh_var_trim_rat.GetXaxis().SetTitleOffset(0.8)
            hist_zh_var_trim_rat.GetXaxis().SetTitle(title)
            hist_zh_var_trim_rat.Draw()
            hist_zh_var_filt_rat.Draw("same")
            hist_zh_var_prun_rat.Draw("same")
            hist_zh_var_AK4_rat.Draw("same")
            hist_zh_var_mdt_rat.Draw("same")
            hist_zh_var_bdrs_rat.Draw("same")

            latex = ROOT.TLatex()
            latex.SetNDC()
            latex.SetTextSize(0.06)
            #latex.DrawLatex(0.14, 0.92, 'L = 5 fb^{-1}')
            latex.DrawLatex(0.10, 0.94, '#color[' + str(4) + ']{' + a + '}')

            xl1=.13; yl1=.6 
            xl2=xl1+.15; yl2=yl1+.23
            leg =ROOT.TLegend(xl1,yl1,xl2,yl2);
            leg.SetFillColor(0);
            leg.SetLineColor(0);
            leg.SetShadowColor(0);
            leg.AddEntry(hist_zh_var_filt,"filtered","l");
            leg.AddEntry(hist_zh_var_prun,"pruned","l");
            leg.AddEntry(hist_zh_var_trim,"trimmed","l");
            leg.AddEntry(hist_zh_var_mdt,"mdt","l");
            leg.AddEntry(hist_zh_var_bdrs,"bdrs","l");
            leg.AddEntry(hist_zh_var_AK4,"AK4","l");
            leg.SetTextSize(0.045);    
            leg.Draw();

            canvas.Update()

            canvas.SaveAs('/uscms_data/d3/ingabu/CSA14/CMSSW_7_1_0_pre9/src/VHbb/HbbAnalyzer/macros/Gifs/MorePlots/Eff_' + v + a + '.gif')

    


#raw_input('...')
