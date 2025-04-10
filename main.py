import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "pdf-viewer"))
)

from eaf_pdf_widget import PdfViewerWidget

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QColor,  QMouseEvent, QCursor
from PyQt6.QtCore import Qt, QTimer, QEvent, QPointF
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
    
def test_select(reader):
    reader.jump_to_page(27, 200)

    # Define the starting and ending coordinates for the selection
    start_pos = QPointF(700, 30)
    end_pos = QPointF(1100, 970)

    reader.setMouseTracking(False)
    QCursor.setPos(start_pos.toPoint())
    
    steps = 30  # Number of steps to move
    current_step = 0
    reader.select_timer = QTimer()
 

    delta_x = (end_pos.x() - start_pos.x()) / steps
    delta_y = (end_pos.y() - start_pos.y()) / steps

    current_pos = start_pos
    def move_mouse():
        nonlocal current_step, current_pos
        if current_step < steps:
            current_pos.setX(int(current_pos.x() + delta_x))
            current_pos.setY(int(current_pos.y() + delta_y))

            # Create and send a mouse move event
            mouse_move_event = QMouseEvent(
                QEvent.Type.MouseMove,
                current_pos,
                Qt.MouseButton.LeftButton,
                Qt.MouseButton.LeftButton,
                Qt.KeyboardModifier.NoModifier,
            )
            QApplication.postEvent(reader, mouse_move_event)
            QCursor.setPos(current_pos.toPoint())
        
            current_step += 1
        else:
            # Send mouse button up event
            reader.setMouseTracking(True)
            reader.select_timer.stop()
    
    reader.select_timer.timeout.connect(move_mouse)
    reader.select_timer.start(10)
    
def profile_select(reader):
    profiler = cProfile.Profile()
    profiler.enable()
    test_select(reader)
    while reader.select_timer.isActive():  # 等待定时器结束
        app.processEvents()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    
    # save first 15 lines to file
    datetime = time.strftime("%Y%m%d_%H-%M-%S", time.localtime())
    with open(f"logs/select-{datetime}.prof", "w") as f:
        stats.stream = f
        stats.print_stats(15)
    
    reader.quit() # raise exception to quit

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EAF PDF Viewer")
    parser.add_argument("--scroll", action="store_true", help="profile scroll")
    parser.add_argument(
        "--select", action="store_true", help="profile select text"
    )
    elisp = "/data/resource/readings/manual/emacs/elisp.pdf"
    parser.add_argument(
        "--file", "-f", type=str, default=elisp, help="file path"
    )
    args = parser.parse_args()
    file_path = args.file
    
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
    elif args.select:
        profile_select(reader)

    
    sys.exit(app.exec())