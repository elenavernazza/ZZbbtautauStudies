import ROOT, os, sys
import matplotlib.cm

# python3 PlotEllipseZZ.py --in /eos/user/e/evernazz/cmt/FeaturePlot2D/ul_2018_v10/cat_mutau/prod_0524_3/root/Htt_mass_Hbb_mass__mutau_os_iso__pg_zz_signal__nodata.root
# python3 PlotEllipseZZ.py --in /eos/user/e/evernazz/cmt/FeaturePlot2D/ul_2018_v10/cat_mutau/prod_0524_2/root/Htt_svfit_mass_Hbb_mass__mutau_os_iso__pg_zz_signal__nodata.root
# python3 PlotEllipseZZ.py --in /eos/user/e/evernazz/cmt/FeaturePlot2D/ul_2018_v10/cat_mutau/prod_0524_3/root/Htt_mass_Hbb_mass__mutau_os_iso__pg_zz_background__nodata.root
# python3 PlotEllipseZZ.py --in /eos/user/e/evernazz/cmt/FeaturePlot2D/ul_2018_v10/cat_mutau/prod_0524_2/root/Htt_svfit_mass_Hbb_mass__mutau_os_iso__pg_zz_background__nodata.root

# python3 PlotEllipseZZ.py --in /eos/user/e/evernazz/cmt/FeaturePlot2D/ul_2018_ZZ_v10/cat_base/prod_0608/root/Htt_svfit_mass_Hbb_mass__pg_zz_background__nodata.root --outdir EllipsePlots/all_base
# python3 PlotEllipseZZ.py --in /eos/user/e/evernazz/cmt/FeaturePlot2D/ul_2018_ZZ_v10/cat_base/prod_0608/root/Htt_svfit_mass_Hbb_mass__pg_zz_signal__nodata.root --outdir EllipsePlots/all_base
# python3 PlotEllipseZZ.py --in /eos/user/e/evernazz/cmt/FeaturePlot2D/ul_2018_ZZ_v10/cat_base/prod_0608/root/Htt_svfit_mass_Hbb_mass__pg_zz_background__nodata.root --outdir EllipsePlots/all_base --add_HH
# python3 PlotEllipseZZ.py --in /eos/user/e/evernazz/cmt/FeaturePlot2D/ul_2018_ZZ_v10/cat_base/prod_0608/root/Htt_svfit_mass_Hbb_mass__pg_zz_signal__nodata.root --outdir EllipsePlots/all_base --add_HH

def CanvasCreator(dims, margins=0.11):
    if len(dims) == 2: canvas = ROOT.TCanvas( "c", "c", dims[0], dims[1] )
    elif len(dims) == 4: canvas = ROOT.TCanvas( "c", "c", dims[0], dims[1], dims[2], dims[3] )
    else: sys.exit("[ERROR] dims argument (1) either list of len 2 or 4")

    # canvOptions = {"SetTitle": "", "SetGrid": True}
    # for opt in canvOptions.keys():
    #     getattr(canvas, opt)(canvOptions[opt])

    ROOT.gPad.SetRightMargin(margins)
    ROOT.gPad.SetLeftMargin(margins)
    ROOT.gPad.SetBottomMargin(margins)
    ROOT.gPad.SetTopMargin(margins)
    ROOT.gPad.SetFrameLineWidth(3)

    canvas.Update()
    return canvas


