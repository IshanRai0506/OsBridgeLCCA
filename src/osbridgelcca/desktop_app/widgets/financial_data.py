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

        # ---------- UI + STYLE (UNCHANGED) ----------
        self.setStyleSheet("""
            #central_panel_widget {
                background-color: #F8F8F8;
                border-radius: 8px;
            }
            #central_panel_widget QLabel {
                color: #333333;
                font-size: 12px;
            }
            #scroll_content_widget {
                background-color: #FFF9F9;
                border: 1px solid #000000;
                padding-bottom: 20px;
            }
            QPushButton#nav_button {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                color: #3F3E5E;
                padding: 6px 15px;
                min-width: 80px;
            }
            QPushButton#nav_button:hover {
                background-color: #F8F8F8;
                border-color: #C0C0C0;
            }
        """)

        self.setObjectName("central_panel_widget")
        left_panel_vlayout = QVBoxLayout(self)
        left_panel_vlayout.setContentsMargins(0, 0, 0, 0)
        left_panel_vlayout.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        scroll_content_widget = QWidget()
        scroll_content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        scroll_content_widget.setObjectName("scroll_content_widget")
        self.scroll_area.setWidget(scroll_content_widget)

        self.scroll_content_layout = QVBoxLayout(scroll_content_widget)
        self.scroll_content_layout.setContentsMargins(0,0,0,0)
        self.scroll_content_layout.setSpacing(0)

        # ----------- FORM FIELDS (UNCHANGED) ----------
        self.general_widget = QWidget()
        self.general_layout = QVBoxLayout(self.general_widget)
        grid_layout = QGridLayout()
        field_width = 200

        def make_input(text="", validator=None):
            edit = QLineEdit()
            if validator: edit.setValidator(validator)
            edit.setText(text)
            edit.setFixedWidth(field_width)
            edit.setStyleSheet("""QLineEdit {border: 1px solid #DDDCE0; border-radius: 10px; padding: 3px 10px;}""")
            self.widgets.append(edit)
            return edit

        # Discount rate
        grid_layout.addWidget(QLabel("Discount Rate (Inflation Adjusted)"), 0, 0)
        grid_layout.addWidget(make_input("6.70"), 0, 1)
        grid_layout.addWidget(QLabel("(%)"), 0, 2)

        # Inflation
        grid_layout.addWidget(QLabel("Inflation Rate"), 1, 0)
        grid_layout.addWidget(make_input("5.15"), 1, 1)
        grid_layout.addWidget(QLabel("(%)"), 1, 2)

        # Interest
        grid_layout.addWidget(QLabel("Interest Rate"), 2, 0)
        grid_layout.addWidget(make_input("7.75"), 2, 1)
        grid_layout.addWidget(QLabel("(%)"), 2, 2)

        # Investment Ratio
        grid_layout.addWidget(QLabel("Investment Ratio"), 3, 0)
        grid_layout.addWidget(make_input("0.5000"), 3, 1)

        # Design Life
        grid_layout.addWidget(QLabel("Design Life"), 4, 0)
        grid_layout.addWidget(make_input("50", QIntValidator()), 4, 1)
        grid_layout.addWidget(QLabel("(years)"), 4, 2)

        # Construction Time
        grid_layout.addWidget(QLabel("Time for construction of Base Project"), 5, 0)
        grid_layout.addWidget(make_input(""), 5, 1)
        grid_layout.addWidget(QLabel("(years)"), 5, 2)

        # Analysis Period
        grid_layout.addWidget(QLabel("Analysis Period"), 6, 0)
        grid_layout.addWidget(make_input("50", QIntValidator()), 6, 1)
        grid_layout.addWidget(QLabel("(years)"), 6, 2)

        self.general_layout.addLayout(grid_layout)
        self.scroll_content_layout.addWidget(self.general_widget)

        # ---------- NAV BUTTONS ----------
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

    # =========================
    # FIXED PDF GENERATION CODE
    # =========================
    def collect_data(self):
        from pprint import pprint
        from pathlib import Path
        from osbridgelcca.reporting.financial_report_bridge import generate_financial_pdf

        data = {
            KEY_DISCOUNT_RATE_IA: 0.0 if not self.widgets[0].text() else float(self.widgets[0].text())/100,
            KEY_INFLATION_RATE: 0.0 if not self.widgets[1].text() else float(self.widgets[1].text())/100,
            KEY_INTEREST_RATE: 0.0 if not self.widgets[2].text() else float(self.widgets[2].text())/100,
            KEY_INVESTMENT_RATIO: 0.0 if not self.widgets[3].text() else float(self.widgets[3].text()),
            KEY_DESIGN_LIFE: 0 if not self.widgets[4].text() else int(self.widgets[4].text()),
            KEY_CONSTR_TIME: 0.0 if not self.widgets[5].text() else float(self.widgets[5].text()),
            KEY_ANALYSIS_PERIOD: 0 if not self.widgets[6].text() else int(self.widgets[6].text()),
        }

        print("\nCollected Data:")
        pprint(data)

        # Save to backend
        self.database_manager.financial_data = data

        # Calculate cost
        time_cost = self.database_manager.calculate_time_cost()
        print("TIME COST =", time_cost)

        # ---- FINANCIAL PDF GENERATION ----
        root = Path(__file__).resolve().parents[2]
        report_folder = root / "reports" / "output"
        report_folder.mkdir(parents=True, exist_ok=True)

        logo_path = root / "desktop_app" / "resources" / "osbridge_logo.png"

         # ⚡ CALL REPORT FUNCTION
         try:
            generated_pdf_path = generate_financial_pdf(data, time_cost, str(logo_path))
            print("PDF Generated:", generated_pdf_path)
        except Exception as e:
            print("⚠ ERROR generating financial PDF:", e)


    def close_widget(self):
        self.closed.emit()
        self.setParent(None)
