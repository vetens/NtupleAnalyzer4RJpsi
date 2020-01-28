#!/usr/bin/env python2.7 
# This macro will make a flat Ntuple out of UZH n-tuples. If you like, 
#
# + You can add additional variables 
# + You can skim
#
# 3 Oct. 2019 @ Yuta Takahashi
#


import os, math, sys, re
from ROOT import TFile, TH1F, gROOT, TTree, Double, TChain, TMath, TLorentzVector
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
parser.add_option("-l","--filelist",  default='', type="string", help="text file containing locations of input files", dest="filelist")
parser.add_option("-d", default=False, action="store_true", help="Flag with -d if you are running over Data", dest="isdat")



(options, args) = parser.parse_args()

#outfilename="./"+options.out
outfilename=options.out

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

isData = options.isdat 

#if not isData:
nevts = 0

if options.xrd == False:
    file2include = 'dcap://t3se01.psi.ch:22125/' + options.path + '/flatTuple*.root'
    #file2include = 'root://cms-xrd-global.cern.ch/'+ options.path + '/flatTuple_11.root'
    print 'file2include = ', file2include 
#    if not isData:
    infile = TFile.Open(file2include)
    nevts += infile.Get('ntuplizer/cutflow_perevt').GetBinContent(1)
    chain.Add(file2include)
if options.xrd == True:
    if options.filelist is '':
        file2include = 'root://cms-xrd-global.cern.ch/'+ options.path
        print 'file2include = ', file2include 
        infile = TFile.Open(file2include)
        nevts += infile.Get('ntuplizer/cutflow_perevt').GetBinContent(1)
        chain.Add(file2include)

    if  options.filelist is not '':
        files = open(options.filelist, "r")
        for tfile in files:
            tfile = tfile.strip()
            print 'file2include = ', tfile
#            if not isData:
            infile = TFile.Open(tfile)
            nevts += infile.Get('ntuplizer/cutflow_perevt').GetBinContent(1)
            chain.Add(tfile)
# This is to make processing faster. 
# If you need more information, you need to activate it ... 
# Remember that, only the activated branches will be saved

#outvars = ['EVENT_run', 'EVENT_lumiBlock']
outvars = ['JpsiMu_Jpsi_lip', 'JpsiMu_Jpsi_lips', 'JpsiMu_Jpsi_pvip', 'JpsiMu_Jpsi_pvips', 'JpsiMu_B_pvip', 'JpsiMu_B_pvips', 'JpsiMu_B_lips', 'JpsiMu_B_fls3d', 'JpsiMu_Jpsi_unfit_mass', 'JpsiMu_B_iso', 'JpsiMu_B_iso_ntracks', 'JpsiMu_B_iso_mindoca', 'JpsiMu_B_fl3d', 'JpsiMu_B_lip', 'JpsiMu_B_mass', 'JpsiMu_B_pt', 'JpsiMu_B_eta', 'JpsiMu_B_phi', 'JpsiMu_B_maxdoca', 'JpsiMu_B_mindoca', 'JpsiMu_Jpsi_maxdoca', 'JpsiMu_Jpsi_mindoca', 'JpsiMu_Jpsi_alpha', 'JpsiMu_Jpsi_fl3d', 'JpsiMu_Jpsi_fls3d', 'JpsiMu_Jpsi_pt', 'JpsiMu_Jpsi_eta', 'JpsiMu_Jpsi_phi', 'JpsiMu_mu1_iso', 'JpsiMu_mu1_dbiso', 'JpsiMu_mu2_iso', 'JpsiMu_mu2_dbiso', 'JpsiMu_mu3_iso', 'JpsiMu_mu3_dbiso', 'JpsiMu_mu1_isSoft', 'JpsiMu_mu2_isSoft', 'JpsiMu_mu3_isGlobal', 'JpsiMu_mu3_pt', 'JpsiMu_mu3_eta', 'JpsiMu_mu3_phi', 'JpsiMu_B_alpha', 'JpsiMu_Jpsi_vprob', 'JpsiMu_B_vprob', 'JpsiMu_mu1_pt', 'JpsiMu_mu1_eta', 'JpsiMu_mu1_phi', 'JpsiMu_mu2_pt', 'JpsiMu_mu2_eta', 'JpsiMu_mu2_phi']# 'nPuVtxTrue', 'PV_N', 'bX']
met_outvars = ['MET_et', 'MET_phi', 'MET_sumEt']
evt_outvars = ['PV_N']
mc_vars = ['nPuVtxTrue', 'bX']
if not isData:
    evt_outvars = evt_outvars + mc_vars
