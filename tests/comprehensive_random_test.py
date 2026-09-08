"""
Comprehensive Random Testing Framework
======================================
1. Load all 24 EMG files (6 people × 2 gestures × 2 trials)
2. Extract random segments from each file
3. Create balanced test dataset (multiple samples per file)
4. Train One-vs-Rest models on 70% data
5. Test on remaining 30% with detailed metrics
6. Analyze per-person, per-gesture, and overall performance
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.fft import fft, fftfreq
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, confusion_matrix, classification_report)
import glob
import os
import random
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
    
    def extract_features_from_segment(self, signal_segment):
        """Extract features from a single segment"""
        time_features = self.extract_time_domain_features(signal_segment)
        freq_features = self.extract_frequency_domain_features(signal_segment)
        return {**time_features, **freq_features}


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


def extract_random_segments(signal_data, num_segments=10, segment_length=100, random_seed=None):
    """
    Extract random segments from EMG signal
    
    Args:
        signal_data: Full EMG signal array
        num_segments: Number of random segments to extract
        segment_length: Length of each segment (in samples, default 100 = 2 seconds at 50Hz)
        random_seed: Random seed for reproducibility
    
    Returns:
        List of random segments
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    max_start = len(signal_data) - segment_length
    if max_start <= 0:
        return [signal_data]
    
    start_positions = np.random.randint(0, max_start, size=num_segments)
    segments = [signal_data[start:start+segment_length] for start in start_positions]
    
    return segments


def create_random_dataset():
    """
    Create a comprehensive random dataset from all EMG files
    """
    
    print("="*80)
    print("COMPREHENSIVE RANDOM TESTING FRAMEWORK")
    print("="*80)
    
    # Initialize
    feature_extractor = EMGFeatureExtractor(sampling_rate=50)
    all_files = glob.glob('d:/Minor/*.txt')
    
    print(f"\nFound {len(all_files)} files")
    
    # Extract random segments from each file
    print("\n" + "="*80)
    print("EXTRACTING RANDOM SEGMENTS FROM ALL FILES")
    print("="*80)
    
    all_samples = []
    file_summary = []
    
    random.seed(42)  # For reproducibility
    
    for idx, filepath in enumerate(all_files, 1):
        person, gesture = parse_filename(filepath)
        
        if person is None or gesture is None:
            continue
        
        print(f"[{idx}/{len(all_files)}] Processing {person}-{gesture}...", end=' ')
        
        # Load full signal
        signal_data = load_data_file(filepath)
        if signal_data is None:
            print("FAILED")
            continue
        
        # Extract 10 random segments of 2 seconds each
        segments = extract_random_segments(signal_data, num_segments=10, 
                                          segment_length=100, random_seed=idx)
        
        print(f"Extracted {len(segments)} segments...", end=' ')
        
        # Extract features from each segment
        for seg_idx, segment in enumerate(segments):
            features = feature_extractor.extract_features_from_segment(segment)
            features['person'] = person
            features['gesture'] = gesture
            features['source_file'] = os.path.basename(filepath)
            features['segment_id'] = seg_idx
            all_samples.append(features)
        
        print("OK")
        
        file_summary.append({
            'file': os.path.basename(filepath),
            'person': person,
            'gesture': gesture,
            'segments_extracted': len(segments)
        })
    
    df = pd.DataFrame(all_samples)
    summary_df = pd.DataFrame(file_summary)
    
    print(f"\n{'='*80}")
    print(f"DATASET CREATION SUMMARY")
    print(f"{'='*80}")
    print(f"Total samples created: {len(df)}")
    print(f"Total files processed: {len(summary_df)}")
    print(f"\nSamples per person:")
    print(df.groupby('person').size().to_string())
    print(f"\nSamples per gesture:")
    print(df.groupby('gesture').size().to_string())
    print(f"\nSamples per person-gesture combination:")
    print(df.groupby(['person', 'gesture']).size().to_string())
    
    return df, summary_df


