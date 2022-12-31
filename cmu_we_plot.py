import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
from matplotlib.patches import Rectangle
from palettable.scientific.diverging import Roma_20_r
segment_length = '2500'
index_x = ['fr', 'pa', 'te', 'oc', 'ci', 'in', 'hi']

colormap = Roma_20_r.mpl_colormap  # 'cividis'
'''
with open("./csv_data/wake_result_{}.txt".format(segment_length), "rb") as f:
    w = pickle.load(f)
with open("./csv_data/early_result_{}.txt".format(segment_length), "rb") as f:
    e = pickle.load(f)
with open("./csv_data/late_result_{}.txt".format(segment_length), "rb") as f:
    l = pickle.load(f)
with open("./csv_data/rem_result_{}.txt".format(segment_length), "rb") as f:
    r = pickle.load(f)
'''
'''
e_result = np.nanmean(e, axis=0)
w_result = np.nanmean(w, axis=0)
l_result = np.nanmean(l, axis=0)
r_result = np.nanmean(r, axis=0)
'''


def array_process(arr):
    result = np.array(arr)
    result = np.where(np.isnan(result), np.ma.array(
        result, mask=np.isnan(result)).mean(axis=0), result)
    #resutl = np.nan_to_num(arr)
    return result

#e_result = np.nanmean(e, axis=2).T
##w_result = np.nanmean(w, axis=2).T
#l_result = np.nanmean(l, axis=2).T
#r_result = np.nanmean(r, axis=2).T


with open("./csv_data_2500_001_all//wake_result_location.txt", "rb") as f:
    w_result = np.array(pickle.load(f))
with open("./csv_data_2500_001_all//early_result_location.txt", "rb") as f:
    e_result = np.array(pickle.load(f))
w_result = array_process(w_result).T
e_result = array_process(e_result).T
# fig, (ax1,cax,ax2) = plt.subplots(ncols=3, figsize=(18, 12)
#                    ,gridspec_kw={"width_ratios":[1, 0.05, 1]})
# fig.subplots_adjust(wspace=0.3)
fig, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(15, 5))
x_aix = np.arange(1, 19)
# y_aix = np.arange(2, 14)
ticklabels = ["{}".format(i) for i in x_aix]

# plt.figure(figsize=(10,10))
# plt.xticks(x_aix)
# plt.yticks(y_aix)
# sh = axs[0, 0].imshow(w_result, interpolation='nearest', extent=[1, 18, 2, 12])
# divider = make_axes_locatable(axs[0,0])
# cax = divider.append_axes("right", size="5%", pad=0.5)
# bar = plt.colorbar(sh, cax=cax)
# bar.set_label('color bar')
arr_we = w_result - e_result
print(arr_we.shape)
combined_data = np.array([w_result, e_result])
_min, _max = combined_data.min() - 0.1, combined_data.max()
print('min {} max {}'.format(_min, _max))
#centers = [1, 18, 2, 9]
centers = [1, 7, 2, 9]
dx, = np.diff(centers[:2])/(w_result.shape[1]-1)
dy, = -np.diff(centers[2:])/(w_result.shape[0]-1)
extent = [centers[0]-dx/2, centers[1]+dx/2, centers[2]+dy/2, centers[3]-dy/2]

im1 = ax1.imshow(w_result, interpolation=None,
                 cmap=colormap, extent=extent, aspect='auto', vmin=_min, vmax=_max)
#ax1.set_xlabel('Participant', fontsize=20)
ax1.set_xticks(range(1, 8), index_x)
ax1.set_title('Wakeful Rest', fontsize=24)
ax1.set_ylabel('$\\lambda$', rotation=0, fontsize=24)
ax1.yaxis.set_label_coords(-0.07, 0.5)

im2 = ax2.imshow(e_result, interpolation='nearest',
                 cmap=colormap, extent=extent, aspect='auto', vmin=_min, vmax=_max)
ax2.set_xticks(range(1, 8), index_x)
ax2.set_ylabel('$\\lambda$', rotation=0, fontsize=24)
ax2.set_title('NREM Early', fontsize=24)
ax2.yaxis.set_label_coords(-0.07, 0.5)
# axs[0,1].fill_between(x_aix, 2, 12, facecolor='white')
for i in range(arr_we.shape[0]):
    for j in range(arr_we.shape[1]):
        if arr_we[i, j] < 0:
            plt.gca().add_patch(Rectangle((0.5+j, 8.5-i), 1, 1, alpha=0.5, hatch='///',
                                          linewidth=0.1, facecolor='none', edgecolor='lightgrey'))
            # plt.gca().add_patch(Rectangle((0.5+j, 8.5-i), 1, 1, alpha=0.5,
            #                              linewidth=1.5, facecolor='none', edgecolor='red'))
            '''
            for k in np.linspace(i+0.5, i+1.5, num=8, endpoint=False):
                a = np.linspace(j+0.5, j+1.6, 10, endpoint=False)
                b = 9 - k
                c = 9 - k - 0.1
                ax2.fill_between(a, b, c, alpha=0.3,
                                 facecolor='lightgrey', step='pre')
            '''
# axs[0,1].imshow(arr_we, alpha=0.2,  extent=[1,18,2,12])
# axs[1,0].imshow(l_result, alpha=1,   extent=extent)
# axs[1,0].imshow(l_result, interpolation='nearest', extent=[1, 18, 2, 12])
# axs[1,1].imshow(r_result, interpolation='nearest', extent=extent)
cax, kw = mpl.colorbar.make_axes([ax1, ax2])
norm = mpl.colors.Normalize(_min, _max)
# plt.colorbar(im1, cax=cax, **kw)
cbar = mpl.colorbar.ColorbarBase(cax, cmap=colormap, norm=norm)
cbar.ax.set_xlabel('$C_\\mu$', rotation=0, fontsize=24)

plt.show()
