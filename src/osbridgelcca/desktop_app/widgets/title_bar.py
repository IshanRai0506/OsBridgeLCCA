from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPixmap, QMouseEvent
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget, QLabel


class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent

        self.setObjectName("custom_title_bar")
        self.setFixedHeight(30)

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
            #custom_title_bar QPushButton#close_button:hover {
                background-color: #E81123;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Left spacer
        icon = QLabel()
        icon.setFixedSize(30, 30)
        layout.addWidget(icon)

        # Title
        title = QLabel("Life Cycle Cost Analysis")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold;")
        layout.addWidget(title, 1)

        self.btn_size = QSize(46, 30)

        def btn(icon_path, close=False):
            b = QPushButton()
            b.setFixedSize(self.btn_size)
            b.setIcon(QIcon(icon_path))
            b.setIconSize(QSize(14, 14))
            if close:
                b.setObjectName("close_button")
            return b

        self.min_btn = btn("resources/window_minimize.svg")
        self.min_btn.clicked.connect(self.parent_window.showMinimized)
        layout.addWidget(self.min_btn)

        self.max_btn = btn("resources/window_maximize.svg")
        self.max_btn.clicked.connect(self.toggle)
        layout.addWidget(self.max_btn)

        self.close_btn = btn("resources/window_close.svg", True)
        self.close_btn.clicked.connect(self.parent_window.close)
        layout.addWidget(self.close_btn)

        self.start_pos = None
        self.start_geo = None

    def toggle(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
            self.max_btn.setIcon(QIcon("resources/window_maximize.svg"))
        else:
            self.parent_window.showMaximized()
            self.max_btn.setIcon(QIcon("resources/window_restore.svg"))

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton and not self.parent_window.isMaximized():
            self.start_pos = e.globalPosition().toPoint()
            self.start_geo = self.parent_window.geometry()

    def mouseMoveEvent(self, e: QMouseEvent):
        if e.buttons() == Qt.LeftButton and self.start_pos:
            d = e.globalPosition().toPoint() - self.start_pos
            self.parent_window.move(
                self.start_geo.x() + d.x(),
                self.start_geo.y() + d.y()
            )

    def mouseReleaseEvent(self, e):
        self.start_pos = None
        self.start_geo = None
