"""
Script to run complete analysis
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.analysis.run_complete_analysis import train_and_evaluate_all_models

if __name__ == '__main__':
    print("Running Complete Analysis...")
    print("=" * 60)
    train_and_evaluate_all_models()
