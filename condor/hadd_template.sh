#!/bin/bash
cd WORKDIR
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
export X509_USER_PROXY=userproxy
hadd -f TARGETRUNTYPEBtrimu.root TARGETRUNTYPECondorJob_*.root
