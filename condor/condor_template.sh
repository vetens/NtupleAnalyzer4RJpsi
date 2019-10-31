#!/bin/bash

cd WORKDIR
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
source /cvmfs/cms.cern.ch/crab3/crab.sh
export X509_USER_PROXY=userproxy
export PYTHONPATH=$PYTHONPATH:/cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/python/2.7.14-omkpbe4/bin/python
./run.py -x -l LISTDIR/listLISTNUMBER -o TARGETRUNTYPECondorJob_JOBNUMBER.root
