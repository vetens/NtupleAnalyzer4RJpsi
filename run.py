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
outvars = ['JpsiMu_Jpsi_lip', 'JpsiMu_Jpsi_lips', 'JpsiMu_Jpsi_pvip', 'JpsiMu_Jpsi_pvips', 'JpsiMu_B_pvip', 'JpsiMu_B_pvips', 'JpsiMu_B_lips', 'JpsiMu_B_fls3d', 'JpsiMu_Jpsi_unfit_mass', 'JpsiMu_B_iso', 'JpsiMu_B_iso_ntracks', 'JpsiMu_B_iso_mindoca', 'JpsiMu_B_fl3d', 'JpsiMu_B_lip', 'JpsiMu_B_mass', 'JpsiMu_B_pt', 'JpsiMu_B_eta', 'JpsiMu_B_phi', 'JpsiMu_B_maxdoca', 'JpsiMu_B_mindoca', 'JpsiMu_Jpsi_maxdoca', 'JpsiMu_Jpsi_mindoca', 'JpsiMu_Jpsi_alpha', 'JpsiMu_Jpsi_fl3d', 'JpsiMu_Jpsi_fls3d', 'JpsiMu_Jpsi_pt', 'JpsiMu_Jpsi_eta', 'JpsiMu_Jpsi_phi', 'JpsiMu_mu1_iso', 'JpsiMu_mu1_dbiso', 'JpsiMu_mu2_iso', 'JpsiMu_mu2_dbiso', 'JpsiMu_mu3_iso', 'JpsiMu_mu3_dbiso', 'JpsiMu_mu1_isSoft', 'JpsiMu_mu1_isTracker', 'JpsiMu_mu1_isGlobal', 'JpsiMu_mu1_isPF', 'JpsiMu_mu1_isTight', 'JpsiMu_mu1_isLoose', 'JpsiMu_mu2_isSoft', 'JpsiMu_mu2_isTracker', 'JpsiMu_mu2_isGlobal', 'JpsiMu_mu2_isPF', 'JpsiMu_mu2_isTight', 'JpsiMu_mu2_isLoose', 'JpsiMu_mu3_isSoft', 'JpsiMu_mu3_isTracker', 'JpsiMu_mu3_isGlobal', 'JpsiMu_mu3_isPF', 'JpsiMu_mu3_isTight', 'JpsiMu_mu3_isLoose', 'JpsiMu_mu3_pt', 'JpsiMu_mu3_eta', 'JpsiMu_mu3_phi', 'JpsiMu_mu3_doca2mu1', 'JpsiMu_mu3_doca2mu2', 'JpsiMu_B_alpha', 'JpsiMu_Jpsi_vprob', 'JpsiMu_B_vprob', 'JpsiMu_mu1_pt', 'JpsiMu_mu1_eta', 'JpsiMu_mu1_phi', 'JpsiMu_mu2_pt', 'JpsiMu_mu2_eta', 'JpsiMu_mu2_phi']# 'nPuVtxTrue', 'PV_N', 'bX']
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
if len(gen_outvars) > 0 and not isData:
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
    
    Xbin = [13,111,211,113,213,221,331,223,333,311,321,313,323,411,421,441,551,553]

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

