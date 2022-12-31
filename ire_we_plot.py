from math import sqrt
import pickle
import numpy as np
from numpy import std, mean, sqrt
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
from matplotlib.patches import Rectangle
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.stats.weightstats import ttest_ind, ztest
import statsmodels.stats as st
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from palettable.colorbrewer.diverging import RdBu_5
from palettable.scientific.diverging import Roma_20_r

import pandas as pd
from os.path import exists
import math
index_x = ['fr', 'pa', 'te', 'oc', 'ci', 'in', 'hi']

with open("./csv_data_2500_001_all//wake_result_2500.txt", "rb") as f:
    w = np.array(pickle.load(f))
with open("./csv_data_2500_001_all//early_result_2500.txt", "rb") as f:
    e = np.array(pickle.load(f))
with open("./csv_data_2500_001_all//late_result_2500.txt", "rb") as f:
    l = np.array(pickle.load(f))
with open("./csv_data_2500_001_all//rem_result_2500.txt", "rb") as f:
    r = np.array(pickle.load(f))
with open("./csv_data_2500_001_all//wake_rev_result_2500.txt", "rb") as f:
    ir_w = np.array(pickle.load(f))
with open("./csv_data_2500_001_all//early_rev_result_2500.txt", "rb") as f:
    ir_e = np.array(pickle.load(f))
with open("./csv_data_2500_001_all//late_rev_result_2500.txt", "rb") as f:
    ir_l = np.array(pickle.load(f))
with open("./csv_data_2500_001_all//rem_rev_result_2500.txt", "rb") as f:
    ir_r = np.array(pickle.load(f))
colormap = Roma_20_r.mpl_colormap

with open("./loc_data/loc_{}.txt".format("fr"), "rb") as f:
    loc_fr = pickle.load(f)
with open("./loc_data/loc_{}.txt".format("pa"), "rb") as f:
    loc_pa = pickle.load(f)
with open("./loc_data/loc_{}.txt".format("te"), "rb") as f:
    loc_te = pickle.load(f)
with open("./loc_data/loc_{}.txt".format("oc"), "rb") as f:
    loc_oc = pickle.load(f)
with open("./loc_data/loc_{}.txt".format("ci"), "rb") as f:
    loc_ci = pickle.load(f)
with open("./loc_data/loc_{}.txt".format("in"), "rb") as f:
    loc_in = pickle.load(f)
with open("./loc_data/loc_{}.txt".format("hi"), "rb") as f:
    loc_hi = pickle.load(f)


def array_process(arr):
    result = np.array(arr)
    result = np.where(np.isnan(result), np.ma.array(
        result, mask=np.isnan(result)).mean(axis=0), result)
    #result[np.isnan(result)] = 0
    return result


with open("./csv_data_2500_001_all/wake_result_location.txt", "rb") as f:
    w_result = np.array(pickle.load(f))
with open("./csv_data_2500_001_all/early_result_location.txt", "rb") as f:
    e_result = np.array(pickle.load(f))
w_result = array_process(w_result).T
e_result = array_process(e_result).T
with open("./csv_data_2500_001_all/wake_rev_result_location.txt", "rb") as f:
    ir_w_result = np.array(pickle.load(f))
with open("./csv_data_2500_001_all/early_rev_result_location.txt", "rb") as f:
    ir_e_result = np.array(pickle.load(f))
ir_w_result = array_process(ir_w_result).T
ir_e_result = array_process(ir_e_result).T


def addDfData(df, arr):
    for lbd in range(arr.shape[0]):
        lvalue = 8 - lbd  # lambda value from 8 down to 2
        for c in range(arr.shape[1]):
            channel = c + 1
            v = arr[lbd, c]
            df = df.append(pd.DataFrame(
                {'Lambda': [lvalue], 'Channel': [channel], 'cmu': [v]}), ignore_index=True)
    return df


fig, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(15, 5))
x_aix = np.arange(1, 11)
ticklabels = ["{}".format(i) for i in x_aix]

arr_we = w_result - e_result
arr_ir_w = w_result - ir_w_result
arr_ir_e = e_result - ir_e_result
arr_ir_we = arr_ir_w - arr_ir_e


def get_channels(regin_idx):
    result = loc_fr
    if regin_idx == 1:
        result = loc_pa
    if regin_idx == 2:
        result = loc_te
    if regin_idx == 3:
        result = loc_oc
    if regin_idx == 4:
        result = loc_ci
    if regin_idx == 5:
        result = loc_in
    if regin_idx == 6:
        result = loc_hi

    return result


count = 0
ccount = 0
t_values = np.zeros(arr_we.shape)
irt_values = np.zeros(arr_we.shape)
p_values = np.zeros(arr_we.shape)
irp_values = np.zeros(arr_we.shape)
count = 0
rr_results = []
oo_results = []
for l in range(8):
    for r in range(7):
        ws_array = []
        irws_array = []
        es_array = []
        ires_array = []
        channels = get_channels(r)
        for p in range(10):
            if len(channels[p]) > 0:
                for c in channels[p]:
                    ws_array.append(w[p, l, c-1])
                    irws_array.append(ir_w[p, l, c-1])
                    es_array.append(e[p, l, c-1])
                    ires_array.append(ir_e[p, l, c-1])
        ws_array = array_process(ws_array)
        irws_array = array_process(irws_array)
        es_array = array_process(es_array)
        ires_array = array_process(ires_array)
        rr = ws_array - es_array
        rr_results.append(rr)
        oo = (ws_array - irws_array) - (es_array - ires_array)
        oo_results.append(oo)
        (t1, p_value1) = stats.ttest_1samp(rr, 0)
        t_values[l][r] = t1
        p_values[l][r] = np.round(p_value1, decimals=4)
        (t2, p_value2) = stats.ttest_1samp(oo, 0)
        irt_values[l][r] = t2
        irp_values[l][r] = p_value2
        if math.isnan(t2):
            irt_values[l][r] = 0
            irp_values[l][r] = 0

_min, _max = -5, 5
centers = [1, 7, 2, 9]
dx, = np.diff(centers[: 2])/(w_result.shape[1]-1)
dy, = -np.diff(centers[2:])/(w_result.shape[0]-1)
extent = [centers[0]-dx/2, centers[1]+dx/2, centers[2]+dy/2, centers[3]-dy/2]

im1 = ax1.imshow(  # arr_we,
    t_values,
    interpolation=None,
    cmap=colormap, extent=extent, aspect='auto', vmin=_min, vmax=_max)
# ax1.set_xlabel('Participant', fontsize=20)
ax1.set_xticks(range(1, 8), index_x)
ax1.set_title('$\\Delta C_\\mu = C_\\mu^W - C_\\mu^{NE}$', fontsize=24)
ax1.set_ylabel('$\\lambda$', rotation=0, fontsize=24)
ax1.yaxis.set_label_coords(-0.07, 0.5)

for i in range(t_values.shape[0]):
    for j in range(t_values.shape[1]):
        if p_values[i, j] < 0.05:
            # ax1.add_patch(Rectangle((0.5+j, 8.5-i), 1, 1, alpha=0.5,
            #              linewidth=1.5, facecolor='none', edgecolor='red'))
            ax1.add_patch(Rectangle((0.5+j, 8.5-i), 1, 1, alpha=0.5,  # hatch='///',
                                    linewidth=1.5, facecolor='none', edgecolor='red'))

im2 = ax2.imshow(irt_values, interpolation='nearest',
                 cmap=colormap, extent=extent, aspect='auto', vmin=_min, vmax=_max)
#ax2.set_xlabel('Participant', fontsize=20)
ax2.set_xticks(range(1, 8), index_x)
ax2.set_ylabel('$\\lambda$', rotation=0, fontsize=24)
ax2.yaxis.set_label_coords(-0.07, 0.5)
ax2.set_title('$\\Delta\\Xi = \\Xi^W - \\Xi^{NE}$', fontsize=24)
for i in range(irt_values.shape[0]):
    for j in range(irt_values.shape[1]):
        if irp_values[i, j] < 0.05:
            # ax2.add_patch(Rectangle((0.5+j, 8.5-i), 1, 1, alpha=0.5,
            #              linewidth=1.5, facecolor='none', edgecolor='red'))
            ax2.add_patch(Rectangle((0.5+j, 8.5-i), 1, 1, alpha=0.6,  # hatch='///',
                                    linewidth=1.5, facecolor='none', edgecolor='red'))
# axs[0,1].fill_between(x_aix, 2, 12, facecolor='white')
fig.subplots_adjust(wspace=0.2)


cax, kw = mpl.colorbar.make_axes([ax1, ax2])
norm = mpl.colors.Normalize(_min, _max)
# plt.colorbar(im1, cax=cax, **kw)
cbar = mpl.colorbar.ColorbarBase(cax, cmap=colormap, norm=norm)
cbar.ax.set_xlabel('$t$', rotation=0, fontsize=24)
plt.show()
