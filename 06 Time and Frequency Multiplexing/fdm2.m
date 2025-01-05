clc
clear
close

% Parameters
fs = 1000;             
N = 200;              
n = (0:N-1)';

% three different signal
x0 = sin(2*pi*10*n/fs);     
x1 = sin(2*pi*20*n/fs);     
x2 = sin(2*pi*30*n/fs);     

% Upsample factor
upsample_factor = 4;
X0_u = upsample(x0, upsample_factor);
X1_u = upsample(x1, upsample_factor);
X2_u = upsample(x2, upsample_factor);

Fs_new = fs * upsample_factor;
M = length(X0_u);
m = (0:M-1)';

% Carrier frequencies
f0 = 0;    
f1 = 100;  
f2 = 200;  

% Modulate 
x0_mod = X0_u .* cos(2*pi*f0*m/Fs_new);
x1_mod = X1_u .* cos(2*pi*f1*m/Fs_new);
x2_mod = X2_u .* cos(2*pi*f2*m/Fs_new);



%% FDM signal
y = x0_mod + x1_mod + x2_mod;



%% Filtering and Demodulation

% For x0 Lowpass below ~50 Hz
lp_cutoff = 50/(Fs_new/2); 
% For x1 100 Hz band
bp1_low = 50/(Fs_new/2);  bp1_high = 150/(Fs_new/2);
% For x2 200 Hz band
bp2_low = 150/(Fs_new/2); bp2_high = 250/(Fs_new/2);

% Filter orders
filt_order = 128;

% Design filters using fir1
bpFilt_x0 = fir1(filt_order, lp_cutoff, 'low'); 
bpFilt_x1 = fir1(filt_order, [bp1_low bp1_high]);
bpFilt_x2 = fir1(filt_order, [bp2_low bp2_high]);

% Filter the FDM signal 
y0_band = conv(y, bpFilt_x0, 'same');
y1_band = conv(y, bpFilt_x1, 'same');
y2_band = conv(y, bpFilt_x2, 'same');

% Downconvert each band
x0_rec_u = (y0_band .* cos(2*pi*f0*m/Fs_new))*2;
x1_rec_u = (y1_band .* cos(2*pi*f1*m/Fs_new))*2;
x2_rec_u = (y2_band .* cos(2*pi*f2*m/Fs_new))*2;

% Lowpass filter 

x0_lp = conv(x0_rec_u, bpFilt_x0, 'same');
x1_lp = conv(x1_rec_u, bpFilt_x0, 'same');
x2_lp = conv(x2_rec_u, bpFilt_x0, 'same');

% Downsample back to original rate
x0_rec = downsample(x0_lp, upsample_factor);
x1_rec = downsample(x1_lp, upsample_factor);
x2_rec = downsample(x2_lp, upsample_factor);




% -------------------------------------------------------------------------
% Plotting
% -------------------------------------------------------------------------
fsz = 12;  
lw = 1.5;  

figure('Color','w','Name','Original Signals');
subplot(3,1,1);
plot(n, x0,'r','LineWidth',lw); grid on;
title('Original x0','FontSize',fsz); xlabel('n','FontSize',fsz); ylabel('Amplitude','FontSize',fsz);

subplot(3,1,2);
plot(n, x1,'g','LineWidth',lw); grid on;
title('Original x1','FontSize',fsz); xlabel('n','FontSize',fsz); ylabel('Amplitude','FontSize',fsz);

subplot(3,1,3);
plot(n, x2,'b','LineWidth',lw); grid on;
title('Original x2','FontSize',fsz); xlabel('n','FontSize',fsz); ylabel('Amplitude','FontSize',fsz);

sgtitle('Original Low-Frequency Signals','FontSize',fsz+2);

figure('Color','w','Name','FDM Signal');
plot(m, y, 'k','LineWidth',lw); grid on;
title('FDM Signal (y)','FontSize',fsz);
xlabel('n (after upsampling)','FontSize',fsz); ylabel('Amplitude','FontSize',fsz);

figure('Color','w','Name','Recovered Signals');
subplot(3,1,1);
plot(n, x0_rec,'r','LineWidth',lw); grid on;
title('Recovered x0','FontSize',fsz); xlabel('n','FontSize',fsz); ylabel('Amplitude','FontSize',fsz);

subplot(3,1,2);
plot(n, x1_rec,'g','LineWidth',lw); grid on;
title('Recovered x1','FontSize',fsz); xlabel('n','FontSize',fsz); ylabel('Amplitude','FontSize',fsz);

subplot(3,1,3);
plot(n, x2_rec,'b','LineWidth',lw); grid on;
title('Recovered x2','FontSize',fsz); xlabel('n','FontSize',fsz); ylabel('Amplitude','FontSize',fsz);

sgtitle('Recovered Signals','FontSize',fsz+2);

% Compare original and recovered signals
mse_x0 = mean((x0 - x0_rec).^2);
mse_x1 = mean((x1 - x1_rec).^2);
mse_x2 = mean((x2 - x2_rec).^2);

disp('Mean Squared Error between original and recovered:');
disp(['x0 MSE: ' num2str(mse_x0)]);
disp(['x1 MSE: ' num2str(mse_x1)]);
disp(['x2 MSE: ' num2str(mse_x2)]);
