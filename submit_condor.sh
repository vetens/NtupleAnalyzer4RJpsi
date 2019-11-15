rm -f $PWD/condor/clusterids.txt
while read cluster; do
    condor_submit ${cluster}condor_multiple.cfg >> clusterids.txt
done < $PWD/condor/clusters.txt 
