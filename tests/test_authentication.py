"""
Test script for EMG authentication system
Demonstrates how to use the trained models for authentication
"""

import numpy as np
import pandas as pd
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.emg_authentication import EMGAuthenticationSystem
import glob


def demo_authentication():
    """Demonstrate authentication with test data"""
    
    print("EMG Authentication Demo")
    print("=" * 60)
    
    # Initialize and load trained models
    auth_system = EMGAuthenticationSystem(data_dir='d:/Minor')
    
    try:
        auth_system.load_models('emg_auth_models.pkl')
    except FileNotFoundError:
        print("Error: Model file not found. Please run emg_authentication.py first to train models.")
        return
    
    # Get all data files
    all_files = glob.glob('d:/Minor/*.txt')
    
    # Test authentication on a few samples
    print("\n" + "="*60)
    print("Testing Authentication")
    print("="*60)
    
    test_count = 0
    correct_auth = 0
    false_accept = 0
    false_reject = 0
    
    for filepath in all_files[:10]:  # Test first 10 files
        # Parse ground truth
        basename = os.path.basename(filepath).lower()
        true_identity = None
        for name in ['devansh', 'divyesh', 'harshit', 'kartik', 'saif', 'vanshish']:
            if name in basename:
                true_identity = name
                break
        
        if true_identity is None:
            continue
        
        # Load signal
        signal_data = auth_system.load_data_file(filepath)
        if signal_data is None:
            continue
        
        print(f"\nFile: {os.path.basename(filepath)}")
        print(f"True Identity: {true_identity}")
        
        # Test 1: Authenticate with correct identity
        result = auth_system.authenticate(signal_data, true_identity, threshold=0.8)
        test_count += 1
        
        print(f"Authentication Result: {result['authenticated']}")
        print(f"Confidence: {result['confidence']:.3f}")
        
        if result['authenticated']:
            correct_auth += 1
        else:
            false_reject += 1
        
        # Test 2: Try with wrong identity (first different person)
        other_people = [p for p in auth_system.people if p != true_identity]
        if other_people:
            imposter = other_people[0]
            result_imposter = auth_system.authenticate(signal_data, imposter, threshold=0.8)
            
            print(f"Imposter Test ({imposter}): {result_imposter['authenticated']}")
            print(f"Imposter Confidence: {result_imposter['confidence']:.3f}")
            
            if result_imposter['authenticated']:
                false_accept += 1
    
    # Print statistics
    print("\n" + "="*60)
    print("Authentication Statistics")
    print("="*60)
    print(f"Total Tests: {test_count}")
    print(f"Correct Authentications: {correct_auth}/{test_count} ({100*correct_auth/test_count:.1f}%)")
    print(f"False Rejections: {false_reject}")
    print(f"False Accepts: {false_accept}")


def interactive_authentication():
    """Interactive authentication demo"""
    
    print("\nInteractive Authentication Demo")
    print("=" * 60)
    
    # Initialize and load trained models
    auth_system = EMGAuthenticationSystem(data_dir='d:/Minor')
    
    try:
        auth_system.load_models('emg_auth_models.pkl')
    except FileNotFoundError:
        print("Error: Model file not found. Please run emg_authentication.py first to train models.")
        return
    
    print(f"\nAvailable identities: {', '.join(auth_system.people)}")
    print("\nTo authenticate:")
    print("1. Enter person name")
    print("2. Enter path to EMG data file")
    print("3. System will verify if the signal matches the claimed identity")
    
    while True:
        print("\n" + "-"*60)
        claimed_identity = input("Enter person name (or 'quit' to exit): ").strip().lower()
        
        if claimed_identity == 'quit':
            break
        
        if claimed_identity not in auth_system.people:
            print(f"Error: '{claimed_identity}' not in trained identities")
            continue
        
        filepath = input("Enter path to EMG file: ").strip()
        
        if not os.path.exists(filepath):
            print(f"Error: File not found: {filepath}")
            continue
        
        # Load signal
        signal_data = auth_system.load_data_file(filepath)
        if signal_data is None:
            print("Error: Could not load signal data")
            continue
        
        # Authenticate
        result = auth_system.authenticate(signal_data, claimed_identity, threshold=0.8)
        
        print("\n" + "="*60)
        print("AUTHENTICATION RESULT")
        print("="*60)
        print(f"Claimed Identity: {result['claimed_identity']}")
        print(f"Authenticated: {'✓ YES' if result['authenticated'] else '✗ NO'}")
        print(f"Confidence: {result['confidence']:.3f}")
        print(f"Threshold: {result['threshold']}")
        print(f"Reason: {result['reason']}")
        print("="*60)


def cross_validation_analysis():
    """Perform detailed cross-validation analysis"""
    
    print("\nCross-Validation Analysis")
    print("=" * 60)
    
    # Initialize system
    auth_system = EMGAuthenticationSystem(data_dir='d:/Minor')
    
    # Load data
    df = auth_system.load_all_data()
    
    if len(df) == 0:
        print("Error: No data loaded!")
        return
    
    X, y_person, y_gesture, feature_cols = auth_system.prepare_data(df)
    X_scaled = auth_system.scaler.fit_transform(X)
    
    print("\n" + "="*60)
    print("Per-Person Authentication Performance")
    print("="*60)
    
    from sklearn.model_selection import cross_val_score
    from sklearn.ensemble import RandomForestClassifier
    
    for person in auth_system.people:
        y_binary = (y_person == person).astype(int)
        
        # Count samples
        n_positive = np.sum(y_binary == 1)
        n_negative = np.sum(y_binary == 0)
        
        print(f"\n{person}:")
        print(f"  Positive samples (this person): {n_positive}")
        print(f"  Negative samples (others): {n_negative}")
        
        if n_positive < 2:
            print(f"  Skipping (insufficient data)")
            continue
        
        # Cross-validation
        clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
        cv_scores = cross_val_score(clf, X_scaled, y_binary, cv=min(3, n_positive), scoring='accuracy')
        
        print(f"  CV Accuracy: {np.mean(cv_scores):.3f} (+/- {np.std(cv_scores):.3f})")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'interactive':
            interactive_authentication()
        elif sys.argv[1] == 'cv':
            cross_validation_analysis()
        else:
            print("Usage:")
            print("  python test_authentication.py          - Run demo authentication")
            print("  python test_authentication.py interactive - Interactive authentication")
            print("  python test_authentication.py cv       - Cross-validation analysis")
    else:
        demo_authentication()
