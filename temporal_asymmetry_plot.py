import scipy.io
import numpy as np
import scipy.stats as stats
from numpy import std, mean, sqrt
from palettable.scientific.diverging import Roma_20_r
import matplotlib.pyplot as plt
import pickle
import matplotlib as mpl
from matplotlib.patches import Rectangle
from statistics import *
import pandas as pd
index_x = ['fr', 'pa', 'te', 'oc', 'ci', 'in', 'hi']

colormap = Roma_20_r.mpl_colormap
segment_length = 2500
mat = scipy.io.loadmat('./csv_data_2500_001_all//gkl.mat')['gradKL_symm_f_r']
dmat = scipy.io.loadmat('./csv_data_2500_001_all//bisc.mat')['bi_sc']
with open("./csv_data_2500_001_all//wake_result_{}.txt".format(segment_length), "rb") as f:
    w = np.array(pickle.load(f))
with open("./csv_data_2500_001_all//early_result_{}.txt".format(segment_length), "rb") as f:
    e = np.array(pickle.load(f))
with open("./csv_data_2500_001_all//wake_rev_result_{}.txt".format(segment_length), "rb") as f:
    irw = np.array(pickle.load(f))
with open("./csv_data_2500_001_all//early_rev_result_{}.txt".format(segment_length), "rb") as f:
    ire = np.array(pickle.load(f))

t_values = np.zeros((8, 7))
p_values = np.zeros((8, 7))
dt_values = np.zeros((8, 7))
dp_values = np.zeros((8, 7))

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


count = 0


def array_process(arr):
    result = np.array(arr)
    result = np.where(np.isnan(result), np.ma.array(
        result, mask=np.isnan(result)).mean(axis=0), result)
    return result


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


w = np.flip(w, axis=1)
e = np.flip(e, axis=1)
irw = np.flip(irw, axis=1)
ire = np.flip(ire, axis=1)

for l in range(8):
    lam = l
    for r in range(7):
        channels = get_channels(r)
        pw_results = []
        pe_results = []
        cw_results = []
        ce_results = []
        w_results = []
        e_results = []
        irw_results = []
        ire_results = []
        for p in range(10):
            for c in channels[p]:
                ch = c - 1
                pw_results.append(mat[p][ch][lam][0])
                pe_results.append(mat[p][ch][lam][1])
                cw_results.append(dmat[p][ch][lam][0])
                ce_results.append(dmat[p][ch][lam][1])
                w_results.append(w[p, lam, ch])
                e_results.append(irw[p, lam, ch])
                irw_results.append(e[p, lam, ch])
                ire_results.append(ire[p, lam, ch])

        pw_results = array_process(pw_results)
        pe_results = array_process(pe_results)
        cw_results = array_process(cw_results)
        ce_results = array_process(ce_results)
        w_results = array_process(w_results)
        e_results = array_process(e_results)
        irw_results = array_process(irw_results)
        ire_results = array_process(ire_results)

        rr = np.round(pw_results - pe_results, decimals=8)
        dd = cw_results - (w_results + irw_results) - \
            (ce_results - (e_results + ire_results))
        (t1, p_value1) = stats.ttest_1samp(rr, 0)
        (t2, p_value2) = stats.ttest_1samp(dd, 0)
        if p_value1 < 0.05:
            count += 1

        t_values[l, r] = t1
        p_values[l, r] = p_value1
        dt_values[l, r] = t2
        dp_values[l, r] = p_value2

t_values = np.flip(t_values, 0)
p_values = np.flip(p_values, 0)
dt_values = np.flip(dt_values, axis=0)
dp_values = np.flip(dp_values, axis=0)
fig, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(15, 5))
x_aix = np.arange(1, 19)
# y_aix = np.arange(2, 14)
ticklabels = ["{}".format(i) for i in x_aix]

_min, _max = -5, 5
centers = [1, 7, 2, 9]
dx, = np.diff(centers[:2])/(t_values.shape[1]-1)
dy, = -np.diff(centers[2:])/(t_values.shape[0]-1)
extent = [centers[0]-dx/2, centers[1]+dx/2, centers[2]+dy/2, centers[3]-dy/2]

im1 = ax1.imshow(  # arr_we,
    dt_values,
    interpolation=None,
    cmap=colormap, extent=extent, aspect='auto', vmin=_min, vmax=_max)
#ax1.set_xlabel('Participant', fontsize=20)
ax1.set_xticks(range(1, 8), index_x)
ax1.set_title('$\\Delta d=d^W - d^{NE}$', fontsize=24)
ax1.set_ylabel('$\\lambda$', rotation=0, fontsize=24)
ax1.yaxis.set_label_coords(-0.07, 0.5)

for i in range(dt_values.shape[0]):
    for j in range(dt_values.shape[1]):
        if dp_values[i, j] < 0.05:
            ax1.add_patch(Rectangle((0.5+j, 8.5-i), 1, 1, alpha=0.5,  # hatch='///',
                                    linewidth=1.5, facecolor='none', edgecolor='red'))

im2 = ax2.imshow(t_values, interpolation='nearest',
                 cmap=colormap, extent=extent, aspect='auto', vmin=_min, vmax=_max)
#ax2.set_xlabel('Participant', fontsize=20)
ax2.set_xticks(range(1, 8), index_x)
ax2.set_ylabel('$\\lambda$', rotation=0, fontsize=24)
ax2.set_title(
    '$\\Delta {D}_{kls} = {D}_{kls}^W - {D}_{kls}^{NE}$', fontsize=24)
ax2.yaxis.set_label_coords(-0.07, 0.5)

for i in range(t_values.shape[0]):
    for j in range(t_values.shape[1]):
        if p_values[i, j] < 0.05:
            ax2.add_patch(Rectangle((0.5+j, 8.5-i), 1, 1, alpha=0.5,  # hatch='////',
                                    linewidth=1.5, facecolor='none', edgecolor='red'))

cax, kw = mpl.colorbar.make_axes([ax1, ax2])
norm = mpl.colors.Normalize(_min, _max)
cbar = mpl.colorbar.ColorbarBase(cax, cmap=colormap, norm=norm)
cbar.ax.set_xlabel('$t$', rotation=0, fontsize=24)

plt.show()
