'''
Calculate statistical complexity according channels and anatomical regions for each participants.
'''
import scipy.io as spio
import pandas as pd
import pickle
import numpy as np

segment_length = 2500

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

# processing array data to replace nan value to 0


def array_process(arr):
    result = np.array(arr)
    # result = np.where(np.isnan(result), np.ma.array(
    #    result, mask=np.isnan(result)).mean(axis=0), result)
    resutl = np.nan_to_num(arr)
    return result


def process_loc_data(w, e, wfile_name, efile_name):

    w_fr_pos = []
    w_pa_pos = []
    w_te_pos = []
    w_oc_pos = []
    w_ci_pos = []
    w_in_pos = []
    w_hi_pos = []

    e_fr_pos = []
    e_pa_pos = []
    e_te_pos = []
    e_oc_pos = []
    e_ci_pos = []
    e_in_pos = []
    e_hi_pos = []

    for i in range(10):
        pa_w_fr_scores = []
        pa_w_pa_scores = []
        pa_w_te_scores = []
        pa_w_oc_scores = []
        pa_w_ci_scores = []
        pa_w_in_scores = []
        pa_w_hi_scores = []
        pa_e_fr_scores = []
        pa_e_pa_scores = []
        pa_e_te_scores = []
        pa_e_oc_scores = []
        pa_e_ci_scores = []
        pa_e_in_scores = []
        pa_e_hi_scores = []
        for c in loc_fr[i]:
            pa_w_fr_scores.append(list(w[i, :, c-1]))
            pa_e_fr_scores.append(list(e[i, :, c-1]))
        for c in loc_pa[i]:
            pa_w_pa_scores.append(list(w[i, :, c-1]))
            pa_e_pa_scores.append(list(e[i, :, c-1]))
        for c in loc_te[i]:
            pa_w_te_scores.append(list(w[i, :, c-1]))
            pa_e_te_scores.append(list(e[i, :, c-1]))
        for c in loc_oc[i]:
            pa_w_oc_scores.append(list(w[i, :, c-1]))
            pa_e_oc_scores.append(list(e[i, :, c-1]))
        for c in loc_ci[i]:
            pa_w_ci_scores.append(list(w[i, :, c-1]))
            pa_e_ci_scores.append(list(e[i, :, c-1]))
        for c in loc_in[i]:
            pa_w_in_scores.append(list(w[i, :, c-1]))
            pa_e_in_scores.append(list(e[i, :, c-1]))
        for c in loc_hi[i]:
            pa_w_hi_scores.append(list(w[i, :, c-1]))
            pa_e_hi_scores.append(list(e[i, :, c-1]))

        if len(loc_fr[i]) > 0:
            w_fr_mean_val = array_process(np.nanmean(pa_w_fr_scores, axis=0))
            e_fr_mean_val = array_process(np.nanmean(pa_e_fr_scores, axis=0))
            w_fr_pos.append(list(w_fr_mean_val))
            e_fr_pos.append(list(e_fr_mean_val))

        if len(loc_pa[i]) > 0:
            w_pa_mean_val = array_process(np.nanmean(pa_w_pa_scores, axis=0))
            e_pa_mean_val = array_process(np.nanmean(pa_e_pa_scores, axis=0))
            w_pa_pos.append(list(w_pa_mean_val))
            e_pa_pos.append(list(e_pa_mean_val))
        if len(loc_te[i]) > 0:
            w_te_mean_val = array_process(np.nanmean(pa_w_te_scores, axis=0))
            e_te_mean_val = array_process(np.nanmean(pa_e_te_scores, axis=0))
            w_te_pos.append(list(w_te_mean_val))
            e_te_pos.append(list(e_te_mean_val))
        if len(loc_oc[i]) > 0:
            w_oc_mean_val = array_process(np.nanmean(pa_w_oc_scores, axis=0))
            e_oc_mean_val = array_process(np.nanmean(pa_e_oc_scores, axis=0))
            w_oc_pos.append(list(w_oc_mean_val))
            e_oc_pos.append(list(e_oc_mean_val))
        if len(loc_ci[i]) > 0:
            w_ci_mean_val = array_process(np.nanmean(pa_w_ci_scores, axis=0))
            e_ci_mean_val = array_process(np.nanmean(pa_e_ci_scores, axis=0))
            w_ci_pos.append(list(w_ci_mean_val))
            e_ci_pos.append(list(e_ci_mean_val))
        if len(loc_in[i]) > 0:
            w_in_mean_val = array_process(np.nanmean(pa_w_in_scores, axis=0))
            e_in_mean_val = array_process(np.nanmean(pa_e_in_scores, axis=0))
            w_in_pos.append(list(w_in_mean_val))
            e_in_pos.append(list(e_in_mean_val))
        if len(loc_hi[i]) > 0:
            w_hi_mean_val = array_process(np.nanmean(pa_w_hi_scores, axis=0))
            e_hi_mean_val = array_process(np.nanmean(pa_e_hi_scores, axis=0))
            w_hi_pos.append(list(w_hi_mean_val))
            e_hi_pos.append(list(e_hi_mean_val))

    w_final_result = np.array([np.mean(w_fr_pos, axis=0), np.mean(w_pa_pos, axis=0), np.mean(w_te_pos, axis=0), np.mean(
        w_oc_pos, axis=0), np.mean(w_ci_pos, axis=0), np.mean(w_in_pos, axis=0), np.mean(w_hi_pos, axis=0)])
    e_final_result = np.array([np.mean(e_fr_pos, axis=0), np.mean(e_pa_pos, axis=0), np.mean(e_te_pos, axis=0), np.mean(
        e_oc_pos, axis=0), np.mean(e_ci_pos, axis=0), np.mean(e__pos, axis=0), np.mean(e_hi_pos, axis=0)])
    with open(wfile_name, "wb") as f:
        pickle.dump(w_final_result, f)
    with open(efile_name, "wb") as f:
        pickle.dump(e_final_result, f)


