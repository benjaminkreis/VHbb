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
#include <fstream>

//Root
#include "TString.h"
#include "TFile.h"
#include "TH1F.h"
#include "TROOT.h"
#include "TCanvas.h"
#include "TPRegexp.h"

//RooFit
#include "RooWorkspace.h"
#include "RooDataHist.h"
#include "RooHistFunc.h"
#include "RooHistPdf.h"
#include "RooPlot.h"
#include "RooFormulaVar.h"

//CMS
#include "HZZ4L_RooSpinZeroPdf_1D.h"
#include "ProcessNormalization.h"
//#include "VerticalInterpHistPdf.h"
//#include "VerticalInterpPdf.h"
 
using namespace std;
using namespace RooFit;


//Global :(
bool verbose = true;
bool ignoreInterference = true;
float xsec_0   = 0.40609546E-05;
float xsec_0p5 = 0.81267106E-05;
float xsec_1   = 0.16300162E-03;
float g4 =  0.15784;
float g1 = 1.0;


std::vector<TString> readSystematicsList(){

  std::vector<TString> myList;

  ifstream myifstream;
  myifstream.open("dataCard_0P_allsyst_exceptsigstat.txt", fstream::in);
  assert(myifstream.is_open());

  string fileLine;
  TString syst, type;

  while(!myifstream.eof()){
    getline(myifstream,fileLine);
    TString thisLine(fileLine.c_str());

    TStringToken token(thisLine," ");
    token.NextToken();
    syst = token;
    if(syst == "") continue;
    token.NextToken();
    type = token;
    if(type == "") continue;
    else if(type == "shape") myList.push_back(syst);
    else if(type == "shape1") myList.push_back(syst);
  }
  
  //print
  if(verbose){
    cout << "List of systematics: " << endl;
    for(unsigned int i=0; i<myList.size(); i++){
      cout << myList[i] << endl;
    }
  }
    
  return myList;

}


//Start with 0+, 0-, and 5050 mix all normalized to same cross section.
//Convert to 0+, 0-, and interference, with appropriate scaling for HZZ4L_RooSpinZeroPdf_1D
void convertToTemplates(TH1F* Sig_T_1, TH1F* Sig_T_2, TH1F* Sig_T_4){
    Sig_T_1->Scale(g1*g1*xsec_0);
    Sig_T_2->Scale(g4*g4*xsec_1);
    Sig_T_4->Scale(xsec_0p5);
    Sig_T_4->Add(Sig_T_1, -1);
    Sig_T_4->Add(Sig_T_2, -1);
    if(ignoreInterference) Sig_T_4->Scale(1e-200);
}


//Convert templates into RooHistFuncs and create and return HZZ4L_RooSpinZeroPdf_1D
HZZ4L_RooSpinZeroPdf_1D createSignalPdf(TString name, RooRealVar* x, RooRealVar* D1, TH1F* Sig_T_1, TH1F* Sig_T_2, TH1F* Sig_T_4){
  
    //RooDataHist
    RooDataHist* Sig_T_1_hist =  new RooDataHist("T_1_hist_"+name, "", RooArgList(*D1), Sig_T_1);
    RooDataHist* Sig_T_2_hist =  new RooDataHist("T_2_hist_"+name, "", RooArgList(*D1), Sig_T_2);
    RooDataHist* Sig_T_4_hist =  new RooDataHist("T_4_hist_"+name, "", RooArgList(*D1), Sig_T_4);

    //RooHistFunc
    RooHistFunc* Sig_T_1_histfunc =  new RooHistFunc("T_1_histfunc_"+name, "", RooArgSet(*D1), *Sig_T_1_hist);
    RooHistFunc* Sig_T_2_histfunc =  new RooHistFunc("T_2_histfunc_"+name, "", RooArgSet(*D1), *Sig_T_2_hist);
    RooHistFunc* Sig_T_4_histfunc =  new RooHistFunc("T_4_histfunc_"+name, "", RooArgSet(*D1), *Sig_T_4_hist);

    //RooSpinZeroPdf_1D
    HZZ4L_RooSpinZeroPdf_1D ggHpdf(name, name, *D1, *x, RooArgList(*Sig_T_1_histfunc, *Sig_T_2_histfunc, *Sig_T_4_histfunc)); 
    //ws.import(ggHpdf, RecycleConflictNodes());
    return ggHpdf;
}


