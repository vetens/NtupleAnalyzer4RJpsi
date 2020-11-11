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
outvars = ['JpsiMu_Jpsi_lip', 'JpsiMu_Jpsi_lips', 'JpsiMu_Jpsi_pvip', 'JpsiMu_Jpsi_pvips', 'JpsiMu_B_pvip', 'JpsiMu_B_pvips', 'JpsiMu_B_lips', 'JpsiMu_B_fls3d', 'JpsiMu_Jpsi_unfit_mass', 'JpsiMu_B_iso', 'JpsiMu_B_iso_ntracks', 'JpsiMu_B_iso_mindoca', 'JpsiMu_B_fl3d', 'JpsiMu_B_lip', 'JpsiMu_B_mass', 'JpsiMu_B_pt', 'JpsiMu_B_eta', 'JpsiMu_B_phi', 'JpsiMu_B_maxdoca', 'JpsiMu_B_mindoca', 'JpsiMu_Jpsi_maxdoca', 'JpsiMu_Jpsi_mindoca', 'JpsiMu_Jpsi_alpha', 'JpsiMu_Jpsi_fl3d', 'JpsiMu_Jpsi_fls3d', 'JpsiMu_Jpsi_pt', 'JpsiMu_Jpsi_eta', 'JpsiMu_Jpsi_phi', 'JpsiMu_mu1_dbiso', 'JpsiMu_mu2_dbiso', 'JpsiMu_mu3_dbiso', 'JpsiMu_mu1_isSoft', 'JpsiMu_mu1_isTracker', 'JpsiMu_mu1_isGlobal', 'JpsiMu_mu1_isPF', 'JpsiMu_mu1_isTight', 'JpsiMu_mu1_isLoose', 'JpsiMu_mu2_isSoft', 'JpsiMu_mu2_isTracker', 'JpsiMu_mu2_isGlobal', 'JpsiMu_mu2_isPF', 'JpsiMu_mu2_isTight', 'JpsiMu_mu2_isLoose', 'JpsiMu_mu3_isSoft', 'JpsiMu_mu3_isTracker', 'JpsiMu_mu3_isGlobal', 'JpsiMu_mu3_isPF', 'JpsiMu_mu3_isTight', 'JpsiMu_mu3_isLoose', 'JpsiMu_mu3_pt', 'JpsiMu_mu3_eta', 'JpsiMu_mu3_phi', 'JpsiMu_mu3_doca2mu1', 'JpsiMu_mu3_doca2mu2', 'JpsiMu_B_alpha', 'JpsiMu_Jpsi_vprob', 'JpsiMu_B_vprob', 'JpsiMu_mu1_pt', 'JpsiMu_mu1_eta', 'JpsiMu_mu1_phi', 'JpsiMu_mu2_pt', 'JpsiMu_mu2_eta', 'JpsiMu_mu2_phi']#, 'nPuVtxTrue', 'PV_N', 'bX']
#met_outvars = ['MET_et', 'MET_phi', 'MET_sumEt']#, 'MET_significance']
evt_outvars = ['PV_N']
gen_outvars = ['genParticle_pdgId', 'genParticle_status', 'genParticle_dau', 'genParticle_mother', 'genParticle_pt', 'genParticle_eta', 'genParticle_phi', 'genParticle_mother_pt']
mc_vars = ['nPuVtxTrue', 'bX']
trig_vars = ['HLT_BPH_isFired']
if not isData:
    evt_outvars = evt_outvars + mc_vars
chain.SetBranchStatus('*', 0)
for var in outvars:
    chain.SetBranchStatus(var, 1)
#for var in met_outvars:
    #chain.SetBranchStatus(var, 1)
for var in evt_outvars:
    chain.SetBranchStatus(var, 1)
for var in trig_vars:
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

JpsiMu_B_mcorr = num.zeros(1,dtype=float)
otree.Branch('JpsiMu_B_mcorr', JpsiMu_B_mcorr , 'JpsiMu_B_mcorr/D') 

