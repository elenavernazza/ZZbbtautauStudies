# Optimization of elliptical cut for ZH->bbtautau analysis

#### With non-negative ellipse bound
# Ztt_hbb
# Best Ellipse (93.0, 172.0, 37.0, 164.0): S_eff=0.8009, B_eff=0.3313, S/sqrt(B)=1.3914
python3 OptimizeEllipseZZ.py \
 --sig /grid_mnt/data__data.polcms/cms/cuisset/cmt/FeaturePlot2D/ul_2018_ZH_v10/cat_base/prod_231222/root/Ztt_svfit_mass_ellipse_Zbb_mass_ellipse__pg_zh_sig_vs_bkg__nodata.root \
 --hSig zh_ztt_hbb_sl_signal \
 --bkg /grid_mnt/data__data.polcms/cms/cuisset/cmt/FeaturePlot2D/ul_2018_ZH_v10/cat_base/prod_231222/root/Ztt_svfit_mass_ellipse_Zbb_mass_ellipse__pg_zh_sig_vs_bkg__nodata.root \
 --hBkg zz_background \
 --outdir ztt_hbb

#Best Ellipse (100.0, 189.0, 64.0, 187.0): S_eff=0.9000, B_eff=0.5304, S/sqrt(B)=1.2358
python3 OptimizeEllipseZZ.py \
 --sig /grid_mnt/data__data.polcms/cms/cuisset/cmt/FeaturePlot2D/ul_2018_ZH_v10/cat_base/prod_231222/root/Ztt_svfit_mass_ellipse_Zbb_mass_ellipse__pg_zh_sig_vs_bkg__nodata.root \
 --hSig zh_ztt_hbb_sl_signal \
 --bkg /grid_mnt/data__data.polcms/cms/cuisset/cmt/FeaturePlot2D/ul_2018_ZH_v10/cat_base/prod_231222/root/Ztt_svfit_mass_ellipse_Zbb_mass_ellipse__pg_zh_sig_vs_bkg__nodata.root \
 --hBkg zz_background \
 --outdir ztt_hbb --eff 0.9

# Zbb_htt
# Best Ellipse (140.0, 82.0, 57.0, 66.0): S_eff=0.8019, B_eff=0.3956, S/sqrt(B)=1.2751
python3 OptimizeEllipseZZ.py \
 --sig /grid_mnt/data__data.polcms/cms/cuisset/cmt/FeaturePlot2D/ul_2018_ZH_v10/cat_base/prod_231222/root/Ztt_svfit_mass_ellipse_Zbb_mass_ellipse__pg_zh_sig_vs_bkg__nodata.root \
 --hSig zh_zbb_htt_sl_signal \
 --bkg /grid_mnt/data__data.polcms/cms/cuisset/cmt/FeaturePlot2D/ul_2018_ZH_v10/cat_base/prod_231222/root/Ztt_svfit_mass_ellipse_Zbb_mass_ellipse__pg_zh_sig_vs_bkg__nodata.root \
 --hBkg zz_background \
 --outdir zbb_htt


# Best Ellipse Best Ellipse (158.0, 118.0, 83.0, 118.0): S_eff=0.9003, B_eff=0.5991, S/sqrt(B)=1.1632
python3 OptimizeEllipseZZ.py \
 --sig /grid_mnt/data__data.polcms/cms/cuisset/cmt/FeaturePlot2D/ul_2018_ZH_v10/cat_base/prod_231222/root/Ztt_svfit_mass_ellipse_Zbb_mass_ellipse__pg_zh_sig_vs_bkg__nodata.root \
 --hSig zh_zbb_htt_sl_signal \
 --bkg /grid_mnt/data__data.polcms/cms/cuisset/cmt/FeaturePlot2D/ul_2018_ZH_v10/cat_base/prod_231222/root/Ztt_svfit_mass_ellipse_Zbb_mass_ellipse__pg_zh_sig_vs_bkg__nodata.root \
 --hBkg zz_background \
 --outdir zbb_htt --eff 0.9

 ############## Without non-negative ellipse bound
python3 OptimizeEllipseZZ.py \
    --sig /grid_mnt/data__data.polcms/cms/cuisset/cmt/FeaturePlot2D/ul_2018_ZH_v10/cat_base/prod_231222/root/Ztt_svfit_mass_ellipse_Zbb_mass_ellipse__pg_zh_sig_vs_bkg__nodata.root \
    --hSig zh_ztt_hbb_sl_signal \
    --bkg /grid_mnt/data__data.polcms/cms/cuisset/cmt/FeaturePlot2D/ul_2018_ZH_v10/cat_base/prod_231222/root/Ztt_svfit_mass_ellipse_Zbb_mass_ellipse__pg_zh_sig_vs_bkg__nodata.root \
    --hBkg zz_background \
    --outdir ztt_hbb_nobound --scan wide --optimizer multiprocess_grid

python3 OptimizeEllipseZZ.py \
 --sig /grid_mnt/data__data.polcms/cms/cuisset/cmt/FeaturePlot2D/ul_2018_ZH_v10/cat_base/prod_231222/root/Ztt_svfit_mass_ellipse_Zbb_mass_ellipse__pg_zh_sig_vs_bkg__nodata.root \
 --hSig zh_zbb_htt_sl_signal \
 --bkg /grid_mnt/data__data.polcms/cms/cuisset/cmt/FeaturePlot2D/ul_2018_ZH_v10/cat_base/prod_231222/root/Ztt_svfit_mass_ellipse_Zbb_mass_ellipse__pg_zh_sig_vs_bkg__nodata.root \
 --hBkg zz_background \
 --outdir zbb_htt_nobound --scan wide --optimizer multiprocess_grid



#######################################################
############# opt ellipse CENTERED
python3 OptimizeEllipse_centered.py \
 --sig /grid_mnt/data__data.polcms/cms/cuisset/cmt/FeaturePlot2D/ul_2018_ZH_v10/cat_base/prod_231222/root/Ztt_svfit_mass_ellipse_Zbb_mass_ellipse__pg_zh_sig_vs_bkg__nodata.root \
 --hSig zh_zbb_htt_sl_signal \
  --bkg /grid_mnt/data__data.polcms/cms/cuisset/cmt/FeaturePlot2D/ul_2018_ZH_v10/cat_base/prod_231222/root/Ztt_svfit_mass_ellipse_Zbb_mass_ellipse__pg_zh_sig_vs_bkg__nodata.root \
 --hBkg zz_background \
 --outdir zbb_htt_centered

python3 OptimizeEllipse_centered.py \
 --sig /grid_mnt/data__data.polcms/cms/cuisset/cmt/FeaturePlot2D/ul_2018_ZH_v10/cat_base/prod_231222/root/Ztt_svfit_mass_ellipse_Zbb_mass_ellipse__pg_zh_sig_vs_bkg__nodata.root \
 --hSig zh_ztt_hbb_sl_signal \
  --bkg /grid_mnt/data__data.polcms/cms/cuisset/cmt/FeaturePlot2D/ul_2018_ZH_v10/cat_base/prod_231222/root/Ztt_svfit_mass_ellipse_Zbb_mass_ellipse__pg_zh_sig_vs_bkg__nodata.root \
 --hBkg zz_background \
 --outdir ztt_hbb_centered