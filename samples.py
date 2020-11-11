import collections
from ROOT import TFile

# luminosity in inverse fb
lumi = 59832.475339

# when adding new samples, add an entry for its TFile, an entry for its dictionary, and an entry for its colors, styles, and widths as with the other samples

#Colors, styles, and widths:
#colours = {"dataC":1, "bg_BOniaAndX_MuMu":2, "bg_BcChic1MuNu":3, "bg_BcJpsiTauNu":4, "bg_BcPsi2STauNu":5, "bg_BOniaAndX_MuMu_J": 6, "bg_OniaAndX_MuMu_J":7, "bg_BcPsi2SMuNu":8, "signal_BcJpsiMuNu":9}
#styles ={"dataC":1, "bg_BOniaAndX_MuMu":2, "bg_BcChic1MuNu":4, "bg_BcJpsiTauNu":3, "bg_BcPsi2STauNu":5, "bg_BOniaAndX_MuMu_J": 7, "bg_OniaAndX_MuMu_J":8, "bg_BcPsi2SMuNu":10, "signal_BcJpsiMuNu":1}
#widths = {"dataC":3, "bg_BOniaAndX_MuMu":3, "bg_BcChic1MuNu":3, "bg_BcJpsiTauNu":3, "bg_BcPsi2STauNu":3, "bg_BOniaAndX_MuMu_J": 3, "bg_OniaAndX_MuMu_J":3, "bg_BcPsi2SMuNu":3, "signal_BcJpsiMuNu":3}

colours = {"DatFull":1, "dataA":1, "dataB":1, "dataC":1, "dataD":1, "bg_BcJpsiTauNu":4, "bg_BcPsi2STauNu":5, "bg_OniaAndX_MuMu_J":2, "bg_BcPsi2SMuNu":8, "signal_BcJpsiMuNu":1}
styles ={"DatFull":1, "dataA":1, "dataB":1, "dataC":1, "dataD":1, "bg_BcJpsiTauNu":3, "bg_BcPsi2STauNu":5, "bg_OniaAndX_MuMu_J":2, "bg_BcPsi2SMuNu":10, "signal_BcJpsiMuNu":1}
widths = {"DatFull":3, "dataA":3, "dataB":3, "dataC":3, "dataD":3, "bg_BcJpsiTauNu":3, "bg_BcPsi2STauNu":3, "bg_OniaAndX_MuMu_J":3, "bg_BcPsi2SMuNu":3, "signal_BcJpsiMuNu":3}

##TFiles

#datfileC = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v8/Charmonium/Charmonium_Run2018C-17Sep2018-v1/Btrimu.root')
#
#bg_OniaAndX_MuMu_J = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v8/OniaAndX_ToMuMu_MuFilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/OniaAndX_ToMuMu_MuFilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/Btrimu.root')
#
#signal_BcJpsiMuNu = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v8/BcToJPsiMuNu_TuneCUEP8M1_13TeV-bcvegpy2-pythia8-evtgen/BcToJPsiMuNu_TuneCUEP8M1_13TeV-bcvegpy2-pythia8-evtgen/Btrimu.root')

#datfileA = TFile('/eos/home-w/wvetens/SkimmedNTuples_V1/Charmonium_2020-06-28-110131_20200628110130_Data_2018UL_muon_channel/Charmonium/Charmonium_Run2018A-12Nov2019_UL2018_rsb-v1_20200628110130_Data_2018UL_muon_channel/Btrimu.root')
#
#datfileB = TFile('/eos/home-w/wvetens/SkimmedNTuples_V1/Charmonium_2020-06-28-110131_20200628110130_Data_2018UL_muon_channel/Charmonium/Charmonium_Run2018B-12Nov2019_UL2018-v1_20200628110130_Data_2018UL_muon_channel/Btrimu.root')
#
#datfileC = TFile('/eos/home-w/wvetens/SkimmedNTuples_V1/Charmonium_2020-06-28-110131_20200628110130_Data_2018UL_muon_channel/Charmonium/Charmonium_Run2018C-12Nov2019_UL2018-v1_20200628110130_Data_2018UL_muon_channel/Btrimu.root')
#
#datfileD = TFile('/eos/home-w/wvetens/SkimmedNTuples_V1/Charmonium_2020-06-28-110131_20200628110130_Data_2018UL_muon_channel/Charmonium/Charmonium_Run2018D-12Nov2019_UL2018-v1_20200628110130_Data_2018UL_muon_channel/Btrimu.root')

