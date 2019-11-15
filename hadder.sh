while read cluster; do
    source ${cluster}CondorJob_hadd.sh
done < $PWD/condor/clusters.txt 
