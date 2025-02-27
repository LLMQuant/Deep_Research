#!/usr/bin/env python3
"""
Test script for the PDF report generator.
This script checks if all required dependencies are installed and if the font is available.
"""

import sys
import os
import importlib.util

def check_module(module_name):
    """Check if a module is installed."""
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"❌ {module_name} is not installed. Please run: pip install {module_name}")
        return False
    print(f"✅ {module_name} is installed")
    return True

def check_font(font_path):
    """Check if the font file exists."""
    if os.path.exists(font_path):
        print(f"✅ Font file found at: {font_path}")
        return True
    else:
        print(f"❌ Font file not found at: {font_path}")
        print("Please update the font path in generate_report.py or install the required font.")
        return False

def check_file(file_path, description):
    """Check if a file exists."""
    if os.path.exists(file_path):
        print(f"✅ {description} found at: {file_path}")
        return True
    else:
        print(f"❌ {description} not found at: {file_path}")
        return False

def main():
    """Run all checks."""
    print("Testing PDF Report Generator dependencies...\n")
    
    # Check required modules
    modules_ok = all([
        check_module("reportlab"),
        check_module("markdown"),
        check_module("jieba")
    ])
    
    print("\nChecking required files...")
    
    # Check font
    font_path = "/System/Library/Fonts/STHeiti Light.ttc"
    font_ok = check_font(font_path)
    
    # Check input files
    input_md = "/Users/haoxue/LLMQuant_report/input.md"
    logo_short = "/Users/haoxue/LLMQuant_report/logo-short.png"
    logo_b = "/Users/haoxue/LLMQuant_report/logo-b.png"
    
    files_ok = all([
        check_file(input_md, "Input markdown file"),
        check_file(logo_short, "Header logo file"),
        check_file(logo_b, "Cover logo file")
    ])
    
    print("\nSummary:")
    if modules_ok and font_ok and files_ok:
        print("✅ All checks passed! You can run the report generator.")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above before running the generator.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 