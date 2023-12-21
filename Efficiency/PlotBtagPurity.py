import ROOT, glob, sys, os, mplhep
import numpy as np
import matplotlib.pyplot as plt
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(000000)
plt.style.use(mplhep.style.CMS)

def GetArraysFromHisto(histo):
    X = [] ; Y = [] ; X_err = [] ; Y_err = []
    for ibin in range(0,histo.GetNbinsX()):
        X.append(histo.GetBinLowEdge(ibin+1) + histo.GetBinWidth(ibin+1)/2.)
        Y.append(histo.GetBinContent(ibin+1))
        X_err.append(histo.GetBinWidth(ibin+1)/2.)
        Y_err.append(histo.GetBinError(ibin+1))
    return X,Y,X_err,Y_err

def SetStyle(ax, x_label, y_label, x_lim = None, y_lim = None, leg_title=''):
    leg = plt.legend(loc = 'upper right', fontsize=20, title=leg_title, title_fontsize=18)
    leg._legend_box.align = "left"
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if x_lim: plt.xlim(x_lim)
    if y_lim: plt.ylim(y_lim)
    plt.grid()
    for xtick in ax.xaxis.get_major_ticks():
        xtick.set_pad(10)
    mplhep.cms.label(data=False)

ROOT.gInterpreter.Declare("""
                using Vfloat = const ROOT::RVec<float>&;
                using Vint   = const ROOT::RVec<int>&;
                ROOT::RVec<int> find_bb_tautau(Vint GenPart_pdgId, Vint GenPart_genPartIdxMother) {
                    bool Foundbjets = false;
                    bool Foundtaus = false;
                    int index_b1 = -1;
                    int index_b2 = -1;
                    int index_t1 = -1;
                    int index_t2 = -1;
                    for (int i_gen = 0; i_gen < GenPart_pdgId.size(); i_gen ++) {
                        if (GenPart_genPartIdxMother.at(i_gen) == -1) continue; // it is the incoming parton
                        if ((Foundbjets != true) && (fabs(GenPart_pdgId.at(i_gen)) == 5) && (GenPart_pdgId.at(GenPart_genPartIdxMother.at(i_gen)) == 23)) {
                            if (index_b1 == -1) index_b1 = i_gen;
                            else if (index_b2 == -1) index_b2 = i_gen;
                            if ((index_b1 != -1) && (index_b2 != -1)) {
                                Foundbjets = true;
                            }
                        }
                        if ((Foundtaus != true) && (fabs(GenPart_pdgId.at(i_gen)) == 15) && (GenPart_pdgId.at(GenPart_genPartIdxMother.at(i_gen)) == 23)) {
                            if (index_t1 == -1) index_t1 = i_gen;
                            else if (index_t2 == -1) index_t2 = i_gen;
                            if ((index_t1 != -1) && (index_t2 != -1)) {
                                Foundtaus = true;
                            }
                        }
                    }
                    return {index_b1, index_b2, index_t1, index_t2} ;
                }
            """)

ROOT.gInterpreter.Declare("""
                using Vfloat = const ROOT::RVec<float>&;
                using Vint   = const ROOT::RVec<int>&;
                bool check_gen_tag_matching(int index_1, int index_2, int bjet1_JetIdx, int bjet2_JetIdx,
                        Vfloat GenPart_pt, Vfloat GenPart_eta, Vfloat GenPart_phi, Vfloat GenPart_mass,
                        Vfloat Jet_pt, Vfloat Jet_eta, Vfloat Jet_phi) {
                    bool matched = false;
                    float deltaR = 0.3;
                    auto b1_gen_tlv = TLorentzVector();
                    auto b2_gen_tlv = TLorentzVector();
                    auto b1_tag_tlv = TLorentzVector();
                    auto b2_tag_tlv = TLorentzVector();
                    b1_gen_tlv.SetPtEtaPhiM(GenPart_pt.at(index_1), GenPart_eta.at(index_1), GenPart_phi.at(index_1), GenPart_mass.at(index_1));
                    b2_gen_tlv.SetPtEtaPhiM(GenPart_pt.at(index_2), GenPart_eta.at(index_2), GenPart_phi.at(index_2), GenPart_mass.at(index_2));
                    b1_tag_tlv.SetPtEtaPhiM(Jet_pt.at(bjet1_JetIdx), Jet_eta.at(bjet1_JetIdx), Jet_phi.at(bjet1_JetIdx), 0);
                    b2_tag_tlv.SetPtEtaPhiM(Jet_pt.at(bjet2_JetIdx), Jet_eta.at(bjet2_JetIdx), Jet_phi.at(bjet2_JetIdx), 0);
                    if (((b1_gen_tlv.DeltaR(b1_tag_tlv) < deltaR) && (b2_gen_tlv.DeltaR(b2_tag_tlv) < deltaR)) ||
                        ((b1_gen_tlv.DeltaR(b2_tag_tlv) < deltaR) && (b2_gen_tlv.DeltaR(b1_tag_tlv) < deltaR))) {
                        matched = true;
                    }
                    return matched;
                }
            """)

