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
        is_key_pressed = event.type() == event.Type.KeyPress
        key = Qt.Key(event.key()) if is_key_pressed else None
        modifiers = QApplication.keyboardModifiers()
        
        if is_key_pressed and key == Qt.Key.Key_Home:
            self.scroll_to_begin()
        elif is_key_pressed and key == Qt.Key.Key_End:
            self.scroll_to_end()
        elif is_key_pressed and key in [Qt.Key.Key_J, ]:
            self.scroll_up()
        elif is_key_pressed and key in [Qt.Key.Key_K]:
            self.scroll_down()
        elif is_key_pressed and key in [Qt.Key.Key_PageDown, Qt.Key.Key_D, Qt.Key.Key_Down]:
            self.scroll_up_page()
        elif is_key_pressed and key in [Qt.Key.Key_PageUp, Qt.Key.Key_U, Qt.Key.Key_Up]:
            self.scroll_down_page()
        elif is_key_pressed and key == Qt.Key.Key_Minus:
            self.zoom_out()
        elif is_key_pressed and key == Qt.Key.Key_Equal:
            self.zoom_in()
        elif is_key_pressed and key == Qt.Key.Key_0:
            self.zoom_reset()
        elif is_key_pressed and modifiers == CONTROL and key == Qt.Key.Key_C:
            content = self.parse_select_obj_list()
            # Copy to clipboard
            clipboard = QApplication.clipboard()
            clipboard.clear(mode=clipboard.Mode.Clipboard)
            clipboard.setText(content, mode=clipboard.Mode.Clipboard)  
        elif is_key_pressed and modifiers == CONTROL and key == Qt.Key.Key_T:
            self.toggle_last_position()
        elif is_key_pressed and modifiers == CONTROL and key == Qt.Key.Key_Q:
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