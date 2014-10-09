//ROOT Libraries
#include "TROOT.h"
#include "TSystem.h"
#include "TStyle.h"
#include "TExec.h"
#include "TFile.h"
#include "TDirectory.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "TH1.h"
#include "TH2.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TLatex.h"
#include "TLegend.h"
#include "TString.h"

//C++ Libraries
#include <iostream>
#include <vector>

//User LIbraries
#include "JetMETAnalysis/JetUtilities/interface/CommandLine.h"
#include "/uscms/home/aperloff/Scripts/tdrstyle.C"

using namespace std;

////////////////////////////////////////////////////////////////////////////////
//  Global Variables
////////////////////////////////////////////////////////////////////////////////
TExec* ex1 = new TExec("ex1","gStyle->SetPalette(1);");
TExec* ex2 = new TExec("ex2","gStyle->SetPalette(53);");

////////////////////////////////////////////////////////////////////////////////
//  Local Functions
////////////////////////////////////////////////////////////////////////////////

/// Get 1-D Higgs mass distributions with PDGID, GEN, RECO
void get_1D_mass_distributions(TDirectory* tdir, map<TString,TCanvas*> & canvases);

/// Get 2-D mass distributions from select telescoped cone sizes
void get_2D_mass_distributions(TDirectory* tdir, map<TString,TCanvas*> & canvases);

/// Get linear correclation factor canvases
void get_linear_correlation_factor_canvases(TDirectory* tdir, map<TString,TCanvas*> & canvases);

/// Get the distributions of the number of interpretations passing the cuts
void get_z_distributions(TDirectory* tdir_signal, TDirectory* tdir_background, map<TString, TCanvas*> &canvases);

/// Get the volatility distributions
void get_volatility_distributions(TDirectory* tdir_signal, TDirectory* tdir_background, map<TString, TCanvas*> &canvases);

/// Save the final canvases as images and together in a ROOT file
void write_canvases(CommandLine & cl, map<TString,TCanvas*> & canvases);

////////////////////////////////////////////////////////////////////////////////
//  main
////////////////////////////////////////////////////////////////////////////////

//______________________________________________________________________________
int main(int argc,char**argv) {
	// evaluate command-line / configuration file options
	CommandLine cl;
	if (!cl.parse(argc,argv)) return 0;

	TString         idir      = cl.getValue<TString> ("idir",                  "./");
	TString         ifilename = cl.getValue<TString> ("ifilename",    "HbbAna.root");
	TString         odir      = cl.getValue<TString> ("odir",                  "./");
	vector<TString> oformats  = cl.getVector<TString>("oformats",     ".png:::.pdf");

	if (!cl.partialCheck()) return 0;
	cl.print();

	//
	// Check the input strings given in the command line options
	//
    if(idir.IsNull()) idir = string (gSystem->pwd())+"/";
    if(!idir.EndsWith("/")) idir+="/";

    //
    // Open the file containing the original, unformated closure plots
    //
	TFile* ifile = new TFile(idir+ifilename,"READ");
	ifile->cd("HbbAnalyzer");
	TDirectory* tdir = gDirectory;

	map<TString,TCanvas*> canvases;

	//
	// Set the overall style of the plots
	//
	TStyle* tdrStyle = getTDRStyle();
	gROOT->SetStyle(tdrStyle->GetName());

	get_1D_mass_distributions(tdir,canvases);
	get_linear_correlation_factor_canvases(tdir,canvases);
	get_2D_mass_distributions(tdir,canvases);
	get_z_distributions(tdir,tdir,canvases);

	//
	// Write the final formatted canvases to files
	//
	write_canvases(cl,canvases);

	//
	// Close the open input ROOT file
	//
	ifile->Close();
}

////////////////////////////////////////////////////////////////////////////////
//  Implement Local Functions
////////////////////////////////////////////////////////////////////////////////

