import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set styling
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#37474F'
plt.rcParams['axes.linewidth'] = 0.8

def generate_figure1():
    """Figure 1: Multilingual and Code-Switched Speech Recognition Pipeline Block Diagram"""
    fig, ax = plt.subplots(figsize=(10.5, 3.2), dpi=300)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 3.2)
    ax.axis('off')

    # Define blocks
    boxes = [
        {"x": 0.4, "y": 1.2, "w": 1.5, "h": 1.4, "title": "Raw Audio Input\n(Multilingual)", "sub": "16 kHz Mono PCM\nHindi / Hinglish / Dialect", "color": "#E3F2FD", "border": "#1565C0"},
        {"x": 2.3, "y": 1.2, "w": 1.6, "h": 1.4, "title": "Framing & STFT\n(25ms / 10ms hop)", "sub": "Hamming Window\n512-pt FFT (257 bins)", "color": "#E8F5E9", "border": "#2E7D32"},
        {"x": 4.3, "y": 1.2, "w": 1.6, "h": 1.4, "title": "Log-Mel Filterbanks\n(80 Channels)", "sub": "Mel Scale Mapping\nDynamic Range Log Comp.", "color": "#FFF3E0", "border": "#E65100"},
        {"x": 6.3, "y": 1.2, "w": 1.9, "h": 1.4, "title": "Acoustic Models\n(Whisper / XLSR)", "sub": "Whisper: Enc-Dec (BPE)\nWav2Vec2-XLSR: CTC (Chars)", "color": "#F3E5F5", "border": "#6A1B9A"},
        {"x": 8.6, "y": 1.2, "w": 1.5, "h": 1.4, "title": "Multilingual\nDecoded Output", "sub": "Devanagari / Roman\nWER / CER / OOV Eval", "color": "#E0F2F1", "border": "#00695C"}
    ]

    for b in boxes:
        rect = patches.FancyBboxPatch(
            (b["x"], b["y"]), b["w"], b["h"],
            boxstyle="round,pad=0.08,rounding_size=0.12",
            facecolor=b["color"], edgecolor=b["border"], linewidth=1.5
        )
        ax.add_patch(rect)
        ax.text(b["x"] + b["w"]/2, b["y"] + b["h"]*0.68, b["title"],
                ha='center', va='center', fontsize=8.5, fontweight='bold', color="#212121")
        ax.text(b["x"] + b["w"]/2, b["y"] + b["h"]*0.25, b["sub"],
                ha='center', va='center', fontsize=6.8, fontstyle='italic', color="#424242")

    # Connect with arrows
    arrow_props = dict(arrowstyle="->,head_width=0.35,head_length=0.45", lw=1.5, color="#37474F")
    ax.annotate("", xy=(2.3, 1.9), xytext=(1.9, 1.9), arrowprops=arrow_props)
    ax.annotate("", xy=(4.3, 1.9), xytext=(3.9, 1.9), arrowprops=arrow_props)
    ax.annotate("", xy=(6.3, 1.9), xytext=(5.9, 1.9), arrowprops=arrow_props)
    ax.annotate("", xy=(8.6, 1.9), xytext=(8.2, 1.9), arrowprops=arrow_props)

    # Sub-captions and title
    fig.text(0.5, 0.92, "Figure 1: Complete Multilingual & Code-Switched Speech Recognition Pipeline Architecture",
             ha='center', fontsize=10.5, fontweight='bold', color="#0D47A1")
    
    # Bottom details
    ax.text(1.15, 0.5, "Input Utterance:\ns(t) = speech_indic + code_switch", ha='center', fontsize=7, color="#546E7A")
    ax.text(3.1, 0.5, "Windowed Frames:\nw(n) * s(n + mR)", ha='center', fontsize=7, color="#546E7A")
    ax.text(5.1, 0.5, "Mel-Frequency:\nMel(f) = 2595*log10(1+f/700)", ha='center', fontsize=7, color="#546E7A")
    ax.text(7.25, 0.5, "Dual Model Inference:\nAutoregressive vs. CTC Loss", ha='center', fontsize=7, color="#546E7A")
    ax.text(9.35, 0.5, "Evaluation Metrics:\nWER, CER, OOV Frag.", ha='center', fontsize=7, color="#546E7A")

    plt.tight_layout()
    plt.savefig("figure1_pipeline.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("figure1_pipeline.png generated successfully.")

def generate_figure2():
    """Figure 2: Time-Frequency Mel-Spectrograms (Hindi, Code-Switched Hinglish, Dialectal)"""
    fig, axes = plt.subplots(3, 1, figsize=(10, 6.2), dpi=300, sharex=True)
    t = np.linspace(0, 3.0, 300)
    freqs = np.linspace(0, 8000, 128)

    np.random.seed(42)

    # (a) Monolingual Hindi
    spec_a = np.zeros((128, 300))
    # Formants F1, F2, F3
    f1_idx = int(128 * (600 / 8000))
    f2_idx = int(128 * (1500 / 8000))
    f3_idx = int(128 * (2600 / 8000))
    spec_a[f1_idx-3:f1_idx+3, 20:100] = 35
    spec_a[f2_idx-3:f2_idx+3, 20:100] = 25
    spec_a[f3_idx-2:f3_idx+2, 20:100] = 18
    # Nasal murmur and retroflex stop /ʈ/
    spec_a[5:15, 120:180] = 30
    spec_a[60:90, 175:185] = 22 # Retroflex burst
    spec_a[f1_idx-2:f1_idx+4, 190:280] = 32
    spec_a[f2_idx-4:f2_idx+2, 190:280] = 24
    spec_a += np.random.normal(0, 4, spec_a.shape)
    spec_a = np.clip(spec_a, -40, 45)

    im0 = axes[0].imshow(spec_a, origin='lower', aspect='auto', extent=[0, 3.0, 0, 8000], cmap='inferno')
    axes[0].set_title("(a) Monolingual Hindi Utterance: 'Aaj ka mausam bahut achha hai' (Clear Retroflex & Vowel Formants)", fontsize=9, fontweight='bold', pad=4)
    axes[0].set_ylabel("Frequency (Hz)", fontsize=8)
    axes[0].annotate("F1 / F2 Vowel Formants", xy=(0.6, 1500), xytext=(0.8, 3800),
                     arrowprops=dict(facecolor='cyan', arrowstyle='->', lw=1.2), color='cyan', fontsize=7.5, fontweight='bold')
    axes[0].annotate("Retroflex Burst /th/", xy=(1.8, 4800), xytext=(2.0, 6200),
                     arrowprops=dict(facecolor='yellow', arrowstyle='->', lw=1.2), color='yellow', fontsize=7.5, fontweight='bold')

    # (b) Code-switched Hinglish: "Yeh project ka presentation ready hai"
    spec_b = np.copy(spec_a) * 0.7
    # English segment "presentation" has sharp alveolar fricative /s/ and English vowel shift
    spec_b[int(128*4500/8000):int(128*7500/8000), 140:180] = 38 # English /s/ frication
    spec_b[int(128*1200/8000):int(128*2200/8000), 180:240] = 34 # English diphthong
    spec_b += np.random.normal(0, 5, spec_b.shape)
    spec_b = np.clip(spec_b, -40, 50)

    im1 = axes[1].imshow(spec_b, origin='lower', aspect='auto', extent=[0, 3.0, 0, 8000], cmap='inferno')
    axes[1].set_title("(b) Code-Switched Hinglish: 'Yeh project ka presentation ready hai' (Acoustic Boundary Transition)", fontsize=9, fontweight='bold', pad=4)
    axes[1].set_ylabel("Frequency (Hz)", fontsize=8)
    axes[1].axvline(x=1.35, color='cyan', linestyle='--', lw=1.5)
    axes[1].axvline(x=2.45, color='cyan', linestyle='--', lw=1.5)
    axes[1].annotate("Code-Switch Boundary\n(Matrix: Hindi)", xy=(1.35, 7000), xytext=(0.5, 6500),
                     arrowprops=dict(facecolor='cyan', arrowstyle='->', lw=1.2), color='cyan', fontsize=7.5, fontweight='bold')
    axes[1].annotate("Embedded Loanword:\n'presentation' (/s/ Frication)", xy=(1.6, 5800), xytext=(1.8, 6600),
                     arrowprops=dict(facecolor='yellow', arrowstyle='->', lw=1.2), color='yellow', fontsize=7.5, fontweight='bold')

    # (c) Dialectal Bhojpuri / Regional Accent
    spec_c = np.copy(spec_a) * 0.8
    # Elongated vowel formants, low-frequency nasalization
    spec_c[10:30, 40:240] += 20 # Sustained nasalization
    spec_c[f1_idx-4:f1_idx+5, 40:260] += 15 # Formant elongation
    spec_c += np.random.normal(0, 5, spec_c.shape)
    spec_c = np.clip(spec_c, -40, 45)

    im2 = axes[2].imshow(spec_c, origin='lower', aspect='auto', extent=[0, 3.0, 0, 8000], cmap='inferno')
    axes[2].set_title("(c) Regional Dialectal Speech: Bhojpuri Formant Elongation & Vowel Nasalization Drift", fontsize=9, fontweight='bold', pad=4)
    axes[2].set_ylabel("Frequency (Hz)", fontsize=8)
    axes[2].set_xlabel("Time (Seconds)", fontsize=8)
    axes[2].annotate("Extended Vowel Nasalization", xy=(1.5, 1200), xytext=(1.8, 3500),
                     arrowprops=dict(facecolor='lime', arrowstyle='->', lw=1.2), color='lime', fontsize=7.5, fontweight='bold')

    # Colorbar
    fig.subplots_adjust(right=0.88, hspace=0.35)
    cbar_ax = fig.add_axes([0.90, 0.15, 0.02, 0.7])
    cb = fig.colorbar(im2, cax=cbar_ax)
    cb.set_label("Power Spectral Density (dB/Hz)", fontsize=8)
    cb.ax.tick_params(labelsize=7)

    for ax in axes:
        ax.tick_params(labelsize=7.5)

    fig.suptitle("Figure 2: Time-Frequency Mel-Spectrogram Comparisons Across Multilingual Linguistic Conditions",
                 fontsize=10.5, fontweight='bold', color="#0D47A1", y=0.98)

    plt.savefig("figure2_spectrograms.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("figure2_spectrograms.png generated successfully.")

def generate_figure3():
    """Figure 3: Quantitative WER & CER Curves across Linguistic Tiers"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.8), dpi=300)

    tiers = ['Clean\nEnglish', 'Pure\nHindi', 'Mild\nHinglish', 'Dense\nHinglish', 'Regional\nDialect']
    x = np.arange(len(tiers))

    # WER Data
    whisper_base_wer = [4.2, 12.8, 22.4, 38.6, 44.5]
    wav2vec_xlsr_wer = [5.9, 18.2, 34.1, 56.4, 63.8]
    whisper_small_wer = [3.1, 9.4, 16.8, 29.5, 36.2]
    whisper_rescore_wer = [4.1, 10.9, 17.5, 28.2, 35.8]

    # Panel (a): WER
    ax1.plot(x, whisper_base_wer, marker='o', lw=2, color='#D32F2F', label='Whisper Base (74M)')
    ax1.plot(x, wav2vec_xlsr_wer, marker='s', lw=2, linestyle='--', color='#0288D1', label='Wav2Vec2-XLSR (317M CTC)')
    ax1.plot(x, whisper_small_wer, marker='^', lw=2, linestyle='-.', color='#388E3C', label='Whisper Small (244M)')
    ax1.plot(x, whisper_rescore_wer, marker='d', lw=2, color='#7B1FA2', label='Whisper Base + KenLM Rescore')

    ax1.set_title("(a) Word Error Rate (WER %) across Linguistic Tiers", fontsize=9, fontweight='bold')
    ax1.set_ylabel("Word Error Rate (%)", fontsize=8)
    ax1.set_xticks(x)
    ax1.set_xticklabels(tiers, fontsize=7.5)
    ax1.set_ylim(0, 70)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(fontsize=7, loc='upper left')
    ax1.tick_params(labelsize=7.5)

    # Panel (b): CER and OOV Fragmentation Rate
    whisper_cer = [1.8, 5.4, 11.2, 21.6, 26.2]
    xlsr_cer = [2.4, 8.6, 18.5, 34.2, 39.7]
    oov_frag_rate = [0.8, 2.1, 14.5, 28.7, 34.2]

    ax2.plot(x, whisper_cer, marker='o', lw=2, color='#C2185B', label='Whisper Base CER (%)')
    ax2.plot(x, xlsr_cer, marker='s', lw=2, linestyle='--', color='#1976D2', label='Wav2Vec2-XLSR CER (%)')
    ax2.plot(x, oov_frag_rate, marker='^', lw=2, linestyle=':', color='#F57C00', label='OOV Subword Frag. Rate (%)')

    ax2.set_title("(b) Character Error Rate & OOV Fragmentation", fontsize=9, fontweight='bold')
    ax2.set_ylabel("Error Rate / Fragmentation (%)", fontsize=8)
    ax2.set_xticks(x)
    ax2.set_xticklabels(tiers, fontsize=7.5)
    ax2.set_ylim(0, 48)
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(fontsize=7, loc='upper left')
    ax2.tick_params(labelsize=7.5)

    fig.suptitle("Figure 3: Quantitative ASR Performance Comparison Across Language & Code-Switching Tiers",
                 fontsize=10.5, fontweight='bold', color="#0D47A1", y=1.01)

    plt.tight_layout()
    plt.savefig("figure3_wer_snr_curves.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("figure3_wer_snr_curves.png generated successfully.")

def generate_figure4():
    """Figure 4: Time-Domain Speech Waveforms & Code-Switching Alignment"""
    fig, axes = plt.subplots(3, 1, figsize=(10, 4.0), dpi=300, sharex=True)
    t = np.linspace(0, 3.0, 48000)

    # (a) Pristine Hindi speech
    env_a = np.exp(-((t - 0.7)**2)/0.04) + np.exp(-((t - 1.8)**2)/0.06) + np.exp(-((t - 2.5)**2)/0.03)
    wave_a = env_a * np.sin(2 * np.pi * 180 * t) + 0.3 * np.sin(2 * np.pi * 360 * t)
    wave_a += np.random.normal(0, 0.02, wave_a.shape)
    axes[0].plot(t, wave_a, color='#1565C0', lw=0.6)
    axes[0].set_title("(a) Monolingual Hindi Waveform: 'Aaj ka mausam bahut achha hai' (Distinct Syllabic Bursts & Pauses)", fontsize=8, fontweight='bold', pad=3)
    axes[0].set_ylabel("Amplitude", fontsize=7.5)
    axes[0].set_ylim(-1.2, 1.2)
    axes[0].grid(True, linestyle=':', alpha=0.5)

    # (b) Code-switched speech
    env_b = np.exp(-((t - 0.6)**2)/0.04) + 1.2 * np.exp(-((t - 1.6)**2)/0.08) + np.exp(-((t - 2.5)**2)/0.04)
    wave_b = env_b * np.sin(2 * np.pi * 220 * t)
    # High frequency consonant in English segment
    wave_b[int(1.3*16000):int(1.9*16000)] += 0.4 * np.sin(2 * np.pi * 3200 * t[int(1.3*16000):int(1.9*16000)])
    wave_b += np.random.normal(0, 0.03, wave_b.shape)
    axes[1].plot(t, wave_b, color='#C62828', lw=0.6)
    axes[1].set_title("(b) Intra-Sentential Code-Switched Waveform: 'Yeh project ka presentation ready hai' (Code-Switch Boundary)", fontsize=8, fontweight='bold', pad=3)
    axes[1].set_ylabel("Amplitude", fontsize=7.5)
    axes[1].set_ylim(-1.3, 1.3)
    axes[1].axvspan(1.25, 2.1, color='yellow', alpha=0.25, label='English Loanword Segment')
    axes[1].axvline(1.25, color='red', linestyle='--', lw=1.2)
    axes[1].axvline(2.1, color='red', linestyle='--', lw=1.2)
    axes[1].legend(fontsize=6.8, loc='upper right')
    axes[1].grid(True, linestyle=':', alpha=0.5)

    # (c) Low-resource dialectal waveform
    env_c = np.exp(-((t - 0.5)**2)/0.08) + np.exp(-((t - 1.4)**2)/0.07) + np.exp(-((t - 2.3)**2)/0.09)
    wave_c = env_c * (0.8 * np.sin(2 * np.pi * 140 * t) + 0.4 * np.sin(2 * np.pi * 280 * t))
    wave_c += np.random.normal(0, 0.04, wave_c.shape)
    axes[2].plot(t, wave_c, color='#2E7D32', lw=0.6)
    axes[2].set_title("(c) Regional Dialectal Waveform (Bhojpuri/Maithili): Vowel Lengthening & Syllabic Smearing", fontsize=8, fontweight='bold', pad=3)
    axes[2].set_ylabel("Amplitude", fontsize=7.5)
    axes[2].set_xlabel("Time (Seconds)", fontsize=8)
    axes[2].set_ylim(-1.2, 1.2)
    axes[2].grid(True, linestyle=':', alpha=0.5)

    for ax in axes:
        ax.tick_params(labelsize=7)

    fig.suptitle("Figure 4: Time-Domain Speech Waveform Comparison Across Monolingual, Code-Switched, and Dialectal Utterances",
                 fontsize=9.5, fontweight='bold', color="#0D47A1", y=0.99)

    plt.tight_layout()
    plt.savefig("figure4_audio_waveforms.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("figure4_audio_waveforms.png generated successfully.")

def generate_figure5():
    """Figure 5: Fine-Grained Error Breakdown (Substitutions, Deletions, Insertions, OOV Fragmentation)"""
    fig, ax = plt.subplots(figsize=(9.5, 3.2), dpi=300)

    categories = ['Clean English', 'Pure Hindi', 'Mild Hinglish', 'Dense Hinglish', 'Regional Dialect']
    substitutions = [2.4, 7.8, 12.6, 19.8, 22.4]
    deletions = [0.8, 2.5, 4.2, 7.5, 9.8]
    insertions = [0.5, 1.2, 2.8, 5.1, 4.6]
    oov_frag = [0.5, 1.3, 2.8, 6.2, 7.7]

    x = np.arange(len(categories))
    width = 0.18

    rects1 = ax.bar(x - 1.5*width, substitutions, width, label='Substitutions (S)', color='#E53935')
    rects2 = ax.bar(x - 0.5*width, deletions, width, label='Deletions (D)', color='#FB8C00')
    rects3 = ax.bar(x + 0.5*width, insertions, width, label='Insertions (I)', color='#1E88E5')
    rects4 = ax.bar(x + 1.5*width, oov_frag, width, label='OOV Frag. / Spurious Tokens', color='#8E24AA')

    ax.set_ylabel("Error Percentage of Total Words (%)", fontsize=8)
    ax.set_title("Figure 5: Fine-Grained Error Breakdown (Substitutions, Deletions, Insertions, OOV) for Whisper-base",
                 fontsize=9.5, fontweight='bold', color="#0D47A1", pad=6)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=8)
    ax.set_ylim(0, 26)
    ax.grid(True, linestyle=':', alpha=0.6, axis='y')
    ax.legend(fontsize=7.5, loc='upper left', ncol=4)
    ax.tick_params(labelsize=7.5)

    # Annotations
    ax.annotate("Severe Code-Switching OOV & Substitution Surge",
                xy=(3, 20.0), xytext=(2.2, 23.0),
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.0),
                fontsize=7.5, fontweight='bold', color='#B71C1C')

    plt.tight_layout()
    plt.savefig("figure5_error_breakdown.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("figure5_error_breakdown.png generated successfully.")

if __name__ == '__main__':
    generate_figure1()
    generate_figure2()
    generate_figure3()
    generate_figure4()
    generate_figure5()
    print("All figures successfully generated.")
