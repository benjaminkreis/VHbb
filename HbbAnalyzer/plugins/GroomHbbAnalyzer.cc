// -*- C++ -*-
//
// Package:    VHbb/HbbAnalyzer
// Class:      HbbAnalyzer
// 
/**\class HbbAnalyzer HbbAnalyzer.cc VHbb/HbbAnalyzer/plugins/HbbAnalyzer.cc

*/
// Original Author:  Inga Bucinskaite
//         Created:  Fri, 12 Sep 2014 15:53:55 GMT


// system include files
#include <memory>
#include <string>
#include <sstream>
#include <map>
#include "TLorentzVector.h"

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "VHbb/HbbProducer/interface/HbbTuple.h"

//
// class declaration
//

class GroomHbbAnalyzer : public edm::EDAnalyzer {
public:
  explicit GroomHbbAnalyzer(const edm::ParameterSet&);
  ~GroomHbbAnalyzer();
  
  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
  void fillHist(const TString& histName, const Double_t& value, const Double_t& wt=1.0);
  void bookHistograms();
  
  
private:

  virtual void beginJob() override;
  virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
  virtual void endJob() override;

  // use the map function to access the rest of the histograms
  std::map<TString, TH1*> m_HistNames;
  std::map<TString, TH1*>::iterator hid;

  std::map<std::string,std::vector<Hbb::Jet> > jetmap;
  std::map<std::string,std::vector<Hbb::SubJet > > submap;

  // ----------member data ---------------------------
  edm::InputTag HbbSrc;
  std::string algo[5] = {"AK4", "AK8", "AK10", "AK12", "AK15"};
  std::string groom[5] = {"_filtered", "_pruned", "_trimmed", "_mdt", "_bdrs"};
 
  
};

// constants, enums and typedefs
// static data member definitions
// constructors and destructor


GroomHbbAnalyzer::GroomHbbAnalyzer(const edm::ParameterSet& iConfig)
  
{
  //now do what ever initialization is needed
  HbbSrc = edm::InputTag(iConfig.getParameter<edm::InputTag>("HbbSource"));
  
}


GroomHbbAnalyzer::~GroomHbbAnalyzer()
{
  
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
  
}


//
// member functions
//

// ------------ method called for each event  ------------
void
GroomHbbAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;

