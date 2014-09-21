#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "VHbb/HbbProducer/interface/HbbTuple.h"

using namespace std;

typedef edm::Handle< edm::View< pat::Jet > > h_patJets;
typedef vector<Hbb::Jet> v_HbbJets;

void getHiggsCandidate(h_patJets inputJets, pat::Jet &d1, pat::Jet &d2){
  double maxPT2=0;
  for(auto jet1=inputJets->begin(); jet1!=inputJets->end(); ++jet1){
    for(auto jet2=jet1+1; jet2!=inputJets->end() && jet1!=inputJets->end()-1; ++jet2){
      double pT2=pow(jet1->px()+jet2->px(),2)+pow(jet1->py()+jet2->py(),2);
      if (pT2>maxPT2){
	d1=*jet1;
	d2=*jet2;
      }
    }
  }
}
