import collections
import itertools
import shutil
import copy, math, os, collections, sys
from numpy import array
#from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from ROOT import TFile, TH1F, TTree, gROOT, gStyle, THStack, TMath, TCanvas, TLegend, TEventList, TDirectory, gObjectTable, TLine, TH2F
from DisplayManager import DisplayManager
from officialStyle import officialStyle
from makeSimpleHtml import writeHTML
from samples import *
from varsdict import *

from optparse import OptionParser, OptionValueError

usage = "usage: python compare.py [--compare: True, False (default: False)] [--CutOpt: True, False (default: False)] [--compareNorm: True, False (default: False)] [--twoDHist: True, False (default: False)] [--rmrf: True, False (default: False)] [--outdir: <Directory For Outgoing Files> (default: /eos/home-w/wvetens/www/BPH_v8/)] [--precut: <Precuts in TCut string format> (default: '')]"
parser = OptionParser(usage)
parser.add_option("-c", "--compare", default=False, action="store_true", help="Use this option to generate comparison plots between signal and background", dest="isCompare")
parser.add_option("-o", "--cutOpt", default=False, action="store_true", help="Use this option to generate scans for cut optimization", dest="isCutOpt")
parser.add_option("-n", "--compareNorm", default=False, action="store_true", help="Use this option to compare the histograms Normalized to 1", dest="isNorm")
parser.add_option("-t", "--twoDHist", default=False, action="store_true", help="Use this option to compare two variables and check for correlations using a two-dimensional histogram", dest="is2DHist")
parser.add_option("-f", "--rmrf", default=False, action="store_true", help="Forcefully overwrite the output directories to remove old outputs", dest="isrmrf")
parser.add_option("--outdir", default='/eos/home-w/wvetens/www/YutaNTuples_cutflowOptimization/', action="store", help="Output Directory for plots", dest="outdir")
parser.add_option("--precut", default='', action="store", help="List of Cuts to apply before plotting", dest="precut")
#parser.add_option("-g", "--gen", default=False, action="store_true", help="Run on Gen Level Info", dest="isgen")


(options, args) = parser.parse_args()

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptStat(0)

directory = options.outdir
cut0 = options.precut

datacuttitle = sampledict['dataC']['title']
NDatEvts = 0
for samplekey, isample in sampledict.iteritems():
    if 'data' in samplekey:
        NDatEvts += isample['file'].Get('cuthist').GetBinContent(1)
datacuttitle += ' ['+str(round(NDatEvts))+':'
#colours = [1, 2, 4, 6, 8, 13, 15]
#styles = [1, 2, 4, 3, 5, 1, 1]
#widths = [3,3,3,3]
def applyHistStyle(h, i):
    h.SetLineColor(colours[i])
    h.SetMarkerColor(colours[i])
    if i =='data':
        h.SetMarkerSize(1)
    else:
        h.SetMarkerSize(0)
    h.SetLineStyle(styles[i])
    h.SetLineWidth(widths[i])
    h.SetStats(False)

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def WeightCalc(crossxn, crossxnerr, Tfile):
    nevts = Tfile.Get('cuthist').GetBinContent(1)
    wgt = lumi * crossxn / nevts
    wgterr = lumi * crossxnerr / nevts
    return [wgt, wgterr, nevts]

def comparisonPlots(hists, titles, isLog=False, LogRange=0, pname='sync.pdf', isRatio=True, isLegend=True, isCutOpt=False, is2D=False):

    display = DisplayManager(pname, isLog, isRatio, LogRange, 0.2, 0.7, isCutOpt, is2D)
    display.draw_legend = isLegend

    display.Draw(hists, titles, isCutOpt, is2D)


def sproducer(key, ivar, samplekey, sample,cut0='', Xtitled=False, Xtitle=''):

    hist = TH1F('h_' + key, 
                'h_' + key, 
                ivar['nbins'], ivar['xmin'], ivar['xmax'])

    hist.Sumw2()
    if "data" in samplekey:
        wgt = '1'
    else:
        wgt = str(WeightCalc(sample['crossxn'],sample['crossxnerr'],sample['file'])[0]) 
    if cut0 == '':
        exp = '('+wgt+')'
    else:
        exp = wgt+'*(' + cut0 + ')'
    rootfile = sample['file']
        
    tree = rootfile.Get('tree')

    if "data" in samplekey:
        tree.Draw(key + ' >> ' + hist.GetName(), exp)
    else:
        tree.Draw(key + ' >> ' + hist.GetName(), 'weight_pu[0]*'+exp)
    if Xtitled:
        hist.GetXaxis().SetTitle(Xtitle)
    else:
        hist.GetXaxis().SetTitle(ivar['xtitle'])
    hist.GetYaxis().SetTitle(ivar['ytitle'])
        
    return copy.deepcopy(hist)
