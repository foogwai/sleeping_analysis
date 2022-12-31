% For bi-direction machine
% Forward time
% reads the state sequence from the _state_series files
%
%   MATLAB shits itself if the delimiter isn't a comma, so the bash file
%   'fixdelimiter' simply changes all delimiters from ; to , . 
%   Run that beforehand
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
                % Create a string that is the text file name, and read the file if it exists.
                textFileName = sprintf('./cssr_output/%s/%s_%s_channel_%d_2500_%d_state_series', p{1}, p{1}, stage{1}, ch-1, lam+1);
                resultFileName = sprintf('./cssr_output/%s/%s_%s_channel_%d_2500_%d_results', p{1}, p{1}, stage{1}, ch-1, lam+1);
                if exist(textFileName, 'file') && exist(resultFileName, 'file')
                    fprintf('attempting %s forward time states now.\n', textFileName);
                    cellstates{pi,ch,lam,a} = readmatrix(textFileName);
                    fbadstates(pi,ch,lam,a) = NaN;
                else
                    fprintf('File %s does not exist NAN NAN NAN NAN NAN NAN NAN NAN.\n', textFileName);
                    fbadstates(pi,ch,lam,a) = NaN;
                end
                clear textFileName
            end %a
        end %lam
    end %ch
end %p
toc
%done = 1
clear done p pi ch lam stage a textFileName
