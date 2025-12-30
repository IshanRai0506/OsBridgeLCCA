from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QSizePolicy, QGridLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QSpacerItem
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

        # ---------- MAIN UI ----------
        self.setObjectName("central_panel_widget")
        left_panel_vlayout = QVBoxLayout(self)
        left_panel_vlayout.setContentsMargins(0, 0, 0, 0)
        left_panel_vlayout.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        scroll_widget.setObjectName("scroll_widget")
        self.scroll_area.setWidget(scroll_widget)

        self.layout = QVBoxLayout(scroll_widget)
        self.layout.setContentsMargins(10, 15, 10, 10)
        self.layout.setSpacing(15)

        grid = QGridLayout()
        grid.setVerticalSpacing(15)
        grid.setHorizontalSpacing(10)
        field_width = 200

        def add_row(text, widget_index, default, unit="", validator=None):
            label = QLabel(text)
            inp = QLineEdit()
            inp.setText(default)
            inp.setFixedWidth(field_width)
            if validator:
                inp.setValidator(QIntValidator(inp))
            self.widgets.append(inp)
            grid.addWidget(label, widget_index, 0)
            grid.addWidget(inp, widget_index, 1)
            if unit:
                grid.addWidget(QLabel(unit), widget_index, 2)

        add_row("Discount Rate (Inflation Adjusted)", 0, "6.70", "(%)")
        add_row("Inflation Rate", 1, "5.15", "(%)")
        add_row("Interest Rate", 2, "7.75", "(%)")
        add_row("Investment Ratio", 3, "0.5000")
        add_row("Design Life", 4, "50", "(years)", validator=True)
        add_row("Time for Construction of Base Project", 5, "", "(days)")
        add_row("Analysis Period", 6, "50", "(years)", validator=True)

        self.layout.addLayout(grid)
        self.layout.addStretch(1)

        # ---- Navigation buttons ----
        btn_row = QHBoxLayout()
        btn_row.addStretch(10)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.back.emit(KEY_FINANCIAL))
        btn_row.addWidget(back_btn)

        next_btn = QPushButton("Next")
        next_btn.clicked.connect(self.collect_data)
        next_btn.clicked.connect(lambda: self.next.emit(KEY_FINANCIAL))
        btn_row.addWidget(next_btn)

        self.layout.addLayout(btn_row)
        left_panel_vlayout.addWidget(self.scroll_area)

    # ---------- Close Widget ----------
    def close_widget(self):
        self.closed.emit()
        self.setParent(None)

    # ---------- Collect + Generate PDF ----------
    def collect_data(self):
        from pprint import pprint
        from osbridgelcca.reporting.financial_report_bridge import generate_financial_pdf

        data = {
            "Discount Rate(Inflation Adjusted)": float(self.widgets[0].text())/100,
            "Inflation Rate": float(self.widgets[1].text())/100,
            "Interest Rate": float(self.widgets[2].text())/100,
            "Investment Ratio": float(self.widgets[3].text()),
            "Design Life": int(self.widgets[4].text()),
            "Time for Construction of Base Project": float(self.widgets[5].text()),
            "Analysis Period": int(self.widgets[6].text()),
        }

        print("\nCollected Data:")
        pprint(data)

        self.database_manager.financial_data = data
        time_cost = self.database_manager.calculate_time_cost()
        print("TIME COST =", time_cost)

        try:
            generate_financial_pdf(data, time_cost)
        except Exception as e:
            print("⚠ PDF ERROR:", e)