#!/usr/bin/env python3
"""
Main entry point for Dubbing Service V2
Imports and runs the console application
"""

import sys
import os

# Add parent directory to path to access original services if needed
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import and run console
from v2.console import main

if __name__ == "__main__":
    main()

