#ifndef VHbb_HbbProducer_HbbTuple_h
#define VHbb_HbbProducer_HbbTuple_h

#include "TLorentzVector.h"

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
  
  struct SubJet:Object
  {
    float area, R;
    
    
  SubJet() : Object()
      {
	this->initialize();
      }
    
  SubJet(TLorentzVector theLV) : Object(theLV)
    {
      this->initialize();
    }
    
  SubJet(double pT, double eta, double phi, double m) : Object(pT, eta, phi, m)
      {
	this->initialize();
      }
    
    void initialize(){
      area=-9999;
      R=-9999;
    }

  };

  //---------------------------------------------------------------------------------
  
  struct Jet:Object
  {
    float area, R;
    float tau1, tau2, tau3;
    float prunedMass, trimmedMass, filteredMass;
    float qJetsVolatility;
    float csv;
    float Nconstit;

    std::vector<SubJet> trimmedSubJets;
    std::vector<SubJet> filteredSubJets;
    std::vector<SubJet> prunedSubJets;
    
  Jet() : Object()
      {
	this->initialize();
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
      tau1=-9999; 
      tau2=-9999;
      tau3=-9999;
      prunedMass=-9999;
      trimmedMass=-9999;
      filteredMass=-9999;
      qJetsVolatility=-9999;
      csv=-9999;
      Nconstit=-9999;
    }

    
  };
  
  //---------------------------------------------------------------------------------

  struct Lepton:Object
  {
    int charge;
    
  Lepton() : Object(),
      charge(-9999)
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

  struct Tau:Lepton
  {
  Tau() : Lepton()
      {
      }

  };

  //---------------------------------------------------------------------------------

  struct V:Object
  {
  };

  //---------------------------------------------------------------------------------

  struct Higgs:Object
  {

    std::vector<Jet> daughters;

    float csv;    
    
  Higgs() : Object()
      {
	this->initialize();
      }

    void initialize(){
      csv=-9999;
    }

  };

  //---------------------------------------------------------------------------------
  struct MET:Object
  {
  };

  //---------------------------------------------------------------------------------

  struct Tuple
  {
    int eventClassification;
    float rho;
    
    std::vector<Jet> AK4PFCHS;
    std::vector<Jet> AK8PFCHS;
    std::vector<Jet> AK10PFCHS;
    std::vector<Jet> AK12PFCHS;
    std::vector<Jet> AK15PFCHS;

    std::vector<Electron> Electrons;
    std::vector<Muon> Muons;
    std::vector<Tau> Taus;

    std::vector<Higgs> THiggs;
    
  Tuple() : 
    rho(-9999), 
      AK4PFCHS(std::vector<Jet>()), AK8PFCHS(std::vector<Jet>()), AK10PFCHS(std::vector<Jet>()), AK12PFCHS(std::vector<Jet>()), AK15PFCHS(std::vector<Jet>()),
      Electrons(std::vector<Electron>()), Muons(std::vector<Muon>()),Taus(std::vector<Tau>()),
      THiggs(std::vector<Higgs>())
    {
    }
  };
  
  typedef std::vector<Object> ObjectCollection;
  typedef std::vector<Jet> JetCollection;
  typedef std::vector<Electron> ElectronCollection;
  typedef std::vector<Muon> MuonCollection;
  typedef std::vector<Tau> TauCollection;
  typedef std::vector<Tuple> TupleCollection;
  typedef std::vector<Higgs> HiggsCollection;
}

#endif
