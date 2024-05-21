# Optimization of elliptical cut for ZZ->bbtautau analysis
# version with ellipse centered on highest signal point

############# opt ellipse CENTERED
python3 OptimizeEllipse_centered.py \
 --sig /grid_mnt/data__data.polcms/cms/vernazza/cmt/FeaturePlot2D/ul_2018_ZZ_v10/cat_base/prod_240208/root/Ztt_svfit_mass_ellipse_Zbb_mass_ellipse__pg_zz_sig_vs_bkg__nodata.root \
 --hSig zz_sl_signal \
  --bkg /grid_mnt/data__data.polcms/cms/vernazza/cmt/FeaturePlot2D/ul_2018_ZZ_v10/cat_base/prod_240208/root/Ztt_svfit_mass_ellipse_Zbb_mass_ellipse__pg_zz_sig_vs_bkg__nodata.root \
 --hBkg all_background \
 --outdir zz

