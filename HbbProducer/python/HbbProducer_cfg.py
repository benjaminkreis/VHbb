import FWCore.ParameterSet.Config as cms


process = cms.Process("Hbb")
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True),
                                     allowUnscheduled = cms.untracked.bool(True) 
                                     )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(20) )
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
        'file:/eos/uscms/store/user/jstupak/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/Spring14dr-PU_S14_POSTLS170_V6AN1-v1/140622_185946/0000/miniAOD-prod_PAT_1.root'
        #'/store/mc/Spring14miniaod/DYJetsToMuMu_PtZ-180_M-50_13TeV-madgraph/MINIAODSIM/PU20bx25_POSTLS170_V5-v1/00000/AAF5494B-9707-E411-90D7-AC162DABCAF8.root'
        )
                            )

theGlobalTag='PLS170_V6AN1::All'   #PU_S14
#theGlobalTag='PLS170_V7AN1::All'   #PU20bx25

process.load("FWCore.MessageService.MessageLogger_cfi")

process.load('VHbb.HbbProducer.HbbProducer_cfi')

#####################################################################################################################################

process.load('PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.Geometry_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = theGlobalTag

process.pfCHS = cms.EDFilter('CandPtrSelector', src = cms.InputTag('packedPFCandidates'), cut = cms.string('fromPV'))
process.pfNoMuonCHS =  cms.EDProducer("CandPtrProjector", src = cms.InputTag("pfCHS"), veto = cms.InputTag("selectedMuons"))

#2012 Tight muon: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideMuonId#Tight_Muon
#missing dZ cut - JS
process.selectedMuons = cms.EDFilter("PATMuonSelector",
                                     src = cms.InputTag("slimmedMuons"),
                                     cut = cms.string('pt > 20. &'
                                                      'abs(eta) < 2.4 &'
                                                      'isGlobalMuon &'
                                                      'isPFMuon &'
                                                      'globalTrack.normalizedChi2 < 10.0 &'
                                                      'globalTrack.hitPattern.numberOfValidMuonHits > 0 &'
                                                      'numberOfMatchedStations > 1 &'
                                                      'abs(dB) < 0.2 &' #This was 0.02 before, ooops.  I think this is right - JS
                                                      'innerTrack.hitPattern.numberOfValidPixelHits > 0 &'
                                                      'innerTrack.hitPattern.trackerLayersWithMeasurement > 5 &'
                                                      '(pfIsolationR04.sumChargedHadronPt+ max(0.,pfIsolationR04.sumNeutralHadronEt+pfIsolationR04.sumPhotonEt-0.5*pfIsolationR04.sumPUPt))/pt < 0.12'
                                                      )
                                     )

#process.muonMatch.match='packedGenParticles'

"""
process.selectedMuons = cms.EDFilter("CandPtrSelector", src = cms.InputTag("slimmedMuons"), cut = cms.string('pt > 20. &'
                                                                                                             'abs(eta) < 2.4 &'
                                                                                                             'isGlobalMuon &' 
                                                                                                             'isPFMuon &'
                                                                                                             'globalTrack.normalizedChi2 < 10.0 &'
                                                                                                             'globalTrack.hitPattern.numberOfValidMuonHits > 0 &'
                                                                                                             'numberOfMatchedStations > 1 &'
                                                                                                             'abs(dB) < 0.02 &'
                                                                                                             'innerTrack.hitPattern.numberOfValidPixelHits > 0 &'
                                                                                                             'innerTrack.hitPattern.trackerLayersWithMeasurement > 5'
                                                                                                             ))
"""
#process.selectedElectrons = cms.EDFilter("CandPtrSelector", src = cms.InputTag("slimmedElectrons"), cut = cms.string("your selection for ele"))

process.load('RecoJets.Configuration.RecoPFJets_cff')
process.load('RecoJets.Configuration.RecoGenJets_cff')
process.fixedGridRhoFastjetAll.pfCandidatesTag = 'packedPFCandidates'

process.ak4PFJets.src = 'packedPFCandidates'
process.ak4PFJetsCHS.src = 'pfNoMuonCHS'

process.ak8PFJetsCHS  = process.ak4PFJetsCHS.clone(rParam = 0.8)
process.ak10PFJetsCHS = process.ak4PFJetsCHS.clone(rParam = 1.0)
process.ak12PFJetsCHS = process.ak4PFJetsCHS.clone(rParam = 1.2)
process.ak15PFJetsCHS = process.ak4PFJetsCHS.clone(rParam = 1.5)

process.ak4GenJets.src = 'packedGenParticles'
process.ak3GenJets  = process.ak4GenJets.clone(rParam = 0.3)
process.ak8GenJets  = process.ak4GenJets.clone(rParam = 0.8)
process.ak10GenJets = process.ak4GenJets.clone(rParam = 1.0)
process.ak12GenJets = process.ak4GenJets.clone(rParam = 1.2)
process.ak15GenJets = process.ak4GenJets.clone(rParam = 1.5)

process.ak8PFJetsCHSPruned.src = 'pfNoMuonCHS'
process.ak8PFJetsCHSTrimmed.src = 'pfNoMuonCHS'
process.ak8PFJetsCHSFiltered.src = 'pfNoMuonCHS'

process.ak10PFJetsCHSPruned = process.ak8PFJetsCHSPruned.clone(rParam = 1)
process.ak10PFJetsCHSTrimmed = process.ak8PFJetsCHSTrimmed.clone(rParam = 1)
process.ak10PFJetsCHSFiltered = process.ak8PFJetsCHSFiltered.clone(rParam = 1)

process.ak12PFJetsCHSPruned = process.ak8PFJetsCHSPruned.clone(rParam = 1.2)
process.ak12PFJetsCHSTrimmed = process.ak8PFJetsCHSTrimmed.clone(rParam = 1.2)
process.ak12PFJetsCHSFiltered = process.ak8PFJetsCHSFiltered.clone(rParam = 1.2)

process.ak15PFJetsCHSPruned = process.ak8PFJetsCHSPruned.clone(rParam = 1.5)
process.ak15PFJetsCHSTrimmed = process.ak8PFJetsCHSTrimmed.clone(rParam = 1.5)
process.ak15PFJetsCHSFiltered = process.ak8PFJetsCHSFiltered.clone(rParam = 1.5)

from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection
from PhysicsTools.PatAlgos.tools.jetTools import switchJetCollection

addJetCollection(
    process,
    labelName = 'AK4PFCHS',
    jetSource = cms.InputTag('ak4PFJetsCHS'),
    algo = 'ak4',
    rParam = 0.4,
    jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    trackSource = cms.InputTag('unpackedTracksAndVertices'),
    pvSource = cms.InputTag('unpackedTracksAndVertices'),
    btagDiscriminators = ['combinedSecondaryVertexBJetTags'],
    )

addJetCollection(
    process,
    labelName = 'AK8PFCHS',
    jetSource = cms.InputTag('ak8PFJetsCHS'),
    algo = 'ak8',
    rParam = 0.8,
    jetCorrections = ('AK8PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    trackSource = cms.InputTag('unpackedTracksAndVertices'),
    pvSource = cms.InputTag('unpackedTracksAndVertices'),
    btagDiscriminators = ['combinedSecondaryVertexBJetTags'],
    )

addJetCollection(
    process,
    labelName = 'AK10PFCHS',
    jetSource = cms.InputTag('ak10PFJetsCHS'),
    algo = 'ak10',
    rParam = 1.0,
    jetCorrections = ('AK10PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    trackSource = cms.InputTag('unpackedTracksAndVertices'),
    pvSource = cms.InputTag('unpackedTracksAndVertices'),
    btagDiscriminators = ['combinedSecondaryVertexBJetTags'],
    )

addJetCollection(
    process,
    labelName = 'AK12PFCHS',
    jetSource = cms.InputTag('ak12PFJetsCHS'),
    algo = 'ak12',
    rParam = 1.2,
    jetCorrections = ('AK10PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    trackSource = cms.InputTag('unpackedTracksAndVertices'),
    pvSource = cms.InputTag('unpackedTracksAndVertices'),
    btagDiscriminators = ['combinedSecondaryVertexBJetTags'],
    )

addJetCollection(
    process,
    labelName = 'AK15PFCHS',
    jetSource = cms.InputTag('ak15PFJetsCHS'),
    algo = 'ak15',
    rParam = 1.5,
    jetCorrections = ('AK10PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    trackSource = cms.InputTag('unpackedTracksAndVertices'),
    pvSource = cms.InputTag('unpackedTracksAndVertices'),
    btagDiscriminators = ['combinedSecondaryVertexBJetTags'],
    )

switchJetCollection(
    process,
    jetSource = cms.InputTag('ak4PFJets'),
    algo = 'ak4',
    rParam = 0.4,
    jetCorrections = ('AK4PF', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'Type-1'),
    trackSource = cms.InputTag('unpackedTracksAndVertices'),
    pvSource = cms.InputTag('unpackedTracksAndVertices'),
    #btagDiscriminators = ['combinedSecondaryVertexBJetTags'],   #this breaks the config
    )

for module in [process.patJetsAK4PFCHS, process.patJetsAK8PFCHS, process.patJetsAK10PFCHS, process.patJetsAK12PFCHS, process.patJetsAK15PFCHS]:
    module.addJetCharge   = False
    module.addBTagInfo    = True   
    module.getJetMCFlavour = False
    module.addAssociatedTracks = False

for module in [process.patJetPartonMatch, process.patJetPartonMatchAK4PFCHS, process.patJetPartonMatchAK8PFCHS, process.patJetPartonMatchAK10PFCHS, process.patJetPartonMatchAK12PFCHS, process.patJetPartonMatchAK15PFCHS]:
    module.matched='prunedGenParticles'

for module in [process.patJetCorrFactors, process.patJetCorrFactorsAK4PFCHS, process.patJetCorrFactorsAK8PFCHS, process.patJetCorrFactorsAK10PFCHS, process.patJetCorrFactorsAK12PFCHS, process.patJetCorrFactorsAK15PFCHS]:
    module.primaryVertices = 'offlineSlimmedPrimaryVertices'

process.load('RecoBTag.Configuration.RecoBTag_cff')
process.load('RecoJets.Configuration.RecoJetAssociations_cff')
process.load('PhysicsTools.PatAlgos.slimming.unpackedTracksAndVertices_cfi')

process.ak4JetTracksAssociatorAtVertexPF.jets = cms.InputTag('ak4PFJets')
process.ak4JetTracksAssociatorAtVertexPF.tracks = cms.InputTag('unpackedTracksAndVertices')

process.ak4JetTracksAssociatorAtVertexPFCHS=process.ak4JetTracksAssociatorAtVertexPF.clone(jets = cms.InputTag('ak4PFJetsCHS'), coneSize = 0.4)
process.ak8JetTracksAssociatorAtVertexPFCHS=process.ak4JetTracksAssociatorAtVertexPF.clone(jets = cms.InputTag('ak8PFJetsCHS'), coneSize = 0.8)
process.ak10JetTracksAssociatorAtVertexPFCHS=process.ak4JetTracksAssociatorAtVertexPF.clone(jets = cms.InputTag('ak10PFJetsCHS'), coneSize = 1)
process.ak12JetTracksAssociatorAtVertexPFCHS=process.ak4JetTracksAssociatorAtVertexPF.clone(jets = cms.InputTag('ak12PFJetsCHS'), coneSize = 1.2)
process.ak15JetTracksAssociatorAtVertexPFCHS=process.ak4JetTracksAssociatorAtVertexPF.clone(jets = cms.InputTag('ak15PFJetsCHS'), coneSize = 1.5)

process.impactParameterTagInfos.primaryVertex = cms.InputTag('unpackedTracksAndVertices')
process.inclusiveSecondaryVertexFinderTagInfos.extSVCollection = cms.InputTag('unpackedTracksAndVertices','secondary','')
process.combinedSecondaryVertex.trackMultiplicityMin = 1

process.secondaryVertexTagInfosAK4PFCHS.trackSelection.jetDeltaRMax = 0.4
process.secondaryVertexTagInfosAK4PFCHS.vertexCuts.maxDeltaRToJetAxis = 0.4
process.combinedSecondaryVertexAK4PFCHS=process.combinedSecondaryVertex.clone()
process.combinedSecondaryVertexAK4PFCHS.trackSelection.jetDeltaRMax = 0.4
process.combinedSecondaryVertexAK4PFCHS.trackPseudoSelection.jetDeltaRMax = 0.4
process.combinedSecondaryVertexBJetTagsAK4PFCHS.jetTagComputer = 'combinedSecondaryVertexAK4PFCHS'

from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters


addJetCollection(
    process,
    labelName = 'AK8PFCHSFiltered',
    jetSource = cms.InputTag('ak8PFJetsCHSFiltered'),
    jetCorrections = ('AK8PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    trackSource = cms.InputTag('unpackedTracksAndVertices'),
    pvSource = cms.InputTag('unpackedTracksAndVertices'),
    btagDiscriminators = ['combinedSecondaryVertexBJetTags'],
    getJetMCFlavour = False
    )

addJetCollection(
    process,
    labelName = 'AK8PFCHSFilteredSubjets',
    jetSource = cms.InputTag('ak8PFJetsCHSFiltered','SubJets'),
    jetCorrections = ('AK8PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    trackSource = cms.InputTag('unpackedTracksAndVertices'),
    pvSource = cms.InputTag('unpackedTracksAndVertices'),
    btagDiscriminators = ['combinedSecondaryVertexBJetTags'],
    getJetMCFlavour = False,
    )

process.patJetsAK8PFCHSFilteredPacked = cms.EDProducer("BoostedJetMerger",
                                                       jetSrc=cms.InputTag("patJetsAK8PFCHSFiltered" ),
                                                       subjetSrc=cms.InputTag("patJetsAK8PFCHSFilteredSubjets")
                                                       )
addJetCollection(
    process,
    labelName = 'AK10PFCHSFiltered',
    jetSource = cms.InputTag('ak10PFJetsCHSFiltered'),
    jetCorrections = ('AK10PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    trackSource = cms.InputTag('unpackedTracksAndVertices'),
    pvSource = cms.InputTag('unpackedTracksAndVertices'),
    btagDiscriminators = ['combinedSecondaryVertexBJetTags'],
    getJetMCFlavour = False
    )                                                  

addJetCollection(
    process,
    labelName = 'AK10PFCHSFilteredSubjets',
    jetSource = cms.InputTag('ak10PFJetsCHSFiltered','SubJets'),
    jetCorrections = ('AK10PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    trackSource = cms.InputTag('unpackedTracksAndVertices'),
    pvSource = cms.InputTag('unpackedTracksAndVertices'),
    btagDiscriminators = ['combinedSecondaryVertexBJetTags'],
    getJetMCFlavour = False,
    )

process.patJetsAK10PFCHSFilteredPacked = cms.EDProducer("BoostedJetMerger",
                                                        jetSrc=cms.InputTag("patJetsAK10PFCHSFiltered" ),
                                                        subjetSrc=cms.InputTag("patJetsAK10PFCHSFilteredSubjets")
                                                        )

addJetCollection(
    process,
    labelName = 'AK12PFCHSFiltered',
    jetSource = cms.InputTag('ak12PFJetsCHSFiltered'),
    jetCorrections = ('AK10PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    trackSource = cms.InputTag('unpackedTracksAndVertices'),
    pvSource = cms.InputTag('unpackedTracksAndVertices'),
    btagDiscriminators = ['combinedSecondaryVertexBJetTags'],
    getJetMCFlavour = False
    )

addJetCollection(
    process,
    labelName = 'AK12PFCHSFilteredSubjets',
    jetSource = cms.InputTag('ak12PFJetsCHSFiltered','SubJets'),
    jetCorrections = ('AK10PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    trackSource = cms.InputTag('unpackedTracksAndVertices'),
    pvSource = cms.InputTag('unpackedTracksAndVertices'),
    btagDiscriminators = ['combinedSecondaryVertexBJetTags'],
    getJetMCFlavour = False,
    )

process.patJetsAK12PFCHSFilteredPacked = cms.EDProducer("BoostedJetMerger",
                                                        jetSrc=cms.InputTag("patJetsAK12PFCHSFiltered" ),
                                                        subjetSrc=cms.InputTag("patJetsAK12PFCHSFilteredSubjets")
                                                        )

addJetCollection(
    process,
    labelName = 'AK15PFCHSFiltered',
    jetSource = cms.InputTag('ak15PFJetsCHSFiltered'),
    jetCorrections = ('AK10PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    trackSource = cms.InputTag('unpackedTracksAndVertices'),
    pvSource = cms.InputTag('unpackedTracksAndVertices'),
    btagDiscriminators = ['combinedSecondaryVertexBJetTags'],
    getJetMCFlavour = False
    )

addJetCollection(
    process,
    labelName = 'AK15PFCHSFilteredSubjets',
    jetSource = cms.InputTag('ak15PFJetsCHSFiltered','SubJets'),
    jetCorrections = ('AK10PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'None'),
    trackSource = cms.InputTag('unpackedTracksAndVertices'),
    pvSource = cms.InputTag('unpackedTracksAndVertices'),
    btagDiscriminators = ['combinedSecondaryVertexBJetTags'],
    getJetMCFlavour = False,
    )

process.patJetsAK15PFCHSFilteredPacked = cms.EDProducer("BoostedJetMerger",
                                                        jetSrc=cms.InputTag("patJetsAK15PFCHSFiltered" ),
                                                        subjetSrc=cms.InputTag("patJetsAK15PFCHSFilteredSubjets")
                                                        )

for module in [process.patJetPartonMatchAK8PFCHSFiltered, process.patJetPartonMatchAK10PFCHSFiltered, process.patJetPartonMatchAK12PFCHSFiltered, process.patJetPartonMatchAK15PFCHSFiltered,
               process.patJetPartonMatchAK8PFCHSFilteredSubjets, process.patJetPartonMatchAK10PFCHSFilteredSubjets, process.patJetPartonMatchAK12PFCHSFilteredSubjets, process.patJetPartonMatchAK15PFCHSFilteredSubjets]:
    module.matched='prunedGenParticles'

for module in [process.patJetCorrFactorsAK8PFCHSFiltered, process.patJetCorrFactorsAK10PFCHSFiltered, process.patJetCorrFactorsAK12PFCHSFiltered, process.patJetCorrFactorsAK15PFCHSFiltered,
               process.patJetCorrFactorsAK8PFCHSFilteredSubjets, process.patJetCorrFactorsAK10PFCHSFilteredSubjets, process.patJetCorrFactorsAK12PFCHSFilteredSubjets, process.patJetCorrFactorsAK15PFCHSFilteredSubjets]:
    module.primaryVertices = 'offlineSlimmedPrimaryVertices'
    
for module in [process.patJetGenJetMatchAK8PFCHSFiltered, process.patJetGenJetMatchAK10PFCHSFiltered, process.patJetGenJetMatchAK12PFCHSFiltered, process.patJetGenJetMatchAK15PFCHSFiltered,
               process.patJetGenJetMatchAK8PFCHSFilteredSubjets, process.patJetGenJetMatchAK10PFCHSFilteredSubjets, process.patJetGenJetMatchAK12PFCHSFilteredSubjets, process.patJetGenJetMatchAK15PFCHSFilteredSubjets]:
    module.matched = 'ak3GenJets'


#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

process.selectedPatJetsAK4PFCHS = cms.EDFilter("PATJetSelector",
                                               src = cms.InputTag("patJetsAK4PFCHS"),
                                               cut = cms.string("pt > 15.0")
                                               )
process.selectedPatJetsAK8PFCHS =process.selectedPatJetsAK4PFCHS.clone(cut="pt > 150.0", src="patJetsAK8PFCHS")
process.selectedPatJetsAK10PFCHS=process.selectedPatJetsAK4PFCHS.clone(cut="pt > 150.0", src="patJetsAK10PFCHS")
process.selectedPatJetsAK12PFCHS=process.selectedPatJetsAK4PFCHS.clone(cut="pt > 150.0", src="patJetsAK12PFCHS")
process.selectedPatJetsAK15PFCHS=process.selectedPatJetsAK4PFCHS.clone(cut="pt > 150.0", src="patJetsAK15PFCHS")

process.selectedPatJetsAK8PFCHSFilteredPacked =process.selectedPatJetsAK4PFCHS.clone(cut="pt > 150.0", src="patJetsAK8PFCHSFilteredPacked")
process.selectedPatJetsAK10PFCHSFilteredPacked=process.selectedPatJetsAK4PFCHS.clone(cut="pt > 150.0", src="patJetsAK10PFCHSFilteredPacked")
process.selectedPatJetsAK12PFCHSFilteredPacked=process.selectedPatJetsAK4PFCHS.clone(cut="pt > 150.0", src="patJetsAK12PFCHSFilteredPacked")
process.selectedPatJetsAK15PFCHSFilteredPacked=process.selectedPatJetsAK4PFCHS.clone(cut="pt > 150.0", src="patJetsAK15PFCHSFilteredPacked")

from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
process.goodPatJetsAK4PFCHS = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                           filterParams = pfJetIDSelector.clone(),
                                           src = cms.InputTag("selectedPatJetsAK4PFCHS")
                                           )
process.goodPatJetsAK8PFCHS=process.goodPatJetsAK4PFCHS.clone(src="selectedPatJetsAK8PFCHS")
process.goodPatJetsAK10PFCHS=process.goodPatJetsAK4PFCHS.clone(src="selectedPatJetsAK10PFCHS")
process.goodPatJetsAK12PFCHS=process.goodPatJetsAK4PFCHS.clone(src="selectedPatJetsAK12PFCHS")
process.goodPatJetsAK15PFCHS=process.goodPatJetsAK4PFCHS.clone(src="selectedPatJetsAK15PFCHS")

process.goodPatJetsAK8PFCHSFilteredPacked =process.goodPatJetsAK4PFCHS.clone(src="selectedPatJetsAK8PFCHSFilteredPacked")
process.goodPatJetsAK10PFCHSFilteredPacked=process.goodPatJetsAK4PFCHS.clone(src="selectedPatJetsAK10PFCHSFilteredPacked")
process.goodPatJetsAK12PFCHSFilteredPacked=process.goodPatJetsAK4PFCHS.clone(src="selectedPatJetsAK12PFCHSFilteredPacked")
process.goodPatJetsAK15PFCHSFilteredPacked=process.goodPatJetsAK4PFCHS.clone(src="selectedPatJetsAK15PFCHSFilteredPacked")

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#JECs for telescoping

process.load('JetMETCorrections/Configuration/JetCorrectionServices_cff')
#process.load('JetMETCorrections/Configuration/JetCorrectionProducers_cff')

#L1Offset correction is bad, we want L1Fastjet
process.ak1PFchsL1Fastjet   = process.ak4PFCHSL1Fastjet.clone( algorithm = 'AK1PFchs' )
process.ak2PFchsL1Fastjet   = process.ak4PFCHSL1Fastjet.clone( algorithm = 'AK2PFchs' )
process.ak3PFchsL1Fastjet   = process.ak4PFCHSL1Fastjet.clone( algorithm = 'AK3PFchs' )
process.ak4PFchsL1Fastjet   = process.ak4PFCHSL1Fastjet.clone( algorithm = 'AK4PFchs' )
process.ak5PFchsL1Fastjet   = process.ak4PFCHSL1Fastjet.clone( algorithm = 'AK5PFchs' )
process.ak6PFchsL1Fastjet   = process.ak4PFCHSL1Fastjet.clone( algorithm = 'AK6PFchs' )
process.ak7PFchsL1Fastjet   = process.ak4PFCHSL1Fastjet.clone( algorithm = 'AK7PFchs' )
process.ak8PFchsL1Fastjet   = process.ak4PFCHSL1Fastjet.clone( algorithm = 'AK8PFchs' )
process.ak9PFchsL1Fastjet   = process.ak4PFCHSL1Fastjet.clone( algorithm = 'AK9PFchs' )
process.ak10PFchsL1Fastjet  = process.ak4PFCHSL1Fastjet.clone( algorithm = 'AK10PFchs')

process.ak1PFchsL2Relative  = process.ak4PFCHSL2Relative.clone( algorithm = 'AK1PFchs' )
process.ak2PFchsL2Relative  = process.ak4PFCHSL2Relative.clone( algorithm = 'AK2PFchs' )
process.ak3PFchsL2Relative  = process.ak4PFCHSL2Relative.clone( algorithm = 'AK3PFchs' )
process.ak4PFchsL2Relative  = process.ak4PFCHSL2Relative.clone( algorithm = 'AK4PFchs' )
process.ak5PFchsL2Relative  = process.ak4PFCHSL2Relative.clone( algorithm = 'AK5PFchs' )
process.ak6PFchsL2Relative  = process.ak4PFCHSL2Relative.clone( algorithm = 'AK6PFchs' )
process.ak7PFchsL2Relative  = process.ak4PFCHSL2Relative.clone( algorithm = 'AK7PFchs' )
process.ak8PFchsL2Relative  = process.ak4PFCHSL2Relative.clone( algorithm = 'AK8PFchs' )
process.ak9PFchsL2Relative  = process.ak4PFCHSL2Relative.clone( algorithm = 'AK9PFchs' )
process.ak10PFchsL2Relative = process.ak4PFCHSL2Relative.clone( algorithm = 'AK10PFchs')

process.ak1PFCHSL3Absolute  = process.ak4PFCHSL3Absolute.clone( algorithm = 'AK1PFchs' )
process.ak2PFCHSL3Absolute  = process.ak4PFCHSL3Absolute.clone( algorithm = 'AK2PFchs' )
process.ak3PFCHSL3Absolute  = process.ak4PFCHSL3Absolute.clone( algorithm = 'AK3PFchs' )
process.ak4PFCHSL3Absolute  = process.ak4PFCHSL3Absolute.clone( algorithm = 'AK4PFchs' )
process.ak5PFCHSL3Absolute  = process.ak4PFCHSL3Absolute.clone( algorithm = 'AK5PFchs' )
process.ak6PFCHSL3Absolute  = process.ak4PFCHSL3Absolute.clone( algorithm = 'AK6PFchs' )
process.ak7PFCHSL3Absolute  = process.ak4PFCHSL3Absolute.clone( algorithm = 'AK7PFchs' )
process.ak8PFCHSL3Absolute  = process.ak4PFCHSL3Absolute.clone( algorithm = 'AK8PFchs' )
process.ak9PFCHSL3Absolute  = process.ak4PFCHSL3Absolute.clone( algorithm = 'AK9PFchs' )
process.ak10PFCHSL3Absolute = process.ak4PFCHSL3Absolute.clone( algorithm = 'AK10PFchs')

process.ak1PFCHSL1L2L3      = process.ak4PFCHSL1L2L3.clone( correctors = ['ak1PFchsL1Fastjet', 'ak1PFchsL2Relative', 'ak1PFCHSL3Absolute'] )
process.ak2PFCHSL1L2L3      = process.ak4PFCHSL1L2L3.clone( correctors = ['ak2PFchsL1Fastjet', 'ak2PFchsL2Relative', 'ak2PFCHSL3Absolute'] )
process.ak3PFCHSL1L2L3      = process.ak4PFCHSL1L2L3.clone( correctors = ['ak3PFchsL1Fastjet', 'ak3PFchsL2Relative', 'ak3PFCHSL3Absolute'] )
process.ak4PFCHSL1L2L3      = process.ak4PFCHSL1L2L3.clone( correctors = ['ak4PFchsL1Fastjet', 'ak4PFchsL2Relative', 'ak4PFCHSL3Absolute'] )
process.ak5PFCHSL1L2L3      = process.ak4PFCHSL1L2L3.clone( correctors = ['ak5PFchsL1Fastjet', 'ak5PFchsL2Relative', 'ak5PFCHSL3Absolute'] )
process.ak6PFCHSL1L2L3      = process.ak4PFCHSL1L2L3.clone( correctors = ['ak6PFchsL1Fastjet', 'ak6PFchsL2Relative', 'ak6PFCHSL3Absolute'] )
process.ak7PFCHSL1L2L3      = process.ak4PFCHSL1L2L3.clone( correctors = ['ak7PFchsL1Fastjet', 'ak7PFchsL2Relative', 'ak7PFCHSL3Absolute'] )
process.ak8PFCHSL1L2L3      = process.ak4PFCHSL1L2L3.clone( correctors = ['ak8PFchsL1Fastjet', 'ak8PFchsL2Relative', 'ak8PFCHSL3Absolute'] )
process.ak9PFCHSL1L2L3      = process.ak4PFCHSL1L2L3.clone( correctors = ['ak9PFchsL1Fastjet', 'ak9PFchsL2Relative', 'ak9PFCHSL3Absolute'] )
process.ak10PFCHSL1L2L3     = process.ak4PFCHSL1L2L3.clone( correctors = ['ak10PFchsL1Fastjet','ak10PFchsL2Relative','ak10PFCHSL3Absolute'])

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
process.load('RecoJets.JetProducers.jettoolbox_cff')
"""
process.NjettinessAK10=process.NjettinessAK8.clone(src="ak10PFJetsCHS", cone=1.0)
process.NjettinessAK12=process.NjettinessAK8.clone(src="ak12PFJetsCHS", cone=1.2)
process.NjettinessAK15=process.NjettinessAK8.clone(src="ak15PFJetsCHS", cone=1.5)

process.RandomNumberGeneratorService=process.RandomNumberGeneratorService.clone(QJetsAdderAK10 = cms.PSet(initialSeed = cms.untracked.uint32(14)),
                                                                                QJetsAdderAK12 = cms.PSet(initialSeed = cms.untracked.uint32(31)),
                                                                                QJetsAdderAK15 = cms.PSet(initialSeed = cms.untracked.uint32(420)))

process.QJetsAdderAK10=process.QJetsAdderAK8.clone(src="ak10PFJetsCHS", jetRad=1.0)
process.QJetsAdderAK12=process.QJetsAdderAK8.clone(src="ak12PFJetsCHS", jetRad=1.2)
process.QJetsAdderAK15=process.QJetsAdderAK8.clone(src="ak15PFJetsCHS", jetRad=1.5)

process.AK8PFJetsCHSPrunedLinks=process.ak8PFJetsCHSPrunedLinks.clone()
process.AK10PFJetsCHSPrunedLinks=process.AK8PFJetsCHSPrunedLinks.clone(src="ak10PFJetsCHS", matched="ak10PFJetsCHSPruned", distMax=1.0)
process.AK12PFJetsCHSPrunedLinks=process.AK8PFJetsCHSPrunedLinks.clone(src="ak12PFJetsCHS", matched="ak12PFJetsCHSPruned", distMax=1.2)
process.AK15PFJetsCHSPrunedLinks=process.AK8PFJetsCHSPrunedLinks.clone(src="ak15PFJetsCHS", matched="ak15PFJetsCHSPruned", distMax=1.5)

process.AK8PFJetsCHSTrimmedLinks=process.ak8PFJetsCHSTrimmedLinks.clone()
process.AK10PFJetsCHSTrimmedLinks=process.AK8PFJetsCHSTrimmedLinks.clone(src="ak10PFJetsCHS", matched="ak10PFJetsCHSTrimmed", distMax=1.0)
process.AK12PFJetsCHSTrimmedLinks=process.AK8PFJetsCHSTrimmedLinks.clone(src="ak12PFJetsCHS", matched="ak12PFJetsCHSTrimmed", distMax=1.2)
process.AK15PFJetsCHSTrimmedLinks=process.AK8PFJetsCHSTrimmedLinks.clone(src="ak15PFJetsCHS", matched="ak15PFJetsCHSTrimmed", distMax=1.5)

process.AK8PFJetsCHSFilteredLinks=process.ak8PFJetsCHSFilteredLinks.clone()
process.AK10PFJetsCHSFilteredLinks=process.AK8PFJetsCHSFilteredLinks.clone(src="ak10PFJetsCHS", matched="ak10PFJetsCHSFiltered", distMax=1.0)
process.AK12PFJetsCHSFilteredLinks=process.AK8PFJetsCHSFilteredLinks.clone(src="ak12PFJetsCHS", matched="ak12PFJetsCHSFiltered", distMax=1.2)
process.AK15PFJetsCHSFilteredLinks=process.AK8PFJetsCHSFilteredLinks.clone(src="ak15PFJetsCHS", matched="ak15PFJetsCHSFiltered", distMax=1.5)

process.patJetsAK8PFCHS.userData.userFloats.src += ['NjettinessAK8:tau1','NjettinessAK8:tau2','NjettinessAK8:tau3',
                                                    'QJetsAdderAK8:QjetsVolatility',
                                                    'AK8PFJetsCHSPrunedLinks','AK8PFJetsCHSTrimmedLinks','AK8PFJetsCHSFilteredLinks']

process.patJetsAK10PFCHS.userData.userFloats.src += ['NjettinessAK10:tau1','NjettinessAK10:tau2','NjettinessAK10:tau3',
                                                    'QJetsAdderAK10:QjetsVolatility',
                                                    'AK10PFJetsCHSPrunedLinks','AK10PFJetsCHSTrimmedLinks','AK10PFJetsCHSFilteredLinks']

process.patJetsAK12PFCHS.userData.userFloats.src += ['NjettinessAK12:tau1','NjettinessAK12:tau2','NjettinessAK12:tau3',
                                                    'QJetsAdderAK12:QjetsVolatility',
                                                    'AK12PFJetsCHSPrunedLinks','AK12PFJetsCHSTrimmedLinks','AK12PFJetsCHSFilteredLinks']

process.patJetsAK15PFCHS.userData.userFloats.src += ['NjettinessAK15:tau1','NjettinessAK15:tau2','NjettinessAK15:tau3',
                                                    'QJetsAdderAK15:QjetsVolatility',
                                                    'AK15PFJetsCHSPrunedLinks','AK15PFJetsCHSTrimmedLinks','AK15PFJetsCHSFilteredLinks']
"""
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                                                             
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 10
process.MessageLogger.suppressWarning = cms.untracked.vstring('ecalLaserCorrFilter','manystripclus53X','toomanystripclus53X')
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.options.allowUnscheduled = cms.untracked.bool(True)

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('Hbb.root'),
                               outputCommands = cms.untracked.vstring(['keep *_HbbProducer_*_*',
                                                                       ])
)

process.end = cms.EndPath(process.out)
