% gradient of KL divergence between forward machi and reverse machine
%
% output
    % rate of KL divergence between the two - are they the same machine?
%

tic

gradKL_f_r = nan(10,31,9,2); %initialize
gradKL_r_f = nan(10,31,9,2);
cellinit = nan(10,31,9,2);
celltrans0 = nan(10,31,9,2);
celltrans1 = nan(10,31,9,2);
rcellinit = nan(10,31,9,2);
rcelltrans0 = nan(10,31,9,2);
rcelltrans1 = nan(10,31,9,2);
gradKL_symm_f_r = nan(10,31,9,2);
pi = 0;

for p = {'ba', 'fe', 'fr', 'gi', 'me', 'pa', 'pe', 'te', 'to', 'za'}
    pi = pi + 1;
    for ch = 1:31
        for lam = 1:8
            for stage = {'W', 'E'}
                if stage{1} == 'E' 
                    a = 2;
                else
                    a = 1;
                end
                %
                textFileName = ['patient' p{1} 'ch' num2str(ch-1) 'a' stage{1} 'lam' num2str(lam)];
                %%%%%%%%
                % get the normal transition matrices from input files forward time cells and reverse time rcells%
                %%%%%%%%
                fprintf('attempting %s now.\n', textFileName);
                % forward machine files
                init_str = sprintf('./cssr_output/%s/%s_%s_channel_%d_2500_%d_inipi', p{1}, p{1}, stage{1}, ch-1, lam+1);
                t0_str = sprintf('./cssr_output/%s/%s_%s_channel_%d_2500_%d_trans0', p{1}, p{1}, stage{1}, ch-1, lam+1);
                t1_str = sprintf('./cssr_output/%s/%s_%s_channel_%d_2500_%d_trans1', p{1}, p{1}, stage{1}, ch-1, lam+1);
                % reverse machine files
                rinit_str = sprintf('./cssr_output/%s/%s_%s_channel_%d_2500_rev_%d_inipi', p{1}, p{1}, stage{1}, ch-1, lam+1);
                r0_str = sprintf('./cssr_output/%s/%s_%s_channel_%d_2500_rev_%d_trans0', p{1}, p{1}, stage{1}, ch-1, lam+1);
                r1_str = sprintf('./cssr_output/%s/%s_%s_channel_%d_2500_rev_%d_trans1', p{1}, p{1}, stage{1}, ch-1, lam+1);
            
                if (isfile(init_str)) && (isfile (rinit_str)) && (isfile(r0_str)) && (isfile(r1_str)) && (isfile(t0_str)) && (isfile(t1_str))
                    % forward form
                    init = readmatrix(init_str, FileType='text').';        
                    T0 = sparse(readmatrix(t0_str, FileType='text'));
                    T1 = sparse(readmatrix(t1_str, FileType='text'));
            
                    % reverse form
                    rinit = readmatrix(rinit_str, FileType='text').';
                    R0 = sparse(readmatrix(r0_str, FileType='text'));
                    R1 = sparse(readmatrix(r1_str, FileType='text'));
                
                    %%--%% 
                    %gradKL for each
                    %%--%% 
                    for n = 12:13 % putting this loop or at least "sequence" further out would be smarter.
                        sequence = (dec2bin(2^n-1:-1:0)-'0')+1; % 2^n rows, n columns each row is one possible observable sequence. 1 is a 0, 2 is a 1 lol
                        f_Pro = zeros(2^n,1);
                        r_Pro = zeros(2^n,1);
                        for k = 1:2^n
                            f_Pro(k,1) = fa_hmm_sparse(sequence(k,:),T0,T1,init); %runs Forward algorithm on all possible sequences, creating a column vector with length 2^n
                            r_Pro(k,1) = fa_hmm_sparse(sequence(k,:),R0,R1,rinit);
                        end
                        % Computer KL divergence between 
                        kldummy = f_Pro.*log2(f_Pro./r_Pro); % P = forward, Q reverse
                        qpdummy = r_Pro.*log2(r_Pro./f_Pro); % opposite to above
                        %
                        kldummy(isnan(kldummy))=0; %sets NaN values due to 0*log(0/Q) to =0
                        kldummy(kldummy == Inf)=0; %sets Inf values due to P*log(P/0) to =0
                        qpdummy(isnan(qpdummy))=0; %sets NaN values due to 0*log(0/Q) to =0
                        qpdummy(qpdummy == Inf)=0; %sets Inf values due to P*log(P/0) to =0
                        %
                        dummy_KL_f_r(n-11) = sum(kldummy); % KL(P|Q)
                        dummy_KL_r_f(n-11) = sum(qpdummy); % KL(Q|P)
                        %dummy_KLdiv(n-11) = sum(kldummy)+ sum(qpdummy); % KL(P|Q) + KL(Q|P)
                        %
                        clear kldummy qpdummy k sequence
                        %
                    end% n loop
                
                    gradKL_f_r(pi,ch,lam,a) = dummy_KL_f_r(2) - dummy_KL_f_r(1); % n13 - n12 for gradient
                    gradKL_r_f(pi,ch,lam,a) = dummy_KL_r_f(2) - dummy_KL_r_f(1);
                    gradKL_symm_f_r(pi,ch,lam,a) = gradKL_f_r(pi,ch,lam,a) + gradKL_r_f(pi,ch,lam,a);
                    %%--%% 
                    % END gradKL
                    %%--%%
                    clear dummy_KL_f_r dummy_KL_r_f n
                
                else % if the entry is empty we cannot compute the rate of KL divergence between the two
                    fprintf('File %s does not exist NAN NAN NAN NAN NAN NAN NAN NAN.\n', textFileName);
                    gradKL_f_r(pi,ch,lam,a) = NaN; % n13 - n12 for gradient
                    gradKL_r_f(pi,ch,lam,a) = NaN;
                    gradKL_symm_f_r(pi,ch,lam,a) = NaN;
                end % if CSSR empty check
            end %stage
        end %lam
    end %channel
end %participant

toc
clear ch lam a textFileName p pi stage
clear T0 T1 R0 R1 r_Pro f_Pro init rinit

