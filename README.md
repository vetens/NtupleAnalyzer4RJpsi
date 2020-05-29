# NtupleAnalyzer4RJpsi

# Generating Condor scripts

To Generate condor scripts, you may simply run

``./condor_setup.sh <OUTDIR> <FILES PER JOB> <LIST OF INPUT NTUPLES>``

These will be placed in the ``condor/condorscripts/`` folder. 

To test your ``run.py`` code locally, you may execute one of the condor scripts that is generated, i.e.:

``./condor/condorscripts/Ntuple_BPH_v6/Charmonium/Charmonium_Run2018C-17Sep2018-v1/CondorJob_0.sh``

# Submitting to Condor

When ready to submit your jobs to Condor, run

``./submit_condor.sh``

You may check the status of these jobs using the ``condor_q`` command, and when the jobs have all finished running, you may run

``./hadder.sh``

to automatically hadd all the root files in each sample into their respective final forms, which are then stored as ``<OUTDIR>/<SAMPLE NAME>/Btrimu.root``

# Plotting

In ``samples.py``, add the names and locations of the skimmed NTuple samples, then for the plotting, you can do,

``python compare.py``

This compare.py will take, as an input, the flat n-tuples produced above.  You may run compare.py with multiple options, accessible by 

``python compare.py -h``

By Default, compare.py is configured to also generate HTML and save the plots to your eos storage so they can then be accessible through a webpage. To disable this option, simply comment out the ``writeHTML`` Lines at the bottom of ``compare.py``.

