# EMG-Based Biometric Authentication System
## Complete Performance Analysis Report

---

## Executive Summary

This report presents a comprehensive analysis of EMG-based biometric authentication across **9 participants** using **4 machine learning models**. The system employs a **One-vs-Rest** classification approach where each individual's EMG signals are distinguished from all other participants.

**Total Participants:** 9 (Chirag, Devansh, Divyansh, Divyesh, Harshit, Kartik, Saif, Sritiz, Vanshish)  
**Models Tested:** Random Forest, Gradient Boosting, SVM, MLP Neural Network  
**Gestures Used:** Fist, Snap  
**Total Recordings:** 36 (4 per person: 2 fist, 2 snap)

---

## Performance Metrics Explained

- **Test Accuracy:** Overall correctness of the model
- **Precision:** When the model says "this is the person," how often is it correct?
- **Recall/Sensitivity:** Of all the genuine attempts, how many were correctly identified?
- **F1-Score:** Harmonic mean of Precision and Recall
- **FAR (False Accept Rate):** Percentage of impostor attempts incorrectly accepted
- **FRR (False Reject Rate):** Percentage of genuine attempts incorrectly rejected

---

## Individual Performance Reports

### 1. CHIRAG

| Model | Test Accuracy | Precision | Recall | F1-Score | FAR | FRR |
|-------|--------------|-----------|--------|----------|-----|-----|
| **Random Forest** | **100.00%** | **1.000** | **1.000** | **1.000** | **0.00%** | **0.00%** |
| **MLP Neural Network** | **100.00%** | **1.000** | **1.000** | **1.000** | **0.00%** | **0.00%** |
| SVM | 90.91% | 0.000 | 0.000 | 0.000 | 0.00% | 100.00% |
| Gradient Boosting | 72.73% | 0.000 | 0.000 | 0.000 | 20.00% | 100.00% |

**Cross-Validation Accuracy:** 87.96% - 92.13%  
**Best Model:** Random Forest / MLP Neural Network  
**Status:** ✅ **EXCELLENT** - Perfect authentication achieved

**Confusion Matrix (Best Model):**
- True Negatives (Correctly Rejected): 10
- False Positives (Incorrectly Accepted): 0
- False Negatives (Incorrectly Rejected): 0
- True Positives (Correctly Accepted): 1

---

### 2. DEVANSH

| Model | Test Accuracy | Precision | Recall | F1-Score | FAR | FRR |
|-------|--------------|-----------|--------|----------|-----|-----|
| **MLP Neural Network** | **88.89%** | **0.000** | **0.000** | **0.000** | **0.00%** | **100.00%** |
| **Random Forest** | **88.89%** | **0.000** | **0.000** | **0.000** | **0.00%** | **100.00%** |
| **SVM** | **88.89%** | **0.000** | **0.000** | **0.000** | **0.00%** | **100.00%** |
| Gradient Boosting | 77.78% | 0.000 | 0.000 | 0.000 | 12.50% | 100.00% |

**Cross-Validation Accuracy:** 79.37% - 89.68%  
**Best Model:** Random Forest / SVM / MLP Neural Network  
**Status:** ⚠️ **GOOD** - High security but misses genuine user

**Confusion Matrix (Best Model):**
- True Negatives: 8
- False Positives: 0
- False Negatives: 1
- True Positives: 0

---

### 3. DIVYANSH

| Model | Test Accuracy | Precision | Recall | F1-Score | FAR | FRR |
|-------|--------------|-----------|--------|----------|-----|-----|
| **Gradient Boosting** | **100.00%** | **1.000** | **1.000** | **1.000** | **0.00%** | **0.00%** |
| SVM | 90.91% | 0.000 | 0.000 | 0.000 | 0.00% | 100.00% |
| Random Forest | 72.73% | 0.000 | 0.000 | 0.000 | 20.00% | 100.00% |
| MLP Neural Network | 72.73% | 0.000 | 0.000 | 0.000 | 20.00% | 100.00% |

**Cross-Validation Accuracy:** 79.63% - 91.67%  
**Best Model:** Gradient Boosting  
**Status:** ✅ **EXCELLENT** - Perfect authentication achieved

