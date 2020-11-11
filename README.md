# NtupleAnalyzer4RJpsi

# Generating Condor scripts for remote processing of NTuples

List the ntuples you want in ``datasets.txt`` using the format beginning with ``/store/user/...`` and ending with ``.../0000``, ``.../0001``, etc - that is to say the file path of the ntuples within their remote storage site.

To Generate condor scripts, you may simply run

``./condor_setup.sh <OUTDIR> <FILES PER JOB> <LIST OF INPUT NTUPLES>``

These will be placed in the ``condor/condorscripts/`` folder. 

To test your ``run.py`` code locally, you may execute one of the condor scripts that is generated, i.e.:

``./condor/condorscripts/Ntuple_BPH_v6/Charmonium/Charmonium_Run2018C-17Sep2018-v1/CondorJob_0.sh``

This will execute on the number of files specified by the ``<FILES PER JOB>`` variable above.

# Skimming NTuples

Make sure that ``run.py`` takes the variables you want from the NTuples - new branches can be added in the variables: ``outvars``, ``gen_outvars``, ``mc_vars``, and ``trig_vars`` for variables from reco level, generator level, monte carlo, and trigger respectively. Analysis you wish to run remotely can also be coded here.

To run locally one can generate condor scripts as above and then execute ``./condor/condorscripts/<SAMPLE SPECIFIC DIRECTORIES>/CondorJob_x.sh``, for integer x. 

# Submitting to Condor

When ready to submit your jobs to Condor, run

``./submit_condor.sh``

You may check the status of these jobs using the ``condor_q`` command, and when the jobs have all finished running, you may run

``./hadder.sh``

to automatically hadd all the root files in each sample into their respective final forms, which are then stored as ``<OUTDIR>/<SAMPLE NAME>/Btrimu.root``

# Flattening NTuples & Applying Scale Factors to MC samples

to Flatten skimmed samples and apply Scale factors, one must use the ``flattener.py`` tool. First, all fragments must be added together through ``hadder.sh`` (described above). Second, the file names and locations must be added to ``samples.py`` as new ``TFile``s. 

Finally, one can run ``python flattener.py --odir=<DESIRED OUTPUT DIRECTORY>`` to flatten the samples and apply final weights to Monte Carlo samples. If one is including generator level information, the tag ``-g`` should also be used.

# Plotting

The branches plotted by ``compare.py`` are stored in ``varsdict.py`` in dictionary form - other plotting information must also be input (several examples are included within ``varsdict.py``)

In ``samples.py``, add the names and locations of the skimmed samples, then for the plotting, you can do,

``python compare.py``

This compare.py will take, as an input, the flat n-tuples produced above.  You may run compare.py with multiple options

-``-c,--compare`` - Generate comparison plots between signal and background for each variable in ``varsdict.py``.
-``-o,--cutopt`` - Generate scans for cut optimization on the branches specified in the ``to_optimize`` dictionary in ``varsdict.py``.
-``-2,--cutopt2`` - Generate scans for cut optimization on the branches specified in the ``to_optimize`` dictionary in ``varsdict.py`` using the second optimization procedure.
-``-n,--compareNorm`` - compared plots will be normalized to 1.
-``-t,--twoDHist`` - generate 2D histograms for pairs listed in the ``corrpairs`` variable in ``varsdict.py``
-``--precut=<CUTS>`` - applies the specified cuts prior to generating plots. Cuts must be formatted as a TString.
-``--checkerr`` - For checking the error bars on your samples.
-``-f,--rmrf`` - Forcefully remove and overwrite old directories and outputs.
-``--outdir=<DIRECTORY>`` - output Directory for plots, ``/eos/home-w/wvetens/www/<DIRECTORY>``, by default change this within line 37 of compare.py. current Default ``<DIRECTORY>``: ``B_pT_comparisons``

By Default, compare.py is configured to also generate HTML and save the plots to your eos storage so they can then be accessible through a webpage. To disable this option, simply comment out the ``writeHTML`` Lines at the bottom of ``compare.py``.

