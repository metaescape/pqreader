import argparse
import sys
from PyQt6.QtWidgets import QApplication
from reader import get_reader

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PQReader")
    parser.add_argument("--file_path", "-f", type=str, help="Path to the PDF file")
    args = parser.parse_args()
    file_path = args.file_path
    if not file_path:
        file_path = "/data/resource/readings/manual/emacs/elisp.pdf"
    app = QApplication(sys.argv)
    reader = get_reader(file_path)
    reader.show()
    
    sys.exit(app.exec())