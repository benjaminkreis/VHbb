#include <iostream>

#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TGraph.h"
#include "TAxis.h"

void analyzeScan(){
  
  //TString outName = "nll_v_fa3";
  //TString fa3 = "CMS_zz4l_fg4";//WHbb 
  //TString xTitle = "f_{a3}^{WH}";
  //float xmax = 1;
  //int ndiv=512;

  //TString outName = "hzz_nll_v_fa3";
  //TString fa3 = "(CMS_zz4l_fg4*0.021)/( (1-CMS_zz4l_fg4)*6.36 + CMS_zz4l_fg4*0.021 )";//H->ZZ
  //TString xTitle = "f_{a3}^{ZZ}";  
  //float xmax = 0.015;//zoom
  //int ndiv = 505;//zoom
  //float xmax = 1.;
  //int ndiv = 512;

  TString outName = "hww_nll_v_fa3";
  TString fa3 = "(CMS_zz4l_fg4*0.021)/( (1-CMS_zz4l_fg4)*3.01 + CMS_zz4l_fg4*0.021 )";//H->WW
  TString xTitle = "f_{a3}^{WW}";  
  float xmax = 0.03;
  int ndiv = 512;


  TFile* fin = TFile::Open("higgsCombine1D_exp_inter.MultiDimFit.mH125.6.123456.root", "READ");

  TTree* limit = (TTree*)fin->Get("limit");
  limit->Draw("2*deltaNLL:"+fa3);

  TGraph* gr = new TGraph(limit->GetSelectedRows(), limit->GetV2(), limit->GetV1());


  TCanvas* c = new TCanvas("c", "c", 640, 640);
  c->cd();
  gr->SetMarkerSize(1);
  gr->SetMarkerStyle(20);
  gr->GetXaxis()->SetRangeUser(0, xmax);
  gr->GetXaxis()->SetNdivisions(ndiv);
  gr->Draw("AP");
  gr->GetXaxis()->SetLabelSize(0.05);
  gr->GetYaxis()->SetLabelSize(0.05);
  gr->GetXaxis()->SetTitleSize(0.05);
  gr->GetYaxis()->SetTitleSize(0.05);
  gr->GetYaxis()->SetTitleOffset(1.2);
  gr->GetXaxis()->SetTitleOffset(1.2);
  gr->GetXaxis()->SetTitle(xTitle);
  gr->GetYaxis()->SetTitle("-2 #Delta ln L");
  gr->SetTitle("");
  gPad->SetBottomMargin(0.14);
  gPad->SetLeftMargin(0.15);
  gPad->Modified();
  c->Print(outName+".png");
  c->Print(outName+".pdf");

  fin->Close();
  
  return;
}
