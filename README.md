# NtupleAnalyzer4RJpsi

To produce flat-tree, you can do, 

> python run.py --path XXX --out YYY

where XXX is the pathname to the directory where you store your ROOT files (can be multiple files -> will be chained automatically) and YYY is the output file name. 

For submitting the jobs using psi batch, you can do, 

> python submit_Yuta.py

But before that, you need to inspect submit_Yuta.sh and need to change "ytakahas" to your user name.



For the plotting, you can do,

> python compare.py

This compare.py will take, as an input, the flat n-tuple produced above. 
