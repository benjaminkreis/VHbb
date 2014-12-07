#!/bin/bash
theDir=$1
condorDir=$PWD

source /cvmfs/cms.cern.ch/cmsset_default.sh

cd $theDir
eval `scramv1 runtime -sh`

#cp doPostProc.py $condorDir
python doPostProc.py $condorDir
