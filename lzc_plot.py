import pickle
import numpy as np
from sklearn.preprocessing import minmax_scale, maxabs_scale, StandardScaler
import matplotlib.pyplot as plt
from numpy import std, mean, sqrt

with open('lzc_result_2500.txt', 'rb') as f:
    patient_lzc = np.array(pickle.load(f))


def cohen_d(x, y):
    nx = len(x)
    ny = len(y)
    dof = nx + ny - 2
    return (mean(x) - mean(y)) / sqrt(((nx-1)*std(x, ddof=1) ** 2 + (ny-1)*std(y, ddof=1) ** 2) / dof)


data = maxabs_scale(np.mean(patient_lzc, axis=1), axis=1)
we_a = 0
we_b = 0
we_c = 0
for i in range(10):
    d = cohen_d(patient_lzc[i, :, 0], patient_lzc[i, :, 1])
    if d > 0.8:
        we_a += 1
    elif d < -0.8:
        we_c += 1
    else:
        we_b += 1

print('WR/NREMe a {} b {} c{}'.format(we_a, we_b, we_c))

we_a = 0
we_b = 0
we_c = 0
for i in range(10):
    d = cohen_d(patient_lzc[i, :, 0], patient_lzc[i, :, 2])
    if d > 0.8:
        we_a += 1
    elif d < -0.8:
        we_c += 1
    else:
        we_b += 1
print('WR/NREMl a {} b {} c{}'.format(we_a, we_b, we_c))
we_a = 0
we_b = 0
we_c = 0
for i in range(10):
    d = cohen_d(patient_lzc[i, :, 0], patient_lzc[i, :, 3])
    if d > 0.8:
        we_a += 1
    elif d < -0.8:
        we_c += 1
    else:
        we_b += 1
print('WR/REM a {} b {} c{}'.format(we_a, we_b, we_c))
we_a = 0
we_b = 0
we_c = 0
for i in range(10):
    d = cohen_d(patient_lzc[i, :, 3], patient_lzc[i, :, 1])
    if d > 0.8:
        we_a += 1
    elif d < -0.8:
        we_c += 1
    else:
        we_b += 1
print('REM/NREMe a {} b {} c{}'.format(we_a, we_b, we_c))
we_a = 0
we_b = 0
we_c = 0
for i in range(10):
    d = cohen_d(patient_lzc[i, :, 3], patient_lzc[i, :, 2])
    if d > 0.8:
        we_a += 1
    elif d < -0.8:
        we_c += 1
    else:
        we_b += 1
print('REM/NREM a {} b {} c{}'.format(we_a, we_b, we_c))
we_a = 0
we_b = 0
we_c = 0
for i in range(10):
    d = cohen_d(patient_lzc[i, :, 2], patient_lzc[i, :, 1])
    if d > 0.8:
        we_a += 1
    elif d < -0.8:
        we_c += 1
    else:
        we_b += 1
print('NREMl/NREMe a {} b {} c{}'.format(we_a, we_b, we_c))
#print(np.mean(patient_lzc, axis=1))
# Set the figure size
plt.rcParams["figure.figsize"] = [6, 5]
plt.rcParams["figure.autolayout"] = True

x_ais = np.arange(1, 11)
# Scatter plot
plt.scatter(x_ais, data[:, 0], marker='o', s=100,
            c='gold', edgecolors='black', label='Wakeful Rest')
#plt.errorbar(x_ais, data[:,0], yerr=stdevs[:,0], ms=10, fmt='o', c='gold', ecolor='red', elinewidth=0.5, capsize=4, capthick=2, label='Wakeful Rest')
plt.scatter(x_ais, data[:, 3], marker='P', s=100, c='teal', label='REM')
#plt.errorbar(x_ais, data[:,3], yerr=stdevs[:,3],fmt='o', ms=10, capthick=2, c='teal', ecolor='red',elinewidth=0.5, capsize=4, label='REM')
plt.scatter(x_ais, data[:, 2], marker='D',
            s=100, c='maroon', label='Late NREM')
#plt.errorbar(x_ais, data[:,2], yerr=stdevs[:,2],fmt='o', ms=10, capthick=2, c='maroon', ecolor='red',elinewidth=0.5, capsize=4, label='Late NREM')
plt.scatter(x_ais, data[:, 1], marker='X', s=100,
            c='lightcoral', label='Early NREM')
#plt.errorbar(x_ais, data[:,1], yerr=stdevs[:,1],fmt='o', ms=10, capthick=2, c='lightcoral', ecolor='red',elinewidth=0.5, capsize=4, label='Late NREM')
plt.xticks(x_ais)
plt.grid(linestyle='-.', axis='x')
plt.xlabel("Participants")
plt.ylabel("Normalization scores of LZc")
plt.legend()
# Display the plot
plt.show()
