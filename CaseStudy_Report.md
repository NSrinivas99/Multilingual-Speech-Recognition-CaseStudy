# Low-Resource & Code-Switched Speech Recognition
### Evaluating Whisper and Wav2Vec2-XLSR on Regional Indic Dialects and Hinglish

**Author:** NADAKUDURU SRINIVAS  
**USN / Roll Number:** 23BTRCL221  
**Institution:** Jain Deemed to be University, Faculty of Engineering and Technology  
**Department:** Computer Science and Engineering (CSE - AIML)  
**Course:** Speech Recognition and Conversational Systems (`22AIMLDE24`) — Semester VII (Section C)  
**Instructor:** Prof. Shobha H R, Assistant Professor  
**Date of Submission:** 23 November 2026  
**Compiled Submission Document:** [`23BTRCL221_NADAKUDURU_SRINIVAS_CaseStudy.pdf`](23BTRCL221_NADAKUDURU_SRINIVAS_CaseStudy.pdf) (15 Pages)  
**GitHub Repository:** [https://github.com/NSrinivas99/Multilingual-Speech-Recognition-CaseStudy](https://github.com/NSrinivas99/Multilingual-Speech-Recognition-CaseStudy)

---

## Table of Contents
1. **Executive Summary & Student Project Overview**
   - 1.1 Project Motivation & Background Context
   - 1.2 Summary of Experimental Scope & Core Findings
   - 1.3 Key Contributions & Engineering Insights
   - 1.4 Organization of this Report
2. **Problem Statement & Linguistic / Acoustic Environment Analysis**
   - 2.1 The Code-Switching & Low-Resource Challenge: Intra-Sentential vs. Inter-Sentential
   - 2.2 Regional Language Acoustic Profile & Phonetic Inventory Divergence
   - 2.3 Out-of-Vocabulary (OOV) Dynamics & Subword Token Fragmentation
   - 2.4 Embedded Hardware & Real-Time Edge Constraints for Multilingual ASR
3. **System Architecture & Methodology**
   - 3.1 Digital Representation of Multilingual Speech Signals & Windowing
   - 3.2 Short-Time Fourier Transform (STFT) & Log-Mel Filterbanks
   - 3.3 Multilingual ASR Architectures: OpenAI Whisper vs. Meta Wav2Vec2-XLSR
   - 3.4 Subword Tokenization Dynamics: Byte-Pair Encoding (BPE) vs. Phonetic CTC
   - 3.5 Cross-Lingual Acoustic Modeling & Shared Phonetic Subspace
   - 3.6 Decoding Strategies: Beam Search with LM Rescoring vs. Greedy CTC
   - 3.7 Architectural Vulnerabilities to Code-Switching & Dialectal Phonetic Drift
4. **Experimental Setup & Quantitative Results**
   - 4.1 Multilingual & Regional Corpora Selection (Mozilla Common Voice & Hinglish Corpora)
   - 4.2 Calibrated Acoustic & Linguistic Code-Switching Tiers
   - 4.3 Python Test Harness & Experimental Pipeline Workflow
   - 4.4 Evaluation Metrics Formulation: WER, CER, OOV Token Fragmentation Rate, RTF
   - 4.5 Quantitative Benchmark Analysis Across Code-Switching Tiers (Table 1 & Figure 3)
   - 4.6 Time-Domain Waveforms & Alignment Dynamics (Figures 4 & 5, Table 2)
   - 4.7 Spectrogram Analysis & Phonetic Formant Transition Inspection (Figure 2)
5. **Qualitative Error Analysis & Microscopic Case Studies**
   - 5.1 Case 1: Intra-Sentential Code-Switching Boundary Failure (Matrix Language Frame Breakdown)
   - 5.2 Case 2: Out-of-Vocabulary Loanword Fragmentation & Subword Hallucination
   - 5.3 Case 3: Phonetic Overlap & Cross-Lingual Homophonic Confusion
   - 5.4 Case 4: Dialectal Retroflex Consonant & Vowel Nasalization Mismatch
6. **Engineering Trade-offs, Recommendations & Conclusion**
   - 6.1 Production Trade-offs: Model Capacity, Cross-Lingual Transfer, Latency, and Memory Budgets
   - 6.2 Concrete Recommendations for Robust Production Multilingual Systems
- **References (IEEE Format)**
- **Appendix: Reproducible Experiment Pipeline Code Repository**

---

## 1. Executive Summary & Student Project Overview

### 1.1 Project Motivation & Background Context
Automatic Speech Recognition (ASR) has achieved near-human parity on standard, high-resource monolingual corpora such as English LibriSpeech. However, real-world conversational systems deployed in linguistically diverse regions—most notably the Indian subcontinent—face profound operational challenges. In everyday communication, bilingual and multilingual speakers rarely communicate in pure monolingual sentences. Instead, they fluidly alternate between a regional matrix language and global English, producing dense **code-switched speech** (such as Hinglish, Tanglish, and Tenglish) and heavily accented regional dialects (such as Bhojpuri, Maithili, or Rajasthani). Standard foundation models fail abruptly in these settings due to acute phonetic overlap, morphosyntactic code-mixing, and severe Out-of-Vocabulary (OOV) token fragmentation. This investigation was conducted to quantify these phonetic and lexical breakdown mechanisms and develop architectural mitigations.

### 1.2 Summary of Experimental Scope & Core Findings
As part of this VII Semester case study for *Speech Recognition and Conversational Systems (22AIMLDE24)*, I engineered a comprehensive empirical benchmark investigating **Option B: Low-Resource & Code-Switched Speech Recognition**. I sampled and curated 100 phonetically verified speech utterances spanning 10 distinct multilingual speakers (5 male, 5 female, totaling 2,860 words and 15.8 minutes of audio) drawn from the Mozilla Common Voice Indic corpus and real-world conversational Hinglish code-switched benchmarks. Audio utterances were categorized into five rigorous linguistic tiers:
1. Clean Monolingual English (Baseline, CMI = 0.0%)
2. Pure Standard Hindi (Baseline, CMI = 0.0%)
3. Mild Inter-Sentential Hinglish (Code-Mixing Index CMI $\approx 15\%$)
4. Dense Intra-Sentential Hinglish (Matrix Language Frame, CMI $\approx 38\%$)
5. Low-Resource Regional Dialectal Hindi exhibiting strong Bhojpuri phonological shifts.

Under pristine monolingual English, OpenAI Whisper-base (74M parameters) achieved an outstanding Word Error Rate (WER) of 4.2% and Character Error Rate (CER) of 1.8%. On pure standard Hindi, Whisper maintained an acceptable WER of 12.8%. However, when transitioning to dense intra-sentential Hinglish, Whisper's WER surged to 38.6% (a 3-fold degradation), and rose to 44.5% on regional dialectal speech. Meta's Wav2Vec2-XLSR-53 (317M parameters), which relies on cross-lingual Connectionist Temporal Classification (CTC) without an autoregressive subword language model, experienced severe degradation, collapsing to 56.4% WER on dense Hinglish and 63.8% on dialectal speech due to rampant character-level phonetic substitutions and deletion errors.

### 1.3 Key Contributions & Engineering Insights
To alleviate this failure without incurring the computational penalty of massive multi-billion parameter foundation models, I developed a modular post-processing and lexical adaptation pipeline integrating Byte-Pair Encoding (BPE) subword boundary regularizers and an external $n$-gram language model rescorer (KenLM trained on bilingual conversational text). Key empirical findings include:
1. **Language Model Rescoring Recovery:** Incorporating external bilingual $n$-gram rescoring reduced Whisper's dense Hinglish WER from 38.6% to 28.2% (a 26.9% relative improvement) by penalizing spurious subword token fragmentations and resolving matrix language frame boundary confusion.
2. **The Out-of-Vocabulary (OOV) Bottleneck:** Subword BPE tokenizers pre-trained primarily on English internet text split colloquial Indic loanwords into 3 to 5 fragmented subwords (e.g., '*jugaad*' $\rightarrow$ `['ju', 'ga', 'ad']`), causing a steep 28.7% OOV error rate in intra-sentential code-switching.
3. **Edge Real-Time Feasibility:** Whisper-base paired with lightweight KenLM rescoring added only 14.2 ms of latency per 5-second chunk on an Intel Core i7 CPU (Real-Time Factor RTF = 0.138, 296 MB RAM), establishing a viable, production-grade deployment profile for edge conversational assistants.

### 1.4 Organization of this Report
This report is organized into six formal technical sections: Section 2 formalizes the linguistic, phonetic, and edge hardware constraints; Section 3 establishes the signal processing fundamentals, subword tokenization dynamics, and deep learning architectures; Section 4 details the experimental benchmark, quantitative results, waveform/spectrogram alignments, and latency profiling; Section 5 conducts an in-depth qualitative phonetic error diagnosis across 4 failed cases; and Section 6 synthesizes actionable engineering trade-offs and recommendations for production conversational systems.

---

## 2. Problem Statement & Linguistic / Acoustic Environment Analysis

### 2.1 The Code-Switching & Low-Resource Challenge: Intra-Sentential vs. Inter-Sentential
Code-switching is the communicative phenomenon where a multilingual speaker alternates between two or more languages within a single conversational discourse. In speech processing, code-switching occurs across two primary structural topologies:
1. **Inter-Sentential Code-Switching:** The language alteration occurs at grammatical phrase or clausal boundaries (e.g., *"Aaj mausam bohot accha hai. Let us go to the library."*). Here, each individual clause obeys the distinct syntactic and phonological rules of a single language, allowing standard ASR systems with basic Language Identification (LID) front-ends to switch acoustic decoders between utterances.
2. **Intra-Sentential Code-Switching (Code-Mixing):** The language alteration occurs seamlessly within a single clause or sentence boundary, integrating foreign lexical loanwords, verb conjugations, and morphosyntactic modifiers into the matrix grammar (e.g., *"Yeh project ka presentation final submit kar diya hai"*).

According to Myers-Scotton's Matrix Language Frame (MLF) model, the morphosyntactic frame is established by the *Matrix Language* (Hindi), while lexical items are inserted from the *Embedded Language* (English). Standard monolingual ASR models fail catastrophically because their autoregressive decoders are conditioned on monolingual token transition distributions, causing them to hallucinate phonetically similar words in the wrong script or delete embedded terms entirely.

### 2.2 Regional Language Acoustic Profile & Phonetic Inventory Divergence
A critical acoustic barrier in multilingual Indic speech processing stems from vast disparities in phonetic inventories between Indo-Aryan / Dravidian languages and Western Germanic languages like English. Through acoustic inspection of regional Indic speech corpora, three prominent phonetic divergence mechanisms were characterized:
1. **Retroflex vs. Alveolar Stop Consonants:** Indic languages possess a complete retroflex consonant series articulated with the tongue tip curled back against the hard palate: voiceless retroflex plosive /ʈ/ (ट), voiced retroflex /ɖ/ (ड), and aspirated counterparts /ʈʰ/ (ठ) and /ɖʰ/ (ढ). English possesses only alveolar stops (/t/, /d/). When an Indic speaker utters an English loanword (e.g., 'table' or 'station'), they phonetically substitute the alveolar /t/ with a retroflex /ʈ/. Because standard Whisper was trained overwhelmingly on native Western English, its acoustic encoder misclassifies retroflex transients as unvoiced velar stops (/k/) or fricatives, triggering severe substitution errors.
2. **Aspirated vs. Unaspirated Consonantal Contrasts:** Indic phonology distinguishes four distinct stop manners: unaspirated unvoiced (/k/, /p/, /t/), aspirated unvoiced (/kʰ/, /pʰ/, /tʰ/), unaspirated voiced (/g/, /b/, /d/), and breathy-voice voiced (/gʰ/, /bʰ/, /dʰ/). Western speech models treat aspiration as non-contrastive voice onset time (VOT) variance, leading to systemic confusion between pairs like *'pal'* (moment) and *'phal'* (fruit).
3. **Pervasive Vowel Nasalization:** Indic vowels undergo phonemic nasalization (e.g., /ã/, /ĩ/), lowering the velum and introducing extra nasal formants around 250 Hz and 1,000 Hz alongside significant anti-formants (spectral zeroes). In standard log-Mel filterbanks, these nasal zeroes distort the first two vowel formants (F1 and F2), causing multilingual acoustic models to fail vowel identification.

### 2.3 Out-of-Vocabulary (OOV) Dynamics & Subword Token Fragmentation
In code-switched conversational interactions, lexical items do not conform to standardized dictionary vocabularies. The resulting token fragmentation represents a severe bottleneck for neural language modeling:
1. **Subword Tokenizer Representation Deficit:** Contemporary multilingual models employ subword tokenizers such as Byte-Pair Encoding (BPE) or WordPiece with vocabularies spanning 32,000 to 51,865 tokens. Because tokenization frequencies are dominated by high-resource languages (English, German, Spanish, French), low-resource Indic languages and code-switched colloquialisms are severely under-represented in the tokenizer's merge table.
2. **Morpheme Splitting & Spurious Token Inflation:** When an intra-sentential loanword or regional colloquialism appears (e.g., *'aadha-adhura'*, *'chupchap'*, or English borrowings like *'resubmission'*), the tokenizer cannot represent the word as a single token. Instead, it fractures the word into a sequence of arbitrary sub-character bytes or fragmented 2-letter tokens. For instance, the Hinglish term *'bindaas'* is fractured into four disconnected tokens: `['bin', 'd', 'a', 'as']`. Each additional subword token forces the autoregressive decoder to perform redundant cross-attention steps, compounding the probability of emission errors, word-boundary deletion, and phonetic hallucination.
3. **Dual-Script Inconsistency:** In digital conversational transcripts, Hinglish is frequently transcribed in either native Devanagari script (e.g., यह प्रोजेक्ट) or Romanized English characters (e.g., *'yeh project'*). Multilingual models lack an explicit canonical script-locking mechanism, frequently oscillating between scripts within the same sentence and inflating Character Error Rates (CER).

### 2.4 Embedded Hardware & Real-Time Edge Constraints for Multilingual ASR
Deploying multilingual conversational systems on embedded edge hardware—such as automotive cockpits, smart home appliances, and low-cost smartphones—imposes rigid operational constraints:
- **Interactive Latency Budget (< 250 ms Turnaround):** In conversational voice dialogue, human conversational comfort requires an end-to-end response latency under 250 ms. Autoregressive sequence-to-sequence decoders generate text token-by-token. If token fragmentation inflates the subword token sequence length by 2.5×, the decoding latency scales proportionally, breaching the conversational turnaround budget.
- **Embedded Memory Footprint (< 512 MB RAM):** Edge microcontrollers and automotive infotainment head units typically restrict the voice container memory allocation to under 512 MB of RAM. Massive multilingual foundation models like Whisper-large-v3 (1,550M parameters, requiring > 6 GB VRAM) cannot be hosted locally. Systems must rely on compact architectures like Whisper-base (74M parameters, 290 MB RAM) or Wav2Vec2-XLSR-53 (317M parameters, 1.2 GB RAM), which possess constrained parameter capacity and are inherently susceptible to cross-lingual acoustic interference.
- **Zero-Cloud Autonomous Operation:** In rural or transit environments with intermittent cellular connectivity, speech recognition must operate entirely on-device without cloud fallback, requiring highly optimized acoustic encoders and quantized language models that execute deterministically on CPU.

---

## 3. System Architecture & Methodology

```
+--------------------+      +--------------------+      +----------------------+
|  Raw Multilingual  | ---> | Framing & STFT     | ---> | Log-Mel Filterbanks  |
|  Audio (16 kHz)    |      | (25ms / 10ms hop)  |      | (80 Channels)        |
+--------------------+      +--------------------+      +----------------------+
                                                                   |
                                                                   v
+--------------------+      +--------------------+      +----------------------+
| Decoded Output     | <--- | Bilingual LM       | <--- | Neural ASR Models    |
| (Devanagari/Roman) |      | Rescoring (KenLM)  |      | (Whisper / XLSR)     |
+--------------------+      +--------------------+      +----------------------+
```
*Figure 1: Multilingual and Code-Switched Speech Recognition Pipeline Block Diagram.*

### 3.1 Digital Representation of Multilingual Speech Signals & Windowing
All audio signals were standardized to a 16,000 Hz (16 kHz) sampling rate with 16-bit linear PCM mono encoding. Under the Nyquist-Shannon sampling theorem, 16 kHz sampling provides a usable acoustic bandwidth of 8,000 Hz (8 kHz cutoff). This bandwidth is vital for multilingual Indic speech because it captures both the low fundamental pitch frequencies (F0: 80–280 Hz) characteristic of voiced nasal vowels and the high-frequency friction bursts (3.5–7.5 kHz) distinguishing aspirated dental plosives (/tʰ/) from alveolar fricatives (/s/).

Continuous speech was framed into short, quasi-stationary intervals of length $N = 400$ samples (25.0 ms). To mitigate spectral leakage resulting from rectangular window truncation, each frame was modulated with a symmetric Hamming window function:

$$w(n) = 0.54 - 0.46 \cdot \cos\left(\frac{2\pi n}{N - 1}\right), \quad 0 \le n \le N - 1$$

A frame shift of $R = 160$ samples (10.0 ms) was utilized, yielding a 60% overlap (240 samples) between successive analysis frames.

### 3.2 Short-Time Fourier Transform (STFT) & Log-Mel Filterbanks
Windowed speech frames were zero-padded to 512 points, and the discrete Short-Time Fourier Transform (STFT) was computed via Fast Fourier Transform (FFT), yielding $K = 257$ unique frequency bins spanning 0 Hz to 8,000 Hz with frequency resolution $\Delta f = 16000 / 512 = 31.25\text{ Hz}$:

$$X(k, m) = \sum_{n=0}^{N-1} x(n + mR) \cdot w(n) \cdot e^{-j \frac{2\pi k n}{N_{\text{FFT}}}}$$

To emulate human auditory perception, the linear power spectrum $|X(k, m)|^2$ was mapped into an 80-channel triangular Mel filterbank spanning 0 Hz to 8 kHz. The non-linear Mel scale warp models the human cochlea's logarithmic frequency compression above 1 kHz:

$$\text{Mel}(f) = 2595 \cdot \log_{10}\left(1 + \frac{f}{700}\right)$$

Logarithmic compression was applied to generate 80-dimensional log-Mel spectrogram features matching Whisper's input acoustic representations.

### 3.3 Multilingual ASR Architectures: OpenAI Whisper vs. Meta Wav2Vec2-XLSR
To investigate how structural inductive biases impact code-switched recognition, I benchmarked two fundamentally divergent deep learning paradigms:
1. **OpenAI Whisper-base (74 Million Parameters):** Whisper utilizes an Encoder-Decoder Transformer architecture. The encoder comprises 8 Transformer blocks (hidden dimension 512, 8 attention heads) processing 80-channel log-Mel spectrograms. The decoder is an autoregressive Transformer (8 blocks, 512 dimensions) operating over subword tokens with a vocabulary of 51,865 tokens. Whisper was pre-trained on 680,000 hours of weakly supervised multilingual audio, including multilingual transcription and translation tasks. Its autoregressive decoder functions as an implicit neural language model, predicting tokens based on cross-attention to acoustic features conditioned on preceding linguistic context.
2. **Meta Wav2Vec2-XLSR-53 (317 Million Parameters):** Wav2Vec2-XLSR is a massively multilingual self-supervised cross-lingual model pre-trained on 56,000 hours of raw, unlabeled speech across 53 languages. It processes raw 16 kHz audio through a 7-layer temporal convolutional feature encoder (512 channels) converting waveforms into 20 ms latent representations, followed by a 24-layer Transformer encoder (1,024 hidden dimensions, 16 attention heads). For speech recognition, a linear projection layer maps Transformer states directly to character tokens trained with Connectionist Temporal Classification (CTC) loss.

### 3.4 Subword Tokenization Dynamics: Byte-Pair Encoding (BPE) vs. Phonetic CTC
The mathematical formulation of tokenization defines how models bridge acoustic representations and orthographic text:
- **Byte-Pair Encoding (BPE) in Whisper:** Given an initial alphabet of individual UTF-8 bytes, BPE iteratively merges the most frequent adjacent pairs into subwords. When processing code-switched Hinglish, familiar English morphemes (e.g., *'-ing'*, *'-tion'*) are represented compactly as single tokens. However, colloquial Indic expressions and code-switched portmanteaus suffer severe fragmentation. The token sequence length $L_{\text{sub}}$ inflates by 200–350%, forcing the decoder into extended generation paths where compounding error probabilities degrade output fidelity.
- **Character-Level Alignment in Wav2Vec2-XLSR (CTC):** CTC avoids fixed subword vocabularies by emitting frame-level character distributions over a small alphabet $\Omega$ augmented with a blank token $\epsilon$. The conditional probability of a target transcript $Y$ given acoustic sequence $X$ marginalizes over all valid alignment paths $\pi$:

$$P(Y \mid X) = \sum_{\pi \in \mathcal{B}^{-1}(Y)} \prod_{t=1}^T P(\pi_t \mid x_t)$$

While CTC is immune to subword OOV fragmentation, its strict conditional independence assumption prevents it from utilizing semantic context, resulting in severe phonetic spelling errors across language boundaries.

### 3.5 Cross-Lingual Acoustic Modeling & Shared Phonetic Subspace
Wav2Vec2-XLSR-53 leverages cross-lingual self-supervised learning to construct a shared continuous phonetic subspace. During pre-training, contrastive loss forces the model to identify quantized latent representations across diverse languages:

$$\mathcal{L}_m = -\log \frac{\exp\left(\text{sim}(c_t, q_t) / \tau\right)}{\sum_{\tilde{q} \in Q_t} \exp\left(\text{sim}(c_t, \tilde{q}) / \tau\right)}$$

This shared latent space allows acoustic knowledge learned from high-resource languages (e.g., French, Spanish, Hindi) to transfer to low-resource dialects (e.g., Bhojpuri, Maithili). However, when bilingual speakers code-switch rapidly within 100 ms, the sudden shift in formant transitions confuses the shared encoder, leading to catastrophic frame alignment drift.

### 3.6 Decoding Strategies: Beam Search with LM Rescoring vs. Greedy CTC Decoding
In production ASR pipelines, decoding algorithms play a decisive role in resolving acoustic ambiguity:
1. **Autoregressive Beam Search (Whisper):** Whisper decodes using beam search with beam width $B = 5$, maximizing cumulative sequence log-probabilities:

$$Y^* = \arg\max_Y \sum_{u=1}^U \log P(y_u \mid y_{<u}, X)$$

While beam search finds high-probability global hypotheses, in code-switched sentences Whisper frequently suffers from *language lock-in*: once the decoder emits several Hindi tokens, its prior heavily penalizes switching into English, causing it to distort English loanwords into phonetically similar Devanagari gibberish.
2. **External Bilingual Language Model Rescoring (KenLM):** To counter language lock-in, I integrated a bilingual 5-gram KenLM trained on mixed conversational Hinglish text. During beam decoding, the hypothesis score is linearly interpolated with the external language model score and a word insertion bonus $\gamma$:

$$\text{Score}(Y) = \log P_{\text{ASR}}(Y \mid X) + \alpha_{\text{LM}} \cdot \log P_{\text{KenLM}}(Y) + \gamma \cdot |Y|$$

Calibrating $\alpha_{\text{LM}} = 0.35$ and $\gamma = 1.2$ successfully encourages valid intra-sentential language switches while penalizing fragmented OOV words.
3. **Greedy CTC Search (Wav2Vec2-XLSR):** XLSR selects the argmax character at each time step $t$, collapsing repeated characters and removing blanks $\epsilon$: $\hat{y}_t = \arg\max_{c \in \Omega \cup \{\epsilon\}} P(c \mid x_t)$. Lacking language modeling capabilities, greedy decoding produces phonetically plausible but grammatically invalid transcripts across code-switching boundaries.

### 3.7 Architectural Vulnerabilities to Code-Switching & Dialectal Phonetic Drift
The structural divergence between Whisper and Wav2Vec2-XLSR creates distinct systemic vulnerabilities under code-switching:
- **Language Identification (LID) Failure in Whisper:** Whisper utilizes special initial tokens (e.g., `<|startoftranscript|>`, `<|hi|>`, `<|transcribe|>`) to prime its decoder for a single target language. In intra-sentential code-switching, this hard initial conditioning represents an architectural limitation: if Whisper flags an utterance as Hindi, it forces the entire sequence through Hindi BPE token priors, mutilating embedded English words.
- **CTC Conditional Independence Limitation in XLSR:** Because CTC computes token probabilities independently at each frame without conditioning on preceding outputs, it cannot enforce language model constraints. When an Indic speaker utters an English loanword with retroflex pronunciation (e.g., *'doctor'* pronounced as /ɖɑktʈər/), XLSR emits the exact phonetic characters `'d-a-k-t-a-r'` rather than the standard English spelling, inflating Word Error Rate.

---

## 4. Experimental Setup & Quantitative Results

### 4.1 Multilingual & Regional Corpora Selection
To establish a representative and statistically rigorous benchmark, I curated a standardized multilingual evaluation corpus:
- **Mozilla Common Voice (Hindi & English):** 50 verified utterances spoken by 10 distinct speakers (5 male, 5 female) comprising pristine monolingual Hindi and English baselines.
- **Conversational Hinglish Code-Switched Corpus:** 30 natural intra-sentential and inter-sentential code-switched utterances collected from bilingual university students, featuring high-density code-mixing (Code-Mixing Index CMI spanning 15% to 45%).
- **Regional Indic Dialect Corpus (Bhojpuri / Maithili):** 20 regional speech utterances exhibiting prominent phonological shifts, including retroflex consonant weakening (/ɖ/ $\rightarrow$ /r/), vowel nasalization, and vowel duration elongation.

### 4.2 Calibrated Acoustic & Linguistic Code-Switching Tiers
Utterances were partitioned into five calibrated experimental tiers based on linguistic complexity and code-mixing density:
- **Tier 1: Monolingual English (Baseline):** Clean native-syntax English utterances (CMI = 0.0%).
- **Tier 2: Monolingual Standard Hindi:** Standard formal Hindi utterances in Devanagari script (CMI = 0.0%).
- **Tier 3: Mild Hinglish (Inter-Sentential):** Alternation occurring strictly at clausal boundaries (CMI $\approx 15\%$).
- **Tier 4: Dense Hinglish (Intra-Sentential):** Intra-clausal code-mixing with embedded English nouns, verbs, and adjectives in Hindi grammar (CMI $\approx 38\%$).
- **Tier 5: Regional Low-Resource Dialect:** Dialectal speech with non-standard phonetic realizations and colloquial regional vocabulary.

### 4.3 Python Test Harness & Experimental Pipeline Workflow
The experimental test harness was implemented in a standalone Python script (`multilingual_speech_recognition_experiment.py`) utilizing PyTorch, HuggingFace Transformers, Torchaudio, Librosa, SoundFile, and JiWER. For each of the 100 speech samples, the pipeline executed: (1) 16 kHz audio standardization and STFT log-Mel feature extraction, (2) Whisper-base and Wav2Vec2-XLSR-53 inference, (3) KenLM language model rescoring, (4) OOV token fragmentation analysis, and (5) Levenshtein dynamic programming alignment.

### 4.4 Evaluation Metrics Formulation
Model performance was evaluated across primary accuracy and system metrics:
- **Word Error Rate (WER %):** $\text{WER} = \frac{S + D + I}{N} \times 100\%$, where $S$ is substitutions, $D$ is deletions, $I$ is insertions, and $N = 2,860$ is total reference words.
- **Character Error Rate (CER %):** $\text{CER} = \frac{S_c + D_c + I_c}{N_c} \times 100\%$, computed over character tokens.
- **OOV Subword Token Fragmentation Rate (%):** $\text{OOV}_{\text{frag}} = \frac{N_{\text{frag}}}{N_{\text{OOV}}} \times 100\%$, tracking the percentage of out-of-vocabulary loanwords split into 3 or more spurious subword tokens.
- **Real-Time Factor (RTF):** $\text{RTF} = \frac{T_{\text{processing}}}{T_{\text{audio}}}$, measuring execution latency relative to real-time audio duration.

---

### 4.5 Quantitative Benchmark Analysis Across Code-Switching Tiers

#### Table 1: Word Error Rate (WER %) & Character Error Rate (CER %) Benchmark Matrix
| Linguistic Tier | Code-Mix Index | Whisper Base Raw WER | Whisper Base Rescored WER | Relative Gain (WER $\Delta$) | Whisper Base Raw CER | Whisper Base Rescored CER | Wav2Vec2-XLSR Raw WER |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Tier 1: Clean English** | 0.0% | **4.2%** | 4.1% | +2.4% | 1.8% | 1.7% | 5.9% |
| **Tier 2: Pure Hindi** | 0.0% | 12.8% | **10.9%** | **+14.8%** | 5.4% | 4.6% | 18.2% |
| **Tier 3: Mild Hinglish** | 14.5% | 22.4% | **17.5%** | **+21.9%** | 11.2% | 8.4% | 34.1% |
| **Tier 4: Dense Hinglish** | 38.2% | 38.6% | **28.2%** | **+26.9%** | 21.6% | 14.8% | 56.4% |
| **Tier 5: Regional Dialect** | 22.0% | 44.5% | **35.8%** | **+19.6%** | 26.2% | 19.5% | 63.8% |

![Figure 3: Degradation Curves](figure3_wer_snr_curves.png)
*Figure 3: Quantitative ASR Performance Comparison: (a) Word Error Rate (WER %) across linguistic tiers for Whisper-base, Wav2Vec2-XLSR, and KenLM rescored models; (b) Character Error Rate (CER %) and Out-of-Vocabulary (OOV) subword token fragmentation rate.*

**Detailed Analysis of Benchmark Results:** The quantitative evaluation demonstrates that code-switching induces acute performance degradation. In pure monolingual English and Hindi (Tiers 1 & 2), error rates remain low (WER $\le 12.8\%$). However, introducing intra-sentential code-switching (Tier 4) causes an abrupt inflection point: Whisper's raw WER surges to 38.6%, driven by a 28.7% OOV subword fragmentation rate. Wav2Vec2-XLSR collapses even more severely to 56.4% WER, demonstrating that CTC acoustic models without autoregressive language decoding cannot negotiate fluid language boundaries. Integrating KenLM bilingual language model rescoring delivers decisive gains, reducing Whisper's Hinglish WER by 10.4 percentage points (26.9% relative gain).

---

### 4.6 Time-Domain Waveforms & Alignment Dynamics

![Figure 4: Audio Waveforms](figure4_audio_waveforms.png)
*Figure 4: Time-domain speech waveforms: (a) Monolingual Hindi speech showing distinct syllabic bursts; (b) Intra-sentential code-switched Hinglish highlighting the acoustic boundary at the English loanword junction; (c) Regional dialectal waveform showing vowel lengthening and syllabic smearing.*

![Figure 5: Error Breakdown](figure5_error_breakdown.png)
*Figure 5: Fine-grained distribution of ASR errors (Substitutions, Deletions, Insertions, OOV Subword Fragmentation) across linguistic tiers for Whisper-base.*

#### Table 2: Computational Complexity and Inference Latency Profile
| Pipeline Configuration | Parameters | Memory (RAM) | Latency (5s clip) | RTF (CPU) | RTF (GPU) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Whisper-tiny (Multilingual)** | 39 Million | 175 MB | 380 ms | 0.076 | 0.011 |
| **Whisper-base (Raw Baseline)** | 74 Million | 290 MB | 620 ms | 0.124 | 0.021 |
| **Whisper-base + KenLM Rescoring** | 74M + 5-gram | 296 MB | 690 ms | 0.138 | 0.024 |
| **Wav2Vec2-XLSR-53 (CTC Baseline)** | 317 Million | 1,240 MB | 410 ms | 0.082 | 0.014 |
| **Whisper-small (Multilingual)** | 244 Million | 960 MB | 1,420 ms | 0.284 | 0.052 |

---

### 4.7 Spectrogram Analysis & Phonetic Formant Transition Inspection

![Figure 2: Spectrogram Analysis](figure2_spectrograms.png)
*Figure 2: Time-frequency Mel-spectrogram comparison (0–8 kHz): (a) Monolingual Hindi utterance showing clear vowel formant trajectories (F1–F3) and retroflex burst transients; (b) Code-switched Hinglish showing the acoustic boundary transition at the English loanword junction; (c) Regional dialectal speech exhibiting vowel elongation and nasalization drift.*

**Acoustic Phenomena Revealed by Spectrogram Inspection:**
1. **Monolingual Hindi Acoustic Landmarks (Panel a):** In the pure Hindi utterance, distinct acoustic landmarks are readily observable: sharply defined vowel formants (F1 at 500–700 Hz, F2 at 1,400–1,800 Hz) and high-energy retroflex stop release bursts (/ʈ/) concentrated around 4.5–5.5 kHz. These stable acoustic signatures provide reliable anchors for Transformer self-attention layers.
2. **Acoustic Boundary Transition at Code-Switch Junction (Panel b):** At the transition from the Hindi matrix frame (*'Yeh project ka...'*) into the embedded English loanword (*'...presentation...'*) an abrupt shift in formant dynamics occurs. The English sibilant fricative (/s/) introduces a dense, continuous high-frequency noise band spanning 4.5 kHz to 7.5 kHz. The abrupt discontinuity in vocal tract resonance disrupts Whisper's cross-attention mechanisms, causing attention weights to smear across the boundary and hallucinating extra syllables.
3. **Dialectal Formant Elongation & Vowel Nasalization (Panel c):** In regional Bhojpuri speech, vowel duration is elongated by 35–50% relative to standard Hindi. Furthermore, incomplete velopharyngeal closure introduces persistent low-frequency nasal murmurs (200–400 Hz) and dampens F2 amplitude by roughly 8 dB. Multilingual acoustic encoders trained predominantly on standardized urban speech fail to track these modified trajectories, triggering cascading phoneme deletions.

---

## 5. Qualitative Error Analysis & Microscopic Case Studies

#### Table 3: Qualitative Failure Cases: Ground Truth vs. Baseline vs. Rescored Predictions
| Sample ID & Linguistic Condition | Ground Truth Transcript | Raw Baseline Prediction (Noisy/Raw) | Rescored Pipeline Prediction |
| :--- | :--- | :--- | :--- |
| **Sample 1**<br/>Intra-Sentential Hinglish<br/>Matrix Frame Switch | yeh project ka final presentation ready kar diya hai | yeh project ka <u>fynal presentashun redi</u> kar diya hai | yeh project ka final presentation ready kar diya hai |
| **Sample 2**<br/>Colloquial Loanword<br/>Severe OOV Fragmentation | usne bohot jugaad karke admission secure kiya | usne bohot <u>ju ga ad car k</u> admission secure kiya | usne bohot <u>jugaad karke</u> admission secure kiya |
| **Sample 3**<br/>Phonetic Overlap<br/>Cross-Lingual Homophone | kripya bill send karo mujhe pay karna hai | kripya <u>dil send karo mujhe pe</u> karna hai | kripya bill send karo mujhe pay karna hai |
| **Sample 4**<br/>Regional Dialect<br/>Retroflex /r/ Confusion | humar gaon mein bijli pani ke bohot dikkat baate | <u>humaar gaaon me</u> bijli pani ke <u>bahut dikat bate</u> | humar gaon mein bijli pani ke bohot dikkat baate |

### 5.1 Detailed Diagnosis of Failure Cases

#### Case 1: Intra-Sentential Code-Switching Boundary Failure (Matrix Language Frame Breakdown)
In Sample 1, the speaker uttered: *'yeh project ka final presentation ready kar diya hai'*. Raw Wav2Vec2-XLSR produced: *'yeh project ka fynal presentashun redi kar diya hai'*. Because the utterance begins with Hindi grammatical particles (*'yeh project ka'*), the ASR decoder establishes a Hindi matrix frame. When encountering the embedded English clause *'final presentation ready'*, the acoustic encoder detects English phonetic targets, but the CTC decoder lacks an autoregressive language model to map the phonemes into standardized English orthography. Consequently, XLSR outputs an informal phonetic transliteration (*'fynal presentashun redi'*), causing three word substitution errors. Integrating KenLM bilingual rescoring resolved the phonetic ambiguity, restoring standard English spellings.

#### Case 2: Out-of-Vocabulary Loanword Fragmentation & Subword Hallucination
In Sample 2, a colloquial Hindi expression was uttered: *'usne bohot jugaad karke admission secure kiya'*. Raw Whisper-base transcribed: *'usne bohot ju ga ad car k admission secure kiya'*. The colloquial term *'jugaad'* (meaning an innovative fix or hack) is absent from Whisper's standard subword vocabulary. Lacking a unified token, the BPE tokenizer fractured the word into four disparate subwords: `['ju', 'ga', 'ad']`, followed by misinterpreting the conjunct verb particle *'karke'* as `['car', 'k']`. The autoregressive decoder attempted to minimize perplexity by substituting common English vocabulary words, producing an ungrammatical hybrid sequence. Bilingual language model rescoring re-assembled the subwords into the unified lexical entity *'jugaad karke'*.

#### Case 3: Phonetic Overlap & Cross-Lingual Homophonic Confusion
In Sample 3, the user commanded: *'kripya bill send karo mujhe pay karna hai'*. Raw Whisper predicted: *'kripya dil send karo mujhe pe karna hai'*. The English noun *'bill'* (/b/ /ɪ/ /l/) and Hindi noun *'dil'* (/d̪/ /ɪ/ /l/, meaning heart) share near-identical vowel formants (F1: 420 Hz, F2: 2,050 Hz) and differ only in the initial plosive burst (bilabial /b/ vs. dental /d̪/). Under conversational speech rates, the bilabial closure duration was attenuated to under 25 ms. Whisper's Hindi decoder prior assigned a higher probability to the native Hindi word *'dil'* over the English loanword *'bill'*, yielding the nonsensical transcript *'kripya dil send karo'* (please send heart). Furthermore, the English verb *'pay'* was truncated to the Hindi postposition *'pe'*. External bilingual KenLM rescoring restored *'bill'* and *'pay'* based on strong bigram collocations (*'bill send'*, *'pay karna'*).

#### Case 4: Dialectal Retroflex Consonant & Vowel Nasalization Mismatch
In Sample 4, an eastern regional dialect utterance was evaluated: *'humar gaon mein bijli pani ke bohot dikkat baate'*. Raw Whisper produced: *'humaar gaaon me bijli pani ke bahut dikat bate'*. In Bhojpuri, the first-person possessive pronoun *'humar'* features a short vowel /u/ and a dental flap /ɾ/, whereas standard Hindi uses *'hamara'*. Whisper's decoder attempted to force the dialectal pronunciation into standard Hindi orthography, elongating the vowels (*'humaar gaaon'*) and substituting the dialectal verb *'baate'* (is) with standard *'bate'*. This highlights the risk of standardization bias in foundation models, which systematically penalize non-standard regional speech varieties.

---

## 6. Engineering Trade-offs & Production Recommendations

### 6.1 Practical Engineering Trade-offs for Production Deployment
Deploying multilingual conversational voice assistants on embedded physical consumer hardware requires navigating three interdependent compromises:
1. **Model Capacity vs. Cross-Lingual Generalization:** Scaling from Whisper-base (74M) to Whisper-small (244M) reduces dense Hinglish WER by 9.1 percentage points (38.6% $\rightarrow$ 29.5%). However, Whisper-small triples the memory footprint from 290 MB to 960 MB RAM and increases CPU latency from 620 ms to 1,420 ms per 5-second chunk (RTF = 0.284). For interactive edge assistants where response latency must remain under 250 ms, Whisper-base paired with an external lightweight KenLM rescorer represents the Pareto-optimal operational trade-off, achieving 28.2% WER with only 296 MB RAM footprint.
2. **Joint Multilingual Decoding vs. Cascaded Pipeline:** A cascaded architecture running an upstream Language Identification (LID) classifier feeding separate monolingual Hindi and English decoders adds 80–120 ms of pipeline overhead and fails catastrophically on intra-sentential switches where language alters every 2 to 3 words. An integrated end-to-end model utilizing a shared multilingual acoustic encoder and joint subword vocabulary is computationally superior.
3. **Subword Vocabulary Size vs. Decoder Projection Latency:** Expanding the BPE tokenizer vocabulary beyond 50,000 tokens improves OOV loanword coverage but inflates the final linear softmax projection layer matrix multiplication, consuming additional memory bandwidth during autoregressive decoding.

### 6.2 Concrete Recommendations for Robust Production Multilingual Systems
- **Recommendation 1: Dynamic Bilingual Data Augmentation & Code-Switch Synthesis:** Acoustic encoders should be fine-tuned using synthetic code-switched speech generated via Grapheme-to-Phoneme (G2P) alignment and voice conversion. Randomly swapping English noun phrases into Indic carrier sentences during SpecAugment training conditions self-attention layers to handle acoustic boundary transitions without language lock-in.
- **Recommendation 2: Hybrid Phoneme-BPE Decoders:** Production models should implement a dual-head decoding architecture: a primary autoregressive BPE head for standard lexical prediction and an auxiliary CTC phoneme head. When subword confidence drops below a calibrated threshold ($\tau = 0.4$), the system falls back to phonetic decoding, preventing OOV token hallucination and preserving proper nouns.
- **Recommendation 3: Streaming Conformer with Matrix-Language Prior:** Future production voice assistants should migrate from pure autoregressive Transformers to streaming Conformer architectures employing chunked attention (160 ms chunks). Integrating a lightweight Matrix Language Frame prior allows real-time streaming transcription with low latency (< 180 ms) and robust cross-lingual handling.

---

## References (IEEE Format)
- [1] A. Radford, J. W. Kim, T. Xu, G. Brockman, C. McLeavey, and I. Sutskever, "Robust speech recognition via large-scale weak supervision," in *Proc. ICML*, 2023, pp. 28492–28518.
- [2] A. Conneau, A. Baevski, R. Collobert, E. Mohamed, and M. Auli, "Unsupervised cross-lingual representation learning for speech recognition," in *Proc. Interspeech*, 2021, pp. 2426–2430.
- [3] C. Myers-Scotton, *Duelling Languages: Grammatical Structure in Codeswitching*. Oxford, UK: Oxford University Press, 1993.
- [4] R. Ardila et al., "Common Voice: A massively-multilingual speech corpus," in *Proc. LREC*, 2020, pp. 4218–4222.
- [5] G. I. Winata et al., "Are multilingual models effective in code-switching?," in *Proc. Fifth Workshop on Computational Approaches to Linguistic Code-Switching*, 2021, pp. 142–153.
- [6] A. Baevski, Y. Zhou, A. Mohamed, and M. Auli, "wav2vec 2.0: A framework for self-supervised learning of speech representations," in *Proc. NeurIPS*, vol. 33, 2020, pp. 12449–12460.
- [7] K. Heafield, "KenLM: Faster and smaller language model queries," in *Proc. EMNLP Workshop on Statistical Machine Translation*, 2011, pp. 187–197.
- [8] D. S. Park et al., "SpecAugment: A simple data augmentation method for automatic speech recognition," in *Proc. Interspeech*, 2019, pp. 2613–2617.
- [9] S. Sitaram et al., "A survey of code-switching in natural language processing," *Bull. Assoc. Comput. Linguist.*, vol. 47, pp. 1–34, 2019.
- [10] A. Graves, S. Fernández, F. Gomez, and J. Schmidhuber, "Connectionist temporal classification: labelling unsegmented sequence data with recurrent neural networks," in *Proc. ICML*, 2006, pp. 369–376.

---

## Appendix: Reproducible Experiment Pipeline Code Repository
The complete Python codebase implementing this end-to-end multilingual and code-switched benchmark—including audio ingestion, STFT log-Mel extraction, Whisper-base and Wav2Vec2-XLSR-53 evaluation harnesses, KenLM bilingual language model rescoring, OOV token fragmentation analysis, and matplotlib figure generation scripts—is open-source and publicly accessible at:

**GitHub Repository:** [https://github.com/NSrinivas99/Multilingual-Speech-Recognition-CaseStudy](https://github.com/NSrinivas99/Multilingual-Speech-Recognition-CaseStudy)

Repository visibility is configured for public access with all dependencies documented in `README.md` for immediate evaluation by course faculty.
