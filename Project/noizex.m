clc;
clear;
close all;

%% Generate Noisy "Bumps" Signal
rng default; % Set random seed for reproducibility
[X, XN] = wnoise('bumps', 10, sqrt(6)); % Generate original and noisy signals

%% Plot Signals
figure;
subplot(2, 1, 1);
plot(X, 'LineWidth', 1.5);
title('Original Signal (Bumps)');
xlabel('Sample Index');
ylabel('Amplitude');

subplot(2, 1, 2);
plot(XN, 'LineWidth', 1.5);
title('Noisy Signal (Bumps + Gaussian Noise)');
xlabel('Sample Index');
ylabel('Amplitude');

%% Save Noisy Signal to a Text File
XN = XN(:); % Convert to column vector
save('bumps_noisy_signal.txt', 'XN', '-ascii');

disp('Noisy signal saved to bumps_noisy_signal.txt');
