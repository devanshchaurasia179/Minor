# Quick Reference: EMG Authentication Accuracy Table

## All Participants - All Models Performance Matrix

| Participant | Random Forest | Gradient Boosting | SVM | MLP Neural Network | Best Accuracy | Best Model(s) |
|-------------|---------------|-------------------|-----|-------------------|---------------|---------------|
| **Saif** | **100.00%** ⭐ | **100.00%** ⭐ | **100.00%** ⭐ | **100.00%** ⭐ | **100.00%** | ALL |
| **Vanshish** | **100.00%** ⭐ | **100.00%** ⭐ | **100.00%** ⭐ | **100.00%** ⭐ | **100.00%** | ALL |
| **Chirag** | **100.00%** ⭐ | 72.73% | 90.91% | **100.00%** ⭐ | **100.00%** | RF, MLP |
| **Harshit** | 83.33% | **100.00%** ⭐ | 83.33% | **100.00%** ⭐ | **100.00%** | GB, MLP |
| **Divyansh** | 72.73% | **100.00%** ⭐ | 90.91% | 72.73% | **100.00%** | GB |
| **Divyesh** | 66.67% | **100.00%** ⭐ | 83.33% | 66.67% | **100.00%** | GB |
| **Sritiz** | 88.89% | 88.89% | 88.89% | 88.89% | 88.89% | All Tied |
| **Devansh** | 88.89% | 77.78% | 88.89% | 88.89% | 88.89% | RF, SVM, MLP |
| **Kartik** | 83.33% | 50.00% | 83.33% | 83.33% | 83.33% | RF, SVM, MLP |

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Participants** | 9 |
| **Total Models Tested** | 4 |
| **Perfect Scores (100%)** | 6 participants |
| **Average Best Accuracy** | 93.45% |
| **Overall System Accuracy** | 88.40% |

---

## Model Rankings (by average accuracy)

1. **MLP Neural Network** - 88.94%
2. **SVM** - 88.80%
3. **Gradient Boosting** - 88.38%
4. **Random Forest** - 88.14%

---

## Performance Categories

### ⭐⭐⭐ Outstanding (100% on ALL models)
- **Saif**
- **Vanshish**

### ⭐⭐⭐ Excellent (100% on at least ONE model)
- **Chirag** (100% on RF, MLP)
- **Divyansh** (100% on GB)
- **Divyesh** (100% on GB)
- **Harshit** (100% on GB, MLP)

### ⭐⭐ Good (83-89% best accuracy)
- **Devansh** (88.89%)
- **Sritiz** (88.89%)
- **Kartik** (83.33%)

---

## Security Metrics Summary

| Participant | Best FAR | Best FRR | Security Rating |
|-------------|----------|----------|-----------------|
| Saif | 0.00% | 0.00% | ⭐⭐⭐⭐⭐ Perfect |
| Vanshish | 0.00% | 0.00% | ⭐⭐⭐⭐⭐ Perfect |
| Chirag | 0.00% | 0.00% | ⭐⭐⭐⭐⭐ Perfect |
| Harshit | 0.00% | 0.00% | ⭐⭐⭐⭐⭐ Perfect |
| Divyansh | 0.00% | 0.00% | ⭐⭐⭐⭐⭐ Perfect |
| Divyesh | 0.00% | 0.00% | ⭐⭐⭐⭐⭐ Perfect |
| Devansh | 0.00% | 100.00% | ⭐⭐⭐⭐ Very Secure (rejects genuine) |
| Sritiz | 0.00% | 100.00% | ⭐⭐⭐⭐ Very Secure (rejects genuine) |
| Kartik | 0.00% | 100.00% | ⭐⭐⭐⭐ Very Secure (rejects genuine) |

**FAR** = False Accept Rate (impostor incorrectly accepted)  
**FRR** = False Reject Rate (genuine user incorrectly rejected)

---

## Recommended Deployment Configuration

| Participant | Deploy? | Model | Expected Accuracy |
|-------------|---------|-------|-------------------|
| Saif | ✅ YES | Any Model | 100% |
| Vanshish | ✅ YES | Any Model | 100% |
| Chirag | ✅ YES | Random Forest or MLP | 100% |
| Harshit | ✅ YES | Gradient Boosting or MLP | 100% |
| Divyansh | ✅ YES | Gradient Boosting | 100% |
| Divyesh | ✅ YES | Gradient Boosting | 100% |
| Devansh | ⚠️ REVIEW | RF/SVM/MLP | 88.89% |
| Sritiz | ⚠️ REVIEW | Any (all tied) | 88.89% |
| Kartik | ⚠️ REVIEW | RF or SVM | 83.33% |

---

**Note:** All accuracy values are test set performance metrics from One-vs-Rest classification.
