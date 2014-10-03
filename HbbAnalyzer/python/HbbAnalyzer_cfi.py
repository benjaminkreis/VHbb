import FWCore.ParameterSet.Config as cms

HbbAnalyzer = cms.EDAnalyzer('HbbAnalyzer',
                      HbbSource    			   =cms.InputTag('HbbProducer'),
                      NInterpretations         = cms.uint32(15),
                      theV_MinMass             = cms.double(70.0),
                      theV_MaxMass             = cms.double(110.0),
                      theV_MinPt               = cms.double(50.0),
                      AK4PFCHS_MinPt    	   = cms.double(25.0),
                      AK4PFCHS_MaxEta   	   = cms.double(2.4),
                      AK4PFCHS_MinCSVBTag      = cms.double(0.679), #Tight(0.898), Medium(0.679), Loose(0.244)
                      Electron_MinPt    	   = cms.double(27.0),
                      Electron_MaxEta   	   = cms.double(2.5),
                      Electron_SCExcludeMinEta = cms.double(1.4442),
                      Electron_SCExcludeMaxEta = cms.double(1.5660),
                      Electron_MaxIso          = cms.double(0.1),
                      Muon_MinPt        	   = cms.double(24.0),
                      Muon_MaxEta       	   = cms.double(2.1),
                      Muon_MaxIso              = cms.double(0.2), #2012 POG recomendation (0.12)
                      Tau_MinPt         	   = cms.double(27.0),
                      Tau_MaxEta        	   = cms.double(2.5),
                      Tau_MaxIso               = cms.double(0.1),
                      MET_MaxPt                = cms.double(9999)
)
