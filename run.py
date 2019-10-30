#!/usr/bin/env python2.7 
# This macro will make a flat Ntuple out of UZH n-tuples. If you like, 
#
# + You can add additional variables 
# + You can skim
#
# 3 Oct. 2019 @ Yuta Takahashi
#


import os, math, sys, re
from ROOT import TFile, TH1F, gROOT, TTree, Double, TChain
import numpy as num

from corrections.PileupWeightTool import *
#__metaclass__ = type # to use super() with subclasses from CommonProducer

gROOT.SetBatch(True)


from optparse import OptionParser, OptionValueError
usage = "usage: python draw.py [tes: 30, m30 (default : None)] [w_scale: 1.1, 0.9 (default : 1)]"
parser = OptionParser(usage)

# if XRD is being nasty about wildcard usage such as '*', use the '-x' flag, and use the 't' flag to point 
# to the text file storing the names and locations of the files you want to use
# To gain such a list, you can run, for example, the script stored in ``getMC.sh`` or ``getdata.sh``
# XRD functionality tested on /store/user/cgalloni/Ntuple_BPH_v0/BJpsiX_MuMu_031019/BJpsiX_MuMu_031019/191014_123225/0000/
parser.add_option("-o", "--out", default='Myroot.root', type="string", help="output filename", dest="out")
parser.add_option("-p", "--path", default='/pnfs/psi.ch/cms/trivcat/store/user/ytakahas/RJpsi_20191002_BcJpsiMuNu_020519/BcJpsiMuNu_020519/BcJpsiMuNu_020519_v1/191002_132739/0000/', type="string", help="path", dest="path")
parser.add_option("-x", default=False, action="store_true", help="use this option if you are pulling a file from xrd. Otherwise file is pulled from psi", dest="xrd")

parser.add_option("-t", default='list.txt', type="string", help="text file containing locations of input files", dest="filelist")
parser.add_option("-l","--filelist",  default='', type="string", help="text file containing locations of input files", dest="filelist")



(options, args) = parser.parse_args()

outfilename="./"+options.out

print 'output file name = ', options.out

outputfile = TFile(outfilename, "recreate")

# # file2include = 'dcap://t3se01.psi.ch:22125/' + options.path + '/flatTuple*.root'
# file2include = 'root://cms-xrd-global.cern.ch/'+ options.path + '/flatTuple_11.root'
# 
# print 'file2include = ', file2include 
# 
# chain = TChain('ntuplizer/tree')
# 
# chain.Add(file2include)

chain = TChain('ntuplizer/tree')

print "doing xrd?", options.xrd

if options.xrd == False:
    #file2include = 'dcap://t3se01.psi.ch:22125/' + options.path + '/flatTuple*.root'
    file2include = 'root://cms-xrd-global.cern.ch/'+ options.path + '/flatTuple_11.root'
    print 'file2include = ', file2include 
    chain.Add(file2include)
if options.xrd == True:

    
    file2include = 'root://cms-xrd-global.cern.ch/'+ options.path
    print 'file2include = ', file2include 
    chain.Add(file2include)

    if  options.filelist is not '':
        files = open(options.filelist, "r")
        for tfile in files:
            tfile = tfile.strip()
            print 'file2include = ', tfile
            chain.Add(tfile)
# This is to make processing faster. 
# If you need more information, you need to activate it ... 
# Remember that, only the activated branches will be saved

#outvars = ['EVENT_run', 'EVENT_lumiBlock']
outvars = ['Jpsi_trimu_fl3d', 'Jpsi_trimu_lip', 'Jpsi_trimu_mass', 'Jpsi_trimu_maxdoca', 'Jpsi_maxdoca', 'Jpsi_pt', 'Jpsi_mu1_isSoft', 'Jpsi_mu2_isSoft', 'Jpsi_mu3_isGlobal', 'Jpsi_mu3_pt']# 'nPuVtxTrue', 'PV_N', 'bX']
evt_outvars =['nPuVtxTrue', 'PV_N', 'bX']
chain.SetBranchStatus('*', 0)
for var in outvars:
    chain.SetBranchStatus(var, 1)
for var in evt_outvars:
    chain.SetBranchStatus(var, 1)

# copy original tree
otree = chain.CloneTree(0)


if options.geteff:
    cuthist = TH1F("cuthist", "cuthist", 2, 0, 2)
otree.SetDirectory(outputfile)

# if you want to add additional variables (on top of the one already existing)
# you can do followings 
#
#    tau_pt = num.zeros(1, dtype=float)
#    otree.Branch('tau_pt', tau_pt, 'tau_pt/D')
#

weight_pu = num.zeros(1,dtype=float)
otree.Branch('weight_pu', weight_pu, 'weight_pu/D') 



Nevt = chain.GetEntries()

print 'Total Number of events = ', Nevt 
evtid = 0

isData = False 

if not  isData:
    puTool         = PileupWeightTool(year=2018)


for evt in xrange(Nevt):
    chain.GetEntry(evt)
    if options.geteff:
        cuthist.Fill(0)

    if evt%100000==0: print '{0:.2f}'.format(Double(evt)/Double(Nevt)*100.), '% processed'
  #  if evt>100: break


    # if you want to put some cuts, you can do followings
    # 
    #   if len(chain.pft_b_mass)==0: continue
    #

    # you can now add additional variables here: 
    #
    #   tau_pt[0] = chain.pft_tau_pt[0]
    #

    weight_pu[0]=1

    for v  in xrange(chain.nPuVtxTrue.size()):
        
        if  chain.bX[v] == 0 :
            
            weight_pu[0] = puTool.getWeight(chain.nPuVtxTrue[v])
            #print " chain.nPuVtxTrue[v] %s, PV_N  %s, PUweight %s" %(chain.nPuVtxTrue[v],  chain.PV_N, weight_pu[0] )
 
           




    mu3pt = 2
    selectedjpsi = -1
    for iJpsi in xrange(chain.Jpsi_mu3_pt.size()):
        if chain.Jpsi_pt[iJpsi] <= 8: continue
        if not chain.Jpsi_mu1_isSoft[iJpsi]: continue
        if not chain.Jpsi_mu2_isSoft[iJpsi]: continue
        if not chain.Jpsi_mu3_isGlobal[iJpsi]: continue
        if chain.Jpsi_trimu_mass[iJpsi] > 9: continue
        if chain.Jpsi_mu3_pt[iJpsi] < mu3pt: continue
        mu3pt = chain.Jpsi_mu3_pt[iJpsi]
        selectedjpsi = iJpsi

    if selectedjpsi == -1: continue
    evtid += 1
    if options.geteff:
        cuthist.Fill(1)
    #otree.Fill()

    if not options.geteff:
        for var in outvars:
            tmp = getattr(chain,var)[selectedjpsi]
            getattr(chain,var).clear()
            getattr(chain,var).push_back(tmp)
        #for var in evt_outvars:
        #    tmp = getattr(chain,var)[selectedjpsi]
        #    getattr(chain,var).clear()
        #    getattr(chain,var).push_back(tmp)
        otree.Fill()
if options.geteff:
    cuthist.Write()
outputfile.cd()

otree.Write()
outputfile.Write()
outputfile.Close()

print Nevt, 'evt processed.', evtid, 'evts passed'
print "Efficiency: ", float(evtid)/Nevt