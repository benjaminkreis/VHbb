import math,ROOT
from ROOT import gStyle

ROOT.gROOT.SetStyle('Plain')
ROOT.gROOT.SetBatch(ROOT.kTRUE)
gStyle.SetOptStat(1110)
gStyle.SetOptTitle(0)
gStyle.SetPadTickY(1)
gStyle.SetPadTickX(1)

doAK4 = False
dofat = False
doZ = False
dogen = False
doHmassAK4 = False
doHmassFat = False
doHmassAK4Int = False
doHmassFatInt = False
dotaus = True
dosingletau=False

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
cuts = ['_nocuts_', '_150cut_', '_150masscut_', '_200cut_', '_200masscut_', '_300cut_', '_300masscut_']

rbn=1
xmin=0
xmax=100
title = 'title'


zh = ROOT.TFile('/eos/uscms/store/user/ingabu/Higgs/CSA14/Anatuples/Hbb__ZH_HToBB_ZToLL_M-125_13TeV_PU40bx50_Moreplots.root')
dy = ROOT.TFile('/eos/uscms/store/user/ingabu/Higgs/CSA14/Anatuples/Hbb__DYJetsToLL_M-50_13TeV_PU40bx50_Moreplots.root')
tt = ROOT.TFile('/eos/uscms/store/user/ingabu/Higgs/CSA14/Anatuples/Hbb__TTJets_13TeV_PU40bx50_Moreplots.root')

#******** Z plots ****************
if doZ:
    for v in Zvar:
        hist_zh_var = zh.Get('HbbAnalyzer/ZBoson/' + v)
        hist_dy_var = dy.Get('HbbAnalyzer/ZBoson/' + v)
        hist_tt_var = tt.Get('HbbAnalyzer/ZBoson/' + v)
        
        if v == 'ZM':
            rbn=2; xmin=0.; xmax=260.; title='Z Mass (GeV)'
        if v == 'ZPt' or v == 'ZPt_150' or v == 'ZPt_300' or v == 'ZPt_onlymcut':
            rbn=2; xmin=0.; xmax=500.; title='Z Pt (GeV)'
        if v == 'ZEta':
            rbn=2; xmin=-4.; xmax=4.; title='Z Eta'
        if v == 'muon1Pt':
            rbn=2; xmin=0.; xmax=500.; title='muon_1 Pt (GeV)'
        if v == 'muon2Pt':
            rbn=2; xmin=0.; xmax=500.; title='muon_2 Pt (GeV)'
        if v == 'muon1Eta':
            rbn=2; xmin=-4.; xmax=4.; title='muon_1 Eta'
        if v == 'muon2Eta':
            rbn=2; xmin=-4.; xmax=4.; title='muon_2 Eta'

        hist_zh_var.Rebin(rbn)
        hist_zh_var.SetLineColor(ROOT.kBlack)
        hist_zh_var.SetStats(0)
        hist_dy_var.Rebin(rbn)
        hist_dy_var.SetLineColor(ROOT.kRed)
        hist_dy_var.SetStats(0)
        hist_tt_var.Rebin(rbn)
        hist_tt_var.SetLineColor(ROOT.kGreen)
        hist_tt_var.SetStats(0)


        canvas = ROOT.TCanvas()
        #canvas.SetLogy()
        hist_zh_var.GetXaxis().SetRangeUser(xmin, xmax)
        hist_zh_var.GetXaxis().SetTitleSize(0.05)
        hist_zh_var.GetXaxis().SetTitleOffset(0.8)
        hist_zh_var.GetXaxis().SetTitle(title)
        hist_dy_var.GetXaxis().SetRangeUser(xmin, xmax)
        hist_dy_var.GetXaxis().SetTitleSize(0.05)
        hist_dy_var.GetXaxis().SetTitleOffset(0.8)
        hist_dy_var.GetXaxis().SetTitle(title)
        hist_tt_var.GetXaxis().SetRangeUser(xmin, xmax)
        hist_tt_var.GetXaxis().SetTitleSize(0.05)
        hist_tt_var.GetXaxis().SetTitleOffset(0.8)
        hist_tt_var.GetXaxis().SetTitle(title)
        hist_zh_var.Draw()
        hist_dy_var.Draw("same")
        hist_tt_var.Draw("same")


        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.06)
        #latex.DrawLatex(0.10, 0.94, '#color[' + str(4) + ']{' + 'Z Boson' + '}')


        xl1=.13; yl1=.68 
        xl2=xl1+.15; yl2=yl1+.23
        leg =ROOT.TLegend(xl1,yl1,xl2,yl2);
        leg.SetFillColor(0);
        leg.SetLineColor(0);
        leg.SetShadowColor(0);
        leg.AddEntry(hist_zh_var,"ZH","l");
        leg.AddEntry(hist_dy_var,"DYJets","l");
        leg.AddEntry(hist_tt_var,"TTBar","l");
        leg.SetTextSize(0.045);    
        leg.Draw();

        canvas.Update()

        canvas.SaveAs('/uscms_data/d3/ingabu/CSA14/CMSSW_7_1_0_pre9/src/VHbb/HbbAnalyzer/macros/Gifs/SB/'+ v + '.gif')

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
        hist_zh_var.SetStats(0)
        hist_dy_var.Rebin(rbn)
        hist_dy_var.SetLineColor(ROOT.kRed)
        hist_dy_var.SetStats(0)
        hist_tt_var.Rebin(rbn)
        hist_tt_var.SetLineColor(ROOT.kGreen)
        hist_tt_var.SetStats(0)

        canvas = ROOT.TCanvas()
        #canvas.SetLogy()
        hist_zh_var.GetXaxis().SetRangeUser(xmin, xmax)
        hist_zh_var.GetXaxis().SetTitleSize(0.05)
        hist_zh_var.GetXaxis().SetTitleOffset(0.8)
        hist_zh_var.GetXaxis().SetTitle(title)
        hist_dy_var.GetXaxis().SetRangeUser(xmin, xmax)
        hist_dy_var.GetXaxis().SetTitleSize(0.05)
        hist_dy_var.GetXaxis().SetTitleOffset(0.8)
        hist_dy_var.GetXaxis().SetTitle(title)
        hist_tt_var.GetXaxis().SetRangeUser(xmin, xmax)
        hist_tt_var.GetXaxis().SetTitleSize(0.05)
        hist_tt_var.GetXaxis().SetTitleOffset(0.8)
        hist_tt_var.GetXaxis().SetTitle(title)
        hist_zh_var.Draw()
        hist_dy_var.Draw("same")
        hist_tt_var.Draw("same")


        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextSize(0.06)
        latex.DrawLatex(0.10, 0.94, '#color[' + str(4) + ']{' + 'GEN' + '}')
        canvas.Update()

        canvas.SaveAs('/uscms_data/d3/ingabu/CSA14/CMSSW_7_1_0_pre9/src/VHbb/HbbAnalyzer/macros/Gifs/First/'+ v + '.gif')

