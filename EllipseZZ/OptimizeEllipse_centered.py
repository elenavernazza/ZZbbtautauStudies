# Elliptical cut optimization for ZZ/ZH->bbtautau analysis
# this version centers the ellipse on the signal maximum and then fits separately the projected histograms 

import ROOT, os, math, sys
import scipy.optimize


def is_inside_ellipse(x1, y1, r1, r2, x, y):
    dist_x = (x - x1) ** 2 / r1 ** 2
    dist_y = (y - y1) ** 2 / r2 ** 2
    dist = math.sqrt(dist_x + dist_y)
    return dist < 1
    
def integrate_inside_ellipse(h, e):
    integral = 0
    x1 = e.GetX1()
    y1 = e.GetY1()
    r1 = e.GetR1()
    r2 = e.GetR2()
    for xbin in range(1, h.GetNbinsX() + 1):
        for ybin in range(1, h.GetNbinsY() + 1):
            bin_center_x = h.GetXaxis().GetBinCenter(xbin)
            bin_center_y = h.GetYaxis().GetBinCenter(ybin)
            # print(xbin, ybin, " ", bin_center_x, bin_center_y)
            
            if is_inside_ellipse(x1, y1, r1, r2, bin_center_x, bin_center_y):
                bin_content = h.GetBinContent(xbin, ybin)
                integral += bin_content
    return integral

if __name__ == "__main__" :

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--sig",       dest="signal",       help="Input signal root file",     default=None                                  )
    parser.add_option("--hSig",      dest="signalHist",   help="Name of the histogram for signal", default="zz_sl_signal")
    parser.add_option("--bkg",       dest="background",   help="Input background root file (for SoB computation)", default=None                                  )
    parser.add_option("--hBkg",      dest="backgroundHist",   help="Name of the histogram for background", default="zz_background")
    parser.add_option("--outdir",    dest="outdir",       help="Output directory",           default='./EllipsePlots'                      )
    parser.add_option("-e", "--eff", dest="efficiencies",   help="Signal efficiency (set multiple times for multiple efficiencies at same time)", action="append", default=[0.8, 0.9, 0.95])
    # parser.add_option("--scan",      dest="scan",         help="Scan type (wide/fine)",      default="fine")
    # parser.add_option("--optimizer", dest="optimizer", help="Optimizer type : grid or scipy or multiprocess_grid", default="grid")
    # parser.add_option("--constrainNonNegative", dest="constrainNonNegative", help="Constrain ellipse so it does not overlap with negative mass regions", default=False, action="store_true")
    (options, args) = parser.parse_args()
    print(options)

    odir = options.outdir 
    os.system("mkdir -p " + odir)
    FileName_sig = options.signal
    FileName_bkg = options.background

    print(' ### INFO: Load histograms')

    tf_sig = ROOT.TFile.Open(FileName_sig)
    dir = tf_sig.Get("histograms")
    dir.cd()
    h_sig = ROOT.TH2D(dir.Get(options.signalHist))

    tf_bkg = ROOT.TFile.Open(FileName_bkg)
    dir = tf_bkg.Get("histograms")
    dir.cd()
    h_bkg = ROOT.TH2D(dir.Get(options.backgroundHist))


    canvas_tautau = ROOT.TCanvas("canvas", "mtautau", 800, 600)
    canvas_tautau.cd()
    h_sig_mtautau = h_sig.ProjectionX()
    fit_mtautau = h_sig_mtautau.Fit("gaus", "S")
    h_sig_mtautau.Draw()
    canvas_tautau.Update()
    canvas_tautau.SaveAs(odir + f"/fit_mtautau.png")
    canvas_tautau.SaveAs(odir + f"/fit_mtautau.pdf")
    canvas_tautau.Close()

    canvas_bb = ROOT.TCanvas("canvas", "mbb", 800, 600)
    canvas_bb.cd()
    h_sig_mbb = h_sig.ProjectionY()
    fit_mbb = h_sig_mbb.Fit("gaus", "S")
    h_sig_mbb.Draw()
    canvas_bb.Update()
    canvas_bb.SaveAs(odir + f"/fit_mbb.png")
    canvas_bb.SaveAs(odir + f"/fit_mbb.pdf")
    canvas_bb.Close()


    def computeSigEff(alpha):
        e = ROOT.TEllipse(fit_mtautau.Get().GetParams()[1], fit_mbb.Get().GetParams()[1], alpha*fit_mtautau.Get().GetParams()[2], alpha*fit_mbb.Get().GetParams()[2])
        return integrate_inside_ellipse(h_sig, e) / h_sig.Integral()
    
    for efficiency_target in options.efficiencies:
        alpha_best = scipy.optimize.bisect(lambda alpha: computeSigEff(alpha) - efficiency_target, 0.1, 10, xtol=0.01)
        Best_E = ROOT.TEllipse(fit_mtautau.Get().GetParams()[1], fit_mbb.Get().GetParams()[1], alpha_best*fit_mtautau.Get().GetParams()[2], alpha_best*fit_mbb.Get().GetParams()[2])
        print(f"Efficiency target : {efficiency_target} -> alpha={alpha_best}, actual efficiency : {computeSigEff(alpha_best)}")

        SoSqrtB = computeSigEff(alpha_best)/max(math.sqrt(integrate_inside_ellipse(h_bkg, Best_E) / h_bkg.Integral()), sys.float_info.epsilon)
        print(f"S/sqrt(B) in ellipse : {SoSqrtB}")

        canvas = ROOT.TCanvas("canvas", "Histogram Canvas", 800, 600)
        canvas.cd()
        canvas.SetRightMargin(0.18)

        h_sig.SetTitle("ZH Signal")
        h_sig.Draw("COLZ")
        h_sig.GetXaxis().SetTitle("m_{#tau#tau}^{SVfit} [GeV]")
        h_sig.GetYaxis().SetTitle("m_{bb} [GeV]")
        h_sig.GetZaxis().SetTitleOffset(1.5)

        Best_E.SetFillStyle(0)
        Best_E.SetFillColorAlpha(0, 0)
        Best_E.SetLineWidth(2)
        Best_E.SetLineColor(ROOT.kGreen)
        Best_E.Draw("SAME")
        h_sig.SetMinimum(0.)
        
        legend = ROOT.TLegend(0.4,0.83,0.82,0.9)
        legend.AddEntry(Best_E, "Ellipse {}% : (X,Y,R1,R2) = ({}, {}, {}, {})".format(int(efficiency_target*100), int(Best_E.GetX1()), int(Best_E.GetY1()), int(Best_E.GetR1()), int(Best_E.GetR2())), "l")
        legend.AddEntry(0, "#alpha = {}, S/sqrt(B) = {}".format(alpha_best, SoSqrtB))
        legend.Draw()
        canvas.Update()
        odir_eff = options.outdir + '/SigEff{}'.format(efficiency_target)
        os.system("mkdir -p " + odir_eff)
        canvas.SaveAs(odir_eff + "/Best_ellipse{}_{}_{}_{}_{}.png".format(efficiency_target, int(Best_E.GetX1()), int(Best_E.GetY1()), int(Best_E.GetR1()), int(Best_E.GetR2())))
        canvas.SaveAs(odir_eff + "/Best_ellipse{}_{}_{}_{}_{}.pdf".format(efficiency_target, int(Best_E.GetX1()), int(Best_E.GetY1()), int(Best_E.GetR1()), int(Best_E.GetR2())))
        # breakpoint()
        canvas.Close()