def train_and_test_models(df, test_size=0.3, random_state=42):
    """
    Train models and evaluate on random test set
    """
    
    # Prepare features
    feature_cols = [col for col in df.columns 
                   if col not in ['person', 'gesture', 'source_file', 'segment_id']]
    
    X = df[feature_cols].values
    y_person = df['person'].values
    y_gesture = df['gesture'].values
    
    people = sorted(df['person'].unique())
    
    print(f"\n{'='*80}")
    print(f"TRAIN/TEST SPLIT (70-30)")
    print(f"{'='*80}")
    
    # Split data
    X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
        X, y_person, np.arange(len(df)), test_size=test_size, 
        random_state=random_state, stratify=y_person
    )
    
    # Get gesture info for test set
    y_test_gesture = df.iloc[idx_test]['gesture'].values
    
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    print(f"\nTrain distribution:")
    train_dist = pd.Series(y_train).value_counts().sort_index()
    print(train_dist.to_string())
    print(f"\nTest distribution:")
    test_dist = pd.Series(y_test).value_counts().sort_index()
    print(test_dist.to_string())
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Define classifiers
    classifiers = {
        'Random Forest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42),
        'SVM': SVC(kernel='rbf', probability=True, random_state=42),
        'MLP Neural Network': MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
    }
    
    # Store all results
    all_results = []
    detailed_predictions = []
    
    print(f"\n{'='*80}")
    print(f"TRAINING & TESTING ONE-VS-REST MODELS")
    print(f"{'='*80}")
    
    # Train for each person
    for person_idx, person in enumerate(people, 1):
        print(f"\n{'='*80}")
        print(f"PERSON {person_idx}/{len(people)}: {person.upper()}")
        print(f"{'='*80}")
        
        # Create binary labels
        y_train_binary = (y_train == person).astype(int)
        y_test_binary = (y_test == person).astype(int)
        
        n_train_pos = np.sum(y_train_binary == 1)
        n_train_neg = np.sum(y_train_binary == 0)
        n_test_pos = np.sum(y_test_binary == 1)
        n_test_neg = np.sum(y_test_binary == 0)
        
        print(f"\nTraining set:")
        print(f"  This person: {n_train_pos} samples")
        print(f"  Others: {n_train_neg} samples")
        print(f"\nTest set:")
        print(f"  This person: {n_test_pos} samples")
        print(f"  Others: {n_test_neg} samples")
        
        print(f"\n{'-'*80}")
        
        for model_name, clf in classifiers.items():
            print(f"\n{model_name}:")
            
            # Train
            clf_copy = type(clf)(**clf.get_params())
            clf_copy.fit(X_train_scaled, y_train_binary)
            
            # Predict
            y_pred = clf_copy.predict(X_test_scaled)
            y_prob = clf_copy.predict_proba(X_test_scaled)[:, 1]
            
            # Calculate metrics
            accuracy = accuracy_score(y_test_binary, y_pred)
            precision = precision_score(y_test_binary, y_pred, zero_division=0)
            recall = recall_score(y_test_binary, y_pred, zero_division=0)
            f1 = f1_score(y_test_binary, y_pred, zero_division=0)
            
            cm = confusion_matrix(y_test_binary, y_pred)
            tn, fp, fn, tp = cm.ravel()
            
            # Calculate FAR and FRR
            far = fp / (fp + tn) if (fp + tn) > 0 else 0
            frr = fn / (fn + tp) if (fn + tp) > 0 else 0
            
            # Authentication at 80% threshold
            y_auth = (y_prob >= 0.8).astype(int)
            auth_tp = np.sum((y_auth == 1) & (y_test_binary == 1))
            auth_fp = np.sum((y_auth == 1) & (y_test_binary == 0))
            auth_fn = np.sum((y_auth == 0) & (y_test_binary == 1))
            auth_tn = np.sum((y_auth == 0) & (y_test_binary == 0))
            
            auth_far = auth_fp / (auth_fp + auth_tn) if (auth_fp + auth_tn) > 0 else 0
            auth_frr = auth_fn / (auth_fn + auth_tp) if (auth_fn + auth_tp) > 0 else 0
            auth_acc = (auth_tp + auth_tn) / len(y_test_binary)
            
            # Store results
            result = {
                'Person': person,
                'Model': model_name,
                'Train_Pos': n_train_pos,
                'Train_Neg': n_train_neg,
                'Test_Pos': n_test_pos,
                'Test_Neg': n_test_neg,
                'Accuracy': accuracy,
                'Precision': precision,
                'Recall': recall,
                'F1_Score': f1,
                'TN': tn,
                'FP': fp,
                'FN': fn,
                'TP': tp,
                'FAR': far,
                'FRR': frr,
                'Auth_Accuracy_80': auth_acc,
                'Auth_FAR_80': auth_far,
                'Auth_FRR_80': auth_frr,
                'Auth_TP': auth_tp,
                'Auth_FP': auth_fp,
                'Auth_FN': auth_fn,
                'Auth_TN': auth_tn
            }
            all_results.append(result)
            
            # Store detailed predictions
            for i in range(len(y_test)):
                detailed_predictions.append({
                    'Person_Model': person,
                    'Model': model_name,
                    'True_Person': y_test[i],
                    'True_Label': y_test_binary[i],
                    'Gesture': y_test_gesture[i],
                    'Predicted': y_pred[i],
                    'Probability': y_prob[i],
                    'Authenticated_80': y_auth[i],
                    'Correct': y_pred[i] == y_test_binary[i]
                })
            
            # Print results
            print(f"  Accuracy:               {accuracy:.4f}")
            print(f"  Precision:              {precision:.4f}")
            print(f"  Recall:                 {recall:.4f}")
            print(f"  F1-Score:               {f1:.4f}")
            print(f"  FAR (Model):            {far:.4f} ({far*100:.2f}%)")
            print(f"  FRR (Model):            {frr:.4f} ({frr*100:.2f}%)")
            print(f"  Auth Accuracy (80%):    {auth_acc:.4f}")
            print(f"  Auth FAR (80%):         {auth_far:.4f} ({auth_far*100:.2f}%)")
            print(f"  Auth FRR (80%):         {auth_frr:.4f} ({auth_frr*100:.2f}%)")
            print(f"  Confusion: TN={tn}, FP={fp}, FN={fn}, TP={tp}")
    
    return pd.DataFrame(all_results), pd.DataFrame(detailed_predictions)