#******** AK4 Jet plots **************
if doAK4:
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
            rbn=2; xmin=0.; xmax=500.; title='jet_2 Pt (GeV)'
        if v == 'j1Eta_' or v == 'j1Eta_nocuts_':
            rbn=1; xmin=-5.; xmax=5.; title='jet_1 Eta'
        if v == 'j2Eta_' or v == 'j2Eta_nocuts_':
            rbn=1; xmin=-5.; xmax=5.; title='jet_2 Eta'
        for a in algo:
            hist_zh_var = zh.Get('HbbAnalyzer/AK4/' + v + a)
            hist_dy_var = dy.Get('HbbAnalyzer/AK4/' + v + a)
            hist_tt_var = tt.Get('HbbAnalyzer/AK4/' + v + a)

            hist_zh_var.Rebin(rbn)
            hist_zh_var.SetLineColor(ROOT.kBlack)
            hist_zh_var.SetStats(0)
            hist_dy_var.Rebin(rbn)
            hist_dy_var.SetLineColor(ROOT.kRed)
            hist_dy_var.SetStats(0)
            hist_tt_var.Rebin(rbn)
            hist_tt_var.SetLineColor(ROOT.kGreen)
            hist_tt_var.SetStats(0)

            canvas = ROOT.TCanvas()
            #canvas.SetLogy()
            hist_zh_var.GetXaxis().SetRangeUser(xmin, xmax)
            hist_zh_var.GetXaxis().SetTitleSize(0.05)
            hist_zh_var.GetXaxis().SetTitleOffset(0.8)
            hist_zh_var.GetXaxis().SetTitle(title)
            hist_dy_var.GetXaxis().SetRangeUser(xmin, xmax)
            hist_dy_var.GetXaxis().SetTitleSize(0.05)
            hist_dy_var.GetXaxis().SetTitleOffset(0.8)
            hist_dy_var.GetXaxis().SetTitle(title)
            hist_tt_var.GetXaxis().SetRangeUser(xmin, xmax)
            hist_tt_var.GetXaxis().SetTitleSize(0.05)
            hist_tt_var.GetXaxis().SetTitleOffset(0.8)
            hist_tt_var.GetXaxis().SetTitle(title)
            hist_zh_var.Draw()
            hist_dy_var.Draw("same")
            hist_tt_var.Draw("same")


            latex = ROOT.TLatex()
            latex.SetNDC()
            latex.SetTextSize(0.06)
            #latex.DrawLatex(0.14, 0.92, 'L = 5 fb^{-1}')
            latex.DrawLatex(0.10, 0.94, '#color[' + str(4) + ']{' + a + '}')

            xl1=.13; yl1=.68 
            xl2=xl1+.15; yl2=yl1+.23
            leg =ROOT.TLegend(xl1,yl1,xl2,yl2);
            leg.SetFillColor(0);
            leg.SetLineColor(0);
            leg.SetShadowColor(0);
            leg.AddEntry(hist_zh_var,"ZH","l");
            leg.AddEntry(hist_dy_var,"DYJets","l");
            leg.AddEntry(hist_tt_var,"TTBar","l");
            leg.SetTextSize(0.045);    
            leg.Draw();

            canvas.Update()

            canvas.SaveAs('/uscms_data/d3/ingabu/CSA14/CMSSW_7_1_0_pre9/src/VHbb/HbbAnalyzer/macros/Gifs/SB/'+ v + a + '.gif')


#******** Fat Jet plots **************
if dofat:
    for v in var:
        if v == 'HiggsM_' or v == 'HiggsM_nocuts_':
            rbn=4; xmin=0.; xmax=260.; title='Higgs Mass (GeV)'
        if v == 'HiggsPt_' or v == 'HiggsPt_nocuts_':
            rbn=2; xmin=0.; xmax=500.; title='Higgs Pt (GeV)'
        if v == 'HiggsEta_' or v == 'HiggsEta_nocuts_':
            rbn=2; xmin=-4.; xmax=4.; title='Higgs Eta'
        if v == 'deltaRbb_' or v == 'deltaRbb_nocuts_':
            rbn=10; xmin=0.; xmax=6.; title='DeltaR(bb)'
        if v == 'j1Pt_' or v == 'j1Pt_nocuts_':
            rbn=2; xmin=0.; xmax=500.; title='jet_1 Pt (GeV)'
        if v == 'j2Pt_' or v == 'j2Pt_nocuts_':
            rbn=2; xmin=0.; xmax=500.; title='jet_2 Pt (GeV)'
        if v == 'j1Eta_' or v == 'j1Eta_nocuts_':
            rbn=2; xmin=-4.; xmax=4.; title='jet_1 Eta'
        if v == 'j2Eta_' or v == 'j2Eta_nocuts_':
            rbn=2; xmin=-4.; xmax=4.; title='jet_2 Eta'
        for a in fat:
            for g in groom:
                hist_zh_var = zh.Get('HbbAnalyzer/' + a + '/' + g + '/' + v + a + g)
                hist_dy_var = dy.Get('HbbAnalyzer/' + a + '/' + g + '/' + v + a + g)
                hist_tt_var = tt.Get('HbbAnalyzer/' + a + '/' + g + '/' + v + a + g)

                hist_zh_var.Rebin(rbn)
                hist_zh_var.SetLineColor(ROOT.kBlack)
                hist_zh_var.SetStats(0)
                hist_dy_var.Rebin(rbn)
                hist_dy_var.SetLineColor(ROOT.kRed)
                hist_dy_var.SetStats(0)
                hist_tt_var.Rebin(rbn)
                hist_tt_var.SetLineColor(ROOT.kGreen)
                hist_tt_var.SetStats(0)

                canvas = ROOT.TCanvas()
                #canvas.SetLogy()
                hist_zh_var.GetXaxis().SetRangeUser(xmin, xmax)
                hist_zh_var.GetXaxis().SetTitleSize(0.05)
                hist_zh_var.GetXaxis().SetTitleOffset(0.8)
                hist_zh_var.GetXaxis().SetTitle(title)
                hist_dy_var.GetXaxis().SetRangeUser(xmin, xmax)
                hist_dy_var.GetXaxis().SetTitleSize(0.05)
                hist_dy_var.GetXaxis().SetTitleOffset(0.8)
                hist_dy_var.GetXaxis().SetTitle(title)
                hist_tt_var.GetXaxis().SetRangeUser(xmin, xmax)
                hist_tt_var.GetXaxis().SetTitleSize(0.05)
                hist_tt_var.GetXaxis().SetTitleOffset(0.8)
                hist_tt_var.GetXaxis().SetTitle(title)
                hist_zh_var.Draw()
                hist_dy_var.Draw("same")
                hist_tt_var.Draw("same")


                latex = ROOT.TLatex()
                latex.SetNDC()
                latex.SetTextSize(0.06)
                #latex.DrawLatex(0.14, 0.92, 'L = 5 fb^{-1}')
                latex.DrawLatex(0.10, 0.94, '#color[' + str(4) + ']{' + a + g + '}')

                xl1=.13; yl1=.68 
                xl2=xl1+.15; yl2=yl1+.23
                leg =ROOT.TLegend(xl1,yl1,xl2,yl2);
                leg.SetFillColor(0);
                leg.SetLineColor(0);
                leg.SetShadowColor(0);
                leg.AddEntry(hist_zh_var,"ZH","l");
                leg.AddEntry(hist_dy_var,"DYJets","l");
                leg.AddEntry(hist_tt_var,"TTBar","l");
                leg.SetTextSize(0.045);    
                leg.Draw();

                canvas.Update()

                canvas.SaveAs('/uscms_data/d3/ingabu/CSA14/CMSSW_7_1_0_pre9/src/VHbb/HbbAnalyzer/macros/Gifs/SB/'+ v + a + g + '.gif')

