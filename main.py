#!/usr/bin/env python3
"""
Heat Abnormal - Terminal Animation Engine
Main entry point for the project.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import main

if __name__ == "__main__":
    sys.exit(main()) 