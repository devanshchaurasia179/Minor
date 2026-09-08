# Quick Start Guide - EMG Authentication System

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

This installs: numpy, pandas, scipy, scikit-learn, matplotlib, seaborn

---

### Step 2: Train the Models (2-5 minutes)

```bash
python emg_authentication.py
```

**What happens:**
- Loads all 48 EMG files
- Extracts ~140 features per file
- Trains 6 authentication models (one per person)
- Saves models to `emg_auth_models.pkl`

**Expected output:**
```
Loading EMG data files...
Found 48 files
Processing devansh-fist...
Processing devansh-snap...
...
Training model for: devansh
  RandomForest: CV Accuracy = 0.892
  Selected: RandomForest
  Test Accuracy: 0.903
...
Models saved to emg_auth_models.pkl
```

---

### Step 3: Test Authentication (30 seconds)

```bash
python test_authentication.py
```

**What happens:**
- Tests authentication on sample files
- Shows both genuine authentication and impostor detection
- Displays confidence scores

**Expected output:**
```
File: Devansh2-Snap-L01.txt
True Identity: devansh
Authentication Result: True
Confidence: 0.872

Imposter Test (divyesh): False
Imposter Confidence: 0.234
```

---

## 📊 Visualize Results (Optional)

```bash
python visualize_results.py
```

**Generates:**
- `accuracy_comparison.png` - Per-person accuracy chart
- `confusion_matrices.png` - Confusion matrix for each person
- `feature_importance.png` - Most important features
- `sample_signals.png` - Example EMG signals
- `feature_distributions.png` - Feature distributions across people

---

## 🎯 Interactive Testing

Test authentication manually with your own files:

```bash
python test_authentication.py interactive
```

Then follow prompts:
```
Enter person name: devansh
Enter path to EMG file: d:/Minor/Devansh2-Snap-L01.txt

AUTHENTICATION RESULT
Authenticated: ✓ YES
Confidence: 0.872
```

---

## 🔍 Cross-Validation Analysis

Detailed performance breakdown:

```bash
python test_authentication.py cv
```

Shows:
- Number of samples per person
- Cross-validation scores
- Data balance information

---

## 💡 Understanding the Results

### Good Results:
- **Accuracy > 0.85** ✅ Excellent
- **Accuracy 0.75-0.85** ✔️ Good
- **Accuracy < 0.75** ⚠️ Needs improvement

### If Accuracy is Low:
1. Check if person has enough data files (need at least 2-4)
2. Verify gesture consistency across recordings
3. Try adjusting authentication threshold
4. Consider collecting more data

---

## 📁 What Each File Does

| File | Purpose |
|------|---------|
| `emg_authentication.py` | Main training script - trains all models |
| `test_authentication.py` | Testing script - demo, interactive, CV modes |
| `visualize_results.py` | Creates plots and analysis report |
| `requirements.txt` | Python package dependencies |
| `README.md` | Complete documentation and methodology |
| `QUICKSTART.md` | This file - quick reference |
| `emg_auth_models.pkl` | Trained models (created by training) |

---

## 🎓 For Your Minor Project Report

### Key Points to Include:

**1. Problem Statement**
- Biometric authentication using EMG signals
- Differentiate individuals based on muscle activation patterns
- Two gestures: fist and snap

**2. Methodology**
- Feature extraction: 140+ time and frequency domain features
- Classification: One-vs-Rest approach with ensemble learning
- Models: Random Forest, Gradient Boosting, SVM, MLP

**3. Dataset**
- 6 people, 2 gestures, 48 total recordings
- 50 Hz sampling rate
- ~2000-2800 seconds per recording

**4. Results**
- Mean accuracy: [Insert your actual value from training]
- Best person: [Insert name and accuracy]
- Selected models: [Insert distribution from report]

**5. Evaluation Metrics**
- Accuracy, Confusion Matrix
- False Accept Rate (FAR), False Reject Rate (FRR)
- Confidence scores

**6. Visualizations**
- Include the generated PNG files in your report
- Confusion matrices show per-person performance
- Feature importance shows what distinguishes people

---

## 🐛 Troubleshooting

**Problem: "No module named 'numpy'"**
```bash
Solution: pip install -r requirements.txt
```

**Problem: "No data loaded"**
```bash
Solution: Verify .txt files are in d:/Minor/ directory
Check filenames contain person name and "fist" or "snap"
```

**Problem: "Model file not found"**
```bash
Solution: Run python emg_authentication.py first
```

**Problem: Low accuracy for specific person**
```bash
Reasons: 
- Insufficient data (need 2-4 recordings minimum)
- Inconsistent gesture execution
- Noisy signals

Solutions:
- Collect more data
- Use consistent electrode placement
- Filter signals (adjust in code)
```

---

## 🎯 Next Steps & Extensions

### Immediate:
1. ✅ Train models (Step 2)
2. ✅ Test authentication (Step 3)
3. ✅ Generate visualizations
4. ✅ Document results for report

### Advanced (For Extra Credit):
1. **Adjust threshold** - Balance FAR vs FRR
2. **Feature selection** - Use only top N features
3. **Ensemble gestures** - Combine fist + snap predictions
4. **Real-time demo** - Stream EMG and authenticate live
5. **Deep learning** - Try CNN or LSTM if you have time

---

## 📞 Quick Command Reference

```bash
# Setup
pip install -r requirements.txt

# Train
python emg_authentication.py

# Test (3 modes)
python test_authentication.py              # Auto demo
python test_authentication.py interactive  # Manual testing
python test_authentication.py cv          # Cross-validation

# Visualize
python visualize_results.py

# Check Python version
python --version  # Need 3.7+
```

---

## ⏱️ Time Estimates

- Installation: 1-2 minutes
- Training: 2-5 minutes (depending on CPU)
- Testing: 30 seconds
- Visualization: 1-2 minutes
- **Total: ~10 minutes to complete everything!**

---

## 🎉 Success Checklist

- [ ] Dependencies installed
- [ ] Training completed without errors
- [ ] `emg_auth_models.pkl` file created
- [ ] Test authentication runs successfully
- [ ] Visualizations generated (5 PNG files)
- [ ] Accuracy > 0.75 for most people
- [ ] Ready to write report!

---

**Good luck with your minor project! 🚀**

*If you encounter any issues, check the detailed README.md for more information.*
