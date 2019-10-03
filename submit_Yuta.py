#! /usr/bin/env python
#
# Creating dir:
#   uberftp t3se01.psi.ch 'mkdir /pnfs/psi.ch/cms/trivcat/store/user/ineuteli/samples/LowMassDiTau_madgraph'
#
# Multicore jobs:
#   to submit multicore job:    qsub -pe smp 8 ...
#   in mg_configuration.txt:    run_mode=2 # multicore
#                               nb_core=8
#   note it might wait longer in queue
# 
# Luca v.s Izaak
#   https://www.diffchecker.com/JSVEi5qL

import os, sys, subprocess, time, glob
from optparse import OptionParser

cdir = os.getcwd()

argv = sys.argv
usage = "This script will produce miniAOD files, starting from GS sample (assuming it is at T3)"

parser = OptionParser(usage=usage,epilog="Success!")


(opts, args) = parser.parse_args(argv)
# if len(argv) == 1:
#     parser.print_help()
#     sys.exit()

WORKPATH        = cdir

n_cores         = 1


samples = [

    ('BcJpsiMuNu', '/pnfs/psi.ch/cms/trivcat/store/user/ytakahas/RJpsi_20191002_BcJpsiMuNu_020519/BcJpsiMuNu_020519/BcJpsiMuNu_020519_v1/*/*'),
#    ('BG', '/pnfs/psi.ch/cms/trivcat/store/user/ytakahas/jobtmp_BJpsiX_MuMu_cgalloni_Fall18_10_2_9-MINIAODSIM_PFak8_v2-837a3da8dcfae4d00b168448aacda8b8/*')
    
    ]



for sample, path2file in samples:

    print sample, path2file

    dirs = glob.glob(path2file)

    flag = True

    REPORTDIR = "%s/job_%s"%(WORKPATH, sample)
    if not os.path.exists(REPORTDIR):
        os.makedirs(REPORTDIR)
        print ">>> made directory " + REPORTDIR



    njobs = 0

    for dir in dirs:

#    if njobs > 10: break
        
        nfile = 0
        
        for file in os.listdir(dir):
        
#        print file
            
            if file.find('.root')!=-1:
                nfile += 1

        if nfile == 0: continue


        print dir, 'is submitted with ', nfile, 'files ...'

        jobname = "%s_%s"%('Jpsi', njobs)

        outputname = cdir + '/out_' + sample + '/Myroot_' + str(njobs) + '.root'

        OUTDIR = cdir + '/out_' + sample
        if not os.path.exists(OUTDIR):
            os.makedirs(OUTDIR)



        command = "qsub -q all.q -l h_vmem=6g -pe smp %d -N %s submit_Yuta.sh %s %s" % (n_cores, jobname, dir, outputname)
#      command = "qsub -q all.q -pe smp %d -N %s submit_Yuta.sh %s %s" % (n_cores, sample, sample, prefix + _file_)
#    print "\n>>> " + command #.replace(jobname,"\033[;1m%s\033[0;0m"%jobname,1)
    
        sys.stdout.write(">>> ")
        sys.stdout.flush()
        os.system(command)
    
        njobs += 1
        
    print '>>>\n>>> ' + str(njobs)  + ' done\n'

