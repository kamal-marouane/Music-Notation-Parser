# Music Notation Parser

A Python application for parsing musical notation from Excel files, recognizing musical elements using image comparison, and generating audio output.

## 📋 Features

- Parse musical notation from Excel spreadsheets
- Identify musical elements (notes, clefs, alterations, etc.) using image recognition
- Validate the musical notation against a formal grammar
- Generate audio output for parsed music
- Play the generated music using PyGame

## 🔧 Requirements

- Python 3.7+
- Libraries: openpyxl, openpyxl-image-loader, pillow, imagehash, moviepy, pygame
- Excel file with musical notation
- Reference images for musical elements
- Audio clips for each note

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/music_notation_parser.git
   cd music_notation_parser
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env file with your paths
   ```

## ⚙️ Configuration

Edit the `.env` file to set your paths:

```
# Excel file paths
EXCEL_FILE_PATH=C:/path/to/your/music_notation.xlsx
EXCEL_SHEET_NAME=Feuil1

# Image paths
NOTES_DIR=C:/path/to/your/notes_images
REFERENCE_IMAGES_PATH=C:/path/to/your/notes_images/reference
TEMP_IMAGE_PATH=C:/path/to/your/notes_images/temp

# Audio paths
MUSIC_DIR=C:/path/to/your/music_clips
OUTPUT_DIR=C:/path/to/your/output
```

## 📂 Directory Structure

Your directories should be organized as follows:

- `notes_images/` - Contains reference images of musical notation
  - `reference/` - Reference images used for comparison
  - `temp/` - Temporary storage for extracted images
- `music_clips/` - Audio files for each note (MP3 format)
- `output/` - Output directory for generated audio files

## 📝 Excel File Format

The Excel file should follow this format:

1. First row: Partition metadata (Nom: [name]; Instrument: [instrument].)
2. Subsequent rows: Musical notation
   - Text cells: Keywords and identifiers
   - Image cells: Musical notation symbols (clefs, notes, alterations, etc.)

## 🎵 Usage

Run the parser with default settings:

```bash
python -m src.main
```

Or specify custom paths:

```bash
python -m src.main --excel "path/to/excel.xlsx" --sheet "SheetName" --notes-dir "path/to/notes" --music-dir "path/to/music" --output-dir "path/to/output" --play
```

### Command Line Arguments:

- `--excel` - Path to the Excel file
- `--sheet` - Name of the sheet in the Excel file
- `--notes-dir` - Directory containing music notation images
- `--music-dir` - Directory containing note audio files
- `--output-dir` - Directory for output files
- `--play` - Play the generated audio after parsing

## 🧩 Project Structure

```
music_notation_parser/
├── .env                        # Environment variables (local)
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore file
├── README.md                   # Project documentation
├── requirements.txt            # Dependencies
├── setup.py                    # Package installation script
├── src/
│   ├── __init__.py
│   ├── config.py               # Configuration management
│   ├── main.py                 # Entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── token.py            # Token definitions and models
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── excel_parser.py     # Excel file reading utilities
│   │   ├── image_parser.py     # Image recognition utilities
│   │   └── music_parser.py     # Grammar and syntax parser
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_utils.py       # File handling utilities
│   │   └── image_utils.py      # Image processing utilities
│   └── audio/
│       ├── __init__.py
│       └── audio_generator.py  # Audio generation and playback
└── tests/
    ├── __init__.py
    ├── test_excel_parser.py
    ├── test_image_parser.py
    └── test_music_parser.py
```

## 📋 How It Works

1. **Excel Parsing**: Reads cells from an Excel file containing musical notations.
2. **Image Recognition**: Recognizes musical symbols by comparing them with reference images.
3. **Grammar Validation**: Validates the sequence of musical elements against formal grammar rules.
4. **Audio Generation**: Creates audio files for the parsed music notation.
5. **Playback**: Plays the generated audio files using PyGame.

## 🔍 Troubleshooting

- Check that all paths in the `.env` file are correct.
- Ensure reference images match the format in the Excel file.
- Verify that audio files are named correctly according to the token naming convention.
- Check the log file `music_parser.log` for detailed error messages.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