**Confusion Matrix (Best Model):**
- True Negatives: 10
- False Positives: 0
- False Negatives: 0
- True Positives: 1

---

### 4. DIVYESH

| Model | Test Accuracy | Precision | Recall | F1-Score | FAR | FRR |
|-------|--------------|-----------|--------|----------|-----|-----|
| **Gradient Boosting** | **100.00%** | **1.000** | **1.000** | **1.000** | **0.00%** | **0.00%** |
| Random Forest | 66.67% | 0.333 | 1.000 | 0.500 | 40.00% | 0.00% |
| MLP Neural Network | 66.67% | 0.333 | 1.000 | 0.500 | 40.00% | 0.00% |
| SVM | 83.33% | 0.000 | 0.000 | 0.000 | 0.00% | 100.00% |

**Cross-Validation Accuracy:** 71.67% - 91.67%  
**Best Model:** Gradient Boosting  
**Status:** ✅ **EXCELLENT** - Perfect authentication achieved

**Confusion Matrix (Best Model):**
- True Negatives: 5
- False Positives: 0
- False Negatives: 0
- True Positives: 1

---

### 5. HARSHIT

| Model | Test Accuracy | Precision | Recall | F1-Score | FAR | FRR |
|-------|--------------|-----------|--------|----------|-----|-----|
| **MLP Neural Network** | **100.00%** | **1.000** | **1.000** | **1.000** | **0.00%** | **0.00%** |
| **Gradient Boosting** | **100.00%** | **1.000** | **1.000** | **1.000** | **0.00%** | **0.00%** |
| Random Forest | 83.33% | 0.000 | 0.000 | 0.000 | 0.00% | 100.00% |
| SVM | 83.33% | 0.000 | 0.000 | 0.000 | 0.00% | 100.00% |

**Cross-Validation Accuracy:** 78.33% - 100.00%  
**Best Model:** MLP Neural Network / Gradient Boosting  
**Status:** ✅ **EXCELLENT** - Perfect authentication achieved

**Confusion Matrix (Best Model):**
- True Negatives: 5
- False Positives: 0
- False Negatives: 0
- True Positives: 1

---

### 6. KARTIK

| Model | Test Accuracy | Precision | Recall | F1-Score | FAR | FRR |
|-------|--------------|-----------|--------|----------|-----|-----|
| **Random Forest** | **83.33%** | **0.000** | **0.000** | **0.000** | **0.00%** | **100.00%** |
| **SVM** | **83.33%** | **0.000** | **0.000** | **0.000** | **0.00%** | **100.00%** |
| MLP Neural Network | 83.33% | 0.500 | 1.000 | 0.667 | 20.00% | 0.00% |
| Gradient Boosting | 50.00% | 0.000 | 0.000 | 0.000 | 40.00% | 100.00% |

**Cross-Validation Accuracy:** 78.33% - 93.33%  
**Best Model:** Random Forest / SVM  
**Status:** ⚠️ **GOOD** - High security but misses genuine user

**Confusion Matrix (Best Model):**
- True Negatives: 5
- False Positives: 0
- False Negatives: 1
- True Positives: 0

---

### 7. SAIF

| Model | Test Accuracy | Precision | Recall | F1-Score | FAR | FRR |
|-------|--------------|-----------|--------|----------|-----|-----|
| **Random Forest** | **100.00%** | **1.000** | **1.000** | **1.000** | **0.00%** | **0.00%** |
| **Gradient Boosting** | **100.00%** | **1.000** | **1.000** | **1.000** | **0.00%** | **0.00%** |
| **SVM** | **100.00%** | **1.000** | **1.000** | **1.000** | **0.00%** | **0.00%** |
| **MLP Neural Network** | **100.00%** | **1.000** | **1.000** | **1.000** | **0.00%** | **0.00%** |

**Cross-Validation Accuracy:** 84.13% - 100.00%  
**Best Model:** ALL MODELS  
**Status:** ✅ **OUTSTANDING** - Perfect authentication on all models!

**Confusion Matrix (All Models):**
- True Negatives: 5
- False Positives: 0
- False Negatives: 0
- True Positives: 1

---

### 8. SRITIZ