def analyze_results(results_df, predictions_df):
    """
    Comprehensive analysis of results
    """
    
    print(f"\n{'='*80}")
    print(f"COMPREHENSIVE RESULTS ANALYSIS")
    print(f"{'='*80}")
    
    # Overall statistics
    print(f"\n{'-'*80}")
    print(f"OVERALL STATISTICS (All Models & People)")
    print(f"{'-'*80}")
    print(f"Mean Accuracy:          {results_df['Accuracy'].mean():.4f} (±{results_df['Accuracy'].std():.4f})")
    print(f"Mean F1-Score:          {results_df['F1_Score'].mean():.4f}")
    print(f"Mean FAR:               {results_df['FAR'].mean():.4f} ({results_df['FAR'].mean()*100:.2f}%)")
    print(f"Mean FRR:               {results_df['FRR'].mean():.4f} ({results_df['FRR'].mean()*100:.2f}%)")
    print(f"\nWith 80% Authentication Threshold:")
    print(f"Mean Auth Accuracy:     {results_df['Auth_Accuracy_80'].mean():.4f}")
    print(f"Mean Auth FAR:          {results_df['Auth_FAR_80'].mean():.4f} ({results_df['Auth_FAR_80'].mean()*100:.2f}%)")
    print(f"Mean Auth FRR:          {results_df['Auth_FRR_80'].mean():.4f} ({results_df['Auth_FRR_80'].mean()*100:.2f}%)")
    
    # Per-model analysis
    print(f"\n{'-'*80}")
    print(f"PER-MODEL PERFORMANCE")
    print(f"{'-'*80}")
    
    for model in results_df['Model'].unique():
        model_data = results_df[results_df['Model'] == model]
        print(f"\n{model}:")
        print(f"  Mean Accuracy:      {model_data['Accuracy'].mean():.4f} (±{model_data['Accuracy'].std():.4f})")
        print(f"  Mean F1-Score:      {model_data['F1_Score'].mean():.4f}")
        print(f"  Mean FAR:           {model_data['FAR'].mean():.4f} ({model_data['FAR'].mean()*100:.2f}%)")
        print(f"  Mean FRR:           {model_data['FRR'].mean():.4f} ({model_data['FRR'].mean()*100:.2f}%)")
        print(f"  Auth Acc (80%):     {model_data['Auth_Accuracy_80'].mean():.4f}")
        print(f"  Auth FAR (80%):     {model_data['Auth_FAR_80'].mean():.4f} ({model_data['Auth_FAR_80'].mean()*100:.2f}%)")
        print(f"  Auth FRR (80%):     {model_data['Auth_FRR_80'].mean():.4f} ({model_data['Auth_FRR_80'].mean()*100:.2f}%)")
    
    # Per-person analysis
    print(f"\n{'-'*80}")
    print(f"PER-PERSON BEST MODEL")
    print(f"{'-'*80}")
    
    for person in results_df['Person'].unique():
        person_data = results_df[results_df['Person'] == person]
        best_idx = person_data['Accuracy'].idxmax()
        best = person_data.loc[best_idx]
        print(f"\n{person.capitalize()}:")
        print(f"  Best Model:         {best['Model']}")
        print(f"  Accuracy:           {best['Accuracy']:.4f}")
        print(f"  FAR:                {best['FAR']:.4f} ({best['FAR']*100:.2f}%)")
        print(f"  FRR:                {best['FRR']:.4f} ({best['FRR']*100:.2f}%)")
        print(f"  Auth Accuracy:      {best['Auth_Accuracy_80']:.4f}")
        print(f"  Auth FAR:           {best['Auth_FAR_80']:.4f} ({best['Auth_FAR_80']*100:.2f}%)")
        print(f"  Auth FRR:           {best['Auth_FRR_80']:.4f} ({best['Auth_FRR_80']*100:.2f}%)")
    
    # Per-gesture analysis
    print(f"\n{'-'*80}")
    print(f"PER-GESTURE ANALYSIS")
    print(f"{'-'*80}")
    
    for gesture in ['fist', 'snap']:
        gesture_preds = predictions_df[predictions_df['Gesture'] == gesture]
        correct = gesture_preds['Correct'].sum()
        total = len(gesture_preds)
        print(f"\n{gesture.capitalize()} Gesture:")
        print(f"  Correct predictions: {correct}/{total} ({100*correct/total:.2f}%)")
    
    # Model recommendation
    print(f"\n{'='*80}")
    print(f"MODEL RECOMMENDATIONS")
    print(f"{'='*80}")
    
    # Best overall
    mean_scores = results_df.groupby('Model').agg({
        'Accuracy': 'mean',
        'Auth_FAR_80': 'mean',
        'Auth_FRR_80': 'mean'
    })
    
    best_acc_model = mean_scores['Accuracy'].idxmax()
    best_sec_model = mean_scores['Auth_FAR_80'].idxmin()
    best_conv_model = mean_scores['Auth_FRR_80'].idxmin()
    
    print(f"\nBest Accuracy:    {best_acc_model} ({mean_scores.loc[best_acc_model, 'Accuracy']:.4f})")
    print(f"Most Secure:      {best_sec_model} (FAR: {mean_scores.loc[best_sec_model, 'Auth_FAR_80']*100:.2f}%)")
    print(f"Most Convenient:  {best_conv_model} (FRR: {mean_scores.loc[best_conv_model, 'Auth_FRR_80']*100:.2f}%)")


def main():
    """Main execution"""
    
    # Create random dataset
    df, summary_df = create_random_dataset()
    
    # Train and test
    results_df, predictions_df = train_and_test_models(df, test_size=0.3, random_state=42)
    
    # Analyze
    analyze_results(results_df, predictions_df)
    
    # Save results
    print(f"\n{'='*80}")
    print(f"SAVING RESULTS")
    print(f"{'='*80}")
    
    results_df.to_csv('d:/Minor/random_test_results.csv', index=False)
    predictions_df.to_csv('d:/Minor/random_test_predictions.csv', index=False)
    summary_df.to_csv('d:/Minor/random_test_dataset_summary.csv', index=False)
    
    print(f"✓ Results saved to: random_test_results.csv")
    print(f"✓ Predictions saved to: random_test_predictions.csv")
    print(f"✓ Dataset summary saved to: random_test_dataset_summary.csv")
    
    # Detailed results table
    print(f"\n{'='*80}")
    print(f"DETAILED RESULTS TABLE")
    print(f"{'='*80}\n")
    print(results_df.to_string(index=False))


if __name__ == '__main__':
    main()
