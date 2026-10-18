"""Tempo estimate for loops (librosa beat tracker), folded into 70-180 BPM."""
import librosa


def fold(bpm, lo=70, hi=180):
    while bpm < lo:
        bpm *= 2
    while bpm > hi:
        bpm /= 2
    return bpm


def estimate(path, sr=22050):
    y, sr = librosa.load(path, sr=sr, mono=True)
    if len(y) < 2 * sr:
        return None  # one-shots: no tempo
    onset = librosa.onset.onset_strength(y=y, sr=sr)
    tempo = librosa.feature.tempo(onset_envelope=onset, sr=sr, aggregate=None)
    return int(round(fold(float(tempo.mean()))))
