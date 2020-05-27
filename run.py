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
parser.add_option("--local", default=False, action="store_true", help="use this option if you are pulling a file locally. Otherwise file is pulled from psi", dest="local")
parser.add_option("-l","--filelist",  default='', type="string", help="text file containing locations of input files", dest="filelist")
parser.add_option("-g", default=False, action="store_true", help="Flag with -g if you are using gen level data", dest="isgen")
parser.add_option("-d", default=False, action="store_true", help="Flag with -d if you are running over Data", dest="isdat")
parser.add_option("-s", default=False, action="store_true", help="Flag with -s if you are running over Signal (at gen level)", dest="issig")



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
isGenLevel = options.isgen 
isSignal = options.issig 

#if not isData:
nevts = 0

if options.xrd == False:
    if options.local == True:
        file2include = options.path 
    else:
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
outvars = ['JpsiMu_Jpsi_lip', 'JpsiMu_Jpsi_lips', 'JpsiMu_Jpsi_pvip', 'JpsiMu_Jpsi_pvips', 'JpsiMu_B_pvip', 'JpsiMu_B_pvips', 'JpsiMu_B_lips', 'JpsiMu_B_fls3d', 'JpsiMu_Jpsi_unfit_mass', 'JpsiMu_B_iso', 'JpsiMu_B_iso_ntracks', 'JpsiMu_B_iso_mindoca', 'JpsiMu_B_fl3d', 'JpsiMu_B_lip', 'JpsiMu_B_mass', 'JpsiMu_B_pt', 'JpsiMu_B_eta', 'JpsiMu_B_phi', 'JpsiMu_B_maxdoca', 'JpsiMu_B_mindoca', 'JpsiMu_Jpsi_maxdoca', 'JpsiMu_Jpsi_mindoca', 'JpsiMu_Jpsi_alpha', 'JpsiMu_Jpsi_fl3d', 'JpsiMu_Jpsi_fls3d', 'JpsiMu_Jpsi_pt', 'JpsiMu_Jpsi_eta', 'JpsiMu_Jpsi_phi', 'JpsiMu_mu1_iso', 'JpsiMu_mu1_dbiso', 'JpsiMu_mu2_iso', 'JpsiMu_mu2_dbiso', 'JpsiMu_mu3_iso', 'JpsiMu_mu3_dbiso', 'JpsiMu_mu1_isSoft', 'JpsiMu_mu1_isTracker', 'JpsiMu_mu1_isGlobal', 'JpsiMu_mu1_isPF', 'JpsiMu_mu1_isTight', 'JpsiMu_mu1_isLoose', 'JpsiMu_mu2_isSoft', 'JpsiMu_mu2_isTracker', 'JpsiMu_mu2_isGlobal', 'JpsiMu_mu2_isPF', 'JpsiMu_mu2_isTight', 'JpsiMu_mu2_isLoose', 'JpsiMu_mu3_isSoft', 'JpsiMu_mu3_isTracker', 'JpsiMu_mu3_isGlobal', 'JpsiMu_mu3_isPF', 'JpsiMu_mu3_isTight', 'JpsiMu_mu3_isLoose', 'JpsiMu_mu3_pt', 'JpsiMu_mu3_eta', 'JpsiMu_mu3_phi', 'JpsiMu_mu3_doca2mu1', 'JpsiMu_mu3_doca2mu2', 'JpsiMu_B_alpha', 'JpsiMu_Jpsi_vprob', 'JpsiMu_B_vprob', 'JpsiMu_mu1_pt', 'JpsiMu_mu1_eta', 'JpsiMu_mu1_phi', 'JpsiMu_mu2_pt', 'JpsiMu_mu2_eta', 'JpsiMu_mu2_phi', 'HLT_isFired']# 'nPuVtxTrue', 'PV_N', 'bX']
met_outvars = ['MET_et', 'MET_phi', 'MET_sumEt', 'MET_significance']
evt_outvars = ['PV_N']
gen_outvars = ['genParticle_pdgId', 'genParticle_status', 'genParticle_dau', 'genParticle_mother', 'genParticle_pt', 'genParticle_eta', 'genParticle_phi', 'genParticle_mother_pt']
# , 'genParticle_Bdau_X_pt', 'genParticle_Bdau_X_eta', 'genParticle_Bdau_X_phi', 'genParticle_Bdau_X_id', 'genParticle_Bdau_mu1_pt', 'genParticle_Bdau_mu1_eta', 'genParticle_Bdau_mu1_phi', 'genParticle_Bdau_mu2_pt', 'genParticle_Bdau_mu2_eta', 'genParticle_Bdau_mu2_phi', 'genParticle_Bdau_Jpsi_pt', 'genParticle_Bdau_Jpsi_eta', 'genParticle_Bdau_Jpsi_phi'
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
if isGenLevel and not isData:
    for var in gen_outvars:
        chain.SetBranchStatus(var,1)

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
    
    if isGenLevel:
        Xbin = [13, 211, 321, 2212, 22, 310]
        sisterbin = [13, 111, 211, 213, 221, 331, 223, 333, 321, 313, 323, 411, 421, 443, 100443, 22, 310, 413, 11, 4122, 433, 423, 511, 311, 4232, 10413, 10411, 5122, 415, 2112, 20413, 435, 10431, 20423, 311, 431, 130]
        Bbin = [511, 521, 531, 541, 443, 431, 421, 411, 15, 5232, 100443]