# processing with different sigma value
for s in ['0001', '001', '005', '01', '05', '1']:
    with open("./csv_data_2500_{}_all/wake_result_{}.txt".format(s, segment_length), "rb") as f:
        fw = np.array(pickle.load(f))
    with open("./csv_data_2500_{}_all/early_result_{}.txt".format(s, segment_length), "rb") as f:
        fe = np.array(pickle.load(f))
    with open("./csv_data_2500_{}_all/late_result_{}.txt".format(s, segment_length), "rb") as f:
        fl = np.array(pickle.load(f))
    with open("./csv_data_2500_{}_all/rem_result_{}.txt".format(s, segment_length), "rb") as f:
        fr = np.array(pickle.load(f))
    with open("./csv_data_2500_{}_all/wake_rev_result_{}.txt".format(s, segment_length), "rb") as f:
        bw = np.array(pickle.load(f))
    with open("./csv_data_2500_{}_all/early_rev_result_{}.txt".format(s, segment_length), "rb") as f:
        be = np.array(pickle.load(f))
    with open("./csv_data_2500_{}_all/late_rev_result_{}.txt".format(s, segment_length), "rb") as f:
        bl = np.array(pickle.load(f))
    with open("./csv_data_2500_{}_all/rem_rev_result_{}.txt".format(s, segment_length), "rb") as f:
        br = np.array(pickle.load(f))
    # $\Delta C_\mu value of wakeful - NREMe for forward and backwor direction$
    process_loc_data(fw, fe, "./csv_data_2500_{}_all/wake_result_location.txt".format(s),
                     "./csv_data_2500_{}_all/early_result_location.txt".format(s))
    process_loc_data(bw, be, "./csv_data_2500_{}_all/wake_rev_result_location.txt".format(s),
                     "./csv_data_2500_{}_all/early_rev_result_location.txt".format(s))
    process_loc_data(fl, fr, "./csv_data_2500_{}_all/late_result_location.txt".format(s),
                     "./csv_data_2500_{}_all/rem_result_location.txt".format(s))
    process_loc_data(bl, br, "./csv_data_2500_{}_all/late_rev_result_location.txt".format(s),
                     "./csv_data_2500_{}_all/rem_rev_result_location.txt".format(s))