JpsiMu_B_reliso= num.zeros(1,dtype=float)
otree.Branch('JpsiMu_B_reliso', JpsiMu_B_reliso, 'JpsiMu_B_reliso/D') 

JpsiMu_mu3_reldbiso= num.zeros(1,dtype=float)
otree.Branch('JpsiMu_mu3_reldbiso', JpsiMu_mu3_reldbiso, 'JpsiMu_mu3_reldbiso/D') 

JpsiMu_mu2_reldbiso= num.zeros(1,dtype=float)
otree.Branch('JpsiMu_mu2_reldbiso', JpsiMu_mu2_reldbiso, 'JpsiMu_mu2_reldbiso/D') 

JpsiMu_mu1_reldbiso= num.zeros(1,dtype=float)
otree.Branch('JpsiMu_mu1_reldbiso', JpsiMu_mu1_reldbiso, 'JpsiMu_mu1_reldbiso/D') 

#dphi_Jpsi_MET = num.zeros(1,dtype=float)
#otree.Branch('dphi_Jpsi_MET', dphi_Jpsi_MET, 'dphi_Jpsi_MET/D')
#cosdphi_Jpsi_MET = num.zeros(1,dtype=float)
#otree.Branch('cosdphi_Jpsi_MET', cosdphi_Jpsi_MET, 'cosdphi_Jpsi_MET/D') 
#
#dphi_mu3_MET = num.zeros(1,dtype=float)
#otree.Branch('dphi_mu3_MET', dphi_mu3_MET, 'dphi_mu3_MET/D')
#cosdphi_mu3_MET = num.zeros(1,dtype=float)
#otree.Branch('cosdphi_mu3_MET', cosdphi_mu3_MET, 'cosdphi_mu3_MET/D') 

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
    isBplusJpsiKplus = num.zeros(1,dtype=bool)
    otree.Branch('isBplusJpsiKplus', isBplusJpsiKplus, 'isBplusJpsiKplus/B')

    isBplusJpsiPiplus = num.zeros(1,dtype=bool)
    otree.Branch('isBplusJpsiPiplus', isBplusJpsiPiplus, 'isBplusJpsiPiplus/B')

    isBplusJpsiKPiPiplus = num.zeros(1,dtype=bool)
    otree.Branch('isBplusJpsiKPiPiplus', isBplusJpsiKPiPiplus, 'isBplusJpsiKPiPiplus/B')

    isBplusJpsi3Kplus = num.zeros(1,dtype=bool)
    otree.Branch('isBplusJpsi3Kplus', isBplusJpsi3Kplus, 'isBplusJpsi3Kplus/B')

    isBplusJpsiPhiKplus = num.zeros(1,dtype=bool)
    otree.Branch('isBplusJpsiPhiKplus', isBplusJpsiPhiKplus, 'isBplusJpsiPhiKplus/B')

    isBplusJpsiK0Piplus = num.zeros(1,dtype=bool)
    otree.Branch('isBplusJpsiK0Piplus', isBplusJpsiK0Piplus, 'isBplusJpsiK0Piplus/B')

    JpsiGen = num.zeros(1,dtype=bool)
    otree.Branch('JpsiGen', JpsiGen, 'JpsiGen/B')

    genBc_pt= num.zeros(1,dtype=float)
    otree.Branch('genBc_pt',genBc_pt, 'genBc_pt/D')

    #JpsiGoodMatch= num.zeros(1,dtype=bool)
    #otree.Branch('JpsiGoodMatch', JpsiGoodMatch, 'JpsiGoodMatch/B')

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
 
           


