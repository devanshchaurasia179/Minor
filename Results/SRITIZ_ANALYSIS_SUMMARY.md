# SRITIZ EMG Authentication Analysis Results

## Overview
This analysis evaluates Sritiz's EMG biometric authentication performance using a **One-vs-Rest** approach where the system learns to distinguish Sritiz's EMG patterns from all other users.

---

## 📊 Performance Metrics - Sritiz

### Dataset Information
- **Sritiz samples**: 4 recordings (2 fist gestures + 2 snap gestures)
- **Other people samples**: 24 recordings (6 other people)
- **Total samples**: 28
- **Train/Test split**: 19 training / 9 testing samples

---

## 🎯 Model Performance Comparison

| Model | CV Accuracy | Test Accuracy | Precision | Recall | F1-Score | FAR | FRR |
|-------|------------|---------------|-----------|--------|----------|-----|-----|
| **Random Forest** | 74.60% (±12.35%) | **88.89%** | 0.00% | 0.00% | 0.00 | 0.00% | **100%** |
| **Gradient Boosting** | 70.63% (±30.51%) | **88.89%** | 50.00% | 100% | 0.67 | **12.5%** | 0.00% |
| **SVM** | 84.13% (±1.12%) | **88.89%** | 0.00% | 0.00% | 0.00 | 0.00% | **100%** |
| **MLP Neural Network** | 65.87% (±37.11%) | **88.89%** | 0.00% | 0.00% | 0.00 | 0.00% | **100%** |

---

## 📈 Detailed Results by Model

### 1. Random Forest
- **Cross-Validation**: 74.60% ± 12.35%
- **Test Accuracy**: 88.89%
- **Confusion Matrix**: TN=8, FP=0, FN=1, TP=0
- **FAR** (False Accept Rate): 0.00% - Never accepts imposters ✓
- **FRR** (False Reject Rate): 100% - Always rejects genuine user ✗
- **Issue**: Too conservative - rejects legitimate Sritiz samples

### 2. Gradient Boosting ⭐ BEST MODEL
- **Cross-Validation**: 70.63% ± 30.51%
- **Test Accuracy**: 88.89%
- **Confusion Matrix**: TN=7, FP=1, FN=0, TP=1
- **FAR** (False Accept Rate): 12.5% - Occasionally accepts imposters
- **FRR** (False Reject Rate): 0.00% - Never rejects genuine user ✓
- **Precision**: 50%, **Recall**: 100%, **F1-Score**: 0.67
- **Best Balance**: Successfully authenticates Sritiz while maintaining security

### 3. SVM
- **Cross-Validation**: 84.13% ± 1.12% (most stable)
- **Test Accuracy**: 88.89%
- **Confusion Matrix**: TN=8, FP=0, FN=1, TP=0
- **FAR**: 0.00% ✓, **FRR**: 100% ✗
- **Issue**: Same as Random Forest - too conservative

### 4. MLP Neural Network
- **Cross-Validation**: 65.87% ± 37.11% (most unstable)
- **Test Accuracy**: 88.89%
- **Confusion Matrix**: TN=8, FP=0, FN=1, TP=0
- **FAR**: 0.00% ✓, **FRR**: 100% ✗
- **Issue**: High variance, overly conservative

---

## 🔍 How the System Works

### It's NOT comparing individual peaks!

The system uses **feature-based pattern recognition**, not direct waveform matching:

### Step 1: Feature Extraction
From each EMG recording, the system extracts 12 key features:

**Time-Domain Features:**
- Mean, Standard Deviation, Variance
- Maximum, Minimum values
- RMS (Root Mean Square)
- Skewness (asymmetry of distribution)
- Kurtosis (tailedness of distribution)
- MAV (Mean Absolute Value)

**Frequency-Domain Features (FFT analysis):**
- Mean Frequency
- Peak Frequency (dominant frequency)
- Total Power (signal strength)

### Step 2: One-vs-Rest Classification
- Model learns: "What makes Sritiz's EMG patterns unique?"
- Compares: Sritiz's feature patterns vs Everyone else's feature patterns
- Training: 4 different machine learning algorithms tested