//#ifdef THIS_IS_AN_EVENT_EXAMPLE
  Handle<Hbb::Tuple> HbbHandle;
  iEvent.getByLabel(HbbSrc,HbbHandle);
  //#endif  

  jetmap["AK4"]=HbbHandle->AK4PFCHS;
  jetmap["AK8"]=HbbHandle->AK8PFCHS;
  jetmap["AK10"]=HbbHandle->AK10PFCHS;
  jetmap["AK12"]=HbbHandle->AK12PFCHS;
  jetmap["AK15"]=HbbHandle->AK15PFCHS;

  for (auto rads =std::begin(algo); rads != std::end(algo); ++rads) {
    if (!(*rads == "AK4") && jetmap[*rads].size() > 0) {
      submap[*rads + "_filtered"]=jetmap[*rads][0].filteredSubJets;
      submap[*rads + "_trimmed"]=jetmap[*rads][0].trimmedSubJets;
      submap[*rads + "_pruned"]=jetmap[*rads][0].prunedSubJets;
      submap[*rads + "_mdt"]=jetmap[*rads][0].mdtSubJets;
      submap[*rads + "_bdrs"]=jetmap[*rads][0].butterSubJets;
    }
  }

 //*************** Z and Muons *************************
  TLorentzVector muon1;
  TLorentzVector muon2; 
  TLorentzVector ZBoson; 
  bool GoodLeptons = false;
  if (HbbHandle->Muons.size() > 1) {
    muon1 = HbbHandle->Muons[0].lv;
    muon2 = HbbHandle->Muons[1].lv;
    ZBoson = HbbHandle->Muons[0].lv+HbbHandle->Muons[1].lv;
    if (muon1.Pt() > 20 && muon2.Pt() > 20 && std::abs(muon1.Eta()) < 2.4 && std::abs(muon2.Eta()) < 2.4 && ZBoson.M() > 75 && ZBoson.M() < 105 && (std::abs(muon1.Eta()) < 1.44 || std::abs(muon1.Eta()) > 1.57) && (std::abs(muon2.Eta()) < 1.44 || std::abs(muon2.Eta()) > 1.57)) {
      GoodLeptons = true;
      fillHist("ZM", ZBoson.M());
      fillHist("ZPt", ZBoson.Pt());
      fillHist("ZEta", ZBoson.Eta());
      fillHist("ZPhi", ZBoson.Phi());
      fillHist("muon1Pt", muon1.Pt());
      fillHist("muon2Pt", muon2.Pt());
      fillHist("muon1Eta", muon1.Eta());
      fillHist("muon2Eta", muon2.Eta());
      fillHist("muon1Phi", muon1.Phi());
      fillHist("muon2Phi", muon2.Phi());  
      if (ZBoson.Pt() > 150) fillHist("ZPt_150", ZBoson.Pt());
      if (ZBoson.Pt() > 200) fillHist("ZPt_200", ZBoson.Pt());
      if (ZBoson.Pt() > 300) fillHist("ZPt_300", ZBoson.Pt());
    }
    if (ZBoson.M() > 75 && ZBoson.M() < 105) fillHist("ZPt_onlymcut", ZBoson.Pt());
  }

 //******************** Generated Particles ****************
  TLorentzVector genb1;
  TLorentzVector genb2; 
  TLorentzVector genHiggs; 
  TLorentzVector genmuon1;
  TLorentzVector genmuon2; 
  TLorentzVector genZ; 
  for (unsigned int g=0; g<HbbHandle->genParticles.size(); g++) {
    //********** gen Higgs *********
    if (std::abs(HbbHandle->genParticles[g].pdgId) == 25 && std::abs(HbbHandle->genParticles[g].daughterIds[0]) == 5) {
      genHiggs = HbbHandle->genParticles[g].lv;
      fillHist("genHM", genHiggs.M());
      fillHist("genHPt", genHiggs.Pt());
      fillHist("genHEta", genHiggs.Eta());
      fillHist("genHPhi", genHiggs.Phi());
    }
    //********** gen b *********
    if (HbbHandle->genParticles[g].pdgId == 5 && std::abs(HbbHandle->genParticles[g].motherId) == 25) {
      genb1 = HbbHandle->genParticles[g].lv;
      fillHist("genbPt", genb1.Pt());
      fillHist("genbEta", genb1.Eta());
      fillHist("genbPhi", genb1.Phi());
    }
    if (HbbHandle->genParticles[g].pdgId == -5 && std::abs(HbbHandle->genParticles[g].motherId) == 25) {
      genb2 = HbbHandle->genParticles[g].lv;
      fillHist("genbPt", genb2.Pt());
      fillHist("genbEta", genb2.Eta());
      fillHist("genbPhi", genb2.Phi());
    }
    //********** gen Z *********
    if (std::abs(HbbHandle->genParticles[g].pdgId) == 23 && std::abs(HbbHandle->genParticles[g].daughterIds[0]) == 13) {
      genZ = HbbHandle->genParticles[g].lv;
      fillHist("genZM", genZ.M());
      fillHist("genZPt", genZ.Pt());
      fillHist("genZEta", genZ.Eta());
      fillHist("genZPhi", genZ.Phi());
    }
    //********** gen muons *********
    if (HbbHandle->genParticles[g].pdgId == 13 && std::abs(HbbHandle->genParticles[g].motherId) == 23) {
      genmuon1 = HbbHandle->genParticles[g].lv;
      fillHist("genmuonPt", genmuon1.Pt());
      fillHist("genmuonEta", genmuon1.Eta());
      fillHist("genmuonPhi", genmuon1.Phi());
    }
    if (HbbHandle->genParticles[g].pdgId == -13 && std::abs(HbbHandle->genParticles[g].motherId) == 23) {
      genmuon2 = HbbHandle->genParticles[g].lv;
      fillHist("genmuonPt", genmuon2.Pt());
      fillHist("genmuonEta", genmuon2.Eta());
      fillHist("genmuonPhi", genmuon2.Phi());
    }
  }

  if (genZ.Pt() > 150) {
    fillHist("genmuonPt_150", genmuon1.Pt());
    fillHist("genmuonPt_150", genmuon2.Pt());
    fillHist("genbPt_150", genb1.Pt());
    fillHist("genbPt_150", genb2.Pt());
  }
  fillHist("gendeltaPhiZH", std::abs(genHiggs.DeltaPhi(genZ)));
  fillHist("gendeltaRbb", genb1.DeltaR(genb2));
  if (genb1.Pt() > 20 && genb2.Pt() > 20 && std::abs(genb1.Eta()) < 2.5 && std::abs(genb2.Eta()) < 2.5) {
    if (genZ.Pt() > 0) fillHist("gendeltaRbb_cuts", genb1.DeltaR(genb2));
    if (genZ.Pt() > 150) fillHist("gendeltaRbb_cuts150", genb1.DeltaR(genb2));
    if (genZ.Pt() > 300) fillHist("gendeltaRbb_cuts300", genb1.DeltaR(genb2));
  }
  if (genZ.Pt() > 150 && genmuon1.Pt() > 20 && genmuon2.Pt() > 20 && std::abs(genmuon1.Eta()) < 2.4 && std::abs(genmuon2.Eta()) < 2.4 && genZ.M() > 75 && genZ.M() < 105 && (std::abs(genmuon1.Eta()) < 1.44 || std::abs(genmuon1.Eta()) > 1.57) && (std::abs(genmuon2.Eta()) < 1.44 || std::abs(genmuon2.Eta()) > 1.57) && genb1.Pt() > 20 && genb2.Pt() > 20 && std::abs(genb1.Eta()) < 2.5 && std::abs(genb2.Eta()) < 2.5 && genHiggs.M() < 250 && std::abs(genHiggs.DeltaPhi(genZ)) > 2.8) {
    fillHist("genHPt_allcuts", genHiggs.Pt());
    fillHist("genHM_allcuts", genHiggs.M());
    fillHist("genZPt_allcuts", genZ.Pt());
    fillHist("genZM_allcuts", genZ.M());
  }
  if (genmuon1.Pt() > 20 && genmuon2.Pt() > 20 && std::abs(genmuon1.Eta()) < 2.4 && std::abs(genmuon2.Eta()) < 2.4 && genZ.M() > 75 && genZ.M() < 105 && (std::abs(genmuon1.Eta()) < 1.44 || std::abs(genmuon1.Eta()) > 1.57) && (std::abs(genmuon2.Eta()) < 1.44 || std::abs(genmuon2.Eta()) > 1.57)) {
    fillHist("genZPt_goodZcuts", genZ.Pt());
    fillHist("genZM_goodZcuts", genZ.M());
    if (HbbHandle->Muons.size()>1) {
      if (GoodLeptons && ZBoson.Pt() > 150) fillHist("genZPt_recoZ", genZ.Pt());
    }
  }
  
  if (HbbHandle->Muons.size() > 1 && GoodLeptons && genb1.Pt() > 20 && genb2.Pt() > 20 && std::abs(genb1.Eta()) < 2.5 && std::abs(genb2.Eta()) < 2.5 && genHiggs.M() < 250) {
    fillHist("genHPt_hcuts", genHiggs.Pt());
  }

  //******** Jets ***************************
  double deltaPhi = 0.0;
  for (auto rads =std::begin(algo); rads != std::end(algo); ++rads) {
    if (jetmap[*rads].size() > 0 && HbbHandle->Muons.size() > 1) {
      if (*rads == "AK4") {
	TLorentzVector higgs; TLorentzVector b1; TLorentzVector b2;
	if (jetmap[*rads].size() > 1) {
	  higgs = jetmap[*rads][0].lv+jetmap[*rads][1].lv;
	  b1 = jetmap[*rads][0].lv;
	  b2 = jetmap[*rads][1].lv;
	  deltaPhi = std::abs(higgs.DeltaPhi(ZBoson));
	  fillHist("HiggsM_nocuts_" + *rads, higgs.M());
	  fillHist("HiggsPt_nocuts_" + *rads, higgs.Pt());
	  fillHist("j1Pt_nocuts_" + *rads, b1.Pt());
	  fillHist("j2Pt_nocuts_" + *rads, b2.Pt());
	  fillHist("j1Eta_nocuts_" + *rads, b1.Eta());
	  fillHist("j2Eta_nocuts_" + *rads, b2.Eta());
	  fillHist("deltaRbb_nocuts_" + *rads, std::abs(b1.DeltaR(b2)));
	  if (higgs.M() < 250) fillHist("HiggsPt_onlymcut_" + *rads, higgs.Pt());
	  if (GoodLeptons && ZBoson.Pt() > 150 && b1.Pt() > 20 && b2.Pt() > 20 && std::abs(b1.Eta()) < 2.5 && std::abs(b2.Eta()) < 2.5 && higgs.M() < 250) {
	    fillHist("HiggsM_bdtcuts_" + *rads, higgs.M());
	    fillHist("ZBosonPt_bdtcuts_" + *rads, ZBoson.Pt());
	    fillHist("HiggsPt_bdtcuts_" + *rads, higgs.Pt());
	    fillHist("j1Pt_bdtcuts_" + *rads, b1.Pt());
	    fillHist("j2Pt_bdtcuts_" + *rads, b2.Pt());
	    fillHist("j1Eta_bdtcuts_" + *rads, b1.Eta());
	    fillHist("j2Eta_bdtcuts_" + *rads, b2.Eta());
	    fillHist("deltaRbb_bdtcuts_" + *rads, std::abs(b1.DeltaR(b2)));
	  }
	  if (GoodLeptons && b1.Pt() > 20 && b2.Pt() > 20 && std::abs(b1.Eta()) < 2.5 && std::abs(b2.Eta()) < 2.5 && higgs.M() < 250 && deltaPhi > 2.8) {
	    if (ZBoson.Pt() > 150) {
	      fillHist("HiggsM_" + *rads, higgs.M());
	      fillHist("HiggsPt_" + *rads, higgs.Pt());
	      fillHist("ZBosonPt_" + *rads, ZBoson.Pt());
	      fillHist("HiggsEta_" + *rads, higgs.Eta());
	      fillHist("HiggsPhi_" + *rads, higgs.Phi());
	      fillHist("j1Pt_"+ *rads, b1.Pt());
	      fillHist("j2Pt_"+ *rads, b2.Pt());
	      fillHist("j1Eta_"+ *rads, b1.Eta());
	      fillHist("j2Eta_"+ *rads, b2.Eta());
	      fillHist("j1Phi_"+ *rads, b1.Phi());
	      fillHist("j2Phi_"+ *rads, b2.Phi());
	      fillHist("deltaRbb_" + *rads, std::abs(b1.DeltaR(b2)));
	    }
	    if (ZBoson.Pt() > 200) {
	      fillHist("HiggsM_200cuts_" + *rads, higgs.M());
	      fillHist("HiggsPt_200cuts_" + *rads, higgs.Pt());
	      fillHist("ZBosonPt_200cuts_" + *rads, ZBoson.Pt());
	      fillHist("j1Pt_200cuts_" + *rads, b1.Pt());
	      fillHist("j2Pt_200cuts_" + *rads, b2.Pt());
	      fillHist("deltaRbb_200cuts_" + *rads, std::abs(b1.DeltaR(b2)));
	    }
	    if (ZBoson.Pt() > 300) {
	      fillHist("HiggsM_300cuts_" + *rads, higgs.M());
	      fillHist("HiggsPt_300cuts_" + *rads, higgs.Pt());
	      fillHist("ZBosonPt_300cuts_" + *rads, ZBoson.Pt());
	      fillHist("j1Pt_300cuts_" + *rads, b1.Pt());
	      fillHist("j2Pt_300cuts_" + *rads, b2.Pt());
	      fillHist("deltaRbb_300cuts_" + *rads, std::abs(b1.DeltaR(b2)));
	    }
	    if (ZBoson.Pt() > 150 && higgs.M() > 70 && higgs.M() < 150) {
	      fillHist("HiggsM_150masscuts_" + *rads, higgs.M());
	      fillHist("HiggsPt_150masscuts_" + *rads, higgs.Pt());
	      fillHist("ZBosonPt_150masscuts_" + *rads, ZBoson.Pt());
	      fillHist("j1Pt_150masscuts_"+ *rads, b1.Pt());
	      fillHist("j2Pt_150masscuts_"+ *rads, b2.Pt());
	      fillHist("deltaRbb_150masscuts_" + *rads, std::abs(b1.DeltaR(b2)));
	    }
	    if (ZBoson.Pt() > 200 && higgs.M() > 70 && higgs.M() < 150) {
	      fillHist("HiggsM_200masscuts_" + *rads, higgs.M());
	      fillHist("HiggsPt_200masscuts_" + *rads, higgs.Pt());
	      fillHist("ZBosonPt_200masscuts_" + *rads, ZBoson.Pt());
	      fillHist("j1Pt_200masscuts_" + *rads, b1.Pt());
	      fillHist("j2Pt_200masscuts_" + *rads, b2.Pt());
	      fillHist("deltaRbb_200masscuts_" + *rads, std::abs(b1.DeltaR(b2)));
	    }
	    if (ZBoson.Pt() > 300 && higgs.M() > 70 && higgs.M() < 150) {
	      fillHist("HiggsM_300masscuts_" + *rads, higgs.M());
	      fillHist("HiggsPt_300masscuts_" + *rads, higgs.Pt());
	      fillHist("ZBosonPt_300masscuts_" + *rads, ZBoson.Pt());
	      fillHist("j1Pt_300masscuts_" + *rads, b1.Pt());
	      fillHist("j2Pt_300masscuts_" + *rads, b2.Pt());
	      fillHist("deltaRbb_300masscuts_" + *rads, std::abs(b1.DeltaR(b2)));
	    }
	  }
	  if (GoodLeptons && genb1.Pt() > 20 && genb2.Pt() > 20 && std::abs(genb1.Eta()) < 2.5 && std::abs(genb2.Eta()) < 2.5 && genHiggs.M() < 250 && b1.Pt() > 20 && b2.Pt() > 20 && std::abs(b1.Eta()) < 2.5 && std::abs(b2.Eta()) < 2.5 && higgs.M() < 250 && higgs.M() > 50 && deltaPhi > 2.8) {
	    if (higgs.Pt() > 150) fillHist("genHPt_recoH_150_" + *rads, genHiggs.Pt());
	    if (higgs.Pt() > 200) fillHist("genHPt_recoH_200_" + *rads, genHiggs.Pt());
	    if (higgs.Pt() > 300) fillHist("genHPt_recoH_300_" + *rads, genHiggs.Pt());
	    if (higgs.M() > 70 && higgs.M() < 150) {
	      if (higgs.Pt() > 150) fillHist("genHPt_recoH_tightm150_" + *rads, genHiggs.Pt());
	      if (higgs.Pt() > 200) fillHist("genHPt_recoH_tightm200_" + *rads, genHiggs.Pt());
	      if (higgs.Pt() > 300) fillHist("genHPt_recoH_tightm300_" + *rads, genHiggs.Pt());
	    }
	  }
	}
      }
      else { // fat jet grooming
	if (GoodLeptons) {
	    fillHist("tau1_nocuts_" + *rads, jetmap[*rads][0].tau1);
	    fillHist("tau2_nocuts_" + *rads, jetmap[*rads][0].tau2);
	    fillHist("tau3_nocuts_" + *rads, jetmap[*rads][0].tau3);
	    fillHist("HiggsM_nocuts_ungr_" + *rads, jetmap[*rads][0].lv.M());
	    fillHist("HiggsPt_nocuts_ungr_" + *rads, jetmap[*rads][0].lv.Pt());
	    if (jetmap[*rads][0].lv.M() < 250 && jetmap[*rads][0].lv.Eta() < 2.5 && ZBoson.Pt() > 150)  {
	      fillHist("tau1_150cut_" + *rads, jetmap[*rads][0].tau1);
	      fillHist("tau2_150cut_" + *rads, jetmap[*rads][0].tau2);
	      fillHist("tau3_150cut_" + *rads, jetmap[*rads][0].tau3);
	      fillHist("HiggsM_150cut_ungr_" + *rads, jetmap[*rads][0].lv.M());
	      fillHist("HiggsPt_150cut_ungr_" + *rads, jetmap[*rads][0].lv.Pt());
	      if (jetmap[*rads][0].lv.M() > 50){
		fillHist("tau1_150masscut_" + *rads, jetmap[*rads][0].tau1);
		fillHist("tau2_150masscut_" + *rads, jetmap[*rads][0].tau2);
		fillHist("tau3_150masscut_" + *rads, jetmap[*rads][0].tau3);
		fillHist("HiggsM_150masscut_ungr_" + *rads, jetmap[*rads][0].lv.M());
		fillHist("HiggsPt_150masscut_ungr_" + *rads, jetmap[*rads][0].lv.Pt());
	      }
	    }
	    if (jetmap[*rads][0].lv.M() < 250 && jetmap[*rads][0].lv.Eta() < 2.5 && ZBoson.Pt() > 200)  {
	      fillHist("tau1_200cut_" + *rads, jetmap[*rads][0].tau1);
	      fillHist("tau2_200cut_" + *rads, jetmap[*rads][0].tau2);
	      fillHist("tau3_200cut_" + *rads, jetmap[*rads][0].tau3);
	      fillHist("HiggsM_200cut_ungr_" + *rads, jetmap[*rads][0].lv.M());
	      fillHist("HiggsPt_200cut_ungr_" + *rads, jetmap[*rads][0].lv.Pt());
	      if (jetmap[*rads][0].lv.M() > 50){
		fillHist("tau1_200masscut_" + *rads, jetmap[*rads][0].tau1);
		fillHist("tau2_200masscut_" + *rads, jetmap[*rads][0].tau2);
		fillHist("tau3_200masscut_" + *rads, jetmap[*rads][0].tau3);
		fillHist("HiggsM_200masscut_ungr_" + *rads, jetmap[*rads][0].lv.M());
		fillHist("HiggsPt_200masscut_ungr_" + *rads, jetmap[*rads][0].lv.Pt());
	      }
	    }
	    if (jetmap[*rads][0].lv.M() < 250 && jetmap[*rads][0].lv.Eta() < 2.5 && ZBoson.Pt() > 300)  {
	      fillHist("tau1_300cut_" + *rads, jetmap[*rads][0].tau1);
	      fillHist("tau2_300cut_" + *rads, jetmap[*rads][0].tau2);
	      fillHist("tau3_300cut_" + *rads, jetmap[*rads][0].tau3);
	      fillHist("HiggsM_300cut_ungr_" + *rads, jetmap[*rads][0].lv.M());
	      fillHist("HiggsPt_300cut_ungr_" + *rads, jetmap[*rads][0].lv.Pt());
	      if (jetmap[*rads][0].lv.M() > 50){
		fillHist("tau1_300masscut_" + *rads, jetmap[*rads][0].tau1);
		fillHist("tau2_300masscut_" + *rads, jetmap[*rads][0].tau2);
		fillHist("tau3_300masscut_" + *rads, jetmap[*rads][0].tau3);
		fillHist("HiggsM_300masscut_ungr_" + *rads, jetmap[*rads][0].lv.M());
		fillHist("HiggsPt_300masscut_ungr_" + *rads, jetmap[*rads][0].lv.Pt());
	      }
	    }
	}
     	for (auto gr =std::begin(groom); gr != std::end(groom); ++gr) {
	  TLorentzVector higgs; TLorentzVector b1; TLorentzVector b2;
     	  if (submap[*rads + *gr].size() > 1) {
	    for(unsigned int fj=0; fj<submap[*rads + *gr].size(); fj++) {
	      higgs = higgs + submap[*rads + *gr][fj].lv;
	    }
	    b1 = submap[*rads + *gr][0].lv;
	    b2 = submap[*rads + *gr][1].lv;
	    deltaPhi = std::abs(higgs.DeltaPhi(ZBoson));
	    fillHist("HiggsM_nocuts_" + *rads + *gr, higgs.M());
	    fillHist("HiggsPt_nocuts_" + *rads + *gr, higgs.Pt());
	    fillHist("j1Pt_nocuts_" + *rads + *gr, b1.Pt());
	    fillHist("j2Pt_nocuts_" + *rads + *gr, b2.Pt());
	    fillHist("j1Eta_nocuts_" + *rads + *gr, b1.Eta());
	    fillHist("j2Eta_nocuts_" + *rads + *gr, b2.Eta());
	    fillHist("deltaRbb_nocuts_" + *rads + *gr, std::abs(b1.DeltaR(b2)));
	    if (higgs.M() < 250) fillHist("HiggsPt_onlymcut_" + *rads + *gr, higgs.Pt());
	    if (GoodLeptons && ZBoson.Pt() > 150 && b1.Pt() > 20 && b2.Pt() > 20 && std::abs(b1.Eta()) < 2.5 && std::abs(b2.Eta()) < 2.5 && higgs.M() < 250) {
	      fillHist("HiggsM_bdtcuts_" + *rads + *gr, higgs.M());
	      fillHist("HiggsPt_bdtcuts_" + *rads + *gr, higgs.Pt());
	      fillHist("ZBosonPt_bdtcuts_" + *rads + *gr, ZBoson.Pt());
	      fillHist("j1Pt_bdtcuts_" + *rads + *gr, b1.Pt());
	      fillHist("j2Pt_bdtcuts_" + *rads + *gr, b2.Pt());
	      fillHist("j1Eta_bdtcuts_" + *rads + *gr, b1.Eta());
	      fillHist("j2Eta_bdtcuts_" + *rads + *gr, b2.Eta());
	      fillHist("deltaRbb_bdtcuts_" + *rads + *gr, std::abs(b1.DeltaR(b2)));
	    }
	    if (GoodLeptons && b1.Pt() > 20 && b2.Pt() > 20 && std::abs(b1.Eta()) < 2.5 && std::abs(b2.Eta()) < 2.5 && higgs.M() < 250 && deltaPhi > 2.8) {
	      if (ZBoson.Pt() > 150) {
		fillHist("HiggsM_" + *rads + *gr, higgs.M());
		fillHist("HiggsPt_" + *rads + *gr, higgs.Pt());
		fillHist("ZBosonPt_" + *rads + *gr, ZBoson.Pt());
		fillHist("HiggsEta_" + *rads + *gr, higgs.Eta());
		fillHist("HiggsPhi_" + *rads + *gr, higgs.Phi());
		fillHist("j1Pt_"+ *rads + *gr, b1.Pt());
		fillHist("j2Pt_"+ *rads + *gr, b2.Pt());
		fillHist("j1Eta_"+ *rads + *gr, b1.Eta());
		fillHist("j2Eta_"+ *rads + *gr, b2.Eta());
		fillHist("j1Phi_"+ *rads + *gr, b1.Phi());
		fillHist("j2Phi_"+ *rads + *gr, b2.Phi());
		fillHist("deltaRbb_" + *rads + *gr, std::abs(b1.DeltaR(b2)));
	      }
	      if (ZBoson.Pt() > 200) {
		fillHist("HiggsM_200cuts_" + *rads + *gr, higgs.M());
		fillHist("HiggsPt_200cuts_" + *rads + *gr, higgs.Pt());
		fillHist("ZBosonPt_200cuts_" + *rads + *gr, ZBoson.Pt());
		fillHist("j1Pt_200cuts_" + *rads + *gr, b1.Pt());
		fillHist("j2Pt_200cuts_" + *rads + *gr, b2.Pt());
		fillHist("deltaRbb_200cuts_" + *rads + *gr, std::abs(b1.DeltaR(b2)));
	      }
	      if (ZBoson.Pt() > 300) {
		fillHist("HiggsM_300cuts_" + *rads + *gr, higgs.M());
		fillHist("HiggsPt_300cuts_" + *rads + *gr, higgs.Pt());
		fillHist("ZBosonPt_300cuts_" + *rads + *gr, ZBoson.Pt());
		fillHist("j1Pt_300cuts_" + *rads + *gr, b1.Pt());
		fillHist("j2Pt_300cuts_" + *rads + *gr, b2.Pt());
		fillHist("deltaRbb_300cuts_" + *rads + *gr, std::abs(b1.DeltaR(b2)));
	      }
	      if (ZBoson.Pt() > 150 && higgs.M() > 70 && higgs.M() < 150) {
		fillHist("HiggsM_150masscuts_" + *rads + *gr, higgs.M());
		fillHist("HiggsPt_150masscuts_" + *rads + *gr, higgs.Pt());
		fillHist("ZBosonPt_150masscuts_" + *rads + *gr, ZBoson.Pt());
		fillHist("j1Pt_150masscuts_"+ *rads + *gr, b1.Pt());
		fillHist("j2Pt_150masscuts_"+ *rads + *gr, b2.Pt());
		fillHist("deltaRbb_150masscuts_" + *rads + *gr, std::abs(b1.DeltaR(b2)));
	      }
	      if (ZBoson.Pt() > 200 && higgs.M() > 70 && higgs.M() < 150) {
		fillHist("HiggsM_200masscuts_" + *rads + *gr, higgs.M());
		fillHist("HiggsPt_200masscuts_" + *rads + *gr, higgs.Pt());
		fillHist("ZBosonPt_200masscuts_" + *rads + *gr, ZBoson.Pt());
		fillHist("j1Pt_200masscuts_" + *rads + *gr, b1.Pt());
		fillHist("j2Pt_200masscuts_" + *rads + *gr, b2.Pt());
		fillHist("deltaRbb_200masscuts_" + *rads + *gr, std::abs(b1.DeltaR(b2)));
	      }
	      if (ZBoson.Pt() > 300 && higgs.M() > 70 && higgs.M() < 150) {
		fillHist("HiggsM_300masscuts_" + *rads + *gr, higgs.M());
		fillHist("HiggsPt_300masscuts_" + *rads + *gr, higgs.Pt());
		fillHist("ZBosonPt_300masscuts_" + *rads + *gr, ZBoson.Pt());
		fillHist("j1Pt_300masscuts_" + *rads + *gr, b1.Pt());
		fillHist("j2Pt_300masscuts_" + *rads + *gr, b2.Pt());
		fillHist("deltaRbb_300masscuts_" + *rads + *gr, std::abs(b1.DeltaR(b2)));
	      }
	    }
	    if (GoodLeptons && genb1.Pt() > 20 && genb2.Pt() > 20 && std::abs(genb1.Eta()) < 2.5 && std::abs(genb2.Eta()) < 2.5 && genHiggs.M() < 250 && b1.Pt() > 20 && b2.Pt() > 20 && std::abs(b1.Eta()) < 2.5 && std::abs(b2.Eta()) < 2.5 && higgs.M() < 250 && higgs.M() > 50 && deltaPhi > 2.8) {
	      if (higgs.Pt() > 150) fillHist("genHPt_recoH_150_" + *rads + *gr, genHiggs.Pt());
	      if (higgs.Pt() > 200) fillHist("genHPt_recoH_200_" + *rads + *gr, genHiggs.Pt());
	      if (higgs.Pt() > 300) fillHist("genHPt_recoH_300_" + *rads + *gr, genHiggs.Pt());
	      if (higgs.M() > 70 && higgs.M() < 150) {
		if (higgs.Pt() > 150) fillHist("genHPt_recoH_tightm150_" + *rads + *gr, genHiggs.Pt());
		if (higgs.Pt() > 200) fillHist("genHPt_recoH_tightm200_" + *rads + *gr, genHiggs.Pt());
		if (higgs.Pt() > 300) fillHist("genHPt_recoH_tightm300_" + *rads + *gr, genHiggs.Pt());
	      }
	    }
     	  }  //if more than one subjet
     	} //Loop over grooming techniques
     }  //Fat jet section
     
    } //If more than zero (fat) jets in the event
  } //Loop over radii
  
