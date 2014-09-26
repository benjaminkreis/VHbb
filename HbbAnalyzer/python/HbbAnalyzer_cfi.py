import FWCore.ParameterSet.Config as cms

HbbAnalyzer = cms.EDAnalyzer('HbbAnalyzer',
                      HbbSource    			   =cms.InputTag('HbbProducer'),
                      AK4PFCHS_MinPt    	   = cms.double(25.0),
                      AK4PFCHS_MaxEta   	   = cms.double(2.4),
                      AK4PFCHS_MinCSVBTag      = cms.double(0.898), #Tight(0.898), Medium(0.679), Loose(0.244)
                      Electron_MinPt    	   = cms.double(27.0),
                      Electron_MaxEta   	   = cms.double(2.5),
                      Electron_SCExcludeMinEta = cms.double(1.4442),
                      Electron_SCExcludeMaxEta = cms.double(1.5660),
                      Muon_MinPt        	   = cms.double(24.0),
                      Muon_MaxEta       	   = cms.double(2.1),
                      Tau_MinPt         	   = cms.double(27.0),
                      Tau_MaxEta        	   = cms.double(2.5),
                      MET_MaxPt                = cms.double(9999)
)
