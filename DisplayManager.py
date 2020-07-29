import ROOT
import copy


def applyLegendSettings(leg):
    leg.SetBorderSize(0)
    leg.SetFillColor(10)
    leg.SetLineColor(0)
    leg.SetFillStyle(0)
#    leg.SetTextSize(0.05)
#    leg.SetTextSize(0.04)
    leg.SetTextSize(0.025)
#    leg.SetTextFont(42)


def createRatioCanvas(name, errorBandFillColor=14, errorBandStyle=3354):
    cv = ROOT.TCanvas(name.replace('.pdf', ''), name.replace('.pdf', ''), 10, 10, 700, 600)

    # this is the tricky part...
    # Divide with correct margins
    cv.Divide(1, 2, 0.0, 0.0)

    # Set Pad sizes
    cv.GetPad(1).SetPad(0.0, 0.32, 1., 1.0)
    cv.GetPad(2).SetPad(0.0, 0.00, 1., 0.34)

    cv.GetPad(1).SetFillStyle(4000)
    cv.GetPad(2).SetFillStyle(4000)

    # Set pad margins 1
    cv.cd(1)
    ROOT.gPad.SetTopMargin(0.08)
    ROOT.gPad.SetLeftMargin(0.12)
    ROOT.gPad.SetBottomMargin(0.03)
    ROOT.gPad.SetRightMargin(0.1)

    # Set pad margins 2
    cv.cd(2)
    ROOT.gPad.SetBottomMargin(0.35)
    ROOT.gPad.SetLeftMargin(0.12)
    ROOT.gPad.SetRightMargin(0.1)

    bogyHist = ROOT.TH1F("legendPseudoHist", "", 1, 1., 2.)
    bogyHist.SetFillColor(errorBandFillColor)
    bogyHist.SetFillStyle(errorBandStyle)
    bogyHist.SetLineColor(0)

    cv.cd(1)
    return cv


class DisplayManager(object):

    def __init__(self, name, isLog, ratio, logrange=0, xmin=0.42, ymin=0.6, isOpt=False, is2D=False):

        if ratio:
            self.canvas = createRatioCanvas(name.replace('pdf', ''))
        else:
            self.canvas = ROOT.TCanvas(name.replace('.pdf', ''))
        if is2D:
            self.canvas.SetRightMargin(0.2)
            self.canvas.SetLeftMargin(0.2)

        self.logrange = logrange
        self.isLog = isLog
        self.name = name
        self.draw_ratio = ratio
        self.histos = []
        self.draw_legend = False
#        self.Legend = ROOT.TLegend(0.42, 0.6, 0.8, 0.85)
        self.Legend = ROOT.TLegend(xmin, ymin, xmin+0.4, ymin+0.2)
        applyLegendSettings(self.Legend)

        self.draw_ratioLegend = ROOT.TLegend(0.15, 0.79, 0.5, 0.89)
        applyLegendSettings(self.draw_ratioLegend)

        self.pullRange = 0.5
#        self.canvas.Print(self.name + '[')

#    def __del__(self):
#        self.canvas.Print(self.name + ']')

    def Draw(self, histos, titles, isOpt, is2D=False):

        self.histos = histos
        self.isOpt = isOpt
        self.is2D = is2D

        self.Legend.Clear()
        self.draw_ratioLegend.Clear()

        for i, h in enumerate(self.histos):
            title = titles[i]
            if not is2D:
                if not isOpt:
                    if h.GetTitle()=="stack":
                        self.Legend.AddEntry(h, title, 'lp')
                    else:
                        self.Legend.AddEntry(h, title, 'lep')
                        #self.Legend.AddEntry(h, title + ': ' + '{0:.1f}'.format(h.Integral()), 'lep')
                    if len(titles) > len(histos) and i == len(histos)-1:
                        j = i + 1
                        while j < len(titles):
                            self.Legend.AddEntry(0, '', '')
                            self.Legend.AddEntry(0, titles[j], '')
                            j += 1
                    ymax = max(h.GetMaximum() for h in self.histos)
                    ymin = min(h.GetMinimum() for h in self.histos)
                        
                    if i == 0:
                        h.Draw('HIST E')
                    else:
                        h.Draw('SAME HIST E')
                else: 
                    self.Legend.AddEntry(h, title, 'l')
                    if len(titles) > len(histos) and i == len(histos)-1:
                        j = i + 1
                        while j < len(titles):
                            self.Legend.AddEntry(0, '', '')
                            self.Legend.AddEntry(0, titles[j], '')
                            j += 1
                    ymax = histos[0].GetMaximum()
                    ymin = histos[0].GetMinimum()
                    if i == 0:
                        h.Draw('HIST')
                    elif i < 3:
                        h.Draw('SAME HIST')
                    else:
                        h.Draw('SAME, HIST')
            else:
                h.Draw('COLZ')

        if self.draw_legend:
            self.histos[0].GetYaxis().SetRangeUser(0., ymax * 1.5)
        elif not is2D:
            self.histos[0].GetYaxis().SetRangeUser(0, ymax * 1.05)
        if not is2D and ymin < 0:
            print 'set negative minimum ...'
            if self.draw_legend:
                self.histos[0].GetYaxis().SetRangeUser(ymin*1.5, ymax * 1.3)
            else:
                self.histos[0].GetYaxis().SetRangeUser(ymin*1.05, ymax * 1.05)

        if self.isLog:
