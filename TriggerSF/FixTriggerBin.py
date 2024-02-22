import ROOT, os

input_file = '/grid_mnt/data__data.polcms/cms/vernazza/FrameworkNanoAOD/hhbbtt-analysis' \
             '/nanoaod_base_analysis/data/cmssw/CMSSW_12_3_0_pre6/src/HTT-utilities/trigSFs_UL_eleMu' \
             '/sf_el_2016post_HLTEle25.root'

input_file_fix = '/grid_mnt/data__data.polcms/cms/vernazza/FrameworkNanoAOD/hhbbtt-analysis' \
                 '/nanoaod_base_analysis/data/cmssw/CMSSW_12_3_0_pre6/src/HTT-utilities/trigSFs_UL_eleMu' \
                 '/sf_el_2016post_HLTEle25_fix.root'

os.system('cp {} {}'.format(input_file, input_file_fix))

file = ROOT.TFile(input_file_fix, "UPDATE")

print("\n ### INFO: Open SF2D")
h_SF2D = file.Get("SF2D")

print(" ### INFO: SF2D Bin Content BEFORE = ", h_SF2D.GetBinContent(14))
h_SF2D.SetBinContent(14, h_SF2D.GetBinContent(70))
print(" ### INFO: SF2D Bin Content AFTER = ", h_SF2D.GetBinContent(14))

print(" ### INFO: SF2D Bin Error BEFORE = ", h_SF2D.GetBinError(14))
h_SF2D.SetBinError(14, h_SF2D.GetBinError(70))
print(" ### INFO: SF2D Bin Eroor AFTER = ", h_SF2D.GetBinError(14))

print("\n ### INFO: Open eff_mc")
h_eff_mc = file.Get("eff_mc")

print(" ### INFO: eff_mc Bin Content BEFORE = ", h_eff_mc.GetBinContent(14))
h_eff_mc.SetBinContent(14, h_eff_mc.GetBinContent(70))
print(" ### INFO: eff_mc Bin Content AFTER = ", h_eff_mc.GetBinContent(14))

print(" ### INFO: eff_mc Bin Error BEFORE = ", h_eff_mc.GetBinError(14))
h_eff_mc.SetBinError(14, h_eff_mc.GetBinError(70))
print(" ### INFO: eff_mc Bin Eroor AFTER = ", h_eff_mc.GetBinError(14))

file.Write("", ROOT.TFile.kOverwrite)

file.Close()