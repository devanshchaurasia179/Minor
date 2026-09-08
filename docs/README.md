# EMG-Based Biometric Authentication System

## Project Overview

This system uses **Electromyography (EMG) signals** from two gestures (**fist** and **snap**) to authenticate individuals. It implements a machine learning-based biometric authentication approach that can differentiate between authorized users and imposters based on the unique characteristics of their muscle activation patterns.

### Key Objectives
- **Person Authentication**: Verify if an EMG signal belongs to a claimed identity
- **Gesture Independence**: Use multiple gesture types (fist/snap) as authentication factors
- **High Accuracy**: Achieve reliable discrimination between individuals

---

## Methodology

### 1. **Feature Extraction**

The system extracts comprehensive features from EMG signals in two domains:

#### **Time-Domain Features** (20+ features)
- **Statistical**: Mean, standard deviation, variance, median, min, max, range
- **Energy-based**: Root mean square (RMS), mean absolute value (MAV), integrated EMG (IEMG)
- **Morphological**: Zero-crossing rate, slope sign changes, waveform length, Willison amplitude
- **Higher-order statistics**: Skewness, kurtosis

#### **Frequency-Domain Features** (15+ features)
- **Spectral characteristics**: Mean frequency, median frequency, peak frequency
- **Power analysis**: Total power, power in frequency bands (0-10Hz, 10-25Hz, 25-50Hz)
- **Band ratios**: Relative power distribution across frequency bands
- **Spectral entropy**: Measure of signal complexity in frequency domain

#### **Sliding Window Segmentation**
- **Window size**: 1 second (50 samples at 50Hz)
- **Overlap**: 50% (0.5 seconds)
- **Aggregation**: Features extracted per segment, then aggregated (mean, std, min, max) across all segments

This produces **~140 features per recording** that capture the unique "signature" of each person's muscle activation patterns.

### 2. **Classification Approach: One-vs-Rest (OvR)**

We use a **One-vs-Rest** strategy where:
- Each person gets their own binary classifier
- Classifier learns: "This person" vs "All other people"
- During authentication: Use the classifier for the claimed identity

**Why One-vs-Rest?**
- ✅ Naturally suited for authentication scenarios (verify claimed identity)
- ✅ Scales well with new users (add one model per person)
- ✅ Provides confidence scores for authentication decisions
- ✅ Handles imbalanced data well (one person vs many others)

### 3. **Model Selection**

The system trains multiple classifiers and selects the best for each person:

1. **Random Forest** - Ensemble of decision trees, robust to overfitting
2. **Gradient Boosting** - Sequential ensemble with high accuracy
3. **Support Vector Machine (SVM)** - Effective for high-dimensional feature spaces
4. **Multi-Layer Perceptron (MLP)** - Neural network for complex patterns

**Selection Criteria**: 3-fold cross-validation accuracy on training data

### 4. **Authentication Process**

```
Input: EMG Signal + Claimed Identity
       ↓
1. Segment signal into 1-second windows
       ↓
2. Extract time & frequency features per segment
       ↓
3. Aggregate features across segments
       ↓
4. Normalize using trained scaler
       ↓
5. Apply person-specific classifier
       ↓
6. Get prediction + confidence score
       ↓
Output: Authenticated (Yes/No) + Confidence
```

**Authentication Threshold**: Confidence ≥ 0.5 (adjustable)

---

## Dataset

### Data Structure
- **Format**: Tab-separated text files with 2 columns
  - Column 1: Raw EMG signal
  - Column 2: Processed signal (integrated/smoothed)
- **Sampling Rate**: 50 Hz
- **Recording Length**: ~2000-2800 seconds per file (33-47 minutes)

### Participants & Gestures
- **People**: 6 individuals (Devansh, Divyesh, Harshit, Kartik, Saif, Vanshish)
- **Gestures**: 2 types (fist, snap)
- **Recordings**: 2-4 trials per person per gesture
- **Total Files**: 48 EMG recordings

### File Naming Convention
```
{person}-{gesture}-{trial}-L01.txt
Examples:
- devansh-fist-1-L01.txt
- harshit-snap-2-L01.txt
```

---

## Installation & Setup

### Prerequisites
- Python 3.7+
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- numpy (numerical operations)
- pandas (data manipulation)
- scipy (signal processing, FFT)
- scikit-learn (machine learning)
- matplotlib, seaborn (visualization - optional)

---

## Usage

### 1. Train the Authentication Models

```bash
python emg_authentication.py
```

**What it does:**
- Loads all 48 EMG files from `d:/Minor/`
- Extracts features from each recording
- Trains one classifier per person
- Saves trained models to `emg_auth_models.pkl`

**Expected Output:**
```
Loading EMG data files...
Found 48 files
Processing devansh-fist...
Processing devansh-snap...
...
Training One-vs-Rest Authentication Models
============================================================
Training model for: devansh
  RandomForest: CV Accuracy = 0.892 (+/- 0.023)
  GradientBoosting: CV Accuracy = 0.876 (+/- 0.031)
  Selected: RandomForest
  Test Accuracy: 0.903
...
Models saved to emg_auth_models.pkl
```

### 2. Test Authentication

#### A. Automated Demo
```bash
python test_authentication.py
```

Tests authentication on first 10 files with both genuine and impostor attempts.

#### B. Interactive Mode
```bash
python test_authentication.py interactive
```

Allows manual testing:
```
Enter person name: devansh
Enter path to EMG file: d:/Minor/Devansh2-Snap-L01.txt

AUTHENTICATION RESULT
============================================================
Claimed Identity: devansh
Authenticated: ✓ YES
Confidence: 0.872
Threshold: 0.5
Reason: Authentication successful
```

