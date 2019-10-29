#!/bin/bash

cd /afs/cern.ch/work/w/wvetens/LowPtTau/CMSSW_10_2_9/src/YutaAnalyzer/NtupleAnalyzer4RJpsi
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
source /cvmfs/cms.cern.ch/crab3/crab.sh
export X509_USER_PROXY=userproxy
export PYTHONPATH=$PYTHONPATH:/cvmfs/cms.cern.ch/slc6_amd64_gcc700/external/python/2.7.14-omkpbe4/bin/python
./run.py -x -t LISTDIR/listLISTNUMBER -o /eos/user/w/wvetens/RUNTYPE/BJpsiX_JOBNUMBER.root
