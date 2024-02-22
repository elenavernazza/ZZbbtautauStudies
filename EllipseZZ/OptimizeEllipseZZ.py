import ROOT, os, math
import numpy as np
import scipy.optimize
import sys
from concurrent.futures import ProcessPoolExecutor
import itertools

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

def sob_fct_forThreads(opt_x, sig_eff_thr):
    #print(opt_x)
    x_c, y_c, x_w, y_w = opt_x
    e = ROOT.TEllipse(x_c, y_c, x_w, y_w)
    sig_efficiency = integrate_inside_ellipse(h_sig, e) / h_sig.Integral()
    #print((sig_efficiency, sig_eff_thr))
    if sig_efficiency <= sig_eff_thr:
        return None
    bkg_efficiency = integrate_inside_ellipse(h_bkg, e) / h_bkg.Integral()
    return sig_efficiency/max(math.sqrt(bkg_efficiency), sys.float_info.epsilon)

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
    parser.add_option("--hSig",      dest="signalHist",   help="Name of the histogram for signal", default="zz_sl_signal")
    parser.add_option("--bkg",       dest="background",   help="Input background root file", default=None                                  )
    parser.add_option("--hBkg",      dest="backgroundHist",   help="Name of the histogram for background", default="zz_background")
    parser.add_option("--outdir",    dest="outdir",       help="Output directory",           default='./EllipsePlots'                      )
    parser.add_option("--eff",       dest="efficiency",   help="Signal efficiency",          default=0.8                                   )
    parser.add_option("--scan",      dest="scan",         help="Scan type (wide/fine)",      default="fine")
    parser.add_option("--optimizer", dest="optimizer", help="Optimizer type : grid or scipy or multiprocess_grid", default="grid")
    parser.add_option("--constrainNonNegative", dest="constrainNonNegative", help="Constrain ellipse so it does not overlap with negative mass regions", default=False, action="store_true")
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
    h_sig = ROOT.TH2D(dir.Get(options.signalHist))

    tf_bkg = ROOT.TFile.Open(FileName_bkg)
    dir = tf_bkg.Get("histograms")
    dir.cd()
    h_bkg = ROOT.TH2D(dir.Get("zz_background"))

    # base
    x_c_vec = np.arange(80,110+1,7)
    x_w_vec = np.arange(50,100+1,10)
    y_c_vec = np.arange(100,180+1,8)
    y_w_vec = np.arange(100,180+1,10)
    
    if options.signalHist == "zh_ztt_hbb_sl_signal":
        ################## Ztt_hbb
        if options.scan == "wide":
            x_c_vec = np.arange(70,110+1,4)
            x_w_vec = np.arange(20,100+1,5)
            y_c_vec = np.arange(70,240+1,5)
            y_w_vec = np.arange(60,230+1,5)
        
        elif options.scan == "fine":
            if options.efficiency == 0.8:
                # sig_efficiency 0.8
                if options.constrainNonNegative:
                    x_c_vec = np.arange(90,95+1,1)
                    x_w_vec = np.arange(35,45+1,1)
                    y_c_vec = np.arange(170,180+1,1)
                    y_w_vec = np.arange(155,170+1,1)
                else:
                    x_c_vec = np.arange(85,95+1,1)
                    x_w_vec = np.arange(35,50+1,1)
                    y_c_vec = np.arange(175,245+1,3)
                    y_w_vec = np.arange(155,220+1,3)

            elif options.efficiency == 0.9:
                if options.constrainNonNegative:
                    # sig eff 0.9
                    x_c_vec = np.arange(88,105+1,1)
                    x_w_vec = np.arange(62,75+1,1)
                    y_c_vec = np.arange(180,205+1,1)
                    y_w_vec = np.arange(175,189+1,1)

    if options.signalHist == "zh_zbb_htt_sl_signal":
        ################## Zbb_htt
        if options.scan == "wide":
            x_c_vec = np.arange(70,160+1,4)
            x_w_vec = np.arange(20,100+1,5)
            y_c_vec = np.arange(60,150+1,5)
            y_w_vec = np.arange(40,150+1,5)
        
        elif options.scan == "fine":
            if options.efficiency == 0.8:
                # # sig_efficiency 0.8 
                x_c_vec = np.arange(135,145+1,1)
                x_w_vec = np.arange(50,65+1,1)
                y_c_vec = np.arange(75,90+1,1)
                y_w_vec = np.arange(60,75+1,1)
            elif options.efficiency == 0.9:
                # sig_efficiency 0.9
                x_c_vec = np.arange(155,165+1,1)
                x_w_vec = np.arange(80,90+1,1)
                y_c_vec = np.arange(110,120+1,1)
                y_w_vec = np.arange(110,125+1,1)

    print(' ### INFO: Start looping')
    print(' x_c in :', x_c_vec)
    print(' y_c in :', y_c_vec)
    print(' x_w in :', x_w_vec)
    print(' y_w in :', y_w_vec)

    if options.optimizer == "scipy":
        raise RuntimeError("Scipy optimizer does not work (yet)")
        start_point = (140, 80, 60, 60)
        def sob_fct(opt_x):
            x_c, y_c, x_w, y_w = opt_x
            e = ROOT.TEllipse(x_c, y_c, x_w, y_w)
            sig_efficiency = integrate_inside_ellipse(h_sig, e) / h_sig.Integral()
            bkg_efficiency = integrate_inside_ellipse(h_bkg, e) / h_bkg.Integral()
            return sig_efficiency/max(math.sqrt(bkg_efficiency), sys.float_info.epsilon)

        def sig_eff_constraint(opt_x):
            x_c, y_c, x_w, y_w = opt_x
            e = ROOT.TEllipse(x_c, y_c, x_w, y_w)
            return integrate_inside_ellipse(h_sig, e) / h_sig.Integral() - sig_eff_thr

        constraint = ({'type': 'ineq', 'fun': sig_eff_constraint})
        # cobyla and SLSQP from minimize do not work correctly due to flat regions in function
        fit_res = scipy.optimize.minimize(sob_fct, start_point, method="SLSQP", options=dict(disp=True))
        print(fit_res)

        Best_E = ROOT.TEllipse(*fit_res.x)
        print("Best Ellipse ({}, {}, {}, {}): S_eff={:.4f}, B_eff={:.4f}, S/sqrt(B)={:.4f}".format(Best_E.GetX1(), Best_E.GetY1(), Best_E.GetR1(), Best_E.GetR2(),
                                sig_eff_constraint(fit_res.x), integrate_inside_ellipse(h_bkg, Best_E) / h_bkg.Integral(), sob_fct(fit_res.x)))

    elif options.optimizer == "multiprocess_grid":
        if options.constrainNonNegative:
            raise RuntimeError("constrainNonNegative and multiprocess_grid are not compatible")
        with ProcessPoolExecutor(max_workers=20) as executor:
            grid_result = executor.map(sob_fct_forThreads, itertools.product(x_c_vec, y_c_vec, x_w_vec, y_w_vec), itertools.repeat(sig_eff_thr), chunksize=20)
            Max_SoB = 0
            best_input = None
            for input_val, SoB in zip(itertools.product(x_c_vec, y_c_vec, x_w_vec, y_w_vec), grid_result):
                if SoB is not None and SoB >= Max_SoB:
                    if SoB == Max_SoB: 
                        best_input.append(input_val)
                    else:
                        best_input = [input_val]
                    Max_SoB = SoB
        if Max_SoB is None:
            raise RuntimeError("Did not find any ellipse matching signal efficiency")
        print(best_input)
        Best_E = ROOT.TEllipse(*best_input[0])
        print("Best Ellipse ({}, {}, {}, {}): S_eff={:.4f}, B_eff={:.4f}, S/sqrt(B)={:.4f}".format(Best_E.GetX1(), Best_E.GetY1(), Best_E.GetR1(), Best_E.GetR2(),
                                integrate_inside_ellipse(h_sig, Best_E) / h_sig.Integral(), integrate_inside_ellipse(h_bkg, Best_E) / h_bkg.Integral(), Max_SoB))
    
    elif options.optimizer == "grid":
        Max_SoB = 0
        Best_E = None
        for x_c in x_c_vec:
            for y_c in y_c_vec:
                for x_w in x_w_vec:
                    for y_w in y_w_vec:
                        if options.constrainNonNegative and y_c < y_w : continue # prevent ellipse holding negative values. Removed now
                        # print(x_c, y_c, x_w, y_w)
                        e = ROOT.TEllipse(x_c, y_c, x_w, y_w)
                        sig_efficiency = integrate_inside_ellipse(h_sig, e) / h_sig.Integral()
                        if sig_efficiency > sig_eff_thr:
                            bkg_efficiency = integrate_inside_ellipse(h_bkg, e) / h_bkg.Integral()
                            SoB = sig_efficiency/math.sqrt(bkg_efficiency)
                            if SoB > Max_SoB:
                                Max_SoB = SoB
                                Best_E = e
                                print("Best Ellipse ({}, {}, {}, {}): S_eff={:.4f}, B_eff={:.4f}, S/sqrt(B)={:.4f}".format(e.GetX1(), e.GetY1(), e.GetR1(), e.GetR2(), sig_efficiency, bkg_efficiency, SoB))
                                # e.SetLineWidth(2)
    else:
        raise RuntimeError("Invalid parameter optimizer " + args.optimizer)

    print(' ### INFO: Plot ellipse')

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

    h_bkg.SetTitle("ZH Sum of Backgrounds")
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
    h_sqrtBkg = h_bkg.Clone("h_sqrtBkg")
    for bin in range(h_sqrtBkg.GetNcells()+1):
        try:
            h_sqrtBkg.SetBinContent(bin, math.sqrt(h_sqrtBkg.GetBinContent(bin)))
        except ValueError:
            h_sqrtBkg.SetBinContent(bin, 0)
    h_ratio.Divide(h_sqrtBkg)
    h_ratio.Draw("COLZ")
    h_ratio.GetXaxis().SetTitle("m_{#tau#tau}^{SVfit} [GeV]")
    h_ratio.GetYaxis().SetTitle("m_{bb} [GeV]")
    h_ratio.GetZaxis().SetTitleOffset(1.5)
    h_ratio.GetZaxis().SetTitle("S/sqrt(B) ratio")
    h_ratio.SetMinimum(0.)
    h_ratio.SetMaximum(0.04)
    h_ratio.SetTitle("ZH S/sqrt(B)")
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