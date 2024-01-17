import ROOT, os, math
import numpy as np

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

'''
python3 OptimizeEllipseZZ.py --sig /eos/user/e/evernazz/cmt/FeaturePlot2D/ul_2018_v10/cat_mutau/prod_0524_2/root/Htt_svfit_mass_Hbb_mass__mutau_os_iso__pg_zz_signal__nodata.root \
 --bkg /eos/user/e/evernazz/cmt/FeaturePlot2D/ul_2018_v10/cat_mutau/prod_0524_2/root/Htt_svfit_mass_Hbb_mass__mutau_os_iso__pg_zz_background__nodata.root
python3 OptimizeEllipseZZ.py --sig /eos/user/e/evernazz/cmt/FeaturePlot2D/ul_2018_ZZ_v10/cat_base/prod_0608/root/Htt_svfit_mass_Hbb_mass__pg_zz_signal__nodata.root \
 --bkg /eos/user/e/evernazz/cmt/FeaturePlot2D/ul_2018_ZZ_v10/cat_base/prod_0608/root/Htt_svfit_mass_Hbb_mass__pg_zz_background__nodata.root --outdir EllipsePlots/all_base
'''
if __name__ == "__main__" :

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--sig",       dest="signal",       help="Input signal root file",     default=None                                  )
    parser.add_option("--bkg",       dest="background",   help="Input background root file", default=None                                  )
    parser.add_option("--outdir",    dest="outdir",       help="Output directory",           default='./EllipsePlots'                      )
    parser.add_option("--eff",       dest="efficiency",   help="Signal efficiency",          default=0.8                                   )
    # parser.add_option("--scan",      dest="scan",         help="Scan type (wide/fine)",      default=False,            action='store_true' )
    (options, args) = parser.parse_args()
    print(options)

    sig_eff_thr = float(options.efficiency)
    odir = options.outdir + '/SigEff{}'.format(sig_eff_thr)
    os.system("mkdir -p " + odir)
    FileName_sig = options.signal
    FileName_bkg = options.background

    print(' ### INFO: Load histograms')

    tf_sig = ROOT.TFile.Open(FileName_sig)
    dir = tf_sig.Get("histograms")
    dir.cd()
    h_sig = ROOT.TH2D(dir.Get("zz_sl_signal"))

    tf_bkg = ROOT.TFile.Open(FileName_bkg)
    dir = tf_bkg.Get("histograms")
    dir.cd()
    h_bkg = ROOT.TH2D(dir.Get("zz_background"))

    # base
    x_c_vec = np.arange(120,128+1,2)
    x_w_vec = np.arange(80,90+1,3)
    y_c_vec = np.arange(165,180+1,2)
    y_w_vec = np.arange(160,180+1,3)

    # # sig_efficiency 0.9 : Best Ellipse (121.0, 177.0, 82.0, 173.0): S_eff=0.9002, B_eff=0.6641, S/B=1.3556
    x_c_vec = np.arange(120,124+1,1)
    x_w_vec = np.arange(81,85+1,1)
    y_c_vec = np.arange(174,179+1,1)
    y_w_vec = np.arange(170,174+1,1)
    # x_c_vec = [121]; x_w_vec = [82]; y_c_vec = [177]; y_w_vec = [173]

    # # sig_efficiency 0.85 : Best Ellipse (113.0, 161.0, 62.0, 155.0): S_eff=0.8506, B_eff=0.5498, S/B=1.5472
    # x_c_vec = np.arange(111,115+1,1)
    # x_w_vec = np.arange(60,65+1,1)
    # y_c_vec = np.arange(158,162+1,1)
    # y_w_vec = np.arange(149,155+1,1)
    # x_c_vec = [113]; x_w_vec = [62]; y_c_vec = [161]; y_w_vec = [155]

    # # sig_efficiency 0.8 : Best Ellipse (105.0, 118.0, 51.0, 113.0): S_eff=0.8001 B_eff=0.4676 S/B=1.7108
    # x_c_vec = np.arange(102,108+1,1)
    # x_w_vec = np.arange(45,55+1,1)
    # y_c_vec = np.arange(115,120+1,1)
    # y_w_vec = np.arange(110,115+1,1)
    # x_c_vec = [105]; x_w_vec = [51]; y_c_vec = [118]; y_w_vec = [113]

    # # sig_efficiency 0.75 : Best Ellipse (103.0, 108.0, 45.0, 91.0): S_eff=0.7501, B_eff=0.3955, S/B=1.8965
    # x_c_vec = np.arange(102,106+1,1)
    # x_w_vec = np.arange(42,48+1,1)
    # y_c_vec = np.arange(105,110+1,1)
    # y_w_vec = np.arange(87,93+1,1)
    # x_c_vec = [103]; x_w_vec = [45]; y_c_vec = [108]; y_w_vec = [91]

    # # sig_efficiency 0.7 : Best Ellipse (101.0, 102.0, 38.0, 83.0): S_eff=0.7008 B_eff=0.3318 S/B=2.1120
    # x_c_vec = np.arange(96,102+1,1)
    # x_w_vec = np.arange(35,45+1,1)
    # y_c_vec = np.arange(100,104+1,1)
    # y_w_vec = np.arange(75,85+1,1)
    # x_c_vec = [101]; x_w_vec = [38]; y_c_vec = [102]; y_w_vec = [83]

    print(' ### INFO: Start looping')
    print(' x_c in :', x_c_vec)
    print(' y_c in :', y_c_vec)
    print(' x_w in :', x_w_vec)
    print(' y_w in :', y_w_vec)

    Max_SoB = 0
    Best_E = None
    for x_c in x_c_vec:
        for y_c in y_c_vec:
            for x_w in x_w_vec:
                for y_w in y_w_vec:
                    if y_c < y_w : continue
                    # print(x_c, y_c, x_w, y_w)
                    e = ROOT.TEllipse(x_c, y_c, x_w, y_w)
                    sig_efficiency = integrate_inside_ellipse(h_sig, e) / h_sig.Integral()
                    if sig_efficiency > sig_eff_thr:
                        bkg_efficiency = integrate_inside_ellipse(h_bkg, e) / h_bkg.Integral()
                        SoB = sig_efficiency/bkg_efficiency
                        if SoB > Max_SoB:
                            Max_SoB = SoB
                            Best_E = e
                            print("Best Ellipse ({}, {}, {}, {}): S_eff={:.4f}, B_eff={:.4f}, S/B={:.4f}".format(e.GetX1(), e.GetY1(), e.GetR1(), e.GetR2(), sig_efficiency, bkg_efficiency, SoB))
                            # e.SetLineWidth(2)

    print(' ### INFO: Plot ellipse')

    canvas = ROOT.TCanvas("canvas", "Histogram Canvas", 800, 600)
    canvas.cd()
    canvas.SetRightMargin(0.18)

    h_sig.SetTitle("ZZ Signal")
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
    legend.AddEntry(Best_E, "Ellipse {}% : (X,Y,R1,R2) = ({}, {}, {}, {})".format(int(sig_eff_thr*100), int(Best_E.GetX1()), int(Best_E.GetY1()), int(Best_E.GetR1()), int(Best_E.GetR2())), "l")
    legend.Draw()
    canvas.Update()
    canvas.SaveAs(odir + "/Best_ellipse{}_{}_{}_{}_{}.png".format(sig_eff_thr, int(Best_E.GetX1()), int(Best_E.GetY1()), int(Best_E.GetR1()), int(Best_E.GetR2())))
    canvas.SaveAs(odir + "/Best_ellipse{}_{}_{}_{}_{}.pdf".format(sig_eff_thr, int(Best_E.GetX1()), int(Best_E.GetY1()), int(Best_E.GetR1()), int(Best_E.GetR2())))
    # breakpoint()
    canvas.Close()

    # Plot backgground
    canvas = ROOT.TCanvas("canvas", "Histogram Canvas", 800, 600)
    canvas.cd()
    canvas.SetRightMargin(0.18)

    h_bkg.SetTitle("ZZ Sum of Backgrounds")
    h_bkg.Draw("COLZ")
    h_bkg.GetXaxis().SetTitle("m_{#tau#tau}^{SVfit} [GeV]")
    h_bkg.GetYaxis().SetTitle("m_{bb} [GeV]")
    h_bkg.GetZaxis().SetTitleOffset(1.5)
    h_bkg.SetMinimum(0.)
    Best_E.Draw("SAME")

    legend = ROOT.TLegend(0.4,0.83,0.82,0.9)
    legend.AddEntry(Best_E, "Ellipse {}% : (X,Y,R1,R2) = ({}, {}, {}, {})".format(int(sig_eff_thr*100), int(Best_E.GetX1()), int(Best_E.GetY1()), int(Best_E.GetR1()), int(Best_E.GetR2())), "l")
    legend.Draw()
    canvas.Update()
    canvas.SaveAs(odir + "/Best_ellipse{}_{}_{}_{}_{}_bkg.png".format(sig_eff_thr, int(Best_E.GetX1()), int(Best_E.GetY1()), int(Best_E.GetR1()), int(Best_E.GetR2())))
    canvas.SaveAs(odir + "/Best_ellipse{}_{}_{}_{}_{}_bkg.pdf".format(sig_eff_thr, int(Best_E.GetX1()), int(Best_E.GetY1()), int(Best_E.GetR1()), int(Best_E.GetR2())))
    canvas.Close()

    # Plot signal/backgground
    canvas = ROOT.TCanvas("canvas", "Histogram Canvas", 800, 600)
    canvas.cd()
    canvas.SetRightMargin(0.18)
    # h_sig.Scale(1.)
    # h_bkg.Scale(1.)
    h_ratio = h_sig.Clone("h_ratio")
    h_ratio.Divide(h_bkg)
    h_ratio.Draw("COLZ")
    h_ratio.GetXaxis().SetTitle("m_{#tau#tau}^{SVfit} [GeV]")
    h_ratio.GetYaxis().SetTitle("m_{bb} [GeV]")
    h_ratio.GetZaxis().SetTitleOffset(1.5)
    h_ratio.GetZaxis().SetTitle("S/B ratio")
    h_ratio.SetMinimum(0.)
    # h_ratio.SetMaximum(0.01)
    h_ratio.SetTitle("ZZ S/B")
    Best_E.Draw("SAME")

    legend = ROOT.TLegend(0.4,0.83,0.82,0.9)
    legend.AddEntry(Best_E, "Ellipse {}% : (X,Y,R1,R2) = ({}, {}, {}, {})".format(int(sig_eff_thr*100), int(Best_E.GetX1()), int(Best_E.GetY1()), int(Best_E.GetR1()), int(Best_E.GetR2())), "l")
    legend.Draw()
    canvas.Update()
    canvas.SaveAs(odir + "/Best_ellipse{}_{}_{}_{}_{}_SoB.png".format(sig_eff_thr, int(Best_E.GetX1()), int(Best_E.GetY1()), int(Best_E.GetR1()), int(Best_E.GetR2())))
    canvas.SaveAs(odir + "/Best_ellipse{}_{}_{}_{}_{}_SoB.pdf".format(sig_eff_thr, int(Best_E.GetX1()), int(Best_E.GetY1()), int(Best_E.GetR1()), int(Best_E.GetR2())))
    canvas.Close()

    # # firts 
    # for x_c in [88,90,92,94,96,98,100,102,104]:
    #     for y_c in [88,90,92,94,96,98,100,102,104]:
    #         for x_w in [30,40,50,60,70,80,90,100,110]:
    #             for y_w in [30,40,50,60,70,80,90,100,110]:

    # # second
    # for x_c in [88,90,92,94,96,98,100,102,104]:
    #     for y_c in [88,90,92,94,96,98,100,102,104]:
    #         for x_w in [40,45,50,55,60,65,70]:
    #             for y_w in [70,75,80,85,90,95,100,110]:

    # third
    # for x_c in [96,97,98,99,100]:
    #     for y_c in [100,101,102,103,104]:
    #         for x_w in [35,36,37,38,39,40,41,42,43,44,45]:
    #             for y_w in [95,96,97,98,99,100,101,102,103,104,105]: