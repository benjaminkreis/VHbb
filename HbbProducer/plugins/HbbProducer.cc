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
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

// user include files
#include "VHbb/HbbProducer/interface/HbbTuple.h"
#include "VHbb/HbbProducer/src/telescope.cc"
#include "VHbb/HbbProducer/src/groom.cc"
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
  
  edm::InputTag _rhoSource;
  edm::InputTag _packedCandidateSource, _prunedGenParticleSource, _packedGenParticleSource;
  edm::InputTag _AK4Source, _AK8Source, _AK10Source, _AK12Source, _AK15Source;
  edm::InputTag _AK8PackedSource, _AK10PackedSource, _AK12PackedSource, _AK15PackedSource;
  edm::InputTag _AK4GenSource;
  edm::InputTag _muonSource;
  
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
  
  _rhoSource=edm::InputTag(iConfig.getParameter<edm::InputTag>("rhoSource"));

  _packedCandidateSource=edm::InputTag(iConfig.getParameter<edm::InputTag>("packedCandidateSource"));

  _prunedGenParticleSource=edm::InputTag(iConfig.getParameter<edm::InputTag>("prunedGenParticleSource"));
  _packedGenParticleSource=edm::InputTag(iConfig.getParameter<edm::InputTag>("packedGenParticleSource"));

  _AK4Source=edm::InputTag(iConfig.getParameter<edm::InputTag>("AK4Source"));
  _AK8Source=edm::InputTag(iConfig.getParameter<edm::InputTag>("AK8Source"));
  _AK10Source=edm::InputTag(iConfig.getParameter<edm::InputTag>("AK10Source"));
  _AK12Source=edm::InputTag(iConfig.getParameter<edm::InputTag>("AK12Source"));
  _AK15Source=edm::InputTag(iConfig.getParameter<edm::InputTag>("AK15Source"));

  _AK8PackedSource=edm::InputTag(iConfig.getParameter<edm::InputTag>("AK8PackedSource"));
  _AK10PackedSource=edm::InputTag(iConfig.getParameter<edm::InputTag>("AK10PackedSource"));
  _AK12PackedSource=edm::InputTag(iConfig.getParameter<edm::InputTag>("AK12PackedSource"));
  _AK15PackedSource=edm::InputTag(iConfig.getParameter<edm::InputTag>("AK15PackedSource"));

  _AK4GenSource=edm::InputTag(iConfig.getParameter<edm::InputTag>("AK4GenSource"));

  _muonSource=edm::InputTag(iConfig.getParameter<edm::InputTag>("muonSource"));

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

  edm::Handle<double> rho;
  iEvent.getByLabel(_rhoSource,rho);

  edm::Handle< edm::View<reco::Candidate> > packedCandidates;
  iEvent.getByLabel(_packedCandidateSource, packedCandidates);

  edm::Handle< edm::View<reco::GenParticle> > prunedGenParticles;
  iEvent.getByLabel(_prunedGenParticleSource, prunedGenParticles);
  
  edm::Handle< edm::View<reco::Candidate> > packedGenParticles;
  iEvent.getByLabel(_packedGenParticleSource, packedGenParticles);

  map< string, h_patJets > fatJetInputs=map< string, h_patJets >();
  map< string, v_HbbJets* > fatJetOutputs=map< string, v_HbbJets* >();

  h_patJets AK4jets;
  iEvent.getByLabel(_AK4Source,AK4jets);

  //h_patJets AK4GenJets;
  //iEvent.getByLabel(_AK4GenSource,AK4GenJets);

  h_patJets AK8jets;
  iEvent.getByLabel(_AK8Source,AK8jets);
  fatJetInputs.insert(pair<string,h_patJets >(string("AK8"),AK8jets));
  fatJetOutputs.insert(pair<string, v_HbbJets* >(string("AK8"),&_output.AK8PFCHS));

  h_patJets AK10jets;
  iEvent.getByLabel(_AK10Source,AK10jets);
  fatJetInputs.insert(pair<string,h_patJets >(string("AK10"),AK10jets));
  fatJetOutputs.insert(pair<string, v_HbbJets* >(string("AK10"),&_output.AK10PFCHS));
  
  h_patJets AK12jets;
  iEvent.getByLabel(_AK12Source,AK12jets);
  fatJetInputs.insert(pair<string,h_patJets >(string("AK12"),AK12jets));
  fatJetOutputs.insert(pair<string, v_HbbJets* >(string("AK12"),&_output.AK12PFCHS));
  
  h_patJets AK15jets;
  iEvent.getByLabel(_AK15Source,AK15jets);
  fatJetInputs.insert(pair<string,h_patJets >(string("AK15"),AK15jets));
  fatJetOutputs.insert(pair<string, v_HbbJets* >(string("AK15"),&_output.AK15PFCHS));
  /*
  h_patJets AK8jets;
  iEvent.getByLabel(_AK8Source,AK8jets);
  fatJetInputs.insert(pair<string,h_patJets >(string("AK8"),AK8jets));
  fatJetOutputs.insert(pair<string, v_HbbJets* >(string("AK8"),&_output.AK8PFCHS));

  h_patJets AK10jets;
  iEvent.getByLabel(_AK10Source,AK10jets);
  fatJetInputs.insert(pair<string,h_patJets >(string("AK10"),AK10jets));
  fatJetOutputs.insert(pair<string, v_HbbJets* >(string("AK10"),&_output.AK10PFCHS));

  h_patJets AK12jets;
  iEvent.getByLabel(_AK12Source,AK12jets);
  fatJetInputs.insert(pair<string,h_patJets >(string("AK12"),AK12jets));
  fatJetOutputs.insert(pair<string, v_HbbJets* >(string("AK12"),&_output.AK12PFCHS));

  h_patJets AK15jets;
  iEvent.getByLabel(_AK15Source,AK15jets);
  fatJetInputs.insert(pair<string,h_patJets >(string("AK15"),AK15jets));
  fatJetOutputs.insert(pair<string, v_HbbJets* >(string("AK15"),&_output.AK15PFCHS));

  h_patJets AK8PackedJets;
  iEvent.getByLabel(_AK8PackedSource,AK8PackedJets);

  h_patJets AK10PackedJets;
  iEvent.getByLabel(_AK10PackedSource,AK10PackedJets);

  h_patJets AK12PackedJets;
  iEvent.getByLabel(_AK12PackedSource,AK12PackedJets);

  h_patJets AK15PackedJets;
  iEvent.getByLabel(_AK15PackedSource,AK15PackedJets);
  */

  edm::Handle< edm::View< pat::Muon > > inputMuons;
  iEvent.getByLabel(_muonSource,inputMuons);

  //clock_t setup=clock();
  //cout<<"Setup time: "<<(setup-start)/(double)(CLOCKS_PER_SEC/1000)<<endl;

  //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
  //Event quantities

  //cout<<"Rho"<<endl;

  _output.rho=*rho;

  //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  //gen particles

  if(prunedGenParticles->size()>0){
    for (auto input=prunedGenParticles->begin(); input!=prunedGenParticles->end(); ++input){
      //cout<<"Gen particle loop"<<endl;
      Hbb::GenParticle output=Hbb::GenParticle(input->pt(), input->eta(), input->phi(), input->mass());
      output.pdgId=input->pdgId();
      output.status=input->status();
      
      //cout<<"Mom"<<endl;
      const reco::Candidate *mom=input->mother();
      if (mom) output.motherId=mom->pdgId();
      
      //cout<<"daughter"<<endl;
      int n = input->numberOfDaughters();
      for(int i=0; i<n; i++) {
	const reco::Candidate *daughter=input->daughter(i);
	if (daughter) output.daughterIds.push_back(daughter->pdgId());
      }

      //cout<<"Special particles"<<endl;
      if(output.daughterIds.size()>0) {
	if((output.pdgId==23||output.pdgId==24) && output.daughterIds[0]==25)
	  _output.genVstar=output;
      }
      else {
	if(output.daughterIds.size()>1) {
	  if ((output.pdgId==23||output.pdgId==24) && output.daughterIds[1]==25)
	    _output.genVstar=output;
	}
      }

      if(output.daughterIds.size()>0) {
	if((output.pdgId==23||output.pdgId==24) && (abs(output.daughterIds[0])==11||
						    abs(output.daughterIds[0])==12||
						    abs(output.daughterIds[0])==13||
						    abs(output.daughterIds[0])==14||
						    abs(output.daughterIds[0])==15||
						    abs(output.daughterIds[0])==16||
						    abs(output.daughterIds[0])==1||
						    abs(output.daughterIds[0])==2||
						    abs(output.daughterIds[0])==3||
						    abs(output.daughterIds[0])==4||
						    abs(output.daughterIds[0])==5||
						    abs(output.daughterIds[0])==6))                       
	  _output.genV=output;
	
	if( output.pdgId==25                     && abs(output.daughterIds[0])==5)
	_output.genHiggs=output;
      }

      if((output.pdgId==11||output.pdgId==12||output.pdgId==13||output.pdgId==14||output.pdgId==15||output.pdgId==16) && (output.motherId==24||output.motherId==25)) 
	_output.genLepton=output;
      if((output.pdgId==-11||output.pdgId==-12||output.pdgId==-13||output.pdgId==-14||output.pdgId==-15||output.pdgId==-16) && (output.motherId==24||output.motherId==25)) 
	_output.genAntiLepton=output;
      if(output.pdgId==5 && output.motherId==25) 
	_output.genB=output;
      if(output.pdgId==-5 && output.motherId==25) 
	_output.genAntiB=output;

      _output.GenParticles.push_back(output);
    }
  }
  
  //clock_t gen=clock();
  //cout<<"Gen time: "<<(gen-setup)/(double)(CLOCKS_PER_SEC/1000)<<endl;

  //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  //AK4 Jets

  for(auto jet1=AK4jets->begin(); jet1!=AK4jets->end(); ++jet1){
    Hbb::Jet jet=Hbb::Jet(jet1->pt(), jet1->eta(), jet1->phi(), jet1->mass());
    jet.R = 0.4;
    jet.area = jet1->jetArea();
    jet.csv = jet1->bDiscriminator("combinedSecondaryVertexBJetTags");
    _output.AK4PFCHS.push_back(jet);
  }

  if(AK4jets->size()>1){
    pat::Jet d1=pat::Jet();
    pat::Jet d2=pat::Jet();
    getHiggsCandidate(AK4jets, d1, d2);
    vector<Hbb::Higgs> theHiggses=telescope(d1, d2, packedCandidates, iEvent, iSetup);
    _output.Higgses=theHiggses;

    theHiggses=telescope(_output.genB, _output.genAntiB, packedGenParticles, iEvent, iSetup);
    _output.GenHiggses=theHiggses;

  }
  
  //clock_t ak4=clock();
  //cout<<"AK4 time: "<<(ak4-gen)/(double)(CLOCKS_PER_SEC/1000)<<endl;

  //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  //AK4 Gen Jets
  /*
  if(AK4GenJets->size()>0){
    for(auto jet1=AK4GenJets->begin(); jet1!=AK4GenJets->end(); ++jet1){
      Hbb::Jet jet=Hbb::Jet(jet1->pt(), jet1->eta(), jet1->phi(), jet1->mass());
      jet.csv = jet1->bDiscriminator("combinedSecondaryVertexBJetTags");
      _output.AK4PFCHS.push_back(jet);
    }
  }

  if(AK4GenJets->size()>1){
    pat::Jet d1=pat::Jet();
    pat::Jet d2=pat::Jet();
    getHiggsCandidate(AK4GenJets, d1, d2);
    vector<Hbb::Higgs> theHiggses=telescope(d1, d2, packedCandidates, iEvent, iSetup);
    _output.Higgses=theHiggses;
  }
  */
  //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  //fat jets
  
  for(auto fatJetCollection=fatJetInputs.begin(); fatJetCollection!=fatJetInputs.end(); ++fatJetCollection){
    
    string name=fatJetCollection->first;
    h_patJets inputJets=fatJetCollection->second;
    
    double radius=.1*std::atof(name.substr(2).c_str());
    
    v_HbbJets outputJets;
    for(auto inputJet=inputJets->begin(); inputJet!=inputJets->end(); ++inputJet){
      
      Hbb::Jet jet=Hbb::Jet(inputJet->pt(), inputJet->eta(), inputJet->phi(), inputJet->mass());
      groom(*inputJet, jet, radius);
      outputJets.push_back(jet);
    }

    *fatJetOutputs[name]=outputJets;
  }

  //clock_t fat=clock();
  //cout<<"Fat jet time: "<<(fat-ak4)/(double)(CLOCKS_PER_SEC/1000)<<endl;

  //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  //Muons

  if(inputMuons->size()>0){
    
    for(auto inputMuon=inputMuons->begin(); inputMuon!=inputMuons->end(); ++inputMuon){
      Hbb::Muon muon=Hbb::Muon();
      muon.lv.SetPtEtaPhiM(inputMuon->pt(), inputMuon->eta(), inputMuon->phi(), inputMuon->mass());
      muon.charge=inputMuon->charge();
      _output.Muons.push_back(muon);
    }
  }

  //clock_t muons=clock();
  //cout<<"Muon time: "<<(muons-fat)/(double)(CLOCKS_PER_SEC/1000)<<endl;

  //- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  auto_ptr<Hbb::Tuple> pOut(new Hbb::Tuple(_output));
  iEvent.put(pOut);

  //clock_t output=clock();
  //cout<<"output time: "<<(output-muons)/(double)(CLOCKS_PER_SEC/1000)<<endl;
  //cout<<endl;
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
  
