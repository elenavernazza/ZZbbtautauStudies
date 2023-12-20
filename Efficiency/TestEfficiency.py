import ROOT
ROOT.gROOT.SetBatch(True)
import matplotlib.pyplot as plt
import numpy as np
import mplhep, glob, json
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

    indir_Stat = '/data_CMS/cms/vernazza/cmt/MergeCategorizationStats/ul_2018_ZZ_v10/'
    indir_Feat = '/data_CMS/cms/vernazza/cmt/FeaturePlot/ul_2018_ZZ_v10/'

    '/ggXZZbbtt_M200/prod_231005/stats.t0.d1.b0.json'

    if ',' in options.mass:
        mass_points = options.mass.split(',')
    else:
        mass_points = [options.mass]

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
            YieldFile = indir_Feat + f'cat_ZZ_elliptical_cut_80_{ch}/prod_231214/yields/ZZKinFit_highmass__{ch}_os_iso__pg_datacard_zz_res__qcd__nodata.json'
            with open(YieldFile, 'r') as json_file: data = json.load(json_file)
            Pass[mass]  += data[f'ggXZZbbtt_M{mass}']['Entries']
            PassW[mass] += data[f'ggXZZbbtt_M{mass}']['Total yield']

    print(Total)
    print(Pass)
    print(TotalW)
    print(PassW)

    def GetUnc(num,den):
        if den != 0 and num != 0: return num/den * np.sqrt((np.sqrt(num)/num)**2+(np.sqrt(den)/den)**2)
        else: return 0
    
    def GetRatio(num,den):
        if den != 0 and num != 0: return num/den
        else: return 0

    mass_points = [float(mass) for mass in mass_points]
    Pass_Percentage = [GetRatio(float(Pass[mass]),float(Total[mass])) for mass in Pass.keys()]
    Pass_Percentage_Error = [GetUnc(float(Pass[mass]),float(Total[mass])) for mass in Pass.keys()]
    PassW_Percentage = [GetRatio(float(PassW[mass]),float(Total[mass])) for mass in PassW.keys()]
    PassW_Percentage_Error = [GetUnc(float(PassW[mass]),float(TotalW[mass])) for mass in PassW.keys()]

    plt.errorbar(mass_points, Pass_Percentage, yerr=Pass_Percentage_Error, marker='o')
    plt.ylabel('Efficiency')
    plt.xlabel('Resonance mass [GeV]')
    plt.grid()
    plt.ylim(-0.005,1.1*np.max(Pass_Percentage))
    plt.savefig('EfficiencyEntries.png')
    plt.close()

    plt.errorbar(mass_points, PassW_Percentage, yerr=Pass_Percentage_Error, marker='o')
    plt.ylabel('Efficiency')
    plt.xlabel('Resonance mass [GeV]')
    plt.grid()
    plt.ylim(-0.005,1.1*np.max(PassW_Percentage))
    plt.savefig('Efficiency.png')