#DataFull= TFile('/eos/home-w/wvetens/SkimmedNTuples_V2/Charmonium_All.root')
#
#bg_OniaAndX_MuMu_J = TFile('/eos/home-w/wvetens/SkimmedNTuples_V2/OniaAndX_ToMuMu_MuFilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen_2020-06-29-135159_20200629135158_BcJpsiX_den_2018/OniaAndX_ToMuMu_MuFilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/OniaAndX_ToMuMu_MuFilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen_20200629135158_BcJpsiX_den_2018/Btrimu.root')
#
#bg_BcJpsiTauNu = TFile('/eos/home-w/wvetens/SkimmedNTuples_V2/BcToJPsiTauNu_TuneCP5_13TeV-bcvegpy2-pythia8-evtgen_2020-07-02-130640_20200702130640_BcJpsiTaulep_MC_2018/BcToJPsiTauNu_TuneCP5_13TeV-bcvegpy2-pythia8-evtgen/BcToJPsiTauNu_TuneCP5_13TeV-bcvegpy2-pythia8-evtgen_20200702130640_BcJpsiTaulep_MC_2018/Btrimu.root')

signal_BcJpsiMuNu = TFile('~/eos_storage/10-26-2020-GenBcPt/BcToJPsiMuNu_denominator_mc_2016/BtrimuFinal.root')

#signal_BcJpsiMuNu_old = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v5_multipleCand/BcJpsiMuNu_020519/BcJpsiMuNu_020519/Btrimu.root')
#
#bg_OniaAndX_MuMu_J_old = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v5_multipleCand/OniaAndX_MuMu_J_211119/OniaAndX_MuMu_J_211119/Btrimu.root')

#datfileC = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v6/Charmonium/Charmonium_Run2018C-17Sep2018-v1/Btrimu.root')
##bg_BcChic1MuNu = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v5_multipleCand/BcChic1MuNu_211019/BcChic1MuNu_211019/Btrimu.root')
##bg_BcJpsiTauNu = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v5_multipleCand/BcJpsiTauNu_020519/BcJpsiTauNu_020519/Btrimu.root')
##bg_BcPsi2STauNu = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v5_multipleCand/BcPsi2STauNu_051019/BcPsi2STauNu_051019/Btrimu.root')
##bg_BOniaAndX_MuMu_J = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v5_multipleCand/BOniaAndX_MuMu_J_211119/BOniaAndX_MuMu_J_211119/Btrimu.root')
#bg_OniaAndX_MuMu_J = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v6/OniaAndX_ToMuMu_MuFilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/OniaAndX_ToMuMu_MuFilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/Btrimu.root')
##bg_BcPsi2SMuNu = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v5_multipleCand/BcPsi2SMuNu_091019/BcPsi2SMuNu_091019/Btrimu.root')
##bg_BOniaAndX_MuMu = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v5_multipleCand/BOniaAndX_MuMu_031019/BOniaAndX_MuMu_031019/Btrimu.root')
#signal_BcJpsiMuNu = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v6/BcToJPsiMuNu_TuneCUEP8M1_13TeV-bcvegpy2-pythia8-evtgen/BcToJPsiMuNu_TuneCUEP8M1_13TeV-bcvegpy2-pythia8-evtgen/Btrimu.root')

sampledict = collections.OrderedDict() 

#Dictionary:

