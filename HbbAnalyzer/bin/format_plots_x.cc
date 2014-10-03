void formatPlots() {
	TExec *ex1 = new TExec("ex1","gStyle->SetPalette(1);");
    TExec *ex2 = new TExec("ex2","gStyle->SetPalette(53);");

	TFile* ifile = new TFile("HbbAna.root","READ");
	HbbAnalyzer->cd();

	TCanvas* c1 = new TCanvas();
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
	//HiggsM_gen->GetXaxis()->SetTitle("M_{H} [GeV]");
	HiggsM_gen->GetXaxis()->SetTitleOffset(1.4);
	//HiggsM_gen->GetYaxis()->SetTitle("events / 1 GeV");
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

	TCanvas* c2 = new TCanvas();
	TH1D* HiggsM_gen_clone = (TH1D*)HiggsM_gen->DrawClone();
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

	TH2D* linear_correlation_coefficients_gen = new TH2D("linear_correlation_coefficients_gen","Linear Correlation Coefficients GEN [\%]",4,0,4,4,0,4);
	TH2D* linear_correlation_coefficients     = new TH2D("linear_correlation_coefficients","Linear Correlation Coefficients [\%]",4,0,4,4,0,4);
	int cs[4] = {3,7,11,14};
	for(int iR = 0; iR<4; iR++) {
		linear_correlation_coefficients_gen->GetXaxis()->SetBinLabel(iR+1,Form("R=%.1f",(cs[iR]+1.0)/10.0));
		linear_correlation_coefficients->GetXaxis()->SetBinLabel(iR+1,Form("R=%.1f",(cs[iR]+1.0)/10.0));
		for(int iR2 = 0; iR2<4; iR2++) {
			linear_correlation_coefficients_gen->GetYaxis()->SetBinLabel(iR+1,Form("R=%.1f",(cs[iR]+1.0)/10.0));
			linear_correlation_coefficients->GetYaxis()->SetBinLabel(iR+1,Form("R=%.1f",(cs[iR]+1.0)/10.0));
			linear_correlation_coefficients_gen->SetBinContent(iR+1,iR2+1,((TH2D*)gDirectory->Get(Form("THiggsM_gen_R%i_R%i",cs[iR],cs[iR2])))->GetCorrelationFactor()*100.0);
			linear_correlation_coefficients_gen->SetBinContent(iR2+1,iR+1,((TH2D*)gDirectory->Get(Form("THiggsM_gen_R%i_R%i",cs[iR],cs[iR2])))->GetCorrelationFactor()*100.0);			
			linear_correlation_coefficients->SetBinContent(iR+1,iR2+1,((TH2D*)gDirectory->Get(Form("THiggsM_R%i_R%i",cs[iR],cs[iR2])))->GetCorrelationFactor()*100.0);
			linear_correlation_coefficients->SetBinContent(iR2+1,iR+1,((TH2D*)gDirectory->Get(Form("THiggsM_R%i_R%i",cs[iR],cs[iR2])))->GetCorrelationFactor()*100.0);
		}
	}
	gStyle->SetPaintTextFormat(".0f");
	TCanvas* c3 = new TCanvas();
	linear_correlation_coefficients_gen->SetMarkerSize(1.5);
	linear_correlation_coefficients_gen->LabelsOption("v","Y");
	linear_correlation_coefficients_gen->GetYaxis()->LabelsOption("v");
	linear_correlation_coefficients_gen->Draw("colz");
	ex1->Draw();
	linear_correlation_coefficients_gen->Draw("text same");
	TCanvas* c4 = new TCanvas();
	linear_correlation_coefficients->SetMarkerSize(1.5);
	linear_correlation_coefficients->LabelsOption("v","Y");
	linear_correlation_coefficients->GetYaxis()->LabelsOption("v");
	linear_correlation_coefficients->Draw("colz");
	ex1->Draw();
	linear_correlation_coefficients->Draw("text same");

	TLatex* t = new TLatex();
	cout << t << endl;
	t->SetTextSize(34);
	t->SetTextColor(kRed+3);
	t->SetTextAlign(11);

	TCanvas* c5 = new TCanvas();
	THiggsM_gen_R4_R11->SetTitle("2D Mass Distribution GEN");
	THiggsM_gen_R4_R11->GetXaxis()->CenterTitle();
	THiggsM_gen_R4_R11->GetXaxis()->SetTitleOffset(1.5);
	THiggsM_gen_R4_R11->GetXaxis()->SetTitle("m_{bb} (R=0.5)");
	THiggsM_gen_R4_R11->GetYaxis()->CenterTitle();
	THiggsM_gen_R4_R11->GetYaxis()->SetTitleOffset(1.7);
	THiggsM_gen_R4_R11->GetYaxis()->SetTitle("m_{bb} (R=1.2)");
	THiggsM_gen_R4_R11->Draw("col");
	t->DrawLatex(120,40,"Signal");
	ex2->Draw();
	THiggsM_gen_R4_R11->Draw("col");
	TCanvas* c6 = new TCanvas();
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
	//t->DrawLatexNDC(0.6,0.2,"Signal");
} 