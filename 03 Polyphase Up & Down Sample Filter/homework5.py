import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve
from scipy.signal.windows import hamming

def downsampling_fir(Signal, M=2, N_range=(-10, 10)):
    """
    Function to perform downsampling using FIR filter with polyphase decomposition.

    Parameters:
    Signal: Input signal to process
    M: Downsampling factor
    N_range: Range for the filter indices (default is -10:10)

    Returns:
    Y: Downsampled signal using the direct method
    Yn: Output signal from polyphase decomposition
    """
    # Filter index range
    N = np.arange(N_range[0], N_range[1] + 1)

    # Define FIR filter based on sinc with Hamming window
    Filter = np.sinc(N) * hamming(len(N))
    Filter /= np.sum(Filter)  # Normalize the filter

    # Split the filter for even and odd components
    E0 = Filter[::M]
    E1 = Filter[1::M]
    # Downsampling the filters
    E0down = np.zeros(M * len(E0))
    E0down[::M] = E0
    E1down = np.zeros(M * len(E1))
    E1down[::M] = E1

    # Apply convolution for direct method
    Y1 = convolve(Signal, E0down, mode="same")
    Y2 = convolve(np.concatenate([Signal[1:], [0]]), E1down, mode="same")
    Y0 = Y1 + Y2

    # Downsample the combined signal
    Y = Y0[::2]


    # Downsample signal into even and odd components
    X0 = Signal[::M]
    X1 = Signal[1::M]

    # Convolve each part with respective polyphase components
    H0 = convolve(X0, E0, mode='same')
    H1 = convolve(X1, E1, mode='same')

    # Combine results from even and odd paths
    Yn = H0 + H1


    # Plot FIR filter and input signal
    plt.figure(figsize=(10, 6))

    # FIR Filter plot
    plt.subplot(2, 1, 1)
    plt.stem(N, Filter, 'r', linefmt='r-', markerfmt='ro', basefmt=" ")
    plt.title('FIR Filter (Sinc with Hamming)')
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')
    plt.grid(True, which='both', linestyle='--')

    # Input Signal plot
    plt.subplot(2, 1, 2)
    plt.stem(Signal, 'b', linefmt='b-', markerfmt='bo', basefmt=" ")
    plt.title('Input Signal')
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')
    plt.grid(True, which='both', linestyle='--')

    plt.tight_layout()
    plt.show()

    # Plot the output signals
    plt.figure(figsize=(10, 6))

    # Output Signal - Yn plot
    plt.subplot(2, 1, 1)
    plt.stem(Yn, 'm', linefmt='m-', markerfmt='mo', basefmt=" ")
    plt.title('Output Signal - Yn')
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')
    plt.grid(True, which='both', linestyle='--')

    # Output Signal - Y plot
    plt.subplot(2, 1, 2)
    plt.stem(Y, 'c', linefmt='c-', markerfmt='co', basefmt=" ")
    plt.title('Output Signal - Y')
    plt.xlabel('Sample Index')
    plt.ylabel('Amplitude')
    plt.grid(True, which='both', linestyle='--')

    plt.tight_layout()
    plt.show()

    return Y, Yn


# Example usage of the function
Signal = np.random.randn(50)  # Random input signal
Y, Yn = downsampling_fir(Signal)