//______________________________________________________________________________
void get_1D_mass_distributions(TDirectory* tdir, map<TString,TCanvas*> & canvases) {
	canvases["HiggsM_gen"] = new TCanvas("canvas_HiggsM_gen","M_{H}^{GEN}");

	TH1D* HiggsM_gen  = (TH1D*)tdir->Get("HiggsM_gen");
	TH1D* mjj_gen     = (TH1D*)tdir->Get("mjj_gen");
	TH1D* THiggsM_gen = (TH1D*)tdir->Get("THiggsM_gen");
	TH1D* Tmjj_gen    = (TH1D*)tdir->Get("Tmjj_gen");
	TH1D* THiggsM     = (TH1D*)tdir->Get("THiggsM");
	TH1D* Tmjj        = (TH1D*)tdir->Get("Tmjj");

	HiggsM_gen->SetLineColor(kRed);
	HiggsM_gen->Draw();
	mjj_gen->SetLineColor(kOrange);
	mjj_gen->SetMarkerColor(kOrange);
	mjj_gen->SetMarkerStyle(20);
	mjj_gen->Draw("sameP");
	THiggsM_gen->Draw("same");
	Tmjj_gen->SetLineColor(kMagenta);
	Tmjj_gen->SetMarkerColor(kMagenta);
	Tmjj_gen->SetMarkerStyle(20);
	Tmjj_gen->Draw("sameP");
	THiggsM->SetLineColor(kGreen);
	THiggsM->Draw("same");
	Tmjj->SetLineColor(kYellow);
	Tmjj->SetMarkerColor(kYellow);
	Tmjj->SetMarkerStyle(20);
	Tmjj->Draw("sameP");
	HiggsM_gen->GetXaxis()->SetTitleOffset(1.4);
	HiggsM_gen->GetYaxis()->SetTitleOffset(1.7);
	HiggsM_gen->GetYaxis()->SetRangeUser(0,500);
	TLegend * leg = new TLegend(0.2,0.6,0.6,0.9);
	leg->SetFillColor(0);
	leg->SetFillStyle(0);
	leg->AddEntry((TObject*)0,"Anti-k_{T} R={0.1-1.5}, PF+CHS","");
	leg->AddEntry(HiggsM_gen,"M_{H}^{GEN} Based on pdgId","l");
	leg->AddEntry(THiggsM_gen,"M_{H}^{GEN} Telescoping","l");
	leg->AddEntry(THiggsM,"M_{H}^{RECO} Telescoping","l");
	leg->AddEntry(mjj_gen,"M_{jj}^{GEN} Based on pdgId","p");
	leg->AddEntry(Tmjj_gen,"M_{jj}^{GEN} Telescoping","p");
	leg->AddEntry(Tmjj,"M_{jj}^{RECO} Telescoping","p");
	leg->Draw("same");

	canvases["HiggsM"] = new TCanvas("canvas_HiggsM","M_{H}");

	TH1D* HiggsM_gen_clone = (TH1D*)HiggsM_gen->DrawClone();
	TH1D* THiggsM_gen_R3   = (TH1D*)tdir->Get("THiggsM_gen_R3");
	TH1D* THiggsM_R3       = (TH1D*)tdir->Get("THiggsM_R3");

	HiggsM_gen_clone->GetYaxis()->SetRangeUser(0,175);
	THiggsM_gen_R3->Draw("same");
	THiggsM_R3->SetLineColor(kGreen);
	THiggsM_R3->Draw("same");
	TLegend * leg2 = new TLegend(0.2,0.6,0.6,0.9);
	leg2->SetFillColor(0);
	leg2->SetFillStyle(0);
	leg2->AddEntry((TObject*)0,"Anti-k_{T} R=0.4, PF+CHS","");
	leg2->AddEntry(HiggsM_gen_clone,"M_{H}^{GEN} Based on pdgId","l");
	leg2->AddEntry(THiggsM_gen_R3,"M_{H}^{GEN} Telescoping","l");
	leg2->AddEntry(THiggsM_R3,"M_{H}^{RECO} Telescoping","l");
	leg2->Draw("same");
}

