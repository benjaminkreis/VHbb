#!/bin/csh

#set noglob   #  prevent filename expansion with wildcard pattern matching

set pid=$argv[1]

set workDir=$ANALYZEDIRECTORY

#set isData=0
set nevts=-1

switch ($pid)
    #case 0:
    #	set inputFiles = "/eos/uscms/store/user/lpcmbja/noreplica/ZH_HToBB_ZToLL_M-125_13TeV_powheg-herwigpp/PU40bx50_PLS170_V6AN1_wBTag/140925_003953/"
    #	set outputFiles = Hbb__ZH_HToBB_ZToLL_M-125_13TeV_PU40bx50_Moreplots.root
    #	breaksw
    #case 1:
    #	set inputFiles  = "/eos/uscms/store/user/lpcmbja/noreplica/DYJetsToLL_M-50_13TeV-madgraph-pythia8/PU40bx50_PLS170_V6AN1wBTag/140925_004012/"
    #	set outputFiles = Hbb__DYJetsToLL_M-50_13TeV_PU40bx50_Moreplots.root
    #	breaksw
    #
    case 0:
 	set inputFiles = "/eos/uscms/store/user/lpcmbja/noreplica/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/PU40bx50_PLS170_V6AN1_wBTag/140925_004031/"
 	set outputFiles = Hbb__TTJets_13TeV_PU40bx50_Moreplots.root
	#$nevts = 5000000
	breaksw
	
    default:
        echo "not setup for this"
        exit 1
endsw

echo "Beginning runCondorJob.csh"

echo "-------------------------------"
echo "Current Directory: "
pwd
echo "-------------------------------"

source /uscmst1/prod/sw/cms/setup/cshrc prod
setenv SCRAM_ARCH slc6_amd64_gcc481
cd $workDir

eval `scram runtime -csh`

echo "-------------------------------"
echo "Working Directory: "
pwd
echo "-------------------------------"

cd -
pwd

cp $workDir/plugins/GroomHbbAnalyzer.cc .
cp $workDir/python/HbbAnalyzerCondor_cfg.py .
cp $workDir/python/HbbAnalyzer_cfi.py .
ls

echo "Submitting job on `date`" 
echo
echo -n "--------------------------------------------"

cmsRun HbbAnalyzerCondor_cfg.py $outputFiles $inputFiles -n $nevts

ls
cp $outputFiles /eos/uscms/store/user/ingabu/Higgs/CSA14/Anatuples/
rm $outputFiles
rm GroomHbbAnalyzer.cc
rm HbbAnalyzerCondor_cfg.py
rm HbbAnalyzer_cfi.py

echo "Job finished on `date`" 