def optsproducer(key, ivar, samplekey, sample, tcut):

    hist = TH1F('h_' + key, 
                'h_' + key, 
                ivar['nbins'], ivar['xmin'], ivar['xmax'])

    wgt =  str(WeightCalc(sample['crossxn'], sample['crossxnerr'], sample['file'])[0])
    rootfile = sample['file']
        
    tree = rootfile.Get('tree')
    hist.GetYaxis().SetTitleOffset(2.5)

    if tcut == '':
        tree.Draw(key + ' >> ' + hist.GetName(), '('+'weight_pu[0]*'+wgt+')')
    else:
        tree.Draw(key + ' >> ' + hist.GetName(), 'weight_pu[0]*'+wgt+'*'+tcut)
        
    return copy.deepcopy(hist)
def sproducer2D(key1, key2, var1, var2, samplekey, sample):

    hist = TH2F('h_' + key1 + '_' + key2, 
                samplekey+';'+var1['xtitle']+';'+var2['xtitle']+';events', 
                var1['nbins'], var1['xmin'], var1['xmax'],
                var2['nbins'], var2['xmin'], var2['xmax'])

    hist.Sumw2()
    if "data" in samplekey:
        wgt = '1'
    else:
        wgt = str(WeightCalc(sample['crossxn'],sample['crossxnerr'],sample['file'])[0]) 
    if cut0 == '':
        exp = '('+wgt+')'
    else:
        exp = wgt+'*(' + cut0 + ')'
    rootfile = sample['file']
        
    tree = rootfile.Get('tree')

    if "data" in samplekey:
        tree.Draw(key2 + ':' + key1 + ' >> ' + hist.GetName(), exp)
    else:
        tree.Draw(key2 + ':' + key1  + ' >> ' + hist.GetName(), "weight_pu[0]*"+exp)
    hist.GetXaxis().SetTitleOffset(1)
    hist.GetYaxis().SetTitleOffset(1.7)
    hist.GetZaxis().SetTitleOffset(1.7)
    #hist.SetFontSize(14)
        
    return copy.deepcopy(hist)

def CutEffects(directory, histname, cut='', tag=''):
    masshists = []
    titles = []
    FullDataHist = TH1F("FullDat"+histname, "FullDat" + histname, vardict['JpsiMu_B_mass']['nbins'], vardict['JpsiMu_B_mass']['xmin'], vardict['JpsiMu_B_mass']['xmax'])
    for samplekey, isample in sampledict.iteritems():
        weight = WeightCalc(isample['crossxn'], isample['crossxnerr'], isample['file'])
        if 'OniaAndX' in samplekey:
            if tag != '' and cut != '':
                masshist = sproducer('JpsiMu_B_mass', vardict['JpsiMu_B_mass'], samplekey, isample, tag + ' && ' + cut, True, histname)
            elif tag != '' and cut == '':
                masshist = sproducer('JpsiMu_B_mass', vardict['JpsiMu_B_mass'], samplekey, isample, tag, True, histname)
            else:
                masshist = sproducer('JpsiMu_B_mass', vardict['JpsiMu_B_mass'], samplekey, isample, cut, True, histname)
            applyHistStyle(masshist, samplekey)
        elif 'data' in samplekey:
            masshist = sproducer('JpsiMu_B_mass', vardict['JpsiMu_B_mass'], samplekey, isample, cut, True, histname)
            FullDataHist.Add(masshist)
        else:
            masshist = sproducer('JpsiMu_B_mass', vardict['JpsiMu_B_mass'], samplekey, isample, cut, True, histname)
            applyHistStyle(masshist, samplekey)
        if not 'data' in samplekey:
            ititle = isample['title'] + ' ['+str(round(isample['file'].Get('cuthist').GetBinContent(1)))+':'+ str(round(masshist.GetBinContent(0) + masshist.Integral() + masshist.GetBinContent(vardict['JpsiMu_B_mass']['nbins']), isample['digits']))+']'
            if options.isNorm:
                if masshist.Integral()!=0:
                    masshist.Scale(1./masshist.Integral()) 
            masshists.append(copy.deepcopy(masshist))
            titles.append(ititle)
    dattitle = datacuttitle + str(round(FullDataHist.GetBinContent(0) + FullDataHist.Integral() + FullDataHist.GetBinContent(vardict['JpsiMu_B_mass']['nbins']), 0))+']'
    titles.append(dattitle)
    if options.isNorm:
        if FullDataHist.Integral()!=0:
            FullDataHist.Scale(1./FullDataHist.Integral())
    applyHistStyle(FullDataHist, 'dataC')
    masshists.append(copy.deepcopy(FullDataHist))
    comparisonPlots(masshists, titles, vardict['JpsiMu_B_mass']['isLog'], vardict['JpsiMu_B_mass']['loglowerlimit'], directory+histname+'.pdf', vardict['JpsiMu_B_mass']['isRatio'], vardict['JpsiMu_B_mass']['isLegended'])