if __name__ == "__main__" :

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--view",      dest="view",         help="Display canvas",      default=False,           action='store_true'  )
    parser.add_option("--in",        dest="infile",       help="Input root file",     default=None                                  )
    parser.add_option("--outdir",    dest="outdir",       help="Output directory",    default='./EllipsePlots'                      )
    parser.add_option("--ellipse",   dest="ellipse",      help="Draw ellipse",        default=False,            action='store_true' )
    parser.add_option("--add_HH",    dest="add_HH",       help="Draw HH ellipse",     default=False,            action='store_true' )
    (options, args) = parser.parse_args()
    print(options)

    if not options.view:
        ROOT.gROOT.SetBatch(True)

    odir = options.outdir
    FileName = options.infile    

    if "background" in FileName:
            HistoName = "zz_background"
            title = "Backgrounds"
            set_max = 0.001
    elif "signal" in FileName:
            HistoName = "zz_sl_signal"
            title = "Signal (ZZ #rightarrow bb#tau#tau)"
    Features = FileName.split("/root/")[1].split(".root")[0]
    if "svfit" in Features:
            x_title = "m_{#tau#tau}^{SVfit} [GeV]"
    else:
            x_title = "m_{#tau#tau} [GeV]"

    tf = ROOT.TFile.Open(FileName)
    directory = tf.Get("histograms")
    directory.cd()
    histogram = ROOT.TH2D(directory.Get(HistoName))

    canvas = ROOT.TCanvas("canvas", "Histogram Canvas", 800, 600)
    canvas.cd()
    canvas.SetRightMargin(0.18)
    histogram.Draw("COLZ")

    histogram.GetXaxis().SetTitle(x_title)
    histogram.GetYaxis().SetTitle("m_{bb} [GeV]")
    histogram.GetZaxis().SetTitleOffset(1.5)
    histogram.SetTitle("")
    histogram.SetMinimum(0)

    ellipse = ""
    if options.ellipse:
        ellipse = "_ellipse"

        # Best Ellipse (101.0, 102.0, 38.0, 83.0): S_eff=0.7008 B_eff=0.3318 S/B=2.1120
        e_ZZ_70 = ROOT.TEllipse(101.0, 102.0, 38.0, 83.0)
        e_ZZ_70.SetFillStyle(0)
        e_ZZ_70.SetFillColorAlpha(0, 0)
        e_ZZ_70.SetLineColor(ROOT.kMagenta)
        e_ZZ_70.SetLineWidth(2)
        e_ZZ_70.Draw("SAME")

        # Best Ellipse (103.0, 108.0, 45.0, 91.0): S_eff=0.7501, B_eff=0.3955, S/B=1.8965
        e_ZZ_75 = ROOT.TEllipse(103.0, 108.0, 45.0, 91.0)
        e_ZZ_75.SetFillStyle(0)
        e_ZZ_75.SetFillColorAlpha(0, 0)
        e_ZZ_75.SetLineColor(ROOT.kRed)
        e_ZZ_75.SetLineWidth(2)
        e_ZZ_75.Draw("SAME")

        # Best Ellipse (105.0, 118.0, 51.0, 113.0): S_eff=0.8001 B_eff=0.4676 S/B=1.7108
        e_ZZ_80 = ROOT.TEllipse(105.0, 118.0, 51.0, 113.0)
        e_ZZ_80.SetFillStyle(0)
        e_ZZ_80.SetFillColorAlpha(0, 0)
        e_ZZ_80.SetLineColor(ROOT.kOrange+1)
        e_ZZ_80.SetLineWidth(2)
        e_ZZ_80.Draw("SAME")

        # Best Ellipse (113.0, 161.0, 62.0, 155.0): S_eff=0.8506, B_eff=0.5498, S/B=1.5472
        e_ZZ_85 = ROOT.TEllipse(113.0, 161.0, 62.0, 155.0)
        e_ZZ_85.SetFillStyle(0)
        e_ZZ_85.SetFillColorAlpha(0, 0)
        e_ZZ_85.SetLineColor(ROOT.kYellow)
        e_ZZ_85.SetLineWidth(2)
        e_ZZ_85.Draw("SAME")

        # Best Ellipse (121.0, 177.0, 82.0, 173.0): S_eff=0.9002, B_eff=0.6641, S/B=1.3556
        e_ZZ_90 = ROOT.TEllipse(121.0, 177.0, 82.0, 173.0)
        e_ZZ_90.SetFillStyle(0)
        e_ZZ_90.SetFillColorAlpha(0, 0)
        e_ZZ_90.SetLineColor(ROOT.kGreen)
        e_ZZ_90.SetLineWidth(2)
        e_ZZ_90.Draw("SAME")

        legend = ROOT.TLegend(0.35,0.7,0.82,0.9)
        legend.AddEntry(e_ZZ_70, "Ellipse E=70% S/B = 2.1120: (X,Y,R1,R2) = ({}, {}, {}, {})".format(101, 102, 38, 83), "l")
        legend.AddEntry(e_ZZ_75, "Ellipse E=75% S/B = 1.8965: (X,Y,R1,R2) = ({}, {}, {}, {})".format(103, 108, 45, 91), "l")
        legend.AddEntry(e_ZZ_80, "Ellipse E=80% S/B = 1.7108: (X,Y,R1,R2) = ({}, {}, {}, {})".format(105, 118, 51, 113), "l")
        legend.AddEntry(e_ZZ_85, "Ellipse E=85% S/B = 1.5472: (X,Y,R1,R2) = ({}, {}, {}, {})".format(113, 161, 62, 155), "l")
        legend.AddEntry(e_ZZ_90, "Ellipse E=90% S/B = 1.3556: (X,Y,R1,R2) = ({}, {}, {}, {})".format(121, 177, 82, 173), "l")
        legend.Draw()

    t1 = ROOT.TLatex(0.11, 0.91, "#scale[1.5]{CMS} Private work")
    t1.SetTextSize(0.03)
    t1.SetNDC(True)
    t1.Draw("SAME")

    t2 = ROOT.TLatex(0.6, 0.91, "2018, (13 TeV) 59.7 fb^{-1}")
    t2.SetTextSize(0.03)
    t2.SetNDC(True)
    t2.Draw("SAME")

    canvas.Update()

    os.system("mkdir -p " + odir)
    canvas.SaveAs(odir + "/{}_{}{}.png".format(HistoName, Features, ellipse))
    canvas.SaveAs(odir + "/{}_{}{}.pdf".format(HistoName, Features, ellipse))

    if options.add_HH:

        canvas = ROOT.TCanvas("canvas", "Histogram Canvas", 800, 600)
        canvas.cd()
        canvas.SetRightMargin(0.18)
        histogram.Draw("COLZ")

        histogram.GetXaxis().SetTitle(x_title)
        histogram.GetYaxis().SetTitle("m_{bb} [GeV]")
        histogram.GetZaxis().SetTitleOffset(1.5)
        histogram.SetTitle("")
        histogram.SetMinimum(0)

        if options.view:
            breakpoint()

        # ZZ
        # Best Ellipse (105.0, 118.0, 51.0, 113.0): S_eff=0.8001 B_eff=0.4676 S/B=1.7108
        e_ZZ_80 = ROOT.TEllipse(105.0, 118.0, 51.0, 113.0)
        e_ZZ_80.SetFillStyle(0)
        e_ZZ_80.SetFillColorAlpha(0, 0)
        e_ZZ_80.SetLineColor(ROOT.kGreen)
        e_ZZ_80.SetLineWidth(2)
        e_ZZ_80.Draw("SAME")

        # HH
        e_HH_90 = ROOT.TEllipse(129.0, 169.0, 53.0, 145.0)
        e_HH_90.SetFillStyle(0)
        e_HH_90.SetFillColorAlpha(0, 0)
        e_HH_90.SetLineColor(ROOT.kOrange+1)
        e_HH_90.SetLineWidth(2)
        e_HH_90.Draw("SAME")

        legend = ROOT.TLegend(0.4,0.75,0.81,0.89)
        legend.SetHeader(f"{title} : Elliptical Mass Cut (X, Y, R1, R2)","C")
        legend.AddEntry(e_ZZ_80, "ZZ (80% eff.) : ({}, {}, {}, {}) [GeV]".format(105, 118, 51, 113), "l")
        legend.AddEntry(e_HH_90, "HH (90% eff.) : ({}, {}, {}, {}) [GeV]".format(129, 169, 53, 145), "l")
        legend.Draw()
        legend.SetTextSize(0.025)
        header = legend.GetListOfPrimitives().First()
        header.SetTextSize(0.025)

        t1 = ROOT.TLatex(0.11, 0.91, "#scale[1.5]{CMS} Private work")
        t1.SetTextSize(0.03)
        t1.SetNDC(True)
        t1.Draw("SAME")

        t2 = ROOT.TLatex(0.6, 0.91, "2018, (13 TeV) 59.7 fb^{-1}")
        t2.SetTextSize(0.03)
        t2.SetNDC(True)
        t2.Draw("SAME")

        canvas.Update()

        os.system("mkdir -p " + odir)
        canvas.SaveAs(odir + "/{}_{}_ZZvsHH.png".format(HistoName, Features))
        canvas.SaveAs(odir + "/{}_{}_ZZvsHH.pdf".format(HistoName, Features))