JpsiMu_B_mcorr = num.zeros(1,dtype=float)
otree.Branch('JpsiMu_B_mcorr', JpsiMu_B_mcorr , 'JpsiMu_B_mcorr/D') 

JpsiMu_mu3_reliso= num.zeros(1,dtype=float)
otree.Branch('JpsiMu_mu3_reliso', JpsiMu_mu3_reliso, 'JpsiMu_mu3_reliso/D') 

JpsiMu_mu2_reliso= num.zeros(1,dtype=float)
otree.Branch('JpsiMu_mu2_reliso', JpsiMu_mu2_reliso, 'JpsiMu_mu2_reliso/D') 

JpsiMu_mu1_reliso= num.zeros(1,dtype=float)
otree.Branch('JpsiMu_mu1_reliso', JpsiMu_mu1_reliso, 'JpsiMu_mu1_reliso/D') 

JpsiMu_B_reliso= num.zeros(1,dtype=float)
otree.Branch('JpsiMu_B_reliso', JpsiMu_B_reliso, 'JpsiMu_B_reliso/D') 

JpsiMu_mu3_reldbiso= num.zeros(1,dtype=float)
otree.Branch('JpsiMu_mu3_reldbiso', JpsiMu_mu3_reldbiso, 'JpsiMu_mu3_reldbiso/D') 

JpsiMu_mu2_reldbiso= num.zeros(1,dtype=float)
otree.Branch('JpsiMu_mu2_reldbiso', JpsiMu_mu2_reldbiso, 'JpsiMu_mu2_reldbiso/D') 

JpsiMu_mu1_reldbiso= num.zeros(1,dtype=float)
otree.Branch('JpsiMu_mu1_reldbiso', JpsiMu_mu1_reldbiso, 'JpsiMu_mu1_reldbiso/D') 

dphi_Jpsi_mu3 = num.zeros(1,dtype=float)
otree.Branch('dphi_Jpsi_mu3', dphi_Jpsi_mu3, 'dphi_Jpsi_mu3/D') 
cosdphi_Jpsi_mu3 = num.zeros(1,dtype=float)
otree.Branch('cosdphi_Jpsi_mu3', cosdphi_Jpsi_mu3, 'cosdphi_Jpsi_mu3/D') 
dR_Jpsi_mu3 = num.zeros(1,dtype=float)
otree.Branch('dR_Jpsi_mu3', dR_Jpsi_mu3, 'dR_Jpsi_mu3/D') 

dphi_Jpsi_MET = num.zeros(1,dtype=float)
otree.Branch('dphi_Jpsi_MET', dphi_Jpsi_MET, 'dphi_Jpsi_MET/D')
cosdphi_Jpsi_MET = num.zeros(1,dtype=float)
otree.Branch('cosdphi_Jpsi_MET', cosdphi_Jpsi_MET, 'cosdphi_Jpsi_MET/D') 

dphi_mu3_MET = num.zeros(1,dtype=float)
otree.Branch('dphi_mu3_MET', dphi_mu3_MET, 'dphi_mu3_MET/D')
cosdphi_mu3_MET = num.zeros(1,dtype=float)
otree.Branch('cosdphi_mu3_MET', cosdphi_mu3_MET, 'cosdphi_mu3_MET/D') 

dphi_mu2_mu3 = num.zeros(1,dtype=float)
otree.Branch('dphi_mu2_mu3', dphi_mu2_mu3, 'dphi_mu2_mu3/D') 
cosdphi_mu2_mu3 = num.zeros(1,dtype=float)
otree.Branch('cosdphi_mu2_mu3', cosdphi_mu2_mu3, 'cosdphi_mu2_mu3/D') 
dR_mu2_mu3 = num.zeros(1,dtype=float)
otree.Branch('dR_mu2_mu3', dR_mu2_mu3, 'dR_mu2_mu3/D') 

dphi_mu1_mu3 = num.zeros(1,dtype=float)
otree.Branch('dphi_mu1_mu3', dphi_mu1_mu3, 'dphi_mu1_mu3/D') 
cosdphi_mu1_mu3 = num.zeros(1,dtype=float)
otree.Branch('cosdphi_mu1_mu3', cosdphi_mu1_mu3, 'cosdphi_mu1_mu3/D') 
dR_mu1_mu3 = num.zeros(1,dtype=float)
otree.Branch('dR_mu1_mu3', dR_mu1_mu3, 'dR_mu1_mu3/D') 