# Trigger selection. We only want particles which triggered on the Jpsi just like for the denominator

    JpsiTrig = False
    JpsiMuTrig = False
    for key, value in list(chain.HLT_BPH_isFired):
        if re.search('HLT_DoubleMu4_JpsiTrk_Displaced_v.+', key) and value:
            JpsiTrig = True
        if re.search('HLT_Dimuon0_Jpsi3p5_Muon2_v.+', key) and value:
            JpsiMuTrig = True
    
    if not JpsiTrig and JpsiMuTrig:
        continue
    if chain.JpsiMu_Jpsi_pt < 8: continue

    mu3ptcut = 4
    #mu3ptcut = 10
    #mu3ptcut = 15
    selectedmu3 = -1
    for iMu3 in xrange(chain.JpsiMu_mu3_pt.size()):
        if chain.JpsiMu_B_vprob[iMu3] < 10**(-4): continue
        #if chain.JpsiMu_B_vprob[iMu3] < 0.1: continue
        #if chain.JpsiMu_B_mass[iMu3] > 9: continue
        if chain.JpsiMu_mu1_pt[iMu3] < 4: continue
        if chain.JpsiMu_mu2_pt[iMu3] < 4: continue
        if not chain.JpsiMu_mu1_isSoft[iMu3]: continue
        if not chain.JpsiMu_mu2_isSoft[iMu3]: continue
        #if not chain.JpsiMu_mu3_isTight[iMu3]: continue
        #if not chain.JpsiMu_mu3_isSoft[iMu3]: continue
        if chain.JpsiMu_mu3_pt[iMu3] < mu3ptcut: continue
        mu3ptcut = chain.JpsiMu_mu3_pt[iMu3]
        selectedmu3 = iMu3

    if selectedmu3 == -1: continue
    evtid += 1
    #print chain.HLT_BPH_isFired[selectedmu3]
    #otree.Fill()
    pB = TLorentzVector.TLorentzVector()
    pmu1 = TLorentzVector.TLorentzVector()
    pmu2 = TLorentzVector.TLorentzVector()
    pmu3 = TLorentzVector.TLorentzVector()
    #pmet = TLorentzVector.TLorentzVector()
    pmu1.SetPtEtaPhiM(chain.JpsiMu_mu1_pt[selectedmu3], chain.JpsiMu_mu1_eta[selectedmu3], chain.JpsiMu_mu1_phi[selectedmu3], MMu)
    pmu2.SetPtEtaPhiM(chain.JpsiMu_mu2_pt[selectedmu3], chain.JpsiMu_mu2_eta[selectedmu3], chain.JpsiMu_mu2_phi[selectedmu3], MMu)
    pmu3.SetPtEtaPhiM(chain.JpsiMu_mu3_pt[selectedmu3], chain.JpsiMu_mu3_eta[selectedmu3], chain.JpsiMu_mu3_phi[selectedmu3], MMu)
    pB.SetPtEtaPhiM(chain.JpsiMu_B_pt[selectedmu3], chain.JpsiMu_B_eta[selectedmu3], chain.JpsiMu_B_phi[selectedmu3], chain.JpsiMu_B_mass[selectedmu3])
    #pmet.SetPtEtaPhiE(chain.MET_et[0], 2, chain.MET_phi[0], -chain.MET_et[0])

    pperp = pB.P() * TMath.Sin(TMath.ACos(chain.JpsiMu_B_alpha[selectedmu3]))
    JpsiMu_B_mcorr[0] = TMath.Sqrt( (chain.JpsiMu_B_mass[selectedmu3])**2 + pperp**2 ) + pperp

    dphi_mu1_mu3[0] = pmu1.DeltaPhi(pmu3)
    dphi_mu1_mu2[0] = pmu1.DeltaPhi(pmu2)
    dphi_mu2_mu3[0] = pmu2.DeltaPhi(pmu3)
    #dphi_Jpsi_MET[0] = pJpsi.DeltaPhi(pmet)
    #dphi_mu3_MET[0] = pmu3.DeltaPhi(pmet)
    dR_mu1_mu3[0] = pmu1.DeltaR(pmu3)
    dR_mu1_mu2[0] = pmu1.DeltaR(pmu2)
    dR_mu2_mu3[0] = pmu2.DeltaR(pmu3)
    cosdphi_mu1_mu3[0] = TMath.Cos(dphi_mu1_mu3[0])
    cosdphi_mu1_mu2[0] = TMath.Cos(dphi_mu1_mu2[0])
    cosdphi_mu2_mu3[0] = TMath.Cos(dphi_mu2_mu3[0])
    #cosdphi_Jpsi_MET[0] = TMath.Cos(dphi_Jpsi_MET[0])
    #cosdphi_mu3_MET[0] = TMath.Cos(dphi_mu3_MET[0])

    JpsiMu_B_reliso[0] = chain.JpsiMu_B_iso[selectedmu3]/chain.JpsiMu_B_pt[selectedmu3]
    JpsiMu_mu3_reldbiso[0] = chain.JpsiMu_mu3_dbiso[selectedmu3]/chain.JpsiMu_mu3_pt[selectedmu3]
    JpsiMu_mu2_reldbiso[0] = chain.JpsiMu_mu2_dbiso[selectedmu3]/chain.JpsiMu_mu2_pt[selectedmu3]
    JpsiMu_mu1_reldbiso[0] = chain.JpsiMu_mu1_dbiso[selectedmu3]/chain.JpsiMu_mu1_pt[selectedmu3]