# plot fraction of b-jets rightly matched over reconstructed b-jets
if __name__ == "__main__" :

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--mass",         dest="mass",        default='200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,2000,3000')
    parser.add_option("--ver",          dest="ver",         default='prod_231005')
    parser.add_option("--plot_only",    dest="plot_only",   default=False,      action='store_true')
    (options, args) = parser.parse_args()

    ver = options.ver
    if ',' in options.mass:
        mass_points = options.mass.split(',')
    else:
        mass_points = [options.mass]

    indir_prep = '/data_CMS/cms/vernazza/cmt/PreprocessRDF/ul_2018_ZZ_v10'

    odir = os.getcwd() + f'/Btag/{ver}'
    print(" ### INFO: Saving output in ", odir)
    os.system('mkdir -p ' + odir)

    H_b1 = []
    H_b1_matched = []
    H_b2 = []
    H_b2_matched = []

    if not options.plot_only:
        for mass in mass_points:

            print(" ### INFO: Analysing mass point", mass)
            folder = indir_prep + f'/ggXZZbbtt_M{mass}/cat_base_selection/prod_231005'
            files = glob.glob(folder + '/*')
            print(" ### INFO: Input folder", folder)

            dataframe_files = ROOT.vector(str)()
            for f in files:
                dataframe_files.push_back(f)
            df = ROOT.RDataFrame("Events", dataframe_files)

            # find index for gen level b jets
            df = df.Define("index_b1", "find_bb_tautau(GenPart_pdgId, GenPart_genPartIdxMother).at(0)")
            df = df.Define("index_b2", "find_bb_tautau(GenPart_pdgId, GenPart_genPartIdxMother).at(1)")

            # check matching between tagged b jets and gen level b jets
            df = df.Define("matched", "check_gen_tag_matching(index_b1, index_b2, bjet1_JetIdx, bjet2_JetIdx,"
                    "GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, Jet_pt, Jet_eta, Jet_phi)")
            df_matched = df.Filter("matched == 1")

            df = df.Define("bjet1_pt_%s" %mass, "Jet_pt.at(bjet1_JetIdx)")
            df = df.Define("bjet2_pt_%s" %mass, "Jet_pt.at(bjet2_JetIdx)")
            df_matched = df_matched.Define("bjet1_pt_matched_%s" %mass, "Jet_pt.at(bjet1_JetIdx)")
            df_matched = df_matched.Define("bjet2_pt_matched_%s" %mass, "Jet_pt.at(bjet2_JetIdx)")

            histo1 = df.Histo1D("bjet1_pt_%s" %mass)
            histo1_matched = df_matched.Histo1D("bjet1_pt_matched_%s" %mass)
            histo2 = df.Histo1D("bjet2_pt_%s" %mass)
            histo2_matched = df_matched.Histo1D("bjet2_pt_matched_%s" %mass)
            
            H_b1.append(histo1.Clone())
            H_b1_matched.append(histo1_matched.Clone())
            H_b2.append(histo2.Clone())
            H_b2_matched.append(histo2_matched.Clone())

        print(" ### INFO: Saving root flies")
        fileout = ROOT.TFile(odir+'/BjetsMatched.root','RECREATE')
        for histo in H_b1:
            histo.Write()
        for histo in H_b1_matched:
            histo.Write()
        for histo in H_b2:
            histo.Write()
        for histo in H_b2_matched:
            histo.Write()
        fileout.Close()

    else:
        filein = ROOT.TFile(odir+'/BjetsMatched.root')
        for mass in mass_points:
            H_b1.append(filein.Get("bjet1_pt_%s" %mass))
            H_b1_matched.append(filein.Get("bjet1_pt_matched_%s" %mass))
            H_b2.append(filein.Get("bjet2_pt_%s" %mass))
            H_b2_matched.append(filein.Get("bjet2_pt_matched_%s" %mass))
            
    print(" ### INFO: Start plotting")

    cmap = plt.get_cmap('viridis')
    fig, ax = plt.subplots(figsize=(10,10))
    for i, mass in enumerate(mass_points):
        X,Y,X_err,Y_err = GetArraysFromHisto(H_b1[i])
        ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=f'{mass} GeV', lw=2, marker='o', color=cmap(i/len(mass_points)))
    SetStyle(ax, x_label=r"$p_{T} (b_{1}) \;[GeV]$", y_label="Entries")
    plt.savefig(odir + '/bjets1_pt.png')
    plt.savefig(odir + '/bjets1_pt.pdf')
    plt.close()    

    fig, ax = plt.subplots(figsize=(10,10))
    for i, mass in enumerate(mass_points):
        X,Y,X_err,Y_err = GetArraysFromHisto(H_b1_matched[i])
        ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=f'{mass} GeV', lw=2, marker='o', color=cmap(i/len(mass_points)))
    SetStyle(ax, x_label=r"$p_{T} (b_{1}) \;[GeV]$", y_label="Entries")
    plt.savefig(odir + '/bjets1_pt_matched.png')
    plt.savefig(odir + '/bjets1_pt_matched.pdf')
    plt.close()

    def GetUnc(num,den):
        return num/den * np.sqrt((np.sqrt(num)/num)**2+(np.sqrt(den)/den)**2)

    fig, ax = plt.subplots(figsize=(10,10))
    btag_efficiency = []
    btag_efficiency_error = []
    for i, mass in enumerate(mass_points):
        btag_efficiency.append(H_b1_matched[i].Integral()/H_b1[i].Integral())
        btag_efficiency_error.append(GetUnc(H_b1_matched[i].Integral(),H_b1[i].Integral()))
    mass = [float(mass) for mass in mass_points]
    ax.errorbar(mass, btag_efficiency, yerr=btag_efficiency_error, lw=2, marker='o', linestyle='', color=cmap(0))
    SetStyle(ax, x_label="Mass [GeV]", y_label="Btag efficiency")
    plt.savefig(odir + '/btag_efficiency.png')
    plt.savefig(odir + '/btag_efficiency.pdf')
    plt.xscale('log')
    plt.savefig(odir + '/btag_efficiencyLogX.png')
    plt.savefig(odir + '/btag_efficiencyLogX.pdf')
    plt.close()

