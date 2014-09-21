from os import system

jobs=[#'REQUESTNAME','INPUTDATASET','PUBLISHDATANAME'],
    ['Zh_PU20bx25','/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM','PU20bx25'],
    ['ZJets_PU20bx25','/DYJetsToMuMu_PtZ-180_M-50_13TeV-madgraph/Spring14miniaod-PU20bx25_POSTLS170_V5-v1/MINIAODSIM','PU20bx25'],
    ['ttbar_PU20bx25','/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Spring14miniaod-PU20bx25_POSTLS170_V5-v2/MINIAODSIM','PU20bx25'],
    ]

template='python/crabTemplate.py'

#---------------------------------------------------------------------------------------------------------------------------------------------------

for job in jobs:
    requestName=job[0]
    inputDS=job[1]
    publishDN=job[2]

    config='python/'+requestName+'.py'
    system('cp '+template+' '+config)
    system('sed s%REQUESTNAME%'+requestName+'%g '+config+' --in-place')
    system('sed s%INPUTDATASET%'+inputDS+'%g '+config+' --in-place')
    system('sed s%PUBLISHDATANAME%'+publishDN+'%g '+config+' --in-place')

    system('crab submit '+config)
