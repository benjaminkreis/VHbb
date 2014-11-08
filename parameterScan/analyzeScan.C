#include <iostream>

#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TGraph.h"
#include "TAxis.h"

void analyzeScan(){

  TFile* fin = TFile::Open("higgsCombine1D_exp_inter.MultiDimFit.mH125.6.123456.root", "READ");

  TTree* limit = (TTree*)fin->Get("limit");
  limit->Draw("deltaNLL:CMS_zz4l_fg4");
  TGraph* gr = new TGraph(limit->GetSelectedRows(), limit->GetV2(), limit->GetV1());
  gr->Draw("A*");
  gr->GetXaxis()->SetTitle("f_{a3}");
  gr->GetYaxis()->SetTitle("NLL");

  fin->Close();
  
  return;
}
