# 
# This macro will make a flat Ntuple out of UZH n-tuples. If you like, 
#
# + You can add additional variables 
# + You can skim
#
# 3 Oct. 2019 @ Yuta Takahashi
#


import os, math, sys
from ROOT import TFile, TH1F, gROOT, TTree, Double, TChain
import numpy as num

gROOT.SetBatch(True)


from optparse import OptionParser, OptionValueError
usage = "usage: python draw.py [tes: 30, m30 (default : None)] [w_scale: 1.1, 0.9 (default : 1)]"
parser = OptionParser(usage)

parser.add_option("-o", "--out", default='Myroot.root', type="string", help="output filename", dest="out")
parser.add_option("-p", "--path", default='/pnfs/psi.ch/cms/trivcat/store/user/ytakahas/RJpsi_20191002_BcJpsiMuNu_020519/BcJpsiMuNu_020519/BcJpsiMuNu_020519_v1/191002_132739/0000/', type="string", help="path", dest="path")


(options, args) = parser.parse_args()

print 'output file name = ', options.out

outputfile = TFile(options.out, 'recreate')

file2include = 'dcap://t3se01.psi.ch:22125/' + options.path + '/flatTuple*.root'

print 'file2include = ', file2include 

chain = TChain('ntuplizer/tree')

chain.Add(file2include)

# This is to make processing faster. 
# If you need more information, you need to activate it ... 
# Remember that, only the activated branches will be saved

chain.SetBranchStatus('*', 0)
chain.SetBranchStatus('Jpsi_*', 1)

# copy original tree
otree = chain.CloneTree(0)



# if you want to add additional variables (on top of the one already existing)
# you can do followings 
#
#    tau_pt = num.zeros(1, dtype=float)
#    otree.Branch('tau_pt', tau_pt, 'tau_pt/D')
#

Nevt = chain.GetEntries()

print 'Total Number of events = ', Nevt 
evtid = 0


for evt in xrange(Nevt):
    chain.GetEntry(evt)

    if evt%100000==0: print '{0:.2f}'.format(Double(evt)/Double(Nevt)*100.), '% processed'


    # if you want to put some cuts, you can do followings
    # 
    #   if len(chain.pft_b_mass)==0: continue
    #

    # you can now add additional variables here: 
    #
    #   tau_pt[0] = chain.pft_tau_pt[0]
    #

    evtid += 1
    otree.Fill()

otree.Write()
outputfile.Close()


print Nevt, 'evt processed.', evtid, 'evt has matching'