if len(gen_outvars) > 0:
    B_pdgId = num.zeros(1,dtype=int)
    otree.Branch('B_pdgId', B_pdgId, 'B_pdgId/I') 
    X_type = num.zeros(1,dtype=int)
    otree.Branch('X_type', X_type, 'X_type/I') 
    genParticle_Bdau_dR = num.zeros(1,dtype=float)
    otree.Branch('genParticle_Bdau_dR', genParticle_Bdau_dR, 'genParticle_Bdau_dR/D')

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

    if not isData and len(gen_outvars) > 0:
        Xmomenta = []
        pmu1 = TLorentzVector.TLorentzVector()
        pmu2 = TLorentzVector.TLorentzVector()
        pB = TLorentzVector.TLorentzVector()
        pB.SetPtEtaPhiM(0,0,0,0)
        pJpsi = TLorentzVector.TLorentzVector()
        pJpsi.SetPtEtaPhiM(0,0,0,0)
        iJpsi = -1
        iB = -1
        Xids = []
        for iGen in xrange(chain.genParticle_pdgId.size()):
            ID = chain.genParticle_pdgId[iGen]
            if ID == 443 and chain.genParticle_status[iGen] == 2 and chain.genParticle_pt[iGen] > pJpsi.Pt():
                pJpsi.SetPtEtaPhiM(chain.genParticle_pt[iGen], chain.genParticle_eta[iGen], chain.genParticle_phi[iGen], MJpsi)
                iJpsi = iGen
            if abs(ID) >= 500 and abs(ID) < 600 and chain.genParticle_status[iGen] == 2:
                iB = iGen
                pB.SetPtEtaPhiM(chain.genParticle_pt[iGen], chain.genParticle_eta[iGen], chain.genParticle_phi[iGen], 6.)
                for iDau in xrange(chain.genParticle_dau[iGen].size()):
                    dauID = abs(chain.genParticle_dau[iGen][iDau])
                    if abs(dauID) == 12 or abs(dauID) == 14 or abs(dauID) == 16: continue
                    if dauID == 443: continue
                    # looking at Background, so we expect the only muons to come from our Jpsi
                    if abs(dauID) == 13: continue
                    else:
                        Xids += [dauID]
        for iGen in xrange(chain.genParticle_pdgId.size()):
            for mompt in chain.genParticle_mother_pt:
                if mompt == pJpsi.Pt() and chain.genParticle_pdgId(iGen) == 13:
                    pmu1.SetPtEtaPhiM(chain.genParticle_pt[iGen], chain.genParticle_eta[iGen], chain.genParticle_phi[iGen], MMu)
                elif mompt == pJpsi.Pt() and chain.genParticle_pdgId(iGen) == -13:
                    pmu1.SetPtEtaPhiM(chain.genParticle_pt[iGen], chain.genParticle_eta[iGen], chain.genParticle_phi[iGen], MMu)
                elif mompt == pB.Pt():
                    for Xid in Xids:
                        if chain.genParticle_pdgId[iGen] == Xid:
                            for index in xrange(Xbin):
                                if Xbin[index] == abs(dauID):
                                    if X_type[0] == 0: X_type[0] = index
                                    else:
                                        X_type += [index]
                                else:
                                    if X_type[0] == 0: X_type[0] = -1
                                    else: X_type += [-1]
                            pX = TLorentzVector.TLorentzVector()
                            pX.SetPtEtaPhiM(chain.genParticle_pt[iGen], chain.genParticle_eta[iGen], chain.genParticle_phi[iGen], MMu)
                            Xmomenta += [pX]
        Xmomenta += [pmu1, pmu2]
        Delta_R = pmu1.DeltaR(pmu2)
        for ip1 in xrange(len(Xmomenta)):
            for ip2 in xrange(len(Xmomenta)):
                if ip2 <= ip1: continue
                DR = Xmomenta[ip1].DeltaR(Xmomenta[ip2])
                if DR >= Delta_R:
                    Delta_R = DR
        genParticle_Bdau_dR[0] = Delta_R

    for var in outvars:
        tmp = getattr(chain,var)[selectedjpsi]
        getattr(chain,var).clear()
        getattr(chain,var).push_back(tmp)
    for var in met_outvars:
        tmp = getattr(chain,var)[0]
        getattr(chain,var).clear()
        getattr(chain,var).push_back(tmp)
   # if not isData and len(gen_outvars) > 0:
   #     tmp = getattr(chain,var)[0]
   #     getattr(chain,var).clear()
   #     getattr(chain,var).push_back(tmp)
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
