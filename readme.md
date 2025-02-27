# LLMQuant Bilingual PDF Report Generator

This application generates a bilingual (Chinese and English) PDF report from markdown content. It's designed to create professional-looking reports with logos, proper formatting, and page numbering.

## Features

- Converts markdown content to a formatted PDF
- Bilingual output (Chinese with English translation)
- Custom cover page with logo
- Header with logo and title on each page
- Page numbering
- Support for various markdown elements (headings, paragraphs, lists, quotes)

## Requirements

- Python 3.6+
- ReportLab 4.0+
- Markdown
- Jieba (for Chinese text processing)
- BeautifulSoup4 (for HTML parsing)

## Installation

1. Clone this repository or download the files
2. Run the setup script which will create a virtual environment and install all dependencies:

```bash
./run.sh
```

```bash
./run.sh /Users/haoxue/Library/Fonts/STKaiti.ttf
```

Alternatively, you can manually set up the environment:

```bash
# Create a virtual environment
python3 -m venv llmquant_env

# Activate the virtual environment
source llmquant_env/bin/activate  # On Windows: llmquant_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

1. Ensure your markdown content is in the `input.md` file
2. Make sure the logo files are in the correct location:
   - Cover page logo: `/Users/haoxue/LLMQuant_report/logo-b.png`
   - Header logo: `/Users/haoxue/LLMQuant_report/logo-short.png`
3. Run the script:

```bash
./run.sh
```

Or if you've manually set up the environment:

```bash
source llmquant_env/bin/activate  # On Windows: llmquant_env\Scripts\activate
python generate_report_simple.py
```

4. The generated PDF will be saved as `LLMQuant_Report.pdf` in the same directory

### Using a Custom Font

You can specify a custom font file (TTF or TTC) to use in the report:

```bash
./run.sh /path/to/your/font.ttf
```

Or if you've manually set up the environment:

```bash
source llmquant_env/bin/activate  # On Windows: llmquant_env\Scripts\activate
python generate_report_simple.py /path/to/your/font.ttf
```

If the specified font file is not found, the application will fall back to the default font.

## Troubleshooting

If you encounter any issues, you can run the test script to check if all dependencies are properly installed:

```bash
source llmquant_env/bin/activate  # On Windows: llmquant_env\Scripts\activate
python test.py
```

## Customization

You can customize the report by:

- Modifying the styles in the `generate_report_simple.py` file
- Changing the font by updating the font path and registration
- Adjusting the page layout parameters in the `generate_pdf` function
- Expanding the translation dictionary for better English translations

## Font Requirements

The application uses "Huawen Kaiti" (华文楷体) font by default. On macOS, it falls back to "STHeiti Light.ttc" if the Huawen Kaiti font is not available. 

To use a different font:
1. Download the desired font file (.ttf or .ttc format)
2. Pass the path to the font file as an argument when running the script

For Chinese text, it's recommended to use a font that supports Chinese characters, such as:
- Huawen Kaiti (华文楷体)
- SimSun (宋体)
- SimHei (黑体)
- Microsoft YaHei (微软雅黑)
- NSimSun (新宋体)

## License

This project is open source and available for any use.