if options.is2DHist:
    tdir = directory+'2dhists/'
    plottdir = tdir+'plots/'
    logstdir = tdir+'logs/'
    if options.isrmrf:
        if os.path.exists(tdir):
            shutil.rmtree(tdir)
    ensureDir(plottdir)
    ensureDir(logstdir)
if options.isCompare:
    cdir = directory+'comparisons/'
    plotcdir = cdir+'plots/'
    logscdir = cdir+'logs/'
    if options.isrmrf:
        if os.path.exists(cdir):
            shutil.rmtree(cdir)
    ensureDir(plotcdir)
    ensureDir(logscdir)
if options.isCutOpt:
    odir = directory+'cutopt/'
    plotodir = odir+'plots/'
    logsodir = odir+'logs/'
    if options.isrmrf:
        if os.path.exists(odir):
            shutil.rmtree(odir)
    ensureDir(plotodir)
    ensureDir(logsodir)


# to add a new variable, add a new entry in 'varsdict.py'. To add a new sample, add a new entry in 'samples.py'.
GoodCuts = []
GoodVars = []
for varkey, ivar in vardict.iteritems():

    if ivar['HasStackPlot']: 
        addtostack = []
    hists = []
    titles = []
    
    var = varkey
    FullDatHist = TH1F('h_dat_'+var, 'h_dat_'+var, ivar['nbins'], ivar['xmin'], ivar['xmax'])
    #print ivar
 
    if var == list(vardict.items()[0])[0]:
        for samplekey, isample in sampledict.iteritems():
            if not options.isNorm:
                print samplekey
                print "Non-PU Weight = ", WeightCalc(isample['crossxn'],0,isample['file'])[0], " +/- ", WeightCalc(0, isample['crossxnerr'], isample['file'])[1]
    #print "Weighted Bc->J/psi+mu+nu evts: ", signal_BcJpsiMuNu.Get('cuthist').GetBinContent(3)*WeightCalc(90,0,signal_BcJpsiMuNu)[0]
    #print "Weighted Bc->J/psi+tau+nu evts: ", bg_BcJpsiTauNu.Get('cuthist').GetBinContent(3)*WeightCalc(90,0,bg_BcJpsiTauNu)[0]
    if options.isCompare:
        gStyle.SetOptTitle(0)
        if ivar['HasStackPlot']:
            stackhist = THStack("stack","stack")
        for samplekey, isample in sampledict.iteritems():
            hist = sproducer(var, ivar, samplekey, isample)
            applyHistStyle(hist, samplekey)
            weight = WeightCalc(isample['crossxn'], isample['crossxnerr'], isample['file'])
            # Add number of initial and final events to title (only want to do this once)
            # add histogram to stack hist if it isn't data and normalize histograms
            if 'data' in samplekey:
                FullDatHist.Add(hist)
            else:
                titles.append(isample['title'] + ' ['+str(round(isample['file'].Get('cuthist').GetBinContent(1)))+':'+ str(round(hist.GetBinContent(0) + hist.Integral() + hist.GetBinContent(ivar['nbins']), isample['digits']))+']')
            if options.isNorm and 'data' not in samplekey:
                if hist.Integral()!=0:
                    hist.Scale(1./hist.Integral()) 
            if 'data' not in samplekey:
                if ivar['HasStackPlot']:
                    stackhist.Add(copy.deepcopy(hist))
                else:
                    hists.append(copy.deepcopy(hist))
        datatitle = datacuttitle + str(round(FullDatHist.GetBinContent(0) + FullDatHist.Integral() + FullDatHist.GetBinContent(ivar['nbins']), 0))+']'
        titles.append(datatitle)
        if options.isNorm:
            if FullDatHist.Integral()!=0:
                FullDatHist.Scale(1./FullDatHist.Integral())
        hists.append(copy.deepcopy(FullDatHist))
    
        if ivar['HasStackPlot']:
            hists.append(stackhist)
            titles.append("stack")
    
        comparisonPlots(hists, titles, ivar['isLog'], ivar['loglowerlimit'], plotcdir+var+'.pdf', ivar['isRatio'], ivar['isLegended'])
    if options.isCutOpt:
        gStyle.SetOptTitle(0)
        if var not in to_optimize:
            continue
        optparams = to_optimize[var]
        print 'optimizing ', var
        granularity = optparams['granularity']
        igran = int(granularity)
        split = (optparams['xmax']-optparams['xmin'])/granularity
        coh1name="cutopthist1"+var
        #coh2name="cutopthist2"+var
        #coh3name="cutopthist3"+var
        signame="sig"+var
        bckgname="bckg"+var
        coh1 = TH1F(coh1name, "Cut Optimization for "+str(ivar['xtitle']), igran, optparams['xmin'], optparams['xmax'])
        coh1.GetYaxis().SetTitle('a.u.')
        coh1.GetYaxis().SetTitleFont(12)
        coh1.GetXaxis().SetTitle(str(ivar['xtitle']))
        #coh2 = TH1F(coh2name, "Cut Optimization for "+str(ivar['xtitle']), igran, optparams['xmin'], optparams['xmax'])
        #coh2.GetYaxis().SetTitle('a.u.')
        #coh2.GetYaxis().SetTitleFont(12)
        #coh2.GetXaxis().SetTitle(str(ivar['xtitle']))
        #coh3 = TH1F(coh3name, "Cut Optimization for "+str(ivar['xtitle']), igran, optparams['xmin'], optparams['xmax'])
        #coh3.GetYaxis().SetTitle('a.u.')
        #coh3.GetYaxis().SetTitleFont(12)
        #coh3.GetXaxis().SetTitle(str(ivar['xtitle']))
        sigh = TH1F(signame, "s", igran, optparams['xmin'], optparams['xmax'])
        bckgh = TH1F(bckgname, "b", igran, optparams['xmin'], optparams['xmax'])
        if cut0 == '':
            signal_BcJpsiMuNu.Get('tree').Draw(var+'>>'+signame)
            bg_OniaAndX_MuMu_J.Get('tree').Draw(var+'>>'+bckgname)
            bh0 = optsproducer('JpsiMu_B_mass', vardict['JpsiMu_B_mass'], samplekey, sampledict['bg_OniaAndX_MuMu_J'], '')
            sh0 = optsproducer('JpsiMu_B_mass', vardict['JpsiMu_B_mass'], samplekey, sampledict['signal_BcJpsiMuNu'], '')
        else:
            signal_BcJpsiMuNu.Get('tree').Draw(var+'>>'+signame, '('+cut0+')')
            bg_OniaAndX_MuMu_J.Get('tree').Draw(var+'>>'+bckgname, '('+cut0+')')
            bh0 = optsproducer('JpsiMu_B_mass', vardict['JpsiMu_B_mass'], samplekey, sampledict['bg_OniaAndX_MuMu_J'], '('+cut0+')')
            sh0 = optsproducer('JpsiMu_B_mass', vardict['JpsiMu_B_mass'], samplekey, sampledict['signal_BcJpsiMuNu'], '('+cut0+')')
        b0 = bh0.Integral()
        s0 = sh0.Integral()
        if not cut0 == '':
            icut = ' && ('+cut0+')'
        else:
            icut = ''
        for x in range(1,igran):
            xparam = optparams['xmin']+split*x
            tcut = '('+var+optparams['isgl']+str(xparam)+icut+')'
            bh = optsproducer('JpsiMu_B_mass', vardict['JpsiMu_B_mass'], samplekey, sampledict['bg_OniaAndX_MuMu_J'], tcut)
            sh = optsproducer('JpsiMu_B_mass', vardict['JpsiMu_B_mass'], samplekey, sampledict['signal_BcJpsiMuNu'], tcut)
            b = bh.Integral()
            s = sh.Integral()
            if b == 0:
                coh1.AddBinContent(x+1, 0)
                #coh2.AddBinContent(x+1, 0)
                #coh3.AddBinContent(x+1, 0)
            else:
                coh1.AddBinContent(x+1, s/TMath.Sqrt(s+b))
                #coh2.AddBinContent(x+1, s/TMath.Sqrt(b))
                #coh3.AddBinContent(x+1, s/b)
        optcutbin1 = coh1.GetMaximumBin()
        optcut1 = coh1.GetBin(optcutbin1)
        optcut1 = optparams['xmin'] + optcutbin1 * split
        cutline1 = TLine.TLine(optcut1, 0, optcut1, coh1.GetMaximum())
        GoodCuts += [var+optparams['isgl']+str(optcut1)]
        GoodVars += [var]
        #optcutbin2 = coh2.GetMaximumBin()
        #optcut2 = optparams['xmin'] + optcutbin2 * split
        #cutline2 = TLine.TLine(optcut2, 0, optcut2, coh2.GetMaximum())
        #optcutbin3 = coh3.GetMaximumBin()
        #optcut3 = coh3.GetBin(optcutbin3)
        #optcut3 = optparams['xmin'] + optcutbin3 * split
        #cutline3 = TLine.TLine(optcut3, 0, optcut3, coh3.GetMaximum())
        histscale = optparams['histscale']
        sigh.SetLineColor(2)
        bckgh.SetLineColor(4)
        cutline1.SetLineColor(6)
        #cutline2.SetLineColor(6)
        #cutline3.SetLineColor(6)
        opt_signif = coh1.GetMaximum()
        sigh.Scale(histscale * coh1.Integral()/sigh.Integral())
        bckgh.Scale(histscale * coh1.Integral()/bckgh.Integral())
        comparisonPlots([coh1, sigh, bckgh, cutline1], ['#frac{s}{#sqrt{s+b}}', 'B_{c}->J/#psi+#mu+#nu Signal', 'pp->J/#psi+X Background', 'Optimal Cut: ' + var +' '+optparams['isgl']+' '+str(optcut1)+'. #frac{s}{#sqrt{s+b}} = '+str(coh1.GetMaximum())+' vs no cuts: '+str(s0/TMath.Sqrt(s0+b0))], False, False, plotodir+var+'_cutopt1'+'.pdf', False, True, True)

