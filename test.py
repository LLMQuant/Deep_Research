#!/usr/bin/env python3
"""
Test script for the PDF report generator.
This script checks if all required dependencies are installed and if the font is available.
"""

import sys
import os

def check_module(module_name):
    """Check if a module is installed by trying to import it."""
    try:
        if module_name == "bs4":
            import bs4
        elif module_name == "PIL":
            import PIL
        elif module_name == "reportlab":
            import reportlab
        elif module_name == "markdown":
            import markdown
        elif module_name == "jieba":
            import jieba
        else:
            __import__(module_name)
        print(f"✅ {module_name} is installed")
        return True
    except ImportError:
        print(f"❌ {module_name} is not installed. Please run: pip install {module_name}")
        return False

def check_font(font_paths):
    """Check if any of the font files exist."""
    for font_path in font_paths:
        if os.path.exists(font_path):
            print(f"✅ Font file found at: {font_path}")
            return True
    
    # If we get here, none of the fonts were found
    print("❌ No suitable font files found at the following locations:")
    for font_path in font_paths:
        print(f"   - {font_path}")
    print("Please ensure at least one of these fonts is available or update the font path in generate_report_simple.py.")
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
        check_module("jieba"),
        check_module("bs4"),  # BeautifulSoup4
        check_module("PIL")   # Pillow
    ])
    
    print("\nChecking required files...")
    
    # Check fonts - try project font first, then system font
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_font_path = os.path.join(script_dir, "font", "STKaiti.ttf")
    system_font_path = "/System/Library/Fonts/STHeiti Light.ttc"
    
    font_ok = check_font([project_font_path, system_font_path])
    
    # Check input files
    base_dir = "/Users/haoxue/LLMQuant_report"
    input_md = os.path.join(base_dir, "input.md")
    logo_short = os.path.join(base_dir, "logo-short.png")
    logo_b = os.path.join(base_dir, "logo-b.png")
    
    files_ok = all([
        check_file(input_md, "Input markdown file"),
        check_file(logo_short, "Header logo file"),
        check_file(logo_b, "Cover logo file")
    ])
    
    # Check output directory
    output_dir = os.path.join(base_dir, "output")
    if not os.path.exists(output_dir):
        print(f"❌ Output directory not found at: {output_dir}")
        print("Creating output directory...")
        try:
            os.makedirs(output_dir, exist_ok=True)
            print(f"✅ Output directory created at: {output_dir}")
        except Exception as e:
            print(f"❌ Failed to create output directory: {e}")
            files_ok = False
    else:
        print(f"✅ Output directory found at: {output_dir}")
    
    print("\nSummary:")
    if modules_ok and font_ok and files_ok:
        print("✅ All checks passed! You can run the report generator.")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above before running the generator.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 