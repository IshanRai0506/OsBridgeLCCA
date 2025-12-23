from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget, QLabel


class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent

        self.setFixedHeight(30)
        self.setObjectName("custom_title_bar")

        self.setStyleSheet("""
            #custom_title_bar {
                background-color: #45913E;
            }
            QLabel {
                color: white;
                font-weight: bold;
            }
            QPushButton {
                background-color: #45913E;
                border: none;
            }
            QPushButton:hover {
                background-color: #55a04c;
            }
            QPushButton#close_button:hover {
                background-color: #E81123;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(0)

        # App title
        self.title_label = QLabel("Life Cycle Cost Analysis")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label, 1)

        btn_size = QSize(40, 30)

        def make_btn(icon_path, close=False):
            btn = QPushButton()
            btn.setFixedSize(btn_size)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(12, 12))
            if close:
                btn.setObjectName("close_button")
            return btn

        self.min_btn = make_btn("resources/window_minimize.svg")
        self.min_btn.clicked.connect(self.parent_window.showMinimized)

        self.max_btn = make_btn("resources/window_maximize.svg")
        self.max_btn.clicked.connect(self.toggle_max_restore)

        self.close_btn = make_btn("resources/window_close.svg", close=True)
        self.close_btn.clicked.connect(self.parent_window.close)

        layout.addWidget(self.min_btn)
        layout.addWidget(self.max_btn)
        layout.addWidget(self.close_btn)

        self._drag_pos = None

    def toggle_max_restore(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
            self.max_btn.setIcon(QIcon("resources/window_maximize.svg"))
        else:
            self.parent_window.showMaximized()
            self.max_btn.setIcon(QIcon("resources/window_restore.svg"))

    # Drag window
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._drag_pos and not self.parent_window.isMaximized():
            delta = event.globalPosition().toPoint() - self._drag_pos
            self.parent_window.move(self.parent_window.pos() + delta)
            self._drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self._drag_pos = None
