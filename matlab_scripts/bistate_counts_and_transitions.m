% For bidirectional machine
%

tic
pi=0;
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
                textFileName = sprintf('./cssr_output/%s/%s_%s_channel_%d_%d_state_series', p{1}, p{1}, stage{1}, ch-1, lam+1);
                if ~( isempty(aligned{pi,ch,lam,a}) ) % skip if that is empty
                    fprintf('attempting %s now.\n', textFileName);
                    fstatepair = aligned{pi,ch,lam,a,1} + 1;
                    rstatepair = aligned{pi,ch,lam,a,2} + 1;
                    num_fstates = max(fstatepair(:));
                    num_rstates = max(rstatepair(:));
                    if isnan(num_fstates) && isnan(num_rstates)
                        fprintf('File %s does not exist NAN NAN NAN NAN NAN NAN NAN NAN.\n', textFileName);
                        bistate_count{pi,ch,lam,a} = [];
                        bitrans_probs{pi,ch,lam,a} = [];
                        bi_sc(pi,ch,lam,a) = NaN;
                    else
                        bistate_count{pi,ch,lam,a} = zeros(num_fstates,num_rstates); % initiali
                        bitrans_count{pi,ch,lam,a} = zeros(num_fstates,num_rstates,num_fstates,num_rstates);
                        bitrans_probs{pi,ch,lam,a} = zeros(num_fstates,num_rstates,num_fstates,num_rstates);% initalizing

                        [row_f, count_f] = size(fstatepair);
                        [row_r, count_r] = size(rstatepair);
                        for l = 1:min(row_f, row_r)
                            current_line = l - 1;
                            for k = 1:min(count_f, count_r)
                                idx = current_line * count_f + k;
                                m = fstatepair(l, k); % the forward time state
                                n = rstatepair(l, k); % the reverse time state
                                if (~isnan(m) && ~isnan(n))
                                    bistate_count{pi,ch,lam,a}(m,n) = bistate_count{pi,ch,lam,a}(m,n)+1;
                                    if k<count_f  %can't do a transition 
                                        q = fstatepair(l, k+1); % the forward time state being transitioned to forwards
                                        r = rstatepair(l, k+1); % the reverse time state being transitioned to forwards
                                        if (~isnan(q) && ~isnan(r)) %making sure we are not transitioning to a nan state.
                                            bitrans_count{pi,ch,lam,a}(m,n,q,r) = bitrans_count{pi,ch,lam,a}(m,n,q,r)+1;
                                        end
                                    end% % bi trans count loop
                                end                                 
                            end % k loop
                        end % l loop
                        clear m n fstatepair rstatepair q r k l

                        % calculate Bi-directional Cmu
                        totalcounts = sum(bistate_count{pi,ch,lam,a},'all'); %how many valid state pairs there are
                        sfrprobs = bistate_count{pi,ch,lam,a}/totalcounts;
                        frdummy = -sfrprobs.*log2(sfrprobs);
                        frdummy(isnan(frdummy)) = 0; %sets NaN values due to 0*log(0) to =0
                        bi_sc(pi,ch,lam,a) = sum(frdummy,'all');
                        clear totalcounts sfrprobs frdummy
                        %
                        % calculate bi-directional forward transition matrix.
                        % we have a counts of transition from state m,n to
                        % state q,r in (m,n,q,r). We want it as a probability ,
                        % so we need to divide by the amount of times m,n
                        % appeared. This is bistate_count(m,n)
                        %
                        % Turn counts into probabilities of transition.
                        for m = 1:num_fstates
                            for n = 1:num_rstates
                                bitrans_probs{pi,ch,lam,a}(m,n,:,:) = bitrans_count{pi,ch,lam,a}(m,n,:,:)./bistate_count{pi,ch,lam,a}(m,n);
                                %disp(bitrans_count{pi,ch,lam,a}(m,n,:,:)./sum(bistate_count{pi,ch,lam,a}(m,n,:)))
                            end % n
                        end % m
                        bitrans_probs{pi,ch,lam,a}(isnan(bitrans_probs{pi,ch,lam,a})) = 0; % Set NaN due to 0/0=Nan back to zero
                    end
                %
                %
                    clear num_fstates num_rstates m n
                else % if the entry is empty
                    fprintf('File %s does not exist NAN NAN NAN NAN NAN NAN NAN NAN.\n', textFileName);
                    bistate_count{pi,ch,lam,a} = [];
                    bitrans_probs{pi,ch,lam,a} = [];
                    bi_sc(pi,ch,lam,a) = NaN;
                end
            end %a
        end %lam
    end %ch
end %
toc
clear pi ch lam a textFileName