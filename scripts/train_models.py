"""
Script to train EMG authentication models
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.emg_authentication import main

if __name__ == '__main__':
    print("Training EMG Authentication Models...")
    print("=" * 60)
    main()