//______________________________________________________________________________
void get_2D_mass_distributions(TDirectory* tdir, map<TString,TCanvas*> & canvases) {
	TLatex* t = new TLatex();
	t->SetNDC();
	t->SetTextSize(0.055);
	t->SetTextColor(kRed+3);
	t->SetTextAlign(11);

	canvases["2D_mass_distribution_gen"] = new TCanvas("canvas_2D_mass_distribution_gen","2D Mass Distribution GEN");
	TH1D* THiggsM_gen_R4_R11 = (TH1D*) tdir->Get("THiggsM_gen_R4_R11");
	THiggsM_gen_R4_R11->SetTitle("2D Mass Distribution GEN");
	THiggsM_gen_R4_R11->GetXaxis()->CenterTitle();
	THiggsM_gen_R4_R11->GetXaxis()->SetTitleOffset(1.5);
	THiggsM_gen_R4_R11->GetXaxis()->SetTitle("m_{bb} (R=0.5)");
	THiggsM_gen_R4_R11->GetYaxis()->CenterTitle();
	THiggsM_gen_R4_R11->GetYaxis()->SetTitleOffset(1.7);
	THiggsM_gen_R4_R11->GetYaxis()->SetTitle("m_{bb} (R=1.2)");
	THiggsM_gen_R4_R11->Draw("col");
	ex2->Draw();
	THiggsM_gen_R4_R11->Draw("col");
	t->DrawLatexNDC(0.6,0.2,"Signal");
	
	canvases["2D_mass_distribution"] = new TCanvas("canvas_2D_mass_distribution","2D Mass Distribution");
	TH1D* THiggsM_R4_R11 = (TH1D*) tdir->Get("THiggsM_R4_R11");
	THiggsM_R4_R11->SetTitle("2D Mass Distribution");
	THiggsM_R4_R11->GetXaxis()->CenterTitle();
	THiggsM_R4_R11->GetXaxis()->SetTitleOffset(1.5);
	THiggsM_R4_R11->GetXaxis()->SetTitle("m_{bb} (R=0.5)");
	THiggsM_R4_R11->GetYaxis()->CenterTitle();
	THiggsM_R4_R11->GetYaxis()->SetTitleOffset(1.7);
	THiggsM_R4_R11->GetYaxis()->SetTitle("m_{bb} (R=1.2)");
	THiggsM_R4_R11->Draw("col");
	ex2->Draw();
	THiggsM_R4_R11->Draw("col same");
	t->DrawLatexNDC(0.6,0.2,"Signal");
}

//______________________________________________________________________________
void get_linear_correlation_factor_canvases(TDirectory* tdir, map<TString,TCanvas*> & canvases) {
	TH2D* linear_correlation_coefficients_gen = new TH2D("linear_correlation_coefficients_gen","Linear Correlation Coefficients GEN [\%]",4,0,4,4,0,4);
	TH2D* linear_correlation_coefficients     = new TH2D("linear_correlation_coefficients","Linear Correlation Coefficients [\%]",4,0,4,4,0,4);
	int cs[4] = {3,7,11,14};
	for(int iR = 0; iR<4; iR++) {
		linear_correlation_coefficients_gen->GetXaxis()->SetBinLabel(iR+1,Form("R=%.1f",(cs[iR]+1.0)/10.0));
		linear_correlation_coefficients->GetXaxis()->SetBinLabel(iR+1,Form("R=%.1f",(cs[iR]+1.0)/10.0));
		for(int iR2 = iR; iR2<4; iR2++) {
			linear_correlation_coefficients_gen->GetYaxis()->SetBinLabel(iR+1,Form("R=%.1f",(cs[iR]+1.0)/10.0));
			linear_correlation_coefficients->GetYaxis()->SetBinLabel(iR+1,Form("R=%.1f",(cs[iR]+1.0)/10.0));
			linear_correlation_coefficients_gen->SetBinContent(iR+1,iR2+1,((TH2D*)tdir->Get(Form("THiggsM_gen_R%i_R%i",cs[iR],cs[iR2])))->GetCorrelationFactor()*100.0);
			linear_correlation_coefficients_gen->SetBinContent(iR2+1,iR+1,((TH2D*)tdir->Get(Form("THiggsM_gen_R%i_R%i",cs[iR],cs[iR2])))->GetCorrelationFactor()*100.0);			
			linear_correlation_coefficients->SetBinContent(iR+1,iR2+1,((TH2D*)tdir->Get(Form("THiggsM_R%i_R%i",cs[iR],cs[iR2])))->GetCorrelationFactor()*100.0);
			linear_correlation_coefficients->SetBinContent(iR2+1,iR+1,((TH2D*)tdir->Get(Form("THiggsM_R%i_R%i",cs[iR],cs[iR2])))->GetCorrelationFactor()*100.0);
		}
	}
	gStyle->SetPaintTextFormat(".0f");
	canvases["linear_correlation_coefficients_gen"] = new TCanvas("canvas_linear_correlation_coefficients_gen","Linear Correlation Coefficients GEN [\%]");
	linear_correlation_coefficients_gen->SetMarkerSize(1.5);
	linear_correlation_coefficients_gen->LabelsOption("v","Y");
	linear_correlation_coefficients_gen->GetYaxis()->LabelsOption("v");
	linear_correlation_coefficients_gen->Draw("colz");
	ex1->Draw();
	linear_correlation_coefficients_gen->Draw("text same");
	canvases["linear_correlation_coefficients"] = new TCanvas("canvas_linear_correlation_coefficients","Linear Correlation Coefficients [\%]");
	linear_correlation_coefficients->SetMarkerSize(1.5);
	linear_correlation_coefficients->LabelsOption("v","Y");
	linear_correlation_coefficients->GetYaxis()->LabelsOption("v");
	linear_correlation_coefficients->Draw("colz");
	ex1->Draw();
	linear_correlation_coefficients->Draw("text same");
}

