import FWCore.ParameterSet.Config as cms

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        #'file:/uscms/home/aperloff/nobackup/YOURWORKINGAREA/VHbb/CMSSW_7_1_0_pre9/src/VHbb/HbbProducer/python/Hbb.root'
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_1.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_2.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_3.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_4.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_5.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_6.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_7.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_8.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_9.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_10.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_11.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_12.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_13.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_14.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_15.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_16.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_17.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_18.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_19.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_20.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_21.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_22.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_23.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_24.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_25.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_26.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_27.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_28.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_29.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_30.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_31.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_32.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_33.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_34.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_35.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_36.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_37.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_38.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_39.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_40.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_41.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_42.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_43.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_44.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_45.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_46.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_47.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_48.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_49.root',
        'file:/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/0000/Hbb_50.root'
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
