import FWCore.ParameterSet.Config as cms

#HbbAnalyzer = cms.EDAnalyzer('GroomHbbAnalyzer',
HbbAnalyzer = cms.EDAnalyzer('HbbAnalyzer',
                      HbbSource=cms.InputTag('HbbProducer')
)
