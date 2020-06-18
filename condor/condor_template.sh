#!/bin/bash
cd WORKDIR
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 runtime -sh`
export X509_USER_PROXY=userproxy
./run.py -x ISDAT ISGEN ISSIG  -l LISTDIR/listLISTNUMBER -o WORKDIRRUNTYPECondorJob_JOBNUMBER.root
mv -f WORKDIRRUNTYPECondorJob_JOBNUMBER.root TARGETRUNTYPECondorJob_JOBNUMBER.root
