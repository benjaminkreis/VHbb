#include "VHbb/HbbProducer/interface/HbbTuple.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/Math/interface/deltaR.h"

#include <fastjet/PseudoJet.hh>
#include <fastjet/FunctionOfPseudoJet.hh>
#include "fastjet/tools/Filter.hh"
#include "fastjet/tools/Pruner.hh"
#include "fastjet/tools/MassDropTagger.hh"
#include "fastjet/ClusterSequenceArea.hh"
#include "fastjet/contrib/Njettiness.hh"

#include <vector>

using namespace std;
using namespace fastjet;
using namespace fastjet::contrib;

//---------------------------------------------------------------------------------------------------------------------------------
//grooming parameters

//trimming
double Rtrim = 0.2;
double ptfrac = 0.05;

//filtering
double Rfilt = 0.2;
double Nfilt = 3;

//pruning
double zcut=0.1;
double rcut_factor=0.5;

//mass drop
double mucut=0.67;
double ycut=0.09;

//butterworth
double bmucut=0.67;
double bycut=0.09;
double Rbut=0.3;
double Nbut=3;

//n-subjettiness
double beta = 1.0; // power for angular dependence, e.g. beta = 1 --> linear k-means, beta = 2 --> quadratic/classic k-means
double Rcut = 10000.0; // maximum R particles can be from axis to be included in jet (large value for no cutoff) 

//---------------------------------------------------------------------------------------------------------------------------------

void groom(pat::Jet iJet, Hbb::Jet& oJet, double R){
  
  oJet.csv = iJet.bDiscriminator("combinedSecondaryVertexBJetTags");

  reco::Jet::Constituents constituents=iJet.getJetConstituents();

  double nconstit = 0.0;

  vector<PseudoJet> fjConstituents;
  for(auto constituentItr=constituents.begin(); constituentItr!=constituents.end(); ++constituentItr){
    edm::Ptr<reco::Candidate> constituent=*constituentItr;

    nconstit = nconstit + 1;

    fjConstituents.push_back(PseudoJet(constituent->px(), constituent->py(), constituent->pz(), constituent->energy()));
  }

  oJet.Nconstit = nconstit;

  JetDefinition jet_def(cambridge_algorithm, R);
  // the use of a ClusterSequenceArea (instead of a plain ClusterSequence)
  // is only needed because we will later combine filtering with area-based
  // subtraction
  ClusterSequenceArea clust_seq(fjConstituents, jet_def, AreaDefinition(active_area_explicit_ghosts));
  vector<PseudoJet> inclusive_jets = sorted_by_pt(clust_seq.inclusive_jets(0));
  PseudoJet theJet=inclusive_jets[0];

  
  //------------------------------------
  // Trimming
  //------------------------------------
  
  Filter trimmer(JetDefinition(cambridge_algorithm, Rtrim), SelectorPtFractionMin(ptfrac) );
  PseudoJet trimmedJet = trimmer(theJet);
  
  oJet.trimmedMass=trimmedJet.m();

  vector<PseudoJet> fjSubjets = trimmedJet.pieces();
  for (size_t i = 0; i < fjSubjets.size(); i++){
    Hbb::SubJet sj=Hbb::SubJet(fjSubjets[i].pt(), fjSubjets[i].eta(), fjSubjets[i].phi(), fjSubjets[i].m());
    sj.R=Rtrim;
    oJet.trimmedSubJets.push_back(sj);
  }

  //------------------------------------
  // Filtering
  //------------------------------------

  Filter filter(JetDefinition(cambridge_algorithm, Rfilt), SelectorNHardest(Nfilt));
  PseudoJet filteredJet = filter(theJet);

  oJet.filteredMass=filteredJet.m();

  fjSubjets = filteredJet.pieces();
  for (size_t i = 0; i < fjSubjets.size(); i++){
    Hbb::SubJet sj=Hbb::SubJet(fjSubjets[i].pt(), fjSubjets[i].eta(), fjSubjets[i].phi(), fjSubjets[i].m());
    sj.R=Rfilt;
    oJet.filteredSubJets.push_back(sj);
  }

  //------------------------------------
  //Pruning
  //------------------------------------

  Pruner pruner(cambridge_algorithm, zcut, rcut_factor);
  PseudoJet prunedJet = pruner(theJet);

  oJet.prunedMass=prunedJet.m();
  
  fjSubjets = prunedJet.pieces();
  for (size_t i = 0; i < fjSubjets.size(); i++){
    Hbb::SubJet sj=Hbb::SubJet(fjSubjets[i].pt(), fjSubjets[i].eta(), fjSubjets[i].phi(), fjSubjets[i].m());
    //sj.R=
    oJet.prunedSubJets.push_back(sj);
  }

  //------------------------------------
  //Mass Drop Tagger 
  //------------------------------------

  MassDropTagger massdroptagger(mucut, ycut);
  PseudoJet mdtJet = massdroptagger(theJet);
  
  if (mdtJet != 0) {

    oJet.mdtMass=mdtJet.m();

    fjSubjets = mdtJet.pieces();
    for (size_t i = 0; i < fjSubjets.size(); i++){
      Hbb::SubJet sj=Hbb::SubJet(fjSubjets[i].pt(), fjSubjets[i].eta(), fjSubjets[i].phi(), fjSubjets[i].m());
      //sj.R=
      oJet.mdtSubJets.push_back(sj);
    }
  }

  //------------------------------------
  //Butterworth Algorithm
  //(basically MDT + filtering)
  //------------------------------------

  PseudoJet bmdtJet;
  if (bmucut == mucut && bycut == ycut) {
    bmdtJet = mdtJet;
  }
  else {
    MassDropTagger bmassdroptagger(bmucut, bycut);
    bmdtJet = bmassdroptagger(theJet);
  }
  
  if (bmdtJet != 0) {

    PseudoJet j1 = bmdtJet.pieces()[0];
    PseudoJet j2 = bmdtJet.pieces()[1];
    double Rbfilt = min(Rbut, deltaR(j1,j2)/2);

    Filter filt(JetDefinition(cambridge_algorithm, Rbfilt), SelectorNHardest(Nbut));
    PseudoJet butterJet = filt(bmdtJet);

    oJet.butterMass=butterJet.m();
    
    fjSubjets = butterJet.pieces();
    for (size_t i = 0; i < fjSubjets.size(); i++){
      Hbb::SubJet sj=Hbb::SubJet(fjSubjets[i].pt(), fjSubjets[i].eta(), fjSubjets[i].phi(), fjSubjets[i].m());
      //sj.R=
      oJet.butterSubJets.push_back(sj);
    }
  }

  //------------------------------------
  // NSubJettiness
  //------------------------------------
  NsubParameters paraNsub(beta, R, Rcut);
  
  Njettiness nSubOnePass(Njettiness::onepass_kt_axes,paraNsub);
  
  oJet.tau1 = nSubOnePass.getTau(1,fjConstituents);
  oJet.tau2 = nSubOnePass.getTau(2,fjConstituents);
  oJet.tau3 = nSubOnePass.getTau(3,fjConstituents);
}
