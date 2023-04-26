#Alyssa La Fleur
#Comparisons with Plaper measurements (small sets of multiple measurements, very little Ns)

import numpy as np
from comparison_datasets import *
from processing_functions import *
import pandas as pd
from scipy import stats
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


def get_correls_double_log(df, colx, coly):
    heatmap_tm_no_nans = df[['PPI', colx, coly]].dropna()
    n_orig = df.shape[0]
    n = heatmap_tm_no_nans.shape[0]
    pearson_r = stats.pearsonr(np.log(heatmap_tm_no_nans[colx]),
                            np.log(heatmap_tm_no_nans[coly]))[0]**2
    spr = stats.spearmanr(np.log(heatmap_tm_no_nans[colx]),
                            np.log(heatmap_tm_no_nans[coly]))[0]
    return n_orig, n, round(pearson_r,2), round(spr,2)


on_targ = ['N5:N6', 'N7:N8', 'P5A:P6A', 'P7A:P8A']
on_targets = "#ffcc00ff"
off_targets = "#782167ff"

y_list = [('tm', 'dummy'), ('Avg_30', 'Stddev_30'), ('Avg_30_30', 'Stddev_30_30'), ('kd_nm', 'kd_error_nm')]
plapers = plaper_other_values()
plapers['on_target'] = plapers.PPI.isin(on_targ) 

plapers['kd_nm'] = plapers['kd']/(10**-9)
plapers['kd_error_nm'] = plapers['kd_error']/(10**-9)

on_targets = "#ffcc00ff"
off_targets = "#782167ff"

deseq_homo_af_batch = pd.read_csv('../processing_pipeline/processed_replicates/deseq_l68_psuedoreplicate_autotune.csv')
deseq_homo_af_batch = deseq_homo_af_batch.rename(columns = {'Unnamed: 0': 'PPI'})
all_plaper_vals = plapers.merge(deseq_homo_af_batch, on = 'PPI')

for pair in y_list:
    print(get_correls(all_plaper_vals, 'ashr_log2FoldChange_HIS_TRP', pair[0], False))
    print(get_correls(all_plaper_vals, 'ashr_log2FoldChange_HIS_TRP', pair[0], True))

    f, ax = plt.subplots()
    plt.errorbar(y = all_plaper_vals[all_plaper_vals.on_target == False][pair[0]],
                x = all_plaper_vals[all_plaper_vals.on_target == False]['ashr_log2FoldChange_HIS_TRP'], 
                xerr= all_plaper_vals[all_plaper_vals.on_target == False]['ashr_lfcSE_HIS_TRP'], 
                yerr= all_plaper_vals[all_plaper_vals.on_target == False][pair[1]],
                fmt="o", elinewidth = 2, alpha = 0.75, color = off_targets, capsize = 3, markersize = 5, ecolor = 'gray')
    plt.errorbar(y = all_plaper_vals[all_plaper_vals.on_target == True][pair[0]],
                x = all_plaper_vals[all_plaper_vals.on_target == True]['ashr_log2FoldChange_HIS_TRP'], 
                xerr= all_plaper_vals[all_plaper_vals.on_target == True]['ashr_lfcSE_HIS_TRP'], 
                yerr= all_plaper_vals[all_plaper_vals.on_target == True][pair[1]],
                fmt="o", elinewidth = 2, markersize = 5, alpha = 0.9, color = on_targets,capsize = 3, ecolor = 'gray')
    if pair[0] != 'tm':
        plt.yscale('log')
    plt.tight_layout()
    f.set_size_inches(1.25,1.25)
    plt.savefig('./figures/' + 'plaper_plfc_' + pair[0] +'.svg', dpi = 300)
    #plt.show()

    print('--------------------')

#comparing plaper measurements with each other 
combos = list(combinations([('tm', 'dummy'), ('Avg_30', 'Stddev_30'), ('Avg_30_30', 'Stddev_30_30'), ('kd_nm', 'kd_error_nm'), ('ashr_log2FoldChange_HIS_TRP', 'ashr_lfcSE_HIS_TRP')], 2))