# New sigma calculation method for signal: http://cms.cern.ch/iCMS/jsp/openfile.jsp?tp=draft&files=AN2019_046_v15.pdf
# sigma=Nproduced/L = Nobs/(e_reco L), all values taken from above source
# sigma(Bc+->Jpsi(->mumu) + pi) = 7629/(1f3 /fb * 0.01313) From this analysis note
# sigma(Bc+-> J/psi+l+nu) = sigma(Bc+->Jpsi(->mumu)+pi) * Br( Bc->J/psi+l+nu )/ Br(Bc->Jpsi(->mumu)+pi)
# sigma(Bc+-> J/psi+l+nu) = sigma(Bc+) * 1/(4.69*10**(-2) , from PG 5 of http://pdg.lbl.gov/2020/listings/rpp2020-list-Bc-plus-minus.pdf
# sigma(Bc+-> J/psi+l+nu) = 8.1623 * 10 ** (4) fb

#sampledict['dataA'] = {'file':datfileA, 'title':'Data (Charmonium Run2018)', 'digits':0, 'crossxn': 1, 'crossxnerr': 0}
#sampledict['dataB'] = {'file':datfileB, 'title':'Data (Charmonium Run2018)', 'digits':0, 'crossxn': 1, 'crossxnerr': 0}
#sampledict['dataC'] = {'file':datfileC, 'title':'Data (Charmonium Run2018)', 'digits':0, 'crossxn': 1, 'crossxnerr': 0}
#sampledict['dataD'] = {'file':datfileD, 'title':'Data (Charmonium Run2018)', 'digits':0, 'crossxn': 1, 'crossxnerr': 0}
#sampledict['DatFull'] = {'file':DataFull, 'title':'Data (Charmonium Run2018)', 'digits':0, 'crossxn': 1, 'crossxnerr': 0}
##sampledict['bg_BcChic1MuNu'] = {'file':bg_BcChic1MuNu,  'title':'B_{c}->#chi_{c}^{1} + #mu + #nu', 'digits':1, 'crossxn': 1, 'crossxnerr': 0}
#sampledict['bg_BcJpsiTauNu'] = {'file':bg_BcJpsiTauNu,  'title':'B_{c}->J/#psi + #tau + #nu', 'digits':3, 'crossxn': 8.2 * 10 ** 1, 'crossxnerr': 0}
##sampledict['bg_BcPsi2STauNu'] = {'file':bg_BcPsi2STauNu,  'title':'B_{c}->#psi(2S) + #tau + #nu', 'digits':1, 'crossxn': 1, 'crossxnerr': 0}
#sampledict['bg_OniaAndX_MuMu_J'] = {'file':bg_OniaAndX_MuMu_J,  'title':'Onia and X BG', 'digits':3, 'crossxn': 1.384 * 10**6, 'crossxnerr': 1.957 * 10**5}
#sampledict['bg_OniaAndX_MuMu_J_old'] = {'file':bg_OniaAndX_MuMu_J_old,  'title':'old pp->J/#psi+X', 'digits':1, 'crossxn': 1.384*10**9, 'crossxnerr': 1.957*10**8}
#sampledict['bg_BcPsi2SMuNu'] = {'file':bg_BcPsi2SMuNu,  'title':'B_{c}->#psi(2S) + #mu + #nu', 'digits':1, 'crossxn': 2.612*10**10, 'crossxnerr': 2.347*10**5}
sampledict['signal_BcJpsiMuNu'] = {'file':signal_BcJpsiMuNu, 'title':'B_{c}->J/#psi + #mu + #nu', 'digits':3, 'crossxn': 8.2 * 10 ** 1, 'crossxnerr': 0}
#sampledict['signal_BcJpsiMuNu_old'] = {'file':signal_BcJpsiMuNu_old, 'title':'Old B_{c}->J/#psi + #mu + #nu', 'digits':1, 'crossxn': 90, 'crossxnerr': 10}
