"""
Script to generate visualizations
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.analysis.visualize_results import main

if __name__ == '__main__':
    print("Generating Visualizations...")
    print("=" * 60)
    main()
