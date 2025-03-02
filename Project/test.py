import numpy as np
import pywt
import matplotlib.pyplot as plt

def load_signal(filename):
    """Load a signal from a text file and ensure it is a 1D array."""
    X = np.loadtxt(filename)
    if X.ndim > 1:
        X = X.ravel()
    return X

def wavespace():
    """
    Create a wavelet space including different wavelet families.
    """
    wave_bior = ["bior1.1", "bior1.3", "bior1.5", "bior2.2", "bior2.4", "bior2.6"]
    wave_coif = ["coif1", "coif2", "coif3", "coif4", "coif5"]
    wave_db   = ["db2", "db3", "db4", "db5", "db6", "db7", "db8", "db9", "db10", "db11"]
    wave_rbio = ["rbio1.3", "rbio1.5", "rbio2.2", "rbio2.4", "rbio2.6", "rbio2.8"]
    wave_sym  = ["sym2", "sym3", "sym4", "sym5", "sym6", "sym7"]
    wave_family = wave_bior + wave_coif + wave_db + ["dmey"] + wave_rbio + wave_sym
    return wave_family

def wavecoef(X, wave_family, N):
    """
    Compute approximation and detail coefficients for each wavelet in the family.
    
    Inputs:
      X           : 1D data array
      wave_family : List of wavelet names (strings)
      N           : Decomposition level (e.g., floor(log2(len(X))))
      
    Output:
      (approx_coeffs, detail_coeffs, N)
      where detail_coeffs is a list of lists for each wavelet.
    """
    wl = len(wave_family)
    det_coef = []
    app_coef = []
    for i in range(wl):
        wavelet_name = wave_family[i]
        try:
            wavelet = pywt.Wavelet(wavelet_name)
        except ValueError:
            raise ValueError("Wavelet {} not found in pywt.".format(wavelet_name))
        coeffs = pywt.wavedec(X, wavelet, level=N)
        # Reverse the order of detail coefficients (to mimic MATLAB code)
        details = coeffs[1:][::-1]
        det_coef.append(details)
        app_coef.append(coeffs[0])
    return app_coef, det_coef, N

def Sparsity(c, m, n):
    """
    Compute the sparsity of the detail coefficients at each level for each wavelet.
    
    Parameters:
      c : list of detail coefficients for each wavelet
      m : number of wavelets (length of wave_family)
      n : decomposition level (N)
      
    Returns:
      s : an (m x n) array of sparsity values
    """
    s = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            if j < len(c[i]):
                coeff = np.array(c[i][j])
                s[i, j] = np.max(np.abs(coeff)) / np.sum(np.abs(coeff))
            else:
                s[i, j] = 0
    return s

def SparsityChange(s, m, n):
    """
    Compute the change in sparsity between consecutive levels.
    
    Parameters:
      s : sparsity matrix (m x n)
      m : number of wavelets
      n : number of levels
      
    Returns:
      sc : an (m x n) matrix where each entry is the change between levels.
    """
    sc = np.zeros((m, n))
    for i in range(m):
        for j in range(1, n):
            sc[i, j] = s[i, j] - s[i, j-1]
    return sc

def Decomlevel(sc, m, n):
    """
    Determine the decomposition level at which the sparsity change exceeds 5%.
    
    Parameters:
      sc : sparsity change matrix (m x n)
      m  : number of wavelets
      n  : number of levels
      
    Returns:
      dl : an array of decomposition levels (one for each wavelet)
    """
    dl = np.zeros(m, dtype=int)
    for i in range(m):
        d = -1
        for j in range(1, n):
            if sc[i, j] > 0.05:
                d = j
                break
        if d == -1:
            raise ValueError("Error: No change in sparsity of at least five percent detected for wavelet index {}.".format(i))
        dl[i] = d
    return dl

def Meansc(s, dl, m, n):
    """
    Compute the mean sparsity change from the second level up to the decomposition level.
    
    Parameters:
      s  : sparsity matrix (m x n)
      dl : array of decomposition levels for each wavelet
      m  : number of wavelets
      n  : number of levels
      
    Returns:
      msc : an array of mean sparsity change values for each wavelet.
    """
    msc = np.zeros(m)
    for i in range(m):
        if dl[i] == 1:
            msc[i] = s[i, 0]
        else:
            if dl[i] < n:
                msc[i] = (s[i, dl[i]] - s[i, 0]) / (dl[i] - 1)
            else:
                msc[i] = (s[i, -1] - s[i, 0]) / (n - 1)
    return msc

def analysis_stem_plot():
    """
    Load three signals (for SNR 5, 10, and 30), compute the mean sparsity change for each wavelet,
    and display a stem plot comparing the results.
    """
    # Load signals and ensure they are 1D arrays
    X1 = load_signal('sig_5.txt')
    X4 = load_signal('sig_10.txt')
    X500 = load_signal('sig_30.txt')
    
    # Obtain wavelet family and determine the number of wavelets
    wave_family = wavespace()
    m = len(wave_family)
    
    # Determine decomposition level (N) for each signal based on its length
    N1 = int(np.floor(np.log2(len(X1))))
    N4 = int(np.floor(np.log2(len(X4))))
    N500 = int(np.floor(np.log2(len(X500))))
    
    # Compute wavelet coefficients for each signal
    _, det_coef1, N1_used = wavecoef(X1, wave_family, N1)
    _, det_coef4, N4_used = wavecoef(X4, wave_family, N4)
    _, det_coef500, N500_used = wavecoef(X500, wave_family, N500)
    
    # Compute sparsity matrices for each signal
    spar1 = Sparsity(det_coef1, m, N1_used)
    spar4 = Sparsity(det_coef4, m, N4_used)
    spar500 = Sparsity(det_coef500, m, N500_used)
    
    # Compute sparsity change matrices
    sc1 = SparsityChange(spar1, m, N1_used)
    sc4 = SparsityChange(spar4, m, N4_used)
    sc500 = SparsityChange(spar500, m, N500_used)
    
    # Determine decomposition levels for each wavelet
    dl1 = Decomlevel(sc1, m, N1_used)
    dl4 = Decomlevel(sc4, m, N4_used)
    dl500 = Decomlevel(sc500, m, N500_used)
    
    # Compute mean sparsity change for each wavelet
    msc1 = Meansc(spar1, dl1, m, N1_used)
    msc4 = Meansc(spar4, dl4, m, N4_used)
    msc500 = Meansc(spar500, dl500, m, N500_used)
    
    # Create stem plots (x-axis: wavelet index)
    x_indices = np.arange(m)
    plt.figure()
    
    markerline1, stemlines1, _ = plt.stem(x_indices, msc1, linefmt='b-', markerfmt='bo', basefmt=' ')
    plt.setp(stemlines1, linewidth=1.5)
    
    markerline4, stemlines4, _ = plt.stem(x_indices, msc4, linefmt='m-', markerfmt='mo', basefmt=' ')
    plt.setp(stemlines4, linewidth=1.5)
    
    markerline500, stemlines500, _ = plt.stem(x_indices, msc500, linefmt='k-', markerfmt='ko', basefmt=' ')
    plt.setp(stemlines500, linewidth=1.5)
    
    plt.xlabel('Wavelet Index')
    plt.ylabel(r'$\mu_{SC}$')
    plt.title('Stem Plot of Mean Sparsity Change ($\mu_{SC}$) for Each Wavelet')
    plt.legend([markerline1, markerline4, markerline500], ['SNR 5', 'SNR 10', 'SNR 30'])
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    analysis_stem_plot()
