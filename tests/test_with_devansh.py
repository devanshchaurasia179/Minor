"""
Train on 5 subjects (Divyesh, Harshit, Kartik, Saif, Vanshish)
Test on 6th subject (Devansh) - completely independent test
This simulates a real-world scenario: train on known users, test on new user
"""

import numpy as np
import pandas as pd
from scipy import signal, stats
from scipy.fft import fft, fftfreq
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
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
        
        features['mean'] = np.mean(signal_data)
        features['std'] = np.std(signal_data)
        features['var'] = np.var(signal_data)
        features['median'] = np.median(signal_data)
        features['max'] = np.max(signal_data)
        features['min'] = np.min(signal_data)
        features['range'] = features['max'] - features['min']
        features['rms'] = np.sqrt(np.mean(signal_data**2))
        features['skewness'] = stats.skew(signal_data)
        features['kurtosis'] = stats.kurtosis(signal_data)
        
        zero_crossings = np.where(np.diff(np.sign(signal_data)))[0]
        features['zero_crossing_rate'] = len(zero_crossings) / len(signal_data)
        
        slopes = np.diff(signal_data)
        slope_changes = np.where(np.diff(np.sign(slopes)))[0]
        features['slope_sign_changes'] = len(slope_changes) / len(signal_data)
        
        features['waveform_length'] = np.sum(np.abs(np.diff(signal_data)))
        features['mav'] = np.mean(np.abs(signal_data))
        features['iemg'] = np.sum(np.abs(signal_data))
        
        threshold = 0.01
        features['willison_amp'] = np.sum(np.abs(np.diff(signal_data)) > threshold)
        
        return features
    
    def extract_frequency_domain_features(self, signal_data):
        """Extract frequency-domain features using FFT"""
        features = {}
        
        fft_vals = fft(signal_data)
        fft_magnitude = np.abs(fft_vals[:len(fft_vals)//2])
        fft_freqs = fftfreq(len(signal_data), 1/self.sampling_rate)[:len(fft_vals)//2]
        
        psd = fft_magnitude ** 2
        
        features['mean_freq'] = np.sum(fft_freqs * psd) / np.sum(psd) if np.sum(psd) > 0 else 0
        
        cumsum_psd = np.cumsum(psd)
        total_power = cumsum_psd[-1]
        if total_power > 0:
            median_idx = np.where(cumsum_psd >= total_power / 2)[0]
            features['median_freq'] = fft_freqs[median_idx[0]] if len(median_idx) > 0 else 0
        else:
            features['median_freq'] = 0
        
        features['peak_freq'] = fft_freqs[np.argmax(psd)] if len(psd) > 0 else 0
        features['total_power'] = np.sum(psd)
        
        low_band = (fft_freqs >= 0) & (fft_freqs < 10)
        mid_band = (fft_freqs >= 10) & (fft_freqs < 25)
        high_band = (fft_freqs >= 25) & (fft_freqs <= 50)
        
        features['power_low'] = np.sum(psd[low_band])
        features['power_mid'] = np.sum(psd[mid_band])
        features['power_high'] = np.sum(psd[high_band])
        
        total = features['power_low'] + features['power_mid'] + features['power_high']
        if total > 0:
            features['ratio_low'] = features['power_low'] / total
            features['ratio_mid'] = features['power_mid'] / total
            features['ratio_high'] = features['power_high'] / total
        else:
            features['ratio_low'] = 0
            features['ratio_mid'] = 0
            features['ratio_high'] = 0
        
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
    # Check for both lowercase and capitalized names
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


def main():
    """
    Main experiment: Train on 5 subjects, test on Devansh
    """
    
    print("="*80)
    print("EMG AUTHENTICATION: TRAIN ON 5 SUBJECTS, TEST ON DEVANSH (6TH SUBJECT)")
    print("="*80)
    
    # Initialize
    feature_extractor = EMGFeatureExtractor(sampling_rate=50)
    
    # Get all files
    all_files = glob.glob('d:/Minor/*.txt')
    
    print(f"\nFound {len(all_files)} total files")
    
    # Separate training (5 subjects) and test (Devansh)
    train_files = []
    test_files = []
    
    for filepath in all_files:
        person, gesture = parse_filename(filepath)
        if person == 'devansh':
            test_files.append(filepath)
        elif person is not None and gesture is not None:
            train_files.append(filepath)
    
    print(f"\nTRAINING FILES: {len(train_files)} (5 subjects)")
    print(f"TEST FILES: {len(test_files)} (Devansh only)")
    
    # Load training data
    print("\n" + "="*80)
    print("LOADING TRAINING DATA (5 SUBJECTS)")
    print("="*80)
    
    train_records = []
    for idx, filepath in enumerate(train_files, 1):
        person, gesture = parse_filename(filepath)
        signal_data = load_data_file(filepath)
        
        if signal_data is None:
            continue
        
        print(f"[{idx}/{len(train_files)}] Processing {person}-{gesture}...", end=' ')
        features = feature_extractor.extract_features(signal_data, window_size=1.0, overlap=0.5)
        
        if len(features) == 0:
            print("FAILED")
            continue
        
        features['person'] = person
        features['gesture'] = gesture
        features['filename'] = os.path.basename(filepath)
        train_records.append(features)
        print("OK")
    
    train_df = pd.DataFrame(train_records)
    
    print(f"\nTraining data loaded:")
    print(f"  Total samples: {len(train_df)}")
    print(f"  People: {sorted(train_df['person'].unique())}")
    print(f"  Samples per person:")
    print(train_df.groupby('person').size().to_string())
    
    # Load test data (Devansh)
    print("\n" + "="*80)
    print("LOADING TEST DATA (DEVANSH)")
    print("="*80)
    
    test_records = []
    for idx, filepath in enumerate(test_files, 1):
        person, gesture = parse_filename(filepath)
        signal_data = load_data_file(filepath)
        
        if signal_data is None:
            continue
        
        print(f"[{idx}/{len(test_files)}] Processing {person}-{gesture}...", end=' ')
        features = feature_extractor.extract_features(signal_data, window_size=1.0, overlap=0.5)
        
        if len(features) == 0:
            print("FAILED")
            continue
        
        features['person'] = person
        features['gesture'] = gesture
        features['filename'] = os.path.basename(filepath)
        test_records.append(features)
        print("OK")
    
    test_df = pd.DataFrame(test_records)
    
    print(f"\nTest data loaded:")
    print(f"  Total samples: {len(test_df)}")
    print(f"  Gestures: {sorted(test_df['gesture'].unique())}")
    print(f"  Files: {test_df['filename'].tolist()}")
    
    # Prepare features
    feature_cols = [col for col in train_df.columns if col not in ['person', 'gesture', 'filename']]
    
    X_train = train_df[feature_cols].values
    y_train_person = train_df['person'].values
    
    X_test = test_df[feature_cols].values
    y_test_true = ['devansh'] * len(test_df)  # All test samples are Devansh
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"\n{'='*80}")
    print(f"FEATURE SUMMARY")
    print(f"{'='*80}")
    print(f"Total features: {len(feature_cols)}")
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    
    # Train models for each of the 5 training subjects
    print(f"\n{'='*80}")
    print(f"TRAINING ONE-VS-REST MODELS FOR 5 SUBJECTS")
    print(f"{'='*80}")
    
    people = sorted(train_df['person'].unique())
    
    classifiers = {
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42),
        'SVM': SVC(kernel='rbf', probability=True, random_state=42),
        'MLP Neural Network': MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
    }
    
    # Store trained models
    trained_models = {}
    
    for person in people:
        print(f"\nTraining models for: {person.upper()}")
        y_binary = (y_train_person == person).astype(int)
        
        trained_models[person] = {}
        
        for model_name, clf in classifiers.items():
            clf_copy = type(clf)(**clf.get_params())
            clf_copy.fit(X_train_scaled, y_binary)
            trained_models[person][model_name] = clf_copy
            print(f"  ✓ {model_name}")
    
    # Test on Devansh
    print(f"\n{'='*80}")
    print(f"TESTING ON DEVANSH (UNKNOWN USER)")
    print(f"{'='*80}")
    
    print("\nExpected Behavior:")
    print("  Since Devansh was NOT in training, all models should REJECT")
    print("  (i.e., confidence scores should be LOW for all 5 subjects)")
    print()
    
    # Test each Devansh sample
    results_summary = []
    
    for test_idx in range(len(test_df)):
        test_sample = X_test_scaled[test_idx:test_idx+1]
        test_info = test_df.iloc[test_idx]
        
        print("="*80)
        print(f"TEST SAMPLE {test_idx+1}/{len(test_df)}: {test_info['filename']}")
        print(f"Gesture: {test_info['gesture']}")
        print("="*80)
        
        for model_name in classifiers.keys():
            print(f"\n{model_name}:")
            print("-" * 60)
            
            # Get predictions from each person's model
            predictions = {}
            for person in people:
                model = trained_models[person][model_name]
                prob = model.predict_proba(test_sample)[0, 1]  # Probability of "this person"
                pred = model.predict(test_sample)[0]
                predictions[person] = {'prob': prob, 'pred': pred}
            
            # Display predictions
            print(f"{'Person':<12} {'Confidence':<12} {'Predicted':<12} {'Authentic?'}")
            print("-" * 60)
            
            threshold = 0.8
            authenticated_by = []
            
            for person in people:
                prob = predictions[person]['prob']
                pred = predictions[person]['pred']
                authentic = "YES" if (pred == 1 and prob >= threshold) else "NO"
                
                if authentic == "YES":
                    authenticated_by.append(person)
                
                status = "✓" if authentic == "YES" else "✗"
                print(f"{person.capitalize():<12} {prob:>6.2%}       {pred:<12} {status} {authentic}")
            
            # Summary for this model
            if len(authenticated_by) == 0:
                result = "✓ CORRECTLY REJECTED (Devansh unknown)"
                status_emoji = "✅"
            else:
                result = f"✗ INCORRECTLY ACCEPTED as {authenticated_by}"
                status_emoji = "❌"
            
            print("-" * 60)
            print(f"Result: {status_emoji} {result}")
            
            # Store summary
            results_summary.append({
                'Test_Sample': test_info['filename'],
                'Gesture': test_info['gesture'],
                'Model': model_name,
                'Authenticated_As': authenticated_by if authenticated_by else ['REJECTED'],
                'Correct': len(authenticated_by) == 0
            })
    
    # Final summary
    print(f"\n{'='*80}")
    print(f"FINAL SUMMARY: DEVANSH TEST RESULTS")
    print(f"{'='*80}\n")
    
    summary_df = pd.DataFrame(results_summary)
    
    # Group by model
    for model_name in classifiers.keys():
        model_results = summary_df[summary_df['Model'] == model_name]
        correct_count = model_results['Correct'].sum()
        total_count = len(model_results)
        
        print(f"{model_name}:")
        print(f"  Correct Rejections: {correct_count}/{total_count} ({100*correct_count/total_count:.1f}%)")
        
        incorrect = model_results[~model_results['Correct']]
        if len(incorrect) > 0:
            print(f"  False Accepts: {len(incorrect)}")
            for _, row in incorrect.iterrows():
                print(f"    - {row['Test_Sample']}: Accepted as {row['Authenticated_As']}")
        else:
            print(f"  ✓ No false accepts!")
        print()
    
    # Overall statistics
    total_tests = len(results_summary)
    correct_rejections = summary_df['Correct'].sum()
    false_accepts = total_tests - correct_rejections
    
    print(f"{'='*80}")
    print(f"OVERALL STATISTICS")
    print(f"{'='*80}")
    print(f"Total Tests: {total_tests} ({len(test_df)} samples × {len(classifiers)} models)")
    print(f"Correct Rejections: {correct_rejections}/{total_tests} ({100*correct_rejections/total_tests:.1f}%)")
    print(f"False Accepts: {false_accepts}/{total_tests} ({100*false_accepts/total_tests:.1f}%)")
    
    if correct_rejections == total_tests:
        print("\n🎉 PERFECT! All models correctly rejected Devansh (unknown user)")
    elif correct_rejections >= total_tests * 0.8:
        print("\n✅ GOOD! Most models correctly rejected Devansh")
    else:
        print("\n⚠️  WARNING: High false accept rate for unknown user")
    
    # Save results
    summary_df.to_csv('d:/Minor/devansh_test_results.csv', index=False)
    print(f"\n{'='*80}")
    print(f"Results saved to: d:/Minor/devansh_test_results.csv")
    print(f"{'='*80}")


if __name__ == '__main__':
    main()
