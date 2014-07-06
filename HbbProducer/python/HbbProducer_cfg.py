import FWCore.ParameterSet.Config as cms

process = cms.Process("Hbb")
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True),
                                     allowUnscheduled = cms.untracked.bool(True) 
                                     )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring('file:/eos/uscms/store/user/jstupak/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/Spring14dr-PU_S14_POSTLS170_V6AN1-v1/140622_185946/0000/miniAOD-prod_PAT_1.root'
                                                              )
                            )

theGlobalTag='PLS170_V6AN1::All'

process.load("FWCore.MessageService.MessageLogger_cfi")

process.load('VHbb.HbbProducer.HbbProducer_cfi')

#####################################################################################################################################

process.load('PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.Geometry_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = theGlobalTag

process.chs = cms.EDFilter('CandPtrSelector', src = cms.InputTag('packedPFCandidates'), cut = cms.string('fromPV'))


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
                                                      'abs(dB) < 0.02 &'
                                                      'innerTrack.hitPattern.numberOfValidPixelHits > 0 &'
                                                      'innerTrack.hitPattern.trackerLayersWithMeasurement > 5'
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
process.ak4PFJetsCHS.src = 'chs'

process.ak8PFJetsCHS = process.ak4PFJets.clone( rParam = 0.8 )
process.ak10PFJetsCHS = process.ak4PFJetsCHS.clone(rParam = 1)
process.ak12PFJetsCHS = process.ak4PFJetsCHS.clone(rParam = 1.2)
process.ak15PFJetsCHS = process.ak4PFJetsCHS.clone(rParam = 1.5)

process.ak4GenJets.src = 'packedGenParticles'
process.ak8GenJets = process.ak4GenJets.clone(rParam = 0.8)
process.ak10GenJets = process.ak8GenJets.clone(rParam = 1)
process.ak12GenJets = process.ak8GenJets.clone(rParam = 12)
process.ak15GenJets = process.ak8GenJets.clone(rParam = 15)

process.ak8PFJetsCHSPruned.src = 'chs'
process.ak8PFJetsCHSTrimmed.src = 'chs'
process.ak8PFJetsCHSFiltered.src = 'chs'

process.ak10PFJetsCHSPruned = process.ak8PFJetsCHSPruned.clone(rParam = 1)
process.ak10PFJetsCHSTrimmed = process.ak8PFJetsCHSTrimmed.clone(rParam = 1)
process.ak10PFJetsCHSFiltered = process.ak8PFJetsCHSFiltered.clone(rParam = 1)

process.ak12PFJetsCHSPruned = process.ak8PFJetsCHSPruned.clone(rParam = 1.2)
process.ak12PFJetsCHSTrimmed = process.ak8PFJetsCHSTrimmed.clone(rParam = 1.2)
process.ak12PFJetsCHSFiltered = process.ak8PFJetsCHSFiltered.clone(rParam = 1.2)

process.ak15PFJetsCHSPruned = process.ak8PFJetsCHSPruned.clone(rParam = 1.5)
process.ak15PFJetsCHSTrimmed = process.ak8PFJetsCHSTrimmed.clone(rParam = 1.5)
process.ak15PFJetsCHSFiltered = process.ak8PFJetsCHSFiltered.clone(rParam = 1.5)

process.cmsTopTagPFJetsCHS.src = 'chs'

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
    )

