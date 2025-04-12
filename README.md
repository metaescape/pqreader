# PQReader

A minimalistic pdf and epub **Reader** depending on **P**yMuPDF and Py**Q**t6.

The core functionality of PQReader is directly based on [eaf-pdf-viewer](https://github.com/emacs-eaf/eaf-pdf-viewer) .

## Installation

```bash
git clone --depth=1 https://github.com/metaescape/pqreader.git
cd pqreader

# submodules pull with depth=1
git submodule update --init --recursive --depth=1
```

### dependencies

You can create a virtual environment before installing the dependencies (Optional but recommended):

``` bash
python -m venv pqreader-venv
. pqreader-venv/bin/activate
python -m pip install --upgrade pip
```

Then install the dependencies using pip:

```bash
pip install PyQt6 PyQt6-Qt6 PyQt6-sip PyMuPDF packaging
```

## Usage

preview the pdf/epub file
```bash
python main.py -f /path/to/file.pdf
python main.py -f /path/to/file.epub
```

## Features and Development
Currently , it provides the core features of a pdf/epub reader:
- smooth scrolling 
- text selection (then C-c to copy)
- cursor hover detection
- link jumping (C-t to toggle the last position)
- PGUP/up/C-u and PGDN/down/C-d to scroll half page
- `=` to zoom in and `-` to zoom out, `0` to reset zoom
- C-q to quit

The full potential of a pdf/epub reader can be unlocked by extending the `Reader` class in `reader.py` with additional 
Qt widgets, such as:

- Add a toolbar for quick access to common actions.
- Integrating a right-click context menu for text highlighting and annotations.
- Implementing a search bar for efficient text search.
- Add a Table of Contents (ToC) sidebar for better document navigation.

all the methods that are needed to implement these features are already provided in 
 `Reader` class (inherited from `PdfViewerWidget` of `eaf-pdf-viewer`).

### test

```bash
# profile fast scroll
python test.py -f /path/to/file.pdf --scroll 

# profile cursor random move, you may need to modify the cursor range depending on your screen size
python test.py -f /path/to/file.pdf --move 
```

checkout `test.py` for more test/profile options



## License
GPL-3.0 (Same as the eaf-pdf-viewer)