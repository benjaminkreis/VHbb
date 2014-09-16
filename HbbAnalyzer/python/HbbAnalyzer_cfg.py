import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        'file:/uscms/home/aperloff/nobackup/YOURWORKINGAREA/VHbb/CMSSW_7_1_0_pre9/src/VHbb/HbbProducer/test/Hbb.root'
    )
)

process.load('VHbb.HbbAnalyzer.HbbAnalyzer_cfi')

#process.demo = cms.EDAnalyzer('HbbAnalyzer'
#)

process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.suppressWarning = cms.untracked.vstring('ecalLaserCorrFilter','manystripclus53X','toomanystripclus53X')
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.options.allowUnscheduled = cms.untracked.bool(True)

process.load('CommonTools.UtilAlgos.TFileService_cfi')
process.TFileService.fileName=cms.string('HbbAna.root')
#process.out = cms.OutputModule("PoolOutputModule",
#                               fileName = cms.untracked.string('HbbAna.root'),
#                               outputCommands = cms.untracked.vstring(['keep *_HbbAnalyzer_*_*',
#                                                                       ])
#)

#process.end = cms.EndPath(process.out)
process.p = cms.Path(process.HbbAnalyzer)