#### C. Cross-Validation Analysis
```bash
python test_authentication.py cv
```

Detailed per-person performance analysis.

### 3. Programmatic Use

```python
from emg_authentication import EMGAuthenticationSystem

# Load trained models
auth_system = EMGAuthenticationSystem()
auth_system.load_models('emg_auth_models.pkl')

# Load new EMG signal
signal = auth_system.load_data_file('path/to/emg_file.txt')

# Authenticate
result = auth_system.authenticate(
    signal_data=signal,
    claimed_identity='devansh',
    threshold=0.5
)

if result['authenticated']:
    print(f"Authenticated with {result['confidence']:.2%} confidence")
else:
    print(f"Authentication failed: {result['reason']}")
```

---

## Performance Metrics

### Evaluation Metrics

1. **Accuracy**: Overall correct classification rate
2. **False Acceptance Rate (FAR)**: Impostor incorrectly authenticated
3. **False Rejection Rate (FRR)**: Genuine user incorrectly rejected
4. **Confidence Score**: Probability output from classifier (0-1)

### Expected Performance

Based on EMG biometric literature and similar systems:
- **Genuine User Accuracy**: 85-95%
- **Impostor Rejection Rate**: 90-98%
- **Cross-validation Score**: 87-93%

*Actual performance depends on data quality, recording conditions, and individual variability.*

---

## Technical Details

### Why These Features?

1. **Time-domain features** capture signal amplitude, variability, and temporal patterns
2. **Frequency-domain features** capture muscle firing rates and contraction patterns
3. **Statistical aggregation** provides robustness to noise and recording variability
4. **Multiple segments** capture gesture dynamics over time

### Feature Importance

Most discriminative features typically include:
- RMS and MAV (muscle activation strength)
- Zero-crossing rate (firing patterns)
- Frequency band ratios (individual muscle characteristics)
- Waveform length (gesture execution style)

### Advantages of This Approach

✅ **No password to remember** - Biometric authentication  
✅ **Multi-gesture support** - Can use different gestures as authentication factors  
✅ **Scalable** - Easy to add new users (train one model)  
✅ **Robust features** - Combines time and frequency domain  
✅ **Interpretable** - Feature-based approach (not black box)  
✅ **Adjustable security** - Threshold can be tuned for FAR/FRR tradeoff  

### Limitations & Challenges

⚠️ **Gesture consistency** - Users must perform gestures similarly  
⚠️ **Electrode placement** - Must be consistent across sessions  
⚠️ **Muscle fatigue** - Long-term changes in muscle response  
⚠️ **Environmental noise** - EMG signals can be noisy  
⚠️ **Limited data** - Only 2-4 samples per person per gesture  

---

## Improving Performance

### If Accuracy is Low:

1. **Collect more data** - More trials per person improve generalization
2. **Consistent recording** - Ensure same electrode placement, gesture execution
3. **Adjust threshold** - Lower threshold = higher FAR, lower FRR (or vice versa)
4. **Feature selection** - Use feature importance analysis to select best features
5. **Hyperparameter tuning** - Optimize classifier parameters (n_estimators, max_depth, etc.)
6. **Data augmentation** - Add noise, shift signals, or segment differently
7. **Deep learning** - Try CNN or LSTM if more data becomes available

### Advanced Enhancements:

- **Template matching** with Dynamic Time Warping (DTW)
- **Siamese networks** for similarity learning
- **Ensemble of gestures** - Combine fist + snap for multi-factor authentication
- **Continuous authentication** - Monitor throughout session, not just at login
- **Anomaly detection** - Flag unusual patterns that don't match any user

---

## Project Structure

```
d:/Minor/
├── emg_authentication.py      # Main training script
├── test_authentication.py     # Testing and demo script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── emg_auth_models.pkl       # Trained models (generated)
└── *.txt                     # EMG data files (48 files)
```

---

## References & Further Reading

### EMG Biometric Authentication Papers:
1. Yamaba et al. (2020) - "Evaluation of Feature Extraction Methods for EMG-based User Authentication"
2. Blasco et al. (2016) - "A Survey of Wearable Biometric Recognition Systems"
3. Cannan & Hu (2013) - "Human identification via electromyogram- and electrocardiogram-based systems"

### Key Concepts:
- **EMG Signal Processing**: Filtering, segmentation, feature extraction
- **Biometric Authentication**: FAR, FRR, EER (Equal Error Rate)
- **One-vs-Rest Classification**: Multi-class to binary reduction
- **Feature Engineering**: Time-domain, frequency-domain, time-frequency analysis

---

## Troubleshooting

### Common Issues:

**Q: "Error: No data loaded!"**  
A: Check that EMG .txt files are in `d:/Minor/` directory

**Q: "Model file not found"**  
A: Run `python emg_authentication.py` first to train models

**Q: Low authentication accuracy**  
A: Try adjusting threshold, collecting more data, or ensuring consistent gesture execution

**Q: "could not parse filename"**  
A: Ensure filenames follow format: `{person}-{gesture}-{trial}-L01.txt`

---

## License & Citation

This project is developed for academic purposes as part of a minor project.

If you use this code or approach in your research, please cite:

```
EMG-Based Biometric Authentication System
Authors: [Your names]
Institution: [Your institution]
Year: 2026
```

---

## Contact & Support

For questions, issues, or improvements:
- Check the code comments for detailed explanations
- Review the paper references for theoretical background
- Experiment with different parameters and features

**Good luck with your minor project! 🚀**
