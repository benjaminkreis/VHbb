// -*- C++ -*-
//
// Package:    VHbb/HbbAnalyzer
// Class:      HbbAnalyzer
// 
/**\class HbbAnalyzer HbbAnalyzer.cc VHbb/HbbAnalyzer/plugins/HbbAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Alexx Perloff
//         Created:  Fri, 12 Sep 2014 15:53:55 GMT
//
//

// ROOT Libraries
#include "TROOT.h"
#include "TSystem.h"
#include "TString.h"
#include "TH1.h"
#include "TH2.h"
#include "TH1D.h"
#include "TH2D.h"

// STL Libraries
#include <assert.h>
#include <iostream>
#include <map>
#include <memory>
#include <utility>
#include <vector>

// User Libraries
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "VHbb/HbbProducer/interface/HbbTuple.h"
#include "VHbb/HbbProducer/src/helpers.cc"

// Namespaces
using namespace edm;
using std::cout;
using std::endl;
using std::pair;
using std::make_pair;
using std::vector;
using std::map;
using std::multimap;

//
// class declaration
//

class HbbAnalyzer : public edm::EDAnalyzer {
   public:
      explicit HbbAnalyzer(const edm::ParameterSet&);
      ~HbbAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

      //Check if GEN/RECO quantities pass the cuts
      bool ZSelection();
      bool leptonSelection();
      bool jetSelection();
      bool eventSelection();
      template<typename T>
      map<Int_t, Int_t> objectMatching(const vector<Hbb::Object> &col1, const vector<T> &col2);

      //Fill the histograms/graphs
      void fillGenObjects();
      void fillRecoObjects();

   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;
      virtual void getCollections(const edm::Event& iEvent);

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------

      //
      //Handles
      //
      edm::InputTag HbbSrc;
      Handle<Hbb::Tuple> HbbHandle;

      //
      //Telescoping Information
      //
      unsigned int NInterpretations;

      //
      //Cuts
      //
      double theV_MinMass;
      double theV_MaxMass;
      double theV_MinPt;
      double AK4PFCHS_MinPt;
      double AK4PFCHS_MaxEta;
      double AK4PFCHS_MinCSVBTag;
      double Electron_MinPt;
      double Electron_MaxEta;
      double Electron_SCExcludeMinEta;
      double Electron_SCExcludeMaxEta;
      double Electron_MaxIso;
      double Muon_MinPt;
      double Muon_MaxEta;
      double Muon_MaxIso;
      double Tau_MinPt;
      double Tau_MaxEta;
      double Tau_MaxIso;
      double MET_MaxPt;

      //
      //Histograms
      //
      map<TString,TH1*> histograms;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
HbbAnalyzer::HbbAnalyzer(const edm::ParameterSet& iConfig)
{
   //now do what ever initialization is needed

   //
   //Tags
   //
   HbbSrc            = iConfig.getParameter<edm::InputTag>("HbbSource");

   //
   //Telescoping Information
   //
   NInterpretations = iConfig.getParameter<unsigned int>("NInterpretations");

   //
   //Cuts
   //
   theV_MinMass             = iConfig.getParameter<double>("theV_MinMass");
   theV_MaxMass             = iConfig.getParameter<double>("theV_MaxMass");
   theV_MinPt               = iConfig.getParameter<double>("theV_MinPt");
   AK4PFCHS_MinPt           = iConfig.getParameter<double>("AK4PFCHS_MinPt");
   AK4PFCHS_MaxEta          = iConfig.getParameter<double>("AK4PFCHS_MaxEta");
   AK4PFCHS_MinCSVBTag      = iConfig.getParameter<double>("AK4PFCHS_MinCSVBTag");
   Electron_MinPt           = iConfig.getParameter<double>("Electron_MinPt");
   Electron_MaxEta          = iConfig.getParameter<double>("Electron_MaxEta");
   Electron_SCExcludeMinEta = iConfig.getParameter<double>("Electron_SCExcludeMinEta");
   Electron_SCExcludeMaxEta = iConfig.getParameter<double>("Electron_SCExcludeMaxEta");
   Electron_MaxIso          = iConfig.getParameter<double>("Electron_MaxIso");
   Muon_MinPt               = iConfig.getParameter<double>("Muon_MinPt");
   Muon_MaxEta              = iConfig.getParameter<double>("Muon_MaxEta");
   Muon_MaxIso              = iConfig.getParameter<double>("Muon_MaxIso");
   Tau_MinPt                = iConfig.getParameter<double>("Tau_MinPt");
   Tau_MaxEta               = iConfig.getParameter<double>("Tau_MaxEta");
   Tau_MaxIso               = iConfig.getParameter<double>("Tau_MaxIso");
   MET_MaxPt                = iConfig.getParameter<double>("MET_MaxPt");
}


HbbAnalyzer::~HbbAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
HbbAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
//#ifdef THIS_IS_AN_EVENT_EXAMPLE
  getCollections(iEvent);

  if(!eventSelection()) return;

  //
  //Gen Level Objects
  //

  //Non-Telescoping Higgs
  histograms["HiggsM_gen"]->Fill(HbbHandle->genHiggs.lv.M());
  histograms["HiggsPt_gen"]->Fill(HbbHandle->genHiggs.lv.Pt());
  histograms["HiggsEta_gen"]->Fill(HbbHandle->genHiggs.lv.Eta());
  histograms["HiggsPhi_gen"]->Fill(HbbHandle->genHiggs.lv.Phi());
  histograms["HiggspdgId_gen"]->Fill(HbbHandle->genHiggs.pdgId);
  histograms["mjj_gen"]->Fill((HbbHandle->genB.lv+HbbHandle->genAntiB.lv).M());

  //Non-Telescoping Jets
  histograms["j1M_gen"]->Fill(HbbHandle->genB.lv.M());
  histograms["j1Pt_gen"]->Fill(HbbHandle->genB.lv.Pt());
  histograms["j1Eta_gen"]->Fill(HbbHandle->genB.lv.Eta());
  histograms["j1Phi_gen"]->Fill(HbbHandle->genB.lv.Phi());
  histograms["j1pdgId_gen"]->Fill(HbbHandle->genB.pdgId);
  histograms["j2M_gen"]->Fill(HbbHandle->genAntiB.lv.M());
  histograms["j2Pt_gen"]->Fill(HbbHandle->genAntiB.lv.Pt());
  histograms["j2Eta_gen"]->Fill(HbbHandle->genAntiB.lv.Eta());
  histograms["j2Phi_gen"]->Fill(HbbHandle->genAntiB.lv.Phi());
  histograms["j2pdgId_gen"]->Fill(HbbHandle->genAntiB.pdgId);

  int interpretations_passing_cuts = 0;
  for(unsigned int iR=0; iR<HbbHandle->genTeleHiggs.size(); iR++) {
    //Telescoping Higgs 
    histograms["THiggsM_gen"]->Fill(HbbHandle->genTeleHiggs[iR].lv.M());
    histograms[Form("THiggsM_gen_R%i",iR)]->Fill(HbbHandle->genTeleHiggs[iR].lv.M());
    for(unsigned int iR2=iR; iR2<HbbHandle->genTeleHiggs.size(); iR2++) {
      histograms[Form("THiggsM_gen_R%i_R%i",iR,iR2)]->Fill(HbbHandle->genTeleHiggs[iR].lv.M(),HbbHandle->genTeleHiggs[iR2].lv.M());
    }
    histograms["THiggsPt_gen"]->Fill(HbbHandle->genTeleHiggs[iR].lv.Pt());
    histograms["THiggsEta_gen"]->Fill(HbbHandle->genTeleHiggs[iR].lv.Eta());
    histograms["THiggsPhi_gen"]->Fill(HbbHandle->genTeleHiggs[iR].lv.Phi());

    //Telescoping Mjj
    pair<int,int> lSublIndex = make_pair(-1,-1);
    getHiggsCandidate(HbbHandle->genTeleHiggs[iR].daughters,lSublIndex);
    double mjj = (HbbHandle->genTeleHiggs[iR].daughters[lSublIndex.first].lv+HbbHandle->genTeleHiggs[iR].daughters[lSublIndex.second].lv).M();
    histograms["Tmjj_gen"]->Fill(mjj);

    //Telescoping Jets
    histograms["Tj1M_gen"]->Fill(HbbHandle->genTeleHiggs[iR].daughters[lSublIndex.first].lv.M());
    histograms["Tj1Pt_gen"]->Fill(HbbHandle->genTeleHiggs[iR].daughters[lSublIndex.first].lv.Pt());
    histograms["Tj1Eta_gen"]->Fill(HbbHandle->genTeleHiggs[iR].daughters[lSublIndex.first].lv.Eta());
    histograms["Tj1Phi_gen"]->Fill(HbbHandle->genTeleHiggs[iR].daughters[lSublIndex.first].lv.Phi());
    histograms["Tj2M_gen"]->Fill(HbbHandle->genTeleHiggs[iR].daughters[lSublIndex.second].lv.M());
    histograms["Tj2Pt_gen"]->Fill(HbbHandle->genTeleHiggs[iR].daughters[lSublIndex.second].lv.Pt());
    histograms["Tj2Eta_gen"]->Fill(HbbHandle->genTeleHiggs[iR].daughters[lSublIndex.second].lv.Eta());
    histograms["Tj2Phi_gen"]->Fill(HbbHandle->genTeleHiggs[iR].daughters[lSublIndex.second].lv.Phi());

    if(mjj>110 && mjj<140 && HbbHandle->genTeleHiggs[iR].daughters[lSublIndex.first].lv.Pt()>25 &&
      HbbHandle->genTeleHiggs[iR].daughters[lSublIndex.second].lv.Pt()>25)
      interpretations_passing_cuts++;
  }

  //Telescoping Interpretations
  histograms["rho_z_gen"]->Fill(double(interpretations_passing_cuts)/HbbHandle->genTeleHiggs.size());

  //
  //RECO Level Objects
  //

  interpretations_passing_cuts = 0;
  for(unsigned int iR=0; iR<HbbHandle->TeleHiggs.size(); iR++) {
    //Telecoping Higgs
    histograms["THiggsM"]->Fill(HbbHandle->TeleHiggs[iR].lv.M());
    histograms[Form("THiggsM_R%i",iR)]->Fill(HbbHandle->TeleHiggs[iR].lv.M());
    for(unsigned int iR2=iR; iR2<HbbHandle->TeleHiggs.size(); iR2++) {
      histograms[Form("THiggsM_R%i_R%i",iR,iR2)]->Fill(HbbHandle->TeleHiggs[iR].lv.M(),HbbHandle->TeleHiggs[iR2].lv.M());
    }

    histograms["THiggsPt"]->Fill(HbbHandle->TeleHiggs[iR].lv.Pt());
    histograms["THiggsEta"]->Fill(HbbHandle->TeleHiggs[iR].lv.Eta());
    histograms["THiggsPhi"]->Fill(HbbHandle->TeleHiggs[iR].lv.Phi());

    //Telescoping Mjj
    pair<int,int> lSublIndex = make_pair(-1,-1);
    getHiggsCandidate(HbbHandle->TeleHiggs[iR].daughters,lSublIndex);
    double mjj = (HbbHandle->TeleHiggs[iR].daughters[lSublIndex.first].lv+HbbHandle->TeleHiggs[iR].daughters[lSublIndex.second].lv).M();
    histograms["Tmjj"]->Fill(mjj);

    //Telescoping Jets
    histograms["Tj1M"]->Fill(HbbHandle->TeleHiggs[iR].daughters[lSublIndex.first].lv.M());
    histograms["Tj1Pt"]->Fill(HbbHandle->TeleHiggs[iR].daughters[lSublIndex.first].lv.Pt());
    histograms["Tj1Eta"]->Fill(HbbHandle->TeleHiggs[iR].daughters[lSublIndex.first].lv.Eta());
    histograms["Tj1Phi"]->Fill(HbbHandle->TeleHiggs[iR].daughters[lSublIndex.first].lv.Phi());
    histograms["Tj2M"]->Fill(HbbHandle->TeleHiggs[iR].daughters[lSublIndex.second].lv.M());
    histograms["Tj2Pt"]->Fill(HbbHandle->TeleHiggs[iR].daughters[lSublIndex.second].lv.Pt());
    histograms["Tj2Eta"]->Fill(HbbHandle->TeleHiggs[iR].daughters[lSublIndex.second].lv.Eta());
    histograms["Tj2Phi"]->Fill(HbbHandle->TeleHiggs[iR].daughters[lSublIndex.second].lv.Phi());

    if(mjj>110 && mjj<140 && HbbHandle->genTeleHiggs[iR].daughters[lSublIndex.first].lv.Pt()>25 &&
      HbbHandle->genTeleHiggs[iR].daughters[lSublIndex.second].lv.Pt()>25)
      interpretations_passing_cuts++;
  }

  //Telescoping Interpretations
  histograms["rho_z"]->Fill(double(interpretations_passing_cuts)/HbbHandle->TeleHiggs.size());
//#endif
   
#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
#endif
}


// ------------ method called once each job just before starting event loop  ------------
void 
HbbAnalyzer::beginJob()
{
  edm::Service<TFileService> fs;
  if (!fs) throw edm::Exception(edm::errors::Configuration,
                                "TFileService missing from configuration!");

    //Use later 
    //(Anti-k_{T} R={0.1-1.5}, PF+CHS)

  //
  //GEN Level Objects
  //

  //Non-Telescoping Higgs
  histograms["HiggsM_gen"]     = fs->make<TH1D>("HiggsM_gen"     ,"M_{H}^{GEN};M_{H}^{GEN} [GeV];Events / 5 GeV"             ,40,0,200);
  histograms["HiggsPt_gen"]    = fs->make<TH1D>("HiggsPt_gen"    ,"p_{T}_{H}^{GEN};p_{T}_{H}^{GEN} [GeV];Events / 5 GeV"     ,200,0,1000);
  histograms["HiggsEta_gen"]   = fs->make<TH1D>("HiggsEta_gen"   ,"#eta_{H}^{GEN};#eta_{H}^{GEN};Events / 0.1"               ,100,-5,5);
  histograms["HiggsPhi_gen"]   = fs->make<TH1D>("HiggsPhi_gen"   ,"#phi_{H}^{GEN};#phi_{H}^{GEN};Events / 6^{#circ}"         ,60,-TMath::Pi(),TMath::Pi());
  histograms["HiggspdgId_gen"] = fs->make<TH1D>("HiggspdgId_gen" ,"pdgId_{H}^{GEN};pdgId_{H}^{GEN};Number of Jets"           ,60,-30,30);
  histograms["mjj_gen"]        = fs->make<TH1D>("mjj_gen"        ,"m_{jj}^{GEN};m_{jj}^{GEN} [GeV];Events / 5 GeV"           ,40,0,200);

  //Non-Telescoping V
  histograms["VM_gen"]     = fs->make<TH1D>("VM_gen"    ,"M_{V}^{GEN};M^{GEN} [GeV];Events / 5 GeV"             ,40,0,200);
  histograms["VPt_gen"]    = fs->make<TH1D>("VPt_gen"   ,"p_{T}_{V}^{GEN};p_{T}_{V}^{GEN} [GeV]; Events / 5 GeV",200,0,1000);
  histograms["VEta_gen"]   = fs->make<TH1D>("VEta_gen"  ,"#eta_{V}^{GEN};#eta_{V}^{GEN};Events / 0.1"           ,100,-5,5);
  histograms["VPhi_gen"]   = fs->make<TH1D>("VPhi_gen"  ,"#phi_{V}^{GEN};#phi_{V}^{GEN};Events / 6^{#circ}"     ,60,-TMath::Pi(),TMath::Pi());
  histograms["VpdgId_gen"] = fs->make<TH1D>("VpdgId_gen","pdgId_{V}^{GEN};pdgId_{V}^{GEN};Number of Jets"       ,60,-30,30);

  //Non-Telescoping Jets
  histograms["j1M_gen"]        = fs->make<TH1D>("j1M_gen"        ,"M^{GEN Leading};M^{GEN Leading} [GeV];Events / 5 GeV"                ,40,0,200);
  histograms["j1Pt_gen"]       = fs->make<TH1D>("j1Pt_gen"       ,"p_{T}^{GEN Leading};p_{T}^{GEN Leading} [GeV];Events / 5 GeV"        ,200,0,1000);
  histograms["j1Eta_gen"]      = fs->make<TH1D>("j1Eta_gen"      ,"#eta^{GEN Leading};#eta^{GEN Leading};Events / 0.1"                  ,100,-5,5);
  histograms["j1Phi_gen"]      = fs->make<TH1D>("j1Phi_gen"      ,"#phi^{GEN Leading};#phi^{GEN Leading};Events/ 6^{#circ}"             ,60,-TMath::Pi(),TMath::Pi());
  histograms["j1pdgId_gen"]    = fs->make<TH1D>("j1pdgId_gen"    ,"pdgId^{GEN Leading};pdgId^{GEN Leading};Number of Jets"              ,60,-30,30);
  histograms["j2M_gen"]        = fs->make<TH1D>("j2M_gen"        ,"M^{GEN Sub-Leading};M^{GEN Sub-Leading} [GeV];Events / 5 GeV"        ,40,0,200);
  histograms["j2Pt_gen"]       = fs->make<TH1D>("j2Pt_gen"       ,"p_{T}^{GEN Sub-Leading};p_{T}^{GEN Sub-Leading} [GeV];Events / 5 GeV",200,0,1000);
  histograms["j2Eta_gen"]      = fs->make<TH1D>("j2Eta_gen"      ,"#eta^{GEN Sub-Leading};#eta^{GEN Sub-Leading};Events / 0.1"          ,100,-5,5);
  histograms["j2Phi_gen"]      = fs->make<TH1D>("j2Phi_gen"      ,"#phi^{GEN Sub-Leading};#phi^{GEN Sub-Leading};Events / 6^{#circ}"    ,60,-TMath::Pi(),TMath::Pi());
  histograms["j2pdgId_gen"]    = fs->make<TH1D>("j2pdgId_gen"    ,"pdgId^{GEN Sub-Leading};pdgId^{GEN Sub-Leading};Number of Jets"      ,60,-30,30);

  //Telescoping Higgs
  histograms["THiggsM_gen"]    = fs->make<TH1D>("THiggsM_gen"     ,"M_{H}^{GEN} (R={0.1-1.5});M_{H}^{GEN} [GeV];Events / 5 GeV"        ,40,0,200);
  histograms["THiggsPt_gen"]   = fs->make<TH1D>("THiggsPt_gen"    ,"p_{T}_{H}^{GEN} (R={0.1-1.5});p_{T}_{H}^{GEN} [GeV];Events / 5 GeV",200,0,1000);
  histograms["THiggsEta_gen"]  = fs->make<TH1D>("THiggsEta_gen"   ,"#eta_{H}^{GEN} (R={0.1-1.5});#eta_{H}^{GEN};Events / 0.1"          ,100,-5,5);
  histograms["THiggsPhi_gen"]  = fs->make<TH1D>("THiggsPhi_gen"   ,"#phi_{H}^{GEN} (R={0.1-1.5});#phi_{H}^{GEN};Events / 6^{#circ}"    ,60,-TMath::Pi(),TMath::Pi());
  for(unsigned int iR=0; iR<NInterpretations; iR++) {
    histograms[Form("THiggsM_gen_R%i",iR)] = fs->make<TH1D>(Form("THiggsM_gen_R%i",iR),Form("M_{H}^{GEN} (Anti-k_{T} R=%.1f, PF+CHS);M_{H}^{GEN} [GeV];Events / 5 GeV",(iR/10.0)+0.1),40,0,200);
    for(unsigned int iR2=iR; iR2<NInterpretations; iR2++) {
      histograms[Form("THiggsM_gen_R%i_R%i",iR,iR2)] = fs->make<TH2D>(Form("THiggsM_gen_R%i_R%i",iR,iR2),Form("M_{H}^{GEN} (Anti-k_{T}, PF+CHS);M_{H}^{GEN} (R=%.1f) [GeV];M_{H}^{GEN} (R=%.1f) [GeV];Events / 5 GeV",(iR/10.0)+0.1,(iR2/10.0)+0.1),40,0,200,40,0,200);
    }
  }
  histograms["Tmjj_gen"]       = fs->make<TH1D>("Tmjj_gen"        ,"m_{jj}^{GEN};M_{jj}^{GEN} [GeV];Events / 5 GeV"                          ,40,0,200);

  //Telescoping Jets
  histograms["Tj1M_gen"]       = fs->make<TH1D>("Tj1M_gen"        ,"M^{GEN Leading Jet};M^{GEN Leading Jet} [GeV];Events / 5 GeV"            ,40,0,200);
  histograms["Tj1Pt_gen"]      = fs->make<TH1D>("Tj1Pt_gen"       ,"p_{T}^{GEN Leading Jet};p_{T}^{GEN Leading Jet} [GeV];Events / 5 GeV"    ,200,0,1000);
  histograms["Tj1Eta_gen"]     = fs->make<TH1D>("Tj1Eta_gen"      ,"#eta^{GEN Leading Jet};#eta^{GEN Leading Jet};Events / 0.1"              ,100,-5,5);
  histograms["Tj1Phi_gen"]     = fs->make<TH1D>("Tj1Phi_gen"      ,"#phi^{GEN Leading Jet};#phi^{GEN Leading Jet};Events / 6^{#circ}"        ,60,-TMath::Pi(),TMath::Pi());
  histograms["Tj2M_gen"]       = fs->make<TH1D>("Tj2M_gen"        ,"M^{GEN Sub-Leading Jet};M^{GEN Sub-Leading Jet} [GeV];Events / 5 GeV"    ,40,0,200);
  histograms["Tj2Pt_gen"]      = fs->make<TH1D>("Tj2Pt_gen"       ,"p_{T}^{GEN Sub-Leading Jet};p_{T}^{GEN Sub-Leading Jet}Events / 5 GeV"   ,200,0,1000);
  histograms["Tj2Eta_gen"]     = fs->make<TH1D>("Tj2Eta_gen"      ,"#eta^{GEN Sub-Leading Jet};;#eta^{GEN Sub-Leading Jet};Events / 0.1"     ,100,-5,5);
  histograms["Tj2Phi_gen"]     = fs->make<TH1D>("Tj2Phi_gen"      ,"#phi^{GEN Sub-Leading Jet};#phi^{GEN Sub-Leading Jet};Events / 6^{#circ}",60,-TMath::Pi(),TMath::Pi());

  //Telescoping Interpretations
  histograms["rho_z_gen"] = fs->make<TH1D>("rho_z_gen","Interpretations Passing The Cuts;z;Events",100,0,1);

  //
  //RECO Level Objects
  //

  //Non-Telescoping V
  histograms["VM"]     = fs->make<TH1D>("VM"    ,"M_{V};M [GeV];Events / 5 GeV"             ,40,0,200);
  histograms["VPt"]    = fs->make<TH1D>("VPt"   ,"p_{T}_{V};p_{T}_{V} [GeV]; Events / 5 GeV",200,0,1000);
  histograms["VEta"]   = fs->make<TH1D>("VEta"  ,"#eta_{V};#eta_{V};Events / 0.1"           ,100,-5,5);
  histograms["VPhi"]   = fs->make<TH1D>("VPhi"  ,"#phi_{V};#phi_{V};Events / 6^{#circ}"     ,60,-TMath::Pi(),TMath::Pi());
  histograms["VpdgId"] = fs->make<TH1D>("VpdgId","pdgId_{V};pdgId_{V};Number of Jets"       ,60,-30,30);

  //Telescoping Higgs
  histograms["THiggsM"]   = fs->make<TH1D>("THiggsM"  ,"M_{H} (R={0.1-1.5});M_{H} [GeV];Events / 5 GeV"                      ,40,0,200);
  histograms["THiggsPt"]  = fs->make<TH1D>("THiggsPt" ,"p_{T}_{H} (R={0.1-1.5});p_{T}_{H} [GeV];Events / 5 GeV"              ,200,0,1000);
  histograms["THiggsEta"] = fs->make<TH1D>("THiggsEta","#eta_{H} (R={0.1-1.5});#eta_{H};Events / 0.1"                        ,100,-5,5);
  histograms["THiggsPhi"] = fs->make<TH1D>("THiggsPhi","#phi_{H} (R={0.1-1.5});#phi_{H};Events / 6^{#circ}"                  ,60,-TMath::Pi(),TMath::Pi());
  for(unsigned int iR=0; iR<NInterpretations; iR++) {
    histograms[Form("THiggsM_R%i",iR)] = fs->make<TH1D>(Form("THiggsM_R%i",iR),Form("M_{H} (Anti-k_{T} R=%.1f, PF+CHS);M_{H} [GeV];Events / 5 GeV",(iR/10.0)+0.1),40,0,200);
    for(unsigned int iR2=iR; iR2<NInterpretations; iR2++) {
      histograms[Form("THiggsM_R%i_R%i",iR,iR2)] = fs->make<TH2D>(Form("THiggsM_R%i_R%i",iR,iR2),Form("M_{H} (Anti-k_{T}, PF+CHS);M_{H} (R=%.1f) [GeV];M_{H} (R=%.1f) [GeV];Events / 5 GeV",(iR/10.0)+0.1,(iR2/10.0)+0.1),40,0,200,40,0,200);
    }
  }
  histograms["Tmjj"]      = fs->make<TH1D>("Tmjj"     ,"m_{jj};M_{jj} [GeV];Events / 5 GeV"                                  ,40,0,200);

  //Telescoping Jets
  histograms["Tj1M"]      = fs->make<TH1D>("Tj1M"     ,"M^{Leading Jet};M^{Leading Jet} [GeV];Events / 5 GeV"                ,40,0,200);
  histograms["Tj1Pt"]     = fs->make<TH1D>("Tj1Pt"    ,"p_{T}^{Leading Jet};p_{T}^{Leading Jet} [GeV];Events / 5 GeV"        ,200,0,1000);
  histograms["Tj1Eta"]    = fs->make<TH1D>("Tj1Eta"   ,"#eta^{Leading Jet};#eta^{Leading Jet};Events / 0.1"                  ,100,-5,5);
  histograms["Tj1Phi"]    = fs->make<TH1D>("Tj1Phi"   ,"#phi^{Leading Jet};#phi^{Leading Jet};Events / 6^{#circ}"            ,60,-TMath::Pi(),TMath::Pi());
  histograms["Tj2M"]      = fs->make<TH1D>("Tj2M"     ,"M^{Sub-Leading Jet};M^{Sub-Leading Jet} [GeV];Events / 5 GeV"        ,40,0,200);
  histograms["Tj2Pt"]     = fs->make<TH1D>("Tj2Pt"    ,"p_{T}^{Sub-Leading Jet};p_{T}^{Sub-Leading Jet} [GeV];Events / 5 GeV",200,0,1000);
  histograms["Tj2Eta"]    = fs->make<TH1D>("Tj2Eta"   ,"#eta^{Sub-Leading Jet};#eta^{Sub-Leading Jet};Events / 0.1"          ,100,-5,5);
  histograms["Tj2Phi"]    = fs->make<TH1D>("Tj2Phi"   ,"#phi^{Sub-Leading Jet};#phi^{Sub-Leading Jet};Events / 6^{#circ}"    ,60,-TMath::Pi(),TMath::Pi());

  //Telescoping Interpretations
  histograms["rho_z"] = fs->make<TH1D>("rho_z","Interpretations Passing The Cuts;z;Events",100,0,1);
}

// ------------ method called once each job just after ending the event loop  ------------
void 
HbbAnalyzer::endJob() 
{
}

// ------------ method called once each event  ------------
void 
HbbAnalyzer::getCollections(const edm::Event& iEvent) {
    iEvent.getByLabel(HbbSrc,HbbHandle);
    assert(HbbHandle.isValid());
}

// ------------ method called once each event  ------------
bool
HbbAnalyzer::ZSelection() {
  bool massWindowCut = (HbbHandle->theV.lv.M()>theV_MinMass && HbbHandle->theV.lv.M()<theV_MaxMass);
  bool ptCut = HbbHandle->theV.lv.Pt()>theV_MinPt;
  map<int, int> daughterToLeptonMap = objectMatching<Hbb::Muon>(HbbHandle->theV.daughters,HbbHandle->Muons);
  bool eq2Leptons = daughterToLeptonMap.size() == 2;
  if(massWindowCut && ptCut && eq2Leptons)
    return true;
  else
    return false;
}

// ------------ method called once each event  ------------
bool
HbbAnalyzer::leptonSelection() {
  pair<int,int> tightElectrons = make_pair(0,-9999);
  pair<int,int> tightMuons = make_pair(0,-9999);
  pair<int,int> tightTaus = make_pair(0,-9999);
  for(unsigned int iElectron=0; iElectron<HbbHandle->Electrons.size(); iElectron++) {
    if(HbbHandle->Electrons[iElectron].lv.Pt()>Electron_MinPt && 
       TMath::Abs(HbbHandle->Electrons[iElectron].lv.Eta())<Electron_MaxEta &&
       TMath::Abs(HbbHandle->Electrons[iElectron].lv.Eta())>Electron_SCExcludeMinEta &&
       TMath::Abs(HbbHandle->Electrons[iElectron].lv.Eta())<Electron_SCExcludeMaxEta &&
       HbbHandle->Electrons[iElectron].isolation<Electron_MaxIso) {
      tightElectrons.first++;
      if(tightElectrons.first==1)
        tightElectrons.second = HbbHandle->Electrons[iElectron].charge;
      else
        tightElectrons.second += HbbHandle->Electrons[iElectron].charge;
    }
  }
  for(unsigned int iMuon=0; iMuon<HbbHandle->Muons.size(); iMuon++) {
    if(HbbHandle->Muons[iMuon].lv.Pt()>Muon_MinPt &&
       TMath::Abs(HbbHandle->Muons[iMuon].lv.Eta())<Muon_MaxEta &&
       HbbHandle->Muons[iMuon].isolation<Muon_MaxIso) {
      tightMuons.first++;
      if(tightMuons.first==1)
        tightMuons.second = HbbHandle->Muons[iMuon].charge;
      else
        tightMuons.second += HbbHandle->Muons[iMuon].charge;
    }
  }
  for(unsigned int iTau=0; iTau<HbbHandle->Taus.size(); iTau++) {
    if(HbbHandle->Taus[iTau].lv.Pt()>Tau_MinPt &&
       TMath::Abs(HbbHandle->Taus[iTau].lv.Eta())<Tau_MaxEta &&
       HbbHandle->Taus[iTau].isolation<Tau_MaxIso) {
      tightTaus.first++;
      if(tightTaus.first==1)
        tightTaus.second = HbbHandle->Taus[iTau].charge;
      else
        tightTaus.second += HbbHandle->Taus[iTau].charge;
    }
  }


  if(tightElectrons.first==2 && tightMuons.first==0 && tightTaus.first==0 && tightElectrons.second==0)
    return true;
  else if(tightElectrons.first==0 && tightMuons.first==2 && tightTaus.first==0 && tightMuons.second==0)
    return true;
  else if(tightElectrons.first==0 && tightMuons.first==0 && tightTaus.first==2 && tightTaus.second==0)
    return true;
  else
    return false;

}

// ------------ method called once each event  ------------
bool
HbbAnalyzer::jetSelection() {
  int tightJetCounter = 0;
  /*
  for(unsigned int iJet=0; iJet<HbbHandle->AK4PFCHS.size(); iJet++) {
    if(HbbHandle->AK4PFCHS[iJet].lv.Pt()>AK4PFCHS_MinPt &&
       TMath::Abs(HbbHandle->AK4PFCHS[iJet].lv.Eta())<AK4PFCHS_MaxEta &&
       HbbHandle->AK4PFCHS[iJet].csv >= AK4PFCHS_MinCSVBTag) {
      tightJetCounter++;
    }
  }
  */
  for(unsigned int iJet=0; iJet<HbbHandle->theHiggs.daughters.size(); iJet++) {
    if(HbbHandle->theHiggs.daughters[iJet].lv.Pt()>AK4PFCHS_MinPt &&
       TMath::Abs(HbbHandle->theHiggs.daughters[iJet].lv.Eta())<AK4PFCHS_MaxEta &&
       HbbHandle->theHiggs.daughters[iJet].csv >= AK4PFCHS_MinCSVBTag) {
      tightJetCounter++;
    }
  }

  if(tightJetCounter>=2)
    return true;
  else
    return false;
}