#******** H mass *******************
if doHmassAK4:
    for v in var:
        if not (v == 'HiggsM_') and not (v == 'HiggsM_nocuts_') and not (v == 'HiggsM_bdtcuts_') and not (v == 'HiggsM_300cuts_'): continue
        if v == 'HiggsM_' or v == 'HiggsM_nocuts_' or v == 'HiggsM_bdtcuts_':
                rbn=10; xmin=0.; xmax=260.; title='Higgs Mass (GeV)'
        if v == 'HiggsM_300cuts_':
                rbn=5; xmin=0.; xmax=260.; title='Higgs Mass (GeV)'
        for a in algo:
            hist_zh_var = zh.Get('HbbAnalyzer/AK4/' + v + a)
            hist_dy_var = dy.Get('HbbAnalyzer/AK4/' + v + a)
            hist_tt_var = tt.Get('HbbAnalyzer/AK4/' + v + a)

            hist_zh_var.Rebin(rbn)
            hist_zh_var.SetLineColor(ROOT.kBlack)
            hist_zh_var.SetLineWidth(3)
            hist_zh_var.SetStats(0)
            hist_zh_var.Scale(20.0 * 0.0288 / 198566.)
            hist_dy_var.Rebin(rbn)
            hist_dy_var.SetLineColor(ROOT.kRed)
            hist_dy_var.SetLineWidth(3)
            hist_dy_var.SetStats(0)
            hist_dy_var.Scale(20.0 * 4746. / 2603552.)
            hist_tt_var.Rebin(rbn)
            hist_tt_var.SetLineColor(ROOT.kBlue)
            hist_tt_var.SetLineWidth(3)
            hist_tt_var.SetStats(0)
            hist_tt_var.Scale(20.0 * 424.5 / 24893609.)

            canvas = ROOT.TCanvas()
            canvas.SetLogy()
            ymin = 10e-5
            ymax = 500.
            hist_zh_var.GetXaxis().SetRangeUser(xmin, xmax)
            hist_zh_var.GetYaxis().SetRangeUser(ymin, ymax)
            hist_zh_var.GetXaxis().SetTitleSize(0.05)
            hist_zh_var.GetXaxis().SetTitleOffset(0.8)
            hist_zh_var.GetXaxis().SetTitle(title)
            hist_dy_var.GetXaxis().SetRangeUser(xmin, xmax)
            hist_dy_var.GetYaxis().SetRangeUser(ymin, ymax)
            hist_dy_var.GetXaxis().SetTitleSize(0.05)
            hist_dy_var.GetXaxis().SetTitleOffset(0.8)
            hist_dy_var.GetXaxis().SetTitle(title)
            hist_tt_var.GetXaxis().SetRangeUser(xmin, xmax)
            hist_tt_var.GetYaxis().SetRangeUser(ymin, ymax)
            hist_tt_var.GetXaxis().SetTitleSize(0.05)
            hist_tt_var.GetXaxis().SetTitleOffset(0.8)
            hist_tt_var.GetXaxis().SetTitle(title)
            hist_dy_var.Draw()
            hist_zh_var.Draw("same")
            hist_tt_var.Draw("same")

            Zh=0
            Zjets=0
            TTbar=0
            ErrZh=0
            ErrZjets=0
            ErrTTbar=0
            for b in range(hist_zh_var.GetNbinsX()):
                if hist_zh_var.GetBinLowEdge(b) >= 90 and hist_zh_var.GetBinLowEdge(b) < 138: # integrate from 90 to 140
                    Zh = Zh+ hist_zh_var.GetBinContent(b)
                    ErrZh = math.sqrt(pow(ErrZh,2)+ pow(hist_zh_var.GetBinError(b),2))
            print hist_zh_var.Integral(), Zh, ErrZh

            imin=hist_zh_var.GetXaxis().FindBin(90.1)
            imax=hist_zh_var.GetXaxis().FindBin(139.9)
            print imin,imax
            print hist_zh_var.Integral()
            error= ROOT.Double(0.)
            int= hist_zh_var.IntegralAndError(imin,imax,error)
            print int, error

            for b in range(hist_dy_var.GetNbinsX()):
                if hist_dy_var.GetBinLowEdge(b) >= 90 and hist_dy_var.GetBinLowEdge(b) < 138:
                    Zjets = Zjets+ hist_dy_var.GetBinContent(b)
                    ErrZjets = math.sqrt(pow(ErrZjets,2)+ pow(hist_dy_var.GetBinError(b),2))
            print hist_dy_var.Integral(),Zjets

            for b in range(hist_tt_var.GetNbinsX()):
                if hist_tt_var.GetBinLowEdge(b) >= 90 and hist_tt_var.GetBinLowEdge(b) < 138:
                    TTbar = TTbar + hist_tt_var.GetBinContent(b)
                    ErrTTbar = math.sqrt(pow(ErrTTbar,2)+ pow(hist_tt_var.GetBinError(b),2))
            print hist_tt_var.Integral(),TTbar


            Bgr = Zjets + TTbar
            ErrBgr = math.sqrt(pow(ErrZjets,2)+ pow(ErrTTbar,2))

            S_B = Zh/math.sqrt(Bgr) 
            Err_S_B = math.sqrt(pow(ErrZh,2)/Bgr + pow(ErrBgr,2)*pow(Zh,2)/(4*pow(Bgr,3)))

            FOM = Zh/(1.5 + math.sqrt(Bgr) + 0.2*Bgr)
            bfom = 1.5 + math.sqrt(Bgr) + 0.2*Bgr
            Twob = (pow(2*math.sqrt(Bgr),-1) + 0.2)
            Err_FOM = math.sqrt(pow(ErrZh,2)/pow(bfom,2) + pow(Zh,2)*pow(ErrBgr,2)*pow(Twob,2)/pow(bfom,4))
            print Err_FOM


            latex = ROOT.TLatex()
            latex.SetNDC()
            latex.SetTextSize(0.06)
            #latex.DrawLatex(0.14, 0.92, 'L = 5 fb^{-1}')
            latex.DrawLatex(0.10, 0.94, '#color[' + str(4) + ']{' + a + '}')

            latex.SetTextSize(0.04)
            latex.DrawLatex(0.65, 0.92, 'L = 20 fb^{-1}')
            latex.DrawLatex(0.55, 0.84, '#color[' + str(ROOT.kBlack) + ']{N_{ZH} = ' + \
                            '{0:.4f}'.format(Zh) + '+-' + '{0:.4f}'.format(ErrZh) + '}')
            latex.DrawLatex(0.55, 0.78, '#color[' + str(ROOT.kRed) + ']{N_{ZJets} = ' + \
                            '{0:.4f}'.format(Zjets) + '+-' + '{0:.4f}'.format(ErrZjets) + '}')
            latex.DrawLatex(0.55, 0.72, '#color[' + str(ROOT.kBlue) + ']{N_{ttbar} = ' + \
                            '{0:.4f}'.format(TTbar) + '+-' + '{0:.4f}'.format(ErrTTbar) + '}')
            latex.DrawLatex(0.13, 0.84, 'FOM = ' + '{0:.4f}'.format(FOM) + \
                            '+-' + '{0:.4f}'.format(Err_FOM))
            latex.DrawLatex(0.13, 0.78, 'S/#sqrt{B} = ' + '{0:.4f}'.format(S_B) + \
                            '+-' + '{0:.4f}'.format(Err_S_B))

            xl1=.13; yl1=.68 
            xl2=xl1+.15; yl2=yl1+.23
            leg =ROOT.TLegend(xl1,yl1,xl2,yl2);
            leg.SetFillColor(0);
            leg.SetLineColor(0);
            leg.SetShadowColor(0);
            leg.AddEntry(hist_zh_var,"ZH","l");
            leg.AddEntry(hist_dy_var,"DYJets","l");
            leg.AddEntry(hist_tt_var,"TTBar","l");
            leg.SetTextSize(0.045);    
            #leg.Draw();

            canvas.Update()

            canvas.SaveAs('/uscms_data/d3/ingabu/CSA14/CMSSW_7_1_0_pre9/src/VHbb/HbbAnalyzer/macros/Gifs/SB/'+ v + a + '.gif')


