"""
EMG-Based Biometric Authentication System
==========================================
Uses EMG signals from fist and snap gestures to authenticate individuals.

Approach: Feature extraction + One-vs-Rest classification
- Extract time-domain, frequency-domain, and statistical features
- Train individual vs others classifier for each person
- Use both gesture types as authentication factors
"""

import numpy as np
import pandas as pd
from scipy import signal, stats
from scipy.fft import fft, fftfreq
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.neural_network import MLPClassifier
import glob
import os
import pickle
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
        
        # Integrated EMG (IEMG)
        features['iemg'] = np.sum(np.abs(signal_data))
        
        # Variance of EMG
        features['var_emg'] = np.var(signal_data)
        
        # Willison amplitude (threshold = 0.01)
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
        
        # Power in specific frequency bands
        # Low: 0-10 Hz, Mid: 10-25 Hz, High: 25-50 Hz
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
        psd_norm = psd_norm[psd_norm > 0]  # Remove zeros
        features['spectral_entropy'] = -np.sum(psd_norm * np.log2(psd_norm)) if len(psd_norm) > 0 else 0
        
        return features
    
    def segment_signal(self, signal_data, window_size=1.0, overlap=0.5):
        """
        Segment signal into windows for feature extraction
        
        Args:
            signal_data: 1D array of EMG signal
            window_size: Window size in seconds
            overlap: Overlap ratio (0-1)
        
        Returns:
            List of signal segments
        """
        window_samples = int(window_size * self.sampling_rate)
        step_samples = int(window_samples * (1 - overlap))
        
        segments = []
        for start in range(0, len(signal_data) - window_samples + 1, step_samples):
            end = start + window_samples
            segments.append(signal_data[start:end])
        
        return segments
    
    def extract_features_from_segments(self, segments):
        """Extract features from all segments and aggregate"""
        all_features = []
        
        for segment in segments:
            # Extract features from this segment
            time_features = self.extract_time_domain_features(segment)
            freq_features = self.extract_frequency_domain_features(segment)
            
            # Combine features
            combined = {**time_features, **freq_features}
            all_features.append(combined)
        
        return all_features
    
    def extract_features(self, signal_data, window_size=1.0, overlap=0.5):
        """
        Main feature extraction pipeline
        
        Returns:
            Dictionary with aggregated features across segments
        """
        # Segment the signal
        segments = self.segment_signal(signal_data, window_size, overlap)
        
        # Extract features from each segment
        segment_features = self.extract_features_from_segments(segments)
        
        if len(segment_features) == 0:
            return {}
        
        # Convert to DataFrame for easy aggregation
        df = pd.DataFrame(segment_features)
        
        # Aggregate features: mean, std, min, max across all segments
        aggregated = {}
        for col in df.columns:
            aggregated[f'{col}_mean'] = df[col].mean()
            aggregated[f'{col}_std'] = df[col].std()
            aggregated[f'{col}_min'] = df[col].min()
            aggregated[f'{col}_max'] = df[col].max()
        
        return aggregated