dphi_mu1_mu2 = num.zeros(1,dtype=float)
otree.Branch('dphi_mu1_mu2', dphi_mu1_mu2, 'dphi_mu1_mu2/D') 
cosdphi_mu1_mu2 = num.zeros(1,dtype=float)
otree.Branch('cosdphi_mu1_mu2', cosdphi_mu1_mu2, 'cosdphi_mu1_mu2/D') 
dR_mu1_mu2 = num.zeros(1,dtype=float)
otree.Branch('dR_mu1_mu2', dR_mu1_mu2, 'dR_mu1_mu2/D') 

if isGenLevel:
    Photon_mother = num.zeros(1,dtype=int)
    otree.Branch('Photon_mother', Photon_mother, 'Photon_mother/I') 
    B_type = num.zeros(1,dtype=int)
    otree.Branch('B_type', B_type, 'B_type/I') 
    X_Mother_pdgId = num.zeros(1,dtype=int)
    otree.Branch('X_Mother_pdgId', X_Mother_pdgId, 'X_Mother_pdgId/I') 
    X_type = num.zeros(1,dtype=int)
    otree.Branch('X_type', X_type, 'X_type/I') 
    X_pdgId = num.zeros(1,dtype=int)
    otree.Branch('X_pdgId', X_pdgId, 'X_pdgId/I') 
    sister_type = num.zeros(1,dtype=int)
    otree.Branch('sister_type', sister_type, 'sister_type/I') 
    genParticle_Bdau_dRmin = num.zeros(1,dtype=float)
    otree.Branch('genParticle_Bdau_dRmin', genParticle_Bdau_dRmin, 'genParticle_Bdau_dRmin/D')
    MultiMother = num.zeros(1,dtype=int)
    otree.Branch('MultiMother', MultiMother, 'MultiMother/I')
    genParticle_sister_pt = num.zeros(1,dtype=float)
    otree.Branch('genParticle_sister_pt', genParticle_sister_pt, 'genParticle_sister_pt/D') 
    genParticle_sister_pdgId = num.zeros(1,dtype=int)
    otree.Branch('genParticle_sister_pdgId', genParticle_sister_pdgId, 'genParticle_sister_pdgId/I') 
    genParticle_cousin_pt = num.zeros(1,dtype=float)
    otree.Branch('genParticle_cousin_pt', genParticle_cousin_pt, 'genParticle_cousin_pt/D') 
    genParticle_cousin_pdgId = num.zeros(1,dtype=int)
    otree.Branch('genParticle_cousin_pdgId', genParticle_cousin_pdgId, 'genParticle_cousin_pdgId/I') 
    genParticle_aunt_pt = num.zeros(1,dtype=float)
    otree.Branch('genParticle_aunt_pt', genParticle_aunt_pt, 'genParticle_aunt_pt/D') 
    genParticle_aunt_pdgId = num.zeros(1,dtype=int)
    otree.Branch('genParticle_aunt_pdgId', genParticle_aunt_pdgId, 'genParticle_aunt_pdgId/I') 
    genParticle_grandmother_pt = num.zeros(1,dtype=float)
    otree.Branch('genParticle_grandmother_pt', genParticle_cousin_pt, 'genParticle_grandmother_pt/D') 
    genParticle_grandmother_pdgId = num.zeros(1,dtype=int)
    otree.Branch('genParticle_grandmother_pdgId', genParticle_grandmother_pdgId, 'genParticle_grandmother_pdgId/I') 
    if isSignal:
        genParticle_Bdau_OtherB_dRmin = num.zeros(1,dtype=float)
        otree.Branch('genParticle_Bdau_OtherB_dRmin', genParticle_Bdau_OtherB_dRmin, 'genParticle_Bdau_OtherB_dRmin/D')

        mismatched_B= num.zeros(1,dtype=int)
        otree.Branch('mismatched_B', mismatched_B, 'mismatched_B/I')

        mismatched_mu1= num.zeros(1,dtype=int)
        otree.Branch('mismatched_mu1', mismatched_mu1, 'mismatched_mu1/I')

        mismatched_mu2= num.zeros(1,dtype=int)
        otree.Branch('mismatched_mu2', mismatched_mu2, 'mismatched_mu2/I')

        mismatched_mu3= num.zeros(1,dtype=int)
        otree.Branch('mismatched_mu3', mismatched_mu3, 'mismatched_mu3/I')

        isMismatched = num.zeros(1,dtype=int)
        otree.Branch('isMismatched',isMismatched, 'isMismatched/I')

Nentries = chain.GetEntries()

print 'Total Number of entries to proces  = ', Nentries 
evtid = 0


if not isData:
    puTool         = PileupWeightTool(year=2018)

