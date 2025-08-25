"""
Dashboard Monokai - Giao diện bảng dashboard theo theme Monokai cổ điển
Thiết kế theo phong cách terminal/console với màu sắc Monokai đặc trưng
-- REFACTORED FOR MODEL/VIEW ARCHITECTURE --
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableView, 
    QHeaderView, QFrame, QPushButton, QLineEdit, QComboBox, QSplitter,
    QGroupBox, QGridLayout, QProgressBar, QTextEdit, QAbstractItemView
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QItemSelectionModel
from PyQt6.QtGui import QFont

# Core components
from core import get_state_manager
from widgets import InstancesModel, InstancesProxy, StatusPillDelegate

class MonokaiDashboard(QWidget):
    """Dashboard với theme Monokai, được tái cấu trúc để sử dụng Model/View."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MonokaiDashboard")
        
        # Managers
        self.state_manager = get_state_manager()

        # Models and Delegates
        self.instances_model = InstancesModel(self)
        self.instances_proxy = InstancesProxy(self)
        self.instances_proxy.setSourceModel(self.instances_model)
        self.status_delegate = StatusPillDelegate(self)

        self.setup_ui()
        self.apply_monokai_style()
        self.connect_signals()

        print("✅ MonokaiDashboard (Refactored) initialized successfully")

    def setup_ui(self):
        """Setup giao diện dashboard"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Main content area
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Table và controls
        left_panel = self.create_left_panel()
        main_splitter.addWidget(left_panel)
        
        # Right panel - Stats và monitoring
        right_panel = self.create_right_panel()
        main_splitter.addWidget(right_panel)
        
        main_splitter.setStretchFactor(0, 7)
        main_splitter.setStretchFactor(1, 3)
        
        layout.addWidget(main_splitter)

    def create_left_panel(self) -> QWidget:
        """Tạo panel bên trái với bảng instances"""
        left_widget = QWidget()
        layout = QVBoxLayout(left_widget)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(5)
        
        # Control bar
        controls = self.create_controls()
        layout.addWidget(controls)
        
        # Instance table
        self.create_instance_table()
        layout.addWidget(self.instance_table)
        
        return left_widget

    def create_controls(self) -> QWidget:
        """Tạo thanh điều khiển"""
        controls_widget = QFrame()
        controls_widget.setObjectName("ControlsFrame")
        controls_widget.setFixedHeight(50)
        
        layout = QHBoxLayout(controls_widget)
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Tìm theo tên hoặc index...")
        self.search_edit.setObjectName("SearchInput")
        layout.addWidget(self.search_edit)
        
        self.filter_combo = QComboBox()
        self.filter_combo.setObjectName("StatusFilter")
        self.filter_combo.addItems(["Tất cả", "Đang chạy", "Đã tắt"])
        layout.addWidget(self.filter_combo)
        
        layout.addStretch()
        
        self.btn_select_all = QPushButton("✅ Chọn tất cả")
        self.btn_select_all.setObjectName("ActionButton")
        layout.addWidget(self.btn_select_all)
        
        self.btn_deselect_all = QPushButton("❌ Bỏ chọn")
        self.btn_deselect_all.setObjectName("ActionButton")
        layout.addWidget(self.btn_deselect_all)

        return controls_widget

    def create_instance_table(self):
        """Tạo bảng hiển thị instances sử dụng QTableView và Model/View."""
        self.instance_table = QTableView()
        self.instance_table.setObjectName("InstanceTableView")
        self.instance_table.setModel(self.instances_proxy)
        
        # Gán delegate cho cột status
        self.instance_table.setItemDelegateForColumn(3, self.status_delegate)
        
        # Tối ưu hiệu suất và giao diện
        self.instance_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.instance_table.setAlternatingRowColors(True)
        self.instance_table.setSortingEnabled(True)
        self.instance_table.setWordWrap(False)
        self.instance_table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.instance_table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.instance_table.verticalHeader().setVisible(False)

        header = self.instance_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) # Cột Name
        header.setStretchLastSection(True)

    def create_right_panel(self) -> QWidget:
        """Tạo panel bên phải với thống kê."""
        right_widget = QWidget()
        layout = QVBoxLayout(right_widget)
        
        stats_group = QGroupBox("System Statistics")
        stats_group.setObjectName("StatsGroup")
        
        stats_layout = QGridLayout(stats_group)
        self.instance_count_label = QLabel("Instances: 0")
        self.running_count_label = QLabel("Running: 0")
        stats_layout.addWidget(self.instance_count_label, 0, 0)
        stats_layout.addWidget(self.running_count_label, 0, 1)
        
        layout.addWidget(stats_group)
        layout.addStretch()
        return right_widget

    def connect_signals(self):
        """Kết nối tất cả các tín hiệu."""
        # StateManager signals
        self.state_manager.instances_changed.connect(self.on_instances_changed)

        # Control signals
        self.search_edit.textChanged.connect(self.on_filter_changed)
        self.filter_combo.currentTextChanged.connect(self.on_filter_changed)
        self.btn_select_all.clicked.connect(lambda: self.instances_model.set_all_checked(True))
        self.btn_deselect_all.clicked.connect(lambda: self.instances_model.set_all_checked(False))

        print("✅ MonokaiDashboard signals connected")

    # --- SLOTS --- #
    def on_instances_changed(self, instances_data: list):
        """Slot xử lý khi dữ liệu instances từ StateManager thay đổi."""
        print(f"Received {len(instances_data)} instances from StateManager. Updating model.")
        self.instances_model.set_rows(instances_data)
        
        # Cập nhật các label thống kê
        running_count = sum(1 for inst in instances_data if inst.get('info', {}).get('is_process_started'))
        self.instance_count_label.setText(f"Instances: {len(instances_data)}")
        self.running_count_label.setText(f"Running: {running_count}")

    def on_filter_changed(self):
        """Slot xử lý khi bộ lọc thay đổi."""
        keyword = self.search_edit.text()
        status = self.filter_combo.currentText()
        self.instances_proxy.set_filters(keyword, status)

    def apply_monokai_style(self):
        """Áp dụng stylesheet Monokai."""
        # (Stylesheet content remains largely the same, but targets QTableView now)
        style = """
        QWidget#MonokaiDashboard {
            background-color: #272822;
            color: #F8F8F2;
        }
        QFrame#ControlsFrame {
            background-color: #2D2A2E;
            border: 1px solid #49483E;
            border-radius: 3px;
        }
        QTableView#InstanceTableView {
            background-color: #272822;
            color: #F8F8F2;
            border: 1px solid #49483E;
            gridline-color: #49483E;
            alternate-background-color: #2D2A2E;
            selection-background-color: #49483E;
            selection-color: #A6E22E;
        }
        QHeaderView::section {
            background-color: #2D2A2E;
            color: #F92672;
            padding: 8px;
            border: 1px solid #49483E;
            font-weight: bold;
        }
        QPushButton, QComboBox, QLineEdit {
             background-color: #2D2A2E;
             border: 1px solid #49483E;
             padding: 5px;
             color: #F8F8F2;
        }
        QPushButton:hover {
            background-color: #49483E;
        }
        QGroupBox {
            color: #FD971F;
            border: 1px solid #49483E;
            border-radius: 3px;
            margin-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        """
        self.setStyleSheet(style)