if doHmassFat:
    for v in var:
        if not (v == 'HiggsM_') and not (v == 'HiggsM_nocuts_') and not (v == 'HiggsM_bdtcuts_') and not (v == 'HiggsM_300cuts_'): continue
        if v == 'HiggsM_' or v == 'HiggsM_nocuts_' or v == 'HiggsM_bdtcuts_':
                rbn=10; xmin=0.; xmax=260.; title='Higgs Mass (GeV)'
        if v == 'HiggsM_300cuts_':
                rbn=5; xmin=0.; xmax=260.; title='Higgs Mass (GeV)'
        for a in fat:
            for g in groom:
                hist_zh_var = zh.Get('HbbAnalyzer/' + a + '/' + g + '/' + v + a + g)
                hist_dy_var = dy.Get('HbbAnalyzer/' + a + '/' + g + '/' + v + a + g)
                hist_tt_var = tt.Get('HbbAnalyzer/' + a + '/' + g + '/' + v + a + g)

                hist_zh_var.Rebin(rbn)
                hist_zh_var.SetLineColor(ROOT.kBlack)
                hist_zh_var.SetLineWidth(3)
                hist_zh_var.SetStats(0)
                hist_zh_var.Scale(20.0 * 0.0288 / 198566.)
                hist_dy_var.Rebin(rbn)
                hist_dy_var.SetLineColor(ROOT.kRed)
                hist_dy_var.SetLineWidth(3)
                hist_dy_var.SetStats(0)
                hist_dy_var.Scale(20.0 * 4746. / 2603552.)
                hist_tt_var.Rebin(rbn)
                hist_tt_var.SetLineColor(ROOT.kBlue)
                hist_tt_var.SetLineWidth(3)
                hist_tt_var.SetStats(0)
                hist_tt_var.Scale(20.0 * 424.5 / 24893609.)

                canvas = ROOT.TCanvas()
                canvas.SetLogy()
                ymin = 10e-5
                ymax = 500.
                hist_zh_var.GetXaxis().SetRangeUser(xmin, xmax)
                hist_zh_var.GetYaxis().SetRangeUser(ymin, ymax)
                hist_zh_var.GetXaxis().SetTitleSize(0.05)
                hist_zh_var.GetXaxis().SetTitleOffset(0.8)
                hist_zh_var.GetXaxis().SetTitle(title)
                hist_dy_var.GetXaxis().SetRangeUser(xmin, xmax)
                hist_dy_var.GetYaxis().SetRangeUser(ymin, ymax)
                hist_dy_var.GetXaxis().SetTitleSize(0.05)
                hist_dy_var.GetXaxis().SetTitleOffset(0.8)
                hist_dy_var.GetXaxis().SetTitle(title)
                hist_tt_var.GetXaxis().SetRangeUser(xmin, xmax)
                hist_tt_var.GetYaxis().SetRangeUser(ymin, ymax)
                hist_tt_var.GetXaxis().SetTitleSize(0.05)
                hist_tt_var.GetXaxis().SetTitleOffset(0.8)
                hist_tt_var.GetXaxis().SetTitle(title)
                hist_zh_var.Draw()
                hist_dy_var.Draw("same")
                hist_tt_var.Draw("same")

                Zh=0
                Zjets=0
                TTbar=0
                ErrZh=0
                ErrZjets=0
                ErrTTbar=0
                for b in range(hist_zh_var.GetNbinsX()):
                    if hist_zh_var.GetBinLowEdge(b) >= 90 and hist_zh_var.GetBinLowEdge(b) < 138: # integrate from 90 to 140
                        Zh = Zh+ hist_zh_var.GetBinContent(b)
                        ErrZh = math.sqrt(pow(ErrZh,2)+ pow(hist_zh_var.GetBinError(b),2))
                print hist_zh_var.Integral(), Zh, ErrZh

                imin=hist_zh_var.GetXaxis().FindBin(90.1)
                imax=hist_zh_var.GetXaxis().FindBin(139.9)
                print imin,imax
                print hist_zh_var.Integral()
                error= ROOT.Double(0.)
                int= hist_zh_var.IntegralAndError(imin,imax,error)
                print int, error

                for b in range(hist_dy_var.GetNbinsX()):
                    if hist_dy_var.GetBinLowEdge(b) >= 90 and hist_dy_var.GetBinLowEdge(b) < 138:
                        Zjets = Zjets+ hist_dy_var.GetBinContent(b)
                        ErrZjets = math.sqrt(pow(ErrZjets,2)+ pow(hist_dy_var.GetBinError(b),2))
                print hist_dy_var.Integral(),Zjets

                for b in range(hist_tt_var.GetNbinsX()):
                    if hist_tt_var.GetBinLowEdge(b) >= 90 and hist_tt_var.GetBinLowEdge(b) < 138:
                        TTbar = TTbar + hist_tt_var.GetBinContent(b)
                        ErrTTbar = math.sqrt(pow(ErrTTbar,2)+ pow(hist_tt_var.GetBinError(b),2))
                print hist_tt_var.Integral(),TTbar


                Bgr = Zjets + TTbar
                ErrBgr = math.sqrt(pow(ErrZjets,2)+ pow(ErrTTbar,2))

                S_B = Zh/math.sqrt(Bgr) 
                Err_S_B = math.sqrt(pow(ErrZh,2)/Bgr + pow(ErrBgr,2)*pow(Zh,2)/(4*pow(Bgr,3)))

                FOM = Zh/(1.5 + math.sqrt(Bgr) + 0.2*Bgr)
                bfom = 1.5 + math.sqrt(Bgr) + 0.2*Bgr
                Twob = (pow(2*math.sqrt(Bgr),-1) + 0.2)
                Err_FOM = math.sqrt(pow(ErrZh,2)/pow(bfom,2) + pow(Zh,2)*pow(ErrBgr,2)*pow(Twob,2)/pow(bfom,4))
                print Err_FOM


                latex = ROOT.TLatex()
                latex.SetNDC()
                latex.SetTextSize(0.06)
                #latex.DrawLatex(0.14, 0.92, 'L = 5 fb^{-1}')
                latex.DrawLatex(0.10, 0.94, '#color[' + str(4) + ']{' + a + g + '}')

                latex.SetTextSize(0.04)
                latex.DrawLatex(0.65, 0.92, 'L = 20 fb^{-1}')
                latex.DrawLatex(0.55, 0.84, '#color[' + str(ROOT.kBlack) + ']{N_{ZH} = ' + \
                                '{0:.4f}'.format(Zh) + '+-' + '{0:.4f}'.format(ErrZh) + '}')
                latex.DrawLatex(0.55, 0.78, '#color[' + str(ROOT.kRed) + ']{N_{ZJets} = ' + \
                                '{0:.4f}'.format(Zjets) + '+-' + '{0:.4f}'.format(ErrZjets) + '}')
                latex.DrawLatex(0.55, 0.72, '#color[' + str(ROOT.kBlue) + ']{N_{ttbar} = ' + \
                                '{0:.4f}'.format(TTbar) + '+-' + '{0:.4f}'.format(ErrTTbar) + '}')
                latex.DrawLatex(0.13, 0.84, 'FOM = ' + '{0:.4f}'.format(FOM) + \
                                '+-' + '{0:.4f}'.format(Err_FOM))
                latex.DrawLatex(0.13, 0.78, 'S/#sqrt{B} = ' + '{0:.4f}'.format(S_B) + \
                                '+-' + '{0:.4f}'.format(Err_S_B))

                xl1=.13; yl1=.68 
                xl2=xl1+.15; yl2=yl1+.23
                leg =ROOT.TLegend(xl1,yl1,xl2,yl2);
                leg.SetFillColor(0);
                leg.SetLineColor(0);
                leg.SetShadowColor(0);
                leg.AddEntry(hist_zh_var,"ZH","l");
                leg.AddEntry(hist_dy_var,"DYJets","l");
                leg.AddEntry(hist_tt_var,"TTBar","l");
                leg.SetTextSize(0.045);    
                #leg.Draw();

                canvas.Update()

                canvas.SaveAs('/uscms_data/d3/ingabu/CSA14/CMSSW_7_1_0_pre9/src/VHbb/HbbAnalyzer/macros/Gifs/SB/'+ v + a + g + '.gif')

