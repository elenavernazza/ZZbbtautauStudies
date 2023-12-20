import os,json, mplhep
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use(mplhep.style.CMS)

def SetStyle(ax, x_label, y_label, x_lim, y_lim, leg_title=''):
    leg = plt.legend(loc = 'upper right', fontsize=18, title=leg_title, title_fontsize=18, frameon=True)
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
    parser.add_option("--ver",     dest="ver",      default='prod_231220')
    (options, args) = parser.parse_args()

    ver = options.ver
    if ',' in options.mass:
        mass_points = options.mass.split(',')
    else:
        mass_points = [options.mass]

    odir = os.getcwd() + f'/CutFlow/{ver}'
    print(" ### INFO: Saving output in ", odir)
    os.system('mkdir -p ' + odir)

    for i, mass in enumerate(mass_points):

        basedir = '/data_CMS/cms/vernazza/cmt/MergeCutFlow/'
        datadir = basedir + f'ul_2018_ZZ_v10/ggXZZbbtt_M{mass}/cat_base_selection/{ver}'
        json_path = datadir + '/cut_flow.json'

        print(" ### INFO: Reading file", json_path)

        if not os.path.exists(json_path): print(" *ERROR*: File not found")

        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
        
        if i == 0:
            CutNames = []
            CutEff = []
            CutEffErr = []
            for j, (CutName, CutRes) in enumerate(data.items()):
                CutNames.append(CutName)
                CutEff.append([])
                CutEff[j].append(CutRes['pass']/CutRes['all'])
                CutEffErr.append([])
                CutEffErr[j].append(np.sqrt(CutRes['pass'])/CutRes['all'])
        else:
            for j, (CutName, CutRes) in enumerate(data.items()):
                CutEff[j].append(CutRes['pass']/CutRes['all'])
                CutEffErr[j].append(np.sqrt(CutRes['pass'])/CutRes['all'])

    print(" ### INFO: Plotting")

    cmap = plt.get_cmap('viridis')
    mass = [float(mass) for mass in mass_points]
    fig, ax = plt.subplots(figsize=(10,10))
    for j, CutName in enumerate(CutNames):
        if CutName == 'ZZBBTauTauFilterRDF_Sig': continue
        ax.errorbar(mass, CutEff[j], yerr=CutEffErr[j], label=CutName, lw=2, linestyle='', marker='o', color=cmap(j/len(CutNames)))

    SetStyle(ax, x_label="Mass [GeV]", y_label="Cut efficiency", x_lim=(np.min(mass)-40, np.max(mass)+40), y_lim=(0,1.2), leg_title='')
    plt.savefig(odir+'/CutFlowEfficiency.png')
    plt.savefig(odir+'/CutFlowEfficiency.pdf')
    plt.xscale('log')
    plt.savefig(odir+'/CutFlowEfficiencyLog.png')
    plt.savefig(odir+'/CutFlowEfficiencyLog.pdf')
    plt.close()
    