if options.isCutOpt:
    ptcut = 'JpsiMu_mu3_pt > 15'
    tags = ['isBplusJpsiKplus', 'isBplusJpsiPiplus', 'isBplusJpsi3Kplus', 'isBplusJpsiKPiPiplus', 'isBplusJpsiPhiKplus', 'isBplusJpsiK0Piplus']
    allcuts = ''
# no optimized cuts no tags
    CutEffects(plotodir, 'NoCuts')
    CutEffects(plotodir, 'pT15_only', ptcut)
# no optimized cuts with tags
    for tag in tags: 
        CutEffects(plotodir, tag+'_NoCuts', '', tag)
        CutEffects(plotodir, tag+'_pT15_only', ptcut, tag)
# now going over optimized cuts, applying one, two, and three cuts
    for icut in xrange(len(GoodCuts)):
        if icut == 0:
            allcuts += GoodCuts[icut]
        else:
            allcuts += ' && ' + GoodCuts[icut]
# One optimized cut no tags
        CutEffects(plotodir, GoodVars[icut]+'_nopT', GoodCuts[icut])
        CutEffects(plotodir, GoodVars[icut]+'_pT15', GoodCuts[icut]+' && '+ptcut)
# one optimized cut with tags
        for tag in tags:
            CutEffects(plotodir, tag+'_'+GoodVars[icut]+'_nopT', GoodCuts[icut], tag)
            CutEffects(plotodir, tag+'_'+GoodVars[icut]+'_pT15', GoodCuts[icut]+' && '+ptcut, tag)
        Twocut_i = GoodCuts[icut]
        Threecut_i = GoodCuts[icut]
        for icut2 in xrange(len(GoodCuts)):
            if icut2 <= icut: continue
            Twocut_i += ' && ' + GoodCuts[icut2]
            Threecut_i += ' && ' + GoodCuts[icut2]