if doHmassAK4Int:
    for v in var:
        #if not (v == 'HiggsM_') and not (v == 'HiggsM_nocuts_'): continue
        if v == 'HiggsM_' or v == 'HiggsM_nocuts_' or v == 'HiggsM_bdtcuts_':
            rbn=10; xmin=0.; xmax=260.; title='Higgs Mass (GeV)'
        if v == 'HiggsPt_' or v == 'HiggsPt_nocuts_' or v == 'HiggsPt_bdtcuts_':
            rbn=2; xmin=0.; xmax=500.; title='Higgs Pt (GeV)'
        if v == 'HiggsEta_' or v == 'HiggsEta_nocuts_':
            rbn=2; xmin=-4.; xmax=4.; title='Higgs Eta'
        if v == 'deltaRbb_' or v == 'deltaRbb_nocuts_' or v == 'deltaRbb_bdtcuts_':
            rbn=5; xmin=0.; xmax=2.; title='DeltaR(bb)'
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
            hist_dy_var = dy.Get('HbbAnalyzer/AK4/' + v + a)
            hist_tt_var = tt.Get('HbbAnalyzer/AK4/' + v + a)

            hist_zh_var.Rebin(rbn)
            hist_zh_var.SetLineColor(ROOT.kBlack)
            hist_zh_var.SetLineWidth(3)
            hist_zh_var.SetStats(0)
            hist_zh_var.Scale(20.0 * 0.0288 / 198566.)
            hist_zh_var.Scale(1/hist_zh_var.Integral())
            hist_dy_var.Rebin(rbn)
            hist_dy_var.SetLineColor(ROOT.kRed)
            hist_dy_var.SetLineWidth(3)
            hist_dy_var.SetStats(0)
            hist_dy_var.Scale(20.0 * 4746. / 2603552.)
            hist_dy_var.Scale(1/hist_dy_var.Integral())
            hist_tt_var.Rebin(rbn)
            hist_tt_var.SetLineColor(ROOT.kBlue)
            hist_tt_var.SetLineWidth(3)
            hist_tt_var.SetStats(0)
            hist_tt_var.Scale(20.0 * 424.5 / 24893609.)
            hist_tt_var.Scale(1/hist_tt_var.Integral())

            canvas = ROOT.TCanvas()
            #canvas.SetLogy()
            ymin = 0.0
            ymax = hist_zh_var.GetMaximum() + .2
            hist_zh_var.GetXaxis().SetRangeUser(xmin, xmax)
            hist_zh_var.GetYaxis().SetRangeUser(ymin, ymax)
            hist_zh_var.GetXaxis().SetTitleSize(0.05)
            hist_zh_var.GetXaxis().SetTitleOffset(0.8)
            hist_zh_var.GetXaxis().SetTitle(title)
            hist_dy_var.GetXaxis().SetRangeUser(xmin, xmax)
            hist_dy_var.GetYaxis().SetRangeUser(ymin, ymax)
            hist_dy_var.GetXaxis().SetTitleSize(0.05)
            hist_dy_var.GetXaxis().SetTitleOffset(0.8)
            hist_dy_var.GetXaxis().SetTitle(title)
            hist_tt_var.GetXaxis().SetRangeUser(xmin, xmax)
            hist_tt_var.GetYaxis().SetRangeUser(ymin, ymax)
            hist_tt_var.GetXaxis().SetTitleSize(0.05)
            hist_tt_var.GetXaxis().SetTitleOffset(0.8)
            hist_tt_var.GetXaxis().SetTitle(title)
            hist_dy_var.Draw()
            hist_zh_var.Draw("same")
            hist_tt_var.Draw("same")

            Zh=0
            Zjets=0
            TTbar=0
            ErrZh=0
            ErrZjets=0
            ErrTTbar=0
            for b in range(hist_zh_var.GetNbinsX()):
                #if hist_zh_var.GetBinLowEdge(b) >= 90 and hist_zh_var.GetBinLowEdge(b) < 138: # integrate from 90 to 140
                Zh = Zh+ hist_zh_var.GetBinContent(b)
                ErrZh = math.sqrt(pow(ErrZh,2)+ pow(hist_zh_var.GetBinError(b),2))
            print hist_zh_var.Integral(), Zh, ErrZh

            imin=hist_zh_var.GetXaxis().FindBin(90.1)
            imax=hist_zh_var.GetXaxis().FindBin(139.9)
            print imin,imax
            print hist_zh_var.Integral()
            error= ROOT.Double(0.)
            int= hist_zh_var.IntegralAndError(imin,imax,error)
            print int, error

            for b in range(hist_dy_var.GetNbinsX()):
                #if hist_dy_var.GetBinLowEdge(b) >= 90 and hist_dy_var.GetBinLowEdge(b) < 138:
                Zjets = Zjets+ hist_dy_var.GetBinContent(b)
                ErrZjets = math.sqrt(pow(ErrZjets,2)+ pow(hist_dy_var.GetBinError(b),2))
            print hist_dy_var.Integral(),Zjets

            for b in range(hist_tt_var.GetNbinsX()):
                #if hist_tt_var.GetBinLowEdge(b) >= 90 and hist_tt_var.GetBinLowEdge(b) < 138:
                TTbar = TTbar + hist_tt_var.GetBinContent(b)
                ErrTTbar = math.sqrt(pow(ErrTTbar,2)+ pow(hist_tt_var.GetBinError(b),2))
            print hist_tt_var.Integral(),TTbar


            Bgr = Zjets + TTbar
            ErrBgr = math.sqrt(pow(ErrZjets,2)+ pow(ErrTTbar,2))

            S_B = Zh/math.sqrt(Bgr) 
            Err_S_B = math.sqrt(pow(ErrZh,2)/Bgr + pow(ErrBgr,2)*pow(Zh,2)/(4*pow(Bgr,3)))

            FOM = Zh/(1.5 + math.sqrt(Bgr) + 0.2*Bgr)
            bfom = 1.5 + math.sqrt(Bgr) + 0.2*Bgr
            Twob = (pow(2*math.sqrt(Bgr),-1) + 0.2)
            Err_FOM = math.sqrt(pow(ErrZh,2)/pow(bfom,2) + pow(Zh,2)*pow(ErrBgr,2)*pow(Twob,2)/pow(bfom,4))
            print Err_FOM


            latex = ROOT.TLatex()
            latex.SetNDC()
            latex.SetTextSize(0.06)
            #latex.DrawLatex(0.14, 0.92, 'L = 5 fb^{-1}')
            latex.DrawLatex(0.10, 0.94, '#color[' + str(4) + ']{' + a + '}')

            latex.SetTextSize(0.04)
            latex.DrawLatex(0.65, 0.92, 'L = 20 fb^{-1}')
            #latex.DrawLatex(0.55, 0.84, '#color[' + str(ROOT.kBlack) + ']{N_{ZH} = ' + \
            #                '{0:.4f}'.format(Zh) + '+-' + '{0:.4f}'.format(ErrZh) + '}')
            #latex.DrawLatex(0.55, 0.78, '#color[' + str(ROOT.kRed) + ']{N_{ZJets} = ' + \
            #                '{0:.4f}'.format(Zjets) + '+-' + '{0:.4f}'.format(ErrZjets) + '}')
            #latex.DrawLatex(0.55, 0.72, '#color[' + str(ROOT.kBlue) + ']{N_{ttbar} = ' + \
            #                '{0:.4f}'.format(TTbar) + '+-' + '{0:.4f}'.format(ErrTTbar) + '}')
            latex.DrawLatex(0.13, 0.84, 'FOM = ' + '{0:.4f}'.format(FOM) + \
                            '+-' + '{0:.4f}'.format(Err_FOM))
            latex.DrawLatex(0.13, 0.78, 'S/#sqrt{B} = ' + '{0:.4f}'.format(S_B) + \
                            '+-' + '{0:.4f}'.format(Err_S_B))

            xl1=.65; yl1=.6
            xl2=xl1+.15; yl2=yl1+.23
            leg =ROOT.TLegend(xl1,yl1,xl2,yl2);
            leg.SetFillColor(0);
            leg.SetLineColor(0);
            leg.SetShadowColor(0);
            leg.AddEntry(hist_zh_var,"ZH","l");
            leg.AddEntry(hist_dy_var,"DYJets","l");
            leg.AddEntry(hist_tt_var,"TTBar","l");
            leg.SetTextSize(0.045);    
            leg.Draw();

            canvas.Update()

            canvas.SaveAs('/uscms_data/d3/ingabu/CSA14/CMSSW_7_1_0_pre9/src/VHbb/HbbAnalyzer/macros/Gifs/SB/'+ v + a + 'Int.gif')


