"""
Complete One-vs-Rest Analysis for All 6 Subjects
Shows results for ALL models (RF, GB, SVM, MLP) for each person
"""

import numpy as np
import pandas as pd
from scipy import signal, stats
from scipy.fft import fft, fftfreq
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.neural_network import MLPClassifier
import glob
import os
import warnings
warnings.filterwarnings('ignore')


class EMGFeatureExtractor:
    """Extract discriminative features from EMG signals"""
    
    def __init__(self, sampling_rate=50):
        self.sampling_rate = sampling_rate
    
    def extract_time_domain_features(self, signal_data):
        """Extract time-domain statistical features"""
        features = {}
        
        # Basic statistics
        features['mean'] = np.mean(signal_data)
        features['std'] = np.std(signal_data)
        features['var'] = np.var(signal_data)
        features['median'] = np.median(signal_data)
        features['max'] = np.max(signal_data)
        features['min'] = np.min(signal_data)
        features['range'] = features['max'] - features['min']
        features['rms'] = np.sqrt(np.mean(signal_data**2))
        
        # Higher order statistics
        features['skewness'] = stats.skew(signal_data)
        features['kurtosis'] = stats.kurtosis(signal_data)
        
        # Zero crossing rate
        zero_crossings = np.where(np.diff(np.sign(signal_data)))[0]
        features['zero_crossing_rate'] = len(zero_crossings) / len(signal_data)
        
        # Slope sign changes
        slopes = np.diff(signal_data)
        slope_changes = np.where(np.diff(np.sign(slopes)))[0]
        features['slope_sign_changes'] = len(slope_changes) / len(signal_data)
        
        # Waveform length
        features['waveform_length'] = np.sum(np.abs(np.diff(signal_data)))
        
        # Mean absolute value
        features['mav'] = np.mean(np.abs(signal_data))
        
        # Integrated EMG
        features['iemg'] = np.sum(np.abs(signal_data))
        
        # Willison amplitude
        threshold = 0.01
        features['willison_amp'] = np.sum(np.abs(np.diff(signal_data)) > threshold)
        
        return features
    
    def extract_frequency_domain_features(self, signal_data):
        """Extract frequency-domain features using FFT"""
        features = {}
        
        # Compute FFT
        fft_vals = fft(signal_data)
        fft_magnitude = np.abs(fft_vals[:len(fft_vals)//2])
        fft_freqs = fftfreq(len(signal_data), 1/self.sampling_rate)[:len(fft_vals)//2]
        
        # Power spectral density
        psd = fft_magnitude ** 2
        
        # Mean and median frequency
        features['mean_freq'] = np.sum(fft_freqs * psd) / np.sum(psd) if np.sum(psd) > 0 else 0
        
        cumsum_psd = np.cumsum(psd)
        total_power = cumsum_psd[-1]
        if total_power > 0:
            median_idx = np.where(cumsum_psd >= total_power / 2)[0]
            features['median_freq'] = fft_freqs[median_idx[0]] if len(median_idx) > 0 else 0
        else:
            features['median_freq'] = 0
        
        # Peak frequency
        features['peak_freq'] = fft_freqs[np.argmax(psd)] if len(psd) > 0 else 0
        
        # Total power
        features['total_power'] = np.sum(psd)
        
        # Power in frequency bands
        low_band = (fft_freqs >= 0) & (fft_freqs < 10)
        mid_band = (fft_freqs >= 10) & (fft_freqs < 25)
        high_band = (fft_freqs >= 25) & (fft_freqs <= 50)
        
        features['power_low'] = np.sum(psd[low_band])
        features['power_mid'] = np.sum(psd[mid_band])
        features['power_high'] = np.sum(psd[high_band])
        
        # Band power ratios
        total = features['power_low'] + features['power_mid'] + features['power_high']
        if total > 0:
            features['ratio_low'] = features['power_low'] / total
            features['ratio_mid'] = features['power_mid'] / total
            features['ratio_high'] = features['power_high'] / total
        else:
            features['ratio_low'] = 0
            features['ratio_mid'] = 0
            features['ratio_high'] = 0
        
        # Spectral entropy
        psd_norm = psd / np.sum(psd) if np.sum(psd) > 0 else psd
        psd_norm = psd_norm[psd_norm > 0]
        features['spectral_entropy'] = -np.sum(psd_norm * np.log2(psd_norm)) if len(psd_norm) > 0 else 0
        
        return features
    
    def segment_signal(self, signal_data, window_size=1.0, overlap=0.5):
        """Segment signal into windows"""
        window_samples = int(window_size * self.sampling_rate)
        step_samples = int(window_samples * (1 - overlap))
        
        segments = []
        for start in range(0, len(signal_data) - window_samples + 1, step_samples):
            end = start + window_samples
            segments.append(signal_data[start:end])
        
        return segments
    
    def extract_features(self, signal_data, window_size=1.0, overlap=0.5):
        """Main feature extraction pipeline"""
        segments = self.segment_signal(signal_data, window_size, overlap)
        
        all_features = []
        for segment in segments:
            time_features = self.extract_time_domain_features(segment)
            freq_features = self.extract_frequency_domain_features(segment)
            combined = {**time_features, **freq_features}
            all_features.append(combined)
        
        if len(all_features) == 0:
            return {}
        
        df = pd.DataFrame(all_features)
        
        aggregated = {}
        for col in df.columns:
            aggregated[f'{col}_mean'] = df[col].mean()
            aggregated[f'{col}_std'] = df[col].std()
            aggregated[f'{col}_min'] = df[col].min()
            aggregated[f'{col}_max'] = df[col].max()
        
        return aggregated


def load_data_file(filepath):
    """Load EMG data from a file"""
    try:
        data = pd.read_csv(filepath, sep='\t', header=None)
        return data.iloc[:, 0].values
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def parse_filename(filename):
    """Parse person name and gesture type from filename"""
    basename = os.path.basename(filename).lower()
    
    person = None
    for name in ['devansh', 'divyesh', 'harshit', 'kartik', 'saif', 'vanshish']:
        if name in basename:
            person = name
            break
    
    gesture = None
    if 'fist' in basename:
        gesture = 'fist'
    elif 'snap' in basename:
        gesture = 'snap'
    
    return person, gesture


def load_all_data():
    """Load all EMG data files and extract features"""
    print("="*80)
    print("LOADING EMG DATA FILES")
    print("="*80)
    
    feature_extractor = EMGFeatureExtractor(sampling_rate=50)
    all_files = glob.glob('d:/Minor/*.txt')
    
    print(f"\nFound {len(all_files)} files")
    
    data_records = []
    
    for idx, filepath in enumerate(all_files, 1):
        person, gesture = parse_filename(filepath)
        
        if person is None or gesture is None:
            continue
        
        signal_data = load_data_file(filepath)
        if signal_data is None:
            continue
        
        print(f"[{idx}/{len(all_files)}] Processing {person}-{gesture}...", end=' ')
        
        features = feature_extractor.extract_features(signal_data, window_size=1.0, overlap=0.5)
        
        if len(features) == 0:
            print("FAILED (no features)")
            continue
        
        features['person'] = person
        features['gesture'] = gesture
        features['filename'] = os.path.basename(filepath)
        
        data_records.append(features)
        print("OK")
    
    df = pd.DataFrame(data_records)
    
    print(f"\n{'='*80}")
    print(f"DATA LOADED SUCCESSFULLY")
    print(f"{'='*80}")
    print(f"Total recordings: {len(df)}")
    print(f"People: {sorted(df['person'].unique())}")
    print(f"Number of people: {df['person'].nunique()}")
    print(f"\nGestures per person:")
    print(df.groupby('person')['gesture'].value_counts().to_string())
    
    return df


def train_and_evaluate_all_models():
    """Train and evaluate ALL models for ALL subjects"""
    
    # Load data
    df = load_all_data()
    
    if len(df) == 0:
        print("ERROR: No data loaded!")
        return
    
    # Prepare features
    feature_cols = [col for col in df.columns if col not in ['person', 'gesture', 'filename']]
    X = df[feature_cols].values
    y_person = df['person'].values
    people = sorted(df['person'].unique())
    
    print(f"\n{'='*80}")
    print(f"FEATURE EXTRACTION SUMMARY")
    print(f"{'='*80}")
    print(f"Total features extracted: {len(feature_cols)}")
    print(f"Feature types: Time-domain + Frequency-domain")
    print(f"Window size: 1 second, Overlap: 50%")
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Define all classifiers
    classifiers = {
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42),
        'SVM': SVC(kernel='rbf', probability=True, random_state=42),
        'MLP Neural Network': MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
    }
    
    # Store all results
    all_results = []
    
    print(f"\n{'='*80}")
    print(f"ONE-VS-REST TRAINING FOR ALL 6 SUBJECTS")
    print(f"{'='*80}\n")
    
    # Train for each person
    for person_idx, person in enumerate(people, 1):
        print(f"\n{'='*80}")
        print(f"SUBJECT {person_idx}/6: {person.upper()}")
        print(f"{'='*80}")
        
        # Create binary labels
        y_binary = (y_person == person).astype(int)
        
        # Count samples
        n_positive = np.sum(y_binary == 1)
        n_negative = np.sum(y_binary == 0)
        
        print(f"\nClass distribution:")
        print(f"  This person ({person}): {n_positive} samples")
        print(f"  Other people: {n_negative} samples")
        print(f"  Total: {len(y_binary)} samples")
        print(f"  Class ratio: 1:{n_negative/n_positive:.1f}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y_binary, test_size=0.3, random_state=42, stratify=y_binary
        )
        
        print(f"\nTrain/Test split:")
        print(f"  Training samples: {len(X_train)}")
        print(f"  Test samples: {len(X_test)}")
        
        print(f"\n{'-'*80}")
        print(f"TRAINING ALL 4 MODELS")
        print(f"{'-'*80}\n")
        
        # Train and evaluate each classifier
        for clf_name, clf in classifiers.items():
            print(f"Model: {clf_name}")
            print(f"  Training...", end=' ')
            
            # Train
            clf.fit(X_train, y_train)
            print("Done")
            
            # Cross-validation on training set
            print(f"  Cross-validation...", end=' ')
            cv_scores = cross_val_score(clf, X_train, y_train, cv=3, scoring='accuracy')
            print(f"Done")
            
            # Test set evaluation
            y_pred = clf.predict(X_test)
            y_prob = clf.predict_proba(X_test)[:, 1]
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, zero_division=0)
            recall = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)
            cm = confusion_matrix(y_test, y_pred)
            
            tn, fp, fn, tp = cm.ravel()
            
            # Calculate FAR and FRR
            far = fp / (fp + tn) if (fp + tn) > 0 else 0  # False Accept Rate
            frr = fn / (fn + tp) if (fn + tp) > 0 else 0  # False Reject Rate
            
            # Store results
            result = {
                'Person': person,
                'Model': clf_name,
                'CV_Mean': np.mean(cv_scores),
                'CV_Std': np.std(cv_scores),
                'Test_Accuracy': accuracy,
                'Precision': precision,
                'Recall': recall,
                'F1_Score': f1,
                'TN': tn,
                'FP': fp,
                'FN': fn,
                'TP': tp,
                'FAR': far,
                'FRR': frr
            }
            all_results.append(result)
            
            # Print results
            print(f"  {'─'*76}")
            print(f"  Cross-Validation Accuracy: {np.mean(cv_scores):.4f} (±{np.std(cv_scores):.4f})")
            print(f"  Test Accuracy:             {accuracy:.4f}")
            print(f"  Precision:                 {precision:.4f}")
            print(f"  Recall (Sensitivity):      {recall:.4f}")
            print(f"  F1-Score:                  {f1:.4f}")
            print(f"  False Accept Rate (FAR):   {far:.4f} ({far*100:.2f}%)")
            print(f"  False Reject Rate (FRR):   {frr:.4f} ({frr*100:.2f}%)")
            print(f"  Confusion Matrix:          TN={tn}, FP={fp}, FN={fn}, TP={tp}")
            print()
    
    # Create results DataFrame
    results_df = pd.DataFrame(all_results)
    
    # Print comprehensive summary
    print(f"\n{'='*80}")
    print(f"COMPLETE RESULTS SUMMARY - ALL SUBJECTS & ALL MODELS")
    print(f"{'='*80}\n")
    
    # Overall statistics
    print(f"Overall Statistics Across All Models and Subjects:")
    print(f"  Mean Test Accuracy: {results_df['Test_Accuracy'].mean():.4f} (±{results_df['Test_Accuracy'].std():.4f})")
    print(f"  Best Test Accuracy: {results_df['Test_Accuracy'].max():.4f}")
    print(f"  Worst Test Accuracy: {results_df['Test_Accuracy'].min():.4f}")
    print(f"  Mean F1-Score: {results_df['F1_Score'].mean():.4f}")
    print(f"  Mean FAR: {results_df['FAR'].mean():.4f} ({results_df['FAR'].mean()*100:.2f}%)")
    print(f"  Mean FRR: {results_df['FRR'].mean():.4f} ({results_df['FRR'].mean()*100:.2f}%)")
    
    # Per-subject summary
    print(f"\n{'-'*80}")
    print(f"PER-SUBJECT BEST MODEL")
    print(f"{'-'*80}")
    for person in people:
        person_results = results_df[results_df['Person'] == person]
        best_idx = person_results['Test_Accuracy'].idxmax()
        best = person_results.loc[best_idx]
        print(f"{person.capitalize():12s} → {best['Model']:20s} Acc={best['Test_Accuracy']:.4f}, FAR={best['FAR']:.4f}, FRR={best['FRR']:.4f}")
    
    # Per-model summary
    print(f"\n{'-'*80}")
    print(f"PER-MODEL PERFORMANCE (Averaged Across All 6 Subjects)")
    print(f"{'-'*80}")
    for model_name in classifiers.keys():
        model_results = results_df[results_df['Model'] == model_name]
        print(f"\n{model_name}:")
        print(f"  Mean Accuracy: {model_results['Test_Accuracy'].mean():.4f} (±{model_results['Test_Accuracy'].std():.4f})")
        print(f"  Mean F1-Score: {model_results['F1_Score'].mean():.4f}")
        print(f"  Mean FAR:      {model_results['FAR'].mean():.4f} ({model_results['FAR'].mean()*100:.2f}%)")
        print(f"  Mean FRR:      {model_results['FRR'].mean():.4f} ({model_results['FRR'].mean()*100:.2f}%)")
        print(f"  Best Subject:  {model_results.loc[model_results['Test_Accuracy'].idxmax(), 'Person']}")
        print(f"  Worst Subject: {model_results.loc[model_results['Test_Accuracy'].idxmin(), 'Person']}")
    
    # Detailed table
    print(f"\n{'='*80}")
    print(f"DETAILED RESULTS TABLE")
    print(f"{'='*80}\n")
    print(results_df.to_string(index=False))
    
    # Save to CSV
    results_df.to_csv('d:/Minor/one_vs_rest_complete_results.csv', index=False)
    print(f"\n{'='*80}")
    print(f"Results saved to: d:/Minor/one_vs_rest_complete_results.csv")
    print(f"{'='*80}")


if __name__ == '__main__':
    train_and_evaluate_all_models()
