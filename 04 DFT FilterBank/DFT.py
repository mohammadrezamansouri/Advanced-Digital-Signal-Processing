import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz, upfirdn

# Parameters
M = 4
N = 256
n = np.arange(-64, 65)

# FIR filter
h0 = np.ones(M)

# Sinc signal
x = np.sinc(n / 8)

# --- Method 1: Downsample -> Filter with Shifted Signal ---
y_subbands = []
x_shifted = x.copy()

for m in range(M):
    hm = h0[np.mod(np.arange(len(h0)), M) == m]
    x_decimated = x_shifted[::M]
    y_filtered = np.convolve(x_decimated, hm, mode='same')
    x_shifted = np.concatenate(([0], x_shifted[:-1]))
    y_subbands.append(y_filtered)

# Matrix W
W = np.exp(-1j * 2 * np.pi * np.outer(np.arange(M), np.arange(M)) / M)

# Combine subband outputs into a matrix
Y = np.zeros((M, len(y_subbands[0])), dtype=complex)
for m in range(M):
    Y[m, :] = y_subbands[m]

Y_transformed = W @ Y

# Display results
plt.figure()
for m in range(M):
    plt.subplot(M, 1, m + 1)
    plt.plot(np.abs(Y_transformed[m, :]), linewidth=1.5)
    plt.title(f'Subband {m + 1} after applying W')
    plt.xlabel('Samples')
    plt.ylabel('|Amplitude|')
    plt.grid()

# --- Method 2: Upsample -> Filter -> Downsample ---
x_shifted2 = x.copy()
y_subbands2 = []
for m in range(M):
    hm2 = h0[np.mod(np.arange(len(h0)), M) == m]
    hm_upsampled = upfirdn([1], hm2, M)
    y_filtered2 = np.convolve(x_shifted2, hm_upsampled, mode='same')
    x_shifted2 = np.concatenate(([0], x_shifted2[:-1]))
    y_decimated2 = y_filtered2[::M]
    y_subbands2.append(y_decimated2)

# Matrix W
W2 = np.exp(-1j * 2 * np.pi * np.outer(np.arange(M), np.arange(M)) / M)

# Combine subband outputs into a matrix
Y2 = np.zeros((M, len(y_subbands2[0])), dtype=complex)
for m in range(M):
    Y2[m, :] = y_subbands2[m]

Y_transformed2 = W2 @ Y2

# Display results
plt.figure()
for m in range(M):
    plt.subplot(M, 1, m + 1)
    plt.plot(np.abs(Y_transformed2[m, :]),'r', linewidth=1.5)
    plt.title(f'Subband {m + 1} after applying W')
    plt.xlabel('Samples')
    plt.ylabel('|Amplitude|')
    plt.grid()

# Error calculation
error = np.abs(Y_transformed - Y_transformed2)
mse_error = np.mean(error**2)
print(f"Mean Squared Error (MSE) between Method 1 and Method 2: {mse_error}")

plt.figure()
for m in range(M):
    plt.subplot(M, 1, m + 1)
    plt.plot(np.abs(Y_transformed[m, :]), 'g', linewidth=1.5, label='Method 1')
    plt.plot(np.abs(Y_transformed2[m, :]), 'r--', linewidth=1.5, label='Method 2')
    plt.title(f'Subband {m + 1} Comparison')
    plt.xlabel('Samples')
    plt.ylabel('|Amplitude|')
    plt.legend()
    plt.grid()

plt.figure()
for m in range(M):
    plt.subplot(M, 1, m + 1)
    plt.plot(error[m, :], 'k', linewidth=1.5)
    plt.title(f'Error in Subband {m + 1}')
    plt.xlabel('Samples')
    plt.ylabel('Error')
    plt.grid()

# FFT for frequency
XF = np.fft.fftshift(np.fft.fft(x, N))

# Frequency response
H, w = freqz(h0, worN=N)
H_shifted = np.fft.fftshift(H)
w_shifted = np.linspace(-np.pi, np.pi, N)

# Plot 1: FIR filter response
plt.figure()
plt.subplot(2, 1, 1)
plt.stem(np.arange(M), h0, 'r', basefmt=" ", use_line_collection=True)
plt.title('Impulse Response of FIR Prototype Filter')
plt.xlabel('n')
plt.ylabel('h_0[n]')
plt.grid()
plt.xlim([-3, M + 3])
plt.ylim([0, 1.2])

plt.subplot(2, 1, 2)
H_fft = np.fft.fftshift(np.fft.fft(h0, N))
plt.plot(w_shifted / np.pi, np.abs(H_fft), 'b', linewidth=1.5)
plt.title('Magnitude Response of FIR Prototype Filter')
plt.xlabel('Normalized Frequency (ω / π)')
plt.ylabel('|H(ω)|')
plt.grid()

# Plot 2: Input signal
plt.figure()
plt.subplot(2, 1, 1)
plt.stem(n, x, 'r', basefmt=" ", use_line_collection=True)
plt.title('Input Signal (Sinc) in Time Domain')
plt.xlabel('n')
plt.ylabel('x[n]')
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(w_shifted / np.pi, np.abs(XF), 'r', linewidth=1.5)
plt.title('Input Signal in Frequency Domain')
plt.xlabel('Normalized Frequency (ω / π)')
plt.ylabel('|X(ω)|')
plt.grid()
plt.show()
