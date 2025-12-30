from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QCoreApplication, Qt, QSize, Signal
from PySide6.QtWidgets import (
    QHBoxLayout, QPushButton, QLineEdit, QComboBox, QGridLayout,
    QWidget, QLabel, QVBoxLayout, QScrollArea, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QIcon, QIntValidator
from .utils.data import *
import sys


class FinancialData(QWidget):
    closed = Signal()
    next = Signal(str)
    back = Signal(str)

    def __init__(self, database, parent=None):
        super().__init__()
        self.parent = parent
        self.database_manager = database
        self.widgets = []

        self.setObjectName("central_panel_widget")
        left_panel_vlayout = QVBoxLayout(self)
        left_panel_vlayout.setContentsMargins(0, 0, 0, 0)
        left_panel_vlayout.setSpacing(0)

        # Scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        scroll_content_widget = QWidget()
        scroll_content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        scroll_content_widget.setObjectName("scroll_content_widget")
        self.scroll_area.setWidget(scroll_content_widget)
        self.scroll_content_layout = QVBoxLayout(scroll_content_widget)
        self.scroll_content_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_content_layout.setSpacing(0)

        # Form container
        self.general_widget = QWidget()
        self.general_layout = QVBoxLayout(self.general_widget)
        self.general_layout.setContentsMargins(10, 20, 10, 10)
        self.general_layout.setSpacing(10)

        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(20)

        field_width = 200

        # 1 — Discount Rate
        label = QLabel("Discount Rate (Inflation Adjusted)")
        input1 = QLineEdit()
        self.widgets.append(input1)
        input1.setFixedWidth(field_width)
        input1.setText("6.70")
        grid.addWidget(label, 0, 0)
        grid.addWidget(input1, 0, 1)
        grid.addWidget(QLabel("(%)"), 0, 2)

        # 2 — Inflation
        label = QLabel("Inflation Rate")
        input2 = QLineEdit()
        self.widgets.append(input2)
        input2.setFixedWidth(field_width)
        input2.setText("5.15")
        grid.addWidget(label, 1, 0)
        grid.addWidget(input2, 1, 1)
        grid.addWidget(QLabel("(%)"), 1, 2)

        # 3 — Interest Rate
        label = QLabel("Interest Rate")
        input3 = QLineEdit()
        self.widgets.append(input3)
        input3.setFixedWidth(field_width)
        input3.setText("7.75")
        grid.addWidget(label, 2, 0)
        grid.addWidget(input3, 2, 1)
        grid.addWidget(QLabel("(%)"), 2, 2)

        # 4 — Investment Ratio
        label = QLabel("Investment Ratio")
        input4 = QLineEdit()
        self.widgets.append(input4)
        input4.setFixedWidth(field_width)
        input4.setText("0.5000")
        grid.addWidget(label, 3, 0)
        grid.addWidget(input4, 3, 1)

        # 5 — Design Life
        label = QLabel("Design Life")
        input5 = QLineEdit()
        input5.setValidator(QIntValidator(input5))
        self.widgets.append(input5)
        input5.setFixedWidth(field_width)
        input5.setText("50")
        grid.addWidget(label, 4, 0)
        grid.addWidget(input5, 4, 1)
        grid.addWidget(QLabel("(years)"), 4, 2)

        # 6 — Construction Duration
        label = QLabel("Time for Construction of Base Project")
        input6 = QLineEdit()
        self.widgets.append(input6)
        input6.setFixedWidth(field_width)
        grid.addWidget(label, 5, 0)
        grid.addWidget(input6, 5, 1)
        grid.addWidget(QLabel("(years)"), 5, 2)

        # 7 — Analysis Period
        label = QLabel("Analysis Period")
        input7 = QLineEdit()
        input7.setValidator(QIntValidator(input7))
        self.widgets.append(input7)
        input7.setFixedWidth(field_width)
        input7.setText("50")
        grid.addWidget(label, 6, 0)
        grid.addWidget(input7, 6, 1)
        grid.addWidget(QLabel("(years)"), 6, 2)

        self.general_layout.addLayout(grid)
        self.general_layout.addStretch(1)
        self.scroll_content_layout.addWidget(self.general_widget)

        # Buttons
        self.button_h_layout = QHBoxLayout()
        self.button_h_layout.addStretch(6)

        back_button = QPushButton("Back")
        back_button.setObjectName("nav_button")
        back_button.clicked.connect(lambda: self.back.emit(KEY_FINANCIAL))
        self.button_h_layout.addWidget(back_button)

        next_button = QPushButton("Next")
        next_button.setObjectName("nav_button")
        next_button.clicked.connect(self.collect_data)
        next_button.clicked.connect(lambda: self.next.emit(KEY_FINANCIAL))
        self.button_h_layout.addWidget(next_button)

        self.scroll_content_layout.addLayout(self.button_h_layout)
        left_panel_vlayout.addWidget(self.scroll_area)

    def close_widget(self):
        self.closed.emit()
        self.setParent(None)

    def collect_data(self):
    from pprint import pprint
    data = {
        "Discount Rate(Inflation Adjusted)": float(self.widgets[0].text())/100 if self.widgets[0].text() else 0.0,
        "Inflation Rate": float(self.widgets[1].text())/100 if self.widgets[1].text() else 0.0,
        "Interest Rate": float(self.widgets[2].text())/100 if self.widgets[2].text() else 0.0,
        "Investment Ratio": float(self.widgets[3].text()) if self.widgets[3].text() else 0.0,
        "Design Life": int(self.widgets[4].text()) if self.widgets[4].text() else 0,
        "Time for Construction of Base Project": float(self.widgets[5].text()) if self.widgets[5].text() else 0.0,
        "Analysis Period": int(self.widgets[6].text()) if self.widgets[6].text() else 0,
    }

    print("\nCollected Data:")
    pprint(data)

    self.database_manager.financial_data = data
    time_cost = self.database_manager.calculate_time_cost()
    print("3.Time Cost: ", time_cost)

    from osbridgelcca.reporting.financial_report_bridge import generate_financial_pdf

    pdf_file = generate_financial_pdf(data, time_cost)
    print("PDF saved:", pdf_file)


        