//______________________________________________________________________________
void get_z_distributions(TDirectory* tdir_signal, TDirectory* tdir_background, map<TString, TCanvas*> &canvases) {
	canvases["rho_z_gen"] = new TCanvas("canvas_rho_z_gen","Fraction of Events Passing the Experimental Cuts at GEN Level");
	TH1D* signal_gen = (TH1D*)tdir_signal->Get("rho_z_gen");
	TH1D* background_gen = (TH1D*)tdir_background->Get("rho_z_gen");
	signal_gen->Scale(1.0/signal_gen->Integral());
	signal_gen->SetLineColor(kBlue);
	signal_gen->SetLineWidth(2);
	signal_gen->GetXaxis()->CenterTitle();
	signal_gen->GetXaxis()->SetTitleOffset(1.5);
	signal_gen->GetYaxis()->SetTitle("Area normalized to 1");
	signal_gen->GetYaxis()->CenterTitle();
	signal_gen->GetYaxis()->SetTitleOffset(1.9);
	background_gen->Scale(1.0/background_gen->Integral());
	background_gen->SetLineColor(kRed);
	background_gen->SetLineWidth(2);
	signal_gen->Draw();
	background_gen->Draw("same");
	TLegend* leg_gen = new TLegend(0.4,0.7,0.8,0.9);
	leg_gen->SetFillColor(0);
	leg_gen->SetFillStyle(0);
	leg_gen->SetBorderSize(1);
	leg_gen->SetTextSize(0.028);
	leg_gen->AddEntry(signal_gen,"ZH telescoping cone","l");
	leg_gen->AddEntry(background_gen,"Zb#bar{b} telescoping cone","l");
	leg_gen->Draw("same");

	canvases["rho_z"] = new TCanvas("canvas_rho_z","Fraction of Events Passing the Experimental Cuts");
	TH1D* signal = (TH1D*)tdir_signal->Get("rho_z");
	TH1D* background = (TH1D*)tdir_background->Get("rho_z");
	signal->Scale(1.0/signal->Integral());
	signal->SetLineColor(kBlue);
	signal->SetLineWidth(2);
	signal->GetXaxis()->CenterTitle();
	signal->GetXaxis()->SetTitleOffset(1.5);
	signal->GetYaxis()->SetTitle("Area normalized to 1");
	signal->GetYaxis()->CenterTitle();
	signal->GetYaxis()->SetTitleOffset(1.9);
	background->Scale(1.0/background->Integral());
	background->SetLineColor(kRed);
	background->SetLineWidth(2);
	signal->Draw();
	background->Draw("same");
	TLegend* leg = new TLegend(0.4,0.7,0.8,0.9);
	leg->SetFillColor(0);
	leg->SetFillStyle(0);
	leg->SetBorderSize(1);
	leg->SetTextSize(0.028);
	leg->AddEntry(signal,"ZH telescoping cone","l");
	leg->AddEntry(background,"Zb#bar{b} telescoping cone","l");
	leg->Draw("same");
}

//______________________________________________________________________________
void get_volatility_distributions(TDirectory* tdir_signal, TDirectory* tdir_background, map<TString, TCanvas*> &canvases) {
	
}

//______________________________________________________________________________
void write_canvases(CommandLine & cl, map<TString,TCanvas*> & canvases) {
	TString         odir     = cl.getValue<TString> ("odir",              "./");
	vector<TString> oformats = cl.getVector<TString>("oformats", ".png:::.pdf");

	if (!cl.partialCheck()) return;

	//
	// Check the output strings given in the command line options
	//
	if(odir.IsNull()) odir = string (gSystem->pwd())+"/";
    if(!odir.EndsWith("/")) odir+="/";

    TFile* ofile = new TFile(odir+"HbbAna_formated.root","RECREATE");

    for(map<TString,TCanvas*>::iterator it=canvases.begin(); it!=canvases.end(); it++) {
    	for(unsigned int iformat=0; iformat<oformats.size(); iformat++) {
    		it->second->SaveAs(odir+it->first+oformats[iformat]);
    	}
    	it->second->Write();
    }

    ofile->Close();
}