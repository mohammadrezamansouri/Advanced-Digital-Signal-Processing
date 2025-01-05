clc;
clear;
close all;

%%%%%%%%%% INITIALIZATION %%%%%%%%%%
M = 2; % Downsampling factor
N = -10:10; 
% Define FIR filter (Decimation filter) based on sinc with Hamming window
Filter = sinc(N) .* hamming(length(N))';
% Normalize filter
Filter = Filter / sum(Filter);
%signal
Signal = randn(1, 30); 

%%%%%%%%%% DIRECT METHOD (H(z) -> Downsampling) %%%%%%%%%%

FilteredSignal = conv(Signal, Filter, 'same');

% Downsample by a factor of M
DownsampledSignal = FilteredSignal(1:M:end);

%%%%%%%%%% POLYPHASE DECOMPOSITION %%%%%%%%%%
% Split the filter into even and odd parts (Polyphase decomposition)
E0 = Filter(1:M:end); % Even part of filter
E1 = Filter(2:M:end); % Odd part of filter

% Downsample signal into even and odd parts
X_even = Signal(1:M:end);
X_odd = Signal(2:M:end);

% Convolve each part with respective polyphase components
Y_even = conv(X_even, E0, 'same');
Y_odd = conv(X_odd, E1, 'same');

% Combine results from even and odd paths
PolyphaseOutput = Y_even + Y_odd;

%%%%%%%%%% PLOT RESULTS %%%%%%%%%%
figure;

% Plot FIR filter
subplot(3,1,1)
stem(N, Filter, 'r', 'LineWidth', 1.5);
title('Decimation Filter (H(z))');
xlabel('Sample Index');
ylabel('Amplitude');
grid on;
grid minor;

% Plot downsampled signal (Direct method)
subplot(3,1,2)
stem(DownsampledSignal, 'b', 'LineWidth', 1.5);
title('Downsampled Signal (Direct Method)');
xlabel('Sample Index');
ylabel('Amplitude');
grid on;
grid minor;

% Plot polyphase output
subplot(3,1,3)
stem(PolyphaseOutput, 'm', 'LineWidth', 1.5);
title('Polyphase Output (Even/Odd Decomposition)');
xlabel('Sample Index');
ylabel('Amplitude');
grid on;
grid minor;

%%%%%%%%%% COMPARISON %%%%%%%%%%
% Compare the two results
Error = norm(DownsampledSignal - PolyphaseOutput);

disp(['Error between direct and polyphase methods: ', num2str(Error)]);
