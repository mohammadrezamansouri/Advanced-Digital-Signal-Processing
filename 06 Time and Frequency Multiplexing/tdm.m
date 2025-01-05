clc
clear
close

N = 30;                  
n = 0:N-1;

% three different signal
x0 = sin(2*pi*0.1*n);         
x1 = sin(2*pi*0.1*n + pi/4);   
x2 = sin(2*pi*0.2*n);          


% Upsample by factor 3
x0_u = upsample(x0, 3); 
x1_u = upsample(x1, 3);
x2_u = upsample(x2, 3);


%  delays z^-1:
x1_d = [0, x1_u(1:end-1)];     
x2_d = [0, 0, x2_u(1:end-2)];   


% Create TDM signal
y = x0_u + x1_d + x2_d;



% Demultiplex 
x0_rec = downsample(y, 3, 0); 
x1_rec = downsample(y, 3, 1); 
x2_rec = downsample(y, 3, 2); 




% --------------------------------------------------------------
%  Plotting
% --------------------------------------------------------------


fs = 12;         
lw = 1.5;        
markerSize = 6;


figure('Name','Original Signals','NumberTitle','off','Color','w');
subplot(3,1,1);
plot(n, x0, 'r-o', 'LineWidth', lw, 'MarkerSize', markerSize, 'MarkerFaceColor','r');
grid on;
title('Original x0','FontSize',fs);
xlabel('n','FontSize',fs); ylabel('Amplitude','FontSize',fs);

subplot(3,1,2);
plot(n, x1, 'g-s', 'LineWidth', lw, 'MarkerSize', markerSize, 'MarkerFaceColor','g');
grid on;
title('Original x1','FontSize',fs);
xlabel('n','FontSize',fs); ylabel('Amplitude','FontSize',fs);

subplot(3,1,3);
plot(n, x2, 'b-^', 'LineWidth', lw, 'MarkerSize', markerSize, 'MarkerFaceColor','b');
grid on;
title('Original x2','FontSize',fs);
xlabel('n','FontSize',fs); ylabel('Amplitude','FontSize',fs);

sgtitle('Original Input Signals','FontSize',fs+2);




figure('Name','Upsampled and Delayed Signals','NumberTitle','off','Color','w');
subplot(3,1,1);
stem(x0_u, 'r', 'LineWidth', lw, 'Marker','o','MarkerFaceColor','r');
grid on;
title('Upsampled x0','FontSize',fs);
xlabel('n','FontSize',fs); ylabel('Amp','FontSize',fs);

subplot(3,1,2);
stem(x1_d, 'g', 'LineWidth', lw, 'Marker','s','MarkerFaceColor','g');
grid on;
title('Delayed x1','FontSize',fs);
xlabel('n','FontSize',fs); ylabel('Amp','FontSize',fs);

subplot(3,1,3);
stem(x2_d, 'b', 'LineWidth', lw, 'Marker','^','MarkerFaceColor','b');
grid on;
title('Delayed x2','FontSize',fs);
xlabel('n','FontSize',fs); ylabel('Amp','FontSize',fs);

sgtitle('Upsampled and Delayed Signals','FontSize',fs+2);



figure('Name','TDM Signal','NumberTitle','off','Color','w');
stem(y, 'k', 'LineWidth', lw, 'Marker','o','MarkerFaceColor','k');
grid on;
title('TDM Output Signal (y)','FontSize',fs);
xlabel('n','FontSize',fs); ylabel('Amplitude','FontSize',fs);




figure('Name','Recovered Signals','NumberTitle','off','Color','w');
subplot(3,1,1);
plot(x0_rec, 'r-o', 'LineWidth', lw, 'MarkerSize', markerSize, 'MarkerFaceColor','r');
grid on;
title('Recovered x0','FontSize',fs);
xlabel('n','FontSize',fs); ylabel('Amplitude','FontSize',fs);

subplot(3,1,2);
plot(x1_rec, 'g-s', 'LineWidth', lw, 'MarkerSize', markerSize, 'MarkerFaceColor','g');
grid on;
title('Recovered x1','FontSize',fs);
xlabel('n','FontSize',fs); ylabel('Amplitude','FontSize',fs);

subplot(3,1,3);
plot(x2_rec, 'b-^', 'LineWidth', lw, 'MarkerSize', markerSize, 'MarkerFaceColor','b');
grid on;
title('Recovered x2','FontSize',fs);
xlabel('n','FontSize',fs); ylabel('Amplitude','FontSize',fs);

sgtitle('Recovered Signals','FontSize',fs+2);



% Compare original and recovered signals 
mse_x0 = mean((x0 - x0_rec).^2);
mse_x1 = mean((x1 - x1_rec).^2);
mse_x2 = mean((x2 - x2_rec).^2);

disp('Mean Squared Error between original and recovered:');
disp(['x0 MSE: ' num2str(mse_x0)]);
disp(['x1 MSE: ' num2str(mse_x1)]);
disp(['x2 MSE: ' num2str(mse_x2)]);

