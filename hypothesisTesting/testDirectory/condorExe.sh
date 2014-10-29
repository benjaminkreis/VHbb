#!/bin/bash
CONDOR_SCRATCH_DIR=$PWD

dir=$1
command=""
for i in "$@"
  do
  command="$command $i"
done
command=`echo $command | cut -d ' ' -f 2-`

source /uscmst1/prod/sw/cms/shrc prod

tar -xzvf condor*tar.gz

cd $dir
eval `scramv1 runtime -sh`

touch $CONDOR_SCRATCH_DIR/startTime

echo $command
$command

find $CONDOR_SCRATCH_DIR -newer $CONDOR_SCRATCH_DIR/startTime -type f  ! -name "*pyc" -exec mv {} $CONDOR_SCRATCH_DIR \;