# Two optimized cuts no tags
            CutEffects(plotodir, GoodVars[icut]+'_'+GoodVars[icut2]+'_nopT', Twocut_i)
            CutEffects(plotodir, GoodVars[icut]+'_'+GoodVars[icut2]+'_pT15', Twocut_i+' && '+ptcut)
# Two optimized cuts with tags
            for tag in tags:
                CutEffects(plotodir, tag+'_'+GoodVars[icut]+'_'+GoodVars[icut2]+'_nopT', Twocut_i, tag)
                CutEffects(plotodir, tag+'_'+GoodVars[icut]+'_'+GoodVars[icut2]+'_pT15', Twocut_i+' && '+ptcut, tag)
            for icut3 in xrange(len(GoodCuts)):
                if icut3 <= icut2: continue
                Threecut_i += ' && ' + GoodCuts[icut3]
# Three optimized cuts no tags
                CutEffects(plotodir, GoodVars[icut]+'_'+GoodVars[icut2]+'_'+GoodVars[icut3]+'_nopT', Threecut_i)
                CutEffects(plotodir, GoodVars[icut]+'_'+GoodVars[icut2]+'_'+GoodVars[icut3]+'_pT15', Threecut_i+' && '+ptcut)
# Three optimized cuts with tags
                for tag in tags:
                    CutEffects(plotodir, tag+'_'+GoodVars[icut]+'_'+GoodVars[icut2]+'_'+GoodVars[icut3]+'_nopT', Twocut_i, tag)
                    CutEffects(plotodir, tag+'_'+GoodVars[icut]+'_'+GoodVars[icut2]+'_'+GoodVars[icut3]+'_pT15', Twocut_i+' && '+ptcut, tag)
            
    CutEffects(plotodir, 'AllCuts_nopT', allcuts)
    CutEffects(plotodir, 'AllCuts_pT15', allcuts + ' && ' + ptcut)
    for tag in tags: 
        CutEffects(plotodir, tag+'_AllCuts_nopT', allcuts, tag)
        CutEffects(plotodir, tag+'_AllCuts_pT15', allcuts + ' && ' + ptcut, tag)
        
            #sigh.Scale(histscale * coh2.Integral()/sigh.Integral())
            #bckgh.Scale(histscale * coh2.Integral()/bckgh.Integral())
            #comparisonPlots([coh2, sigh, bckgh, cutline2], ['#frac{s}{#sqrt{b}}', 'B_{c}->J/#psi+#mu+#nu Signal', 'pp->J/#psi+X Background', 'Cut: ' + var+' '+optparams['isgl']+' '+str(optcut2)+'.#frac{s}{#sqrt{b}} = '+str(round(coh2.GetMaximum(), 4))+' : '+str(round(s0/TMath.Sqrt(b0), 4))], False, False, plotodir+var+'_cutopt2'+'.pdf', False, True, True)
    
            #sigh.Scale(histscale * coh3.Integral()/sigh.Integral())
            #bckgh.Scale(histscale * coh3.Integral()/bckgh.Integral())
            #comparisonPlots([coh3, sigh, bckgh, cutline3], ['#frac{s}{b}', 'B_{c}->J/#psi+#mu+#nu Signal', 'pp->J/#psi+X Background', 'Cut: ' + var+' '+optparams['isgl']+' '+str(optcut3)+'.#frac{s}{b} = '+str(round(coh3.GetMaximum(), 8))+' : '+str(round(s0/b0, 8))], False, False, plotodir+var+'_cutopt3'+'.pdf', False, True, True)
    

