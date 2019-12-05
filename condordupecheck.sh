#!/bin/bash
cd /afs/cern.ch/work/w/wvetens/LowPtTau/CMSSW_10_2_9/src/YutaAnalyzer/NtupleAnalyzer4RJpsi
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
export X509_USER_PROXY=userproxy
./dupecheck.py
