#include <iostream>

#include "TFile.h"
#include "TH1F.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TGraph.h"
#include "TAxis.h"
#include "TMultiGraph.h"
#include "TLegend.h"
#include "TLatex.h"

//LINEAR INTERPOLATION
void findCrossing(double y_value, int n_points, double* x, double* y){

  std::vector<double> x_values;
  
  double last_x = -1;//to check sorting 
  double last_y = -1;
  for(int i=0; i<n_points-1; i++){//IGNORE LAST POINT
    cout << "i " << i << ", x " << x[i] << ", y " << y[i] << endl;
    
    assert(x[i] > last_x);//to check sorting

    //right on it
    if(y_value == y[i]){    
      x_values.push_back(x[i]);
    }
    //crossing from below
    else if(y_value > last_y && y_value < y[i]){
      double slope = (y[i] - last_y)/(x[i] - last_x);
      double x_value = last_x + (y_value - last_y)/slope;
      x_values.push_back(x_value);
    }
    //crossing from above
    else if(y_value > y[i] && y_value < last_y){
      double slope = (y[i] - last_y)/(x[i] - last_x);//SAME CODE... i forgot geometry
      double x_value = last_x + (y_value - last_y)/slope;
      x_values.push_back(x_value);
    }

    //for the next iteration
    last_x = x[i];
    last_y = y[i];
  }

  for(int i=0; i<x_values.size(); i++) cout << "crossing y = " << y_value << " at x = " << x_values[i] << endl;
  if(x_values.size() == 0) cout << "No crossings at  y = " << y_value << " found." << endl;

}


//All scans will be in fa3zz.  Convert to ww, wh, and zh.
// f_old R_old / [(1-f_old)R_new + f_old R_old], where R = sigma1/sigma3
// 7 TeV: Rzz=6.36, Rww=3.01, Rzh=0.0249, Rwh=0.0181
// 8 TeV: Rzz=6.36, Rww=3.01, Rzh=0.023868, Rwh=0.017382
TString fa3zzTozz = "CMS_zz4l_fg4";
TString fa3zzToww = "CMS_zz4l_fg4*6.36/( (1-CMS_zz4l_fg4)*3.01   + CMS_zz4l_fg4*6.36)";
TString fa3zzTowh = "CMS_zz4l_fg4*6.36/( (1-CMS_zz4l_fg4)*0.017382 + CMS_zz4l_fg4*6.36)";
TString fa3zzTozh = "CMS_zz4l_fg4*6.36/( (1-CMS_zz4l_fg4)*0.023868 + CMS_zz4l_fg4*6.36)";

//Input files, all in terms of ZZ
TString fin_WH   = "/uscms_data/d1/jstupak/fa3Combo/CMSSW_6_1_1/src/vhvv_combination/realDeal/templates_012715_bugfix/Wh/higgsCombine1D_exp_sys.MultiDimFit.mH125.6.root";
TString fin_ZH   = "/uscms_data/d1/jstupak/fa3Combo/CMSSW_6_1_1/src/vhvv_combination/realDeal/templates_012715_bugfix/Zh/higgsCombine1D_exp_sys.MultiDimFit.mH125.6.root";
TString fin_VH   = "/uscms_data/d1/jstupak/fa3Combo/CMSSW_6_1_1/src/vhvv_combination/realDeal/templates_012715_bugfix/Vh/higgsCombine1D_exp_sys.MultiDimFit.mH125.6.root";
TString fin_WW   = "/uscms_data/d1/jstupak/fa3Combo/CMSSW_6_1_1/src/vhvv_combination/hVVCards/WW/higgsCombine1D_exp_sys.MultiDimFit.mH125.6.root";
TString fin_WWWH_float = "/uscms/home/kreis/Hbb/combine/Meng/CMSSW_6_1_1/src/20150127_fa3/CMSstyle/WWWh/higgsCombine1D_exp_sys.MultiDimFit.mH125.6.root";
TString fin_WWWH = "/uscms_data/d1/jstupak/fa3Combo/CMSSW_6_1_1/src/vhvv_combination/realDeal/templates_012715_bugfix/WWWh/higgsCombine1D_exp_sys.MultiDimFit.mH125.6.root";
TString fin_ZZ   = "/uscms_data/d1/jstupak/fa3Combo/CMSSW_6_1_1/src/vhvv_combination/hVVCards/ZZ/higgsCombine1D_exp_sys.MultiDimFit.mH125.6.root";
TString fin_ZZZH_float = "/uscms/home/kreis/Hbb/combine/Meng/CMSSW_6_1_1/src/20150127_fa3/CMSstyle/ZZZh/higgsCombine1D_exp_sys.MultiDimFit.mH125.6.root";
TString fin_ZZZH = "/uscms_data/d1/jstupak/fa3Combo/CMSSW_6_1_1/src/vhvv_combination/realDeal/templates_012715_bugfix/ZZZh/higgsCombine1D_exp_sys.MultiDimFit.mH125.6.root";
TString fin_VV   = "/uscms_data/d1/jstupak/fa3Combo/CMSSW_6_1_1/src/vhvv_combination/hVVCards/VV/higgsCombine1D_exp_sys.MultiDimFit.mH125.6.root";
TString fin_VVVH_float = "/uscms/home/kreis/Hbb/combine/Meng/CMSSW_6_1_1/src/20150127_fa3/CMSstyle/VVVh/higgsCombine1D_exp_sys.MultiDimFit.mH125.6.root";
TString fin_VVVH = "/uscms_data/d1/jstupak/fa3Combo/CMSSW_6_1_1/src/vhvv_combination/realDeal/templates_012715_bugfix/VVVh/higgsCombine1D_exp_sys.MultiDimFit.mH125.6.root";