df_to_graph = pd.DataFrame({'PPI':[], 'correl':[], 'rho':[], 'correl_log':[], 'rho_log':[], 'n':[]})
for a, b in combos:
    print (a,b)
    if 'ashr' in a[0]:
        total, reduced, r2, rho = get_correls(all_plaper_vals, a[0], b[0], False)
        total, reduced, r2_log, rho_log = get_correls(all_plaper_vals, a[0], b[0], True)
        df_to_graph.loc[df_to_graph.shape[0]] = [make_ppi(a[0],b[0]), r2, rho, r2_log, rho_log, reduced]
    elif 'ashr' in b[0]:
       total, reduced, r2, rho = get_correls(all_plaper_vals, b[0], a[0], False)
       total, reduced, r2_log, rho_log = get_correls(all_plaper_vals, b[0], a[0], True)
       df_to_graph.loc[df_to_graph.shape[0]] = [make_ppi(a[0],b[0]), r2, rho, r2_log, rho_log, reduced]
    else:
        total, reduced, r2, rho = get_correls(all_plaper_vals, a[0], b[0], False)
        total, reduced, r2_log, rho_log = get_correls(all_plaper_vals, a[0], b[0], True)
        df_to_graph.loc[df_to_graph.shape[0]] = [make_ppi(a[0],b[0]), r2, rho, r2_log, rho_log, reduced]
    f, ax = plt.subplots()
    plt.errorbar(y = all_plaper_vals[all_plaper_vals.on_target == False][a[0]],
                x = all_plaper_vals[all_plaper_vals.on_target == False][b[0]], 
                xerr= all_plaper_vals[all_plaper_vals.on_target == False][b[1]], 
                yerr= all_plaper_vals[all_plaper_vals.on_target == False][a[1]],
                fmt="o", elinewidth = 2, alpha = 0.75, color = off_targets, capsize = 3, markersize = 5, ecolor = 'gray')
    plt.errorbar(y = all_plaper_vals[all_plaper_vals.on_target == True][a[0]],
                x = all_plaper_vals[all_plaper_vals.on_target == True][b[0]], 
                xerr= all_plaper_vals[all_plaper_vals.on_target == True][b[1]], 
                yerr= all_plaper_vals[all_plaper_vals.on_target == True][a[1]],
                fmt="o", elinewidth = 2, markersize = 5, alpha = 0.9, color = on_targets,capsize = 3, ecolor = 'gray')
    #plt.yscale('log')
    #plt.xscale('log')
    plt.tight_layout()
    f.set_size_inches(1.25,1.25)
    plt.savefig('./figures/' + 'plaper_x' + str(b[0]) + '_y_' + str(a[0]) +'.svg', dpi = 300)
    #plt.show()   


#make a heatplot of correlations for plaper & plaper values, ashr values 
order_libraries = ['tm', 'Avg_30', 'Avg_30_30', 'kd_nm',  'ashr_log2FoldChange_HIS_TRP' ]
x = make_specific_order_lower_triangle(order_libraries, df_to_graph, 'correl',  get_diag = False)
y = make_specific_order_lower_triangle(order_libraries, df_to_graph, 'rho',  get_diag = False)
y = y.T
make_double_heatmap(x, y, order_libraries, 'copper_r', 'bone_r', size_1 = 2.5, size_2 = 2.5,show_names = False, annot = True, font_size = 8, saveName= 'correls_diff_plaper_sets.svg', show=False)


order_libraries = ['tm', 'Avg_30', 'Avg_30_30', 'kd_nm',  'ashr_log2FoldChange_HIS_TRP' ]
x = make_specific_order_lower_triangle(order_libraries, df_to_graph, 'correl_log',  get_diag = False)
make_lower_heatmap(x, order_libraries, 'copper_r',  size_1 = 2.5, size_2 = 2.5,show_names = False, annot = True, font_size = 8, saveName= 'correls_diff_plaper_sets_log.svg', show=False)


x = make_specific_order_lower_triangle(order_libraries, df_to_graph, 'n',  get_diag = False)
make_lower_heatmap(x, order_libraries, 'Purples',  size_1 = 2.5, size_2 = 2.5,show_names = False, annot = True, font_size = 8, saveName= 'correls_diff_plaper_set_sizes.svg', show=False)