if doHmassFatInt:
    for v in var:
        #if not (v == 'HiggsM_') and not (v == 'HiggsM_nocuts_'): continue
        if v == 'HiggsM_' or v == 'HiggsM_nocuts_' or v == 'HiggsM_bdtcuts_':
            rbn=10; xmin=0.; xmax=260.; title='Higgs Mass (GeV)'
        if v == 'HiggsPt_' or v == 'HiggsPt_nocuts_' or v == 'HiggsPt_bdtcuts_':
            rbn=2; xmin=0.; xmax=500.; title='Higgs Pt (GeV)'
        if v == 'HiggsEta_' or v == 'HiggsEta_nocuts_':
            rbn=2; xmin=-4.; xmax=4.; title='Higgs Eta'
        if v == 'deltaRbb_' or v == 'deltaRbb_nocuts_' or v == 'deltaRbb_bdtcuts_':
            rbn=5; xmin=0.; xmax=2.; title='DeltaR(bb)'
        if v == 'j1Pt_' or v == 'j1Pt_nocuts_' or v == 'j1Pt_bdtcuts_':
            rbn=2; xmin=0.; xmax=500.; title='jet_1 Pt (GeV)'
        if v == 'j2Pt_' or v == 'j2Pt_nocuts_' or v == 'j2Pt_bdtcuts_':
            rbn=2; xmin=0.; xmax=300.; title='jet_2 Pt (GeV)'
        if v == 'j1Eta_' or v == 'j1Eta_nocuts_' or v == 'j1Eta_bdtcuts_':
            rbn=2; xmin=-4.; xmax=4.; title='jet_1 Eta'
        if v == 'j2Eta_' or v == 'j2Eta_nocuts_' or v == 'j2Eta_bdtcuts_':
            rbn=2; xmin=-4.; xmax=4.; title='jet_2 Eta'
        for a in fat:
            for g in groom:
                hist_zh_var = zh.Get('HbbAnalyzer/' + a + '/' + g + '/' + v + a + g)
                hist_dy_var = dy.Get('HbbAnalyzer/' + a + '/' + g + '/' + v + a + g)
                hist_tt_var = tt.Get('HbbAnalyzer/' + a + '/' + g + '/' + v + a + g)

                hist_zh_var.Rebin(rbn)
                hist_zh_var.SetLineColor(ROOT.kBlack)
                hist_zh_var.SetLineWidth(3)
                hist_zh_var.SetStats(0)
                hist_zh_var.Scale(20.0 * 0.0288 / 198566.)
                hist_zh_var.Scale(1/hist_zh_var.Integral())
                hist_dy_var.Rebin(rbn)
                hist_dy_var.SetLineColor(ROOT.kRed)
                hist_dy_var.SetLineWidth(3)
                hist_dy_var.SetStats(0)
                hist_dy_var.Scale(20.0 * 4746. / 2603552.)
                hist_dy_var.Scale(1/hist_dy_var.Integral())
                hist_tt_var.Rebin(rbn)
                hist_tt_var.SetLineColor(ROOT.kBlue)
                hist_tt_var.SetLineWidth(3)
                hist_tt_var.SetStats(0)
                hist_tt_var.Scale(20.0 * 424.5 / 24893609.)
                hist_tt_var.Scale(1/hist_tt_var.Integral())

                canvas = ROOT.TCanvas()
                #canvas.SetLogy()
                ymin = 0.
                ymax = hist_zh_var.GetMaximum() + .2
                hist_zh_var.GetXaxis().SetRangeUser(xmin, xmax)
                hist_zh_var.GetYaxis().SetRangeUser(ymin, ymax)
                hist_zh_var.GetXaxis().SetTitleSize(0.05)
                hist_zh_var.GetXaxis().SetTitleOffset(0.8)
                hist_zh_var.GetXaxis().SetTitle(title)
                hist_dy_var.GetXaxis().SetRangeUser(xmin, xmax)
                hist_dy_var.GetYaxis().SetRangeUser(ymin, ymax)
                hist_dy_var.GetXaxis().SetTitleSize(0.05)
                hist_dy_var.GetXaxis().SetTitleOffset(0.8)
                hist_dy_var.GetXaxis().SetTitle(title)
                hist_tt_var.GetXaxis().SetRangeUser(xmin, xmax)
                hist_tt_var.GetYaxis().SetRangeUser(ymin, ymax)
                hist_tt_var.GetXaxis().SetTitleSize(0.05)
                hist_tt_var.GetXaxis().SetTitleOffset(0.8)
                hist_tt_var.GetXaxis().SetTitle(title)
                hist_zh_var.Draw()
                hist_dy_var.Draw("same")
                hist_tt_var.Draw("same")

                Zh=0
                Zjets=0
                TTbar=0
                ErrZh=0
                ErrZjets=0
                ErrTTbar=0
                for b in range(hist_zh_var.GetNbinsX()):
                    #if hist_zh_var.GetBinLowEdge(b) >= 90 and hist_zh_var.GetBinLowEdge(b) < 138: # integrate from 90 to 140
                    Zh = Zh+ hist_zh_var.GetBinContent(b)
                    ErrZh = math.sqrt(pow(ErrZh,2)+ pow(hist_zh_var.GetBinError(b),2))
                print hist_zh_var.Integral(), Zh, ErrZh

                imin=hist_zh_var.GetXaxis().FindBin(90.1)
                imax=hist_zh_var.GetXaxis().FindBin(139.9)
                print imin,imax
                print hist_zh_var.Integral()
                error= ROOT.Double(0.)
                int= hist_zh_var.IntegralAndError(imin,imax,error)
                print int, error

                for b in range(hist_dy_var.GetNbinsX()):
                    #if hist_dy_var.GetBinLowEdge(b) >= 90 and hist_dy_var.GetBinLowEdge(b) < 138:
                    Zjets = Zjets+ hist_dy_var.GetBinContent(b)
                    ErrZjets = math.sqrt(pow(ErrZjets,2)+ pow(hist_dy_var.GetBinError(b),2))
                print hist_dy_var.Integral(),Zjets

                for b in range(hist_tt_var.GetNbinsX()):
                    #if hist_tt_var.GetBinLowEdge(b) >= 90 and hist_tt_var.GetBinLowEdge(b) < 138:
                    TTbar = TTbar + hist_tt_var.GetBinContent(b)
                    ErrTTbar = math.sqrt(pow(ErrTTbar,2)+ pow(hist_tt_var.GetBinError(b),2))
                print hist_tt_var.Integral(),TTbar


                Bgr = Zjets + TTbar
                ErrBgr = math.sqrt(pow(ErrZjets,2)+ pow(ErrTTbar,2))

                S_B = Zh/math.sqrt(Bgr) 
                Err_S_B = math.sqrt(pow(ErrZh,2)/Bgr + pow(ErrBgr,2)*pow(Zh,2)/(4*pow(Bgr,3)))

                FOM = Zh/(1.5 + math.sqrt(Bgr) + 0.2*Bgr)
                bfom = 1.5 + math.sqrt(Bgr) + 0.2*Bgr
                Twob = (pow(2*math.sqrt(Bgr),-1) + 0.2)
                Err_FOM = math.sqrt(pow(ErrZh,2)/pow(bfom,2) + pow(Zh,2)*pow(ErrBgr,2)*pow(Twob,2)/pow(bfom,4))
                print Err_FOM


                latex = ROOT.TLatex()
                latex.SetNDC()
                latex.SetTextSize(0.06)
                #latex.DrawLatex(0.14, 0.92, 'L = 5 fb^{-1}')
                latex.DrawLatex(0.10, 0.94, '#color[' + str(4) + ']{' + a + g + '}')

                latex.SetTextSize(0.04)
                latex.DrawLatex(0.65, 0.92, 'L = 20 fb^{-1}')
                #latex.DrawLatex(0.55, 0.84, '#color[' + str(ROOT.kBlack) + ']{N_{ZH} = ' + \
                #                '{0:.4f}'.format(Zh) + '+-' + '{0:.4f}'.format(ErrZh) + '}')
                #latex.DrawLatex(0.55, 0.78, '#color[' + str(ROOT.kRed) + ']{N_{ZJets} = ' + \
                #                '{0:.4f}'.format(Zjets) + '+-' + '{0:.4f}'.format(ErrZjets) + '}')
                #latex.DrawLatex(0.55, 0.72, '#color[' + str(ROOT.kBlue) + ']{N_{ttbar} = ' + \
                #                '{0:.4f}'.format(TTbar) + '+-' + '{0:.4f}'.format(ErrTTbar) + '}')
                latex.DrawLatex(0.13, 0.84, 'FOM = ' + '{0:.4f}'.format(FOM) + \
                                '+-' + '{0:.4f}'.format(Err_FOM))
                latex.DrawLatex(0.13, 0.78, 'S/#sqrt{B} = ' + '{0:.4f}'.format(S_B) + \
                                '+-' + '{0:.4f}'.format(Err_S_B))

                xl1=.65; yl1=.6 
                xl2=xl1+.15; yl2=yl1+.23
                leg =ROOT.TLegend(xl1,yl1,xl2,yl2);
                leg.SetFillColor(0);
                leg.SetLineColor(0);
                leg.SetShadowColor(0);
                leg.AddEntry(hist_zh_var,"ZH","l");
                leg.AddEntry(hist_dy_var,"DYJets","l");
                leg.AddEntry(hist_tt_var,"TTBar","l");
                leg.SetTextSize(0.045);    
                leg.Draw();

                canvas.Update()

                canvas.SaveAs('/uscms_data/d3/ingabu/CSA14/CMSSW_7_1_0_pre9/src/VHbb/HbbAnalyzer/macros/Gifs/SB/'+ v + a + g + 'Int.gif')