TString fin_WH_tev   = "/uscms/home/kreis/Hbb/combine/Meng/CMSSW_6_1_1/src/20150127_fa3/TEVstyle/Wh/higgsCombine1D_exp_sys.MultiDimFit.mH125.6.root";
TString fin_ZH_tev   = "/uscms/home/kreis/Hbb/combine/Meng/CMSSW_6_1_1/src/20150127_fa3/TEVstyle/Zh/higgsCombine1D_exp_sys.MultiDimFit.mH125.6.root";
TString fin_VH_tev   = "/uscms/home/kreis/Hbb/combine/Meng/CMSSW_6_1_1/src/20150127_fa3/TEVstyle/Vh/higgsCombine1D_exp_sys.MultiDimFit.mH125.6.root";

//TString fin_WWus = "/uscms_data/d1/jstupak/fa3Combo/CMSSW_6_1_1/src/vhvv_combination/hVVCards/WW/higgsCombine1D_exp_sys.MultiDimFit.mH125.6.root";
//TString fin_ZZus = "/uscms_data/d1/jstupak/fa3Combo/CMSSW_6_1_1/src/vhvv_combination/hVVCards/ZZ/higgsCombine1D_exp_sys.MultiDimFit.mH125.6.root";

void makeOnePlot(TString f1 = "", TString axis1 = "", TString leg1 = "",
		 TString f2 = "", TString axis2 = "", TString leg2 = "",
		 TString f3 = "", TString axis3 = "", TString leg3 = "",
		 TString f4 = "", TString axis4 = "", TString leg4 = "",
		 double myMin = 0, double myMax = 5, double legy = 0.5,
		 TString f4_scale = "1",
		 TString cut1 = "", TString cut2 = "", TString cut3 = "", TString cut4 = "",
		 TString xTitle = "f_{a3}", TString outName = "fa3", bool zoom=true){
  
  float xmax = 1;
  int ndiv = 512;
  if(zoom){
    outName+="_zoom";
    xmax = 0.015;
    ndiv = 505;
  }
  
  //1
  TFile* fin1 = TFile::Open(f1, "READ");
  if(fin1->IsZombie()) {cout << "no file!" << endl; return;}
  TTree* limit1 = (TTree*)fin1->Get("limit");
  //limit1->Draw("2*deltaNLL:"+axis1);
  TString ystring1 = "2*deltaNLL - 2*";
  ystring1 += limit1->GetMinimum("deltaNLL");//offset due to rough initial scan
  limit1->Draw(ystring1+":"+axis1, "deltaNLL!=0 && " + fa3zzTozz+">=0 &&" +cut1); //remove first point from initial scan and only look at fa3>0
  TGraph* gr1 = new TGraph(limit1->GetSelectedRows(), limit1->GetV2(), limit1->GetV1());
  gr1->SetMarkerSize(1);
  gr1->SetMarkerStyle(20);
  gr1->SetMarkerColor(kBlack);
  gr1->SetLineColor(kBlack);
  gr1->SetLineWidth(2);
  cout << f1 << " (black)" << endl;
  findCrossing(1, limit1->GetSelectedRows(), limit1->GetV2(), limit1->GetV1());
  findCrossing(3.84, limit1->GetSelectedRows(), limit1->GetV2(), limit1->GetV1());


  //2
  TFile* fin2 = TFile::Open(f2, "READ");
  if(fin2->IsZombie()) {cout << "no file!" << endl; return;}
  TTree* limit2 = (TTree*)fin2->Get("limit");
  //limit2->Draw("2*deltaNLL:"+axis2); 
  TString ystring2 = "2*deltaNLL - 2*";
  ystring2 += limit2->GetMinimum("deltaNLL");
  limit2->Draw(ystring2+":"+axis2, "deltaNLL!=0 && " + fa3zzTozz+">=0 &&" +cut2); 
  TGraph* gr2 = new TGraph(limit2->GetSelectedRows(), limit2->GetV2(), limit2->GetV1());
  gr2->SetMarkerSize(1);
  gr2->SetMarkerStyle(22);
  gr2->SetMarkerColor(kBlue);
  gr2->SetLineColor(kBlue);
  gr2->SetLineWidth(2);
  cout << f2 << " (blue)" << endl;
  findCrossing(1, limit2->GetSelectedRows(), limit2->GetV2(), limit2->GetV1());
  findCrossing(3.84, limit2->GetSelectedRows(), limit2->GetV2(), limit2->GetV1());

  //3
  TFile* fin3 = TFile::Open(f3, "READ");
  if(fin3->IsZombie()) {cout << "no file!" << endl; return;}
  TTree* limit3 = (TTree*)fin3->Get("limit");
  //limit3->Draw("2*deltaNLL:"+axis3);
  TString ystring3 = "2*deltaNLL - 2*";
  ystring3 += limit3->GetMinimum("deltaNLL");
  limit3->Draw(ystring3+":"+axis3, "deltaNLL!=0 && " + fa3zzTozz+">=0 &&" +cut3); 
  TGraph* gr3 = new TGraph(limit3->GetSelectedRows(), limit3->GetV2(), limit3->GetV1());
  gr3->SetMarkerSize(1);
  gr3->SetMarkerStyle(23);
  gr3->SetMarkerColor(kRed);
  gr3->SetLineColor(kRed);
  gr3->SetLineWidth(2);
  cout << f3 << " (red)" << endl;
  findCrossing(1, limit3->GetSelectedRows(), limit3->GetV2(), limit3->GetV1());
  findCrossing(3.84, limit3->GetSelectedRows(), limit3->GetV2(), limit3->GetV1());

  //4
  TFile* fin4;
  TTree* limit4;
  TGraph* gr4;
  if(f4 != ""){
    fin4 = TFile::Open(f4, "READ");
    if(fin4->IsZombie()) {cout << "no file!" << endl; return;}
    limit4 = (TTree*)fin4->Get("limit");
    //limit4->Draw("2*deltaNLL:"+axis4);
    TString ystring4 = f4_scale;
    ystring4 += "*(2*deltaNLL - 2*";
    ystring4 += limit4->GetMinimum("deltaNLL");
    limit4->Draw(ystring4+"):"+axis4, "deltaNLL!=0 && " + fa3zzTozz+">=0 &&" +cut4); 
    gr4 = new TGraph(limit4->GetSelectedRows(), limit4->GetV2(), limit4->GetV1());
    gr4->SetMarkerSize(1);
    gr4->SetMarkerStyle(24);
    gr4->SetMarkerColor(kViolet);
    gr4->SetLineColor(kViolet);
    gr4->SetLineWidth(2);
    cout << f4 << " (violet) WITH SCALE " << f4_scale << endl;
    findCrossing(1, limit4->GetSelectedRows(), limit4->GetV2(), limit4->GetV1());
    findCrossing(3.84, limit4->GetSelectedRows(), limit4->GetV2(), limit4->GetV1());
  }

  TLegend* leg = new TLegend(0.2, legy, .57, legy+0.17);
  leg->AddEntry(gr1, leg1, "l");
  leg->AddEntry(gr2, leg2, "l");
  leg->AddEntry(gr3, leg3, "l");
  if(f4!="") leg->AddEntry(gr4, leg4, "l");
  leg->SetLineColor(0);
  leg->SetFillColor(0);

  TLatex* prelimTex = new TLatex();
  prelimTex->SetNDC();
  prelimTex->SetTextSize(0.03);
  prelimTex->SetTextAlign(31);//right
  prelimTex->SetTextFont(42);

  /*
  double myMax = gr1->GetMaximum();
  if(gr2->GetMaximum ()> myMax) myMax = gr2->GetMaximum();
  if(gr3->GetMaximum ()> myMax) myMax = gr3->GetMaximum();
  myMax = 1.2*myMax;
  cout << "myMax = " << myMax << endl;

  double myMin = gr1->GetMinimum();
  if(gr2->GetMinimum ()< myMin) myMin = gr2->GetMinimum();
  if(gr3->GetMinimum ()< myMin) myMin = gr3->GetMinimum();
  myMin = 1.2*myMin;
  cout << "myMin = " << myMin << endl;
  */

  TCanvas* cs = new TCanvas("cs", "cs", 640, 640);
  cs->cd();
  TH1F* hs = cs->DrawFrame(0, myMin, xmax, myMax);
  hs->GetXaxis()->SetNdivisions(ndiv);
  hs->GetXaxis()->SetLabelSize(0.05);
  hs->GetYaxis()->SetLabelSize(0.05);
  hs->GetXaxis()->SetTitleSize(0.05);
  hs->GetYaxis()->SetTitleSize(0.05);
  hs->GetYaxis()->SetTitleOffset(1.2);
  hs->GetXaxis()->SetTitleOffset(1.2);
  hs->GetXaxis()->SetTitle(xTitle);
  hs->GetYaxis()->SetTitle("-2 #Delta ln L");
  gPad->SetBottomMargin(0.14);
  gPad->SetLeftMargin(0.15);
  gPad->Modified();
  TString style = "L";
  gr1->Draw(style);
  gr2->Draw(style);
  gr3->Draw(style);
  if(f4 != "") gr4->Draw(style);
  leg->Draw();
  prelimTex->DrawLatex(0.88,0.91, "CMS Preliminary, 18.94 fb^{-1} at #sqrt{s} = 8 TeV");
  gPad->Update();
  cs->SaveAs(outName+"_compare.pdf");
  cs->SaveAs(outName+"_compare.png");

  if(f4 != "") fin4->Close();
  fin3->Close();
  fin2->Close();
  fin1->Close();

  delete fin1; delete fin2; delete fin3;
  
  return;
}


