import ROOT, glob, sys, os, mplhep
from tqdm import tqdm
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
    mplhep.cms.label(data=False, rlabel='(13.6 TeV)')

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
                Float_t computeDeltaR(Vfloat GenPart_pt, Vfloat GenPart_eta, Vfloat GenPart_phi, Vfloat GenPart_mass, int index_1, int index_2) {
                    auto part1_tlv = TLorentzVector();
                    auto part2_tlv = TLorentzVector();
                    part1_tlv.SetPtEtaPhiM(GenPart_pt.at(index_1), GenPart_eta.at(index_1), GenPart_phi.at(index_1), GenPart_mass.at(index_1));
                    part2_tlv.SetPtEtaPhiM(GenPart_pt.at(index_2), GenPart_eta.at(index_2), GenPart_phi.at(index_2), GenPart_mass.at(index_2));
                    return part1_tlv.DeltaR(part2_tlv);
                }
            """)

if __name__ == "__main__" :

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--mass",         dest="mass",        default='200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,2000,3000')
    parser.add_option("--ver",          dest="ver",         default='prod_231005')
    parser.add_option("--plot_only",    dest="plot_only",   default=False,      action='store_true')
    (options, args) = parser.parse_args()

    indir_nano = '/data_CMS/cms/vernazza/MCProduction/2023_11_14/MyPrivateGridpacks'
    indir_prep = '/data_CMS/cms/vernazza/cmt/PreprocessRDF/ul_2018_ZZ_v10'

    ver = options.ver
    if ',' in options.mass:
        mass_points = options.mass.split(',')
    else:
        mass_points = [options.mass]

    odir = os.getcwd() + f'/DeltaR/{ver}'
    print(" ### INFO: Saving output in ", odir)
    os.system('mkdir -p ' + odir)

    H_DeltaR_b = []
    H_DeltaR_t = []

    if not options.plot_only:
        for mass in mass_points:

            print(" ### INFO: Analysing mass point", mass)
            # files = glob.glob(indir_prep + f'/gg_X_ZZbbtautau_M{mass}/*')
            files = glob.glob(indir_prep + f'/ggXZZbbtt_M{mass}/cat_base_selection/prod_231005/*')
            print(" ### INFO: Input folder", indir_prep + f'/ggXZZbbtt_M{mass}/cat_base_selection/prod_231005/*')

            dataframe_files = ROOT.vector(str)()
            for f in files:
                dataframe_files.push_back(f)
            df = ROOT.RDataFrame("Events", dataframe_files)

            df = df.Define("index_b1", "find_bb_tautau(GenPart_pdgId, GenPart_genPartIdxMother).at(0)")
            df = df.Define("index_b2", "find_bb_tautau(GenPart_pdgId, GenPart_genPartIdxMother).at(1)")
            df = df.Define("index_t1", "find_bb_tautau(GenPart_pdgId, GenPart_genPartIdxMother).at(2)")
            df = df.Define("index_t2", "find_bb_tautau(GenPart_pdgId, GenPart_genPartIdxMother).at(3)")

            df = df.Define("deltaR_bjets_%s" %mass, "computeDeltaR(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, index_b1, index_b2)")
            df = df.Define("deltaR_taus_%s" %mass, "computeDeltaR(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, index_t1, index_t2)")

            histo1 = df.Histo1D("deltaR_bjets_%s" %mass)
            histo2 = df.Histo1D("deltaR_taus_%s" %mass)
            H_DeltaR_b.append(histo1.Clone())
            H_DeltaR_t.append(histo2.Clone())


        print(" ### INFO: Saving root flies")
        fileout = ROOT.TFile(odir+'/DeltaR.root','RECREATE')
        for histo in H_DeltaR_b:
            histo.Write()
        for histo in H_DeltaR_t:
            histo.Write()
        fileout.Close()

    else:
        filein = ROOT.TFile(odir+'/DeltaR.root')
        for mass in mass_points:
            H_DeltaR_b.append(filein.Get("deltaR_bjets_%s" %mass))
            H_DeltaR_t.append(filein.Get("deltaR_taus_%s" %mass))
    
    print(" ### INFO: Start plotting")

    cmap = plt.get_cmap('viridis')
    fig, ax = plt.subplots(figsize=(10,10))
    for i, mass in enumerate(mass_points):
        X,Y,X_err,Y_err = GetArraysFromHisto(H_DeltaR_b[i])
        ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=f'{mass} GeV', lw=2, marker='o', color=cmap(i/len(mass_points)))
    SetStyle(ax, x_label=r"$\Delta R(b_{1},b_{2})$", x_lim=(0,4), y_label="Entries")
    plt.savefig(odir + '/DeltaR_bjets.png')
    plt.savefig(odir + '/DeltaR_bjets.pdf')
    plt.close()    

    fig, ax = plt.subplots(figsize=(10,10))
    for i, mass in enumerate(mass_points):
        X,Y,X_err,Y_err = GetArraysFromHisto(H_DeltaR_t[i])
        ax.errorbar(X, Y, xerr=X_err, yerr=Y_err, label=f'{mass} GeV', lw=2, marker='o', color=cmap(i/len(mass_points)))
    SetStyle(ax, x_label=r"$\Delta R(\tau_{1},\tau_{2})$", x_lim=(0,4), y_label="Entries")
    plt.savefig(odir + '/DeltaR_taus.png')
    plt.savefig(odir + '/DeltaR_taus.pdf')
    plt.close()  

