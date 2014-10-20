import FWCore.ParameterSet.Config as cms

HbbProducer = cms.EDProducer('HbbProducer',
                             rhoSource=cms.InputTag('fixedGridRhoFastjetAll'),

                             packedCandidateSource=cms.InputTag('pfNoElectronsCHS'),
                             prunedGenParticleSource=cms.InputTag('prunedGenParticles'),
                             packedGenParticleSource=cms.InputTag('packedGenParticles'),

                             AK4Source =cms.InputTag('goodPatJetsAK4PFCHS'),
                             AK8Source =cms.InputTag('goodPatJetsAK8PFCHS'),
                             AK10Source=cms.InputTag('goodPatJetsAK10PFCHS'),
                             AK12Source=cms.InputTag('goodPatJetsAK12PFCHS'),
                             AK15Source=cms.InputTag('goodPatJetsAK15PFCHS'),

                             AK8PackedSource =cms.InputTag('goodPatJetsAK8PFCHSFilteredPacked'),
                             AK10PackedSource=cms.InputTag('goodPatJetsAK10PFCHSFilteredPacked'),
                             AK12PackedSource=cms.InputTag('goodPatJetsAK12PFCHSFilteredPacked'),
                             AK15PackedSource=cms.InputTag('goodPatJetsAK15PFCHSFilteredPacked'),
                             
                             AK4GenSource =cms.InputTag('ak4GenJets'),
                             
                             muonSource=cms.InputTag('selectedMuons'),
                             electronSource=cms.InputTag('selectedElectrons'),
)
