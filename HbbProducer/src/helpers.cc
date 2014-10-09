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
      if (pT2>maxPT2 && fabs(jet1->p4().Eta())<2.5 && fabs(jet2->p4().Eta())<2.5 && jet1->p4().Pt()>20 && jet2->p4().Pt()>20){
	d1=*jet1;
	d2=*jet2;
      }
    }
  }
}

void getHiggsCandidate(vector<Hbb::Jet> inputJets, pair<int,int> &leadingSubleadingIndex){
  double maxPT2=0;
  for(unsigned int jet1=0; jet1<inputJets.size(); jet1++){
     for(unsigned int jet2=jet1+1; jet2<inputJets.size() && jet1<inputJets.size()-1; jet2++){
      double pT2=pow(inputJets[jet1].lv.Px()+inputJets[jet2].lv.Px(),2)+
         pow(inputJets[jet1].lv.Py()+inputJets[jet2].lv.Py(),2);
      if (pT2>maxPT2){
         leadingSubleadingIndex=make_pair(jet1,jet2);
      }
    }
  }
}
