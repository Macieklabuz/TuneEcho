import librosa
import numpy as np
from scipy.ndimage import maximum_filter, generate_binary_structure, binary_erosion

# parametry
N_FFT = 4096
HOP = 512
PEAK_NEIGHBORHOOD = (15, 15)
FAN_VALUE = 5
MIN_DT, MAX_DT = 1, 200

def load_audio(path, sr=22050):
    y, sr = librosa.load(path, sr=sr, mono=True)
    return y, sr

def compute_spectrogram(y):
    S = np.abs(librosa.stft(y, n_fft=N_FFT, hop_length=HOP))
    S_db = librosa.amplitude_to_db(S, ref=np.max)
    return S_db

def find_peaks(S_db):
    footprint = np.ones(PEAK_NEIGHBORHOOD, dtype=bool)
    local_max = maximum_filter(S_db, footprint=footprint) == S_db
    background = (S_db < (S_db.max() - 20))
    eroded = binary_erosion(background, structure=generate_binary_structure(2, 1), iterations=1)
    peaks = local_max & (~eroded)
    f_idx, t_idx = np.where(peaks)
    return list(zip(f_idx, t_idx))  # (freq, time)

def make_hash(f1, f2, dt):
    return ((f1 & 0xFFFFF) << 40) | ((f2 & 0xFFFFF) << 20) | (dt & 0xFFFFF)

def generate_fingerprints(peaks):
    hashes = []
    for i in range(len(peaks)):
        f1, t1 = peaks[i]
        for j in range(1, FAN_VALUE):
            if i + j < len(peaks):
                f2, t2 = peaks[i+j]
                dt = t2 - t1
                if MIN_DT <= dt <= MAX_DT:
                    h = make_hash(f1, f2, dt)
                    hashes.append((h, t1))
    return hashes