switchJetCollection(
    process,
    jetSource = cms.InputTag('ak4PFJets'),
    algo = 'ak4',
    rParam = 0.4,
    jetCorrections = ('AK5PF', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute']), 'Type-1'),
    # btagDiscriminators = ['jetBProbabilityBJetTags',
    #                       'jetProbabilityBJetTags',
    #                       'trackCountingHighPurBJetTags',
    #                       'trackCountingHighEffBJetTags',
    #                       'simpleSecondaryVertexHighEffBJetTags',
    #                       'simpleSecondaryVertexHighPurBJetTags',
    #                       'combinedSecondaryVertexBJetTags'
    #                       ],
    trackSource = cms.InputTag('unpackedTracksAndVertices'),
    pvSource = cms.InputTag('unpackedTracksAndVertices'),
    )


process.patJetsAK4PFCHS.addJetCharge   = False
process.patJetsAK4PFCHS.addBTagInfo    = True
process.patJetsAK4PFCHS.getJetMCFlavour = False
process.patJetsAK4PFCHS.addAssociatedTracks = False
process.patJetPartonMatchAK4PFCHS.matched='prunedGenParticles'
process.patJetCorrFactorsAK4PFCHS.primaryVertices = 'offlineSlimmedPrimaryVertices'

for module in [process.patJetsAK8PFCHS, process.patJetsAK10PFCHS, process.patJetsAK12PFCHS, process.patJetsAK15PFCHS]:
    module.addJetCharge   = False
    module.addBTagInfo    = False    #For some reason this has to be False 
    module.getJetMCFlavour = False
    module.addAssociatedTracks = False

process.patJetPartonMatchAK8PFCHS.matched='prunedGenParticles'
process.patJetCorrFactorsAK8PFCHS.primaryVertices = 'offlineSlimmedPrimaryVertices'

process.patJetPartonMatchAK10PFCHS.matched='prunedGenParticles'
process.patJetCorrFactorsAK10PFCHS.primaryVertices = 'offlineSlimmedPrimaryVertices'

process.patJetPartonMatchAK12PFCHS.matched='prunedGenParticles'
process.patJetCorrFactorsAK12PFCHS.primaryVertices = 'offlineSlimmedPrimaryVertices'

process.patJetPartonMatchAK15PFCHS.matched='prunedGenParticles'
process.patJetCorrFactorsAK15PFCHS.primaryVertices = 'offlineSlimmedPrimaryVertices'

process.patJetPartonMatch.matched = 'prunedGenParticles'
process.patJetCorrFactors.primaryVertices = 'offlineSlimmedPrimaryVertices'

process.load('RecoBTag.Configuration.RecoBTag_cff')
process.load('RecoJets.Configuration.RecoJetAssociations_cff')
process.load('PhysicsTools.PatAlgos.slimming.unpackedTracksAndVertices_cfi')

process.ak4JetTracksAssociatorAtVertexPF.jets = cms.InputTag('ak4PFJetsCHS')
process.ak4JetTracksAssociatorAtVertexPF.tracks = cms.InputTag('unpackedTracksAndVertices')
process.ak8JetTracksAssociatorAtVertexPF=process.ak4JetTracksAssociatorAtVertexPF.clone(jets = cms.InputTag('ak8PFJetsCHS'), coneSize = 0.8)
process.ak10JetTracksAssociatorAtVertexPF=process.ak4JetTracksAssociatorAtVertexPF.clone(jets = cms.InputTag('ak10PFJetsCHS'), coneSize = 1)
process.ak12JetTracksAssociatorAtVertexPF=process.ak4JetTracksAssociatorAtVertexPF.clone(jets = cms.InputTag('ak12PFJetsCHS'), coneSize = 1.2)
process.ak15JetTracksAssociatorAtVertexPF=process.ak4JetTracksAssociatorAtVertexPF.clone(jets = cms.InputTag('ak15PFJetsCHS'), coneSize = 1.5)

process.impactParameterTagInfos.primaryVertex = cms.InputTag('unpackedTracksAndVertices')
process.inclusiveSecondaryVertexFinderTagInfos.extSVCollection = cms.InputTag('unpackedTracksAndVertices','secondary','')
process.combinedSecondaryVertex.trackMultiplicityMin = 1 #silly sv, uses un filtered tracks.. i.e. any pt                                                                        

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
process.load('RecoJets.JetProducers.jettoolbox_cff')

process.NjettinessAK10=process.NjettinessAK8.clone(src="ak10PFJetsCHS", cone=1.0)
process.NjettinessAK12=process.NjettinessAK8.clone(src="ak12PFJetsCHS", cone=1.2)
process.NjettinessAK15=process.NjettinessAK8.clone(src="ak15PFJetsCHS", cone=1.5)

process.RandomNumberGeneratorService=process.RandomNumberGeneratorService.clone(QJetsAdderAK10 = cms.PSet(initialSeed = cms.untracked.uint32(14)),
                                                                                QJetsAdderAK12 = cms.PSet(initialSeed = cms.untracked.uint32(31)),
                                                                                QJetsAdderAK15 = cms.PSet(initialSeed = cms.untracked.uint32(420)))

process.QJetsAdderAK10=process.QJetsAdderAK8.clone(src="ak10PFJetsCHS", jetRad=1.0)
process.QJetsAdderAK12=process.QJetsAdderAK8.clone(src="ak12PFJetsCHS", jetRad=1.2)
process.QJetsAdderAK15=process.QJetsAdderAK8.clone(src="ak15PFJetsCHS", jetRad=1.5)

process.load('RecoJets.JetProducers.ak4PFJetsPruned_cfi')
ak10PFJetsCHSPruned=process.ak4PFJetsPruned.clone(rParam=1.0)
ak12PFJetsCHSPruned=process.ak4PFJetsPruned.clone(rParam=1.2)
ak15PFJetsCHSPruned=process.ak4PFJetsPruned.clone(rParam=1.5)

process.load('RecoJets.JetProducers.ak4PFJetsTrimmed_cfi')
ak10PFJetsCHSTrimmed=process.ak4PFJetsTrimmed.clone(rParam=1.0)
ak12PFJetsCHSTrimmed=process.ak4PFJetsTrimmed.clone(rParam=1.2)
ak15PFJetsCHSTrimmed=process.ak4PFJetsTrimmed.clone(rParam=1.5)

process.load('RecoJets.JetProducers.ak4PFJetsFiltered_cfi')
ak10PFJetsCHSFiltered=process.ak4PFJetsFiltered.clone(rParam=1.0)
ak12PFJetsCHSFiltered=process.ak4PFJetsFiltered.clone(rParam=1.2)
ak15PFJetsCHSFiltered=process.ak4PFJetsFiltered.clone(rParam=1.5)

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