// ------------ method called once each event  ------------
bool
HbbAnalyzer::eventSelection() {
  return ZSelection()&&leptonSelection()&&jetSelection();
}

// ------------ methods called when matching any two collections of Hbb::Objects  ------------
template<typename T>
map<Int_t, Int_t>
HbbAnalyzer::objectMatching(const vector<Hbb::Object> &col1, const vector<T> &col2){
   map<Int_t, Int_t> matchingMap;

   // Create an aux map with the dR of all the possible
   // combinations of jets in both events
   multimap<double, pair<Int_t, Int_t> >  auxMap;
   for (unsigned int col1Index = 0; col1Index<col1.size(); col1Index++) {
      bool matchMade = false;
      int col2Index = -1;
      for (typename vector<T>::const_iterator col2It = col2.begin();col2It != col2.end();++col2It) {
         col2Index++;
         if (col2It->lv.Pt()==0) {
            continue;
          }
         if(col2It->lv.Pt()>1.0e-6) {
            double dR = reco::deltaR(col2It->lv.Eta(), col2It->lv.Phi(), col1[col1Index].lv.Eta(), col1[col1Index].lv.Phi());
            //if(auxMap.find(dR) != auxMap.end())
               //cout << "HbbAnalyzer::objectMatching::WARNING Duplicate DeltaR when doing matching." << endl;
            auxMap.insert(make_pair(dR,make_pair(col1Index, col2Index)));
            matchMade = true;
            //if (recIndex == 1)
            //   cout << "RecIndex == 1 and a match made and entered into auxMap[" << dR << "] = std::make_pair(" << recIndex << "," << genIndex << ")" << endl;
         }
      }
      if (!matchMade) {
         cout << "No match" << endl;
         auxMap.insert(make_pair(-1-col1Index,make_pair(col1Index,-1-col1Index)));
      }
   }
   
   //cout << "auxMap.size() = " << auxMap.size() << endl;
   //for (std::multimap<double,pair<int,int> >::iterator it=auxMap.begin(); it!=auxMap.end(); ++it)
   //  std::cout << (*it).first << " => " << (*it).second.first << ","<<(*it).second.second << '\n';

   // First clear the map for this new set of events
   matchingMap.clear();

   // 1-Find the pair of jets with the smallest dr. Add them to resulting map
   // 2-Remove the pair from the map, rinse and repeat.
   while (auxMap.size() > 0){

      // 1- The first element which is the one with the smallest dR. Get the jet indexes
      int j1 = auxMap.begin()->second.first;
      int j2 = auxMap.begin()->second.second;

      // Add to the results
      //if (auxMap.begin()->first < 0.25 && fabs(jp4[j1].refLV.Pt()-(genParticleHandle->begin()+j2)->pt())<1)
      matchingMap[j1] = j2;
      //cout << "RecJet = " << j1 << "\tGenJet = " << j2 << endl;
      
      // 2- Now remove all elements from the auxMap that contain either the first or second jet
      map<double, pair<Int_t, Int_t> >::iterator itr = auxMap.begin();
      while(itr != auxMap.end()){
         if (itr->second.first == j1 || itr->second.second == j2)
            auxMap.erase(itr++);
         else
            ++itr;

      }//while removing

   }//while
   
   //cout << "matchingMap.size() = " << matchingMap.size() << endl;
   
   //Double check that each rec jet has a gen jet match. If not, put a placeholder in.
   for (unsigned int iCol1 = 0; iCol1<col1.size(); iCol1++) {
      if (matchingMap.find(iCol1)!=matchingMap.end())
         continue;
      else {
         cout << "HbbAnalyzer::objectMatching::WARNING Did not find col2 match for col1 index " << iCol1 << endl;
         matchingMap[iCol1] = -1-iCol1;
      }
   }

   return matchingMap;
}//objectMatching

// ------------ method called when starting to processes a run  ------------
/*
void 
HbbAnalyzer::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void 
HbbAnalyzer::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
HbbAnalyzer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
HbbAnalyzer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
HbbAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(HbbAnalyzer);