#Gen Level
    if not isData and isGenLevel:
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
        def getdaughterids(gen_num, NoIntermediateParticles = True, NoNu = True):
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
        def getsisterids(gen_num, NoIntermediateParticles = True, NoNu = True):
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

        dRthresh_mu1 = 0.1
        dRthresh_mu2 = 0.1
        dRthresh_mu3 = 0.1
        genmatch_thresh_list = [dRthresh_mu1, dRthresh_mu2, dRthresh_mu3]
        # first we pick out what gen level particle our reco mu3 most likely corresponds to
        matchedparticles = multimindr(genmatch_thresh_list, [pmu1, pmu2, pmu3])
        mu3_gen_num = matchedparticles[2][0]
        mu3_sisters = getsisterids(mu3_gen_num, False)
        if mu3_gen_num == -1: continue
        JpsiGen[0] = False
        iGenJpsi = -1
        for sis in mu3_sisters:
            if JpsiGen[0]:
                continue
            if TMath.Abs(chain.genParticle_pdgId[sis]) != 443:
                continue
            else:
                #print "Jpsi found", chain.genParticle_pdgId[sis]
                JpsiGen[0] = True
                iGenJpsi = sis
        isBplusJpsiKplus[0] = False
        isBplusJpsiPiplus[0] = False
        isBplusJpsi3Kplus[0] = False
        isBplusJpsiKPiPiplus[0] = False
        isBplusJpsiPhiKplus[0] = False
        isBplusJpsiK0Piplus[0] = False
        #print "Mu3 ID", chain.genParticle_pdgId[mu3_gen_num]
        #for sis in mu3_sisters:
        #    print "Sister ID", chain.genParticle_pdgId[sis]
        if iGenJpsi == -1:
            continue
        if len(mu3_sisters) == 3: 
            sis1 = -1
            sis2 = -1
            for sis in mu3_sisters:
                if sis == iGenJpsi: continue
                elif sis1 == -1:
                    sis1 = sis
                elif sis2 == -1:
                    sis2 = sis

        if TMath.Abs(chain.genParticle_mother[mu3_gen_num][0]) == 541:
        # checking for BcJpsiMuNu - the only vis sister should be jpsi (jpsi already confirmed above) so just need to confirm only 1 vis sister and the id of the matched muon as a mu
            if len(mu3_sisters) == 1 and TMath.Abs(chain.genParticle_pdgId[mu3_gen_num]):
                genBc_pt[0] = chain.genParticle_mother_pt[mu3_gen_num][0]
        #for iGen in xrange(len(chain.genParticle_pt)):
        #    print "Gen Particle pT: ", chain.genParticle_pt[iGen]
        if TMath.Abs(chain.genParticle_mother[mu3_gen_num][0]) == 521:
            if TMath.Abs(chain.genParticle_pdgId[mu3_gen_num]) == 321:
                if len(mu3_sisters) == 1:
                    #print "sister id (should be a Jpsi)", chain.genParticle_pdgId[mu3_sisters[0]]
                    isBplusJpsiKplus[0] = True
                elif len(mu3_sisters) == 2:
                    for sis in mu3_sisters:
                        if sis == iGenJpsi:
                            #print "sister id (should be a Jpsi)", chain.genParticle_pdgId[sis]
                            continue
                        if abs(chain.genParticle_pdgId[sis]) == 333:
                            isBplusJpsiPhiKplus[0] = True
                elif len(mu3_sisters) == 3: 
                    if abs(chain.genParticle_pdgId[sis1]) == 321 and abs(chain.genParticle_pdgId[sis2]) == 321: 
                        isBplusJpsi3Kplus[0] = True
                    elif abs(chain.genParticle_pdgId[sis1]) == 321 and abs(chain.genParticle_pdgId[sis1]) == 211:
                        isBplusJpsiKPiPiplus[0] = True
                    elif abs(chain.genParticle_pdgId[sis2]) == 321 and abs(chain.genParticle_pdgId[  sis1]) == 211:
                        isBplusJpsiKPiPiplus[0] = True
            elif TMath.Abs(chain.genParticle_pdgId[mu3_gen_num]) == 211:
                if len(mu3_sisters) == 1:
                    #print "sister id (should be a Jpsi)", chain.genParticle_pdgId[mu3_sisters[0]]
                    isBplusJpsiPiplus[0] = True
                elif len(mu3_sisters) == 2:
                    for sis in mu3_sisters:
                        if sis == iGenJpsi: continue
                        if TMath.Abs(chain.genParticle_pdgId[sis]) == 311:
                            isBplusJpsiK0Piplus[0] = True
                elif len(mu3_sisters) == 3:
                    if abs(chain.genParticle_pdgId[sis1]) == 321 and abs(chain.genParticle_pdgId[sis1]) == 211:
                        isBplusJpsiKPiPiplus[0] = True
                    elif abs(chain.genParticle_pdgId[sis2]) == 321 and abs(chain.genParticle_pdgId[  sis1]) == 211:
                        isBplusJpsiKPiPiplus[0] = True

        #if isBplusJpsiKplus[0]: print "Tag Successful!, It's a:", "B+->JpsiK+"
        #if isBplusJpsiPiplus[0]: print "Tag Successful!, It's a:", "B+->JpsiPi+"
        #if isBplusJpsi3Kplus[0]: print "Tag Successful!, It's a:", "B+->Jpsi3K+"
        #if isBplusJpsiKPiPiplus[0]: print "Tag Successful!, It's a:", "B+->JpsiK+2Pi+"
        #if isBplusJpsiPhiKplus[0]: print "Tag Successful!, It's a:", "B+->JpsiPhiK+"
        #if isBplusJpsiK0Piplus[0]: print "Tag Successful!, It's a:", "B+->JpsiK0Pi+"
        #print "Tagging complete"
    if not isData and isGenLevel:
        for var in gen_outvars:
            tmpvec = []
            for iGen in xrange(len(chain.genParticle_pt)):
                tmpvec += [getattr(chain,var)[iGen]]
            getattr(chain,var).clear()
            for iGen in xrange(len(tmpvec)):
                getattr(chain,var).push_back(tmpvec[iGen])
    for var in outvars:
        if "_Jpsi_" in var:
            tmp = getattr(chain,var)[0]
            getattr(chain,var).clear()
            getattr(chain,var).push_back(tmp)
        else:
            tmp = getattr(chain,var)[selectedmu3]
            getattr(chain,var).clear()
            getattr(chain,var).push_back(tmp)
    #for var in met_outvars:
    #    tmp = getattr(chain,var)[0]
    #    getattr(chain,var).clear()
    #    getattr(chain,var).push_back(tmp)
    cuthist.Fill(1)
    if not isData:
        cuthist.Fill(2, weight_evt)
        #for var in evt_outvars:
        #    tmp = getattr(chain,var)[selectedmu3]
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
    if nevts !=0:
        print "Efficiency: ", float(evtid)/nevts
