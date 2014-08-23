#include "VHbb/HbbProducer/interface/HbbTuple.h"

#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "JetMETCorrections/Objects/interface/JetCorrector.h"
#include "Math/LorentzVector.h"

#include "TMath.h"

#include <vector>

using namespace std;

int nInterpretations=15;
float Rmin=0.1;
float Rmax=1.5;

typedef ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double> > XYZTLorentzVectorD;

vector<Hbb::Higgs> telescope(pat::Jet inputJet1, pat::Jet inputJet2, edm::Handle< edm::PtrVector<reco::Candidate> > candidates,  edm::Event& iEvent, const edm::EventSetup& iSetup){
  vector<Hbb::Higgs> result;

  for(int i=0; i<nInterpretations; i++){
    float R=Rmin+(i*(Rmax-Rmin)/nInterpretations);
    
    Hbb::Higgs H;
    Hbb::Jet j1, j2;
    j1.lv.SetPxPyPzE(0,0,0,0);
    j2.lv.SetPxPyPzE(0,0,0,0);
    
    for(auto candidateItr=candidates->begin(); candidateItr!=candidates->end(); ++candidateItr){
      edm::Ptr<reco::Candidate> candidate=*candidateItr;

      TLorentzVector p4=TLorentzVector();
      p4.SetPxPyPzE(candidate->px(), candidate->py(), candidate->pz(), candidate->energy());
      
      double dR1Squared=deltaR2(inputJet1, *candidate);
      double dR2Squared=deltaR2(inputJet2, *candidate);

      if(dR1Squared<R*R || dR2Squared<R*R){
	if(dR1Squared<dR2Squared) j1.lv+=p4;
	else j2.lv+=p4;
      }
    }

    double delta=deltaR(inputJet1,inputJet2);
    double A=TMath::Pi()*R*R;
    if(delta<2*R) A=A - (R*R*TMath::ACos(delta/(2*R))) + (.5*delta*R*sqrt(1-pow(delta/(2*R),2))); //I added the factor of 0.5 in the last term, not sure if this is correct - JS
    j1.area=A;
    j2.area=A;
    j1.R=R;
    j2.R=R;

    double corrR=1;
    if (R<corrR) corrR=R;
    char c[99];
    sprintf(c, "ak%iPFCHSL1L2L3", int(10*corrR));
    const JetCorrector* corrector = JetCorrector::getJetCorrector(string(c),iSetup);
    
    //JetCorrector objects only work with real jets - So create them

    XYZTLorentzVectorD lv_j1;
    lv_j1.SetPx(j1.lv.Px());
    lv_j1.SetPy(j1.lv.Py());
    lv_j1.SetPz(j1.lv.Pz());
    lv_j1.SetE(j1.lv.E());

    XYZTLorentzVectorD lv_j2;
    lv_j2.SetPx(j2.lv.Px());
    lv_j2.SetPy(j2.lv.Py());
    lv_j2.SetPz(j2.lv.Pz());
    lv_j2.SetE(j2.lv.E());

    pat::Jet p_j1;
    p_j1.setJetArea(A);
    p_j1.setP4(lv_j1);
    double f1=corrector->correction(p_j1, iEvent, iSetup);
    j1.lv*=f1;

    pat::Jet p_j2;
    p_j2.setJetArea(A);
    p_j2.setP4(lv_j2);    
    double f2=corrector->correction(p_j2, iEvent, iSetup);
    j2.lv*=f2;

    H.lv=j1.lv+j2.lv;
    H.daughters.push_back(j1);
    H.daughters.push_back(j2);
    result.push_back(H);
  } 
  
  return result;
}
