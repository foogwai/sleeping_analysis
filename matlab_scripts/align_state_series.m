% For bidirectional machine
%
% input 2 files: the forward state series and the reverse state series
	

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
                % Create a string that is the text file name, and read the file if it exists.
                textFileName = sprintf('./cssr_output/%s/%s_%s_channel_%d_2500_%d_state_series', p{1}, p{1}, stage{1}, ch-1, lam+1);
                if ~( isempty(cellstates{pi,ch,lam,a}) || isempty(rcellstates{pi,ch,lam,a}) ) % if that or that is empty we skip
                    fprintf('attempting %s now.\n', textFileName);
                    aligned{pi,ch,lam,a,1} = cellstates{pi,ch,lam,a};
                    aligned{pi,ch,lam,a,2} = flip(rcellstates{pi,ch,lam,a}, 2);
                else % if the entry is empty
                    fprintf('File %s does not exist NAN NAN NAN NAN NAN NAN NAN NAN.\n', textFileName);
                    aligned{pi,ch,lam,a} = [];
                end
            end %a
        end %lam
    end %ch
end %participant
done = 1
clear done pi ch lam a textFileName