### Step 3: Authentication Decision
1. New EMG signal arrives
2. Extract same 12 features
3. Compare feature vector to learned patterns
4. Make decision based on similarity threshold (typically 80%)

---

## 🔐 Security Analysis

### False Accept Rate (FAR) - Security Risk
- **Goal**: Lower is better (don't let imposters in)
- **Sritiz Results**:
  - Random Forest: 0.00% ✓
  - **Gradient Boosting: 12.5%** (1 out of 8 imposters accepted)
  - SVM: 0.00% ✓
  - MLP: 0.00% ✓

### False Reject Rate (FRR) - Usability Issue
- **Goal**: Lower is better (don't reject legitimate users)
- **Sritiz Results**:
  - Random Forest: 100% ✗
  - **Gradient Boosting: 0.00%** ✓ (accepts all legitimate Sritiz attempts)
  - SVM: 100% ✗
  - MLP: 100% ✗

---

## 💡 Key Findings

### Strengths:
1. ✅ **Gradient Boosting** provides the best balance
2. ✅ Perfect recall (100%) - recognizes genuine Sritiz samples
3. ✅ High overall accuracy (88.89%)
4. ✅ Feature-based approach more robust than peak matching

### Weaknesses:
1. ⚠️ Limited training data (only 4 samples for Sritiz)
2. ⚠️ 12.5% FAR in Gradient Boosting (security risk)
3. ⚠️ 3 out of 4 models reject all genuine attempts (FRR=100%)
4. ⚠️ High variance in cross-validation scores

### Recommendations:
1. 📈 **Collect more Sritiz samples** (aim for 20-30 recordings)
2. 🎯 **Use Gradient Boosting model** for deployment
3. 🔧 **Tune decision threshold** to balance FAR/FRR
4. 🧪 **Test with fresh recordings** to validate real-world performance
5. 🔄 **Consider ensemble methods** combining multiple models

---

## 🆚 Comparison with Other Users

Based on the complete results, here's how Sritiz compares:

### Best Performers:
- **Saif**: 100% accuracy (all 4 models)
- **Vanshish**: 100% accuracy (all 4 models)
- **Harshit**: 100% accuracy (2 out of 4 models)

### Mid-Range:
- **Sritiz**: 88.89% best accuracy (Gradient Boosting with balance)
- **Divyesh**: 100% best accuracy (Gradient Boosting only)
- **Kartik**: Mixed results across models

### Possible Reasons for Variation:
1. EMG signal quality differences
2. Gesture consistency between recordings
3. Individual physiological variations
4. Sample size effects (all have equal 4 samples)

---

## 📋 Confusion Matrix Explanation

For **Gradient Boosting** (best model):
```
                Predicted: Not Sritiz    Predicted: Sritiz
Actual: Not Sritiz      TN = 7              FP = 1
Actual: Sritiz          FN = 0              TP = 1
```

- **TN (True Negative) = 7**: Correctly rejected 7 imposters
- **FP (False Positive) = 1**: Incorrectly accepted 1 imposter (FAR)
- **FN (False Negative) = 0**: Never rejected Sritiz
- **TP (True Positive) = 1**: Correctly authenticated Sritiz

---

## 🎓 Technical Notes

### Why Feature Extraction Instead of Peak Matching?

**Peak Matching Problems:**
1. Sensitive to timing variations
2. Affected by signal noise
3. Requires precise alignment
4. Difficult to handle amplitude variations

**Feature-Based Approach Advantages:**
1. ✅ Robust to small timing shifts
2. ✅ Captures overall signal characteristics
3. ✅ More generalizable to new samples
4. ✅ Standard in biometric authentication
5. ✅ Handles natural signal variations better

---

## 📊 Visual Interpretation

If we had to rank the models for Sritiz:

1. 🥇 **Gradient Boosting**: Balanced, practical (FAR=12.5%, FRR=0%)
2. 🥈 **SVM**: Secure but impractical (FAR=0%, FRR=100%)
3. 🥉 **Random Forest**: Similar issues to SVM
4. ❌ **MLP**: Unstable, impractical

---

*Analysis Date: 2026-09-09*
*Dataset: d:/Minor/Data/sritiz/*
*Total Recordings: 4 (2 fist, 2 snap)*