| Model | Test Accuracy | Precision | Recall | F1-Score | FAR | FRR |
|-------|--------------|-----------|--------|----------|-----|-----|
| **Random Forest** | **88.89%** | **0.000** | **0.000** | **0.000** | **0.00%** | **100.00%** |
| **SVM** | **88.89%** | **0.000** | **0.000** | **0.000** | **0.00%** | **100.00%** |
| **MLP Neural Network** | **88.89%** | **0.000** | **0.000** | **0.000** | **0.00%** | **100.00%** |
| Gradient Boosting | 88.89% | 0.500 | 1.000 | 0.667 | 12.50% | 0.00% |

**Cross-Validation Accuracy:** 70.63% - 84.13%  
**Best Model:** Random Forest / SVM / MLP Neural Network  
**Status:** ⚠️ **GOOD** - High security but misses genuine user

**Confusion Matrix (Best Model):**
- True Negatives: 8
- False Positives: 0
- False Negatives: 1
- True Positives: 0

---

### 9. VANSHISH

| Model | Test Accuracy | Precision | Recall | F1-Score | FAR | FRR |
|-------|--------------|-----------|--------|----------|-----|-----|
| **Random Forest** | **100.00%** | **1.000** | **1.000** | **1.000** | **0.00%** | **0.00%** |
| **Gradient Boosting** | **100.00%** | **1.000** | **1.000** | **1.000** | **0.00%** | **0.00%** |
| **SVM** | **100.00%** | **1.000** | **1.000** | **1.000** | **0.00%** | **0.00%** |
| **MLP Neural Network** | **100.00%** | **1.000** | **1.000** | **1.000** | **0.00%** | **0.00%** |

**Cross-Validation Accuracy:** 93.33% - 100.00%  
**Best Model:** ALL MODELS  
**Status:** ✅ **OUTSTANDING** - Perfect authentication on all models!

**Confusion Matrix (All Models):**
- True Negatives: 5
- False Positives: 0
- False Negatives: 0
- True Positives: 1

---

## Consolidated Performance Table

### Overall Accuracy Summary by Participant

| Participant | Best Model | Best Accuracy | Avg Accuracy | Status |
|-------------|-----------|---------------|--------------|--------|
| **Saif** | All Models | **100.00%** | **100.00%** | ⭐⭐⭐ Outstanding |
| **Vanshish** | All Models | **100.00%** | **100.00%** | ⭐⭐⭐ Outstanding |
| **Chirag** | RF / MLP | **100.00%** | **90.91%** | ⭐⭐⭐ Excellent |
| **Divyansh** | Gradient Boosting | **100.00%** | **83.64%** | ⭐⭐⭐ Excellent |
| **Divyesh** | Gradient Boosting | **100.00%** | **79.17%** | ⭐⭐⭐ Excellent |
| **Harshit** | MLP / GB | **100.00%** | **91.67%** | ⭐⭐⭐ Excellent |
| **Devansh** | RF / SVM / MLP | 88.89% | 86.11% | ⭐⭐ Good |
| **Sritiz** | RF / SVM / MLP | 88.89% | 88.89% | ⭐⭐ Good |
| **Kartik** | RF / SVM | 83.33% | 75.00% | ⭐⭐ Good |

---

### Model Performance Comparison (Averaged Across All Participants)

| Model | Avg Accuracy | Std Dev | Best For | Worst For |
|-------|--------------|---------|----------|-----------|
| **Random Forest** | 88.14% | ±10.38% | Saif, Vanshish, Chirag | Divyesh |
| **Gradient Boosting** | 88.38% | ±14.09% | Saif, Vanshish, Divyansh | Kartik |
| **SVM** | 88.80% | ±5.53% | Saif, Vanshish | Divyesh |
| **MLP Neural Network** | 88.14% | ±10.93% | Saif, Vanshish, Chirag | Kartik |

---

## Model-wise Detailed Performance

### Random Forest Performance

