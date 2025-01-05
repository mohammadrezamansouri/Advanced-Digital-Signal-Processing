clc;
clear;
close all;

% Generate Input Signal
Fs = 100;                      
t = -5:1/Fs:5;             
x = sin(pi*t); 


% Filter
Order = 64;
H0 = fir1(Order, 0.5, kaiser(Order+1, 0.5)); 

% Polyphase 
E0 = H0(1:2:end);  
E1 = H0(2:2:end);  



%%% Analysis Bank %%%

x_even = downsample(x, 2); 
x_odd = downsample([0, x(1:end-1)], 2); 

y_even = conv(x_even, E0, 'same');
y_odd = conv(x_odd, E1, 'same'); 

y0 = y_even;
y1 = y_odd;

% [1 1 ;1 -1]
v0= y0+y1;
v1=y0-y1;



%%% Synthesis Bank %%%

% [1 1 ;1 -1]
w0=v0+v1;
w1=v0-v1;

z0= conv(w0, E1, 'same'); 
z1 = conv(w1, E0, 'same'); 

% up
z0_up = upsample(z0, 2); 
z1_up = upsample(z1, 2);


% Apply Delay
z0_up = [0, z0_up(1:end-1)]; 

% Combine Outputs
x_hat = z0_up + z1_up;

%%% Apply Compensation %%%
x_hat_compensated = (max(x)/max(x_hat))*x_hat;


%%% Error Calculation %%%
error = x - x_hat_compensated(1:length(x));
MSE = mean(error.^2);

fprintf('Mean Squared Error (MSE): %g\n', MSE);


% Plot 
figure;
subplot(3,1,1); 
plot(x, 'LineWidth', 3); 
title('Original Signal'); 
xlabel('Sample Index'); ylabel('Amplitude');

subplot(3,1,2); 
plot(x_hat, 'g', 'LineWidth', 3); 
title('Reconstructed Signal'); 
xlabel('Sample Index'); ylabel('Amplitude');

subplot(3,1,3); 
plot(x_hat_compensated, 'r', 'LineWidth', 3); 
title('Compensated Reconstructed Signal (c*x)'); 
xlabel('Sample Index'); ylabel('Amplitude');


% vs
figure;
plot(x, 'b', 'LineWidth', 1.5); 
hold on;
plot(x_hat_compensated, 'r--', 'LineWidth', 1.5);
title('Original vs Compensated Reconstructed Signal');
xlabel('Sample Index');
ylabel('Amplitude');
legend('Original Signal', 'Compensated Reconstructed Signal');
grid on;

