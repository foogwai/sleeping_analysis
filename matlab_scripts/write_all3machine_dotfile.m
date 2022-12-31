% Print a .dot file that has the forward-time, reverse-time and bidirectional machine together in a single picture. 
%
% input: 
% The bi_trans_probs{p,ch,lam,a} cell that contains (m,n,q,r) bistate
% transition probabilities - transition from bidirectional state (m,n) to
% bidirectional state (q,r). (first index is forward time state, second is
% reverse time state. 
%
% output
% The all 3 machines - forward machine, reverse machine and bidirectional
% machine together in a single .dot file

tic
pi=0;
for p = {'ba', 'fe', 'fr', 'gi', 'me', 'pa', 'pe', 'te', 'to', 'za'}
    pi = pi + 1;
    for ch = 1:18
        for lam = 2%1:7
            for stage = {'W', 'E'}
                if stage{1} == 'E' 
                    a = 2;
                else
                    a = 1;
                end
                textFileName = sprintf('./cssr_output/%s/%s_%s_channel_%d_2500_%d_all3.dot', p{1}, p{1}, stage{1}, ch-1, lam+1);
                init_str = sprintf('./cssr_output/%s/%s_%s_channel_%d_2500_%d_inipi', p{1}, p{1}, stage{1}, ch-1, lam+1);
                t0_str = sprintf('./cssr_output/%s/%s_%s_channel_%d_2500_%d_trans0', p{1}, p{1}, stage{1}, ch-1, lam+1);
                t1_str = sprintf('./cssr_output/%s/%s_%s_channel_%d_2500_%d_trans1', p{1}, p{1}, stage{1}, ch-1, lam+1);
                rinit_str = sprintf('./cssr_output/%s/%s_%s_channel_%d_2500_rev_%d_inipi', p{1}, p{1}, stage{1}, ch-1, lam+1);
                r0_str = sprintf('./cssr_output/%s/%s_%s_channel_%d_2500_rev_%d_trans0', p{1}, p{1}, stage{1}, ch-1, lam+1);
                r1_str = sprintf('./cssr_output/%s/%s_%s_channel_%d_2500_rev_%d_trans1', p{1}, p{1}, stage{1}, ch-1, lam+1);
                head1 = 'digraph G {subgraph cluster0 {node [style=filled,color=white];style=filled;color=lightgrey;';
                ftran0 = readmatrix(t0_str, FileType='text');
                ftran1 = readmatrix(t1_str, FileType='text');
                rtran0 = readmatrix(r0_str, FileType='text');
                rtran1 = readmatrix(r1_str, FileType='text');
                if ~( isempty(bitrans_probs{pi,ch,lam,a}) ) && exist(t0_str, 'file') && exist(t1_str, 'file') && exist(r0_str, 'file') && exist(r1_str, 'file') && exist(t0_str, 'file')% if that is empty we skip
                    fprintf('attempting %s now.\n', textFileName);
                    %
                    % print header of .dot file
                    fid = fopen(textFileName,'wt');
                    fprintf(fid,'%s\n',head1);
                    %
                    num_fstates = size(bitrans_probs{pi,ch,lam,a},1);
                    num_rstates = size(bitrans_probs{pi,ch,lam,a},2);
                    %
                    % print forward machine transitions
                    for u = 1:num_fstates
                        for v = 1:num_fstates
                            prob0 = ftran0(u,v); 
                            prob1 = ftran1(u,v);
                                    if prob0 > 0
                                        symbol = 0;
                                        string_trans = ['"' num2str(u-1) '" -> "' num2str(v-1) '" [label = " ' num2str(symbol) ':' num2str(round(prob0,3)) '   "];'];
                                        fprintf(fid,'%s\n',string_trans);
                                    end % if it was zero we don't have a transition to put down.
                                    if prob1 > 0
                                        symbol = 1;
                                        string_trans = ['"' num2str(u-1) '" -> "' num2str(v-1) '" [label = " ' num2str(symbol) ':' num2str(round(prob1,3)) '   "];'];
                                        fprintf(fid,'%s\n',string_trans);
                                    end
                        end % v the column
                    end % u the row
                    %
                    % print head2
                    head2 = 'label = "Forward machine";}subgraph cluster1 {node [style=filled,color=white];style=filled;color=lightblue;';
                    fprintf(fid,'%s\n',head2);
                    %
                    % print reverse machine transitions
                    for u = 1:num_rstates
                        for v = 1:num_rstates
                            prob0 = rtran0(u,v); 
                            prob1 = rtran1(u,v);
                                    if prob0 > 0
                                        symbol = 0;
                                        string_trans = ['"' num2str(u-1) '`" -> "' num2str(v-1) '`" [label = " ' num2str(symbol) ':' num2str(round(prob0,3)) '   "];'];
                                        fprintf(fid,'%s\n',string_trans);
                                    end % if it was zero we don't have a transition to put down.
                                    if prob1 > 0
                                        symbol = 1;
                                        string_trans = ['"' num2str(u-1) '`" -> "' num2str(v-1) '`" [label = " ' num2str(symbol) ':' num2str(round(prob1,3)) '   "];'];
                                        fprintf(fid,'%s\n',string_trans);
                                    end
                        end % v the column
                    end % u the row
                    clear prob0 prob1 u v symbol string_trans
                    %
                    % print head3
                    head3 = 'label = "Reverse Machine";}subgraph cluster2 {node [style=filled];';
                    fprintf(fid,'%s\n',head3);
                    %
                    % print the bi-transitions, they should look like:
                    % "A,C" -> "B,D" [label = "1: 0.5   "];
                    % sub-optimal code ahead
                    for m = 1:num_fstates
                        for n = 1:num_rstates % (m,m) is state we are transitioning from
                            for q = 1:num_fstates
                                for r = 1:num_rstates % (q,r) is state we are transitioning to
                                    prob = bitrans_probs{pi,ch,lam,a}(m,n,q,r);
                                    if prob > 0
                                        if ftran0(m,q)>0 %only transitions between forward states
                                            symbol = 0;
                                        else
                                            symbol = 1;
                                        end
                                        string_trans = ['"' num2str(m-1) ',' num2str(n-1) '" -> "' num2str(q-1) ',' num2str(r-1) '" [label = " ' num2str(symbol) ':' num2str(round(prob,3)) '   "];'];
                                        fprintf(fid,'%s\n',string_trans);
                                    end % if it was zero we don't have a transition to put down.
                                end %r loop
                            end % q loop
                        end % n loop
                    end %m loop
                    tail = 'label = "Bidirectional Machine";color=black}}';
                    fprintf(fid,'%s\n',tail); % this should be the end of the file.    
                    fclose(fid);
                    %
                end % empty check
            end %a
        end %lam
    end %ch
end 
toc
clear pi ch lam a textFileName
clear symbol head1 head2 head3 tail m n q r prob num_fstates num_rstates string_trans fid