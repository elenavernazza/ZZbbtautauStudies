import ROOT
ROOT.gROOT.SetBatch(True)
import matplotlib.pyplot as plt
import numpy as np
import mplhep
plt.style.use(mplhep.style.CMS)

if __name__ == "__main__" :

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--mass",    dest="mass",     default='200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,2000,3000')
    parser.add_option("--dirs",    dest="dirs",     default='prod_231129_M900')
    parser.add_option("--feat",    dest="feat",     default='ZZKinFit_mass')
    parser.add_option("--ver",     dest="ver",      default='prod_231129')
    parser.add_option("--ch",      dest="ch",       default='combination')
    (options, args) = parser.parse_args()

    indir = '/data_CMS/cms/vernazza/cmt/FeaturePlot/ul_2018_ZZ_v10/'

    if ',' in options.mass:
        mass_points = options.mass.split(',')
    else:
        mass_points = [options.mass]

    isBoosted = {mass: 0 for mass in mass_points}
    isNotBoosted = {mass: 0 for mass in mass_points}
    Total = {mass: 0 for mass in mass_points}

    for ch in ['etau', 'mutau', 'tautau']:

        FileName = indir + f'cat_ZZ_elliptical_cut_80_{ch}/prod_231216/root/boosted__{ch}_os_iso__pg_ggXZZbbtt__nodata.root'

        tf_sig = ROOT.TFile.Open(FileName)
        dir = tf_sig.Get("histograms")
        dir.cd()

        for mass in mass_points:

            h = ROOT.TH1D(dir.Get(f"ggXZZbbtt_M{mass}"))

            isNotBoosted[mass] += h.GetBinContent(1)
            isBoosted[mass] += h.GetBinContent(2)
            Total[mass] += h.Integral()

    print(isBoosted)
    print(isNotBoosted)

    def GetUnc(num,den):
        return num/den * np.sqrt((np.sqrt(num)/num)**2+(np.sqrt(den)/den)**2)

    isBoosted_Percentage = [float(isBoosted[mass]/Total[mass]) for mass in isBoosted.keys()]
    isBoosted_Percentage_Error = [GetUnc(float(isBoosted[mass]),float(Total[mass])) for mass in isBoosted.keys()]
    isNotBoosted_Percentage = [float(isNotBoosted[mass]/Total[mass]) for mass in isNotBoosted.keys()]
    mass_points = [float(mass) for mass in mass_points]

    plt.stackplot(mass_points, isBoosted_Percentage, isNotBoosted_Percentage, labels=['isBoosted', 'isNotBoosted'], colors=['lightcoral','skyblue'])
    plt.ylabel('Percentage')
    plt.xlabel('Resonance mass [GeV]')
    plt.legend(frameon=True)
    plt.savefig('EfficiencyBoostedStack.png')
    plt.close()

    plt.errorbar(mass_points, isBoosted_Percentage, yerr=isBoosted_Percentage_Error, marker='o')
    plt.ylabel('Boosted fraction')
    plt.xlabel('Resonance mass [GeV]')
    plt.grid()
    plt.savefig('EfficiencyBoosted.png')

