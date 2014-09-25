from os import system

jobs=[#'REQUESTNAME','INPUTDATASET','PUBLISHDATANAME','LBSPERJOB'],
    #['Zh_PU20bx25_PLS170_V7AN1',          '/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',             'PU20bx25_PLS170_V7AN1',50,  'global'],
    #['boostedZJets_PU20bx25_PLS170_V7AN1','/DYJetsToMuMu_PtZ-180_M-50_13TeV-madgraph/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM',               'PU20bx25_PLS170_V7AN1',50,  'global'],
    #['ttbar_PU20bx25_PLS170_V7AN1',       '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v2/MINIAODSIM','PU20bx25_PLS170_V7AN1',1200,'global'],
    ['Zh_PU40bx50_PLS170_V6AN1',           '/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/jstupak-Spring14dr-PU_S14_POSTLS170_V6AN1-miniAOD706p1-814812ec83fce2f620905d2bb30e9100/USER',                     'PU40bx50_PLS170_V6AN1',50,  'phys03'],
    ['ZJets_PU40bx50_PLS170_V6AN1',        '/DYJetsToLL_M-50_13TeV-madgraph-pythia8/StoreResults-Spring14dr_PU_S14_POSTLS170_V6AN1_miniAOD706p1_814812ec83fce2f620905d2bb30e9100-v1/USER',                 'PU40bx50_PLS170_V6AN1',50,  'phys03'],
    ['ttbar_PU40bx50_PLS170_V6AN1',        '/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/StoreResults-Spring14dr_PU_S14_POSTLS170_V6AN1_miniAOD706p1_814812ec83fce2f620905d2bb30e9100-v2/USER','PU40bx50_PLS170_V6AN1',1200,'phys03'],
    ]

template='python/crabTemplate.py'

#---------------------------------------------------------------------------------------------------------------------------------------------------

for job in jobs:
    requestName=job[0]
    inputDS=job[1]
    publishDN=job[2]
    LBs=str(job[3])
    dbsUrl=job[4]
    
    config='python/'+requestName+'.py'
    system('cp '+template+' '+config)
    system('sed s%REQUESTNAME%'+requestName+'%g '+config+' --in-place')
    system('sed s%INPUTDATASET%'+inputDS+'%g '+config+' --in-place')
    system('sed s%PUBLISHDATANAME%'+publishDN+'%g '+config+' --in-place')
    system('sed s%LBSPERJOB%'+LBs+'%g '+config+' --in-place')
    system('sed s%DBSURL%'+dbsUrl+'%g '+config+' --in-place')

    system('crab submit '+config)
