/*

     To run, in root do
       gSystem->AddIncludePath("-I$ROOFITSYS/include")
       gSystem->AddIncludePath("-I$CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/interface/")
       gSystem->Load("$CMSSW_BASE/lib/slc5_amd64_gcc472/libHiggsAnalysisCombinedLimit.so")
       .L workspaceBuilder.C++
       workspaceBuilder()

*/

//C++
#include <iostream>

//Root
#include "TString.h"
#include "TFile.h"
#include "TH1F.h"
#include "TROOT.h"

//RooFit
#include "RooWorkspace.h"
#include "RooDataHist.h"
#include "RooHistFunc.h"
#include "RooHistPdf.h"
#include "RooPlot.h"

//CMS
#include "HZZ4L_RooSpinZeroPdf_1D.h"

using namespace std;
using namespace RooFit;


void workspaceBuilder(){

  //Create workspace
  RooWorkspace ws("w");
  ws.autoImportClassCode(true);

  const int numChannels = 4;
  TString basename = "mainBDT_v_VstarMass_bdt";
  TString channels[numChannels] = {"Vtype2_medBoost", "Vtype3_medBoost", "Vtype2_highBoost", "Vtype3_highBoost"};
  //TString channels[numChannels] = {"Vtype2_medBoost"};
  TFile * inputHistogramsFile = TFile::Open("plots.root");
  
  //fa3
  RooRealVar x("CMS_zz4l_fg4", "CMS_zz4l_fg4", -1, 1);//really -1 to 1?
  x.setBins(1000);

  float xsec_0   = 0.40609546E-05;
  float xsec_0p5 = 0.81267106E-05;
  float xsec_1   = 0.16300162E-03;
  float g4 =  0.15784;
  float g1 = 1.0;

  std::vector<TH1F*> h0, h0p5, h1, hTotalBackground, hData;
  std::vector<TH1F*> Sig_T_1, Sig_T_2, Sig_T_4;
  std::vector<RooRealVar*> D1;
  std::vector<RooDataHist*> Sig_T_1_hist, Sig_T_2_hist, Sig_T_4_hist, TotalBackground_hist;
  std::vector<RooHistFunc*> Sig_T_1_histfunc, Sig_T_2_histfunc, Sig_T_4_histfunc;

  for(int c=0; c<numChannels; c++){

    TString loopName = basename + "_" + channels[c];

    /////////////////////////
    // Signal
    /////////////////////////
    
    //Get histograms from input file
    h0.push_back(   (TH1F*)inputHistogramsFile->Get(basename + "_" + channels[c] + "__Wh_125p6_0P") );
    h0p5.push_back( (TH1F*)inputHistogramsFile->Get(basename + "_" + channels[c] + "__Wh_125p6_0Mf05ph0") );
    h1.push_back(   (TH1F*)inputHistogramsFile->Get(basename + "_" + channels[c] + "__Wh_125p6_0M") );
    
    //Create T1 T2 and T4 histograms
    Sig_T_1.push_back( h0[c] );
    Sig_T_2.push_back( h1[c] );
    Sig_T_4.push_back( h0p5[c] );//c1*T(fa3=0.5)- c2*T(fa3=0)-c3*T(fa3=1), where the c are the xsecs
    Sig_T_1[c]->Scale(g1*g1*xsec_0);
    Sig_T_2[c]->Scale(g4*g4*xsec_1);
    Sig_T_4[c]->Scale(xsec_0p5);
    Sig_T_4[c]->Add(Sig_T_1[c], -1);
    Sig_T_4[c]->Add(Sig_T_2[c], -1);
    
    //RooRealVar
    double dLowX  = Sig_T_1[c]->GetXaxis()->GetXmin();
    double dHighX = Sig_T_1[c]->GetXaxis()->GetXmax();
    int dBinsX    = Sig_T_1[c]->GetXaxis()->GetNbins();
    D1.push_back( new RooRealVar("D1_"+loopName, "D1_"+loopName, dLowX, dHighX) ); 
    D1[c]->setBins(dBinsX);

    //RooDataHist
    Sig_T_1_hist.push_back( new RooDataHist("T_1_hist_"+loopName, "", RooArgList(*D1[c]), Sig_T_1[c]) );
    Sig_T_2_hist.push_back( new RooDataHist("T_2_hist_"+loopName, "", RooArgList(*D1[c]), Sig_T_2[c]) );
    Sig_T_4_hist.push_back( new RooDataHist("T_4_hist_"+loopName, "", RooArgList(*D1[c]), Sig_T_4[c]) );

    //RooHistFunc
    Sig_T_1_histfunc.push_back( new RooHistFunc("T_1_histfunc_"+loopName, "", RooArgSet(*D1[c]), *Sig_T_1_hist[c]) );
    Sig_T_2_histfunc.push_back( new RooHistFunc("T_2_histfunc_"+loopName, "", RooArgSet(*D1[c]), *Sig_T_2_hist[c]) );
    Sig_T_4_histfunc.push_back( new RooHistFunc("T_4_histfunc_"+loopName, "", RooArgSet(*D1[c]), *Sig_T_4_hist[c]) );

    //RooSpinZeroPdf_1D
    HZZ4L_RooSpinZeroPdf_1D ggHpdf(loopName+"__signal_fai", loopName+"__signal_fai", *D1[c], x, RooArgList(*Sig_T_1_histfunc[c], *Sig_T_2_histfunc[c], *Sig_T_4_histfunc[c])); 
    ws.import(ggHpdf, RecycleConflictNodes());
 

    /////////////////////////
    // Backgrounds
    /////////////////////////

    hTotalBackground.push_back( (TH1F*)inputHistogramsFile->Get(basename + "_" + channels[c] + "__totalBackground") );
    TotalBackground_hist.push_back( new RooDataHist("TotalBackground_hist_"+loopName, "", RooArgList(*D1[c]), hTotalBackground[c]) );
    RooHistPdf TotalBackground_histpdf(loopName+"__totalBackground_fai", "", RooArgList(*D1[c]), *TotalBackground_hist[c]);
    ws.import(TotalBackground_histpdf, RecycleConflictNodes());


    ///////////////////////
    // Data
    ///////////////////////

    hData.push_back( (TH1F*)inputHistogramsFile->Get(basename + "_" + channels[c] + "__Data") );
    RooDataHist Data_hist(loopName+"__Data_fai", "", RooArgList(*D1[c]), hData[c]);
    ws.import(Data_hist);//RecycleConflictNodes not allowed here for some reason  


    ////////////////////
    // Plot
    ///////////////////

    //RooPlot* plot =  ws.var("D1_mainBDT_v_VstarMass_bdt_Vtype2_medBoost")->frame()
    //ws.pdf("mainBDT_v_VstarMass_bdt_Vtype2_medBoost__totalBackground_fai")->plotOn(plot)
    //plot->Draw()


    cout << loopName << " total background = " << hTotalBackground[c]->Integral() << endl;
    cout << loopName << " signal = " << h0[c]->Integral() << endl;

  }
  inputHistogramsFile->Close();
   
  ws.Print();
  ws.writeToFile("myWorkspace.root", true);
  
  
  return;
}
