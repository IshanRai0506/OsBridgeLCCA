from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QScrollArea, QSizePolicy,
    QLabel, QLineEdit, QPushButton, QHBoxLayout, QGridLayout, QSpacerItem
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QIntValidator
from .utils.data import *
from pathlib import Path


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
        self.setStyleSheet("""
            #central_panel_widget { background-color: #F8F8F8; border-radius: 8px; }
            #central_panel_widget QLabel { color: #333; font-size: 12px; }
            QScrollArea { background-color: transparent; }
            #scroll_content_widget { background-color: #FFF9F9; border: 1px solid #000; }
            QPushButton#nav_button {
                background:#FFF;border:1px solid #ccc;color:#3F3E5E;
                border-radius:8px;padding:6px 15px;min-width:80px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        scroll_content = QWidget()
        scroll_content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        scroll_content.setObjectName("scroll_content_widget")
        self.scroll_area.setWidget(scroll_content)

        self.scroll_layout = QVBoxLayout(scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)

        # ---------- FORM ----------
        self.form_widget = QWidget()
        form = QGridLayout(self.form_widget)
        form.setHorizontalSpacing(10)
        form.setVerticalSpacing(15)
        field_width = 200

        def make_input(default=""):
            w = QLineEdit()
            w.setFixedWidth(field_width)
            w.setAlignment(Qt.AlignLeft)
            w.setStyleSheet("QLineEdit{border:1px solid #DDD; border-radius:8px; padding:3px 10px;}")
            w.setText(default)
            self.widgets.append(w)
            return w

        # Fields
        form.addWidget(QLabel("Discount Rate (Inflation Adjusted)"), 0, 0)
        i1 = make_input("6.70")
        form.addWidget(i1, 0, 1); form.addWidget(QLabel("(%)"), 0, 2)

        form.addWidget(QLabel("Inflation Rate"), 1, 0)
        i2 = make_input("5.15")
        form.addWidget(i2, 1, 1); form.addWidget(QLabel("(%)"), 1, 2)

        form.addWidget(QLabel("Interest Rate"), 2, 0)
        i3 = make_input("7.75")
        form.addWidget(i3, 2, 1); form.addWidget(QLabel("(%)"), 2, 2)

        form.addWidget(QLabel("Investment Ratio"), 3, 0)
        i4 = make_input("0.5000")
        form.addWidget(i4, 3, 1)

        form.addWidget(QLabel("Design Life"), 4, 0)
        i5 = make_input("50")
        i5.setValidator(QIntValidator(i5))
        form.addWidget(i5, 4, 1); form.addWidget(QLabel("(years)"), 4, 2)

        form.addWidget(QLabel("Time for Construction (Base Project)"), 5, 0)
        i6 = make_input("")
        form.addWidget(i6, 5, 1); form.addWidget(QLabel("(years)"), 5, 2)

        form.addWidget(QLabel("Analysis Period"), 6, 0)
        i7 = make_input("50")
        i7.setValidator(QIntValidator(i7))
        form.addWidget(i7, 6, 1); form.addWidget(QLabel("(years)"), 6, 2)

        self.scroll_layout.addWidget(self.form_widget)

        # ---------- NAV BUTTONS ----------
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(5)

        back = QPushButton("Back")
        back.setObjectName("nav_button")
        back.clicked.connect(lambda: self.back.emit(KEY_FINANCIAL))
        btn_layout.addWidget(back)

        next_btn = QPushButton("Next")
        next_btn.setObjectName("nav_button")
        next_btn.clicked.connect(self.collect_data)
        next_btn.clicked.connect(lambda: self.next.emit(KEY_FINANCIAL))
        btn_layout.addWidget(next_btn)

        self.scroll_layout.addLayout(btn_layout)
        self.scroll_layout.addSpacerItem(QSpacerItem(0, 20))

    def collect_data(self):
        """ Read UI values + save + trigger PDF """
        data = {
            KEY_DISCOUNT_RATE_IA: float(self.widgets[0].text() or 0) / 100,
            KEY_INFLATION_RATE: float(self.widgets[1].text() or 0) / 100,
            KEY_INTEREST_RATE: float(self.widgets[2].text() or 0) / 100,
            KEY_INVESTMENT_RATIO: float(self.widgets[3].text() or 0),
            KEY_DESIGN_LIFE: int(self.widgets[4].text() or 0),
            KEY_CONSTR_TIME: float(self.widgets[5].text() or 0),
            KEY_ANALYSIS_PERIOD: int(self.widgets[6].text() or 0),
        }

        print("\nCollected Data:")
        print(data)

        self.database_manager.financial_data = data
        time_cost = self.database_manager.calculate_time_cost()
        print("TIME COST =", time_cost)

        # ------- CALL REPORT -------
        from osbridgelcca.reporting.financial_report_bridge import generate_financial_pdf
        generate_financial_pdf(data, time_cost)

        print("PDF Generated Successfully.")

    def close_widget(self):
        self.closed.emit()
        self.setParent(None)
