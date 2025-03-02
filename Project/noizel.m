clc;
clear;
close all;

%% Load the "leleccum" Signal
load leleccum; % Load the built-in signal
indx = 2000:3450; % Select a segment of the signal
signal = leleccum(indx); % Extract the selected segment
noisy_signal = signal;

%% Plot Signals
figure;

plot(noisy_signal, 'LineWidth', 1.5);
title('Noisy Signal');
xlabel('Sample Index');
ylabel('Amplitude');

%% Save the Noisy Signal to a Text File
noisy_signal = noisy_signal(:); % Convert to column vector
save('leleccum_noisy_signal.txt', 'noisy_signal', '-ascii');

disp('Noisy signal saved to leleccum_noisy_signal.txt');
