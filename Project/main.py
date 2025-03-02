import numpy as np
import pywt
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  
import os 




def welcome_window():
    root = tk.Tk()
    root.title("Optimal Wavelet Selection for Signal Denoising")
    root.geometry("600x500")
    
    top_frame = tk.Frame(root)
    top_frame.pack(side="top", fill="x", pady=10)
    
    try:
       
        gif_path = "E:\github\Advanced-Digital-Signal-Processing\Project\WwjV1.gif"  # نام فایل GIF متحرک شما
        pil_img = Image.open(gif_path)
        frames = []
        try:
            while True:
                frames.append(ImageTk.PhotoImage(pil_img.copy()))
                pil_img.seek(len(frames)) 
        except EOFError:
            pass  

       
        animated_label = tk.Label(top_frame)
        animated_label.pack(side="top")
        
        
        def update(ind):
            frame = frames[ind]
            ind = (ind + 1) % len(frames)
            animated_label.configure(image=frame)
            root.after(100, update, ind)  

        
        root.after(0, update, 0)
    except Exception as e:
        print("Error loading animated GIF:", e)
    
    
    main_frame = tk.Frame(root)
    main_frame.pack(expand=True)
    
    welcome_label = tk.Label(main_frame, text="Optimal Wavelet Selection for Signal Denoising", 
                             font=("Helvetica", 16, "bold"))
    welcome_label.pack(pady=10)
    
    
    instruction_label = tk.Label(main_frame, text="Please select your noisy signal", 
                                 font=("Helvetica", 14))
    instruction_label.pack(pady=10)
    
    select_btn = tk.Button(main_frame, text="Select File", font=("Helvetica", 14), command=lambda: select_file(root))
    select_btn.pack(pady=20)
    
    
    credit_label = tk.Label(main_frame, text="Created by Mohammad Reza Mansouri", 
                            font=("Helvetica", 12), fg="blue")
    credit_label.pack(pady=5)
    
    root.mainloop()

def select_file(parent):
    file_path = filedialog.askopenfilename(parent=parent, filetypes=[("Data Files", "*.asc *.dat *.txt")])
    if not file_path:
        messagebox.showinfo("No File Selected", "No file was selected. Please try again.")
        return
    
   
    file_name = os.path.basename(file_path)
    
   
    data = np.loadtxt(file_path)
    data = data.flatten()
    wave_family = wavespace()
    nw = 5
    try:
        optimal_waves = optimalwavelets(data, wave_family, nw)
    except Exception as e:
        messagebox.showerror("Processing Error", str(e))
        return

   
    show_results(optimal_waves, file_name)


def show_results(optimal_waves, file_name):
    """نمایش موجک‌های بهینه در یک پنجره گرافیکی با استفاده از لیست‌باکس."""
    result_win = tk.Toplevel()
    result_win.title("Optimal Wavelets")
    result_win.geometry("500x350")
    
    
    
    file_label = tk.Label(result_win, text=f"Selected File: {file_name}", font=("Helvetica", 12, "bold"), fg="red")
    file_label.pack(pady=10)

    header = tk.Label(result_win, text="Optimal Wavelets:", font=("Helvetica", 14, "bold"))
    header.pack(pady=10)

    listbox = tk.Listbox(result_win, font=("Helvetica", 12))
    listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    for wave, level, mean_sc in optimal_waves:
        listbox.insert(tk.END, f"Wavelet: {wave}, Level: {level}, Mean SC: {mean_sc:.4f}")

    close_btn = tk.Button(result_win, text="Close", command=result_win.destroy)
    close_btn.pack(pady=10)






def optimalwavelets(X, wave_family, nw):
    """
    انتخاب موجک‌های بهینه برای داده X با استفاده از خانواده موج.
    
    ورودی‌ها:
      X           : آرایه یک‌بعدی داده
      wave_family : لیست نام موج‌ها (به صورت رشته)
      nw          : تعداد موج‌های بهینه مورد نظر
      
    خروجی:
      لیستی از تاپل‌ها به شکل (نام موج، سطح تجزیه، تغییر میانگین اسپارسیتی)
    """
    wl = len(wave_family)
    N = int(np.floor(np.log2(len(X))))
    
    app_coef, det_coef, N = wavecoef(X, wave_family, N)
    
    effective_levels = []
    ratio_level = np.zeros((wl, N))
    for i in range(wl):
        try:
            filt_length = len(pywt.Wavelet(wave_family[i]).dec_lo)
        except ValueError:
            raise ValueError("Wavelet {} not found in pywt library.".format(wave_family[i]))
        
        N_ratio = 0
        r = float('inf')
        for j in range(N):
            if r > 1.5 and N_ratio < N:
                N_ratio += 1
                if j < len(det_coef[i]):
                    r = len(det_coef[i][j]) / filt_length
                    ratio_level[i, N_ratio-1] = r
                else:
                    break
        effective_level = N_ratio - 1
        effective_levels.append(effective_level)

    spar = Sparsity(det_coef, wl, N)
    spar_change = SparsityChange(spar, wl, N)
    decom_level = Decomlevel(spar_change, wl, N)
    mu_sc = Meansc(spar, decom_level, wl, N)
    
    mu_sc = np.array(mu_sc)
    sorted_indices = np.argsort(-mu_sc)
    selected = []
    for k in range(nw):
        ind = sorted_indices[k]
        selected.append((wave_family[ind], decom_level[ind], mu_sc[ind]))
        
    return selected




def wavespace():
    """
    ایجاد فضای موج شامل خانواده‌های مختلف موج.
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
    محاسبه ضرایب تقریب و جزئیات برای هر موج در خانواده موج.
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
        details = coeffs[1:][::-1]
        det_coef.append(details)
        app_coef.append(coeffs[0])
    return app_coef, det_coef, N




def Sparsity(c, m, n):
    """
    محاسبه اسپارسیتی ضرایب جزئیات در هر سطح.
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
    محاسبه تغییر اسپارسیتی بین سطوح مختلف.
    """
    sc = np.zeros((m, n))
    for i in range(m):
        for j in range(1, n):
            sc[i, j] = s[i, j] - s[i, j-1]
    return sc



def Decomlevel(sc, m, n):
    """
    تعیین سطح تجزیه‌ای که تغییر اسپارسیتی از ۵٪ بیشتر می‌شود.
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
    محاسبه تغییر میانگین اسپارسیتی از سطح دوم تا سطح تجزیه.
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



if __name__ == "__main__":
    welcome_window()
