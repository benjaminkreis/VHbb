// -*- C++ -*-
//
// Package:    VHbb/HbbProducer
// Class:      HbbProducer
// 
/**\class HbbProducer HbbProducer.cc VHbb/HbbProducer/plugins/HbbProducer.cc

   Description: [one line class summary]

   Implementation:
   [Notes on implementation]
*/
//
// Original Author:  john stupak
//         Created:  Fri, 27 Jun 2014 22:16:05 GMT
//
//


// system include files
#include <memory>
#include <vector>
#include <ctime>

// cmssw include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

// user include files
#include "VHbb/HbbProducer/interface/HbbTuple.h"
#include "VHbb/HbbProducer/src/helpers.cc"

using namespace std;

//
// class declaration
//

class HbbProducer : public edm::EDProducer {
public:
  explicit HbbProducer(const edm::ParameterSet&);
  ~HbbProducer();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  virtual void beginJob() override;
  virtual void produce(edm::Event&, const edm::EventSetup&) override;
  virtual void endJob() override;
  
  //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
  //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
  //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
  //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
  
  edm::InputTag _AK4Source;
  edm::InputTag _muonSource;
  edm::InputTag _electronSource;
  
  Hbb::Tuple _output;
  
  
  // ----------member data ---------------------------
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
HbbProducer::HbbProducer(const edm::ParameterSet& iConfig)
{
  _AK4Source=edm::InputTag(iConfig.getParameter<edm::InputTag>("AK4Source"));
  _muonSource=edm::InputTag(iConfig.getParameter<edm::InputTag>("muonSource"));
  _electronSource=edm::InputTag(iConfig.getParameter<edm::InputTag>("electronSource"));

  //register your products
  produces<Hbb::Tuple>();
}


HbbProducer::~HbbProducer()
{
 
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
HbbProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  //clock_t start=clock();
  
  _output=Hbb::Tuple();

  h_patJets AK4jets;
  iEvent.getByLabel(_AK4Source,AK4jets);

  edm::Handle< edm::View< pat::Muon > > inputMuons;
  iEvent.getByLabel(_muonSource,inputMuons);

  edm::Handle< edm::View< pat::Electron > > inputElectrons;
  iEvent.getByLabel(_electronSource,inputElectrons);

  //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  //AK4 Jets

  for(auto inputJet=AK4jets->begin(); inputJet!=AK4jets->end(); ++inputJet){
    Hbb::Jet outputJet=Hbb::Jet(*inputJet);
    outputJet.R = 0.4;
    _output.AK4PFCHS.push_back(outputJet);
  }

  //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  //Muons

  if(inputMuons->size()>0){
    
    for(auto inputMuon=inputMuons->begin(); inputMuon!=inputMuons->end(); ++inputMuon){
      Hbb::Muon muon=Hbb::Muon();
      muon.lv.SetPtEtaPhiM(inputMuon->pt(), inputMuon->eta(), inputMuon->phi(), inputMuon->mass());
      muon.charge=inputMuon->charge();
      muon.isolation=(inputMuon->pfIsolationR04().sumChargedHadronPt + max(0., inputMuon->pfIsolationR04().sumNeutralHadronEt + inputMuon->pfIsolationR04().sumPhotonEt - 0.5*inputMuon->pfIsolationR04().sumPUPt))/inputMuon->pt();
      _output.Muons.push_back(muon);
    }
  }

  //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  //Electrons

  if(inputElectrons->size()>0){
    
    for(auto inputElectron=inputElectrons->begin(); inputElectron!=inputElectrons->end(); ++inputElectron){
      Hbb::Electron electron=Hbb::Electron();
      electron.lv.SetPtEtaPhiM(inputElectron->pt(), inputElectron->eta(), inputElectron->phi(), inputElectron->mass());
      electron.charge=inputElectron->charge();
      electron.isolation=(inputElectron->pfIsolationVariables().sumChargedHadronPt + max(0., inputElectron->pfIsolationVariables().sumNeutralHadronEt + inputElectron->pfIsolationVariables().sumPhotonEt - 0.5*inputElectron->pfIsolationVariables().sumPUPt))/inputElectron->pt();
      _output.Electrons.push_back(electron);
    }
  }

  //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  auto_ptr<Hbb::Tuple> pOut(new Hbb::Tuple(_output));
  iEvent.put(pOut);

}
  
// ------------ method called once each job just before starting event loop  ------------
void 
HbbProducer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
HbbProducer::endJob() {
}

// ------------ method called when starting to processes a run  ------------
/*
  void
  HbbProducer::beginRun(edm::Run const&, edm::EventSetup const&)
  {
  }
*/
 
// ------------ method called when ending the processing of a run  ------------
/*
  void
  HbbProducer::endRun(edm::Run const&, edm::EventSetup const&)
  {
  }
*/
 
// ------------ method called when starting to processes a luminosity block  ------------
/*
  void
  HbbProducer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
  {
  }
*/
 
// ------------ method called when ending the processing of a luminosity block  ------------
/*
  void
  HbbProducer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
  {
  }
*/
 
// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
HbbProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
  
//define this as a plug-in
DEFINE_FWK_MODULE(HbbProducer);
  
