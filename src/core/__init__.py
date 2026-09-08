"""
Core authentication modules
"""

from .emg_authentication import EMGAuthenticationSystem, EMGFeatureExtractor
from .improved_authentication import ImprovedEMGAuthentication

__all__ = [
    'EMGAuthenticationSystem',
    'EMGFeatureExtractor',
    'ImprovedEMGAuthentication'
]