###### NJettiness ########
if dotaus:
    for a in fat: 
        for c in cuts:
            hist_zh_var1 = zh.Get('HbbAnalyzer/' + a + '/tau2' + c + a)
            hist_zh_var1.Sumw2()
            hist_dy_var1 = dy.Get('HbbAnalyzer/' + a + '/tau2' + c + a)
            hist_dy_var1.Sumw2()
            hist_tt_var1 = tt.Get('HbbAnalyzer/' + a + '/tau2' + c + a)
            hist_tt_var1.Sumw2()

            hist_zh_var2 = zh.Get('HbbAnalyzer/' + a + '/tau3' + c + a)
            hist_zh_var2.Sumw2()
            hist_dy_var2 = dy.Get('HbbAnalyzer/' + a + '/tau3' + c + a)
            hist_dy_var2.Sumw2()
            hist_tt_var2 = tt.Get('HbbAnalyzer/' + a + '/tau3' + c + a)
            hist_tt_var2.Sumw2()

            rbn=2; xmin=0.0; xmax=0.4; title='#tau_{3}/#tau_{2}'

            hist_zh_var1.Rebin(rbn)
            hist_zh_var1.SetLineColor(ROOT.kBlack)
            hist_zh_var1.SetLineWidth(3)
            hist_zh_var1.SetStats(0)
            hist_dy_var1.Rebin(rbn)
            hist_dy_var1.SetLineColor(ROOT.kRed)
            hist_dy_var1.SetLineWidth(3)
            hist_dy_var1.SetStats(0)
            hist_tt_var1.Rebin(rbn)
            hist_tt_var1.SetLineColor(ROOT.kGreen)
            hist_tt_var1.SetLineWidth(3)
            hist_tt_var1.SetStats(0)
            hist_zh_var2.Rebin(rbn)
            hist_zh_var2.SetLineColor(ROOT.kBlack)
            hist_zh_var2.SetLineWidth(3)
            hist_zh_var2.SetStats(0)
            hist_dy_var2.Rebin(rbn)
            hist_dy_var2.SetLineColor(ROOT.kRed)
            hist_dy_var2.SetLineWidth(3)
            hist_dy_var2.SetStats(0)
            hist_tt_var2.Rebin(rbn)
            hist_tt_var2.SetLineColor(ROOT.kGreen)
            hist_tt_var2.SetLineWidth(3)
            hist_tt_var2.SetStats(0)

            hist_zh_var = hist_zh_var1.Clone()
            hist_zh_var.Divide(hist_zh_var2,hist_zh_var1,1.,1.,"b");
            hist_dy_var = hist_dy_var1.Clone()
            hist_dy_var.Divide(hist_dy_var2,hist_dy_var1,1.,1.,"b");
            hist_tt_var = hist_tt_var1.Clone()
            hist_tt_var.Divide(hist_tt_var2,hist_tt_var1,1.,1.,"b");


            canvas = ROOT.TCanvas()
            #canvas.SetLogy()

            zhnbins = hist_zh_var.GetSize() - 2
            dynbins = hist_dy_var.GetSize() - 2
            ttnbins = hist_tt_var.GetSize() - 2

            hist_zh_var.Scale(1/hist_zh_var.Integral(0,zhnbins))
            hist_dy_var.Scale(1/hist_dy_var.Integral(0,dynbins))
            hist_tt_var.Scale(1/hist_tt_var.Integral(0,ttnbins))

            ymin = 0.; ymax = hist_zh_var.GetMaximum()
            if ymax < hist_dy_var.GetMaximum(): ymax = hist_dy_var.GetMaximum()
            if ymax < hist_tt_var.GetMaximum(): ymax = hist_tt_var.GetMaximum()
            ymax = 1.3*ymax

            hist_zh_var.SetMarkerStyle(20)
            hist_zh_var.SetMarkerColor(ROOT.kBlack)
            hist_zh_var.SetFillColor(ROOT.kBlack)
            hist_zh_var.SetFillStyle(3016)
            hist_zh_var.GetXaxis().SetRangeUser(xmin, xmax)
            hist_zh_var.GetYaxis().SetRangeUser(ymin, ymax)
            hist_zh_var.GetXaxis().SetTitleSize(0.05)
            hist_zh_var.GetXaxis().SetTitleOffset(0.8)
            hist_zh_var.GetXaxis().SetTitle(title)
            hist_dy_var.SetMarkerStyle(22)
            hist_dy_var.SetMarkerColor(ROOT.kRed)
            hist_dy_var.SetFillColor(ROOT.kRed)
            hist_dy_var.SetFillStyle(3013)
            hist_dy_var.GetXaxis().SetRangeUser(xmin, xmax)
            hist_dy_var.GetYaxis().SetRangeUser(ymin, ymax)
            hist_dy_var.GetXaxis().SetTitleSize(0.05)
            hist_dy_var.GetXaxis().SetTitleOffset(0.8)
            hist_dy_var.GetXaxis().SetTitle(title)
            hist_tt_var.SetMarkerStyle(21)
            hist_tt_var.SetMarkerColor(ROOT.kGreen)
            hist_tt_var.SetFillColor(ROOT.kGreen)
            hist_tt_var.SetFillStyle(3004)
            hist_tt_var.GetXaxis().SetRangeUser(xmin, xmax)
            hist_tt_var.GetYaxis().SetRangeUser(ymin, ymax)
            hist_tt_var.GetXaxis().SetTitleSize(0.05)
            hist_tt_var.GetXaxis().SetTitleOffset(0.8)
            hist_tt_var.GetXaxis().SetTitle(title)
            hist_zh_var.Draw("HIST")
            hist_dy_var.Draw("same HIST")
            hist_tt_var.Draw("same HIST")


            latex = ROOT.TLatex()
            latex.SetNDC()
            latex.SetTextSize(0.06)
            latex.DrawLatex(0.10, 0.94, '#color[' + str(4) + ']{' + a + '}')


            xl1=.7; yl1=.63 
            xl2=xl1+.15; yl2=yl1+.23
            leg =ROOT.TLegend(xl1,yl1,xl2,yl2);
            leg.SetFillColor(0);
            leg.SetLineColor(0);
            leg.SetShadowColor(0);
            leg.AddEntry(hist_zh_var,"ZH","l");
            leg.AddEntry(hist_dy_var,"DYJets","l");
            leg.AddEntry(hist_tt_var,"TTBar","l");
            leg.SetTextSize(0.045);    
            leg.Draw();

            canvas.Update()

            canvas.SaveAs('/uscms_data/d3/ingabu/CSA14/CMSSW_7_1_0_pre9/src/VHbb/HbbAnalyzer/macros/Gifs/SB/MorePlots/tau3o2'+ c + a + '.gif')

