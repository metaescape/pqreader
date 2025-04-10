import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "pdf-viewer"))
)

from eaf_pdf_widget import PdfViewerWidget

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, QTimer, QCoreApplication
from core.utils import get_emacs_vars, SynctexInfo
import argparse
import time
import cProfile
import pstats


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
          
def test_scroll(reader, steps=100):
    import time
    start_time = time.time()
    reader.scroll_steps = steps
    reader.scroll_count = 0
    reader.scroll_timer = QTimer()
    reader.scroll_timer.timeout.connect(lambda: scroll_step(reader, start_time))
    reader.scroll_timer.start(30) 

def scroll_step(reader, start_time):
    if reader.scroll_count < reader.scroll_steps:
        reader.scroll_up()  # 将 scroll_down() 替换为 scroll_up()
        reader.scroll_count += 1
    else:
        reader.scroll_timer.stop()
        end_time = time.time()
        print(f"test_scroll {reader.scroll_steps} up cost: {end_time - start_time}")

def profile_scroll_step(steps=150):
    profiler = cProfile.Profile()
    profiler.enable()
    test_scroll(reader, steps)
    while reader.scroll_timer.isActive():  # 等待定时器结束
        app.processEvents()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    
    # save first 15 lines to file
    datetime = time.strftime("%Y%m%d_%H-%M-%S", time.localtime())
    with open(f"logs/scroll_{steps}-{datetime}.prof", "w") as f:
        stats.stream = f
        stats.print_stats(15)
    
    reader.quit() # raise exception to quit

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EAF PDF Viewer")
    parser.add_argument("--scroll", action="store_true", help="profile scroll")
    # parser.add_argument(
    #     "--file", "-f", type=str, required=True, help="Path to the PDF file"
    # )
    args = parser.parse_args()
    # file_path = args.file
    file_path = "/data/resource/readings/manual/emacs/elisp.pdf"
    app = QApplication(sys.argv)
    (background_color,) = get_emacs_vars(["eaf-buffer-background-color"])
    reader = Reader(
        url=file_path,
        background_color=QColor(background_color),
        buffer=None,
        buffer_id=1,
        synctex_info=SynctexInfo(),
    )

    reader.show()
    if args.scroll:
        profile_scroll_step(steps=1500)

    
    sys.exit(app.exec())