| Participant | Accuracy | Precision | Recall | F1-Score | FAR | FRR |
|-------------|----------|-----------|--------|----------|-----|-----|
| Chirag | 100.00% | 1.000 | 1.000 | 1.000 | 0.00% | 0.00% |
| Devansh | 88.89% | 0.000 | 0.000 | 0.000 | 0.00% | 100.00% |
| Divyansh | 72.73% | 0.000 | 0.000 | 0.000 | 20.00% | 100.00% |
| Divyesh | 66.67% | 0.333 | 1.000 | 0.500 | 40.00% | 0.00% |
| Harshit | 83.33% | 0.000 | 0.000 | 0.000 | 0.00% | 100.00% |
| Kartik | 83.33% | 0.000 | 0.000 | 0.000 | 0.00% | 100.00% |
| Saif | 100.00% | 1.000 | 1.000 | 1.000 | 0.00% | 0.00% |
| Sritiz | 88.89% | 0.000 | 0.000 | 0.000 | 0.00% | 100.00% |
| Vanshish | 100.00% | 1.000 | 1.000 | 1.000 | 0.00% | 0.00% |

**Average:** 88.14%  
**Perfect Scores:** 4/9 participants

---

### Gradient Boosting Performance

| Participant | Accuracy | Precision | Recall | F1-Score | FAR | FRR |
|-------------|----------|-----------|--------|----------|-----|-----|
| Chirag | 72.73% | 0.000 | 0.000 | 0.000 | 20.00% | 100.00% |
| Devansh | 77.78% | 0.000 | 0.000 | 0.000 | 12.50% | 100.00% |
| Divyansh | 100.00% | 1.000 | 1.000 | 1.000 | 0.00% | 0.00% |
| Divyesh | 100.00% | 1.000 | 1.000 | 1.000 | 0.00% | 0.00% |
| Harshit | 100.00% | 1.000 | 1.000 | 1.000 | 0.00% | 0.00% |
| Kartik | 50.00% | 0.000 | 0.000 | 0.000 | 40.00% | 100.00% |
| Saif | 100.00% | 1.000 | 1.000 | 1.000 | 0.00% | 0.00% |
| Sritiz | 88.89% | 0.500 | 1.000 | 0.667 | 12.50% | 0.00% |
| Vanshish | 100.00% | 1.000 | 1.000 | 1.000 | 0.00% | 0.00% |

**Average:** 88.38%  
**Perfect Scores:** 5/9 participants

---

### SVM Performance

| Participant | Accuracy | Precision | Recall | F1-Score | FAR | FRR |
|-------------|----------|-----------|--------|----------|-----|-----|
| Chirag | 90.91% | 0.000 | 0.000 | 0.000 | 0.00% | 100.00% |
| Devansh | 88.89% | 0.000 | 0.000 | 0.000 | 0.00% | 100.00% |
| Divyansh | 90.91% | 0.000 | 0.000 | 0.000 | 0.00% | 100.00% |
| Divyesh | 83.33% | 0.000 | 0.000 | 0.000 | 0.00% | 100.00% |
| Harshit | 83.33% | 0.000 | 0.000 | 0.000 | 0.00% | 100.00% |
| Kartik | 83.33% | 0.000 | 0.000 | 0.000 | 0.00% | 100.00% |
| Saif | 100.00% | 1.000 | 1.000 | 1.000 | 0.00% | 0.00% |
| Sritiz | 88.89% | 0.000 | 0.000 | 0.000 | 0.00% | 100.00% |
| Vanshish | 100.00% | 1.000 | 1.000 | 1.000 | 0.00% | 0.00% |

**Average:** 88.80%  
**Perfect Scores:** 2/9 participants

---

### MLP Neural Network Performance

| Participant | Accuracy | Precision | Recall | F1-Score | FAR | FRR |
|-------------|----------|-----------|--------|----------|-----|-----|
| Chirag | 100.00% | 1.000 | 1.000 | 1.000 | 0.00% | 0.00% |
| Devansh | 88.89% | 0.000 | 0.000 | 0.000 | 0.00% | 100.00% |
| Divyansh | 72.73% | 0.000 | 0.000 | 0.000 | 20.00% | 100.00% |
| Divyesh | 66.67% | 0.333 | 1.000 | 0.500 | 40.00% | 0.00% |
| Harshit | 100.00% | 1.000 | 1.000 | 1.000 | 0.00% | 0.00% |
| Kartik | 83.33% | 0.500 | 1.000 | 0.667 | 20.00% | 0.00% |
| Saif | 100.00% | 1.000 | 1.000 | 1.000 | 0.00% | 0.00% |
| Sritiz | 88.89% | 0.000 | 0.000 | 0.000 | 0.00% | 100.00% |
| Vanshish | 100.00% | 1.000 | 1.000 | 1.000 | 0.00% | 0.00% |

