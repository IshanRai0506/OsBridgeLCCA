from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QMouseEvent
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget, QLabel


class CustomTitleBar(QWidget):
    """
    Custom title bar for a frameless QMainWindow
    Supports dragging, minimize, maximize/restore, close
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent

        self.setObjectName("custom_title_bar")
        self.setFixedHeight(30)

        # ---------------- STYLE ----------------
        self.setStyleSheet("""
            #custom_title_bar {
                background-color: #45913E;
            }
            #custom_title_bar QLabel {
                color: white;
                font-weight: bold;
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

        # ---------------- LAYOUT ----------------
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Left spacer (optional icon area)
        left_spacer = QLabel()
        left_spacer.setFixedWidth(30)
        layout.addWidget(left_spacer)

        # Title
        self.title_label = QLabel("Life Cycle Cost Analysis")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label, 1)

        # Button size
        self.btn_size = QSize(46, 30)

        # ---------------- BUTTON FACTORY ----------------
        def create_button(icon_path, is_close=False):
            btn = QPushButton()
            btn.setFixedSize(self.btn_size)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(14, 14))
            if is_close:
                btn.setObjectName("close_button")
            return btn

        # Minimize
        self.minimize_button = create_button("resources/window_minimize.svg")
        self.minimize_button.clicked.connect(self.parent_window.showMinimized)
        layout.addWidget(self.minimize_button)

        # Maximize / Restore
        self.maximize_button = create_button("resources/window_maximize.svg")
        self.maximize_button.clicked.connect(self.toggle_maximize_restore)
        layout.addWidget(self.maximize_button)

        # Close
        self.close_button = create_button("resources/window_close.svg", is_close=True)
        self.close_button.clicked.connect(self.parent_window.close)
        layout.addWidget(self.close_button)

        # Drag support
        self.start_pos = None
        self.start_geometry = None

    # ---------------- ICON SWITCH ----------------
    def set_maximize_icon(self):
        self.maximize_button.setIcon(QIcon("resources/window_maximize.svg"))

    def set_restore_icon(self):
        self.maximize_button.setIcon(QIcon("resources/window_restore.svg"))

    def toggle_maximize_restore(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
            self.set_maximize_icon()
        else:
            self.parent_window.showMaximized()
            self.set_restore_icon()

    # ---------------- DRAGGING ----------------
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
                self.start_geometry.y() + delta.y()
            )
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.start_pos = None
        self.start_geometry = None
        event.accept()