#            h.GetYaxis().SetRangeUser(0.001, ymax * 100)
            self.histos[0].GetYaxis().SetRangeUser((0.1)**(self.logrange), ymax * 2 )
        if self.draw_legend:
            self.Legend.Draw()

        if self.isLog:
            if self.draw_ratio:
                self.canvas.GetPad(1).SetLogy()
            else:
                self.canvas.SetLogy()

        pull_histos = []

        if self.draw_ratio:
            self.canvas.cd(2)

            for ihist in range(1, len(self.histos)):
                histPull = copy.deepcopy(self.histos[ihist])
                pull_histos.append(histPull)
                histPull.Divide(self.histos[0])
                histPull.UseCurrentStyle()

                histPull.SetLineColor(self.histos[ihist].GetLineColor())
                histPull.SetMarkerColor(self.histos[ihist].GetLineColor())
                histPull.SetMarkerSize(self.histos[ihist].GetMarkerSize())
                histPull.SetLineStyle(self.histos[ihist].GetLineStyle())
                histPull.SetLineWidth(self.histos[ihist].GetLineWidth())

                histPull.GetYaxis().SetRangeUser(-self.pullRange + 1., self.pullRange + 1.)

                # defaultYtoPixel = 408.  # height in pixels of default canvas
                defaultYtoPixel = self.canvas.GetPad(1).YtoPixel(0.)
                pad2YtoPixel = float(self.canvas.GetPad(2).YtoPixel(0))
                pad2XaxisFactor = defaultYtoPixel / pad2YtoPixel

#                print 'Pad size : ', self.histos[0].GetXaxis().GetLabelSize(), pad2XaxisFactor
                histPull.GetXaxis().SetLabelSize(self.histos[0].GetXaxis().GetLabelSize()*pad2XaxisFactor)
                histPull.GetXaxis().SetLabelOffset(self.histos[0].GetXaxis().GetLabelOffset()*pad2XaxisFactor)
                histPull.GetXaxis().SetTitleSize(self.histos[0].GetXaxis().GetTitleSize()*pad2XaxisFactor)
                histPull.GetXaxis().SetTitleOffset(self.histos[0].GetXaxis().GetTitleOffset()/pad2XaxisFactor*2.5)

                histPull.GetYaxis().SetLabelSize(self.histos[0].GetYaxis().GetLabelSize()*pad2XaxisFactor)
                histPull.GetYaxis().SetLabelOffset(self.histos[0].GetYaxis().GetLabelOffset()*pad2XaxisFactor)
                histPull.GetYaxis().SetTitleSize(self.histos[0].GetYaxis().GetTitleSize()*pad2XaxisFactor)
                histPull.GetYaxis().SetTitleOffset(0.8*self.histos[0].GetYaxis().GetTitleOffset()/pad2XaxisFactor)

                histos[0].GetYaxis().SetTitleOffset(1.15)

                histPull.GetYaxis().CenterTitle()
                histPull.GetXaxis().SetTickLength(histPull.GetXaxis().GetTickLength()*pad2XaxisFactor)
                histPull.GetYaxis().SetNdivisions(306)

                histPull.GetYaxis().SetTitle("Ratio")
                histPull.SetTitle('')
                if ihist == 1:
                    histPull.Draw("ep")
                else:
                    histPull.Draw("same ep")

                line = ROOT.TLine(histPull.GetXaxis().GetXmin(), 1., histPull.GetXaxis().GetXmax(), 1.)
                line.SetLineStyle(2)
                line.Draw()

                self.draw_ratioLegend.AddEntry(histPull, titles[ihist])


#            self.draw_ratioLegend.Draw()

            # This is a little bit ugly though ...

            for i, h in enumerate(self.histos):
                h.GetXaxis().SetLabelSize(0)

            self.canvas.cd(1)

        self.canvas.Update()
        self.canvas.Print(self.name)
        self.canvas.Print(self.name.replace('.pdf', '.png'))