class EMGAuthenticationSystem:
    """EMG-based biometric authentication system"""
    
    def __init__(self, data_dir='d:/Minor', sampling_rate=50):
        self.data_dir = data_dir
        self.sampling_rate = sampling_rate
        self.feature_extractor = EMGFeatureExtractor(sampling_rate)
        self.scaler = StandardScaler()
        self.models = {}  # One model per person
        self.feature_names = None
        self.people = []
    
    def load_data_file(self, filepath):
        """Load EMG data from a file"""
        try:
            data = pd.read_csv(filepath, sep='\t', header=None)
            # Use first column as the main signal
            return data.iloc[:, 0].values
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            return None
    
    def parse_filename(self, filename):
        """Parse person name and gesture type from filename"""
        basename = os.path.basename(filename).lower()
        
        # Extract person name
        person = None
        for name in ['devansh', 'divyesh', 'harshit', 'kartik', 'saif', 'sritiz', 'vanshish']:
            if name in basename:
                person = name
                break
        
        # Extract gesture type
        gesture = None
        if 'fist' in basename:
            gesture = 'fist'
        elif 'snap' in basename:
            gesture = 'snap'
        
        return person, gesture
    
    def load_all_data(self):
        """Load all EMG data files and extract features"""
        print("Loading EMG data files...")
        
        all_files = glob.glob(os.path.join(self.data_dir, 'Data', '**', '*.txt'), recursive=True)
        print(f"Found {len(all_files)} files")
        
        data_records = []
        
        for filepath in all_files:
            person, gesture = self.parse_filename(filepath)
            
            if person is None or gesture is None:
                print(f"Skipping {filepath}: could not parse filename")
                continue
            
            # Load signal
            signal_data = self.load_data_file(filepath)
            if signal_data is None:
                continue
            
            # Extract features
            print(f"Processing {person}-{gesture}...")
            features = self.feature_extractor.extract_features(signal_data, window_size=1.0, overlap=0.5)
            
            if len(features) == 0:
                print(f"  Warning: No features extracted from {filepath}")
                continue
            
            # Add metadata
            features['person'] = person
            features['gesture'] = gesture
            features['filename'] = os.path.basename(filepath)
            
            data_records.append(features)
        
        # Convert to DataFrame
        df = pd.DataFrame(data_records)
        print(f"\nLoaded {len(df)} recordings from {df['person'].nunique()} people")
        print(f"People: {sorted(df['person'].unique())}")
        print(f"Gestures per person:\n{df.groupby('person')['gesture'].value_counts()}")
        
        return df
    
    def prepare_data(self, df):
        """Prepare features and labels for training"""
        # Separate features from metadata
        feature_cols = [col for col in df.columns if col not in ['person', 'gesture', 'filename']]
        
        X = df[feature_cols].values
        y_person = df['person'].values
        y_gesture = df['gesture'].values
        
        self.feature_names = feature_cols
        self.people = sorted(df['person'].unique())
        
        return X, y_person, y_gesture, feature_cols
    
    def train_one_vs_rest(self, df):
        """
        Train one-vs-rest classifiers for each person
        Each model predicts: "This person" vs "Other people"
        """
        print("\n" + "="*60)
        print("Training One-vs-Rest Authentication Models")
        print("="*60)
        
        X, y_person, y_gesture, feature_cols = self.prepare_data(df)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        results = {}
        
        # Train a model for each person
        for person in self.people:
            print(f"\nTraining model for: {person}")
            
            # Create binary labels: 1 if this person, 0 otherwise
            y_binary = (y_person == person).astype(int)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y_binary, test_size=0.3, random_state=42, stratify=y_binary
            )
            
            # Train multiple classifiers and choose the best
            classifiers = {
                'RandomForest': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
                'GradientBoosting': GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42),
                'SVM': SVC(kernel='rbf', probability=True, random_state=42),
                'MLP': MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
            }
            
            best_score = 0
            best_model = None
            best_name = None
            
            for name, clf in classifiers.items():
                # Cross-validation
                cv_scores = cross_val_score(clf, X_train, y_train, cv=3, scoring='accuracy')
                mean_score = np.mean(cv_scores)
                
                print(f"  {name}: CV Accuracy = {mean_score:.3f} (+/- {np.std(cv_scores):.3f})")
                
                if mean_score > best_score:
                    best_score = mean_score
                    best_model = clf
                    best_name = name
            
            # Train best model on full training set
            print(f"  Selected: {best_name}")
            best_model.fit(X_train, y_train)
            
            # Evaluate
            y_pred = best_model.predict(X_test)
            y_prob = best_model.predict_proba(X_test)[:, 1]
            
            accuracy = accuracy_score(y_test, y_pred)
            
            print(f"  Test Accuracy: {accuracy:.3f}")
            print(f"  Confusion Matrix:")
            cm = confusion_matrix(y_test, y_pred)
            print(f"    {cm}")
            
            # Store model
            self.models[person] = {
                'model': best_model,
                'model_type': best_name,
                'accuracy': accuracy,
                'confusion_matrix': cm
            }
            
            results[person] = {
                'accuracy': accuracy,
                'model_type': best_name
            }
        
        return results
    
    def authenticate(self, signal_data, claimed_identity, threshold=0.8):
        """
        Authenticate a person based on their EMG signal
        
        Args:
            signal_data: EMG signal array
            claimed_identity: Person's claimed identity
            threshold: Probability threshold for authentication (default: 0.8 = 80% confidence)
        
        Returns:
            Dictionary with authentication result
        """
        if claimed_identity not in self.models:
            return {
                'authenticated': False,
                'reason': f'No model trained for {claimed_identity}',
                'confidence': 0.0
            }
        
        # Extract features
        features = self.feature_extractor.extract_features(signal_data, window_size=1.0, overlap=0.5)
        
        # Create feature vector in correct order
        feature_vector = np.array([features.get(col, 0) for col in self.feature_names])
        feature_vector = feature_vector.reshape(1, -1)
        
        # Scale features
        feature_vector_scaled = self.scaler.transform(feature_vector)
        
        # Get model for claimed identity
        model_info = self.models[claimed_identity]
        model = model_info['model']
        
        # Predict
        prediction = model.predict(feature_vector_scaled)[0]
        confidence = model.predict_proba(feature_vector_scaled)[0, 1]
        
        authenticated = (prediction == 1) and (confidence >= threshold)
        
        return {
            'authenticated': authenticated,
            'claimed_identity': claimed_identity,
            'confidence': float(confidence),
            'threshold': threshold,
            'reason': 'Authentication successful' if authenticated else 'Confidence below threshold or prediction failed'
        }
    
    def save_models(self, filepath='emg_auth_models.pkl'):
        """Save trained models to disk"""
        model_data = {
            'models': self.models,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'people': self.people,
            'sampling_rate': self.sampling_rate
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"\nModels saved to {filepath}")
    
    def load_models(self, filepath='emg_auth_models.pkl'):
        """Load trained models from disk"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.models = model_data['models']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.people = model_data['people']
        self.sampling_rate = model_data['sampling_rate']
        
        print(f"Models loaded from {filepath}")
        print(f"Available identities: {self.people}")


def main():
    """Main training and evaluation pipeline"""
    
    print("EMG-Based Biometric Authentication System")
    print("=" * 60)
    
    # Initialize system
    auth_system = EMGAuthenticationSystem(data_dir='d:/Minor', sampling_rate=50)
    
    # Load and process all data
    df = auth_system.load_all_data()
    
    if len(df) == 0:
        print("Error: No data loaded!")
        return
    
    # Train models
    results = auth_system.train_one_vs_rest(df)
    
    # Print summary
    print("\n" + "="*60)
    print("Training Summary")
    print("="*60)
    for person, metrics in results.items():
        print(f"{person:15s}: {metrics['accuracy']:.3f} ({metrics['model_type']})")
    
    # Save models
    auth_system.save_models('emg_auth_models.pkl')
    
    print("\n" + "="*60)
    print("Training Complete!")
    print("="*60)
    print("\nTo authenticate:")
    print("1. Load a new EMG signal")
    print("2. Call auth_system.authenticate(signal, 'person_name')")
    print("3. Check the 'authenticated' field in the result")


if __name__ == '__main__':
    main()
