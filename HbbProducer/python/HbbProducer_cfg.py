import FWCore.ParameterSet.Config as cms


process = cms.Process("Hbb")
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True),
                                     allowUnscheduled = cms.untracked.bool(True) 
                                     )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
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
process.pfNoElectronsCHS = cms.EDProducer("CandPtrProjector", src = cms.InputTag("pfNoMuonCHS"), veto =  cms.InputTag("selectedElectrons"))

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


##**** Electron definition from https://github.com/cms-sw/cmssw/blob/CMSSW_7_3_X/PhysicsTools/PatAlgos/test/miniAOD/example_ei.py - IB
process.selectedElectrons = cms.EDFilter("PATElectronSelector", 
                                         src = cms.InputTag("slimmedElectrons"), 
                                         cut = cms.string('abs(eta)<2.5 &'
                                                          'pt>20. &'
                                                          'gsfTrack.isAvailable() &'
                                                          'gsfTrack.trackerExpectedHitsInner().numberOfLostHits() < 2 &'
                                                          '(pfIsolationVariables().sumChargedHadronPt+max(0.,pfIsolationVariables().sumNeutralHadronEt+pfIsolationVariables().sumPhotonEt-0.5*pfIsolationVariables().sumPUPt))/pt < 0.15'))

process.load('RecoJets.Configuration.RecoPFJets_cff')
process.load('RecoJets.Configuration.RecoGenJets_cff')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

process.selectedPatJetsAK4PFCHS = cms.EDFilter("PATJetSelector",
                                               src = cms.InputTag("slimmedJets"),
                                               cut = cms.string("pt > 15.0")
                                               )

from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
process.goodPatJetsAK4PFCHS = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                           filterParams = pfJetIDSelector.clone(),
                                           src = cms.InputTag("selectedPatJetsAK4PFCHS")
                                           )
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                                                             
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 10
process.MessageLogger.suppressWarning = cms.untracked.vstring('ecalLaserCorrFilter','manystripclus53X','toomanystripclus53X')
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.options.allowUnscheduled = cms.untracked.bool(True)

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('HbbEle.root'),
                               outputCommands = cms.untracked.vstring(['keep *_HbbProducer_*_*',
                                                                       ])
)

process.end = cms.EndPath(process.out)
