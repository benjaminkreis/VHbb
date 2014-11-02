import FWCore.ParameterSet.Config as cms

HbbProducer = cms.EDProducer('HbbProducer',
                             AK4Source =cms.InputTag('goodPatJetsAK4PFCHS'),
                             muonSource=cms.InputTag('selectedMuons'),
                             electronSource=cms.InputTag('selectedElectrons'),
)
