# PQReader

A simple and fast pdf and epub reader depending on PyQt6 and PyMuPDF .

The core functionality of PQReader is directly based on eaf-pdf-viewer .

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
pip install PyQt6 PyQt6-Qt6 PyQt6-sip PyMuPDF
```


## Usage
```bash
python main.py -f /path/to/file.pdf
python main.py -f /path/to/file.epub
```

```bash
python test.py -f /path/to/file.pdf --sroll # profile fast scroll
```

checkout `test.py` for more  test/profile options