MJpsi=3.096916
MMu=0.1056583745
#if not isData:
cuthist.Fill(0, nevts)
print "Running over", Nentries, "entries!"
NBadMatches = 0
NJpsiB = 0
NNotMu = 0
for evt in xrange(Nentries):
    chain.GetEntry(evt)

    if evt%100000==0: print '{0:.2f}'.format(Double(evt)/Double(Nentries)*100.), '% processed'
    #if evt>100: break


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
 
           



    mu3ptcut = 2
    selectedjpsi = -1
    for iJpsi in xrange(chain.JpsiMu_mu3_pt.size()):
        if chain.JpsiMu_mu3_pt.size() < 1: continue
        if chain.JpsiMu_Jpsi_pt[iJpsi] < 8: continue
        if chain.JpsiMu_B_mass[iJpsi] > 9: continue
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
    pJpsi = TLorentzVector.TLorentzVector()
    pB = TLorentzVector.TLorentzVector()
    pmu1 = TLorentzVector.TLorentzVector()
    pmu2 = TLorentzVector.TLorentzVector()
    pmu3 = TLorentzVector.TLorentzVector()
    pmet = TLorentzVector.TLorentzVector()
    pJpsi.SetPtEtaPhiM(chain.JpsiMu_Jpsi_pt[selectedjpsi], chain.JpsiMu_Jpsi_eta[selectedjpsi], chain.JpsiMu_Jpsi_phi[selectedjpsi], MJpsi)
    pmu1.SetPtEtaPhiM(chain.JpsiMu_mu1_pt[selectedjpsi], chain.JpsiMu_mu1_eta[selectedjpsi], chain.JpsiMu_mu1_phi[selectedjpsi], MMu)
    pmu2.SetPtEtaPhiM(chain.JpsiMu_mu2_pt[selectedjpsi], chain.JpsiMu_mu2_eta[selectedjpsi], chain.JpsiMu_mu2_phi[selectedjpsi], MMu)
    pmu3.SetPtEtaPhiM(chain.JpsiMu_mu3_pt[selectedjpsi], chain.JpsiMu_mu3_eta[selectedjpsi], chain.JpsiMu_mu3_phi[selectedjpsi], MMu)
    pB.SetPtEtaPhiM(chain.JpsiMu_B_pt[selectedjpsi], chain.JpsiMu_B_eta[selectedjpsi], chain.JpsiMu_B_phi[selectedjpsi], chain.JpsiMu_B_mass[selectedjpsi])
    pmet.SetPtEtaPhiE(chain.MET_et[0], 2, chain.MET_phi[0], -chain.MET_et[0])

    pperp = pB.P() * TMath.Sin(TMath.ACos(chain.JpsiMu_B_alpha[selectedjpsi]))
    JpsiMu_B_mcorr[0] = TMath.Sqrt( (chain.JpsiMu_B_mass[selectedjpsi])**2 + pperp**2 ) + pperp

    dphi_Jpsi_mu3[0] = pJpsi.DeltaPhi(pmu3)
    dphi_mu1_mu3[0] = pmu1.DeltaPhi(pmu3)
    dphi_mu1_mu2[0] = pmu1.DeltaPhi(pmu2)
    dphi_mu2_mu3[0] = pmu2.DeltaPhi(pmu3)
    dphi_Jpsi_MET[0] = pJpsi.DeltaPhi(pmet)
    dphi_mu3_MET[0] = pmu3.DeltaPhi(pmet)
    dR_Jpsi_mu3[0] = pJpsi.DeltaR(pmu3)
    dR_mu1_mu3[0] = pmu1.DeltaR(pmu3)
    dR_mu1_mu2[0] = pmu1.DeltaR(pmu2)
    dR_mu2_mu3[0] = pmu2.DeltaR(pmu3)
    cosdphi_Jpsi_mu3[0] = TMath.Cos(dphi_Jpsi_mu3[0])
    cosdphi_mu1_mu3[0] = TMath.Cos(dphi_mu1_mu3[0])
    cosdphi_mu1_mu2[0] = TMath.Cos(dphi_mu1_mu2[0])
    cosdphi_mu2_mu3[0] = TMath.Cos(dphi_mu2_mu3[0])
    cosdphi_Jpsi_MET[0] = TMath.Cos(dphi_Jpsi_MET[0])
    cosdphi_mu3_MET[0] = TMath.Cos(dphi_mu3_MET[0])

    JpsiMu_mu3_reliso[0] = chain.JpsiMu_mu3_iso[selectedjpsi]/chain.JpsiMu_mu3_pt[selectedjpsi]
    JpsiMu_mu2_reliso[0] = chain.JpsiMu_mu2_iso[selectedjpsi]/chain.JpsiMu_mu2_pt[selectedjpsi]
    JpsiMu_mu1_reliso[0] = chain.JpsiMu_mu1_iso[selectedjpsi]/chain.JpsiMu_mu1_pt[selectedjpsi]
    JpsiMu_B_reliso[0] = chain.JpsiMu_B_iso[selectedjpsi]/chain.JpsiMu_B_pt[selectedjpsi]
    JpsiMu_mu3_reldbiso[0] = chain.JpsiMu_mu3_dbiso[selectedjpsi]/chain.JpsiMu_mu3_pt[selectedjpsi]
    JpsiMu_mu2_reldbiso[0] = chain.JpsiMu_mu2_dbiso[selectedjpsi]/chain.JpsiMu_mu2_pt[selectedjpsi]
    JpsiMu_mu1_reldbiso[0] = chain.JpsiMu_mu1_dbiso[selectedjpsi]/chain.JpsiMu_mu1_pt[selectedjpsi]