void workspaceBuilder(){

  //Create workspace
  RooWorkspace ws("w");
  ws.autoImportClassCode(true);

  const int numChannels = 4;
  TString basename = "mainBDT_v_VstarMass_bdt";
  TString channels[numChannels] = {"Vtype2_medBoost", "Vtype3_medBoost", "Vtype2_highBoost", "Vtype3_highBoost"};
  //TString channels[numChannels] = {"Vtype2_medBoost"};
  TFile * inputHistogramsFile = TFile::Open("plots.root");
  
  std::vector<TString> systematicsList = readSystematicsList();

  //fa3
  RooRealVar x("CMS_zz4l_fg4", "CMS_zz4l_fg4", 0, 0, 1);
  x.setBins(1000);

  for(int c=0; c<numChannels; c++){

    TString loopName = basename + "_" + channels[c];

    /////////////////////////OA
    // Signal
    /////////////////////////

    //Create nominal T1 T2 and T4 histograms
    TH1F* Sig_T_1 = (TH1F*)inputHistogramsFile->Get(loopName + "__Wh_125p6_0P");
    TH1F* Sig_T_2 = (TH1F*)inputHistogramsFile->Get(loopName + "__Wh_125p6_0M");
    TH1F* Sig_T_4 = (TH1F*)inputHistogramsFile->Get(loopName + "__Wh_125p6_0Mf05ph0");
    convertToTemplates(Sig_T_1, Sig_T_2, Sig_T_4);

    //Observable RooRealVar
    double dLowX  = Sig_T_1->GetXaxis()->GetXmin();
    double dHighX = Sig_T_1->GetXaxis()->GetXmax();
    int dBinsX    = Sig_T_1->GetXaxis()->GetNbins();
    RooRealVar* D1 =  new RooRealVar("D1_"+loopName, "D1_"+loopName, dLowX, dHighX); 
    D1->setBins(dBinsX);
    
    //Normalization for combine
    ProcessNormalization* T1_const =  new ProcessNormalization("T1_processNormalization_"+loopName, "T1_processNormalization_"+loopName, Sig_T_1->Integral());
    ProcessNormalization* T2_const =  new ProcessNormalization("T2_processNormalization_"+loopName, "T2_processNormalization_"+loopName, Sig_T_2->Integral());
    ProcessNormalization* T4_const =  new ProcessNormalization("T4_processNormalization_"+loopName, "T4_processNormalization_"+loopName, Sig_T_4->Integral());
    RooFormulaVar ggH_norm(loopName+"__signal_fai"+"_norm","((1-abs(@0))*@1 + abs(@0)*@2 + (@0>0 ? 1.:-1.)*sqrt(abs(@0)*(1-abs(@0)))*(@3))/@1 >0 ? ((1-abs(@0))*@1 + abs(@0)*@2 + (@0>0 ? 1.:-1.)*sqrt(abs(@0)*(1-abs(@0)))*(@3))/@1 : 1.e-20", RooArgList(x, *T1_const, *T2_const, *T4_const));
    ws.import(ggH_norm,RecycleConflictNodes());
    
    //Nominal signal pdf
    HZZ4L_RooSpinZeroPdf_1D ggHpdf = createSignalPdf(loopName+"__signal_fai", &x, D1, Sig_T_1, Sig_T_2, Sig_T_4);
    ws.import(ggHpdf, RecycleConflictNodes());  

    for(unsigned int s=0; s<systematicsList.size(); s++){
      cout << "**BEN** try signal systematic " << systematicsList[s] << endl;
      TH1F* Sig_T_1_up = (TH1F*)inputHistogramsFile->Get(loopName+"__Wh_125p6_0P_"+systematicsList[s]+"Up");
      TH1F* Sig_T_2_up = (TH1F*)inputHistogramsFile->Get(loopName+"__Wh_125p6_0M_"+systematicsList[s]+"Up");
      TH1F* Sig_T_4_up = (TH1F*)inputHistogramsFile->Get(loopName+"__Wh_125p6_0Mf05ph0_"+systematicsList[s]+"Up");

      TH1F* Sig_T_1_down = (TH1F*)inputHistogramsFile->Get(loopName+"__Wh_125p6_0P_"+systematicsList[s]+"Down");
      TH1F* Sig_T_2_down = (TH1F*)inputHistogramsFile->Get(loopName+"__Wh_125p6_0M_"+systematicsList[c]+"Down");
      TH1F* Sig_T_4_down = (TH1F*)inputHistogramsFile->Get(loopName+"__Wh_125p6_0Mf05ph0_"+systematicsList[s]+"Down");

      if( (Sig_T_1_up == NULL)   || (Sig_T_2_up == NULL)   || (Sig_T_4_up == NULL) )   continue;
      if( (Sig_T_1_down == NULL) || (Sig_T_2_down == NULL) || (Sig_T_4_down == NULL) ) continue;
      cout << "**BEN** found signal systematic " << systematicsList[s] << endl;
      convertToTemplates(Sig_T_1_up,   Sig_T_2_up,   Sig_T_4_up);
      convertToTemplates(Sig_T_1_down, Sig_T_2_down, Sig_T_4_down);

      HZZ4L_RooSpinZeroPdf_1D ggHpdf_up   = createSignalPdf(loopName+"__signal_fai_"+systematicsList[s]+"Up",   &x, D1, Sig_T_1_up,   Sig_T_2_up,   Sig_T_4_up  );
      HZZ4L_RooSpinZeroPdf_1D ggHpdf_down = createSignalPdf(loopName+"__signal_fai_"+systematicsList[s]+"Down", &x, D1, Sig_T_1_down, Sig_T_2_down, Sig_T_4_down);

      ws.import(ggHpdf_up,   RecycleConflictNodes());
      ws.import(ggHpdf_down, RecycleConflictNodes());
    }


    /////////////////////////
    // Backgrounds
    /////////////////////////

    std::vector<TString> backgroundNames;
    backgroundNames.push_back("W_light");
    backgroundNames.push_back("W_b");
    backgroundNames.push_back("W_bb");
    backgroundNames.push_back("ZJets");
    backgroundNames.push_back("ttbar");
    backgroundNames.push_back("singleTop");
    backgroundNames.push_back("VZ");
    backgroundNames.push_back("VV");

    for(unsigned int b=0; b<backgroundNames.size(); b++){

      //Nominal
      //TH1F* hBackground = (TH1F*)inputHistogramsFile->Get(basename + "_" +  channels[c] + "__"+backgroundNames[b]);
      TH1F* hBackground = (TH1F*)inputHistogramsFile->Get(loopName + "__"+backgroundNames[b]);
      RooDataHist* Background_hist =  new RooDataHist(backgroundNames[b]+"_hist_"+loopName, "", RooArgList(*D1), hBackground);
      RooHistPdf Background_histpdf(loopName+"__"+backgroundNames[b]+"_fai", "", RooArgList(*D1), *Background_hist);
      ws.import(Background_histpdf, RecycleConflictNodes());

      //Systematics
      for(unsigned int s=0; s<systematicsList.size(); s++){
	TString systRetrieveBaseName = loopName+"__"+backgroundNames[b]+"_"+systematicsList[s];
	TString systNewBaseName = loopName+"__"+backgroundNames[b]+"_fai_"+systematicsList[s];
	TH1F* hup = (TH1F*)inputHistogramsFile->Get(systRetrieveBaseName+"Up");
	if(hup != NULL){
	  RooDataHist* rdh_up = new RooDataHist("RooDataHist_"+systNewBaseName+"Up", "", RooArgList(*D1), hup);
	  RooHistPdf rhp_up(systNewBaseName+"Up", "", RooArgList(*D1), *rdh_up);//This name is not flexible
	  ws.import(rhp_up, RecycleConflictNodes());

	  TH1F* hdown = (TH1F*)inputHistogramsFile->Get(systRetrieveBaseName+"Down");
	  assert(hdown != NULL);
	  RooDataHist* rdh_down = new RooDataHist("RooDataHist_"+systNewBaseName+"Down", "", RooArgList(*D1), hdown);
	  RooHistPdf rhp_down(systNewBaseName+"Down", "", RooArgList(*D1), *rdh_down);//This name is not flexible
	  ws.import(rhp_down, RecycleConflictNodes());
	}

      }

    }
    //TH1F* hTotalBackground = (TH1F*)inputHistogramsFile->Get(basename + "_" +  channels[c] + "__totalBackground");
    //RooDataHist* TotalBackground_hist =  new RooDataHist("TotalBackground_hist_"+loopName, "", RooArgList(*D1), hTotalBackground);
    //RooHistPdf TotalBackground_histpdf(loopName+"__totalBackground_fai", "", RooArgList(*D1), *TotalBackground_hist);
    //ws.import(TotalBackground_histpdf, RecycleConflictNodes());


    
    ///////////////////////
    // Data
    ///////////////////////

    TH1F* hData =  (TH1F*)inputHistogramsFile->Get(basename + "_"+ channels[c] + "__Data");
    RooDataHist Data_hist(loopName+"__Data_fai", "", RooArgList(*D1), hData);
    ws.import(Data_hist);//RecycleConflictNodes not allowed here for some reason  


    ////////////////////
    // Plot
    ///////////////////
    
    /*
    TCanvas myCanvas("myCanvas", "myCanvas", 640, 480);
    myCanvas.cd();
    RooPlot* plot =  ws.var("D1_mainBDT_v_VstarMass_bdt_Vtype2_medBoost")->frame();
    ws.pdf("mainBDT_v_VstarMass_bdt_Vtype2_medBoost__signal_fai")->plotOn(plot);
    plot->Draw();
    myCanvas.Print("c.png");
    */

    //cout << loopName << " total background = " << hTotalBackground->Integral() << endl;
    //cout << loopName << " signal = " << h0->Integral() << endl;
    
  }
  inputHistogramsFile->Close();
   
  ws.Print();
  ws.writeToFile("myWorkspace.root", true);
  
  return;
}
