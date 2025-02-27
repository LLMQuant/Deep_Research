#!/usr/bin/env python3
"""
Simple script to check if reportlab is installed and can be imported.
"""

try:
    import reportlab
    print(f"✅ ReportLab is installed (version: {reportlab.__version__})")
    print(f"   Location: {reportlab.__file__}")
except ImportError:
    print("❌ ReportLab is not installed or cannot be imported") 