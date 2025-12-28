from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QCoreApplication, Qt, QSize, Signal
from PySide6.QtWidgets import (QHBoxLayout, QPushButton, QLineEdit, QComboBox, QGridLayout, QWidget, QLabel, QVBoxLayout, QScrollArea, QSpacerItem, QSizePolicy, QFrame)
from PySide6.QtGui import QIcon, QIntValidator
from .utils.data import *
import sys
import os

class FinancialData(QWidget):
    closed = Signal()
    next = Signal(str)
    back = Signal(str)

    def __init__(self, database, parent=None):
        super().__init__()
        self.parent = parent
        self.database_manager = database
        self.widgets = []

        self.setStyleSheet("""
            #central_panel_widget {
                background-color: #F8F8F8;
                border-radius: 8px;
            }
        """)

        self.setObjectName("central_panel_widget")
        left_panel_vlayout = QVBoxLayout(self)
        left_panel_vlayout.setContentsMargins(0, 0, 0, 0)
        left_panel_vlayout.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        scroll_content_widget = QWidget()
        scroll_content_widget.setObjectName("scroll_content_widget")
        scroll_content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.scroll_area.setWidget(scroll_content_widget)

        self.scroll_content_layout = QVBoxLayout(scroll_content_widget)
        self.scroll_content_layout.setContentsMargins(0,0,0,0)
        self.scroll_content_layout.setSpacing(0)

        # ------------------------- INPUT FORM WIDGETS -------------------------
        grid_layout = QGridLayout()
        field_width = 200

        labels = [
            ("Discount Rate (Inflation Adjusted)", "(%)", "6.70"),
            ("Inflation Rate", "(%)", "5.15"),
            ("Interest Rate", "(%)", "7.75"),
            ("Investment Ratio", "", "0.5000"),
            ("Design Life", "(years)", "50"),
            ("Time for construction of Base Project", "(years)", ""),
            ("Analysis Period", "(years)", "50"),
        ]

        for index, (text, unit, default) in enumerate(labels):
            label = QLabel(text)
            input_f = QLineEdit()
            input_f.setText(default)
            input_f.setFixedWidth(field_width)
            if "years" in unit:
                input_f.setValidator(QIntValidator(input_f))
            self.widgets.append(input_f)

            grid_layout.addWidget(label, index, 0)
            grid_layout.addWidget(input_f, index, 1)
            if unit:
                grid_layout.addWidget(QLabel(unit), index, 2)

        form = QWidget()
        form_layout = QVBoxLayout(form)
        form_layout.addLayout(grid_layout)
        self.scroll_content_layout.addWidget(form)

        # ------------------------- NEXT/BACK BUTTONS -------------------------
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.back.emit(KEY_FINANCIAL))
        btn_layout.addWidget(back_button)

        next_button = QPushButton("Next")
        next_button.clicked.connect(self.collect_data)      # <-- PDF triggered here
        next_button.clicked.connect(lambda: self.next.emit(KEY_FINANCIAL))
        btn_layout.addWidget(next_button)

        self.scroll_content_layout.addLayout(btn_layout)
        left_panel_vlayout.addWidget(self.scroll_area)

    # ------------------------- CLOSE HANDLER -------------------------
    def close_widget(self):
        self.closed.emit()
        self.setParent(None)

    # ------------------------- DATA COLLECTION + PDF REPORT -------------------------
    def collect_data(self):
        from pprint import pprint

        data = {
            KEY_DISCOUNT_RATE_IA: 0.0 if not self.widgets[0].text() else float(self.widgets[0].text())/100,
            KEY_INFLATION_RATE: 0.0 if not self.widgets[1].text() else float(self.widgets[1].text())/100,
            KEY_INTEREST_RATE: 0.0 if not self.widgets[2].text() else float(self.widgets[2].text())/100,
            KEY_INVESTMENT_RATIO: 0.0 if not self.widgets[3].text() else float(self.widgets[3].text()),
            KEY_DESIGN_LIFE: 0 if not self.widgets[4].text() else int(self.widgets[4].text()),
            KEY_CONSTR_TIME: 0.0 if not self.widgets[5].text() else float(self.widgets[5].text()),
            KEY_ANALYSIS_PERIOD: 0 if not self.widgets[6].text() else int(self.widgets[6].text()),
        }

        print("\nCollected Data from Financial UI:")
        pprint(data)

        # save backend data
        self.database_manager.financial_data = data

        # calculate time cost
        time_cost = self.database_manager.calculate_time_cost()
        print("TIME COST =", time_cost)

        # ==== GENERATE PDF ====
        try:
            from osbridgelcca.reporting.financial_report_bridge import generate_financial_pdf
            from pathlib import Path

            root = Path(__file__).resolve().parents[2]
            output_dir = root / "reports" / "output"
            logo_path = root / "desktop_app" / "resources" / "osbridge_logo.png"

            pdf = generate_financial_pdf(
                data_dict=data,
                output_dir=output_dir,
                time_cost=time_cost,
                logo_path=str(logo_path)
            )
            print("PDF SAVED:", pdf)

        except Exception as e:
            print("⚠ PDF Generation FAILED:", e)
