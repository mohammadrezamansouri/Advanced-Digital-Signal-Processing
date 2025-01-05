clc;
close all;
clear;


%% Filter H
wp_H = 0.09;
ws_H = 0.11;
delta1_H = 0.02;
delta2_H = 0.001;
[h_H, H_H, w_H, N_H] = design_kaiser_filter(wp_H, ws_H, delta1_H, delta2_H);
fprintf('Filter H - Order: %d\n', N_H);

%% Filter G
wp_G = 0.18;
ws_G = 0.22;
delta1_G = 0.01;
delta2_G = 0.001;
[h_G, H_G, w_G, N_G] = design_kaiser_filter(wp_G, ws_G, delta1_G, delta2_G);
fprintf('Filter G - Order: %d\n', N_G);

%% Filter I 
wp_I = 0.09;
ws_I = 0.89;
delta1_I = 0.01;
delta2_I = 0.001;
[h_I, H_I, w_I, N_I] = design_kaiser_filter(wp_I, ws_I, delta1_I, delta2_I);
fprintf('Filter I - Order: %d\n', N_I);


%% Upsampling G(z) to G(z^2)
h_G_upsampled = upsample(h_G, 2); % Upsample G by a factor of 2
[H_G2, w_G2] = freqz(h_G_upsampled, 1, 1024);


%% Combined Response with G(z^2) and I(z)
h_combined_G2 = conv(h_G_upsampled, h_I); % Combine G(z^2) and I(z)
[H_combined_G2, w_combined_G2] = freqz(h_combined_G2, 1, 1024);


%% Error Calculation
error_response = abs(H_H) - abs(H_combined_G2(1:length(H_H)));
mse_error = mean(error_response.^2);
fprintf('Mean Squared Error (MSE) Between Filter H and Combined G+I: %e\n', mse_error);


%% Plots for All Filters
figure;
subplot(5,1,1);
plot(w_H/pi, 20*log10(abs(H_H)), 'LineWidth', 1.5);
title('Frequency Response of Filter H(z)');
xlabel('Normalized Frequency (\pi rad/sample)');
ylabel('Magnitude (dB)');
grid on;
ylim([-100 10]);

subplot(5,1,2);
plot(w_G/pi, 20*log10(abs(H_G)), 'LineWidth', 1.5);
title('Frequency Response of Filter G(z)');
xlabel('Normalized Frequency (\pi rad/sample)');
ylabel('Magnitude (dB)');
grid on;
ylim([-100 10]);

subplot(5,1,3);

plot(w_G2/pi, 20*log10(abs(H_G2)), 'LineWidth', 1.5);
title('Frequency Response of Upsampled Filter G(z^2)');
xlabel('Normalized Frequency (\pi rad/sample)');
ylabel('Magnitude (dB)');
grid on;
ylim([-100 10]);


subplot(5,1,4);
plot(w_I/pi, 20*log10(abs(H_I)), 'LineWidth', 1.5);
title('Frequency Response of Filter I(z)');
xlabel('Normalized Frequency (\pi rad/sample)');
ylabel('Magnitude (dB)');
grid on;
ylim([-100 10]);

subplot(5,1,5);
plot(w_combined_G2/pi, 20*log10(abs(H_combined_G2)), 'LineWidth', 1.5);
title('Combined Response of G(z^2) and I(z)');
xlabel('Normalized Frequency (\pi rad/sample)');
ylabel('Magnitude (dB)');
grid on;
ylim([-100 10]);

