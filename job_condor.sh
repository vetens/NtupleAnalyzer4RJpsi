#!/bin/bash 
# run this with the option either `data` or `MC`
dir0=$PWD
listdir=$dir0/lists/$1/condor
runtype=$1
cd $listdir
shopt -s nullglob
numfiles=(*)
numfiles=${#numfiles[@]}
FirstRun=0;
LastRun=$numfiles;  ## Total jobs for the dataset
# LastRun=$numfiles;  ## Total jobs for the dataset
cd $dir0
if [ ! -d condorscripts ]; then
    mkdir -p condorscripts;
fi
cd condorscripts
if [ ! -d $runtype ]; then
    mkdir -p $runtype;
fi
cd $runtype
writeScript() {
    listNumber=$(echo $1 | awk '{ printf("%03d",$1) }')
    jobNumber=$1
    scriptname=BJpsiX_${1}.sh
#    touch $scriptname
    sed -e 's&LISTDIR&'"$listdir"'&' \
        -e 's/LISTNUMBER/'"$listNumber"'/' \
        -e 's/JOBNUMBER/'"$jobNumber"'/' \
        -e 's/RUNTYPE/'"$runtype"'/' < $dir0/condor_starter.sh > $scriptname 
    chmod u+xrw $scriptname
}
for (( i=$FirstRun; i<$LastRun; i++ ));
do
    writeScript $i
done
sed 's/RUNTYPE/'"$runtype"'/' < $dir0/hadd_script.sh > BJpsiX_${LastRun}.sh
chmod u+xrw BJpsiX_${LastRun}.sh
echo "THERE ARE"$LastRun+1"FILES TO RUN OVER FOR THIS SUBMISSION:"$runtype
cd $dir0
