"""
Visualization and analysis script for EMG authentication system
Creates plots to understand model performance and feature importance
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.core.emg_authentication import EMGAuthenticationSystem
import pickle

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)


def plot_confusion_matrices():
    """Plot confusion matrices for all person models"""
    
    # Load models
    with open('emg_auth_models.pkl', 'rb') as f:
        model_data = pickle.load(f)
    
    models = model_data['models']
    people = model_data['people']
    
    n_people = len(people)
    n_cols = 3
    n_rows = (n_people + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
    axes = axes.flatten() if n_people > 1 else [axes]
    
    for idx, person in enumerate(people):
        cm = models[person]['confusion_matrix']
        accuracy = models[person]['accuracy']
        model_type = models[person]['model_type']
        
        ax = axes[idx]
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                   xticklabels=['Other', 'This Person'],
                   yticklabels=['Other', 'This Person'])
        ax.set_title(f'{person.capitalize()}\n{model_type}, Acc: {accuracy:.3f}')
        ax.set_ylabel('True Label')
        ax.set_xlabel('Predicted Label')
    
    # Hide extra subplots
    for idx in range(n_people, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.savefig('confusion_matrices.png', dpi=300, bbox_inches='tight')
    print("Saved: confusion_matrices.png")
    plt.show()


def plot_feature_importance():
    """Plot feature importance for Random Forest models"""
    
    # Load models
    with open('emg_auth_models.pkl', 'rb') as f:
        model_data = pickle.load(f)
    
    models = model_data['models']
    feature_names = model_data['feature_names']
    people = model_data['people']
    
    # Collect feature importances from Random Forest models
    rf_models = {person: info for person, info in models.items() 
                 if info['model_type'] == 'RandomForest'}
    
    if not rf_models:
        print("No Random Forest models found")
        return
    
    fig, axes = plt.subplots(len(rf_models), 1, figsize=(12, 6*len(rf_models)))
    if len(rf_models) == 1:
        axes = [axes]
    
    for idx, (person, model_info) in enumerate(rf_models.items()):
        model = model_info['model']
        importances = model.feature_importances_
        
        # Get top 20 features
        indices = np.argsort(importances)[::-1][:20]
        top_features = [feature_names[i] for i in indices]
        top_importances = importances[indices]
        
        ax = axes[idx]
        ax.barh(range(len(top_features)), top_importances, color='steelblue')
        ax.set_yticks(range(len(top_features)))
        ax.set_yticklabels(top_features, fontsize=8)
        ax.set_xlabel('Feature Importance')
        ax.set_title(f'Top 20 Features for {person.capitalize()}')
        ax.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
    print("Saved: feature_importance.png")
    plt.show()


def plot_accuracy_comparison():
    """Plot accuracy comparison across all people"""
    
    # Load models
    with open('emg_auth_models.pkl', 'rb') as f:
        model_data = pickle.load(f)
    
    models = model_data['models']
    people = model_data['people']
    
    # Extract data
    names = []
    accuracies = []
    model_types = []
    
    for person in people:
        names.append(person.capitalize())
        accuracies.append(models[person]['accuracy'])
        model_types.append(models[person]['model_type'])
    
    # Create DataFrame
    df = pd.DataFrame({
        'Person': names,
        'Accuracy': accuracies,
        'Model': model_types
    })
    
    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Accuracy bar chart
    colors = sns.color_palette("husl", len(names))
    bars = ax1.bar(df['Person'], df['Accuracy'], color=colors)
    ax1.set_xlabel('Person')
    ax1.set_ylabel('Accuracy')
    ax1.set_title('Authentication Accuracy by Person')
    ax1.set_ylim([0, 1.0])
    ax1.axhline(y=df['Accuracy'].mean(), color='r', linestyle='--', 
                label=f'Mean: {df["Accuracy"].mean():.3f}')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}',
                ha='center', va='bottom', fontsize=10)
    
    # Model type distribution
    model_counts = df['Model'].value_counts()
    ax2.pie(model_counts.values, labels=model_counts.index, autopct='%1.1f%%',
           startangle=90, colors=sns.color_palette("pastel"))
    ax2.set_title('Best Model Distribution')
    
    plt.tight_layout()
    plt.savefig('accuracy_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved: accuracy_comparison.png")
    plt.show()


def plot_sample_signals():
    """Plot sample EMG signals from different people"""
    
    auth_system = EMGAuthenticationSystem()
    
    # Load a few sample files
    samples = [
        'd:/Minor/Devansh2-Snap-L01.txt',
        'd:/Minor/divyesh-3-snap-L01.txt',
        'd:/Minor/harshit-snap-1-L01.txt',
    ]
    
    fig, axes = plt.subplots(len(samples), 1, figsize=(14, 4*len(samples)))
    if len(samples) == 1:
        axes = [axes]
    
    for idx, filepath in enumerate(samples):
        if not os.path.exists(filepath):
            continue
        
        # Load signal
        signal = auth_system.load_data_file(filepath)
        if signal is None:
            continue
        
        # Parse person name
        person, gesture = auth_system.parse_filename(filepath)
        
        # Plot first 10 seconds (500 samples at 50Hz)
        time = np.arange(min(500, len(signal))) / 50.0  # Time in seconds
        signal_segment = signal[:min(500, len(signal))]
        
        ax = axes[idx]
        ax.plot(time, signal_segment, linewidth=0.5)
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('EMG Amplitude')
        ax.set_title(f'{person.capitalize()} - {gesture.capitalize()} Gesture (First 10 seconds)')
        ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('sample_signals.png', dpi=300, bbox_inches='tight')
    print("Saved: sample_signals.png")
    plt.show()


def plot_feature_distributions():
    """Plot distributions of key features across people"""
    
    auth_system = EMGAuthenticationSystem()
    df = auth_system.load_all_data()
    
    if len(df) == 0:
        print("No data loaded")
        return
    
    # Select a few key features
    key_features = [
        'rms_mean',
        'mav_mean', 
        'zero_crossing_rate_mean',
        'mean_freq_mean',
        'total_power_mean',
        'spectral_entropy_mean'
    ]
    
    # Filter features that exist
    available_features = [f for f in key_features if f in df.columns]
    
    if len(available_features) == 0:
        print("No matching features found")
        return
    
    n_features = len(available_features)
    n_cols = 2
    n_rows = (n_features + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 5*n_rows))
    axes = axes.flatten() if n_features > 1 else [axes]
    
    for idx, feature in enumerate(available_features):
        ax = axes[idx]
        
        # Create violin plot
        sns.violinplot(data=df, x='person', y=feature, ax=ax, palette='Set2')
        ax.set_xlabel('Person')
        ax.set_ylabel(feature.replace('_', ' ').title())
        ax.set_title(f'Distribution of {feature}')
        ax.tick_params(axis='x', rotation=45)
    
    # Hide extra subplots
    for idx in range(n_features, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.savefig('feature_distributions.png', dpi=300, bbox_inches='tight')
    print("Saved: feature_distributions.png")
    plt.show()


def generate_report():
    """Generate a comprehensive analysis report"""
    
    print("\n" + "="*70)
    print("EMG AUTHENTICATION SYSTEM - ANALYSIS REPORT")
    print("="*70)
    
    # Load models
    try:
        with open('emg_auth_models.pkl', 'rb') as f:
            model_data = pickle.load(f)
    except FileNotFoundError:
        print("Error: Model file not found. Please train models first.")
        return
    
    models = model_data['models']
    people = model_data['people']
    feature_names = model_data['feature_names']
    
    print(f"\nNumber of Users: {len(people)}")
    print(f"Users: {', '.join([p.capitalize() for p in people])}")
    print(f"Number of Features: {len(feature_names)}")
    
    print("\n" + "-"*70)
    print("PER-USER PERFORMANCE")
    print("-"*70)
    print(f"{'Person':<15} {'Model Type':<20} {'Accuracy':<10} {'TN':<5} {'FP':<5} {'FN':<5} {'TP':<5}")
    print("-"*70)
    
    accuracies = []
    for person in people:
        info = models[person]
        cm = info['confusion_matrix']
        tn, fp, fn, tp = cm.ravel()
        
        print(f"{person.capitalize():<15} {info['model_type']:<20} {info['accuracy']:<10.3f} "
              f"{tn:<5} {fp:<5} {fn:<5} {tp:<5}")
        accuracies.append(info['accuracy'])
    
    print("-"*70)
    print(f"\nOverall Statistics:")
    print(f"  Mean Accuracy: {np.mean(accuracies):.3f}")
    print(f"  Std Accuracy:  {np.std(accuracies):.3f}")
    print(f"  Min Accuracy:  {np.min(accuracies):.3f}")
    print(f"  Max Accuracy:  {np.max(accuracies):.3f}")
    
    # Model type distribution
    model_types = [info['model_type'] for info in models.values()]
    unique_types = set(model_types)
    
    print(f"\nModel Selection Summary:")
    for model_type in unique_types:
        count = model_types.count(model_type)
        print(f"  {model_type}: {count}/{len(people)} users")
    
    print("\n" + "="*70)


def main():
    """Run all visualizations"""
    
    print("EMG Authentication System - Visualization")
    print("=" * 60)
    
    try:
        # Check if models exist
        if not os.path.exists('emg_auth_models.pkl'):
            print("Error: Models not found. Please run emg_authentication.py first.")
            return
        
        print("\nGenerating visualizations...\n")
        
        # Generate report
        generate_report()
        
        # Create plots
        print("\nCreating plots...")
        plot_accuracy_comparison()
        plot_confusion_matrices()
        plot_feature_importance()
        plot_sample_signals()
        plot_feature_distributions()
        
        print("\n" + "="*60)
        print("All visualizations complete!")
        print("="*60)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
