import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve, firwin

# Generate Input Signal 
Fs = 100
t = np.arange(-5, 5 + 1/Fs, 1/Fs)
x = np.sin(np.pi * t)

 # filter 
Order = 64
H0 = firwin(Order + 1, 0.5, window=('kaiser', 0.5))
n = np.arange(Order + 1)
H1 = ((-1) ** n) * H0

# Apply Analysis Filters 
X0 = convolve(x, H0, mode='same')
X1 = convolve(x, H1, mode='same')

# Downsampling
V0 = X0[::2]
V1 = X1[::2]

# Upsampling
Y0 = np.zeros(len(V0) * 2)
Y0[::2] = V0
Y1 = np.zeros(len(V1) * 2)
Y1[::2] = V1
 # Define Synthesis Filters %%% 
F0 = H0
F1 = -H1
 # Apply Synthesis Filters using conv %%%
Z0 = convolve(Y0, F0, mode='same')
Z1 = convolve(Y1, F1, mode='same')

 # Reconstruct the Signal %%%
x_hat = Z0 + Z1

  # Apply Compensation %%%
x_hat_compensated = (np.max(x) / np.max(x_hat)) * x_hat

  # Calculate Error After Compensation %%%
e_compensated = x - x_hat_compensated[: len(x)]
MAE_compensated = np.mean(np.abs(e_compensated))
MSE_compensated = np.mean(e_compensated**2)

print(f'Mean Absolute Error (MAE) After Compensation: {MAE_compensated}')
print(f'Mean Squared Error (MSE) After Compensation: {MSE_compensated}')

# Plot Reconstructed Signal After Compensation
plt.figure()
plt.subplot(3, 1, 1)
plt.plot(x, 'b', linewidth=3)
plt.title('Original Signal')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')

plt.subplot(3, 1, 2)
plt.plot(x_hat, 'g', linewidth=3)
plt.title('Reconstructed Signal')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')

plt.subplot(3, 1, 3)
plt.plot(x_hat_compensated, 'r', linewidth=3)
plt.title('Compensated Reconstructed Signal (c*x)')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.tight_layout()
plt.show()

# vs
plt.figure()
plt.plot(x, 'b', linewidth=1.5)  # Original Signal
plt.plot(x_hat_compensated, 'r--', linewidth=1.5)  # Compensated Reconstructed Signal
plt.title('Original vs Compensated Reconstructed Signal')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.legend(['Original Signal', 'Compensated Reconstructed Signal'])
plt.grid(True)
plt.show()

# plot Frequency Responses of H0 and H1 
N_fft = 1024
H0_fft = np.fft.fft(H0, n=N_fft)
H1_fft = np.fft.fft(H1, n=N_fft)
H0_fft_shifted = np.fft.fftshift(H0_fft)
H1_fft_shifted = np.fft.fftshift(H1_fft)
f = np.linspace(-0.5, 0.5, N_fft)
H0_mag = np.abs(H0_fft_shifted)
H1_mag = np.abs(H1_fft_shifted)

plt.figure()
plt.subplot(2, 1, 1)
plt.plot(f, H0_mag, 'b', linewidth=1.5)
plt.title('Magnitude Response of H0')
plt.xlabel('Normalized Frequency (×π rad/sample)')
plt.ylabel('Magnitude')
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(f, H1_mag, 'r', linewidth=1.5)
plt.title('Magnitude Response of H1')
plt.xlabel('Normalized Frequency (×π rad/sample)')
plt.ylabel('Magnitude')
plt.grid(True)
plt.tight_layout()
plt.show()
