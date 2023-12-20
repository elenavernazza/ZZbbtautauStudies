import matplotlib.pyplot as plt
import numpy as np
import mplhep, glob, json, os
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
    parser.add_option("--feat",    dest="feat",     default='ZZKinFit_highmass')
    parser.add_option("--ver",     dest="ver",      default='prod_231214')
    (options, args) = parser.parse_args()

    indir_Stat = '/data_CMS/cms/vernazza/cmt/MergeCategorizationStats/ul_2018_ZZ_v10/'
    indir_Feat = '/data_CMS/cms/vernazza/cmt/FeaturePlot/ul_2018_ZZ_v10/'

    feat = options.feat
    ver = options.ver
    if ',' in options.mass:
        mass_points = options.mass.split(',')
    else:
        mass_points = [options.mass]

    odir = os.getcwd() + f'/Efficiency/{ver}'
    print(" ### INFO: Saving output in ", odir)
    os.system('mkdir -p ' + odir)

    Total  = {mass: 0 for mass in mass_points}
    TotalW = {mass: 0 for mass in mass_points}
    Pass   = {mass: 0 for mass in mass_points}
    PassW  = {mass: 0 for mass in mass_points}

    for mass in mass_points:

        CountingFiles = glob.glob(indir_Stat + f'/ggXZZbbtt_M{mass}/prod_231005/stats.t0.*.json')
        if mass == '400': CountingFiles = [indir_Stat + '/ggXZZbbtt_M400/prod_231005/stats.json']
        for CountingFile in CountingFiles:
            with open(CountingFile, 'r') as json_file: data = json.load(json_file)
            Total[mass]  += data['nevents']
            TotalW[mass] += data['nweightedevents']

        for ch in ['etau', 'mutau', 'tautau']:
            YieldFile = indir_Feat + f'cat_ZZ_elliptical_cut_80_{ch}/{ver}/yields/{feat}__{ch}_os_iso__pg_datacard_zz_res__qcd__nodata.json'
            with open(YieldFile, 'r') as json_file: data = json.load(json_file)
            Pass[mass]  += data[f'ggXZZbbtt_M{mass}']['Entries']
            PassW[mass] += data[f'ggXZZbbtt_M{mass}']['Total yield']

    def GetUnc(num,den):
        if den != 0 and num != 0: return num/den * np.sqrt((np.sqrt(num)/num)**2+(np.sqrt(den)/den)**2)
        else: return 0
    
    def GetRatio(num,den):
        if den != 0 and num != 0: return num/den
        else: return 0

    mass = [float(mass) for mass in mass_points]
    Pass_Percentage = [GetRatio(float(Pass[mass]),float(Total[mass])) for mass in Pass.keys()]
    Pass_Percentage_Error = [GetUnc(float(Pass[mass]),float(Total[mass])) for mass in Pass.keys()]
    PassW_Percentage = [GetRatio(float(PassW[mass]),float(Total[mass])) for mass in PassW.keys()]
    PassW_Percentage_Error = [GetUnc(float(PassW[mass]),float(TotalW[mass])) for mass in PassW.keys()]

    cmap = plt.get_cmap('viridis')
    fig, ax = plt.subplots(figsize=(10,10))
    ax.errorbar(mass, Pass_Percentage, yerr=Pass_Percentage_Error, lw=2, linestyle='', marker='o', color=cmap(0))
    SetStyle(ax, x_label="Mass [GeV]", y_label="Efficiency", x_lim=(np.min(mass)-40, np.max(mass)+40), y_lim=(0,1.1*np.max(Pass_Percentage)), leg_title='')
    plt.savefig(odir + '/EfficiencyEntries.png')
    plt.savefig(odir + '/EfficiencyEntries.pdf')
    plt.xscale('log')
    plt.savefig(odir + '/EfficiencyEntriesLogX.png')
    plt.savefig(odir + '/EfficiencyEntriesLogX.pdf')
    plt.close()

    # ax.errorbar(mass, PassW_Percentage, yerr=Pass_Percentage_Error, marker='o')

