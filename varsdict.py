import collections
from ROOT import TMath

# the 'loglowerlimit' parameter is only taken into account for variables which will be plotted on a Log scale, i.e. when 'isLog' is True.
# When the graph is shown in Log-scale, 'loglowerlimit' is the negative of the minimum power of ten shown, i.e. -4.5 corresponds to 
# 10^(-4.5)


vardict = collections.OrderedDict()

vardict['JpsiMu_B_mcorr'] = {'xtitle': 'm_{corr} [Gev]', 'nbins': 60, 'xmin': 3.5, 'xmax': 14, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_B_mass'] = {'xtitle': 'm(#mu#mu#mu) inv mass [Gev]', 'nbins': 60, 'xmin': 3, 'xmax': 9, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_Jpsi_unfit_mass'] = {'xtitle': 'Unfit J/#psi mass [Gev]', 'nbins': 60, 'xmin': 2, 'xmax': 4, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['MET_et'] = {'xtitle': 'MET_et (GeV)', 'nbins': 60, 'xmin': 0, 'xmax': 10, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['MET_sumEt'] = {'xtitle': 'MET_sumEt (GeV)', 'nbins': 60, 'xmin': 0, 'xmax': 3500, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 3} 
vardict['MET_significance'] = {'xtitle': 'MET_significance', 'nbins': 60, 'xmin': 0, 'xmax': 30, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 3} 
vardict['JpsiMu_Jpsi_lip'] = {'xtitle': 'J/#psi Longitudinal Impact Parameter', 'nbins': 60, 'xmin': -2, 'xmax': 2, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['JpsiMu_Jpsi_pvip'] = {'xtitle': 'J/#psi Impact Param. to the Primary Vertex', 'nbins': 60, 'xmin': 0, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['JpsiMu_Jpsi_pvips'] = {'xtitle': 'J/#psi PVIP significance', 'nbins': 60, 'xmin': 0, 'xmax': 7, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['JpsiMu_Jpsi_lips'] = {'xtitle': 'J/#psi LIP significance', 'nbins': 60, 'xmin': -5, 'xmax': 5, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['JpsiMu_Jpsi_fl3d'] = {'xtitle': 'J/#psi Flight Length 3D', 'nbins': 60, 'xmin': 0, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['JpsiMu_Jpsi_pt'] = {'xtitle': 'p_{T} of the J/#psi (GeV)', 'nbins': 60, 'xmin': 8, 'xmax': 14, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3.7} 
vardict['JpsiMu_Jpsi_eta'] = {'xtitle': '#eta of the J/#psi', 'nbins': 60, 'xmin': -2.4, 'xmax': 2.4, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3.7} 
vardict['JpsiMu_Jpsi_phi'] = {'xtitle': '#phi of the J/#psi', 'nbins': 60, 'xmin': -3.15, 'xmax': 3.15, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3.7} 
vardict['JpsiMu_Jpsi_fls3d'] = {'xtitle': 'J/#psi FL3D Significance', 'nbins': 60, 'xmin': 0, 'xmax': 30, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 3.5} 
vardict['JpsiMu_B_pt'] = {'xtitle': 'p_{T} of the trimuon (GeV)', 'nbins': 60, 'xmin': 8, 'xmax': 30, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3.7} 
vardict['JpsiMu_B_eta'] = {'xtitle': '#eta of the trimuon', 'nbins': 60, 'xmin': -2.4, 'xmax': 2.4, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3.7} 
vardict['JpsiMu_B_phi'] = {'xtitle': '#phi of the trimuon', 'nbins': 60, 'xmin': -3.15, 'xmax': 3.15, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3.7} 
vardict['JpsiMu_mu3_pt'] = {'xtitle': 'p_{T} of the #mu_{3} (GeV)', 'nbins': 60, 'xmin': 2, 'xmax': 20, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_mu3_eta'] = {'xtitle': '#eta of the #mu_{3} (GeV)', 'nbins': 60, 'xmin': -2.4, 'xmax': 2.4, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_mu2_pt'] = {'xtitle': 'p_{T} of the #mu_{2} (GeV)', 'nbins': 60, 'xmin': 4, 'xmax': 11, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_mu2_eta'] = {'xtitle': '#eta of the #mu_{2} (GeV)', 'nbins': 60, 'xmin': -2.4, 'xmax': 2.4, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_mu1_pt'] = {'xtitle': 'p_{T} of the #mu_{1} (GeV)', 'nbins': 60, 'xmin': 4, 'xmax': 11, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_mu1_eta'] = {'xtitle': '#eta of the #mu_{1} (GeV)', 'nbins': 60, 'xmin': -2.4, 'xmax': 2.4, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_B_fl3d'] = {'xtitle': 'B_{c} Flight Length 3D', 'nbins': 60, 'xmin': 0, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['JpsiMu_B_fls3d'] = {'xtitle': 'B_{c} FL3D Significance', 'nbins': 60, 'xmin': 0, 'xmax': 80, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 3.5} 
vardict['JpsiMu_B_iso_ntracks'] = {'xtitle': '# of PF tracks used for B_{c} iso', 'nbins': 15, 'xmin': 0, 'xmax': 15, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 2} 
vardict['JpsiMu_B_iso_mindoca'] = {'xtitle': 'Min DOCA of tracks in B_{c} iso', 'nbins': 60, 'xmin': 0, 'xmax': 0.15, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 3} 
vardict['JpsiMu_B_lip'] = {'xtitle': 'B_{c} Longitudinal Impact Parameter', 'nbins': 60, 'xmin': 0, 'xmax': 0.02, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['JpsiMu_B_lips'] = {'xtitle': 'B_{c} LIP Significance', 'nbins': 60, 'xmin': 0, 'xmax': 7, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['JpsiMu_B_pvip'] = {'xtitle': 'B_{c} Impact Parameter to the P.V.', 'nbins': 60, 'xmin': 0, 'xmax': 0.02, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['JpsiMu_B_pvips'] = {'xtitle': 'B_{c} PVIP significance', 'nbins': 60, 'xmin': 0, 'xmax': 7, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['JpsiMu_B_maxdoca'] = {'xtitle': 'B_{c} max doca', 'nbins': 60, 'xmin': 0, 'xmax': 0.05, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['JpsiMu_B_mindoca'] = {'xtitle': 'B_{c} min doca', 'nbins': 60, 'xmin': 0, 'xmax': 0.015, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['JpsiMu_Jpsi_maxdoca'] = {'xtitle': 'J/#psi max doca', 'nbins': 60, 'xmin': 0, 'xmax': 0.05, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 6} 
vardict['JpsiMu_Jpsi_mindoca'] = {'xtitle': 'J/#psi min doca', 'nbins': 60, 'xmin': 0, 'xmax': 0.015, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 3.5} 
vardict['JpsiMu_mu3_doca2mu1'] = {'xtitle': 'DOCA between #mu_{3} and #mu_{1}', 'nbins': 60, 'xmin': 0, 'xmax': 0.05, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['JpsiMu_mu3_doca2mu2'] = {'xtitle': 'DOCA between #mu_{3} and #mu_{2}', 'nbins': 60, 'xmin': 0, 'xmax': 0.05, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['cosdphi_mu1_mu3'] = {'xtitle': 'Cos(#Delta#phi_{#mu_{1},#mu_{3}})', 'nbins': 60, 'xmin': 0.5, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['cosdphi_mu2_mu3'] = {'xtitle': 'Cos(#Delta#phi_{#mu_{2},#mu_{3}})', 'nbins': 60, 'xmin': 0.5, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['cosdphi_mu1_mu2'] = {'xtitle': 'Cos(#Delta#phi_{#mu_{1},#mu_{2}})', 'nbins': 60, 'xmin': 0.6, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['cosdphi_Jpsi_mu3'] = {'xtitle': 'Cos(#Delta#phi_{J/#psi,#mu_{3}})', 'nbins': 60, 'xmin': 0.5, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
vardict['cosdphi_Jpsi_MET'] = {'xtitle': 'Cos(#Delta#phi_{J/#psi,MET})', 'nbins': 60, 'xmin': -1, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 2.6} 
vardict['cosdphi_mu3_MET'] = {'xtitle': 'Cos(#Delta#phi_{#mu_{3},MET})', 'nbins': 61, 'xmin': -1, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 2.4} 
#vardict['dphi_mu1_mu3'] = {'xtitle': '#Delta#phi_{#mu_{1},#mu_{3}}', 'nbins': 60, 'xmin': -TMath.Pi(), 'xmax': TMath.Pi(), 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
#vardict['dphi_mu2_mu3'] = {'xtitle': '#Delta#phi_{#mu_{2},#mu_{3}}', 'nbins': 60, 'xmin': -TMath.Pi(), 'xmax': TMath.Pi(), 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
#vardict['dphi_mu1_mu2'] = {'xtitle': '#Delta#phi_{#mu_{1},#mu_{2}}', 'nbins': 60, 'xmin': -TMath.Pi(), 'xmax': 0.8, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
#vardict['dphi_Jpsi_mu3'] = {'xtitle': '#Delta#phi_{J/#psi,#mu_{3}}', 'nbins': 60, 'xmin': -TMath.Pi(), 'xmax': TMath.Pi(), 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
#vardict['dphi_Jpsi_MET'] = {'xtitle': '#Delta#phi_{J/#psi,MET}', 'nbins': 60, 'xmin': -TMath.Pi(), 'xmax': TMath.Pi(), 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
#vardict['dphi_mu3_MET'] = {'xtitle': '#Delta#phi_{#mu_{3},MET}', 'nbins': 61, 'xmin': 0, 'xmax': TMath.Pi(), 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 4} 
#vardict['dR_Jpsi_mu3'] = {'xtitle': '#Delta R_{J/#psi,#mu_{3}}', 'nbins': 60, 'xmin': 0, 'xmax': 0.8, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 1} 
#vardict['dR_mu1_mu3'] = {'xtitle': '#Delta R_{#mu_{1},#mu_{3}}', 'nbins': 60, 'xmin': 0, 'xmax': 0.8, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 1} 
#vardict['dR_mu2_mu3'] = {'xtitle': '#Delta R_{#mu_{2},#mu_{3}}', 'nbins': 60, 'xmin': 0, 'xmax': 0.8, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 1} 
#vardict['dR_mu1_mu2'] = {'xtitle': '#Delta R_{#mu_{1},#mu_{2}}', 'nbins': 60, 'xmin': 0, 'xmax': 0.8, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 1} 
vardict['JpsiMu_mu3_reliso'] = {'xtitle': 'Relative iso of the #mu_{3}', 'nbins': 60, 'xmin': 0, 'xmax': 2, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_mu3_iso'] = {'xtitle': 'Absolute iso of the #mu_{3}', 'nbins': 60, 'xmin': 0.5, 'xmax': 6, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_mu2_reliso'] = {'xtitle': 'Relative iso of the #mu_{2}', 'nbins': 60, 'xmin': 0, 'xmax': 2, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_mu2_iso'] = {'xtitle': 'Absolute iso of the #mu_{2}', 'nbins': 60, 'xmin': 0.5, 'xmax': 6, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_mu1_reliso'] = {'xtitle': 'Relative iso of the #mu_{1}', 'nbins': 60, 'xmin': 0, 'xmax': 2, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_mu1_iso'] = {'xtitle': 'Absolute iso of the #mu_{1}', 'nbins': 60, 'xmin': 0.5, 'xmax': 6, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_B_reliso'] = {'xtitle': 'Relative iso of the B_{c}', 'nbins': 60, 'xmin': 0, 'xmax': 2, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_B_iso'] = {'xtitle': 'Absolute iso of the B_{c}', 'nbins': 60, 'xmin': 0.5, 'xmax': 6, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_mu3_reldbiso'] = {'xtitle': 'Relative PF iso of the #mu_{3}', 'nbins': 60, 'xmin': 0, 'xmax': 2, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_mu3_dbiso'] = {'xtitle': 'PF iso of the #mu_{3}', 'nbins': 60, 'xmin': 0, 'xmax': 8, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_mu2_reldbiso'] = {'xtitle': 'Relative PF iso of the #mu_{2}', 'nbins': 60, 'xmin': 0, 'xmax': 2, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_mu2_dbiso'] = {'xtitle': 'PF iso of the #mu_{2}', 'nbins': 60, 'xmin': 0, 'xmax': 8, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_mu1_reldbiso'] = {'xtitle': 'Relative PF iso of the #mu_{1}', 'nbins': 60, 'xmin': 0, 'xmax': 2, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_mu1_dbiso'] = {'xtitle': 'PF iso of the #mu_{1}', 'nbins': 60, 'xmin': 0, 'xmax': 8, 'ytitle': '', 'isLog': False, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': -3} 
vardict['JpsiMu_Jpsi_vprob'] = {'xtitle': 'J/#psi Vertex Probability', 'nbins': 60, 'xmin': 0, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 2} 
vardict['JpsiMu_B_vprob'] = {'xtitle': 'Trimuon Vertex Probability', 'nbins': 60, 'xmin': 0, 'xmax': 0.3, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 3} 
vardict['JpsiMu_Jpsi_alpha'] = {'xtitle': 'J/#psi Cos(#alpha)', 'nbins': 60, 'xmin': -1, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 3.7} 
vardict['JpsiMu_B_alpha'] = {'xtitle': 'B_{c} Cos(#alpha)', 'nbins': 60, 'xmin': -1, 'xmax': 1, 'ytitle': '', 'isLog': True, 'isRatio': False, 'isLegended': True, 'HasStackPlot': False, 'loglowerlimit': 2.9} 

# These are variables for which to optimize cutflow


to_optimize = collections.OrderedDict()

to_optimize['JpsiMu_mu3_doca2mu2'] = {'var': vardict['JpsiMu_mu3_doca2mu2'], 'isgl': '<', 'granularity': 100.0, 'histscale': 0.14, 'xmax': 0.05, 'xmin': 0}
to_optimize['JpsiMu_mu3_doca2mu1'] = {'var': vardict['JpsiMu_mu3_doca2mu1'], 'isgl': '<', 'granularity': 100.0, 'histscale': 0.14, 'xmax': 0.05, 'xmin': 0}
to_optimize['JpsiMu_B_fls3d'] = {'var': vardict['JpsiMu_B_fls3d'], 'isgl': '<', 'granularity': 100.0, 'histscale': 0.13, 'xmax': 30, 'xmin': 0}
to_optimize['JpsiMu_Jpsi_fls3d'] = {'var': vardict['JpsiMu_Jpsi_fls3d'], 'isgl': '<', 'granularity': 100.0, 'histscale': 0.13, 'xmax': 30, 'xmin': 0}
to_optimize['JpsiMu_mu3_reliso'] = {'var': vardict['JpsiMu_mu3_reliso'], 'isgl': '<', 'granularity': 100.0, 'histscale': 0.1, 'xmax': 2, 'xmin': 0.0}
to_optimize['JpsiMu_mu3_reldbiso'] = {'var': vardict['JpsiMu_mu3_reldbiso'], 'isgl': '<', 'granularity': 100.0, 'histscale': 0.1, 'xmax': 2, 'xmin': 0.0}
to_optimize['JpsiMu_B_reliso'] = {'var': vardict['JpsiMu_B_reliso'], 'isgl': '<', 'granularity': 100.0, 'histscale': 0.1, 'xmax': 2, 'xmin': 0.0}
to_optimize['JpsiMu_B_alpha'] = {'var': vardict['JpsiMu_B_alpha'], 'isgl': '>', 'granularity': 100.0, 'histscale': 0.05, 'xmax': 1, 'xmin': 0.8}
to_optimize['JpsiMu_B_pvips'] = {'var': vardict['JpsiMu_B_pvips'], 'isgl': '<', 'granularity': 100.0, 'histscale': 0.2, 'xmax': 7, 'xmin': 0}
to_optimize['JpsiMu_B_lips'] = {'var': vardict['JpsiMu_B_lips'], 'isgl': '<', 'granularity': 100.0, 'histscale': 0.13, 'xmax': 7, 'xmin': 0}
to_optimize['JpsiMu_B_maxdoca'] = {'var': vardict['JpsiMu_B_maxdoca'], 'isgl': '<', 'granularity': 100.0, 'histscale': 0.07, 'xmax': 0.05, 'xmin': 0}
to_optimize['JpsiMu_B_mindoca'] = {'var': vardict['JpsiMu_B_mindoca'], 'isgl': '<', 'granularity': 100.0, 'histscale': 0.13, 'xmax': 0.015, 'xmin': 0}
to_optimize['JpsiMu_B_iso_mindoca'] = {'var': vardict['JpsiMu_B_iso_mindoca'], 'isgl': '<', 'granularity': 100.0, 'histscale': 0.11, 'xmax': 0.2, 'xmin': 0}
to_optimize['JpsiMu_B_vprob'] = {'var': vardict['JpsiMu_B_vprob'], 'isgl': '>', 'granularity': 100.0, 'histscale': 0.2, 'xmax': 0.3, 'xmin': 0}
to_optimize['JpsiMu_mu3_pt'] = {'var': vardict['JpsiMu_mu3_pt'], 'isgl': '>', 'granularity': 100.0, 'histscale': 0.2, 'xmax': 6, 'xmin': 2}
to_optimize['JpsiMu_B_pt'] = {'var': vardict['JpsiMu_B_pt'], 'isgl': '>', 'granularity': 100.0, 'histscale': 0.2, 'xmax': 30, 'xmin': 6}
to_optimize['MET_sumEt'] = {'var': vardict['MET_sumEt'], 'isgl': '<', 'granularity': 100.0, 'histscale': 0.13, 'xmax': 3000, 'xmin': 0}
to_optimize['cosdphi_mu1_mu3'] = {'var': vardict['cosdphi_mu1_mu3'], 'isgl': '>', 'granularity': 100.0, 'histscale': 0.05, 'xmax': 1, 'xmin': 0.5}
to_optimize['cosdphi_mu2_mu3'] = {'var': vardict['cosdphi_mu2_mu3'], 'isgl': '>', 'granularity': 100.0, 'histscale': 0.05, 'xmax': 1, 'xmin': 0.5}
to_optimize['cosdphi_Jpsi_mu3'] = {'var': vardict['cosdphi_Jpsi_mu3'], 'isgl': '>', 'granularity': 100.0, 'histscale': 0.05, 'xmax': 1, 'xmin': 0.5}
to_optimize['JpsiMu_B_iso_ntracks'] = {'var': vardict['JpsiMu_B_iso_ntracks'], 'isgl': '>', 'granularity': 15.0, 'histscale': 0.12, 'xmax': 15, 'xmin': 0}
to_optimize['JpsiMu_B_mass'] = {'var': vardict['JpsiMu_B_mass'], 'isgl': '<', 'granularity': 36.0, 'histscale': 0.12, 'xmax': 9, 'xmin': 3}
to_optimize['JpsiMu_B_mcorr'] = {'var': vardict['JpsiMu_B_mcorr'], 'isgl': '>', 'granularity': 36.0, 'histscale': 0.12, 'xmax': 14, 'xmin': 3.5}

# Pairs to plot as 2D histograms for correlation checks

corrpairs = [

    ['JpsiMu_B_mcorr', 'JpsiMu_B_mass'],
    ['JpsiMu_mu3_pt', 'JpsiMu_B_mass'],
    ['JpsiMu_mu3_pt', 'JpsiMu_mu3_doca2mu1'],
    ['JpsiMu_mu3_pt', 'JpsiMu_mu3_doca2mu2'],
    ['JpsiMu_mu3_pt', 'cosdphi_Jpsi_mu3'],
    ['JpsiMu_mu3_pt', 'JpsiMu_B_vprob'],
    ['JpsiMu_mu3_pt', 'JpsiMu_Jpsi_fls3d'],

]
