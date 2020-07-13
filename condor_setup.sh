#!/bin/bash
target=${1:-/eos/home-w/wvetens/SkimmedNTuples_V1/}
splitting=${2:-20}
inlist=${3:-'datasets.txt'}
prefix1="/store/user"
workdir=$PWD
FirstRun=0;
rm -f $workdir/condor/clusters.txt
rm -rf $workdir/condor/outCondor/*
rm -rf $workdir/condor/condorscripts
rm -rf $workdir/condor/lists
touch $workdir/condor/clusters.txt
cp -f $(voms-proxy-info --path) userproxy
# function to write condor submitted scripts, called later within while loop
writeScript() {
    listNumber=$(echo $1 | awk '{ printf("%03d",$1) }')
    jobNumber=$1
    scriptname=CondorJob_${1}.sh
    if [ -e $workdir/condor/condorscripts/$2$scriptname ]; then
        jobNumber=$(($jobNumber+1)) \
        scriptname=CondorJob_${jobNumber}.sh
    fi
    # Flag for either Data or Monte Carlo
    if [[ $2 == *"Charmonium"* ]]; then
        sed -e 's&LISTDIR&'"$3"'&g' \
            -e 's&ISDAT&-d&g' \
            -e 's&ISGEN&&g' \
            -e 's&ISSIG&&g' \
            -e 's&TARGET&'"$target"'&g' \
            -e 's&WORKDIR&'"$workdir"'&g' \
            -e 's/LISTNUMBER/'"$listNumber"'/g' \
            -e 's/JOBNUMBER/'"$jobNumber"'/g' \
            -e 's&RUNTYPE&'"$2"'&g' < $workdir/condor/condor_template.sh > $scriptname 
    elif [[ $2 == *"BcJpsiMu"* ]]; then
        sed -e 's&LISTDIR&'"$3"'&g' \
            -e 's&ISGEN&-g&g' \
            -e 's&ISSIG&-s&g' \
            -e 's&TARGET&'"$target"'&g' \
            -e 's&WORKDIR&'"$workdir"'&g' \
            -e 's/LISTNUMBER/'"$listNumber"'/g' \
            -e 's/JOBNUMBER/'"$jobNumber"'/g' \
            -e 's&RUNTYPE&'"$2"'&g' < $workdir/condor/condor_template.sh > $scriptname
    else
        sed -e 's&LISTDIR&'"$3"'&g' \
            -e 's&ISDAT&&g' \
            -e 's&ISGEN&-g&g' \
            -e 's&ISSIG&&g' \
            -e 's&TARGET&'"$target"'&g' \
            -e 's&WORKDIR&'"$workdir"'&g' \
            -e 's/LISTNUMBER/'"$listNumber"'/g' \
            -e 's/JOBNUMBER/'"$jobNumber"'/g' \
            -e 's&RUNTYPE&'"$2"'&g' < $workdir/condor/condor_template.sh > $scriptname 
    fi
    chmod u+xrw $scriptname
}
while read dir; do
    # remove '/store/user/USERNAME/' from the front and '/######_######/####/' from the back 
    # basically, abbreviate the directory to have a more convenient storage of the runs
    dir1=$( echo "$dir" | sed -e "s@^$prefix1@@" )
    prefix2=$( echo "$dir1" | awk -F"/" '{print "/"$2}' )
    dir2=$( echo "$dir1" | sed -e "s@^$prefix2@@" )
    run=$(dirname $(dirname $dir2))/
    # Get list of files for each dataset and split for desired condor splitting
    if [ ! -d $workdir/condor/lists${run}condorsplit ]; then
        mkdir -p $workdir/condor/lists${run}condorsplit;
    fi
    cd $workdir/condor/lists$run
    uberftp -ls gsiftp://storage01.lcg.cscs.ch/pnfs/lcg.cscs.ch/cms/trivcat/$dir > list.txt;
    awk '{printf("%s\n", $9)}' <list.txt | tr -d '\r'> list2.txt;
    sed -i '/log/d' list2.txt;
    rm list.txt;
    sed -e "s&^&root://cms-xrd-global.cern.ch/$dir&" list2.txt > list.txt;
    rm list2.txt;
    cd condorsplit;
    split -l $splitting -a 3 -d ../list.txt list;
    # produce scripts to be run on condor
    listdir=$workdir/condor/lists${run}condorsplit
    numfiles=(*)
    numfiles=${#numfiles[@]}
    LastRun=$numfiles
    numofjobs=$(($LastRun))
    cd $workdir
    if [ ! -d condor/condorscripts$run ]; then
        mkdir -p condor/condorscripts$run;
    fi
    rm -rf $target$run
    mkdir -p $target$run;
    rm -rf $workdir$run
    mkdir -p $workdir$run;
    if [ ! -d condor/outCondor$run ]; then
        mkdir -p condor/outCondor$run;
    fi
    cd condor/condorscripts$run
    for (( i=$FirstRun; i<$LastRun; i++ ));
    do
        writeScript $i $run $listdir
    done
    # Write the script to run after other condor jobs which hadds the results together 
    sed -e 's&RUNTYPE&'"$run"'&g' \
        -e 's&WORKDIR&'"$workdir"'&g' \
        -e 's&TARGET&'"$target"'&g' < $workdir/condor/hadd_template.sh > CondorJob_hadd.sh
    chmod u+xrw CondorJob_hadd.sh
    # write list of condor clusters to be submitted
    sed -e 's&RUNTYPE&'"$run"'&g' \
        -e 's&WORKDIR&'"$workdir"'&g' \
        -e 's&NUMOFJOBS&'"$numofjobs"'&g' < $workdir/condor/condor_config_template.cfg \
        > $workdir/condor/condorscripts${run}condor_multiple.cfg
    echo "$workdir/condor/condorscripts${run}" >> $workdir/condor/clusters.txt
    cd $workdir
done < $inlist
# ./job_condor.sh $runtype;
