import librosa
import librosa.display
import numpy as np
from scipy.io.wavfile import write, read
import sounddevice as sd
import time
import sys
import os
from audio_processing import upsample_audio, downsample_audio, fractional_resample  # Import functions
from tkinter import Tk, Label, Button, Entry, StringVar, IntVar, filedialog,Radiobutton
from PIL import Image, ImageTk

# GUI Setup
def process_audio(factor_var=None, fraction_numerator_var=None, fraction_denominator_var=None):
    global x, sr

    operation = operation_var.get()
    try:
        if operation == 1:
            L = int(factor_var.get())
            upsample_audio(x, sr, L)
        elif operation == 2:
            M = int(factor_var.get())
            downsample_audio(x, sr, M)
        elif operation == 3:
            numerator = int(fraction_numerator_var.get())
            denominator = int(fraction_denominator_var.get())
            fractional_resample(x, sr, numerator, denominator)
        else:
            status_var.set("Invalid operation selected.")
    except Exception as e:
        status_var.set(f"Error: {str(e)}")

def load_default_audio():
    global x, sr, status_var
    x, sr = librosa.load(librosa.ex('trumpet'))
    x = x / np.max(np.abs(x))  # نرمال‌سازی سیگنال
    status_var.set("Loaded default audio file (trumpet).")

def load_audio_file():
    global x, sr, status_var
    filepath = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.wav *.mp3 *.flac"), ("All Files", "*.*")]
    )
    if filepath:
        x, sr = librosa.load(filepath, sr=None)
        x = x / np.max(np.abs(x))  # نرمال‌سازی سیگنال
        status_var.set(f"Loaded file: {os.path.basename(filepath)}")

def record_audio():
    global x, sr, status_var
    duration = 3
    sr = 44100
    status_var.set("Recording...")
    audio_data = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype='float32')
    sd.wait()
    x = audio_data.flatten()
    status_var.set("Recording finished.")


def perform_operation():
    global x, sr, status_var
    operation = operation_var.get()

    try:
        if operation == 1:
            if not entry_factor.get().strip():
                raise ValueError("Upsampling factor is required.")
            L = int(entry_factor.get())
            upsample_audio(x, sr, L)
        elif operation == 2:
            if not entry_factor.get().strip():
                raise ValueError("Downsampling factor is required.")
            M = int(entry_factor.get())
            downsample_audio(x, sr, M)
        elif operation == 3:
            if not entry_numerator.get().strip() or not entry_denominator.get().strip():
                raise ValueError("Numerator and denominator are required for fractional resampling.")
            numerator = int(entry_numerator.get())
            denominator = int(entry_denominator.get())
            fractional_resample(x, sr, numerator, denominator)
        else:
            status_var.set("Invalid operation selected.")
    except ValueError as ve:
        status_var.set(f"Input Error: {ve}")
    except Exception as e:
        status_var.set(f"Error: {str(e)}")
# Main Application

root = Tk()
root.title("Audio Processing")
logo_image = Image.open("Persian_Gulf_university_logo.png")
logo_image = logo_image.resize((100, 100))
logo = ImageTk.PhotoImage(logo_image)

logo_label = Label(root, image=logo)
logo_label.pack(pady=10)

status_var = StringVar()
status_var.set("No file loaded.")

Label(root, text="Audio Processing Tool", font=("Arial", 16)).pack()

Button(root, text="Load Audio File", command=load_audio_file).pack(pady=5)
Button(root, text="Load Default Audio", command=load_default_audio).pack(pady=5)
Button(root, text="Record Audio", command=record_audio).pack(pady=5)

operation_var = IntVar()
operation_var.set(1)  # پیش‌فرض: عملیات اول انتخاب شده

Label(root, text="Choose Operation:").pack(pady=5)

Radiobutton(root, text="Up-sample", variable=operation_var, value=1).pack(anchor="w")
Radiobutton(root, text="Down-sample", variable=operation_var, value=2).pack(anchor="w")
Label(root, text="Enter Factor (M or L):").pack(pady=5)

entry_factor = Entry(root)
entry_factor.pack(pady=5)

Radiobutton(root, text="Fractional Resampling", variable=operation_var, value=3).pack(anchor="w")

Label(root, text="Enter numerator:").pack(pady=5)


entry_numerator = Entry(root)
entry_numerator.pack(pady=5)
Label(root, text="Enter denominator:").pack(pady=5)
entry_denominator = Entry(root)
entry_denominator.pack(pady=5)

Button(root, text="Perform Operation",bg="yellow", command=perform_operation).pack(pady=10)
Label(root, textvariable=status_var, fg="green").pack()
root.geometry("400x700")
root.eval('tk::PlaceWindow . center')

root.mainloop()
