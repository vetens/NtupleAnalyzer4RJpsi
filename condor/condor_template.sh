#!/bin/bash
cd WORKDIR
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
#export X509_USER_PROXY=userproxy
./run.py -x -l LISTDIR/listLISTNUMBER -o TARGETRUNTYPECondorJob_JOBNUMBER.root
