import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
from statistics import *
import scipy
import scipy.stats as st
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
segment_length = '2500'
with open("./csv_data_2500_1_all//wake_result_{}.txt".format(segment_length), "rb") as f:
    w = np.array(pickle.load(f))
with open("./csv_data_2500_1_all//early_result_{}.txt".format(segment_length), "rb") as f:
    e = np.array(pickle.load(f))
with open("./csv_data_2500_1_all//late_result_{}.txt".format(segment_length), "rb") as f:
    l = np.array(pickle.load(f))
with open("./csv_data_2500_1_all//rem_result_{}.txt".format(segment_length), "rb") as f:
    r = np.array(pickle.load(f))


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    se = scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)

    return h


x_major_locator = plt.MultipleLocator(1)
y_major_locator = plt.MultipleLocator(0.2)

e_result = np.nanmean(e, axis=0)
w_result = np.nanmean(w, axis=0)
l_result = np.nanmean(l, axis=0)
r_result = np.nanmean(r, axis=0)
print(w_result.shape)
# temp

e_result = e_result
w_result = w_result
l_result = l_result
r_result = r_result

arr_we = w_result - e_result
arr_wl = w_result - l_result
arr_wr = w_result - r_result
arr_re = r_result - e_result
arr_rl = r_result - l_result
arr_le = l_result - e_result

y_we = np.flip(np.nanmean(arr_we, axis=1))

std_we = np.flip(np.std(arr_we, axis=1))
y_wl = np.flip(np.nanmean(arr_wl, axis=1))
y_wr = np.flip(np.nanmean(arr_wr, axis=1))
y_re = np.flip(np.nanmean(arr_re, axis=1))
y_rl = np.flip(np.nanmean(arr_rl, axis=1))
y_le = np.flip(np.nanmean(arr_le, axis=1))

we_error_bars = []
wl_error_bars = []
re_error_bars = []
rl_error_bars = []
wr_error_bars = []
le_error_bars = []

for i in range(8):
    p_w_result = np.array(w)[:, i, :]
    p_e_result = np.array(e)[:, i, :]
    p_l_result = np.array(l)[:, i, :]
    p_r_result = np.array(r)[:, i, :]

    data = np.nanmean(p_w_result - p_e_result, axis=1)
    we_error_bars.append(mean_confidence_interval(data))
    data = np.nanmean(p_w_result - p_l_result, axis=1)
    wl_error_bars.append(mean_confidence_interval(data))
    data = np.nanmean(p_r_result - p_e_result, axis=1)
    re_error_bars.append(mean_confidence_interval(data))
    data = np.nanmean(p_r_result - p_l_result, axis=1)
    rl_error_bars.append(mean_confidence_interval(data))
    data = np.nanmean(p_w_result - p_r_result, axis=1)
    wr_error_bars.append(mean_confidence_interval(data))
    data = np.nanmean(p_l_result - p_e_result, axis=1)
    le_error_bars.append(mean_confidence_interval(data))

x = np.arange(2, 10)

fig, axs = plt.subplots(2, 3, figsize=(18, 12))
# axs[0, 0].plot(x, y_we, label='WR/NREMe')
# print(1.95 * np.std(y_we)/np.sqrt(len(y_we)))

#axs[0, 0].legend()
axs[0, 0].set_title('$\\Delta C_\\mu = C_\\mu^w - C_\\mu^{ne}$', fontsize=22)
for i in range(10):
    result = np.flip(np.nanmean(np.array(w[i]) - np.array(e[i]), axis=1))
    axs[0, 0].plot(x, result, label='p{}'.format(i), color='lightgrey')

axs[0, 0].errorbar(x, y_we, yerr=np.flip(we_error_bars), fmt='-', label='WR/NREMe', color='salmon', linewidth=2.5,
                   ecolor='black', capsize=4, capthick=1.5, elinewidth=1.5, barsabove=True)

#axs[0, 1].plot(x, y_wl, label='WR/NREMl')
#axs[0, 1].legend()
axs[1, 0].set_title('$\\Delta C_\\mu = C_\\mu^w - C_\\mu^{nl}$', fontsize=22)
for i in range(10):
    result = np.flip(np.nanmean(np.array(w[i]) - np.array(l[i]), axis=1))
    axs[0, 1].plot(x, result, label='p{}'.format(i), color='lightgrey')
axs[1, 0].errorbar(x, y_wl, yerr=np.flip(wl_error_bars), fmt='-', label='WR/NREMe', color='orange', linewidth=2.5,
                   ecolor='black', capsize=4, capthick=1.5, elinewidth=1.5, barsabove=True)

#axs[0, 2].plot(x, y_wr, label='WR/REM')
#axs[0, 2].legend()
axs[1, 2].set_title('$\\Delta C_\\mu = C_\\mu^w - C_\\mu^{rem}$', fontsize=22)
for i in range(10):
    result = np.flip(np.nanmean(np.array(w[i]) - np.array(r[i]), axis=1))
    axs[0, 2].plot(x, result, label='p{}'.format(i), color='lightgrey')
axs[1, 2].errorbar(x, y_wr, yerr=np.flip(wr_error_bars), fmt='-', label='WR/REM', color='darkblue', linewidth=2.5,
                   ecolor='black', capsize=4, capthick=1.5, elinewidth=1.5, barsabove=True)

#axs[1, 0].plot(x, y_re, label='REM/NREMe')
#axs[1, 0].legend()
axs[0, 1].set_title(
    '$\\Delta C_\\mu = C_\\mu^{rem} - C_\\mu^{ne}$', fontsize=22)
for i in range(10):
    result = np.flip(np.nanmean(np.array(r[i]) - np.array(e[i]), axis=1))
    axs[1, 0].plot(x, result, label='p{}'.format(i), color='lightgrey')
axs[0, 1].errorbar(x, y_re, yerr=np.flip(re_error_bars), fmt='-', label='WR/NREMe', color='teal', linewidth=2.5,
                   ecolor='black', capsize=4, capthick=1.5, elinewidth=1.5, barsabove=True)

#axs[1, 1].plot(x, y_rl, label='REM/NREMl')
#axs[1, 1].legend()
axs[1, 1].set_title(
    '$\\Delta C_\\mu = C_\\mu^{rem} - C_\\mu^{nl}$', fontsize=22)
for i in range(10):
    result = np.flip(np.nanmean(np.array(r[i]) - np.array(l[i]), axis=1))
    axs[1, 1].plot(x, result, label='p{}'.format(i), color='lightgrey')
axs[1, 1].errorbar(x, y_rl, yerr=np.flip(rl_error_bars), fmt='-', label='REM/NREMl', color='purple', linewidth=2.5,
                   ecolor='black', capsize=4, capthick=1.5, elinewidth=1.5, barsabove=True)

#axs[1, 2].plot(x, y_le, label='NREMl/NREMe')
#axs[1, 2].legend()
axs[0, 2].set_title(
    '$\\Delta C_\\mu = C_\\mu^{nl} - C_\\mu^{ne}$', fontsize=22)
for i in range(10):
    result = np.flip(np.nanmean(np.array(l[i]) - np.array(e[i]), axis=1))
    axs[1, 2].plot(x, result, label='p{}'.format(i), color='lightgrey')
axs[0, 2].errorbar(x, y_le, yerr=np.flip(rl_error_bars), fmt='-', label='NREMl/NREMe', color='steelblue', linewidth=2.5,
                   ecolor='black', capsize=4, capthick=1.5, elinewidth=1.5, barsabove=True)

for i in range(0, 2):
    for j in range(0, 3):
        axs[i, j].set_xlabel('$\\lambda$', rotation=0, fontsize=24)
        axs[i, j].set_ylabel('$\\Delta C_\\mu$', rotation=90, fontsize=18)
        axs[i, j].xaxis.set_major_locator(x_major_locator)
        #axs[i, j].yaxis.set_major_locator(y_major_locator)
        axs[i, j].axhline(0, color='grey', linestyle='--')

# plt.plot(x, y_wl, label = 'WR/NREMl')
# plt.plot(x, y_wr, label = 'WR/REM')
# plt.plot(x, y_re, label = 'REM/NREMe')
# plt.plot(x, y_rl, label = 'REM/NREMl')
# plt.plot(x, y_le, label = 'NREMl/NREMe')
fig.tight_layout(pad=2)
# plt.legend()
plt.show()
x = np.arange(1, 19)
r = []

plt.figure(figsize=(15, 5))
errors = []
results = np.array(w)[:, 7, :] - np.array(e)[:, 7, :]
print(results)
for i in range(10):
    result = results[i]
    r.append(result)
    plt.plot(x, result, label='p{}'.format(i), color='lightgrey')

y = np.nanmean(r, axis=0)
for i in range(18):
    _presults = np.array(r)[:, i]
    errors.append(mean_confidence_interval(_presults))

plt.errorbar(x, y, yerr=errors,  # yerr=abs(np.nanmean(r, axis=0)*0.95),
             fmt='-', label='p{}'.format(i), color='red', ecolor='black', linewidth=2.5,
             capsize=4, capthick=1.5, elinewidth=1.5, barsabove=True)
# plt.errorbar(x, np.nanmean(r, asix=0), yerr=r, ms=10, fmt='o', c='gold', ecolor='red', elinewidth=0.5, capsize=4, capthick=1.5, label='Wakeful Rest')
ax = plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
plt.axhline(0, color='grey', linestyle='--')

plt.show()
