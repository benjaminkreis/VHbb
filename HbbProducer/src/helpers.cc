#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

#include "VHbb/HbbProducer/interface/HbbTuple.h"

using namespace std;

typedef edm::Handle< edm::View< pat::Jet > > h_patJets;
typedef vector<Hbb::Jet> v_HbbJets;
