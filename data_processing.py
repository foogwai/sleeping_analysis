import pickle
import numpy as np
import numpy.ma as ma
from os.path import exists

data_path = './cssr_output'
patients = ['ba', 'fe', 'fr', 'gi', 'me', 'pa', 'pe', 'te', 'to', 'za']
sleep_stages = ['W', 'E', 'L', 'R']
segment_length = 2500
w_result_total = []
e_result_total = []
l_result_total = []
r_result_total = []

w_result_rev_total = []
e_result_rev_total = []
l_result_rev_total = []
r_result_rev_total = []

for patient in patients:
    w_result = []
    e_result = []
    l_result = []
    r_result = []
    w_rev_result = []
    e_rev_result = []
    l_rev_result = []
    r_rev_result = []
    for stage in sleep_stages:
        print('processing patient {} staging {}'.format(patient, stage))
        for l in reversed(range(2, 10)):
            channels = []
            channels_rev = []
            for c in range(31):
                source_file = './out/{}_{}_channel_{}_{}'.format(
                    patient, stage, c, segment_length)
                if not exists(source_file):
                    channels.append(np.nan)
                    channels_rev.append(np.nan)
                    continue
                fname = '{}/{}/{}_{}_channel_{}_{}_{}_info'.format(
                    data_path, patient, patient, stage, c, segment_length, l)
                frevname = '{}/{}/{}_{}_channel_{}_{}_rev_{}_info'.format(
                    data_path, patient, patient, stage, c, segment_length, l)

                cmu = np.nan
                rev_cmu = np.nan
                try:
                    lines = open(fname, 'r').readlines(0)
                    for line in lines:
                        if 'Statistical Complexity' in line:
                            r = line.split(':')
                            cmu = float(r[1].strip())
                except:
                    print('error {}'.format(fname))
                try:
                    lines = open(frevname, 'r').readlines(0)
                    for line in lines:
                        if 'Statistical Complexity' in line:
                            r = line.split(':')
                            rev_cmu = float(r[1].strip())
                except:
                    print('error {}'.format(frevname))
                channels.append(cmu)
                channels_rev.append(rev_cmu)
            if stage == 'W':
                w_result.append(channels)
                w_rev_result.append(channels_rev)
            if stage == 'E':
                e_result.append(channels)
                e_rev_result.append(channels_rev)
            if stage == 'L':
                l_result.append(channels)
                l_rev_result.append(channels_rev)
            if stage == 'R':
                r_result.append(channels)
                r_rev_result.append(channels_rev)

    w_result_rev_total.append(w_rev_result)
    e_result_rev_total.append(e_rev_result)
    l_result_rev_total.append(l_rev_result)
    r_result_rev_total.append(r_rev_result)

    w_result_total.append(w_result)
    e_result_total.append(e_result)
    l_result_total.append(l_result)
    r_result_total.append(r_result)

with open("wake_result_{}.txt".format(segment_length), "wb") as f:
    pickle.dump(w_result_total, f)
with open("early_result_{}.txt".format(segment_length), "wb") as f:
    pickle.dump(e_result_total, f)
with open("late_result_{}.txt".format(segment_length), "wb") as f:
    pickle.dump(l_result_total, f)
with open("rem_result_{}.txt".format(segment_length), "wb") as f:
    pickle.dump(r_result_total, f)

with open("wake_rev_result_{}.txt".format(segment_length), "wb") as f:
    pickle.dump(w_result_rev_total, f)
with open("early_rev_result_{}.txt".format(segment_length), "wb") as f:
    pickle.dump(e_result_rev_total, f)
with open("late_rev_result_{}.txt".format(segment_length), "wb") as f:
    pickle.dump(l_result_rev_total, f)
with open("rem_rev_result_{}.txt".format(segment_length), "wb") as f:
    pickle.dump(r_result_rev_total, f)
