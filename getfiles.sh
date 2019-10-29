#!/bin/bash
# The first option says whether you are running on data or Monte Carlo, so make it either
# data
# or
# MC
# or 
# signalmc
# The second option says whether or not you are also splitting these jobs for condor. If you make option 2
# condor
# then this script will automatically split the text lists according to the splitting defined in option 3
# default splitting 10
# it will then also automatically generate condor scripts if the condor option is selected
runtype=${1:-'MC'}
iscondor=${2:-'no'}
splitting=${3:-10}
if [ ! -d lists/$runtype ]; then
    mkdir -p lists/$runtype;
    if [ $iscondor = 'condor' ] && [ ! -d lists/$runtype/condor ]; then
        mkdir -p lists/$runtype/condor;
    fi
fi
cd lists/$runtype
if [ $runtype = 'MC' ]; then
    uberftp -ls gsiftp://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat/store/user/cgalloni/Ntuple_BPH_v0/BJpsiX_MuMu_031019/BJpsiX_MuMu_031019/191014_123225/0000/ > list.txt;
    awk '{printf("%s\n", $9)}' <list.txt | tr -d '\r'> list2.txt;
    sed -i '/log/d' list2.txt;
    rm list.txt;
    awk '{print "root://cms-xrd-global.cern.ch//store/user/cgalloni/Ntuple_BPH_v0/BJpsiX_MuMu_031019/BJpsiX_MuMu_031019/191014_123225/0000/"$0}' list2.txt > list.txt;
    rm list2.txt;
elif [ $runtype = 'data' ]; then
#     uberftp -ls gsiftp://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat/store/user/cgalloni/Ntuple_BPH_v0/Charmonium/Charmonium_Run2018A-17Sep2018-v1/191014_123757/0000/ > listA.txt;
#     awk '{printf("%s\n", $9)}' <listA.txt | tr -d '\r'> list2A.txt;
#     sed -i '/log/d' list2A.txt;
#     rm listA.txt;
#     awk '{print "root://cms-xrd-global.cern.ch//store/user/cgalloni/Ntuple_BPH_v0/Charmonium/Charmonium_Run2018A-17Sep2018-v1/191014_123757/0000/"$0}' list2A.txt > listA.txt;
#     rm list2A.txt;
#     
#     uberftp -ls gsiftp://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat/store/user/cgalloni/Ntuple_BPH_v0/Charmonium/Charmonium_Run2018B-17Sep2018-v1/191014_123757/0000/ > listB.txt;
#     awk '{printf("%s\n", $9)}' <listB.txt | tr -d '\r'> list2B.txt;
#     sed -i '/log/d' list2B.txt;
#     rm listB.txt;
#     awk '{print "root://cms-xrd-global.cern.ch//store/user/cgalloni/Ntuple_BPH_v0/Charmonium/Charmonium_Run2018B-17Sep2018-v1/191014_123757/0000/"$0}' list2B.txt > listB.txt;
#     rm list2B.txt;
#     
    uberftp -ls gsiftp://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat/store/user/cgalloni/Ntuple_BPH_v0/Charmonium/Charmonium_Run2018C-17Sep2018-v1/191014_123757/0000/ > listC.txt;
    awk '{printf("%s\n", $9)}' <listC.txt | tr -d '\r'> list2C.txt;
    sed -i '/log/d' list2C.txt;
    rm listC.txt;
    awk '{print "root://cms-xrd-global.cern.ch//store/user/cgalloni/Ntuple_BPH_v0/Charmonium/Charmonium_Run2018C-17Sep2018-v1/191014_123757/0000/"$0}' list2C.txt > listC.txt;
    rm list2C.txt;
    mv listC.txt list.txt;
    
#    uberftp -ls gsiftp://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat/store/user/cgalloni/Ntuple_BPH_v0/Charmonium/Charmonium_Run2018D-PromptReco-v2/191014_123759/0000/ > listD.txt;
#    awk '{printf("%s\n", $9)}' <listD.txt | tr -d '\r'> list2D.txt;
#    sed -i '/log/d' list2D.txt;
#    rm listD.txt;
#    awk '{print "root://cms-xrd-global.cern.ch//store/user/cgalloni/Ntuple_BPH_v0/Charmonium/Charmonium_Run2018D-PromptReco-v2/191014_123759/0000/"$0}' list2D.txt > listD.txt;
#    rm list2D.txt;
#    
#    cat listA.txt listB.txt listC.txt listD.txt >> list.txt;
elif [ $runtype = 'signalmc' ]; then

    uberftp -ls gsiftp://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat/store/user/cgalloni/Ntuple_BPH_v0/BcJpsiMuNu_020519/BcJpsiMuNu_020519/191014_123225/0000/ > list.txt;
    awk '{printf("%s\n", $9)}' <list.txt | tr -d '\r'> list2.txt;
    sed -i '/log/d' list2.txt;
    rm list.txt;
    awk '{print "root://cms-xrd-global.cern.ch//store/user/cgalloni/Ntuple_BPH_v0/BcJpsiMuNu_020519/BcJpsiMuNu_020519/191014_123225/0000/"$0}' list2.txt > list.txt;
    rm list2.txt;
fi
if [ $iscondor = 'condor' ]; then
    cd condor;
    split -l $splitting -a 3 -d ../list.txt list;
    cd ../../..;
    ./job_condor.sh $runtype;
else
    cd ../..;
fi
