from pathlib import Path
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget, QLabel


class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent

        # ✅ Absolute resource path (THIS IS THE KEY FIX)
        BASE_DIR = Path(__file__).resolve().parent
        RES = BASE_DIR / "resources"

        self.ICON_MIN = str(RES / "window_minimize.svg")
        self.ICON_MAX = str(RES / "window_maximize.svg")
        self.ICON_RESTORE = str(RES / "window_restore.svg")
        self.ICON_CLOSE = str(RES / "window_close.svg")

        self.setObjectName("custom_title_bar")
        self.setFixedHeight(30)

        # Styles (unchanged)
        self.setStyleSheet("""
            #custom_title_bar { background-color: #45913E; }
            #custom_title_bar QLabel { color: white; }
            #custom_title_bar QPushButton {
                background-color: #45913E;
                border: none;
            }
            #custom_title_bar QPushButton:hover { background-color: #55a04c; }
            #custom_title_bar QPushButton#close_button:hover { background-color: #E81123; }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Left spacer
        spacer = QLabel()
        spacer.setFixedSize(30, 30)
        layout.addWidget(spacer)

        # Title
        title = QLabel("Life Cycle Cost Analysis")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold;")
        layout.addWidget(title, 1)

        self.btn_size = QSize(46, 30)

        def make_button(icon, close=False):
            b = QPushButton()
            b.setFixedSize(self.btn_size)
            b.setIcon(QIcon(icon))
            b.setIconSize(QSize(14, 14))
            if close:
                b.setObjectName("close_button")
            return b

        self.min_btn = make_button(self.ICON_MIN)
        self.min_btn.clicked.connect(self.parent_window.showMinimized)
        layout.addWidget(self.min_btn)

        self.max_btn = make_button(self.ICON_MAX)
        self.max_btn.clicked.connect(self.toggle_maximize_restore)
        layout.addWidget(self.max_btn)

        self.close_btn = make_button(self.ICON_CLOSE, close=True)
        self.close_btn.clicked.connect(self.parent_window.close)
        layout.addWidget(self.close_btn)

        self.start_pos = None
        self.start_geom = None

    def toggle_maximize_restore(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
            self.max_btn.setIcon(QIcon(self.ICON_MAX))
        else:
            self.parent_window.showMaximized()
            self.max_btn.setIcon(QIcon(self.ICON_RESTORE))

    # Drag
    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton and not self.parent_window.isMaximized():
            self.start_pos = e.globalPosition().toPoint()
            self.start_geom = self.parent_window.geometry()

    def mouseMoveEvent(self, e: QMouseEvent):
        if self.start_pos and e.buttons() == Qt.LeftButton:
            delta = e.globalPosition().toPoint() - self.start_pos
            self.parent_window.move(
                self.start_geom.x() + delta.x(),
                self.start_geom.y() + delta.y()
            )

    def mouseReleaseEvent(self, e: QMouseEvent):
        self.start_pos = None
        self.start_geom = None
