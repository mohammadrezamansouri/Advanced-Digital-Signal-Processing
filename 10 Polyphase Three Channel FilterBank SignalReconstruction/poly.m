clear
close
clc
%%  Input Signal
M = 3;
Fs = 100;
t = -10:1/Fs:10;
x = sin(pi * t);

%% Filters Hk 

N = 500;
b = fir1(N-1, 1/4, 'low', kaiser(N, 10));
h_0 = filter(b, 1, [1; zeros(N-1, 1)]);
h_1 = h_0 .* exp(-1i * (1:length(h_0)) * 2 * pi / 3);
h_2 = h_0 .* exp(+1i * (1:length(h_0)) * 2 * pi / 3);



%% Filters E_00 ... E_22, P
N0 = length(h_0);
N1 = length(h_1);
N2 = length(h_2);

E_00 = zeros(1, ceil(N0/M));
E_01 = zeros(1, ceil(N0/M));
E_02 = zeros(1, ceil(N0/M));

E_10 = zeros(1, ceil(N1/M));
E_11 = zeros(1, ceil(N1/M));
E_12 = zeros(1, ceil(N1/M));

E_20 = zeros(1, ceil(N2/M));
E_21 = zeros(1, ceil(N2/M));
E_22 = zeros(1, ceil(N2/M));

idx_00 = 1; idx_01 = 1; idx_02 = 1;
idx_10 = 1; idx_11 = 1; idx_12 = 1;
idx_20 = 1; idx_21 = 1; idx_22 = 1;


%E00 E01 E02

for i = 1:N0
    if mod(i,M) == 1
        E_00(idx_00) = h_0(i);
        idx_00 = idx_00 + 1;
    elseif mod(i,M) == 2
        E_01(idx_01) = h_0(i);
        idx_01 = idx_01 + 1;
    elseif mod(i,M) == 0
        E_02(idx_02) = h_0(i);
        idx_02 = idx_02 + 1;
    end
end

% E10 E11 E12

for i = 1:N1
    if mod(i,M) == 1
        E_10(idx_10) = h_1(i);
        idx_10 = idx_10 + 1;
    elseif mod(i,M) == 2
        E_11(idx_11) = h_1(i);
        idx_11 = idx_11 + 1;
    elseif mod(i,M) == 0
        E_12(idx_12) = h_1(i);
        idx_12 = idx_12 + 1;
    end
end

% E20 E21 E22 

for i = 1:N2
    if mod(i,M) == 1
        E_20(idx_20) = h_2(i);
        idx_20 = idx_20 + 1;
    elseif mod(i,M) == 2
        E_21(idx_21) = h_2(i);
        idx_21 = idx_21 + 1;
    elseif mod(i,M) == 0
        E_22(idx_22) = h_2(i);
        idx_22 = idx_22 + 1;
    end
end


E = [E_00; E_01; E_02; E_10; E_11; E_12; E_20; E_21; E_22];

R = E';

P = E * R;


%%   Polyphase Three Channel FilterBank SignalReconstruction

x_0=downsample(x,M);
x_1=downsample([0 x(1:end-1)],M);
x_2=downsample([0 0 x(1:end-2)],M);

u_0=conv(x_0,P(1),"same");
u_1=conv(x_1,P(1),"same");
u_2=conv(x_2,P(1),"same");

y_0 = upsample(u_0 ,M);
y_1 = upsample( u_1,M);
y_2 = upsample(u_2 ,M);

y_1= ([0 y_0(1:end-1)] + y_1 );

x_hat =[0 y_1(1:end-1)]+y_2;


%% Compensation

x_hat_compensated = max(x)/max(x_hat)*x_hat;

x_hat_compensated = [x_hat_compensated(3:end) 0 0];

%% MSE


MSE = mean(abs(x_hat_compensated-x).^2);
fprintf("MSE = %g\n", MSE );




%% Plot signals in subplots

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
