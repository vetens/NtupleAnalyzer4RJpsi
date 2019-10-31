# NtupleAnalyzer4RJpsi

To produce flat-tree, you can do, 

``python run.py --path XXX --out YYY``

where XXX is the pathname to the directory where you store your ROOT files (can be multiple files -> will be chained automatically) and YYY is the output file name. 

For submitting the jobs using psi batch, you can do, 

``python submit_Yuta.py``

But before that, you need to inspect submit_Yuta.py (you need to change input data path) as well as submit_Yuta.sh (you need to change "ytakahas" to your user name).


For the plotting, you can do,

``python compare.py``

This compare.py will take, as an input, the flat n-tuple produced above. 

Running on LXPLUS instead of psi
--------------------------------

First you must save your list of files to a .txt file, for example by using the following code(The first line dumps the contents of the folder into a file, the second formats whitespace properly, the third and fourth remove any 'log' files from the list, and the fifth and sixth set up the files to be automatically accessed through xrootd:

```
uberftp -ls gsiftp://<STORAGE SERVER>/<PATH TO FOLDER CONTAINING FILES> > list.txt
awk '{printf("%s\n", $9)}' <list.txt | tr -d '\r'> list2.txt
sed -i '/log/d' list2.txt
rm list2.txt
sed -e "s&^&\"root://cms-xrd-global.cern.ch/$dir\"&" list2.txt > list.txt
rm list2.txt
```

then run the following command:

`` python run.py -x -l list.txt -o OUTPUTDIRECTORY/OUTPUTNAME``


Running on Condor
-----------------

Save your Grid Certificate to a file, ``userproxy``, which is accessible to condor for use with your jobs:

``cp $(voms-proxy-info --path) userproxy``

then execute (with positionally dependent optional commands)

``./condor_setup.sh <OUTPUTDIRECTORY = /eos/user/w/wvetens> <NUM_OF_FILES_PER_JOB = 20> <LIST_OF_INPUT_DATASETS = datasets.txt>`` 

which auto generates the condor submission scripts and config files from templates. To submit to condor then execute

``./submit_condor.sh``
