import numpy as np
import matplotlib.pyplot as plt

def generate_leleccum_signal(length=3450):
    """Generate a synthetic signal similar to leleccum"""
    t = np.linspace(0, 10, length)
    
    # Create signal components
    component1 = np.sin(2 * np.pi * 2 * t)  # Low frequency component
    component2 = 0.5 * np.sin(2 * np.pi * 15 * t)  # Medium frequency component
    component3 = 0.2 * np.random.randn(length)  # Noise component
    chirp = 0.3 * np.sin(2 * np.pi * (5 + t**2) * t)  # Chirp component
    
    # Combine components
    signal = component1 + component2 + component3 + chirp
    return signal

# Generate synthetic signal
leleccum = generate_leleccum_signal()

# Select signal segment (Python uses 0-based indexing)
indx_start = 2000  # Original MATLAB index (1-based)
indx_end = 3450    # Python will exclude the end index
signal = leleccum[indx_start-1:indx_end]  # Adjust for 0-based indexing

# Create noisy signal (add actual noise if needed)
noise_level = 0.2  # Adjust this parameter to control noise level
noisy_signal = signal + noise_level * np.random.randn(len(signal))

# Plot signals
plt.figure(figsize=(10, 6))

# Plot original signal
plt.subplot(2, 1, 1)
plt.plot(signal, linewidth=1.5)
plt.title('Original Synthetic Signal')
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.grid(True)

# Plot noisy signal
plt.subplot(2, 1, 2)
plt.plot(noisy_signal, linewidth=1.5)
plt.title('Noisy Signal (SNR = {} dB)'.format(round(20*np.log10(np.std(signal)/np.std(noisy_signal-signal)), 1)))
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.grid(True)

plt.tight_layout()
plt.show()

# Save noisy signal to text file
np.savetxt('leleccum_noisy_signal.txt', noisy_signal, fmt='%.6f')

print('Noisy signal saved to leleccum_noisy_signal.txt')