# Getting Started - EMG Authentication System

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Install Dependencies

```bash
pip install -r config/requirements.txt
```

**Required packages**: numpy, pandas, scipy, scikit-learn, matplotlib, seaborn

### Step 2: Train the Models

```bash
python scripts/train_models.py
```

**What happens:**
- Loads all EMG files from `Data/` folder
- Extracts 140+ features per recording (time & frequency domain)
- Trains 6 One-vs-Rest authentication models
- Saves models to `src/models/`

**Expected output:**
```
Training EMG Authentication Models...
============================================================
Loading EMG data files...
Found 48 files
Processing devansh-fist-1...
...
Training One-vs-Rest Authentication Models
Training model for: devansh
  Best Model: Random Forest
  Test Accuracy: 0.903
...
Models saved successfully!
```

### Step 3: Run Analysis

```bash
python scripts/run_analysis.py
```

This generates comprehensive results and saves them to `Results/` folder.

### Step 4: Visualize Results

```bash
python scripts/visualize.py
```

Creates performance plots and charts.

---

## 📂 Project Structure

```
Minor/
├── src/
│   ├── core/              # Core authentication modules
│   ├── analysis/          # Analysis and evaluation
│   ├── models/            # Trained models (.pkl files)
│   └── utils/             # Utility functions
│
├── scripts/               # Entry point scripts
│   ├── train_models.py
│   ├── run_analysis.py
│   └── visualize.py
│
├── tests/                 # Test scripts
├── Data/                  # EMG signal datasets
├── Results/               # Analysis results and metrics
├── docs/                  # Documentation
└── config/                # Configuration files
```

---

## 🧪 Running Tests

### Basic Authentication Test
```bash
python tests/test_authentication.py
```

### Comprehensive Random Testing
```bash
python tests/comprehensive_random_test.py
```

### Subject-Specific Test
```bash
python tests/test_with_devansh.py
```

---

## 📚 Understanding the System

### How It Works

1. **Feature Extraction**: Extracts statistical and spectral features from EMG signals
   - Time-domain: mean, RMS, variance, zero-crossing rate, etc.
   - Frequency-domain: FFT power spectrum, frequency bands, spectral entropy

2. **One-vs-Rest Classification**: Each person gets their own binary classifier
   - Classifier learns: "This person" vs "All other people"
   - During authentication: Use the classifier for the claimed identity

3. **Authentication**: Compare new EMG signal against trained model
   - Extract features → Normalize → Predict → Confidence score
   - Threshold: 0.5 (adjustable)

### Key Metrics

- **Accuracy**: Overall correct classification rate
- **FAR (False Accept Rate)**: Impostor incorrectly authenticated
- **FRR (False Reject Rate)**: Genuine user incorrectly rejected
- **F1-Score**: Harmonic mean of precision and recall

---

## 🔍 Programmatic Usage

```python
from src.core.emg_authentication import EMGAuthenticationSystem

# Load trained models
auth_system = EMGAuthenticationSystem()
auth_system.load_models('path/to/models.pkl')

# Load new EMG signal
signal = auth_system.load_data_file('path/to/emg_file.txt')

# Authenticate
result = auth_system.authenticate(
    signal_data=signal,
    claimed_identity='devansh',
    threshold=0.5
)

if result['authenticated']:
    print(f"✓ Authenticated with {result['confidence']:.2%} confidence")
else:
    print(f"✗ Authentication failed: {result['reason']}")
```

---

## 📊 Expected Performance

Based on the dataset:
- **Average Accuracy**: 87-93%
- **Best Subject**: Devansh (95.83%)
- **Models**: Random Forest, Gradient Boosting, SVM, MLP

---

## 🛠️ Troubleshooting

**Q: "No data loaded" error**  
A: Verify EMG data files are in `Data/` folder with correct naming format

**Q: "Model file not found"**  
A: Run `python scripts/train_models.py` first to train models

**Q: Low authentication accuracy**  
A: Try adjusting threshold, collecting more data, or ensuring consistent gestures

**Q: Import errors**  
A: Ensure you're running from project root directory

---

## 📖 Further Documentation

- **Technical Details**: See [docs/README.md](README.md)
- **Presentation Guide**: See [docs/PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md)
- **Analysis Reports**: See [docs/analysis/](analysis/)
- **Troubleshooting FAR/FRR**: See [docs/SOLVING_HIGH_FAR_FRR.md](SOLVING_HIGH_FAR_FRR.md)

---

## 💡 Next Steps

1. ✅ Train your models
2. ✅ Run the analysis
3. ✅ Review the results in `Results/` folder
4. ✅ Read the analysis documentation
5. ✅ Prepare your presentation using [PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md)

---

**Need Help?** Check the full documentation in [docs/README.md](README.md)
