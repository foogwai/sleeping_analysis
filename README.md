# sleeping_analysis

code for master thesis

## python code file list

- location.py: save the channel index of anatomical region for each participant.
- data_processing: process the statistical complexity value for each channel and all 4 stages.
- location_data_process.py: organize the statistical complexity value with anatomical region.
- cmu_we_plot.py: plot the statistical complexity color map(Figure 6 in paper).
- cmu_total_plot.py: Plot the different statistical complexity between stages(Figure 7 in paper).
- ire_we_plot.py: plot the $\Delta C_\mu$ and $\Delta \Xi$ color map(Figure 8 in paper).  
- temporal_asymmetry_plot.py: plot the crypticity and microscopic irreversibility difference (Figure 9 in paper)
- lzc.py: compute complexity measures LZc, code from Schartner et al. - 2015.
- lze_plot.py: plot Lempel-Ziv complexity score for all participants in different sleeping stage, Figure 5 in paper.
  
## bash scripts

- alpha.txt: required file for generate_emfile.sh.
- generate_emfile.sh: generate CSSR related information.
- transition_grab.sh: grabs the initial probability vector (in a column file) and the transition matrix from CSSR output for forward-time machine
- rev_transition_grab.sh: same functions as transition_grab.sh but for reversed-time machine
- fixdelimiter.sh: converts all ';' delimiters in the *_state_series to ',' in forward-time machine CSSR file.
- fixdelimiter_rev.sh: converts all ';' delimiters in the *_state_series to ',' in reversed-time machine CSSR file.

## Matlab functions list

- fa_hmm_sparse.m: probability of observing the given sequence, required for gradle_f_m.m.
- gradle_f_m.m: Calculate the rate of KL divergence between any forward and backward machines.
- getcell_state_series.m,getcell_rstate_series.m: Load the state series output files from CSSR for both M+ and M-.
- align_state_series.m: align the forward time and reverse time state series.
- bistate_counts_and_transitions.m: calculate bidirectional $C_\mu^{+-}$ and crypticity.
- write_all3machine_dotfile.m: writes that information for forward, reverse and bidirectional machines together in one .dot file.