chain.SetBranchStatus('*', 0)
for var in outvars:
    chain.SetBranchStatus(var, 1)
for var in met_outvars:
    chain.SetBranchStatus(var, 1)
for var in evt_outvars:
    chain.SetBranchStatus(var, 1)

# copy original tree
otree = chain.CloneTree(0)


# if you want to add additional variables (on top of the ones already existing)
# you can do followings 
#
#    tau_pt = num.zeros(1, dtype=float)
#    otree.Branch('tau_pt', tau_pt, 'tau_pt/D')
#

otree.SetDirectory(outputfile)


cuthist = TH1F("cuthist", "cuthist", 3, 0, 3)
if not isData:
    weight_pu = num.zeros(1,dtype=float)
    otree.Branch('weight_pu', weight_pu, 'weight_pu/D') 
    
    weight_evt = num.zeros(1,dtype=float)
    otree.Branch('weight_evt', weight_evt, 'weight_evt/D') 

mcorr = num.zeros(1,dtype=float)
otree.Branch('mcorr', mcorr , 'mcorr/D') 
dphi_JpsiMu_mu3 = num.zeros(1,dtype=float)
otree.Branch('dphi_JpsiMu_mu3', dphi_JpsiMu_mu3, 'dphi_JpsiMu_mu3/D') 
cosdphi_JpsiMu_mu3 = num.zeros(1,dtype=float)
otree.Branch('cosdphi_JpsiMu_mu3', cosdphi_JpsiMu_mu3, 'cosdphi_JpsiMu_mu3/D') 
dphi_JpsiMu_MET = num.zeros(1,dtype=float)
otree.Branch('dphi_JpsiMu_MET', dphi_JpsiMu_MET, 'dphi_JpsiMu_MET/D')
cosdphi_JpsiMu_MET = num.zeros(1,dtype=float)
otree.Branch('cosdphi_JpsiMu_MET', cosdphi_JpsiMu_mu3, 'cosdphi_JpsiMu_MET/D') 
dphi_mu3_MET = num.zeros(1,dtype=float)
otree.Branch('dphi_mu3_MET', dphi_mu3_MET, 'dphi_mu3_MET/D')
cosdphi_mu3_MET = num.zeros(1,dtype=float)
otree.Branch('cosdphi_mu3_MET', cosdphi_JpsiMu_mu3, 'cosdphi_mu3_MET/D') 
dR_JpsiMu_mu3 = num.zeros(1,dtype=float)
otree.Branch('dR_JpsiMu_mu3', dR_JpsiMu_mu3, 'dR_JpsiMu_mu3/D') 

Nentries = chain.GetEntries()

print 'Total Number of entries to proces  = ', Nentries 
evtid = 0


if not isData:
    puTool         = PileupWeightTool(year=2018)

