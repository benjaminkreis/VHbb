#ifndef VHbb_HbbProducer_HbbTuple_h
#define VHbb_HbbProducer_HbbTuple_h

#include "TLorentzVector.h"

#include "DataFormats/PatCandidates/interface/Jet.h"

#include <string>

namespace Hbb
{

  //---------------------------------------------------------------------------------

  struct Object
  {
    TLorentzVector lv;

  Object() :
    lv(TLorentzVector())
    {
    }

  Object(TLorentzVector theLV) : lv(TLorentzVector())
    {
      lv.SetPtEtaPhiM(theLV.Pt(), theLV.Eta(), theLV.Phi(), theLV.M());
    }

  Object(double pT, double eta, double phi, double m) : lv(TLorentzVector())
    {
      lv.SetPtEtaPhiM(pT, eta, phi, m);
    }

  };

  //---------------------------------------------------------------------------------

  struct Jet:Object
  {
    float area, R;
    float csv;

  Jet() : Object()
      {
	this->initialize();
      }

  Jet(pat::Jet input) : Object(input.pt(), input.eta(), input.phi(), input.mass())
      {
	this->initialize();
	this->area = input.jetArea();
	this->csv = input.bDiscriminator("combinedSecondaryVertexBJetTags");
      }
    
  Jet(TLorentzVector theLV) : Object(theLV)
    {
      this->initialize();
    }
    
  Jet(double pT, double eta, double phi, double m) : Object(pT, eta, phi, m)
      {
	this->initialize();
      }
    
    void initialize(){
      area=-9999;
      R=-9999;
      csv=-9999;
    }
    
  };
  
  //---------------------------------------------------------------------------------

  struct Lepton:Object
  {
    int charge;
    double isolation;
    
  Lepton() : Object(),
      charge(-9999), isolation(-9999)
      {
      }

  };

  //---------------------------------------------------------------------------------
  
  struct Electron:Lepton
  {
  Electron() : Lepton()
      {
      }

  };
  
  //---------------------------------------------------------------------------------
  
  struct Muon:Lepton
  {
  Muon() : Lepton()
      {
      }

  };

  //---------------------------------------------------------------------------------

  struct Tuple
  {
    std::vector<Jet> AK4PFCHS;
    std::vector<Electron> Electrons;
    std::vector<Muon> Muons;

  Tuple() : 
    AK4PFCHS(std::vector<Jet>()),
    Electrons(std::vector<Electron>()), 
    Muons(std::vector<Muon>())
    {
    }
  };
  
  typedef std::vector<Object> ObjectCollection;
  typedef std::vector<Jet> JetCollection;
  typedef std::vector<Electron> ElectronCollection;
  typedef std::vector<Muon> MuonCollection;
}

#endif
