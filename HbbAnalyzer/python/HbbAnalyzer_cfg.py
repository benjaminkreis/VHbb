import FWCore.ParameterSet.Config as cms
import glob

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        ######################
        #My cmsRun Production#
        ######################
        #'file:/uscms/home/aperloff/nobackup/YOURWORKINGAREA/VHbb/CMSSW_7_1_0_pre9/src/VHbb/HbbProducer/python/Hbb.root'
        ####
        #ZH#
        ####
        ('file:%s ' % name) for name in glob.glob('/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_noMuIso/141001_010002/0000/Hbb*.root')
        #######
        #ZJets#
        #######
        #('file:%s ' % name) for name in glob.glob('/eos/uscms/store/user/lpcmbja/noreplica/DYJetsToLL_M-50_13TeV-madgraph-pythia8/PU40bx50_PLS170_V6AN1_noMuIso/141001_010020/*/Hbb*.root')
        ########
        #TTJets#
        ########
        #('file:%s ' % name) for name in glob.glob('/eos/uscms/store/user/lpcmbja/noreplica/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/PU40bx50_PLS170_V6AN1_noMuIso/141001_010043/*/Hbb*.root')
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