MJpsi=3.096916
MMu=0.1056583745
#if not isData:
cuthist.Fill(0, nevts)
for evt in xrange(Nentries):
    chain.GetEntry(evt)

    if evt%100000==0: print '{0:.2f}'.format(Double(evt)/Double(Nentries)*100.), '% processed'
  #  if evt>100: break


    # if you want to put some cuts, you can do followings
    # 
    #   if len(chain.pft_b_mass)==0: continue
    #

    # you can now add additional variables here: 
    #
    #   tau_pt[0] = chain.pft_tau_pt[0]
    #
    if not isData:
        weight_pu[0]=1
        weight_evt[0]=1

        for v  in xrange(chain.nPuVtxTrue.size()):
            
            if  chain.bX[v] == 0 :
                
                weight_pu[0] = puTool.getWeight(chain.nPuVtxTrue[v])
                #print " chain.nPuVtxTrue[v] %s, PV_N  %s, PUweight %s" %(chain.nPuVtxTrue[v],  chain.PV_N, weight_pu[0] )

         #weight_evt will just be the product of all the other weights
        weight_evt[0] = weight_pu[0]
 
           



    mu3ptcut = 4
    selectedjpsi = -1
    for iJpsi in xrange(chain.JpsiMu_mu3_pt.size()):
        if chain.JpsiMu_mu3_pt.size() < 1: continue
        if chain.JpsiMu_Jpsi_pt[iJpsi] < 8: continue
        if chain.JpsiMu_mu1_pt[iJpsi] < 4: continue
        if chain.JpsiMu_mu2_pt[iJpsi] < 4: continue
        if not chain.JpsiMu_mu1_isSoft[iJpsi]: continue
        if not chain.JpsiMu_mu2_isSoft[iJpsi]: continue
        if not chain.JpsiMu_mu3_isGlobal[iJpsi]: continue
        if chain.JpsiMu_mu3_pt[iJpsi] < mu3ptcut: continue
        mu3ptcut = chain.JpsiMu_mu3_pt[iJpsi]
        selectedjpsi = iJpsi

    if selectedjpsi == -1: continue
    evtid += 1
    #otree.Fill()
    pJpsiMu = TLorentzVector.TLorentzVector()
    pB = TLorentzVector.TLorentzVector()
    pmu3 = TLorentzVector.TLorentzVector()
    pmet = TLorentzVector.TLorentzVector()
    pJpsiMu.SetPtEtaPhiM(chain.JpsiMu_Jpsi_pt[selectedjpsi], chain.JpsiMu_Jpsi_eta[selectedjpsi], chain.JpsiMu_Jpsi_phi[selectedjpsi], MJpsi)
    pmu3.SetPtEtaPhiM(chain.JpsiMu_mu3_pt[selectedjpsi], chain.JpsiMu_mu3_eta[selectedjpsi], chain.JpsiMu_mu3_phi[selectedjpsi], MMu)
    pB.SetPtEtaPhiM(chain.JpsiMu_B_pt[selectedjpsi], chain.JpsiMu_B_eta[selectedjpsi], chain.JpsiMu_B_phi[selectedjpsi], chain.JpsiMu_B_mass[selectedjpsi])
    pmet.SetPtEtaPhiE(chain.MET_et[0], 2, chain.MET_phi[0], -chain.MET_et[0])

    pperp = pB.P() * TMath.Sin(chain.JpsiMu_B_alpha[selectedjpsi])
    mcorr[0] = TMath.Sqrt( (chain.JpsiMu_B_mass[selectedjpsi])**2 + pperp**2 ) + pperp

    dphi_JpsiMu_mu3[0] = pJpsiMu.DeltaPhi(pmu3)
    dphi_JpsiMu_MET[0] = pJpsiMu.DeltaPhi(pmet)
    dphi_mu3_MET[0] = pmu3.DeltaPhi(pmet)
    dR_JpsiMu_mu3[0] = pJpsiMu.DeltaR(pmu3)
    cosdphi_JpsiMu_mu3[0] = TMath.Cos(dphi_JpsiMu_mu3[0])
    cosdphi_JpsiMu_MET[0] = TMath.Cos(dphi_JpsiMu_MET[0])
    cosdphi_mu3_MET[0] = TMath.Cos(dphi_mu3_MET[0])

    for var in outvars:
        tmp = getattr(chain,var)[selectedjpsi]
        getattr(chain,var).clear()
        getattr(chain,var).push_back(tmp)
    for var in met_outvars:
        tmp = getattr(chain,var)[0]
        getattr(chain,var).clear()
        getattr(chain,var).push_back(tmp)
    cuthist.Fill(1)
    if not isData:
        cuthist.Fill(2, weight_evt)
        #for var in evt_outvars:
        #    tmp = getattr(chain,var)[selectedjpsi]
        #    getattr(chain,var).clear()
        #    getattr(chain,var).push_back(tmp)
    otree.Fill()

outputfile.cd()
#if not isData:
cuthist.Write()
otree.Write()
outputfile.Write()
outputfile.Close()

print Nentries, 'entries processed.', evtid, 'evts passed'
if not isData:
    print "Efficiency: ", float(evtid)/nevts
