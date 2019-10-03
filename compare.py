import copy, math, os, collections, sys
from numpy import array
#from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from ROOT import TFile, TH1F, TTree, gROOT, gStyle
from DisplayManager import DisplayManager
from officialStyle import officialStyle

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

colours = [1, 2, 4, 6, 8, 13, 15]
styles = [1, 2, 4, 3, 5, 1, 1]
widths = [3,3,3,3]

def applyHistStyle(h, i):
    h.SetLineColor(colours[i])
    h.SetMarkerColor(colours[i])
    h.SetMarkerSize(0)
    h.SetLineStyle(styles[i])
    h.SetLineWidth(widths[i])
    h.SetStats(False)

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def comparisonPlots(hists, titles, isLog=False, pname='sync.pdf', isRatio=True, isLegend=True):

    display = DisplayManager(pname, isLog, isRatio, 0.2, 0.7)
    display.draw_legend = isLegend

    display.Draw(hists, titles)


def sproducer(key, rootfile, name, ivar):

    hist = TH1F('h_' + key + '_' + name, 
                'h_' + key + '_' + name, 
                ivar['nbin'], ivar['xmin'], ivar['xmax'])

    hist.Sumw2()
    exp = '(' + ivar['sel'] + ')'
        
    tree = rootfile.Get(ivar['tree'])

    print ivar['var'] + ' >> ' + hist.GetName(), exp
    
    tree.Draw(ivar['var'] + ' >> ' + hist.GetName(), exp)
    hist.GetXaxis().SetTitle(ivar['xtitle'])
    hist.GetYaxis().SetTitle(ivar['ytitle'])
        
    return copy.deepcopy(hist)

ensureDir('Plots/')

pfile = TFile('Myroot_test.root')
sfile = TFile('Myroot_pvip.root')

hists = []
titles = []


nbin = 100
x_min = -4.
x_max = 4.
xtitle = 'selected vtx_{z} - gen. vtx_{z} (cm)'
ytitle = 'a.u.'

vardict = collections.OrderedDict() 

vardict['PV'] = {'file':pfile, 'tree':'tree', 'var':'Jpsi_PV_vz - Jpsi_genPV_vz', 'nbin':nbin, 'xmin':x_min, 'xmax':x_max, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'PV'}
vardict['JPVZ'] = {'file':pfile, 'tree':'tree', 'var':'Jpsi_vz - Jpsi_genPV_vz', 'nbin':nbin, 'xmin':x_min, 'xmax':x_max, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'min. #Deltaz(J/#psi SV vz)'}
vardict['bbPV'] = {'file':pfile, 'tree':'tree', 'var':'Jpsi_bbPV_vz - Jpsi_genPV_vz', 'nbin':nbin, 'xmin':x_min, 'xmax':x_max, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'min. #Deltaz(J/#psi ext. back to beamline)'}
vardict['pvipPV'] = {'file':sfile, 'tree':'tree', 'var':'Jpsi_bbPV_vz - Jpsi_genPV_vz', 'nbin':nbin, 'xmin':x_min, 'xmax':x_max, 'xtitle':xtitle, 'ytitle':ytitle, 'sel':'1', 'title':'min. doc (J/#psi ext. back to beamline)'}



for vkey, ivar in vardict.iteritems():

    print vkey

    hist = sproducer(vkey, pfile, vkey, ivar)
    hists.append(copy.deepcopy(hist))
    titles.append(ivar['title'])

   
for ii, ihist in enumerate(hists):
    applyHistStyle(ihist, ii)
#    ihist.Scale(1./ihist.GetSumOfWeights())
    ihist.SetMaximum(ihist.GetBinContent(ihist.GetMaximumBin())*1.2)
        
comparisonPlots(hists, titles, False, 'Plots/pvchoice.pdf', False)
comparisonPlots(hists, titles, True, 'Plots/pvchoice_log.pdf', False)


