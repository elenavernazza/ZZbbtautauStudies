import ROOT
ROOT.gROOT.SetBatch(True)
import matplotlib.pyplot as plt
import numpy as np
import mplhep, os
plt.style.use(mplhep.style.CMS)

def SetStyle(ax, x_label, y_label, x_lim, y_lim, leg_title=''):
    leg = plt.legend(loc = 'upper right', fontsize=18, title=leg_title, title_fontsize=18)
    leg._legend_box.align = "left"
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xlim(x_lim)
    plt.ylim(y_lim)
    plt.grid()
    for xtick in ax.xaxis.get_major_ticks():
        xtick.set_pad(10)
    mplhep.cms.label(data=False)

if __name__ == "__main__" :

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("--mass",    dest="mass",     default='200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,2000,3000')
    parser.add_option("--ver",     dest="ver",      default='prod_231216')
    (options, args) = parser.parse_args()

    indir = '/data_CMS/cms/vernazza/cmt/FeaturePlot/ul_2018_ZZ_v10/'

    ver = options.ver
    if ',' in options.mass:
        mass_points = options.mass.split(',')
    else:
        mass_points = [options.mass]

    odir = os.getcwd() + f'/Boosted/{ver}'
    print(" ### INFO: Saving output in ", odir)
    os.system('mkdir -p ' + odir)

    isBoosted = {mass: 0 for mass in mass_points}
    isNotBoosted = {mass: 0 for mass in mass_points}
    Total = {mass: 0 for mass in mass_points}
    isBoostedNew = {mass: 0 for mass in mass_points}
    isNotBoostedNew = {mass: 0 for mass in mass_points}
    TotalNew = {mass: 0 for mass in mass_points}

    for ch in ['etau', 'mutau', 'tautau']:

        FileName = indir + f'cat_ZZ_elliptical_cut_80_{ch}/{ver}/root/boosted__{ch}_os_iso__pg_ggXZZbbtt__nodata.root'
        print(" ### INFO: Reading file", FileName)

        tf_sig = ROOT.TFile.Open(FileName)
        dir = tf_sig.Get("histograms")
        dir.cd()

        for mass in mass_points:

            h = ROOT.TH1D(dir.Get(f"ggXZZbbtt_M{mass}"))

            isNotBoosted[mass] += h.GetBinContent(1)
            isBoosted[mass] += h.GetBinContent(2)
            Total[mass] += h.Integral()

    ###############################################################################
    # Temporary
    FileName = indir + 'cat_ZZ_elliptical_cut_80_sr/prod_240210/root/boosted__os_iso__pg_ggXZZbbtt__nodata.root'
    tf_sig = ROOT.TFile.Open(FileName)
    dir = tf_sig.Get("histograms")
    dir.cd()

    for mass in mass_points:

        h = ROOT.TH1D(dir.Get(f"ggXZZbbtt_M{mass}"))

        isNotBoostedNew[mass] += h.GetBinContent(1)
        isBoostedNew[mass] += h.GetBinContent(2)
        TotalNew[mass] += h.Integral()
    
    ###############################################################################


    def GetUnc(num,den):
        return num/den * np.sqrt((np.sqrt(num)/num)**2+(np.sqrt(den)/den)**2)

    isBoosted_Percentage = [float(isBoosted[mass]/Total[mass]) for mass in isBoosted.keys()]
    isBoosted_Percentage_Error = [GetUnc(float(isBoosted[mass]),float(Total[mass])) for mass in isBoosted.keys()]
    isNotBoosted_Percentage = [float(isNotBoosted[mass]/Total[mass]) for mass in isNotBoosted.keys()]

    isBoostedNew_Percentage = [float(isBoostedNew[mass]/TotalNew[mass]) for mass in isBoostedNew.keys()]
    isBoostedNew_Percentage_Error = [GetUnc(float(isBoostedNew[mass]),float(TotalNew[mass])) for mass in isBoostedNew.keys()]
    isNotBoostedNew_Percentage = [float(isBoostedNew[mass]/TotalNew[mass]) for mass in isBoostedNew.keys()]

    mass = [float(mass) for mass in mass_points]

    cmap = plt.get_cmap('viridis')
    fig, ax = plt.subplots(figsize=(10,10))
    ax.errorbar(mass, isBoosted_Percentage, yerr=isBoosted_Percentage_Error, lw=2, linestyle='', marker='o', color=cmap(0), label='Old')
    ax.errorbar(mass, isBoostedNew_Percentage, yerr=isBoostedNew_Percentage_Error, lw=2, linestyle='', marker='o', color=cmap(0.5), label='New')
    SetStyle(ax, x_label="Mass [GeV]", y_label="Boosted fraction", x_lim=(np.min(mass)-40, np.max(mass)+40), y_lim=(0,1.1), leg_title='')
    plt.savefig(odir + '/BoostedFractionNew.png')
    plt.savefig(odir + '/BoostedFractionNew.pdf')
    plt.xscale('log')
    plt.savefig(odir + '/BoostedFractionNewLogX.png')
    plt.savefig(odir + '/BoostedFractionNewLogX.pdf')
    plt.close()


    # ax.stackplot(mass, isBoosted_Percentage, isNotBoosted_Percentage, labels=['isBoosted', 'isNotBoosted'], colors=['lightcoral','skyblue'])