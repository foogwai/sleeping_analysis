'''
Save channel information of different anatomical region for each participant
'''
import scipy.io as spio
import pandas as pd
import pickle


patients = ['ba', 'fe', 'fr', 'gi', 'me', 'pa', 'pe', 'te', 'to', 'za']

frs = [[],
       [1, 2, 3],
       [1],
       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
       [1, 2, 3, 4, 5, 6, 7, 8],
       [1, 2, 3],
       [],
       [1, 2, 3, 4, 5],
       [],
       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
pas = [[1, 2, 3, 4, 5, 6, 7],
       [4, 5, 6, 7, 8, 9],
       [2, 3, 4, 5, 6, 7, 8, 9, 10],
       [13],
       [9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
       [4, 5],
       [1],
       [6],
       [1, 2, 3, 4, 5],
       []]
tes = [[8, 9, 10, 11],
       [10, 11, 12, 13, 14, 15, 16],
       [11, 12, 13, 14],
       [14, 15, 16, 17],
       [],
       [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
       [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
       [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
       [6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
       [12, 13, 14, 15, 16, 17, 18, 19]]
ocs = [[12, 13, 14, 15, 16],
       [17, 18],
       [15],
       [],
       [],
       [21],
       [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
       [23],
       [16, 17, 18, 19, 20, 21, 22, 23],
       []]
cis = [[17, 18, 19, 20, 21],
       [19, 20, 21, 22],
       [16, 17, 18],
       [18, 19],
       [19, 20, 21, 22, 23],
       [22],
       [],
       [],
       [24],
       [20]]
ins = [[22],
       [23],
       [],
       [20, 21, 22],
       [],
       [23, 24, 25, 26, 27, 28],
       [28], [24, 25, 26, 27, 28], [], [21, 22, 23, 24, 25, 26]]
his = [[], [], [], [], [], [], [29, 30, 31], [29], [25], []]

with open("loc_fr.txt", "wb") as f:
    pickle.dump(frs, f)
with open("loc_pa.txt", "wb") as f:
    pickle.dump(pas, f)
with open("loc_te.txt", "wb") as f:
    pickle.dump(tes, f)
with open("loc_oc.txt", "wb") as f:
    pickle.dump(ocs, f)
with open("loc_ci.txt", "wb") as f:
    pickle.dump(cis, f)
with open("loc_in.txt", "wb") as f:
    pickle.dump(ins, f)
with open("loc_hi.txt", "wb") as f:
    pickle.dump(his, f)