# Gen Level Info

    if not isData and isGenLevel > 0:
        def getmatches(thresh, momentum):
            gen_num = -1
            pgen = TLorentzVector.TLorentzVector()
            matches = []
            for iGen in xrange(chain.genParticle_pdgId.size()):
                if chain.genParticle_status[iGen] != 1: continue
                if abs(chain.genParticle_pdgId[iGen]) == 12: continue
                if abs(chain.genParticle_pdgId[iGen]) == 14: continue
                if abs(chain.genParticle_pdgId[iGen]) == 16: continue
                pgen.SetPtEtaPhiM(chain.genParticle_pt[iGen], chain.genParticle_eta[iGen], chain.genParticle_phi[iGen], MMu)
                dR = pgen.DeltaR(momentum)
                if dR <= thresh:
                    matches += [[iGen, dR]] 
            return matches

        def mindr(matches, thresh):
            bestmatch = [-1, thresh]
            for match in matches:
                if match[1] <= thresh:
                    bestmatch = match
            return bestmatch
        def checkdupes(matchlist, threshlist):
            drlist = []
            hasdupes = False
            for iParticle in xrange(len(matchlist)):
                drlist += [mindr(matchlist[iParticle], threshlist[iParticle])]
            for iParticle in xrange(len(drlist)):
                for iParticle2 in xrange(len(drlist)):
                    if iParticle2 <= iParticle: continue
                    if drlist[iParticle][0] == drlist[iParticle2][0]:
                        hasdupes = True
                        break
                    else: continue
                    break
                break
            return hasdupes

        def removedupes(matchlist, threshlist):
            if not checkdupes(matchlist, threshlist):
                return matchlist
            else:
                drlist = []
                matchlist2 = matchlist
                for iParticle in xrange(len(matchlist)):
                    drlist += [mindr(matchlist[iParticle], threshlist[iParticle])]
                for iParticle in xrange(len(drlist)):
                    for iParticle2 in xrange(len(drlist)):
                        if iParticle2 <= iParticle: continue
                        if drlist[iParticle][0] == drlist[iParticle2][0]:
                            for imatch1 in xrange(len(matchlist[iParticle])):
                                if matchlist[iParticle][imatch1][0] != drlist[iParticle][0]: 
                                    continue
                                for imatch2 in xrange(len(matchlist[iParticle2])):
                                    if matchlist[iParticle2][imatch2][0] != drlist[iParticle2][0]: 
                                        continue
                                    if drlist[iParticle][1] >= drlist[iParticle2][1]:
                                        del matchlist2[iParticle][imatch1]
                                    else:
                                        del matchlist2[iParticle2][imatch2]
                for iParticle in xrange(len(matchlist2)):
                    if matchlist2[iParticle] == []:
                        return matchlist2
                    else: break
                if len(matchlist2) ==0:
                    return matchlist2
                else:
                    return removedupes(matchlist2, threshlist)

        def multimindr(threshlist, momentumlist):
            matchlist = []
            drlist = []
            for iParticle in xrange(len(threshlist)):
                matchlist += [getmatches(threshlist[iParticle], momentumlist[iParticle])]
            matchlist2 = removedupes(matchlist, threshlist)
            for iParticle in xrange(len(matchlist2)):
                drlist += [mindr(matchlist2[iParticle], threshlist[iParticle])]
            return drlist
    
        def getmotherids(gen_num):
            pdgid_list = chain.genParticle_mother[gen_num]
            pt_list = chain.genParticle_mother_pt[gen_num]
            idlist = []
            for imom in xrange(len(pdgid_list)):
                for iGen in xrange(chain.genParticle_pdgId.size()):
                    if chain.genParticle_status[iGen] != 2: continue
                    if chain.genParticle_pdgId[iGen] == pdgid_list[imom]:
                        if chain.genParticle_pt[iGen] == pt_list[imom]:
                            idlist += [iGen]
            return idlist
        def getdaughterids(gen_num, NoIntermediateParticles = True, NoNu = False):
            pt = chain.genParticle_pt[gen_num]
            pdgid= chain.genParticle_pdgId[gen_num]
            daulist = []
            for iGen in xrange(chain.genParticle_pdgId.size()):
                if iGen == gen_num: continue
                if NoNu:
                    if abs(chain.genParticle_pdgId[iGen]) == 12: continue
                    if abs(chain.genParticle_pdgId[iGen]) == 14: continue
                    if abs(chain.genParticle_pdgId[iGen]) == 16: continue
                if NoIntermediateParticles:
                    if chain.genParticle_status[iGen] != 1: continue
                else:
                    if chain.genParticle_status[iGen] != 2 and chain.genParticle_status[iGen] != 1: continue
                momlist = chain.genParticle_mother[iGen]
                momptlist = chain.genParticle_mother_pt[iGen]
                isdau = False
                for imom in xrange(len(momlist)):
                    if momlist[imom] == pdgid and momptlist[imom] == pt:
                        isdau = True
                        break
                if isdau: 
                    daulist += [iGen]
            return daulist
        def getsisterids(gen_num, NoIntermediateParticles = True, NoNu = False):
            mothers = getmotherids(gen_num)
            sisters0 = []
            for mom in mothers:
                sisters0 += getdaughterids(mom, NoIntermediateParticles, NoNu)
            # remove duplicates
            sisters = list(set(sisters0))
            # make sure the original particle isn't counted as a sister
            for isis in xrange(len(sisters)):
                if sisters[isis] == gen_num:
                    del sisters[isis]
                    break
            return sisters

        def getgrandmotherids(gen_num):
            mothers = getmotherids(gen_num)
            grandmas = []
            for mom in mothers:
                grandmas += getmotherids(mom)
            return list(set(grandmas))
        
        def getauntids(gen_num):
            mothers = getmotherids(gen_num)
            aunts0 = []
            for mother in mothers:
                aunts0 += getsisterids(mother, False)
            return list(set(aunts0))

        def getcousinids(gen_num, AsymptoticOnly = True, NoNu = False):
            cousins0 = []
            aunts = getauntids(gen_num)
            for aunt in aunts: 
                cousins0 += getdaughterids(aunt, AsymptoticOnly, NoNu)
            return list(set(cousins0))
            
        psis = TLorentzVector.TLorentzVector()
        pmu3_gen = TLorentzVector.TLorentzVector()
        dRthresh_mu1 = 0.1
        dRthresh_mu2 = 0.1
        dRthresh_mu3 = 0.1
        genmatch_thresh_list = [dRthresh_mu1, dRthresh_mu2, dRthresh_mu3]
        # first we pick out what gen level particle our reco mu3 most likely corresponds to
        matchedparticles = multimindr(genmatch_thresh_list, [pmu1, pmu2, pmu3])
        mu1_gen_num = matchedparticles[0][0]
        mu2_gen_num = matchedparticles[1][0]
        mu3_gen_num = matchedparticles[2][0]
        pmu3_gen.SetPtEtaPhiM(chain.genParticle_pt[mu3_gen_num], chain.genParticle_eta[mu3_gen_num], chain.genParticle_phi[mu3_gen_num], MMu)
        if mu3_gen_num == -1: continue
        if chain.genParticle_pdgId[mu3_gen_num] == 22:
                Photon_mother = chain.genParticle_mother[mu3_gen_num]
        #now getting the sisters, mothers, etc
        sisterlist = getsisterids(mu3_gen_num)
        unasymptoticsisterlist = getsisterids(mu3_gen_num, False)
        for sister in unasymptoticsisterlist:
            if abs(chain.genParticle_pdgId[sister]) == 12: continue
            if abs(chain.genParticle_pdgId[sister]) == 14: continue
            if abs(chain.genParticle_pdgId[sister]) == 16: continue
            for index in xrange(len(sisterbin)):
                if sisterbin[index] == abs(chain.genParticle_pdgId[sister]):
                    Other = False
                    sister_type[0] = index + 1
                    break
                else: 
                    Other = True
            if Other == True:
               print "Sister ID:", chain.genParticle_pdgId[sister]
               sister_type[0] = len(sisterbin)+1
        X_pdgId[0] = TMath.Abs(chain.genParticle_pdgId[mu3_gen_num])
        for sister in unasymptoticsisterlist:
            if genParticle_sister_pdgId[0] == 0:
                genParticle_sister_pdgId[0] = TMath.Abs(chain.genParticle_pdgId[sister])
                genParticle_sister_pt[0] = chain.genParticle_pt[sister]
            else:
                genParticle_sister_pdgId += [TMath.Abs(chain.genParticle_pdgId[sister])]
                genParticle_sister_pt += [chain.genParticle_pt[sister]]
        motherlist = getmotherids(mu3_gen_num)
        for mother in motherlist:
            if X_Mother_pdgId[0] == 0:
                X_Mother_pdgId[0] = TMath.Abs(chain.genParticle_pdgId[mother])
            else:
                X_Mother_pdgId += [chain.genParticle_pdgId[mother]]
        auntlist = getauntids(mu3_gen_num)
        for aunt in auntlist:
            if genParticle_aunt_pdgId[0] == 0:
                genParticle_aunt_pdgId[0] = chain.genParticle_pdgId[aunt]
                genParticle_aunt_pt[0] = chain.genParticle_pt[aunt]
            else:
                genParticle_aunt_pdgId += [chain.genParticle_pdgId[aunt]]
                genParticle_aunt_pt += [chain.genParticle_pt[aunt]]
        cousinlist = getcousinids(mu3_gen_num)
        for cousin in cousinlist:
            if genParticle_cousin_pdgId[0] == 0:
                genParticle_cousin_pdgId[0] = chain.genParticle_pdgId[cousin]
                genParticle_cousin_pt[0] = chain.genParticle_pt[cousin]
            else:
                genParticle_cousin_pdgId += [chain.genParticle_pdgId[cousin]]
                genParticle_cousin_pt += [chain.genParticle_pt[cousin]]
        grandmotherlist = getgrandmotherids(mu3_gen_num)
        for grandmother in grandmotherlist:
            if genParticle_grandmother_pdgId[0] == 0:
                genParticle_grandmother_pdgId[0] = chain.genParticle_pdgId[grandmother]
                genParticle_grandmother_pt[0] = chain.genParticle_pt[grandmother]
            else:
                genParticle_grandmother_pdgId += [chain.genParticle_pdgId[grandmother]]
                genParticle_grandmother_pt += [chain.genParticle_pt[grandmother]]
        immediate_family = unasymptoticsisterlist+motherlist
        if len(sisterlist) == 0: continue
        iclosestSis = -1
        dRthresh_dau = -1
        # Finding the closest visible sister
        for iSis in sisterlist:
            if iSis == mu3_gen_num: continue
            if chain.genParticle_status[iSis] != 1: continue
            if abs(chain.genParticle_pdgId[iSis]) == 12: continue
            if abs(chain.genParticle_pdgId[iSis]) == 14: continue
            if abs(chain.genParticle_pdgId[iSis]) == 16: continue
            psis.SetPtEtaPhiM(chain.genParticle_pt[iSis], chain.genParticle_eta[iSis], chain.genParticle_phi[iSis], MMu)
            dR = psis.DeltaR(pmu3_gen)
            if iSis == sisterlist[0] and dRthresh_dau == -1: dRthresh_dau = dR
            if dR <= dRthresh_dau:
                dRthresh_dau = dR
                iclosestSis = iSis
            
        genParticle_Bdau_dRmin[0] = dRthresh_dau
        Other = True
        X_type[0] = -1
        for index in xrange(len(Xbin)):
            if Xbin[index] == abs(chain.genParticle_pdgId[mu3_gen_num]):
                Other = False
                X_type[0] = index + 1
                break
            else: 
                Other = True
        if Other == True:
           X_type[0] = len(Xbin)+1
           #print "X ID:", chain.genParticle_pdgId[mu3_gen_num]
        B_type[0] = -1
        if len(chain.genParticle_mother[mu3_gen_num]) > 1: 
            MultiMother[0] = 1
            for mom in xrange(len(chain.genParticle_mother[mu3_gen_num])):
                Other = True
                for index in xrange(len(Bbin)):
                    if Bbin[index] == abs(chain.genParticle_mother[mu3_gen_num][mom]):
                        Other = False
                        if B_type[0] == -1: B_type[0] = index + 1
                        else:
                            B_type += [index + 1]
                        break
                    else:
                        Other = True
                if Other == True:       
                    if B_type[0] == -1: B_type[0] = len(Bbin)+1
                    else: B_type += [len(Bbin)+1]
        else:
            MultiMother[0] = 0
            Other = True
            for index in xrange(len(Bbin)):
                if Bbin[index] == abs(chain.genParticle_mother[mu3_gen_num][0]):
                    Other = False
                    B_type[0] = index + 1
                    break
                else: Other = True
            if Other == True:
                B_type[0] = len(Bbin)+1
                print "ID of B Classified as Other:", abs(chain.genParticle_mother[mu3_gen_num][0])
        if isSignal:
            isBadMatch = False
            isNotBc = False
            isJpsi = False
            isNotMu = False
            for iB in xrange(len(B_type)):
                if B_type[iB] != 9:
                    isBadMatch = True
                    isNotBc = True
                    if abs(chain.genParticle_mother[mu3_gen_num][iB]) == 443:
                        isJpsi = True
                    break
            if X_type[0] != 1: 
                isBadMatch = True
                isNotMu = True
            if isBadMatch:
                NBadMatches += 1
                mismatched_mu1[0] = abs(chain.genParticle_pdgId[mu1_gen_num])
                mismatched_mu2[0] = abs(chain.genParticle_pdgId[mu2_gen_num])
                mismatched_mu3[0] = Xbin[X_type[0]-1]
                isMismatched[0] = 1
               # print "Mu 3 matched to pdgID ", X_pdgId[0]
               # if B_type[0] > len(Bbin):
               #     print "B: ", chain.genParticle_mother[mu3_gen_num][0]
               # else:
               #     print "B: ", Bbin[B_type[0]-1]
               # print "Sisters: "
               # for sister in sisterlist:
               #     print chain.genParticle_pdgId[sister]
            if isJpsi:
                NJpsiB +=1
            if isNotMu:
                NNotMu +=1
            if isBadMatch and not isJpsi:
                if B_type[0]<len(Bbin): 
                    mismatched_B[0] = Bbin[B_type[0]-1]
                #    print "Mismatched B: ", mismatched_B[0]
                else:
                    mismatched_B[0] = abs(chain.genParticle_mother[mu3_gen_num][0])
                #    print "Mismatched B: ", mismatched_B[0]
                #if len(B_type)>1:
                #    print "Other mom:", abs(chain.genParticle_mother[mu3_gen_num][1])
            elif isBadMatch and isJpsi:
                mismatched_B[0] = 443
        # Now we look at the other b in the event and note its daughters
        if isSignal:
            MomNum2 = -1
            pmom2 = TLorentzVector.TLorentzVector()
            OtherMother = False
            for iGen in xrange(chain.genParticle_pdgId.size()):
                if OtherMother == True: break
                if iGen == mu3_gen_num: continue
                if abs(chain.genParticle_pdgId[iGen]) < 600 and abs(chain.genParticle_pdgId[iGen]) >= 500:
                    for iRel in xrange(len(immediate_family)):
                        if OtherMother == True: continue
                        if chain.genParticle_pt[iGen] == chain.genParticle_pt[immediate_family[iRel]]: continue
                        OtherMother == True
                        MomNum2 = iGen
                        mompt2 = chain.genParticle_pt[iGen]
                        pmom2.SetPtEtaPhiM(chain.genParticle_pt[iGen], chain.genParticle_eta[iGen], chain.genParticle_phi[iGen], MMu)
            dR = 0
            dauID = 0
            dRmin = -1
            otherdaughters = getdaughterids(MomNum2)