void plotEverything(){
  
  /*
  //WH, ZH, VH in fa3ZZ -- ZOOM
  makeOnePlot(fin_WH, fa3zzTozz, "WH",
	      fin_ZH, fa3zzTozz, "ZH",
	      fin_VH, fa3zzTozz, "WH+ZH",
	      "", "", "",
	      0, 1.5, 0.7,
	      "1",
	      "1", "1", "1", "1",
	      "f_{a3}^{ZZ}", "WH_ZH_VH_fa3ZZ", true);
  */

  //Tev - NUMERICAL
  makeOnePlot(fin_WH_tev, fa3zzTozz, "WH",
              fin_ZH_tev, fa3zzTozz, "ZH",
              fin_VH_tev, fa3zzTozz, "WH+ZH",
              "", "", "",
              0, 30, 0.7,
              "1",
              "1", "1", "1", "1",
              "f_{a3}^{ZZ}", "TeV_WH_ZH_VH_fa3ZZ", false);
  

  //WH, ZH, VH in fa3ZZ -- PAPER
  makeOnePlot(fin_WH, fa3zzTozz, "WH",
	      fin_ZH, fa3zzTozz, "ZH",
	      fin_VH, fa3zzTozz, "WH+ZH",
	      "", "", "",
	      0, 1.5, 0.7,
	      "1",
	      "1", "1", "2*deltaNLL<1.02224", "1",
	      "f_{a3}^{ZZ}", "WH_ZH_VH_fa3ZZ", false);
    
  /*
  //WH, ZH, VH in fa3ZH 
  makeOnePlot(fin_WH, fa3zzTozh, "WH",
	      fin_ZH, fa3zzTozh, "ZH",
	      fin_VH, fa3zzTozh, "WH+ZH",
	      "", "", "",
	      0, 1.5, 0.7,
	      "1",
	      "1", "1", "1", "1",
	      "f_{a3}^{ZH}", "WH_ZH_VH_fa3ZH", false);
  */

  /*
  //WW, WH, WW+WH in fa3WW
  makeOnePlot(fin_WW,   fa3zzToww, "WW",
	      fin_WH,   fa3zzToww, "WH",
	      fin_WWWH_float, fa3zzToww, "WW+WH",
	      "", "", "",
	      0, 2, 0.5,
	      "1",
	      "1", "1", "1", "1",
	      "f_{a3}^{WW}", "WW_WH_WWWH_fa3WW", false);

  //WW, WH, WW+WH in fa3WH
  makeOnePlot(fin_WW,   fa3zzTowh, "WW",
	      fin_WH,   fa3zzTowh, "WH",
	      fin_WWWH_float, fa3zzTowh, "WW+WH",
	      "", "", "",
	      0, 2, 0.5,
	      "1",
	      "1", "1", "1", "1",
	      "f_{a3}^{WH}", "WW_WH_WWWH_fa3WH", false);
  */

  //WW, WH, WW+WH in fa3WW -- PAPER
  makeOnePlot(fin_WW,   fa3zzToww, "WW",
	      fin_WH,   fa3zzToww, "WH",
	      fin_WWWH_float, fa3zzToww, "WW+WH",
	      fin_WWWH, fa3zzToww, "#mu^{WW}=#mu^{WH} WW+WH  (#times 1/20)" ,
	      0, 1.7, 0.7,
	      "1/20", 
	      "1", "1", "2*deltaNLL<1.4", "1",
	      "f_{a3}^{WW}", "WW_WH_WWWH_sameMu_fa3WW", false);

  /*
  //WW, WH, WW+WH in fa3WH
  makeOnePlot(fin_WW,   fa3zzTowh, "WW",
	      fin_WH,   fa3zzTowh, "WH",
	      fin_WWWH_float, fa3zzTowh, "WW+WH",
	      fin_WWWH, fa3zzTowh, "#mu^{WW}=#mu^{WH} WW+WH (#times 1/20)",
	      0, 1.7, 0.7,
	      "1/20", 
	      "1", "1", "1", "1",
	      "f_{a3}^{WH}", "WW_WH_WWWH_sameMu_fa3WH", false);
  */

  /*
  //ZZ, ZH, ZZ+ZH in fa3ZZ
  makeOnePlot(fin_ZZ,   fa3zzTozz, "ZZ",
	      fin_ZH,   fa3zzTozz, "ZH",
	      fin_ZZZH_float, fa3zzTozz, "ZZ+ZH",
	      "", "", "",
	      0, 15, 0.5,
	      "1",
	      "1", "1", "1", "1",
	      "f_{a3}^{ZZ}", "ZZ_ZH_ZZZH_fa3ZZ", false);

  //ZZ, ZH, ZZ+ZH in fa3ZH
  makeOnePlot(fin_ZZ,   fa3zzTozh, "ZZ",
	      fin_ZH,   fa3zzTozh, "ZH",
	      fin_ZZZH_float, fa3zzTozh, "ZZ+ZH",
	      "", "", "",
	      0, 15, 0.5,
	      "1", 
	      "1", "1", "1", "1",
	      "f_{a3}^{ZH}", "ZZ_ZH_ZZZH_fa3ZH", false);
  */

  //ZZ, ZH, ZZ+ZH in fa3ZZ -- PAPER
  makeOnePlot(fin_ZZ,   fa3zzTozz, "ZZ",
	      fin_ZH,   fa3zzTozz, "ZH",
	      fin_ZZZH_float, fa3zzTozz, "ZZ+ZH",
	      fin_ZZZH, fa3zzTozz, "#mu^{ZZ}=#mu^{ZH} ZZ+ZH (#times 1/3)",
	      0, 13.5, 0.5,
	      "1/3",
	      "1", "1", "1", "1",
	      "f_{a3}^{ZZ}", "ZZ_ZH_ZZZH_sameMu_fa3ZZ", false);

  /*
  //ZZ, ZH, ZZ+ZH in fa3ZH
  makeOnePlot(fin_ZZ,   fa3zzTozh, "ZZ",
	      fin_ZH,   fa3zzTozh, "ZH",
	      fin_ZZZH_float, fa3zzTozh, "ZZ+ZH",
	      fin_ZZZH, fa3zzTozh, "#mu^{ZZ}=#mu^{ZH} ZZ+ZH (#times 1/3)",
	      0, 13.5, 0.5,
	      "1/3",
	      "1", "1", "1", "1",
	      "f_{a3}^{ZH}", "ZZ_ZH_ZZZH_sameMu_fa3ZH", false);
  */

  /*
  //VV, VH, VV+VH in fa3ZZ
  makeOnePlot(fin_VV,   fa3zzTozz, "VV",
	      fin_VH,   fa3zzTozz, "VH",
	      fin_VVVH_float, fa3zzTozz, "VV+VH",
	      "", "", "",
	      0, 15, 0.5,
	      "1", 
	      "1", "1", "1", "1",
	      "f_{a3}^{ZZ}", "VV_VH_VVVH_fa3ZZ", false);
  */

  //VV, VH, VV+VH in fa3ZZ -- PAPER
  makeOnePlot(fin_VV,   fa3zzTozz, "VV",
	      fin_VH,   fa3zzTozz, "VH",
	      fin_VVVH_float, fa3zzTozz, "VV+VH",
	      fin_VVVH, fa3zzTozz, "#mu^{VV}=#mu^{VH} VV+VH (#times 1/5)",
	      0, 13.5, 0.5,
	      "1/5",
	      "1", "1", "1", "1",
	      "f_{a3}^{ZZ}", "VV_VH_VVVH_sameMu_fa3ZZ", false);

}
