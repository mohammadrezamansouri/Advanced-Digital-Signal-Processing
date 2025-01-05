%% Kaiser Window Function 
function [h, H, w, N] = design_kaiser_filter(wp, ws, delta1, delta2)
    A = -20*log10(min(delta1, delta2)); % Attenuation in dB
    if A > 50
        beta = 0.1102 * (A - 8.7);
    elseif A >= 21
        beta = 0.5842 * (A - 21)^0.4 + 0.07886 * (A - 21);
    else
        beta = 0;
    end
    
    N = ceil((A - 8) / (2.285 * (ws - wp)));
    
    h = fir1(N, wp, kaiser(N+1, beta));
    
    [H, w] = freqz(h, 1, 1024);
end