#            for daughter in otherdaughters:
#                print chain.genParticle_pdgId[daughter]
            pdau = TLorentzVector.TLorentzVector()
            for iDau in otherdaughters:
                if abs(chain.genParticle_pdgId[iDau]) == 12: continue
                if abs(chain.genParticle_pdgId[iDau]) == 14: continue
                if abs(chain.genParticle_pdgId[iDau]) == 16: continue
                if iDau == mu3_gen_num: continue
                if chain.genParticle_status[iDau] != 1 and chain.genParticle_status[iDau] != 2: continue
                pdau.SetPtEtaPhiM(chain.genParticle_pt[iDau], chain.genParticle_eta[iDau], chain.genParticle_phi[iDau], MMu)
                dR = pdau.DeltaR(pmu3)
                if dRmin == -1: dRmin = dR
                if dR <= dRmin:
                    dauID = chain.genParticle_pdgId[iDau]
                    dRmin = dR
            #if dRmin == -1: continue
            genParticle_Bdau_OtherB_dRmin[0] = dRmin
        #print "-----------------------------------------------------"
        #print "imu1 gen:", mu1_gen_num
        #print "mu1 gen lv PT:" , chain.genParticle_pt[mu1_gen_num]
        #print "pdgid:", chain.genParticle_pdgId[mu1_gen_num]
        #print "imu2 gen:", mu2_gen_num
        #print "mu2 gen lv PT:" , chain.genParticle_pt[mu2_gen_num] 
        #print "pdgid:", chain.genParticle_pdgId[mu2_gen_num]
        #print "imu3 gen:", mu3_gen_num
        #print "mu3 gen lv PT:" , chain.genParticle_pt[mu3_gen_num]
        #print "pdgid:", chain.genParticle_pdgId[mu3_gen_num]
        #print "min dR between this and its sisters:", dRthresh_dau
        #print "iclosest sister:", iclosestSis
        #print "closest sister:", chain.genParticle_pdgId[iclosestSis]
        #print "closest sister PT:", chain.genParticle_pt[iclosestSis]
        #print "closest mother:", motherlist
        #if isSignal:
        #    print "Closest gen particle from other B:", dauID
        #    print "with delta R:", dRthresh_other_B
        #    print "Daughters of Other B:", otherdaughters
        #print "-----------------------------------------------------"

    for var in outvars:
        tmp = getattr(chain,var)[selectedjpsi]
        getattr(chain,var).clear()
        getattr(chain,var).push_back(tmp)
    for var in met_outvars:
        tmp = getattr(chain,var)[0]
        getattr(chain,var).clear()
        getattr(chain,var).push_back(tmp)
    #if isGenLevel:
    #    for iGen in xrange(chain.genParticle_pdgId.size()):
    #        for var in gen_outvars:
    #            print iGen, var
    #            tmp = getattr(chain,var)[0]
    #            print tmp
    #            getattr(chain,var).clear()
    #            getattr(chain,var).push_back(tmp)
    #        otree.Fill()

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
print NJpsiB, "- Number of X coming from Jpsi"
print NNotMu, "- Number of X which are not muons"
print NBadMatches, "- Number of X coming from a particle which is not Bc"
