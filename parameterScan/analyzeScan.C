#include <iostream>

#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TGraph.h"
#include "TAxis.h"

void analyzeScan(){

  TFile* fin = TFile::Open("higgsCombine1D_exp_inter.MultiDimFit.mH125.6.123456.root", "READ");

  TTree* limit = (TTree*)fin->Get("limit");
  limit->Draw("2*deltaNLL:CMS_zz4l_fg4");

  TGraph* gr = new TGraph(limit->GetSelectedRows(), limit->GetV2(), limit->GetV1());


  TCanvas* c = new TCanvas("c", "c", 640, 640);
  c->cd();
  gr->Draw("A*");
  gr->GetXaxis()->SetLabelSize(0.05);
  gr->GetYaxis()->SetLabelSize(0.05);
  gr->GetXaxis()->SetTitleSize(0.05);
  gr->GetYaxis()->SetTitleSize(0.05);
  gr->GetYaxis()->SetTitleOffset(1.2);
  gr->GetXaxis()->SetTitle("f_{a3}");
  gr->GetYaxis()->SetTitle("-2 #Delta ln L");
  gr->SetTitle("");
  gPad->SetBottomMargin(0.13);
  gPad->SetLeftMargin(0.15);
  gPad->Modified();
  c->Print("nll_v_fa3.png");
  c->Print("nll_v_fa3.pdf");

  fin->Close();
  
  return;
}
