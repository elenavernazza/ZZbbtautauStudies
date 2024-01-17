import ROOT, os

# # Signal
# type = "signal"
# HistoName = "zz_sl_signal"
# title = "ZZ Signal"
# x_title = "m_{#tau#tau}^{SVfit} [GeV]"
# base_dir = "/eos/user/e/evernazz/cmt/FeaturePlot2D/ul_2018_ZZ_v10/"
# f_etau = base_dir + "/cat_etau/prod_0608/root/Htt_svfit_mass_Hbb_mass__etau_os_iso__pg_zz_signal__nodata.root"
# f_mutau = base_dir + "/cat_mutau/prod_0608/root/Htt_svfit_mass_Hbb_mass__mutau_os_iso__pg_zz_signal__nodata.root"
# f_tautau = base_dir + "/cat_tautau/prod_0608/root/Htt_svfit_mass_Hbb_mass__tautau_os_iso__pg_zz_signal__nodata.root"

# Background
type = "background"
HistoName = "zz_background"
title = "Sum of Background"
x_title = "m_{#tau#tau}^{SVfit} [GeV]"
base_dir = "/eos/user/e/evernazz/cmt/FeaturePlot2D/ul_2018_ZZ_v10/"
f_etau = base_dir + "cat_etau/prod_0608/root/Htt_svfit_mass_Hbb_mass__etau_os_iso__pg_zz_background__nodata.root"
f_mutau = base_dir + "cat_mutau/prod_0608/root/Htt_svfit_mass_Hbb_mass__mutau_os_iso__pg_zz_background__nodata.root"
f_tautau = base_dir + "cat_tautau/prod_0608/root/Htt_svfit_mass_Hbb_mass__tautau_os_iso__pg_zz_background__nodata.root"

Features = f_etau.split("/root/")[1].split("__etau")[0]

tf_etau = ROOT.TFile.Open(f_etau)
directory = tf_etau.Get("histograms")
directory.cd()
h_etau = ROOT.TH2D(directory.Get(HistoName))

tf_mutau = ROOT.TFile.Open(f_mutau)
directory = tf_mutau.Get("histograms")
directory.cd()
h_mutau = ROOT.TH2D(directory.Get(HistoName))

tf_tautau = ROOT.TFile.Open(f_tautau)
directory = tf_tautau.Get("histograms")
directory.cd()
h_tautau = ROOT.TH2D(directory.Get(HistoName))

h_dummy = ROOT.TH2D("dummy", "dummy", 70, 0, 350, 100, 0, 500)
h_dummy.SetStats(0)

h_all = ROOT.THStack("h_all", "")
h_all.Add(h_etau)
h_all.Add(h_mutau)
h_all.Add(h_tautau)

print(h_etau.Integral(), h_mutau.Integral(), h_tautau.Integral())

canvas = ROOT.TCanvas("canvas", "Canvas", 800, 600)
canvas.cd()
canvas.SetRightMargin(0.18)
h_dummy.Draw()
h_all.Draw("SAME COLZ")

# Original ellipse for HH
x_bb_c = 129.
y_tt_c = 169.
x_bb_w = 53.
y_tt_w = 145.
ellipse_HH = ROOT.TEllipse(x_bb_c, y_tt_c, x_bb_w, y_tt_w)
ellipse_HH.SetFillStyle(0)
ellipse_HH.SetFillColorAlpha(0, 0)
ellipse_HH.SetLineColor(ROOT.kRed)
# ellipse_HH.Draw("SAME")

x_bb_c = 91.
y_tt_c = 91.
x_bb_w = 53.
y_tt_w = 145.
ellipse_ZZ = ROOT.TEllipse(x_bb_c, y_tt_c, x_bb_w, y_tt_w)
ellipse_ZZ.SetFillStyle(0)
ellipse_ZZ.SetFillColorAlpha(0, 0)
ellipse_ZZ.SetLineColor(ROOT.kGreen)
# ellipse_ZZ.Draw("SAME")

h_dummy.GetXaxis().SetTitle(x_title)
h_dummy.GetYaxis().SetTitle("m_{bb} [GeV]")
h_dummy.GetZaxis().SetTitle("Events")
# h_dummy.GetZaxis().SetTitleOffset(1.5)
h_dummy.SetMaximum(0.3*h_all.GetMaximum())
h_dummy.SetTitle(title)

# canvas.Update()

os.system("mkdir -p EllipsePlots")
canvas.SaveAs("EllipsePlots/{}_all_{}.png".format(HistoName, Features))
canvas.SaveAs("EllipsePlots/{}_all_{}.pdf".format(HistoName, Features))