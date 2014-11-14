#include <iostream>

#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TGraph.h"
#include "TAxis.h"
#include "TMultiGraph.h"
#include "TLegend.h"

void analyzeScan_WW(){
  
  //TString outName = "nll_v_fa3";
  //TString fa3 = "CMS_zz4l_fg4";//WHbb 
  //TString xTitle = "f_{a3}^{WH}";
  //float xmax = 1;
  //int ndiv=512;

  //TString outName = "zz_nll_v_fa3_zoom";
  //TString fa3 = "(CMS_zz4l_fg4*0.0249)/( (1-CMS_zz4l_fg4)*6.36 + CMS_zz4l_fg4*0.0249 )";//H->ZZ
  //TString xTitle = "f_{a3}^{ZZ}";  
  //float xmax = 0.015;//zoom
  //int ndiv = 505;//zoom
  //float xmax = 1.;
  //int ndiv = 512;

  TString outName = "hww_nll_v_fa3";
  TString fa3 = "(CMS_zz4l_fg4*0.0249)/( (1-CMS_zz4l_fg4)*3.01 + CMS_zz4l_fg4*0.0249 )";//H->WW
  TString xTitle = "f_{a3}^{WW}";  
  float xmax = 1;
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
  

  //Now get H->WW
  TFile* fin2 = TFile::Open("HtoWW_higgsCombine1D_exp_inter_8TeV_old.MultiDimFit.mH125.6.123456.root", "read");
  
  TTree* limit2 = (TTree*)fin2->Get("limit");
  limit2->Draw("2*deltaNLL:CMS_zz4l_fg4");

  TGraph* gr2 = new TGraph(limit2->GetSelectedRows(), limit2->GetV2(), limit2->GetV1());
  gr2->SetMarkerSize(1);
  gr2->SetMarkerStyle(20);
  gr2->SetMarkerColor(kBlue);

  TMultiGraph *mg = new TMultiGraph();
  mg->Add(gr,"p");
  mg->Add(gr2,"p");

  TLegend* leg = new TLegend(0.45, 0.65, .85, .8);
  leg->AddEntry(gr, "WH (expected)", "P");
  leg->AddEntry(gr2, "H #rightarrow WW (expected)", "P");
  leg->SetLineColor(0);
  leg->SetFillColor(0);
  

  TCanvas* c2 = new TCanvas("c2", "c2", 640, 640);
  c2->cd();
  mg->Draw("a");
  leg->Draw();
  mg->GetXaxis()->SetRangeUser(0, xmax);
  mg->GetXaxis()->SetLabelSize(0.05);
  mg->GetYaxis()->SetLabelSize(0.05);
  mg->GetXaxis()->SetTitleSize(0.05);
  mg->GetYaxis()->SetTitleSize(0.05);
  mg->GetYaxis()->SetTitleOffset(1.2);
  mg->GetXaxis()->SetTitleOffset(1.2);
  mg->GetXaxis()->SetTitle(xTitle);
  mg->GetYaxis()->SetTitle("-2 #Delta ln L");
  gPad->SetBottomMargin(0.14);
  gPad->SetLeftMargin(0.15);
  gPad->Modified();
  c2->Print(outName+"_HtoWW.png");
  c2->Print(outName+"_HtoWW.pdf");  


  fin2->Close();
  fin->Close();
  
  return;
}