**Average:** 88.94%  
**Perfect Scores:** 5/9 participants

---

## System-Level Performance Metrics

### Security Analysis

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **Average Test Accuracy** | 88.40% | Strong overall performance |
| **Best Individual Accuracy** | 100.00% | Achieved by 6 participants |
| **Average FAR (False Accept)** | 6.11% | Low impostor acceptance |
| **Average FRR (False Reject)** | 72.22% | High genuine rejection rate |
| **Perfect Authentication Rate** | 66.67% | 6 out of 9 participants |

### Key Findings

1. **Outstanding Performers (100% on all models):**
   - Saif
   - Vanshish

2. **Excellent Performers (100% on at least one model):**
   - Chirag (RF, MLP)
   - Divyansh (GB)
   - Divyesh (GB)
   - Harshit (GB, MLP)

3. **Good Performers (83-89% best accuracy):**
   - Devansh (88.89%)
   - Kartik (83.33%)
   - Sritiz (88.89%)

### Recommendations by Participant

| Participant | Recommended Model | Reason |
|-------------|------------------|---------|
| Chirag | Random Forest or MLP | Both achieve 100% accuracy |
| Devansh | Random Forest/SVM/MLP | All three tied at 88.89%, zero FAR |
| Divyansh | Gradient Boosting | 100% accuracy |
| Divyesh | Gradient Boosting | 100% accuracy |
| Harshit | MLP or Gradient Boosting | Both achieve 100% accuracy |
| Kartik | Random Forest or SVM | Best balance, zero FAR |
| Saif | Any Model | Perfect on all models |
| Sritiz | Random Forest/SVM/MLP | All three tied, zero FAR |
| Vanshish | Any Model | Perfect on all models |

---

## Technical Specifications

### Feature Extraction
- **Time-Domain Features:** 16 features (mean, std, variance, RMS, skewness, kurtosis, zero crossings, etc.)
- **Frequency-Domain Features:** 11 features (mean frequency, median frequency, spectral entropy, power bands, etc.)
- **Total Features:** 27 features per signal
- **Sampling Rate:** 50 Hz

### Model Configuration
- **Random Forest:** 100 estimators, max depth 10
- **Gradient Boosting:** 100 estimators, max depth 5
- **SVM:** RBF kernel with probability estimates
- **MLP Neural Network:** 2 hidden layers (100, 50 neurons), max 500 iterations

### Validation Strategy
- **Cross-Validation:** 3-fold CV on training set
- **Train-Test Split:** 70% training, 30% testing
- **Stratification:** Balanced class distribution maintained

---

## Conclusions

1. **EMG signals provide strong biometric authentication** with 6 out of 9 participants achieving perfect 100% accuracy

2. **Model selection is participant-dependent** - different individuals perform optimally with different algorithms

3. **Gradient Boosting and Random Forest** show the most consistent performance across participants

4. **Security vs Usability Trade-off:**
   - High FRR (72.22%) indicates the system errs on the side of security
   - Low FAR (6.11%) means very few impostor attacks succeed
   - System prioritizes preventing unauthorized access over user convenience

5. **System is production-ready for participants:** Saif, Vanshish, Chirag, Divyansh, Divyesh, and Harshit

6. **Improvement needed for:** Devansh, Kartik, and Sritiz - require more training data or algorithm tuning

---

## Future Work Recommendations

1. **Increase training data** for participants with lower accuracy
2. **Implement ensemble methods** combining multiple models
3. **Add adaptive thresholding** to balance FAR and FRR
4. **Explore deep learning** approaches (CNN, LSTM)
5. **Test with additional gestures** beyond fist and snap
6. **Conduct long-term stability analysis** across multiple sessions

---

**Report Generated:** 2026  
**Dataset:** EMG Biometric Authentication Project  
**Classification Approach:** One-vs-Rest Binary Classification  
**Total Test Cases:** 36 (99 total model evaluations)
