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

CONTROL = Qt.KeyboardModifier.ControlModifier
class Reader(PdfViewerWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Floating")
        self.resize(800, 1000)
    
    # keyboard shortcuts
    def eventFilter(self, obj, event):
        keypressed = event.type() == event.Type.KeyPress
        key = Qt.Key(event.key()) if keypressed else None
        modifiers = QApplication.keyboardModifiers()
        
        if keypressed and key == Qt.Key.Key_Home:
            self.scroll_to_begin()
        elif keypressed and key == Qt.Key.Key_End:
            self.scroll_to_end()
        elif keypressed and key in [Qt.Key.Key_J, ]:
            self.scroll_up()
        elif keypressed and key in [Qt.Key.Key_K]:
            self.scroll_down()
        elif keypressed and key in [Qt.Key.Key_PageDown, Qt.Key.Key_D, Qt.Key.Key_Down]:
            self.scroll_up_page()
        elif keypressed and key in [Qt.Key.Key_PageUp, Qt.Key.Key_U, Qt.Key.Key_Up]:
            self.scroll_down_page()
        elif keypressed and key == Qt.Key.Key_Minus:
            self.zoom_out()
        elif keypressed and key == Qt.Key.Key_Equal:
            self.zoom_in()
        elif keypressed and key == Qt.Key.Key_0:
            self.zoom_reset()
        elif keypressed and modifiers == CONTROL and key == Qt.Key.Key_C:
            content = self.parse_select_obj_list()
            # Copy to clipboard
            clipboard = QApplication.clipboard()
            clipboard.clear(mode=clipboard.Mode.Clipboard)
            clipboard.setText(content, mode=clipboard.Mode.Clipboard)
            self.cleanup_select()   
        elif keypressed and modifiers == CONTROL and key == Qt.Key.Key_C:
            content = self.parse_select_obj_list()
            # Copy to clipboard
            clipboard = QApplication.clipboard()
            clipboard.clear(mode=clipboard.Mode.Clipboard)
            clipboard.setText(content, mode=clipboard.Mode.Clipboard)
            self.cleanup_select()  
        elif keypressed and modifiers == CONTROL and key == Qt.Key.Key_T:
            self.toggle_last_position()
        elif keypressed and modifiers == CONTROL and key == Qt.Key.Key_Q:
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