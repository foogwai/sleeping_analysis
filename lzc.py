from numpy import *
from numpy.linalg import *
from scipy import signal
from scipy.signal import hilbert
from scipy.stats import ranksums
from scipy.io import savemat
from scipy.io import loadmat
from random import *
from itertools import combinations
# from filter_data_methods import *
from pylab import *
from skimage.measure import block_reduce
import pickle

'''
Python code to compute complexity measures LZc, ACE and SCE as described in "Complexity of multi-dimensional spontaneous EEG decreases during propofol induced general anaesthesia"

Author: m.schartner@sussex.ac.uk
Date: 09.12.14

To compute the complexity meaures LZc, ACE, SCE for continuous multidimensional time series X, where rows are time series (minimum 2), and columns are observations, type the following in ipython:

execfile('CompMeasures.py')
LZc(X)
ACE(X)
SCE(X)


Some functions are shared between the measures.
'''


def Pre(X):
    '''
    Detrend and normalize input data, X a multidimensional time series
    '''
    ro, co = shape(X)
    Z = zeros((ro, co))
    for i in range(ro):
        Z[i, :] = signal.detrend(X[i, :]-mean(X[i, :]), axis=0)
    return Z


##########
'''
LZc - Lempel-Ziv Complexity, column-by-column concatenation
'''
##########


def cpr(string):
    '''
    Lempel-Ziv-Welch compression of binary input string, e.g. string='0010101'. It outputs the size of the dictionary of binary words.
    '''
    d = {}
    w = ''
    # i=1
    for c in string:
        wc = w + c
        if wc in d:
            w = wc
        else:
            d[wc] = wc
            w = c
    # i+=1
    return len(d)


def str_col(X):
    '''
    Input: Continuous multidimensional time series
    Output: One string being the binarized input matrix concatenated comlumn-by-column
    '''
    ro, co = shape(X)
    TH = zeros(ro)
    M = zeros((ro, co))
    for i in range(ro):
        M[i, :] = abs(hilbert(X[i, :]))
        TH[i] = mean(M[i, :])

    s = ''
    for j in range(co):
        for i in range(ro):
            if M[i, j] > TH[i]:
                s += '1'
            else:
                s += '0'
    return s


def LZc(X):
    '''
    Compute LZc and use shuffled result as normalization
    '''
    X = Pre(X)
    SC = str_col(X)
    M = list(SC)
    shuffle(M)
    w = ''

    for i in range(len(M)):
        w += M[i]
    sc_cpr = cpr(SC)
    w_cpr = cpr(w)
    # print('sc {} w {}'.format(sc_cpr, w_cpr))
    return sc_cpr/float(w_cpr)
    # return cpr(SC)/float(cpr(w))


data_path = './data'
patients = ['ba', 'fe', 'fr', 'gi', 'me', 'pa', 'pe', 'te', 'to', 'za']
sleeping_stages = ['W', 'E', 'L', 'R']

patient_scores = []
segment_length = 2500
patient_lzc = np.zeros((10, 18, 4))
pidx = 0
for patient in patients:
    staging_scores = []
    stage_idx = 0
    for stage in sleeping_stages:
        p_lzc = []
        mat = loadmat('{}/{}/{}1000.mat'.format(data_path, patient, stage))
        data = mat['dat']
        # print(data)
        # channels, obs = data.shape
        # , func=np.mean, cval=np.mean(data))
        new_data = block_reduce(data, block_size=(1, 4), func=np.average)
        channels, obs = new_data.shape
        # new_data = data
        for i in range(18):  # range(channels)[-18:]:
            # seq = np.array([np.append([], new_data[i])])
            # p_lzc.append(LZc(seq))

            segments = int(obs / segment_length)
            c_lzc = []
            for j in range(segments+1):
                end_idx = (j+1)*segment_length
                if end_idx == obs + segment_length:
                    continue
                if end_idx > obs and obs > j*segment_length:
                    end_idx = obs
                seq = np.array(
                    [np.append([], new_data[i][j*segment_length:end_idx])])
                lzc_result = LZc(seq)
                c_lzc.append(lzc_result)
                # print('LZc value of Patitient {} in {} stage with channel {} is {}'.format(
                #    patient, stage, i, lzc_result))
            p_lzc.append(np.mean(c_lzc))
            patient_lzc[pidx, i, stage_idx] = np.mean(c_lzc)
            # print(seq)
        print('LZc value of Patitient {} in {} stage is {}'.format(
            patient, stage, np.mean(p_lzc)))
        # np.savetxt('{}{}/lzc_{}_{}_ms_result.csv'.format(data_path,
        #           patient, patient, stage), p_lzc, delimiter=',', fmt='%f')
        stage_idx += 1
    pidx += 1

with open("lzc_result_{}.txt".format(segment_length), "wb") as f:
    pickle.dump(patient_lzc, f)
