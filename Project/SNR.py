import numpy as np
import matplotlib.pyplot as plt


scan1 = np.loadtxt('sig_5.txt')
scan4 = np.loadtxt('sig_10.txt')
scan500 = np.loadtxt('sig_30.txt')


if scan1.ndim == 1:
    data1 = scan1
else:
    data1 = scan1[:, 0]

if scan4.ndim == 1:
    data4 = scan4
else:
    data4 = scan4[:, 0]

if scan500.ndim == 1:
    data500 = scan500
else:
    data500 = scan500[:, 0]

# Create the x-axis data based on the range of the first dataset
x_scan = np.linspace(np.min(data1), np.max(data1), len(data1))

# Plot the signals with different colors and line widths
plt.figure()

plt.plot(x_scan, data1, 'b', linewidth=1, label='SNR=5')
plt.plot(x_scan, data4, 'k', linewidth=1, label='SNR=10')
plt.plot(x_scan, data500, 'r', linewidth=1.5, label='SNR=30')

plt.xlabel('Magnetic Field Strength (Gauss)')
plt.ylabel('Amplitude (a.u.)')
plt.legend()
plt.title('(a) Commercial Spectrometer')
plt.show()
