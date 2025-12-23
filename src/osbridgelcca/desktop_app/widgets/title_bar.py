from pathlib import Path
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget, QLabel


class CustomTitleBar(QWidget):
    """
    Custom title bar widget for a frameless QMainWindow.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent

        # 🔒 Resolve paths RELATIVE TO THIS FILE
        BASE_DIR = Path(__file__).resolve().parent
        RESOURCES = BASE_DIR / "resources"

        self.ICON_MIN = str(RESOURCES / "window_minimize.svg")
        self.ICON_MAX = str(RESOURCES / "window_maximize.svg")
        self.ICON_RESTORE = str(RESOURCES / "window_restore.svg")
        self.ICON_CLOSE = str(RESOURCES / "window_close.svg")

        self.setObjectName("custom_title_bar")
        self.setFixedHeight(30)

        # 🎨 STYLES (UNCHANGED)
        self.setStyleSheet("""
            #custom_title_bar {
                background-color: #45913E;
            }
            #custom_title_bar QLabel {
                background-color: #45913E;
                color: white;
            }
            #custom_title_bar QPushButton {
                background-color: #45913E;
                border: none;
            }
            #custom_title_bar QPushButton:hover {
                background-color: #55a04c;
            }
            #custom_title_bar QPushButton:pressed {
                background-color: #3d7936;
            }
            #custom_title_bar QPushButton#close_button:hover {
                background-color: #E81123;
            }
            #custom_title_bar QPushButton#close_button:pressed {
                background-color: #F1707A;
            }
        """)

        # 📐 Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Left spacer / icon
        icon_label = QLabel()
        icon_label.setFixedSize(30, 30)
        layout.addWidget(icon_label)

        # Title
        title = QLabel("Life Cycle Cost Analysis")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold;")
        layout.addWidget(title, 1)

        self.btn_size = QSize(46, 30)

        def make_button(icon_path, close=False):
            btn = QPushButton()
            btn.setFixedSize(self.btn_size)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(14, 14))
            if close:
                btn.setObjectName("close_button")
            return btn

        # Minimize
        self.min_btn = make_button(self.ICON_MIN)
        self.min_btn.clicked.connect(self.parent_window.showMinimized)
        layout.addWidget(self.min_btn)

        # Maximize / Restore
        self.max_btn = make_button(self.ICON_MAX)
        self.max_btn.clicked.connect(self.toggle_maximize_restore)
        layout.addWidget(self.max_btn)

        # Close
        self.close_btn = make_button(self.ICON_CLOSE, close=True)
        self.close_btn.clicked.connect(self.parent_window.close)
        layout.addWidget(self.close_btn)

        # Drag vars
        self.start_pos = None
        self.start_geometry = None

    # 🔁 Icon switching (SAFE)
    def set_maximize_icon(self):
        self.max_btn.setIcon(QIcon(self.ICON_MAX))

    def set_restore_icon(self):
        self.max_btn.setIcon(QIcon(self.ICON_RESTORE))

    def toggle_maximize_restore(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
            self.set_maximize_icon()
        else:
            self.parent_window.showMaximized()
            self.set_restore_icon()

    # 🖱️ Dragging
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and not self.parent_window.isMaximized():
            self.start_pos = event.globalPosition().toPoint()
            self.start_geometry = self.parent_window.geometry()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and self.start_pos:
            delta = event.globalPosition().toPoint() - self.start_pos
            self.parent_window.move(
                self.start_geometry.x() + delta.x(),
                self.start_geometry.y() + delta.y(),
            )
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.start_pos = None
        self.start_geometry = None
        event.accept()
