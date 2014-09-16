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


// system include files
#include <memory>

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

class HbbAnalyzer : public edm::EDAnalyzer {
   public:
      explicit HbbAnalyzer(const edm::ParameterSet&);
      ~HbbAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
      edm::InputTag HbbSrc;
      TH1D* mHiggs;
      TH1D* mjj;
      TH1D* HiggsPt;
      TH1D* j1Pt;
      TH1D* j2Pt;
      TH1D* HiggsEta;
      TH1D* j1Eta;
      TH1D* j2Eta;
      TH1D* HiggsPhi;
      TH1D* j1Phi;
      TH1D* j2Phi;
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
   HbbSrc = edm::InputTag(iConfig.getParameter<edm::InputTag>("HbbSource"));

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
  using namespace edm;



//#ifdef THIS_IS_AN_EVENT_EXAMPLE
  Handle<Hbb::Tuple> HbbHandle;
  iEvent.getByLabel(HbbSrc,HbbHandle);
  mHiggs->Fill(HbbHandle->Higgses[3].lv.M());
  HiggsPt->Fill(HbbHandle->Higgses[3].lv.Pt());
  HiggsEta->Fill(HbbHandle->Higgses[3].lv.Eta());
  HiggsPhi->Fill(HbbHandle->Higgses[3].lv.Phi());
  for(unsigned int iR=0; iR<HbbHandle->Higgses.size(); iR++) {
    mjj->Fill((HbbHandle->Higgses[iR].daughters[0].lv+HbbHandle->Higgses[iR].daughters[1].lv).M());
    j1Pt->Fill(HbbHandle->Higgses[iR].daughters[0].lv.Pt());
    j2Pt->Fill(HbbHandle->Higgses[iR].daughters[1].lv.Pt());
    j1Eta->Fill(HbbHandle->Higgses[iR].daughters[0].lv.Eta());
    j2Eta->Fill(HbbHandle->Higgses[iR].daughters[1].lv.Eta());
    j1Phi->Fill(HbbHandle->Higgses[iR].daughters[0].lv.Phi());
    j2Phi->Fill(HbbHandle->Higgses[iR].daughters[1].lv.Phi());
  }
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

  mHiggs   = fs->make<TH1D>("mHiggs","mHiggs",200,0,200);//40,120,160);
  mjj      = fs->make<TH1D>("mjj","mjj",200,0,200);
  HiggsPt  = fs->make<TH1D>("HiggsPt","HiggsPt",200,0,1000);
  j1Pt     = fs->make<TH1D>("j1Pt","j1Pt",200,0,1000);
  j2Pt     = fs->make<TH1D>("j2Pt","j2Pt",200,0,1000);
  HiggsEta = fs->make<TH1D>("HiggsEta","HiggsEta",100,-5,5);
  j1Eta    = fs->make<TH1D>("j1Eta","j1Eta",100,-5,5);
  j2Eta    = fs->make<TH1D>("j2Eta","j2Eta",100,-5,5);
  HiggsPhi = fs->make<TH1D>("HiggsPhi","HiggsPhi",60,-TMath::Pi(),TMath::Pi());
  j1Phi    = fs->make<TH1D>("j1Phi","j1Phi",60,-TMath::Pi(),TMath::Pi());
  j2Phi    = fs->make<TH1D>("j2Phi","j2Phi",60,-TMath::Pi(),TMath::Pi());
}

// ------------ method called once each job just after ending the event loop  ------------
void 
HbbAnalyzer::endJob() 
{
}

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
