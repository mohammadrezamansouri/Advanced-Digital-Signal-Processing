import numpy as np
from scipy.signal import butter, lfilter
import sounddevice as sd
import matplotlib.pyplot as plt

def butter_lowpass_filter(data, cutoff, fs, order=4):
    nyquist = fs / 2
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, data)

def upsample_audio(x, fs, L):
    y_upsampled = np.zeros(len(x) * L)
    y_upsampled[::L] = x

    cutoff = fs / (2 * L)
    y_filtered = butter_lowpass_filter(y_upsampled, cutoff, fs * L)

    inserted_indices = np.setdiff1d(np.arange(len(y_upsampled)), np.arange(len(x)) * L)


    fig, axs = plt.subplots(2, 1, figsize=(12, 8))


    axs[0].stem(np.arange(len(x)), x, linefmt='blue', markerfmt='bo', basefmt='gray', label='Original Signal')
    axs[0].set_title('Original Signal (Before Upsampling)')
    axs[0].set_xlabel('Sample Index')
    axs[0].set_ylabel('Amplitude')
    axs[0].legend()


    axs[1].stem(np.arange(len(y_filtered)), y_filtered, linefmt='blue', markerfmt='bo', basefmt='gray', label='Filtered Original Signal')
    axs[1].stem(inserted_indices, y_filtered[inserted_indices], linefmt='green', markerfmt='go', basefmt='gray', label='Inserted Samples (After Filtering)')
    axs[1].set_title(f'Upsampled Signal (Factor = {L}, After Filtering)')
    axs[1].set_xlabel('Sample Index')
    axs[1].set_ylabel('Amplitude')
    axs[1].legend()

    plt.tight_layout()
    plt.show()

    print("Playing original signal...")
    sd.play(x, fs)
    sd.wait()

    print("Playing upsampled signal (after filtering)...")
    sd.play(y_filtered, fs * L)
    sd.wait()

def downsample_audio(x, fs, M):
    cutoff = fs / (2 * M)  # Cutoff frequency for anti-aliasing
    y_filtered = butter_lowpass_filter(x, cutoff, fs)  # Apply low-pass filter
    y_downsampled = y_filtered[::M]  # Downsample the filtered signal

    original_indices = np.arange(len(x))
    downsampled_indices = original_indices[::M]
    removed_indices = np.setdiff1d(original_indices, downsampled_indices)

    plt.figure(figsize=(10, 6))

    plt.subplot(2, 1, 1)
    plt.stem(original_indices, x, linefmt='blue', markerfmt='bo', basefmt='gray', label='Original Signal')
    plt.title('Original Signal')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.stem(original_indices, y_filtered, linefmt='blue', markerfmt='bo', basefmt='gray', label='Filtered Signal')
    plt.stem(downsampled_indices, y_downsampled, linefmt='green', markerfmt='go', basefmt='gray', label='Retained Samples')
    plt.stem(removed_indices, y_filtered[removed_indices], linefmt='red', markerfmt='ro', basefmt='gray', label='Removed Samples')
    plt.title(f'Downsampled Signal (Factor = {M})')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.tight_layout()
    plt.show()

    print("Playing original signal...")
    sd.play(x, fs)
    sd.wait()

    print("Playing downsampled signal...")
    sd.play(y_downsampled, fs // M)
    sd.wait()

def fractional_resample(x, fs, numerator, denominator):
    y_upsampled = np.zeros(len(x) * numerator)
    y_upsampled[::numerator] = x
    cutoff = fs / (2 * numerator)
    y_filtered = butter_lowpass_filter(y_upsampled, cutoff, fs * numerator)
    y_resampled = y_filtered[::denominator]

    plt.figure()
    plt.subplot(3, 1, 1)
    plt.plot(x, label='Original Signal')
    plt.title('Original Signal')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(y_filtered, label='After Upsampling and Filtering')
    plt.title('After Upsampling and Filtering')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.stem(y_resampled, linefmt='yellow', markerfmt='yo', basefmt='gray', label=f'Fractionally Resampled Signal (Rate = {numerator}/{denominator})')
    plt.title(f'Fractionally Resampled Signal (Rate = {numerator}/{denominator})')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.tight_layout()
    plt.show()

    print("Playing original signal...")
    sd.play(x, fs)
    sd.wait()

    print("Playing fractionally resampled signal...")
    sd.play(y_resampled, fs * numerator / denominator)
    sd.wait()
