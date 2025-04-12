import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "pdf-viewer"))
)

from eaf_pdf_widget import PdfViewerWidget
from PyQt6.QtWidgets import QApplication
from core.utils import get_emacs_vars, SynctexInfo
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

class Reader(PdfViewerWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Floating")
        self.resize(800, 1000)
    
    # keyboard shortcuts
    def eventFilter(self, obj, event):
        if event.type() == event.Type.KeyPress and event.key() == Qt.Key.Key_Home:
            self.scroll_to_begin()
        elif event.type() == event.Type.KeyPress and event.key() == Qt.Key.Key_End:
            self.scroll_to_end()
        elif event.type() == event.Type.KeyPress and event.key() == Qt.Key.Key_J:
            self.scroll_up()
        elif event.type() == event.Type.KeyPress and event.key() == Qt.Key.Key_K:
            self.scroll_down()
        elif event.type() == event.Type.KeyPress and event.key() in  [Qt.Key.Key_PageDown, Qt.Key.Key_D]:
            self.scroll_up_page()
        elif event.type() == event.Type.KeyPress and event.key() in [Qt.Key.Key_PageUp, Qt.Key.Key_U]:
            self.scroll_down_page()
        elif event.type() == event.Type.KeyPress and event.key()  == Qt.Key.Key_Minus:
            self.zoom_out()
        elif event.type() == event.Type.KeyPress and event.key() == Qt.Key.Key_Equal:
            self.zoom_in()
        elif event.type() == event.Type.KeyPress and event.key() == Qt.Key.Key_0:
            self.zoom_reset()
        elif event.type() == event.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            self.close()

            
        return super().eventFilter(obj, event)
       
  
             
def get_reader(file_path):
    (background_color,) = get_emacs_vars(["eaf-buffer-background-color"])
    reader = Reader(
        url=file_path,
        background_color=QColor(background_color),
        buffer=None,
        buffer_id=1,
        synctex_info=SynctexInfo(),
    ) 
    return reader