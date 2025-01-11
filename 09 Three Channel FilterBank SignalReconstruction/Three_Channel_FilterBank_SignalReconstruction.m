
clear; clc; close all;

%% 1) Parameter Settings

%Input signal
Fs = 100;
t = -5:1/Fs:5;
x = sin(pi * t);


M = 3;               
 

%% 2) Design of Analysis Filters

Order = 128;         
beta_kaiser = 10;   
cutoff_lp = 0.3;
cutoff_bp = [0.3, 0.6];
cutoff_hp = 0.6;
w = kaiser(Order+1, beta_kaiser);

% Lowpass filter (H0)
H0 = fir1(Order, cutoff_lp, 'low', w, 'scale');

% Bandpass filter (H1)
H1 = fir1(Order, cutoff_bp, 'bandpass', w, 'scale');

% Highpass filter (H2)
H2 = fir1(Order, cutoff_hp, 'high', w, 'scale');


%% 3) Analysis 
X0 = conv(x, H0, 'same');
X1 = conv(x, H1, 'same');
X2 = conv(x, H2, 'same');




%% 4) Expansion & Decimation
V0 = downsample(X0, M);
V1 = downsample(X1, M);
V2 = downsample(X2, M);

U0 = upsample(V0, M);
U1 = upsample(V1, M);
U2 = upsample(V2, M);


%% 5) Synthesis Filters
% In this example, we use the same filters for synthesis
F0 = H0;
F1 = H1;
F2 = H2;

Z0 = conv(U0, F0, 'same');
Z1 = conv(U1, F1, 'same');
Z2 = conv(U2, F2, 'same');

% Combine outputs from all channels
x_hat = Z0 + Z1 + Z2;

%% 6) Gain Compensation
if max(x_hat) ~= 0
    gain = max(x) / max(x_hat);
else
    gain = 1;
end

x_hat_compensated = gain * x_hat;

%% 7) Error Calculation and Plots
min_len = min(length(x), length(x_hat_compensated));
e = x(1:min_len) - x_hat_compensated(1:min_len);

MAE = mean(abs(e));
MSE = mean(e.^2);

fprintf('MSE (Compensated): %g\n', MSE);

% Plot signals in subplots
figure('Units','normalized','Position',[0.1 0.1 0.6 0.8]);

subplot(3,1,1)
plot(x, 'b','LineWidth',1.2);
title('Original Signal');
xlabel('Sample');
ylabel('Amplitude');
grid on;

subplot(3,1,2)
plot(x_hat, 'g','LineWidth',1.2);
title('Reconstructed Signal (no gain compensation)');
xlabel('Sample');
ylabel('Amplitude');
grid on;

subplot(3,1,3)
plot(x_hat_compensated, 'r','LineWidth',1.2);
title('Compensated Reconstructed Signal');
xlabel('Sample');
ylabel('Amplitude');
grid on;

% Comparison on one figure
figure('Units','normalized','Position',[0.2 0.2 0.5 0.4]);
plot(x, 'b','LineWidth',1.2);
hold on;
plot(x_hat_compensated, '--r','LineWidth',1.2);
title('Original vs. Compensated Reconstructed');
xlabel('Sample');
ylabel('Amplitude');
legend('Original','Compensated Reconstructed');
grid on;