if options.is2DHist:
    gStyle.SetOptTitle(1)
    gStyle.SetTitleX(.5)
    for item in corrpairs:
        mmhist1 = sproducer2D(item[0], item[1], vardict[item[0]], vardict[item[1]], 'bg_OniaAndX_MuMu_J', sampledict['bg_OniaAndX_MuMu_J']);
        mmhist2 = sproducer2D(item[0], item[1], vardict[item[0]], vardict[item[1]], 'signal_BcJpsiMuNu', sampledict['signal_BcJpsiMuNu']);
        mmhist3 = sproducer2D(item[0], item[1], vardict[item[0]], vardict[item[1]], 'dataC', sampledict['dataC']);
        comparisonPlots([mmhist1], [""], False, False, plottdir+item[0]+'_'+item[1]+'_'+'bg''.pdf', False, False, False, True)
        comparisonPlots([mmhist2], [""], False, False, plottdir+item[0]+'_'+item[1]+'_'+'signal'+'.pdf', False, False, False, True)
        comparisonPlots([mmhist3], [""], False, False, plottdir+item[0]+'_'+item[1]+'_'+'dataC'+'.pdf', False, False, False, True)
            
# This writes to a webpage so you can more easily view all the plots you've created in a web browser, which will display them simultaneously.
# This is optional, you can comment it out if you want to ...
if options.is2DHist:
    writeHTML(tdir, "2-D Histograms")
if options.isCompare:
    writeHTML(cdir, "Comparison Plots")
if options.isCutOpt:
    writeHTML(odir, "Cut Optimization")
