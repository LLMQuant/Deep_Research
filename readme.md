# LLMQuant Bilingual PDF Report Generator

A professional tool for generating bilingual (Chinese and English) financial reports in PDF format from markdown content. This application is designed to create professional-looking reports with logos, proper formatting, and page numbering.

## Features

- **Bilingual Output**: Automatically generates reports with both Chinese and English content
- **Professional Financial Report Format**: Includes executive summary, financial highlights, and proper sections
- **Custom Cover Page**: Creates a professional cover page with logo and report information
- **Consistent Headers and Footers**: Adds logo, title, and page numbers to each page
- **Markdown Support**: Converts markdown content to formatted PDF with proper styling
- **Custom Font Support**: Use your preferred font for better typography
- **Confidentiality Notices**: Includes proper disclaimers for financial documents
- **Table of Contents**: Automatically generates a navigable table of contents

## Screenshots

![Sample Report Cover](logo-b.png)

## Requirements

- Python 3.6+
- ReportLab 4.0+
- Markdown
- Jieba (for Chinese text processing)
- BeautifulSoup4 (for HTML parsing)
- Pillow (for image processing)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/LLMQuant/report_generator.git
cd report_generator
```

2. Run the setup script which will create a virtual environment and install all dependencies:
```bash
./run.sh
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

1. Prepare your markdown content in the `input.md` file
2. Make sure the logo files are in the correct location:
   - Cover page logo: `logo-b.png`
   - Header logo: `logo-short.png`
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

## Customization

You can customize the report by:

- Modifying the styles in the `generate_report_simple.py` file
- Changing the font by updating the font path and registration
- Adjusting the page layout parameters in the `generate_pdf` function
- Expanding the translation dictionary for better English translations
- Modifying the executive summary and financial highlights sections

## Font Requirements

The application uses "Huawen Kaiti" (华文楷体) font by default. On macOS, it falls back to "STHeiti Light.ttc" if the Huawen Kaiti font is not available.

For Chinese text, it's recommended to use a font that supports Chinese characters, such as:
- Huawen Kaiti (华文楷体)
- SimSun (宋体)
- SimHei (黑体)
- Microsoft YaHei (微软雅黑)
- NSimSun (新宋体)

## Troubleshooting

If you encounter any issues, you can run the test script to check if all dependencies are properly installed:
```bash
source llmquant_env/bin/activate  # On Windows: llmquant_env\Scripts\activate
python test.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## About LLMQuant

[LLMQuant](https://github.com/LLMQuant) is an open-source community focusing on AI, LLM (large language model) and Quantitative research. We aim to leverage AI for quantitative research with feasible collection of techniques and solutions. 