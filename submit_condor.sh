while read cluster; do
    condor_submit $cluster
done < $PWD/condor/configlist.txt 