#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
  ESHandle<SetupData> pSetup;
  iSetup.get<SetupRecord>().get(pSetup);
#endif
}

void
GroomHbbAnalyzer::fillHist(const TString& histName, const Double_t& value, const Double_t& wt) {

  hid=m_HistNames.find(histName);
  if (hid==m_HistNames.end())
    std::cout << "%fillHist -- Could not find histogram with name: " << histName << std::endl;
  else
    hid->second->Fill(value,wt); 

}

void
GroomHbbAnalyzer::bookHistograms() {
  
  edm::Service<TFileService> fs;
  if (!fs) throw edm::Exception(edm::errors::Configuration,
                                "TFileService missing from configuration!");

  TString hname, htitle;

  TFileDirectory ZDir = fs->mkdir("ZBoson");
  hname= "ZM";
  htitle="ZM";
  m_HistNames[hname] = ZDir.make<TH1D>(hname,htitle,260,0.0,260.);
  hname= "ZEta";
  htitle="ZEta";
  m_HistNames[hname] = ZDir.make<TH1D>(hname,htitle,100,-5.,5.);
  hname= "ZPhi";
  htitle="ZPhi";
  m_HistNames[hname] = ZDir.make<TH1D>(hname,htitle,60,-TMath::Pi(),TMath::Pi());
  hname= "ZPt";
  htitle="ZPt";
  m_HistNames[hname] = ZDir.make<TH1D>(hname,htitle,200,0,1000);
  hname= "ZPt_150";
  htitle="ZPt_150";
  m_HistNames[hname] = ZDir.make<TH1D>(hname,htitle,200,0,1000);
  hname= "ZPt_200";
  htitle="ZPt_200";
  m_HistNames[hname] = ZDir.make<TH1D>(hname,htitle,200,0,1000);
  hname= "ZPt_300";
  htitle="ZPt_300";
  m_HistNames[hname] = ZDir.make<TH1D>(hname,htitle,200,0,1000);
  hname= "ZPt_onlymcut";
  htitle="ZPt_onlymcut";
  m_HistNames[hname] = ZDir.make<TH1D>(hname,htitle,200,0,1000);
  hname= "muon1Pt";
  htitle="muon1Pt";
  m_HistNames[hname] = ZDir.make<TH1D>(hname,htitle,200,0,1000);
  hname= "muon2Pt";
  htitle="muon2Pt";
  m_HistNames[hname] = ZDir.make<TH1D>(hname,htitle,200,0,1000);
  hname= "muon1Eta";
  htitle="muon1Eta";
  m_HistNames[hname] = ZDir.make<TH1D>(hname,htitle,100,-5.,5.);
  hname= "muon2Eta";
  htitle="muon2Eta";
  m_HistNames[hname] = ZDir.make<TH1D>(hname,htitle,100,-5.,5.);
  hname= "muon1Phi";
  htitle="muon1Phi";
  m_HistNames[hname] = ZDir.make<TH1D>(hname,htitle,60,-TMath::Pi(),TMath::Pi());
  hname= "muon2Phi";
  htitle="muon2Phi";
  m_HistNames[hname] = ZDir.make<TH1D>(hname,htitle,60,-TMath::Pi(),TMath::Pi());
  
  TFileDirectory genDir = fs->mkdir("genParticles");
  hname= "genZM";
  htitle="genZM";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,260,0.0,260.);
  hname= "genZM_allcuts";
  htitle="genZM_allcuts";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,260,0.0,260.);
  hname= "genZM_goodZcuts";
  htitle="genZM_goodZcuts";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,260,0.0,260.);
  hname= "genZPt";
  htitle="genZPt";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,200,0,1000);
  hname= "genZPt_allcuts";
  htitle="genZPt_allcuts";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,200,0,1000);
  hname= "genZPt_goodZcuts";
  htitle="genZPt_goodZcuts";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,200,0,1000);
  hname= "genZPt_recoZ";
  htitle="genZPt_recoZ";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,200,0,1000);
  hname= "genZEta";
  htitle="genZEta";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,100,-5.,5.);
  hname= "genZPhi";
  htitle="genZPhi";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,60,-TMath::Pi(),TMath::Pi());
  hname= "genmuonPt";
  htitle="genmuonPt";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,200,0,1000);
  hname= "genmuonPt_150";
  htitle="genmuonPt_150";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,200,0,1000);
  hname= "genmuonEta";
  htitle="genmuonEta";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,100,-5.,5.);
  hname= "genmuonPhi";
  htitle="genmuonPhi";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,60,-TMath::Pi(),TMath::Pi());

  hname= "genHM";
  htitle="genHM";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,260,0.0,260.);
  hname= "genHM_allcuts";
  htitle="genHM_allcuts";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,260,0.0,260.);
  hname= "genHPt";
  htitle="genHPt";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,200,0,1000);
  hname= "genHPt_onlymuons";
  htitle="genHPt_onlymuons";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,200,0,1000);
  hname= "genHPt_allcuts";
  htitle="genHPt_allcuts";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,200,0,1000);
  hname= "genHPt_hcuts";
  htitle="genHPt_hcuts";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,200,0,1000);
  hname= "genHEta";
  htitle="genHEta";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,100,-5.,5.);
  hname= "genHPhi";
  htitle="genHPhi";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,60,-TMath::Pi(),TMath::Pi());
  hname= "genbPt";
  htitle="genbPt";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,200,0,1000);
  hname= "genbPt_150";
  htitle="genbPt_150";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,200,0,1000);
  hname= "genbEta";
  htitle="genbEta";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,100,-5.,5.);
  hname= "genbPhi";
  htitle="genbPhi";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,60,-TMath::Pi(),TMath::Pi());

  hname= "gendeltaPhiZH";
  htitle="gendeltaPhiZH";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,60,0.0,TMath::Pi());
  hname= "gendeltaRbb";
  htitle="gendeltaRbb";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,60,0.0,6.0);
  hname= "gendeltaRbb_cuts";
  htitle="gendeltaRbb_cuts";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,60,0.0,6.0);
  hname= "gendeltaRbb_cuts150";
  htitle="gendeltaRbb_cuts150";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,60,0.0,6.0);
  hname= "gendeltaRbb_cuts300";
  htitle="gendeltaRbb_cuts300";
  m_HistNames[hname] = genDir.make<TH1D>(hname,htitle,60,0.0,6.0);


  for (auto rads =std::begin(algo); rads != std::end(algo); ++rads) {  
    
    if (*rads == "AK4") {
      TFileDirectory subDir = fs->mkdir(*rads);
      hname= "HiggsM_" + *rads;
      htitle="HiggsM_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,260,0.0,260.);
      hname= "HiggsM_nocuts_" + *rads;
      htitle="HiggsM_nocuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,260,0.0,260.);
      hname= "HiggsM_bdtcuts_" + *rads;
      htitle="HiggsM_bdtcuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,260,0.0,260.);
      hname= "HiggsPt_" + *rads;
      htitle="HiggsPt_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "HiggsPt_nocuts_" + *rads;
      htitle="HiggsPt_nocuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "HiggsPt_bdtcuts_" + *rads;
      htitle="HiggsPt_bdtcuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "ZBosonPt_" + *rads;
      htitle="ZBosonPt_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "ZBosonPt_bdtcuts_" + *rads;
      htitle="ZBosonPt_bdtcuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "HiggsPt_onlymcut_" + *rads;
      htitle="HiggsPt_onlymcut_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "genHPt_recoH_150_" + *rads;
      htitle="genHPt_recoH_150_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "genHPt_recoH_200_" + *rads;
      htitle="genHPt_recoH_200_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "genHPt_recoH_300_" + *rads;
      htitle="genHPt_recoH_300_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "genHPt_recoH_tightm150_" + *rads;
      htitle="genHPt_recoH_tightm150_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "genHPt_recoH_tightm200_" + *rads;
      htitle="genHPt_recoH_tightm200_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "genHPt_recoH_tightm300_" + *rads;
      htitle="genHPt_recoH_tightm300_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "HiggsEta_" + *rads;
      htitle="HiggsEta_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,-5.0,5.0);
      hname= "HiggsPhi_" + *rads;
      htitle="HiggsPhi_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,60,-TMath::Pi(),TMath::Pi());
      hname= "j1Pt_" + *rads;
      htitle="j1Pt_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "j2Pt_" + *rads;
      htitle="j2Pt_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "j1Pt_nocuts_" + *rads;
      htitle="j1Pt_nocuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "j2Pt_nocuts_" + *rads;
      htitle="j2Pt_nocuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "j1Pt_bdtcuts_" + *rads;
      htitle="j1Pt_bdtcuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "j2Pt_bdtcuts_" + *rads;
      htitle="j2Pt_bdtcuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "j1Eta_" + *rads;
      htitle="j1Eta_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,-5.0,5.0);
      hname= "j2Eta_" + *rads;
      htitle="j2Eta_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,-5.0,5.0);
      hname= "j1Eta_nocuts_" + *rads;
      htitle="j1Eta_nocuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,-5.0,5.0);
      hname= "j2Eta_nocuts_" + *rads;
      htitle="j2Eta_nocuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,-5.0,5.0);
      hname= "j1Eta_bdtcuts_" + *rads;
      htitle="j1Eta_bdtcuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,-5.0,5.0);
      hname= "j2Eta_bdtcuts_" + *rads;
      htitle="j2Eta_bdtcuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,-5.0,5.0);
      hname= "j1Phi_" + *rads;
      htitle="j1Phi_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,60,-TMath::Pi(),TMath::Pi());
      hname= "j2Phi_" + *rads;
      htitle="j2Phi_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,60,-TMath::Pi(),TMath::Pi());
      hname= "deltaRbb_" + *rads;
      htitle="deltaRbb_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,600,0.0,6.0);
      hname= "deltaRbb_nocuts_" + *rads;
      htitle="deltaRbb_nocuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,600,0.0,6.0);
      hname= "deltaRbb_bdtcuts_" + *rads;
      htitle="deltaRbb_bdtcuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,600,0.0,6.0);
      hname= "HiggsM_200cuts_" + *rads;
      htitle="HiggsM_200cuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,260,0.0,260.);
      hname= "HiggsPt_200cuts_" + *rads;
      htitle="HiggsPt_200cuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "ZBosonPt_200cuts_" + *rads;
      htitle="ZBosonPt_200cuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "j1Pt_200cuts_" + *rads;
      htitle="j1Pt_200cuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "j2Pt_200cuts_" + *rads;
      htitle="j2Pt_200cuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "deltaRbb_200cuts_" + *rads;
      htitle="deltaRbb_200cuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,600,0.0,6.0);
      hname= "HiggsM_300cuts_" + *rads;
      htitle="HiggsM_300cuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,260,0.0,260.);
      hname= "HiggsPt_300cuts_" + *rads;
      htitle="HiggsPt_300cuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "ZBosonPt_300cuts_" + *rads;
      htitle="ZBosonPt_300cuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "j1Pt_300cuts_" + *rads;
      htitle="j1Pt_300cuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "j2Pt_300cuts_" + *rads;
      htitle="j2Pt_300cuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "deltaRbb_300cuts_" + *rads;
      htitle="deltaRbb_300cuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,600,0.0,6.0);
      hname= "HiggsM_150masscuts_" + *rads;
      htitle="HiggsM_150masscuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,260,0.0,260.);
      hname= "HiggsPt_150masscuts_" + *rads;
      htitle="HiggsPt_150masscuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "ZBosonPt_150masscuts_" + *rads;
      htitle="ZBosonPt_150masscuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "j1Pt_150masscuts_" + *rads;
      htitle="j1Pt_150masscuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "j2Pt_150masscuts_" + *rads;
      htitle="j2Pt_150masscuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "deltaRbb_150masscuts_" + *rads;
      htitle="deltaRbb_150masscuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,600,0.0,6.0);
      hname= "HiggsM_200masscuts_" + *rads;
      htitle="HiggsM_200masscuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,260,0.0,260.);
      hname= "HiggsPt_200masscuts_" + *rads;
      htitle="HiggsPt_200masscuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "ZBosonPt_200masscuts_" + *rads;
      htitle="ZBosonPt_200masscuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "j1Pt_200masscuts_" + *rads;
      htitle="j1Pt_200masscuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "j2Pt_200masscuts_" + *rads;
      htitle="j2Pt_200masscuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "deltaRbb_200masscuts_" + *rads;
      htitle="deltaRbb_200masscuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,600,0.0,6.0);
      hname= "HiggsM_300masscuts_" + *rads;
      htitle="HiggsM_300masscuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,260,0.0,260.);
      hname= "HiggsPt_300masscuts_" + *rads;
      htitle="HiggsPt_300masscuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "ZBosonPt_300masscuts_" + *rads;
      htitle="ZBosonPt_300masscuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "j1Pt_300masscuts_" + *rads;
      htitle="j1Pt_300masscuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "j2Pt_300masscuts_" + *rads;
      htitle="j2Pt_300masscuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "deltaRbb_300masscuts_" + *rads;
      htitle="deltaRbb_300masscuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,600,0.0,6.0);
    }
    else {
      TFileDirectory subDir = fs->mkdir(*rads);
      hname= "tau1_nocuts_" + *rads;
      htitle= "tau1_nocuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "tau2_nocuts_" + *rads;
      htitle= "tau2_nocuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "tau3_nocuts_" + *rads;
      htitle= "tau3_nocuts_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "tau1_150cut_" + *rads;
      htitle= "tau1_150cut_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "tau2_150cut_" + *rads;
      htitle= "tau2_150cut_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "tau3_150cut_" + *rads;
      htitle= "tau3_150cut_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "tau1_200cut_" + *rads;
      htitle= "tau1_200cut_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "tau2_200cut_" + *rads;
      htitle= "tau2_200cut_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "tau3_200cut_" + *rads;
      htitle= "tau3_200cut_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "tau1_300cut_" + *rads;
      htitle= "tau1_300cut_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "tau2_300cut_" + *rads;
      htitle= "tau2_300cut_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "tau3_300cut_" + *rads;
      htitle= "tau3_300cut_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "tau1_150masscut_" + *rads;
      htitle= "tau1_150masscut_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "tau2_150masscut_" + *rads;
      htitle= "tau2_150masscut_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "tau3_150masscut_" + *rads;
      htitle= "tau3_150masscut_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "tau1_200masscut_" + *rads;
      htitle= "tau1_200masscut_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "tau2_200masscut_" + *rads;
      htitle= "tau2_200masscut_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "tau3_200masscut_" + *rads;
      htitle= "tau3_200masscut_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "tau1_300masscut_" + *rads;
      htitle= "tau1_300masscut_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "tau2_300masscut_" + *rads;
      htitle= "tau2_300masscut_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "tau3_300masscut_" + *rads;
      htitle= "tau3_300masscut_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,100,0.0,1.);
      hname= "HiggsM_nocuts_ungr_" + *rads;
      htitle= "HiggsM_nocuts_ungr_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,260,0.0,260.);
      hname= "HiggsPt_nocuts_ungr_" + *rads;
      htitle= "HiggsPt_nocuts_ungr_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "HiggsM_150cut_ungr_" + *rads;
      htitle= "HiggsM_150cut_ungr_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,260,0.0,260.);
      hname= "HiggsPt_150cut_ungr_" + *rads;
      htitle= "HiggsPt_150cut_ungr_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "HiggsM_200cut_ungr_" + *rads;
      htitle= "HiggsM_200cut_ungr_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,260,0.0,260.);
      hname= "HiggsPt_200cut_ungr_" + *rads;
      htitle= "HiggsPt_200cut_ungr_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "HiggsM_300cut_ungr_" + *rads;
      htitle= "HiggsM_300cut_ungr_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,260,0.0,260.);
      hname= "HiggsPt_300cut_ungr_" + *rads;
      htitle= "HiggsPt_300cut_ungr_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "HiggsM_150masscut_ungr_" + *rads;
      htitle= "HiggsM_150masscut_ungr_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,260,0.0,260.);
      hname= "HiggsPt_150masscut_ungr_" + *rads;
      htitle= "HiggsPt_150masscut_ungr_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "HiggsM_200masscut_ungr_" + *rads;
      htitle= "HiggsM_200masscut_ungr_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,260,0.0,260.);
      hname= "HiggsPt_200masscut_ungr_" + *rads;
      htitle= "HiggsPt_200masscut_ungr_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      hname= "HiggsM_300masscut_ungr_" + *rads;
      htitle= "HiggsM_300masscut_ungr_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,260,0.0,260.);
      hname= "HiggsPt_300masscut_ungr_" + *rads;
      htitle= "HiggsPt_300masscut_ungr_" + *rads;
      m_HistNames[hname] = subDir.make<TH1D>(hname,htitle,200,0.0,1000.);
      for (auto gr =std::begin(groom); gr != std::end(groom); ++gr) {  	
    	TFileDirectory ssDir = subDir.mkdir(*gr);
	hname= "HiggsM_" + *rads + *gr;
	htitle="HiggsM_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,260,0.0,260.);
	hname= "HiggsM_nocuts_" + *rads + *gr;
	htitle="HiggsM_nocuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,260,0.0,260.);
	hname= "HiggsPt_" + *rads + *gr;
	htitle="HiggsPt_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "HiggsPt_nocuts_" + *rads + *gr;
	htitle="HiggsPt_nocuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "HiggsM_bdtcuts_" + *rads + *gr;
	htitle="HiggsM_bdtcuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,260,0.0,260.);
	hname= "HiggsPt_bdtcuts_" + *rads + *gr;
	htitle="HiggsPt_bdtcuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "ZBosonPt_" + *rads + *gr;
	htitle="ZBosonPt_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "ZBosonPt_bdtcuts_" + *rads + *gr;
	htitle="ZBosonPt_bdtcuts" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "HiggsPt_onlymcut_" + *rads + *gr;
	htitle="HiggsPt_onlymcut_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "genHPt_recoH_150_" + *rads + *gr;
	htitle="genHPt_recoH_150_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "genHPt_recoH_200_" + *rads + *gr;
	htitle="genHPt_recoH_200_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "genHPt_recoH_300_" + *rads + *gr;
	htitle="genHPt_recoH_300_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "genHPt_recoH_tightm150_" + *rads + *gr;
	htitle="genHPt_recoH_tightm150_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "genHPt_recoH_tightm200_" + *rads + *gr;
	htitle="genHPt_recoH_tightm200_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "genHPt_recoH_tightm300_" + *rads + *gr;
	htitle="genHPt_recoH_tightm300_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "HiggsEta_" + *rads + *gr;
	htitle="HiggsEta_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,100,-5.0,5.0);
	hname= "HiggsPhi_" + *rads + *gr;
	htitle="HiggsPhi_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,60,-TMath::Pi(),TMath::Pi());
	hname= "j1Pt_" + *rads + *gr;
	htitle="j1Pt_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "j2Pt_" + *rads + *gr;
	htitle="j2Pt_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "j1Pt_nocuts_" + *rads + *gr;
	htitle="j1Pt_nocuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "j2Pt_nocuts_" + *rads + *gr;
	htitle="j2Pt_nocuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "j1Pt_bdtcuts_" + *rads + *gr;
	htitle="j1Pt_bdtcuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "j2Pt_bdtcuts_" + *rads + *gr;
	htitle="j2Pt_bdtcuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "j1Eta_" + *rads + *gr;
	htitle="j1Eta_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,100,-5.0,5.0);
	hname= "j2Eta_" + *rads + *gr;
	htitle="j2Eta_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,100,-5.0,5.0);
	hname= "j1Eta_nocuts_" + *rads + *gr;
	htitle="j1Eta_nocuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,100,-5.0,5.0);
	hname= "j2Eta_nocuts_" + *rads + *gr;
	htitle="j2Eta_nocuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,100,-5.0,5.0);
	hname= "j1Eta_bdtcuts_" + *rads + *gr;
	htitle="j1Eta_bdtcuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,100,-5.0,5.0);
	hname= "j2Eta_bdtcuts_" + *rads + *gr;
	htitle="j2Eta_bdtcuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,100,-5.0,5.0);
	hname= "j1Phi_" + *rads + *gr;
	htitle="j1Phi_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,60,-TMath::Pi(),TMath::Pi());
	hname= "j2Phi_" + *rads + *gr;
	htitle="j2Phi_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,60,-TMath::Pi(),TMath::Pi());
	hname= "deltaRbb_" + *rads + *gr;
	htitle="deltaRbb_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,600,0.0,6.0);
	hname= "deltaRbb_nocuts_" + *rads + *gr;
	htitle="deltaRbb_nocuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,600,0.0,6.0);
	hname= "deltaRbb_bdtcuts_" + *rads + *gr;
	htitle="deltaRbb_bdtcuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,600,0.0,6.0);
	hname= "HiggsM_200cuts_" + *rads + *gr;
	htitle="HiggsM_200cuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,260,0.0,260.);
	hname= "HiggsPt_200cuts_" + *rads + *gr;
	htitle="HiggsPt_200cuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "ZBosonPt_200cuts_" + *rads + *gr;
	htitle="ZBosonPt_200cuts" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "j1Pt_200cuts_" + *rads + *gr;
	htitle="j1Pt_200cuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "j2Pt_200cuts_" + *rads + *gr;
	htitle="j2Pt_200cuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "deltaRbb_200cuts_" + *rads + *gr;
	htitle="deltaRbb_200cuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,600,0.0,6.0);
	hname= "HiggsM_300cuts_" + *rads + *gr;
	htitle="HiggsM_300cuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,260,0.0,260.);
	hname= "HiggsPt_300cuts_" + *rads + *gr;
	htitle="HiggsPt_300cuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "ZBosonPt_300cuts_" + *rads + *gr;
	htitle="ZBosonPt_300cuts" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "j1Pt_300cuts_" + *rads + *gr;
	htitle="j1Pt_300cuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "j2Pt_300cuts_" + *rads + *gr;
	htitle="j2Pt_300cuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "deltaRbb_300cuts_" + *rads + *gr;
	htitle="deltaRbb_300cuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,600,0.0,6.0);
	hname= "HiggsM_150masscuts_" + *rads + *gr;
	htitle="HiggsM_150masscuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,260,0.0,260.);
	hname= "HiggsPt_150masscuts_" + *rads + *gr;
	htitle="HiggsPt_150masscuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "ZBosonPt_150masscuts_" + *rads + *gr;
	htitle="ZBosonPt_150masscuts" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "j1Pt_150masscuts_" + *rads + *gr;
	htitle="j1Pt_150masscuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "j2Pt_150masscuts_" + *rads + *gr;
	htitle="j2Pt_150masscuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "deltaRbb_150masscuts_" + *rads + *gr;
	htitle="deltaRbb_150masscuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,600,0.0,6.0);
	hname= "HiggsM_200masscuts_" + *rads + *gr;
	htitle="HiggsM_200masscuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,260,0.0,260.);
	hname= "HiggsPt_200masscuts_" + *rads + *gr;
	htitle="HiggsPt_200masscuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "ZBosonPt_200masscuts_" + *rads + *gr;
	htitle="ZBosonPt_200masscuts" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "j1Pt_200masscuts_" + *rads + *gr;
	htitle="j1Pt_200masscuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "j2Pt_200masscuts_" + *rads + *gr;
	htitle="j2Pt_200masscuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "deltaRbb_200masscuts_" + *rads + *gr;
	htitle="deltaRbb_200masscuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,600,0.0,6.0);
	hname= "HiggsM_300masscuts_" + *rads + *gr;
	htitle="HiggsM_300masscuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,260,0.0,260.);
	hname= "HiggsPt_300masscuts_" + *rads + *gr;
	htitle="HiggsPt_300masscuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "ZBosonPt_300masscuts_" + *rads + *gr;
	htitle="ZBosonPt_300masscuts" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "j1Pt_300masscuts_" + *rads + *gr;
	htitle="j1Pt_300masscuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "j2Pt_300masscuts_" + *rads + *gr;
	htitle="j2Pt_300masscuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,200,0.0,1000.);
	hname= "deltaRbb_300masscuts_" + *rads + *gr;
	htitle="deltaRbb_300masscuts_" + *rads + *gr;
	m_HistNames[hname] = ssDir.make<TH1D>(hname,htitle,600,0.0,6.0);
      } 
    }
  }
  
}

// ------------ method called once each job just before starting event loop  ------------
void 
GroomHbbAnalyzer::beginJob()
{
  bookHistograms();
}

// ------------ method called once each job just after ending the event loop  ------------
void 
GroomHbbAnalyzer::endJob() 
{
}


// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
GroomHbbAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(GroomHbbAnalyzer);
