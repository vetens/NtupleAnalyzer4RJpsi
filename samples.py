import collections
from ROOT import TFile

lumi = 6.894770971

# when adding new samples, add an entry for its TFile, an entry for its dictionary, and an entry for its colors, styles, and widths as with the other samples

#Colors, styles, and widths:
colours = {"dataC":1, "bg_BJpsiX_MuMu":2, "bg_BcChic1MuNu":3, "bg_BcJpsiTauNu":4, "bg_BcPsi2STauNu":5, "bg_BJpsiX_MuMu_J": 6, "bg_JpsiX_MuMu_J":7, "bg_BcPsi2SMuNu":8, "signal_BcJpsiMuNu":9}
styles ={"dataC":1, "bg_BJpsiX_MuMu":2, "bg_BcChic1MuNu":4, "bg_BcJpsiTauNu":3, "bg_BcPsi2STauNu":5, "bg_BJpsiX_MuMu_J": 7, "bg_JpsiX_MuMu_J":8, "bg_BcPsi2SMuNu":10, "signal_BcJpsiMuNu":1}
widths = {"dataC":3, "bg_BJpsiX_MuMu":3, "bg_BcChic1MuNu":3, "bg_BcJpsiTauNu":3, "bg_BcPsi2STauNu":3, "bg_BJpsiX_MuMu_J": 3, "bg_JpsiX_MuMu_J":3, "bg_BcPsi2SMuNu":3, "signal_BcJpsiMuNu":3}

##TFiles

datfileC = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v8/Charmonium/Charmonium_Run2018A-17Sep2018-v1/Btrimu.root')

bg_JpsiX_MuMu_J = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v8/OniaAndX_ToMuMu_MuFilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/OniaAndX_ToMuMu_MuFilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/Btrimu.root')

signal_BcJpsiMuNu = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v8/BcToJPsiMuNu_TuneCUEP8M1_13TeV-bcvegpy2-pythia8-evtgen/BcToJPsiMuNu_TuneCUEP8M1_13TeV-bcvegpy2-pythia8-evtgen/Btrimu.root')


#datfileC = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v6/Charmonium/Charmonium_Run2018C-17Sep2018-v1/Btrimu.root')
##bg_BcChic1MuNu = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v5_multipleCand/BcChic1MuNu_211019/BcChic1MuNu_211019/Btrimu.root')
##bg_BcJpsiTauNu = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v5_multipleCand/BcJpsiTauNu_020519/BcJpsiTauNu_020519/Btrimu.root')
##bg_BcPsi2STauNu = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v5_multipleCand/BcPsi2STauNu_051019/BcPsi2STauNu_051019/Btrimu.root')
##bg_BJpsiX_MuMu_J = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v5_multipleCand/BJpsiX_MuMu_J_211119/BJpsiX_MuMu_J_211119/Btrimu.root')
#bg_JpsiX_MuMu_J = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v6/OniaAndX_ToMuMu_MuFilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/OniaAndX_ToMuMu_MuFilter_SoftQCDnonD_TuneCP5_13TeV-pythia8-evtgen/Btrimu.root')
##bg_BcPsi2SMuNu = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v5_multipleCand/BcPsi2SMuNu_091019/BcPsi2SMuNu_091019/Btrimu.root')
##bg_BJpsiX_MuMu = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v5_multipleCand/BJpsiX_MuMu_031019/BJpsiX_MuMu_031019/Btrimu.root')
#signal_BcJpsiMuNu = TFile('/eos/home-w/wvetens/SkimmedNTuples/Ntuple_BPH_v6/BcToJPsiMuNu_TuneCUEP8M1_13TeV-bcvegpy2-pythia8-evtgen/BcToJPsiMuNu_TuneCUEP8M1_13TeV-bcvegpy2-pythia8-evtgen/Btrimu.root')

sampledict = collections.OrderedDict() 

#Dictionary:

# New sigma calculation method for signal: http://cms.cern.ch/iCMS/jsp/openfile.jsp?tp=draft&files=AN2019_046_v6.pdf
# sigma=Nproduced/L = Nobs/(e_reco L), all values taken from above source
# Using this, we get 90 \pm 10 pb for our cross section for signal 

sampledict['dataC'] = {'file':datfileC, 'title':'Data (Charmonium Run2018C)', 'digits':0, 'crossxn': 1, 'crossxnerr': 0}
#sampledict['bg_BJpsiX_MuMu'] = {'file':bg_BJpsiX_MuMu,  'title':'B->J/#psi + X', 'digits':1, 'crossxn': 5.588*10**8, 'crossxnerr': 3.951*10**8}
#sampledict['bg_BcChic1MuNu'] = {'file':bg_BcChic1MuNu,  'title':'B_{c}->#chi_{c}^{1} + #mu + #nu', 'digits':1, 'crossxn': 1, 'crossxnerr': 0}
#sampledict['bg_BcJpsiTauNu'] = {'file':bg_BcJpsiTauNu,  'title':'B_{c}->J/#psi + #tau + #nu', 'digits':1, 'crossxn': 90, 'crossxnerr': 10}
#sampledict['bg_BcPsi2STauNu'] = {'file':bg_BcPsi2STauNu,  'title':'B_{c}->#psi(2S) + #tau + #nu', 'digits':1, 'crossxn': 1, 'crossxnerr': 0}
#sampledict['bg_BJpsiX_MuMu_J'] = {'file':bg_BJpsiX_MuMu_J,  'title':'B->J/#psi, 'digits':1, 'crossxn': 1.080 * 10 ** 9, 'crossxnerr': 1.730 *10**8}
sampledict['bg_JpsiX_MuMu_J'] = {'file':bg_JpsiX_MuMu_J,  'title':'pp->J/#psi+X', 'digits':1, 'crossxn': 1.384*10**9, 'crossxnerr': 1.957*10**8}
#sampledict['bg_BcPsi2SMuNu'] = {'file':bg_BcPsi2SMuNu,  'title':'B_{c}->#psi(2S) + #mu + #nu', 'digits':1, 'crossxn': 2.612*10**10, 'crossxnerr': 2.347*10**5}
sampledict['signal_BcJpsiMuNu'] = {'file':signal_BcJpsiMuNu, 'title':'B_{c}->J/#psi + #mu + #nu', 'digits':1, 'crossxn': 90, 'crossxnerr': 10}