if dosingletau:
    for a in fat: 
        for t in tau:
            hist_zh_var = zh.Get('HbbAnalyzer/' + a + '/' + t + a)
            hist_zh_var.Sumw2()
            hist_dy_var = dy.Get('HbbAnalyzer/' + a + '/' + t + a)
            hist_dy_var.Sumw2()
            hist_tt_var = tt.Get('HbbAnalyzer/' + a + '/' + t + a)
            hist_tt_var.Sumw2()

            rbn=2; xmin=0.0; xmax=0.8;
            if t.find('tau1') > -1: title='#tau_{1}'
            if t.find('tau2') > -1: title='#tau_{2}'
            if t.find('tau3') > -1: title='#tau_{3}'

            hist_zh_var.Rebin(rbn)
            hist_zh_var.SetLineColor(ROOT.kBlack)
            hist_zh_var.SetLineWidth(3)
            hist_zh_var.SetStats(0)
            hist_dy_var.Rebin(rbn)
            hist_dy_var.SetLineColor(ROOT.kRed)
            hist_dy_var.SetLineWidth(3)
            hist_dy_var.SetStats(0)
            hist_tt_var.Rebin(rbn)
            hist_tt_var.SetLineColor(ROOT.kGreen)
            hist_tt_var.SetLineWidth(3)
            hist_tt_var.SetStats(0)

            canvas = ROOT.TCanvas()
            #canvas.SetLogy()

            #hist_zh_var.Scale(1/hist_zh_var.IntegralAndError(imin,imax,error))
            hist_zh_var.Scale(1/hist_zh_var.Integral())
            #hist_dy_var.Scale(1/hist_dy_var.IntegralAndError(imin,imax,error))
            hist_dy_var.Scale(1/hist_dy_var.Integral())
            #hist_tt_var.Scale(1/hist_tt_var.IntegralAndError(imin,imax,error))
            hist_tt_var.Scale(1/hist_tt_var.Integral())

            ymin = 0.; ymax = hist_zh_var.GetMaximum()
            if ymax < hist_dy_var.GetMaximum(): ymax = hist_dy_var.GetMaximum()
            if ymax < hist_tt_var.GetMaximum(): ymax = hist_tt_var.GetMaximum()
            ymax = 1.3*ymax

            hist_zh_var.SetFillColor(ROOT.kBlack)
            hist_zh_var.SetFillStyle(3016)
            hist_zh_var.GetXaxis().SetRangeUser(xmin, xmax)
            hist_zh_var.GetYaxis().SetRangeUser(ymin, ymax)
            hist_zh_var.GetXaxis().SetTitleSize(0.05)
            hist_zh_var.GetXaxis().SetTitleOffset(0.8)
            hist_zh_var.GetXaxis().SetTitle(title)
            hist_dy_var.SetFillColor(ROOT.kRed)
            hist_dy_var.SetFillStyle(3013)
            hist_dy_var.GetXaxis().SetRangeUser(xmin, xmax)
            hist_dy_var.GetYaxis().SetRangeUser(ymin, ymax)
            hist_dy_var.GetXaxis().SetTitleSize(0.05)
            hist_dy_var.GetXaxis().SetTitleOffset(0.8)
            hist_dy_var.GetXaxis().SetTitle(title)
            hist_tt_var.SetFillColor(ROOT.kGreen)
            hist_tt_var.SetFillStyle(3004)
            hist_tt_var.GetXaxis().SetRangeUser(xmin, xmax)
            hist_tt_var.GetYaxis().SetRangeUser(ymin, ymax)
            hist_tt_var.GetXaxis().SetTitleSize(0.05)
            hist_tt_var.GetXaxis().SetTitleOffset(0.8)
            hist_tt_var.GetXaxis().SetTitle(title)
            hist_zh_var.Draw("HIST")
            hist_dy_var.Draw("same HIST")
            hist_tt_var.Draw("same HIST")


            latex = ROOT.TLatex()
            latex.SetNDC()
            latex.SetTextSize(0.06)
            latex.DrawLatex(0.10, 0.94, '#color[' + str(4) + ']{' + a + '}')


            xl1=.7; yl1=.63 
            xl2=xl1+.15; yl2=yl1+.23
            leg =ROOT.TLegend(xl1,yl1,xl2,yl2);
            leg.SetFillColor(0);
            leg.SetLineColor(0);
            leg.SetShadowColor(0);
            leg.AddEntry(hist_zh_var,"ZH","l");
            leg.AddEntry(hist_dy_var,"DYJets","l");
            leg.AddEntry(hist_tt_var,"TTBar","l");
            leg.SetTextSize(0.045);    
            leg.Draw();

            canvas.Update()

            canvas.SaveAs('/uscms_data/d3/ingabu/CSA14/CMSSW_7_1_0_pre9/src/VHbb/HbbAnalyzer/macros/Gifs/SB/MorePlots/' + t + a + '.gif')

#raw_input('...')
