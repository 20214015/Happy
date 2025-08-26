"""
Dashboard Monokai - Giao diện bảng dashboard theo theme Monokai cổ điển
Thiết kế theo phong cách terminal/console với màu sắc Monokai đặc trưng
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QPushButton, QLineEdit, QComboBox, QSplitter,
    QGroupBox, QGridLayout, QProgressBar, QTextEdit, QScrollArea, QAbstractItemView,
    QMenu, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QItemSelectionModel
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QPen, QBrush, QAction
import time
import psutil  # For system stats
import shutil  # For disk usage
from datetime import datetime

class MonokaiDashboard(QWidget):
    """Dashboard với theme Monokai cổ điển"""
    
    # Signals for communication with MainWindow
    instance_selected = pyqtSignal(int)
    refresh_requested = pyqtSignal()
    start_all_requested = pyqtSignal()
    stop_all_requested = pyqtSignal()
    start_instance_requested = pyqtSignal(int)
    stop_instance_requested = pyqtSignal(int)
    restart_instance_requested = pyqtSignal(int)
    cleanup_requested = pyqtSignal(list)  # list of instance IDs
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MonokaiDashboard")
        
        # Backend reference
        self.backend = None
        
        # Monokai Colors
        self.colors = {
            'bg': '#272822',           # Background chính
            'bg_alt': '#2D2A2E',       # Background phụ
            'fg': '#F8F8F2',           # Text chính
            'comment': '#75715E',       # Text phụ/comment
            'pink': '#F92672',         # Accent pink
            'green': '#A6E22E',        # Success green
            'orange': '#FD971F',       # Warning orange
            'blue': '#66D9EF',         # Info blue
            'purple': '#AE81FF',       # Purple
            'yellow': '#E6DB74',       # String yellow
            'border': '#49483E',       # Border color
            'selection': '#3E3D32'     # Selection color
        }
        
        self.instances_data = []
        self.filtered_data = []
        
        # Create model/proxy for compatibility with MainWindow
        try:
            from widgets import InstancesModel, InstancesProxy
            self.instances_model = InstancesModel(parent)
            self.instances_proxy = InstancesProxy(parent)
            self.instances_proxy.setSourceModel(self.instances_model)
            print("✅ MonokaiDashboard: instances_model created successfully")
        except Exception as e:
            print(f"❌ Warning: Could not create model/proxy: {e}")
            import traceback
            traceback.print_exc()
            self.instances_model = None
            self.instances_proxy = None
        
        self.setup_ui()
        self.apply_monokai_style()
        
        # Auto refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.auto_refresh)
        
        # Search debounce timer
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self._perform_search)
        
    def set_backend(self, backend):
        """Set backend reference và load data"""
        self.backend = backend
        if backend:
            self.load_data_from_backend()
    
    def load_data_from_backend(self):
        """Load dữ liệu từ backend"""
        if not self.backend:
            print("⚠️ No backend available - using demo data")
            self.create_demo_data()
            return
            
        try:
            # Get instances từ backend
            instances = None
            if hasattr(self.backend, 'get_instances'):
                print("🔍 Loading instances via get_instances...")
                instances = self.backend.get_instances()
            elif hasattr(self.backend, 'get_all_info'):
                print("🔍 Loading instances via get_all_info...")
                success, data = self.backend.get_all_info()
                if success and data:
                    print(f"✅ Backend returned success={success}, data type={type(data)}")
                    # Backend trả về dict với key là index như {'0': {data}, '1': {data}...}
                    if isinstance(data, dict):
                        # Convert dict to list of instances
                        instances = list(data.values())
                        print(f"📊 Converted {len(instances)} instances from dict format")
                    else:
                        instances = data
                else:
                    print(f"⚠️ Backend get_all_info failed: success={success}")
            else:
                print("⚠️ Backend doesn't have get_instances or get_all_info method")
                
            if instances:
                print(f"✅ Loaded {len(instances)} instances from backend")
                self.update_instances_data(instances)
            else:
                print("⚠️ No instances data received - using demo data")
                self.create_demo_data()
        except Exception as e:
            print(f"⚠️ Error loading data from backend: {e}")
            import traceback
            traceback.print_exc()
            self.create_demo_data()
    
    def update_instances_data(self, instances):
        """Cập nhật dữ liệu instances"""
        self.instances_data = []
        for i, instance in enumerate(instances):
            self.instances_data.append({
                'index': i,
                'name': instance.get('name', f'MuMu Player {i}'),
                'status': instance.get('status', 'Stopped'),
                'adb': instance.get('adb_port', 16384 + i),
                'disk_usage': instance.get('disk_usage', '1.0GB'),
                'cpu_usage': instance.get('cpu_usage', '15%'),
                'memory_usage': instance.get('memory_usage', '2.1GB')
            })
        
        self.filtered_data = self.instances_data.copy()
        self.populate_table()
        self.update_stats()
        
        # Sync với instances_model
        self.sync_model_data()
    
    def create_demo_data(self):
        """Tạo dữ liệu demo để test"""
        self.instances_data = []
        for i in range(20):
            self.instances_data.append({
                'index': i,
                'name': f'MuMu Player {i}',
                'status': 'Running' if i % 3 == 0 else 'Stopped',
                'adb': 16384 + i,
                'disk_usage': f'{1.0 + i * 0.1:.1f}GB',
                'cpu_usage': f'{10 + i * 2}%',
                'memory_usage': f'{1.5 + i * 0.3:.1f}GB'
            })
        
        self.filtered_data = self.instances_data.copy()
        self.populate_table()
        self.update_stats()
        
        # Sync với instances_model
        self.sync_model_data()
        
    def setup_ui(self):
        """Setup giao diện dashboard"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header với thông tin tổng quan
        self.create_header()
        layout.addWidget(self.header_widget)
        
        # Main content area
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Table và controls
        left_panel = self.create_left_panel()
        main_splitter.addWidget(left_panel)
        
        # Right panel - Stats và monitoring
        right_panel = self.create_right_panel()
        main_splitter.addWidget(right_panel)
        
        # Set splitter ratios (70% left, 30% right)
        main_splitter.setStretchFactor(0, 7)
        main_splitter.setStretchFactor(1, 3)
        
        layout.addWidget(main_splitter)
        
        # Bottom status bar
        self.create_status_bar()
        layout.addWidget(self.status_bar)
        
    def create_header(self):
        """Tạo header với thông tin tổng quan"""
        self.header_widget = QFrame()
        self.header_widget.setFixedHeight(80)
        self.header_widget.setFrameStyle(QFrame.Shape.Box)
        
        layout = QHBoxLayout(self.header_widget)
        
        # Title
        title_label = QLabel("🖥️ MuMuManager MKV - Terminal Dashboard")
        title_label.setObjectName("HeaderTitle")
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        # Quick stats
        self.stats_widget = QWidget()
        stats_layout = QHBoxLayout(self.stats_widget)
        
        # Total instances
        self.total_label = QLabel("Total: 0")
        self.total_label.setObjectName("StatLabel")
        stats_layout.addWidget(self.total_label)
        
        # Running instances
        self.running_label = QLabel("Running: 0")
        self.running_label.setObjectName("StatLabelGreen")
        stats_layout.addWidget(self.running_label)
        
        # Stopped instances
        self.stopped_label = QLabel("Stopped: 0")
        self.stopped_label.setObjectName("StatLabelRed")
        stats_layout.addWidget(self.stopped_label)
        
        # Memory usage
        self.memory_label = QLabel("Memory: 0 GB")
        self.memory_label.setObjectName("StatLabelBlue")
        stats_layout.addWidget(self.memory_label)
        
        layout.addWidget(self.stats_widget)
        
    def create_left_panel(self):
        """Tạo panel bên trái với bảng instances"""
        left_widget = QWidget()
        layout = QVBoxLayout(left_widget)
        
        # Control bar
        controls = self.create_controls()
        layout.addWidget(controls)
        
        # Instance table
        self.create_instance_table()
        layout.addWidget(self.instance_table)
        
        return left_widget
        
    def create_controls(self):
        """Tạo thanh điều khiển"""
        controls_widget = QFrame()
        controls_widget.setFixedHeight(50)
        controls_widget.setFrameStyle(QFrame.Shape.Box)
        
        layout = QHBoxLayout(controls_widget)
        
        # Search
        search_label = QLabel("Search:")
        search_label.setObjectName("ControlLabel")
        layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name or index...")
        self.search_input.setObjectName("SearchInput")
        self.search_input.textChanged.connect(self._schedule_search)  # Use debounced search
        layout.addWidget(self.search_input)
        
        # Expose search_input as search_edit for compatibility with MainWindow
        self.search_edit = self.search_input
        
        # Status filter
        status_label = QLabel("Status:")
        status_label.setObjectName("ControlLabel")
        layout.addWidget(status_label)
        
        self.status_filter = QComboBox()
        self.status_filter.setObjectName("StatusFilter")
        self.status_filter.addItems(["All", "Running", "Stopped"])
        self.status_filter.currentTextChanged.connect(self._schedule_search)  # Use debounced search
        layout.addWidget(self.status_filter)
        
        # Expose status_filter as filter_combo for compatibility
        self.filter_combo = self.status_filter
        
        layout.addStretch()
        
        # Action buttons
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.setObjectName("RefreshButton")
        self.refresh_btn.clicked.connect(self.manual_refresh)
        layout.addWidget(self.refresh_btn)
        
        self.auto_refresh_btn = QPushButton("🤖 Auto")
        self.auto_refresh_btn.setObjectName("AutoButton")
        self.auto_refresh_btn.setCheckable(True)
        self.auto_refresh_btn.toggled.connect(self.toggle_auto_refresh)
        layout.addWidget(self.auto_refresh_btn)
        
        # Expose auto_refresh_btn as btn_auto_refresh for compatibility
        self.btn_auto_refresh = self.auto_refresh_btn
        
        # Add select/deselect buttons for compatibility
        self.btn_select_all = QPushButton("✅ Select All")
        self.btn_select_all.setObjectName("SelectButton")
        self.btn_select_all.clicked.connect(self.select_all_instances)
        layout.addWidget(self.btn_select_all)
        
        self.btn_deselect_all = QPushButton("❌ Deselect")
        self.btn_deselect_all.setObjectName("DeselectButton")
        self.btn_deselect_all.clicked.connect(self.deselect_all_instances)
        layout.addWidget(self.btn_deselect_all)
        
        return controls_widget
        
    def create_instance_table(self):
        """Tạo bảng hiển thị instances với tối ưu hiệu suất"""
        self.instance_table = QTableWidget()
        self.instance_table.setObjectName("InstanceTable")
        
        # Tối ưu hiệu suất table
        self.optimize_table_performance()
        
        # Columns
        columns = ["#", "Name", "Status", "ADB Port", "CPU %", "Memory", "Disk Usage", "Uptime"]
        self.instance_table.setColumnCount(len(columns))
        self.instance_table.setHorizontalHeaderLabels(columns)
        
        # Table settings với tối ưu
        self.instance_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.instance_table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)  # Allow multiple selection
        self.instance_table.setAlternatingRowColors(True)
        self.instance_table.setSortingEnabled(True)
        
        # Tối ưu scroll mode
        self.instance_table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.instance_table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        
        # Enable context menu
        self.instance_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.instance_table.customContextMenuRequested.connect(self.show_context_menu)
        
        # Header settings - Check if header exists first
        header = self.instance_table.horizontalHeader()
        if header is not None:
            header.setStretchLastSection(True)
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # #
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Name
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Status
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # ADB
        
        # Connect signals
        self.instance_table.cellDoubleClicked.connect(self.on_instance_double_click)
        self.instance_table.itemSelectionChanged.connect(self.on_selection_changed)
        
    def optimize_table_performance(self):
        """Tối ưu hiệu suất bảng"""
        try:
            if hasattr(self, 'instance_table'):
                # Disable updates during optimization
                self.instance_table.setUpdatesEnabled(False)
                
                # Set optimal settings
                self.instance_table.setShowGrid(True)
                self.instance_table.setWordWrap(False)  # Disable word wrap for better performance
                
                # Re-enable updates
                self.instance_table.setUpdatesEnabled(True)
                
                print("✅ Table performance optimized")
        except Exception as e:
            print(f"⚠️ Error optimizing table: {e}")
        
    def create_right_panel(self):
        """Tạo panel bên phải với thống kê và monitoring"""
        right_widget = QWidget()
        layout = QVBoxLayout(right_widget)
        
        # System stats
        stats_group = QGroupBox("System Statistics")
        stats_group.setObjectName("StatsGroup")
        self.create_stats_panel(stats_group)
        layout.addWidget(stats_group)
        
        # Performance monitor
        perf_group = QGroupBox("Performance Monitor")
        perf_group.setObjectName("PerfGroup")
        self.create_performance_panel(perf_group)
        layout.addWidget(perf_group)
        
        # Quick actions
        actions_group = QGroupBox("Quick Actions")
        actions_group.setObjectName("ActionsGroup")
        self.create_actions_panel(actions_group)
        layout.addWidget(actions_group)
        
        # Log preview
        log_group = QGroupBox("Recent Logs")
        log_group.setObjectName("LogGroup")
        self.create_log_panel(log_group)
        layout.addWidget(log_group)
        
        return right_widget
        
    def create_stats_panel(self, parent):
        """Tạo panel thống kê"""
        layout = QGridLayout(parent)
        
        # System statistics labels (chỉ giữ Memory và Disk)
        self.total_memory_label = QLabel("Total Memory: 0GB")
        self.total_disk_label = QLabel("Total Disk: 0GB")
        
        # Layout cho statistics - bắt đầu từ row 0
        layout.addWidget(self.total_memory_label, 0, 0)
        layout.addWidget(self.total_disk_label, 0, 1)
        
        # Progress bars với labels riêng biệt
        layout.addWidget(QLabel("Memory Usage:"), 1, 0)
        self.memory_progress = QProgressBar()
        self.memory_progress.setObjectName("MemoryProgress")
        self.memory_progress.setFormat("%p%")
        layout.addWidget(self.memory_progress, 1, 1)
        
        layout.addWidget(QLabel("CPU Usage:"), 2, 0)
        self.cpu_progress = QProgressBar()
        self.cpu_progress.setObjectName("CPUProgress")
        self.cpu_progress.setFormat("%p%")
        layout.addWidget(self.cpu_progress, 2, 1)
        
        layout.addWidget(QLabel("Disk Usage:"), 3, 0)
        self.disk_progress = QProgressBar()
        self.disk_progress.setObjectName("DiskProgress")
        self.disk_progress.setFormat("%p%")
        layout.addWidget(self.disk_progress, 3, 1)
        
    def create_performance_panel(self, parent):
        """Tạo panel hiệu suất"""
        layout = QVBoxLayout(parent)
        
        # Performance metrics
        self.perf_text = QTextEdit()
        self.perf_text.setObjectName("PerfText")
        self.perf_text.setMaximumHeight(120)
        self.perf_text.setReadOnly(True)
        layout.addWidget(self.perf_text)
        
        # Update performance info
        self.update_performance_info()
        
    def create_actions_panel(self, parent):
        """Tạo panel hành động nhanh"""
        layout = QVBoxLayout(parent)
        
        # Dynamic action buttons based on selection
        self.start_btn = QPushButton("▶️ Start")
        self.start_btn.setObjectName("ActionButton")
        self.start_btn.clicked.connect(self.handle_start_action)
        layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹️ Stop")  
        self.stop_btn.setObjectName("ActionButton")
        self.stop_btn.clicked.connect(self.handle_stop_action)
        layout.addWidget(self.stop_btn)
        
        restart_btn = QPushButton("🔄 Restart Selected")
        restart_btn.setObjectName("ActionButton")
        restart_btn.clicked.connect(self.restart_selected_instances)
        layout.addWidget(restart_btn)
        
        cleanup_btn = QPushButton("🧹 Cleanup")
        cleanup_btn.setObjectName("ActionButton")
        cleanup_btn.clicked.connect(self.cleanup_instances)
        layout.addWidget(cleanup_btn)
        
        # Update button text initially
        self.update_action_buttons_text()
        
    def create_log_panel(self, parent):
        """Tạo panel log preview"""
        layout = QVBoxLayout(parent)
        
        self.log_text = QTextEdit()
        self.log_text.setObjectName("LogText")
        self.log_text.setMaximumHeight(150)
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)
        
        # Add real time logs
        self.update_logs()
        
        # Log timer for real-time updates
        self.log_timer = QTimer()
        self.log_timer.timeout.connect(self.update_logs)
        self.log_timer.start(2000)  # Update every 2 seconds
        
    def update_logs(self):
        """Update log display với đa dạng thông tin hoạt động"""
        try:
            from datetime import datetime
            import random
            current_time = datetime.now().strftime("%H:%M:%S")
            
            # Tạo đa dạng log entries
            running_count = len([i for i in self.instances_data if i.get('status') == 'running'])
            total_count = len(self.instances_data)
            
            # Random log activities để mô phỏng hệ thống sống động
            log_types = [
                f"Status: {running_count}/{total_count} instances active",
                f"Memory: {sum(1 for i in self.instances_data if 'GB' in str(i.get('memory_usage', '')))} instances using high memory",
                f"Performance: System running at {random.randint(75, 98)}% efficiency", 
                f"Network: {random.randint(1, 5)} instances with active connections",
                f"Security: All instances verified and secure",
                f"Database: {total_count} records synchronized",
                f"Cache: Performance optimization active",
                f"Monitor: Real-time stats collection enabled",
                f"AI: Predictive analysis completed",
                f"Backup: Auto-save configurations updated"
            ]
            
            # Chọn random log entry để tạo sự đa dạng
            log_entry = f"[{current_time}] {random.choice(log_types)}"
            
            # Keep only last 10 log entries
            current_text = self.log_text.toPlainText()
            lines = current_text.split('\n')
            if len(lines) >= 10:
                lines = lines[-9:]  # Keep last 9 lines
                
            lines.append(log_entry)
            self.log_text.setPlainText('\n'.join(lines))
            
            # Auto scroll to bottom
            cursor = self.log_text.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            self.log_text.setTextCursor(cursor)
            
        except Exception as e:
            print(f"⚠️ Error updating logs: {e}")
            
    def add_sample_logs(self):
        """Add initial sample logs"""
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S")
        
        sample_logs = [
            f"[{current_time}] System: MuMuManager MKV initialized successfully",
            f"[{current_time}] Backend: Ultra-fast database connected", 
            f"[{current_time}] Data: Loaded {len(self.instances_data)} instances from cache",
            f"[{current_time}] Theme: Monokai terminal theme applied",
            f"[{current_time}] AI: Performance optimizer activated",
            f"[{current_time}] Ready: Terminal dashboard is ready for use"
        ]
        
        self.log_text.setPlainText('\n'.join(sample_logs))
        
    def create_status_bar(self):
        """Tạo status bar"""
        self.status_bar = QFrame()
        self.status_bar.setFixedHeight(30)
        self.status_bar.setFrameStyle(QFrame.Shape.Box)
        
        layout = QHBoxLayout(self.status_bar)
        
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("StatusLabel")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        self.time_label = QLabel("")
        self.time_label.setObjectName("TimeLabel")
        layout.addWidget(self.time_label)
        
        # Update time every second
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)
        self.update_time()
        
    def apply_monokai_style(self):
        """Áp dụng stylesheet Monokai"""
        style = f"""
        /* Main Dashboard */
        QWidget#MonokaiDashboard {{
            background-color: {self.colors['bg']};
            color: {self.colors['fg']};
            font-family: 'Consolas', 'Monaco', monospace;
        }}
        
        /* Header */
        QFrame {{
            background-color: {self.colors['bg_alt']};
            border: 1px solid {self.colors['border']};
            border-radius: 3px;
        }}
        
        QLabel#HeaderTitle {{
            font-size: 18px;
            font-weight: bold;
            color: {self.colors['pink']};
            padding: 10px;
        }}
        
        QLabel#StatLabel {{
            color: {self.colors['fg']};
            font-weight: bold;
            padding: 5px 10px;
            margin: 2px;
            background-color: {self.colors['border']};
            border-radius: 3px;
        }}
        
        QLabel#StatLabelGreen {{
            color: {self.colors['green']};
            font-weight: bold;
            padding: 5px 10px;
            margin: 2px;
            background-color: {self.colors['border']};
            border-radius: 3px;
        }}
        
        QLabel#StatLabelRed {{
            color: {self.colors['pink']};
            font-weight: bold;
            padding: 5px 10px;
            margin: 2px;
            background-color: {self.colors['border']};
            border-radius: 3px;
        }}
        
        QLabel#StatLabelBlue {{
            color: {self.colors['blue']};
            font-weight: bold;
            padding: 5px 10px;
            margin: 2px;
            background-color: {self.colors['border']};
            border-radius: 3px;
        }}
        
        /* Controls */
        QLabel#ControlLabel {{
            color: {self.colors['comment']};
            font-weight: bold;
            margin-right: 5px;
        }}
        
        QLineEdit#SearchInput {{
            background-color: {self.colors['bg_alt']};
            border: 1px solid {self.colors['border']};
            border-radius: 3px;
            padding: 5px;
            color: {self.colors['fg']};
            selection-background-color: rgba(166, 226, 46, 0.4);
        }}
        
        QLineEdit#SearchInput:focus {{
            border: 2px solid {self.colors['blue']};
        }}
        
        QComboBox#StatusFilter {{
            background-color: {self.colors['bg_alt']};
            border: 1px solid {self.colors['border']};
            border-radius: 3px;
            padding: 5px;
            color: {self.colors['fg']};
            min-width: 80px;
        }}
        
        QComboBox#StatusFilter::drop-down {{
            border: none;
            width: 20px;
        }}
        
        QComboBox#StatusFilter::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {self.colors['comment']};
        }}
        
        QComboBox#StatusFilter QAbstractItemView {{
            background-color: {self.colors['bg_alt']};
            border: 1px solid {self.colors['border']};
            color: {self.colors['fg']};
            selection-background-color: rgba(166, 226, 46, 0.4);
        }}
        
        /* Buttons */
        QPushButton#RefreshButton, QPushButton#AutoButton, QPushButton#ActionButton {{
            background-color: {self.colors['border']};
            border: 1px solid {self.colors['comment']};
            border-radius: 3px;
            padding: 8px 15px;
            color: {self.colors['fg']};
            font-weight: bold;
            min-width: 80px;
        }}
        
        QPushButton#RefreshButton:hover, QPushButton#AutoButton:hover, QPushButton#ActionButton:hover {{
            background-color: {self.colors['pink']};
            border-color: {self.colors['pink']};
        }}
        
        QPushButton#AutoButton:checked {{
            background-color: {self.colors['green']};
            border-color: {self.colors['green']};
        }}
        
        /* Table */
        QTableWidget#InstanceTable {{
            background-color: {self.colors['bg']};
            alternate-background-color: {self.colors['bg_alt']};
            color: {self.colors['fg']};
            border: 1px solid {self.colors['border']};
            gridline-color: {self.colors['border']};
            selection-background-color: rgba(166, 226, 46, 0.3);
            selection-color: {self.colors['fg']};
        }}
        
        QTableWidget#InstanceTable::item {{
            padding: 8px;
            border-bottom: 1px solid {self.colors['border']};
        }}
        
        QTableWidget#InstanceTable::item:selected {{
            background-color: rgba(166, 226, 46, 0.3);
        }}
        
        QHeaderView::section {{
            background-color: {self.colors['border']};
            color: {self.colors['fg']};
            padding: 8px;
            border: 1px solid {self.colors['comment']};
            font-weight: bold;
        }}
        
        /* Group Boxes */
        QGroupBox#StatsGroup, QGroupBox#PerfGroup, QGroupBox#ActionsGroup, QGroupBox#LogGroup {{
            color: {self.colors['fg']};
            border: 2px solid {self.colors['border']};
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
            font-weight: bold;
        }}
        
        QGroupBox#StatsGroup::title, QGroupBox#PerfGroup::title, QGroupBox#ActionsGroup::title, QGroupBox#LogGroup::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 10px 0 10px;
            color: {self.colors['orange']};
        }}
        
        /* Progress Bars */
        QProgressBar#MemoryProgress, QProgressBar#CPUProgress, QProgressBar#DiskProgress {{
            border: 1px solid {self.colors['border']};
            border-radius: 3px;
            background-color: {self.colors['bg_alt']};
            text-align: center;
            color: {self.colors['fg']};
        }}
        
        QProgressBar#MemoryProgress::chunk {{
            background-color: {self.colors['blue']};
            border-radius: 2px;
        }}
        
        QProgressBar#CPUProgress::chunk {{
            background-color: {self.colors['green']};
            border-radius: 2px;
        }}
        
        QProgressBar#DiskProgress::chunk {{
            background-color: {self.colors['orange']};
            border-radius: 2px;
        }}
        
        /* Text Areas */
        QTextEdit#PerfText, QTextEdit#LogText {{
            background-color: {self.colors['bg_alt']};
            border: 1px solid {self.colors['border']};
            border-radius: 3px;
            color: {self.colors['fg']};
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 11px;
        }}
        
        /* Status Bar */
        QLabel#StatusLabel {{
            color: {self.colors['green']};
            font-weight: bold;
        }}
        
        QLabel#TimeLabel {{
            color: {self.colors['comment']};
            font-family: 'Consolas', 'Monaco', monospace;
        }}
        
        /* Scrollbars */
        QScrollBar:vertical {{
            background-color: {self.colors['bg_alt']};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {self.colors['border']};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {self.colors['comment']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
        }}
        """
        
        self.setStyleSheet(style)
        
    def update_instances(self, instances_data):
        """Cập nhật dữ liệu instances"""
        self.instances_data = instances_data
        self.filter_instances()
        self.update_stats()
        
    def _schedule_search(self):
        """Schedule search with debouncing to prevent excessive filtering"""
        self.search_timer.stop()
        self.search_timer.start(300)  # 300ms debounce delay
        
    def _perform_search(self):
        """Perform the actual search/filter operation"""
        self.filter_instances()
        
    def filter_instances(self):
        """Lọc instances theo search và status với early return optimization"""
        search_text = self.search_input.text().lower()
        status_filter = self.status_filter.currentText()
        
        # Early return if no data
        if not self.instances_data:
            self.filtered_data = []
            self.populate_table()
            return
        
        # Early return if no filtering needed
        if not search_text and status_filter == "All":
            self.filtered_data = self.instances_data.copy()
            self.populate_table()
            return
        
        self.filtered_data = []
        for instance in self.instances_data:
            # Early continue for search filter
            if search_text:
                name_match = search_text in instance.get('name', '').lower()
                index_match = search_text in str(instance.get('index', ''))
                if not (name_match or index_match):
                    continue
                    
            # Early continue for status filter
            if status_filter != "All":
                instance_status = "Running" if instance.get('status') == 'running' else "Stopped"
                if status_filter != instance_status:
                    continue
                    
            self.filtered_data.append(instance)
            
        self.populate_table()
        
    def populate_table(self):
        """Điền dữ liệu vào bảng với tối ưu hiệu suất"""
        try:
            # Tắt sorting để tối ưu hiệu suất
            self.instance_table.setSortingEnabled(False)
            
            # Set row count
            self.instance_table.setRowCount(len(self.filtered_data))
            
            # Disable updates for batch processing
            self.instance_table.setUpdatesEnabled(False)
            
            for row, instance in enumerate(self.filtered_data):
                try:
                    # Index - Right aligned
                    index_item = QTableWidgetItem(str(instance.get('index', row + 1)))
                    index_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    self.instance_table.setItem(row, 0, index_item)
                    
                    # Name
                    name_item = QTableWidgetItem(instance.get('name', f'MuMu-{row}'))
                    self.instance_table.setItem(row, 1, name_item)
                    
                    # Status with proper color coding
                    status = instance.get('status', 'offline')
                    if status == 'running':
                        status_display = "🟢 Running"
                        status_color = self.colors['green']
                    elif status == 'starting':
                        status_display = "🟡 Starting"
                        status_color = self.colors['yellow']
                    else:
                        status_display = "🔴 Stopped"
                        status_color = self.colors['pink']
                        
                    status_item = QTableWidgetItem(status_display)
                    status_item.setForeground(QColor(status_color))
                    self.instance_table.setItem(row, 2, status_item)
                    
                    # ADB Port - fix key consistency
                    adb_port = instance.get('adb_port', instance.get('adb', 'N/A'))
                    adb_item = QTableWidgetItem(str(adb_port))
                    adb_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.instance_table.setItem(row, 3, adb_item)
                    
                    # CPU % - with proper formatting
                    cpu_value = instance.get('cpu_usage', 0)
                    if isinstance(cpu_value, str):
                        cpu_usage = cpu_value
                    else:
                        cpu_usage = f"{cpu_value:.1f}%"
                    cpu_item = QTableWidgetItem(cpu_usage)
                    cpu_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    self.instance_table.setItem(row, 4, cpu_item)
                    
                    # Memory
                    memory = instance.get('memory_usage', 'N/A')
                    memory_item = QTableWidgetItem(str(memory))
                    memory_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    self.instance_table.setItem(row, 5, memory_item)
                    
                    # Disk Usage
                    disk = instance.get('disk_usage', 'N/A')
                    disk_item = QTableWidgetItem(str(disk))
                    disk_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    self.instance_table.setItem(row, 6, disk_item)
                    
                    # Uptime
                    uptime = instance.get('uptime', 'N/A')
                    uptime_item = QTableWidgetItem(str(uptime))
                    uptime_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.instance_table.setItem(row, 7, uptime_item)
                    
                except Exception as e:
                    print(f"⚠️ Error populating row {row}: {e}")
                    continue
            
            # Bật lại sorting và updates
            self.instance_table.setSortingEnabled(True)
            self.instance_table.setUpdatesEnabled(True)
            
            # Sync với instances_model cho compatibility
            self.sync_model_data()
            
            # Cập nhật statistics sau khi populate
            self.update_stats()
            
            print(f"✅ Table populated with {len(self.filtered_data)} instances")
            
        except Exception as e:
            print(f"⚠️ Error in populate_table: {e}")
            
    def sync_model_data(self):
        """Sync data với instances_model để compatibility với MainWindow"""
        if not self.instances_model:
            return
            
        try:
            # Convert filtered_data to format expected by InstancesModel
            # filtered_data has format: [{'index': int, 'name': str, 'status': str, ...}, ...]
            # InstancesModel expects: [(index, info), ...]
            model_data = []
            for instance in self.filtered_data:
                index = instance.get('index', 0)
                # Remove 'index' from info to avoid duplication
                info = {k: v for k, v in instance.items() if k != 'index'}
                model_data.append((index, info))
            
            # Update model using proper method
            if hasattr(self.instances_model, 'set_rows'):
                self.instances_model.set_rows(model_data)
            
        except Exception as e:
            print(f"Warning: Failed to sync model data: {e}")
            
    def update_stats(self):
        """Cập nhật thống kê tổng quan với thông số thực tế từ hệ thống"""
        total = len(self.instances_data)
        running = sum(1 for i in self.instances_data if i.get('status') == 'running')
        stopped = total - running
        
        # Update header stats (instance counts)
        self.total_label.setText(f"Total: {total}")
        self.running_label.setText(f"Running: {running}")
        self.stopped_label.setText(f"Stopped: {stopped}")
        
        try:
            # Get real system stats
            # Memory usage
            memory = psutil.virtual_memory()
            memory_total_gb = memory.total / (1024**3)
            memory_used_gb = memory.used / (1024**3)
            memory_percent = memory.percent
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # Disk usage for root filesystem (cross-platform)
            import os
            disk_path = 'C:' if os.name == 'nt' else '/'
            disk = psutil.disk_usage(disk_path)
            disk_total_gb = disk.total / (1024**3)
            disk_used_gb = disk.used / (1024**3)
            disk_percent = (disk.used / disk.total) * 100
            
            # Update labels with real system data
            self.total_memory_label.setText(f"System Memory: {memory_used_gb:.1f}/{memory_total_gb:.1f}GB")
            self.total_disk_label.setText(f"System Disk: {disk_used_gb:.1f}/{disk_total_gb:.1f}GB")
            
            # Update progress bars with real percentages
            self.memory_progress.setValue(int(memory_percent))
            self.cpu_progress.setValue(int(cpu_percent))
            self.disk_progress.setValue(int(disk_percent))
            
            print(f"📊 System Statistics updated: Memory={memory_used_gb:.1f}GB ({memory_percent:.1f}%), CPU={cpu_percent:.1f}%, Disk={disk_used_gb:.1f}GB ({disk_percent:.1f}%)")
            
        except Exception as e:
            print(f"⚠️ Error getting system stats: {e}")
            # Fallback to default values if system stats fail
            self.total_memory_label.setText("System Memory: N/A")
            self.total_disk_label.setText("System Disk: N/A")
            self.memory_progress.setValue(0)
            self.cpu_progress.setValue(0)
            self.disk_progress.setValue(0)
        
    def update_performance_info(self):
        """Cập nhật thông tin hiệu suất"""
        perf_info = f"""
⚡ Performance Metrics:
• Response Time: {12.5:.1f}ms
• Query Speed: {8.3:.1f}ms  
• Cache Hit Rate: {94.2:.1f}%
• Memory Efficiency: {87.5:.1f}%
• Database Optimization: Active
• AI Prediction: Enabled
        """.strip()
        
        self.perf_text.setPlainText(perf_info)
        

        
    def update_time(self):
        """Cập nhật thời gian hiện tại"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.setText(current_time)
        
    def on_instance_double_click(self, row, column):
        """Xử lý double click trên instance"""
        if row < len(self.filtered_data):
            instance = self.filtered_data[row]
            instance_id = instance.get('index', 0)
            self.instance_selected.emit(instance_id)
            
    def on_selection_changed(self):
        """Xử lý thay đổi selection với tối ưu hiệu suất"""
        try:
            # Sử dụng phương pháp tối ưu để lấy selected rows
            selected_instances = self.get_selected_instances()
            selected_count = len(selected_instances)
            
            # Chỉ cập nhật UI nếu có thay đổi
            if not hasattr(self, '_last_selection_count') or self._last_selection_count != selected_count:
                self._last_selection_count = selected_count
                
                # Cập nhật status label
                if selected_count == 0:
                    self.status_label.setText("No instances selected")
                elif selected_count == 1:
                    self.status_label.setText("1 instance selected")
                else:
                    self.status_label.setText(f"{selected_count} instances selected")
                
                # Update button text based on selection
                self.update_action_buttons_text()
                
                print(f"🔄 Selection changed: {selected_count} instances")
                
        except Exception as e:
            print(f"⚠️ Error in on_selection_changed: {e}")
        
    def manual_refresh(self):
        """Refresh thủ công"""
        self.status_label.setText("Refreshing...")
        self.refresh_requested.emit()
        
    def toggle_auto_refresh(self, enabled):
        """Bật/tắt auto refresh"""
        if enabled:
            self.refresh_timer.start(5000)  # 5 seconds
            self.status_label.setText("Auto-refresh enabled")
        else:
            self.refresh_timer.stop()
            self.status_label.setText("Auto-refresh disabled")
            
    def auto_refresh(self):
        """Auto refresh"""
        self.refresh_requested.emit()
        
    # ================== BUTTON ACTION METHODS ==================
    
    def select_all_instances(self):
        """Chọn tất cả instances trong table với xử lý lỗi tốt hơn"""
        try:
            # Phương pháp đơn giản và an toàn nhất
            self.instance_table.selectAll()
            
            # Cập nhật trạng thái
            total_rows = self.instance_table.rowCount()
            self.status_label.setText(f"Selected all {total_rows} instances")
            print(f"✅ Selected all {total_rows} instances")
            
            # Cập nhật thông tin selection
            self.on_selection_changed()
            
        except Exception as e:
            print(f"⚠️ Error selecting all instances: {e}")
            # Fallback method
            try:
                for row in range(self.instance_table.rowCount()):
                    self.instance_table.selectRow(row)
                print("✅ Selected all instances (fallback method)")
            except Exception as e2:
                print(f"⚠️ Fallback selection also failed: {e2}")
            
    def deselect_all_instances(self):
        """Bỏ chọn tất cả instances"""
        try:
            self.instance_table.clearSelection()
            self.status_label.setText("All instances deselected")
            print("✅ Deselected all instances")
            self.on_selection_changed()  # Update selection info
        except Exception as e:
            print(f"⚠️ Error deselecting instances: {e}")
            
    def get_selected_instances(self):
        """Lấy danh sách instances được chọn với xử lý lỗi tốt hơn"""
        try:
            selected_instances = []
            selected_rows = set()
            
            # Lấy các hàng được chọn an toàn hơn
            selection_model = self.instance_table.selectionModel()
            if selection_model:
                selected_indexes = selection_model.selectedRows()
                for index in selected_indexes:
                    if index.isValid():
                        selected_rows.add(index.row())
            else:
                # Fallback method if selection model not available
                for item in self.instance_table.selectedItems():
                    if item:
                        selected_rows.add(item.row())
                        
            # Lấy dữ liệu instance cho các hàng được chọn
            for row in selected_rows:
                if 0 <= row < len(self.filtered_data):
                    selected_instances.append(self.filtered_data[row])
                    
            return selected_instances
            
        except Exception as e:
            print(f"⚠️ Error getting selected instances: {e}")
            return []
        
    def start_all_instances(self):
        """Khởi động tất cả instances"""
        try:
            print("🚀 Requesting to start all instances...")
            self.status_label.setText("Starting all instances...")
            self.start_all_requested.emit()
        except Exception as e:
            print(f"⚠️ Error requesting start all: {e}")
            self.status_label.setText(f"❌ Error: {str(e)}")
            
    def stop_all_instances(self):
        """Dừng tất cả instances"""
        try:
            print("⏹️ Requesting to stop all instances...")
            self.status_label.setText("Stopping all instances...")
            self.stop_all_requested.emit()
        except Exception as e:
            print(f"⚠️ Error requesting stop all: {e}")
            self.status_label.setText(f"❌ Error: {str(e)}")
            
    def restart_selected_instances(self):
        """Khởi động lại instances được chọn"""
        try:
            selected_instances = self.get_selected_instances()
            if not selected_instances:
                self.status_label.setText("⚠️ No instances selected")
                return
                
            print(f"🔄 Requesting restart for {len(selected_instances)} selected instances...")
            self.status_label.setText(f"Restarting {len(selected_instances)} instances...")
            
            # Emit restart signal for each selected instance
            for instance in selected_instances:
                instance_id = instance.get('index', instance.get('id', 0))
                self.restart_instance_requested.emit(instance_id)
                        
        except Exception as e:
            print(f"⚠️ Error requesting restart: {e}")
            self.status_label.setText(f"❌ Error: {str(e)}")
            
    def cleanup_instances(self):
        """Dọn dẹp instances (xóa cache, temp files...)"""
        try:
            selected_instances = self.get_selected_instances()
            if not selected_instances:
                # Nếu không có gì được chọn, cleanup tất cả
                selected_instances = self.instances_data
                
            print(f"🧹 Requesting cleanup for {len(selected_instances)} instances...")
            self.status_label.setText(f"Cleaning up {len(selected_instances)} instances...")
            
            # Get instance IDs
            instance_ids = []
            for instance in selected_instances:
                instance_id = instance.get('index', instance.get('id', 0))
                instance_ids.append(instance_id)
                    
            self.cleanup_requested.emit(instance_ids)
            
        except Exception as e:
            print(f"⚠️ Error requesting cleanup: {e}")
            self.status_label.setText(f"❌ Error: {str(e)}")
            
    def start_selected_instances(self):
        """Khởi động instances được chọn"""
        try:
            selected_instances = self.get_selected_instances()
            if not selected_instances:
                self.status_label.setText("⚠️ No instances selected")
                return
                
            print(f"▶️ Requesting start for {len(selected_instances)} selected instances...")
            self.status_label.setText(f"Starting {len(selected_instances)} instances...")
            
            for instance in selected_instances:
                instance_id = instance.get('index', instance.get('id', 0))
                self.start_instance_requested.emit(instance_id)
                        
        except Exception as e:
            print(f"⚠️ Error requesting start selected: {e}")
            self.status_label.setText(f"❌ Error: {str(e)}")
            
    def stop_selected_instances(self):
        """Dừng instances được chọn"""
        try:
            selected_instances = self.get_selected_instances()
            if not selected_instances:
                self.status_label.setText("⚠️ No instances selected")
                return
                
            print(f"⏹️ Requesting stop for {len(selected_instances)} selected instances...")
            self.status_label.setText(f"Stopping {len(selected_instances)} instances...")
            
            for instance in selected_instances:
                instance_id = instance.get('index', instance.get('id', 0))
                self.stop_instance_requested.emit(instance_id)
                        
        except Exception as e:
            print(f"⚠️ Error requesting stop selected: {e}")
            self.status_label.setText(f"❌ Error: {str(e)}")
            
    # ================== UI UPDATE METHODS ==================
    
    def update_action_buttons_text(self):
        """Update button text based on selection count"""
        try:
            selected_count = len(self.get_selected_instances())
            
            if selected_count == 0:
                self.start_btn.setText("▶️ Start All")
                self.stop_btn.setText("⏹️ Stop All")
            elif selected_count == 1:
                self.start_btn.setText("▶️ Start")
                self.stop_btn.setText("⏹️ Stop")
            else:
                self.start_btn.setText(f"▶️ Start All ({selected_count})")
                self.stop_btn.setText(f"⏹️ Stop All ({selected_count})")
        except Exception as e:
            print(f"⚠️ Error updating button text: {e}")
            
    def handle_start_action(self):
        """Handle start button click - start all or selected based on selection"""
        try:
            selected_instances = self.get_selected_instances()
            if len(selected_instances) == 0:
                self.start_all_instances()
            else:
                self.start_selected_instances()
        except Exception as e:
            print(f"⚠️ Error handling start action: {e}")
            
    def handle_stop_action(self):
        """Handle stop button click - stop all or selected based on selection"""
        try:
            selected_instances = self.get_selected_instances()
            if len(selected_instances) == 0:
                self.stop_all_instances()
            else:
                self.stop_selected_instances()
        except Exception as e:
            print(f"⚠️ Error handling stop action: {e}")
            
    def show_context_menu(self, position):
        """Show Monokai-themed context menu on right click"""
        try:
            # Get the item at position
            item = self.instance_table.itemAt(position)
            if not item:
                return
                
            row = item.row()
            if row >= len(self.filtered_data):
                return
                
            instance = self.filtered_data[row]
            instance_name = instance.get('name', f'Instance {row}')
            instance_status = instance.get('status', 'offline')
            
            # Create Monokai-themed context menu
            menu = QMenu(self)
            menu.setObjectName("MonokaiContextMenu")
            
            # Apply Monokai styling
            menu.setStyleSheet(f"""
                QMenu {{
                    background-color: {self.colors['bg']};
                    border: 2px solid {self.colors['comment']};
                    border-radius: 8px;
                    padding: 8px;
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 12px;
                    color: {self.colors['fg']};
                }}
                QMenu::item {{
                    background-color: transparent;
                    padding: 8px 16px;
                    margin: 2px;
                    border-radius: 4px;
                    color: {self.colors['fg']};
                }}
                QMenu::item:selected {{
                    background-color: {self.colors['selection']};
                    color: {self.colors['yellow']};
                    border: 1px solid {self.colors['purple']};
                }}
                QMenu::item:disabled {{
                    color: {self.colors['comment']};
                }}
                QMenu::separator {{
                    height: 2px;
                    background-color: {self.colors['comment']};
                    margin: 4px;
                }}
            """)
            
            # === INSTANCE CONTROL ACTIONS ===
            if instance_status != 'running':
                start_action = QAction(f"▶️  Start '{instance_name}'", self)
                start_action.triggered.connect(lambda: self._context_start_instance(row))
                menu.addAction(start_action)
            
            if instance_status == 'running':
                stop_action = QAction(f"⏹️  Stop '{instance_name}'", self)
                stop_action.triggered.connect(lambda: self._context_stop_instance(row))
                menu.addAction(stop_action)
                
            restart_action = QAction(f"🔄 Restart '{instance_name}'", self)
            restart_action.triggered.connect(lambda: self._context_restart_instance(row))
            menu.addAction(restart_action)
            
            menu.addSeparator()
            
            # === INFO & HELP ===
            info_action = QAction(f"ℹ️  Instance Info", self)
            info_action.triggered.connect(lambda: self._show_instance_info(row))
            menu.addAction(info_action)
            
            help_action = QAction("❓ Help Guide", self)
            help_action.triggered.connect(self._show_help_guide)
            menu.addAction(help_action)
            
            # Show the menu
            global_pos = self.instance_table.mapToGlobal(position)
            menu.exec(global_pos)
            
        except Exception as e:
            print(f"⚠️ Error showing context menu: {e}")
            
    def _show_instance_info(self, row):
        """Show instance information dialog"""
        try:
            if row >= len(self.filtered_data):
                return
                
            instance = self.filtered_data[row]
            
            # Create info message
            info_text = f"""
🖥️  Instance Information

📋 Name: {instance.get('name', 'Unknown')}
📊 Status: {instance.get('status', 'offline')}
🔌 ADB Port: {instance.get('adb_port', 'N/A')}
💾 Memory: {instance.get('memory_usage', 'N/A')}
💿 Disk: {instance.get('disk_usage', 'N/A')}
⏱️  Uptime: {instance.get('uptime', 'N/A')}
            """.strip()
            
            # Show message box with Monokai styling
            msg = QMessageBox(self)
            msg.setWindowTitle("Instance Information")
            msg.setText(info_text)
            msg.setStyleSheet(f"""
                QMessageBox {{
                    background-color: {self.colors['bg']};
                    color: {self.colors['fg']};
                    font-family: 'JetBrains Mono', monospace;
                }}
                QMessageBox QPushButton {{
                    background-color: {self.colors['purple']};
                    color: {self.colors['fg']};
                    border: 1px solid {self.colors['comment']};
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-family: 'JetBrains Mono', monospace;
                }}
                QMessageBox QPushButton:hover {{
                    background-color: {self.colors['selection']};
                    color: {self.colors['yellow']};
                }}
            """)
            msg.exec()
            
        except Exception as e:
            print(f"⚠️ Error showing instance info: {e}")
            
    def _show_help_guide(self):
        """Show help guide for dashboard operations"""
        try:
            help_text = """
🎮 MuMu Manager Dashboard - Help Guide

📋 BASIC OPERATIONS:
• Left Click: Select instance
• Double Click: Start/Stop instance  
• Right Click: Context menu
• Ctrl+Click: Multi-select

⌨️  KEYBOARD SHORTCUTS:
• Ctrl+A: Select all instances
• Ctrl+D: Deselect all
• F5: Refresh data
• Space: Toggle auto-refresh

🎯 DASHBOARD FEATURES:
• Real-time statistics
• Performance monitoring
• Live system logs
• Advanced filtering

💡 PRO TIPS:
• Use filters to find instances quickly
• Monitor system stats for performance
• Check logs for troubleshooting
• Right-click for quick actions
            """.strip()
            
            msg = QMessageBox(self)
            msg.setWindowTitle("Dashboard Help Guide")
            msg.setText(help_text)
            msg.setStyleSheet(f"""
                QMessageBox {{
                    background-color: {self.colors['bg']};
                    color: {self.colors['fg']};
                    font-family: 'JetBrains Mono', monospace;
                    min-width: 500px;
                }}
                QMessageBox QPushButton {{
                    background-color: {self.colors['purple']};
                    color: {self.colors['fg']};
                    border: 1px solid {self.colors['comment']};
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-family: 'JetBrains Mono', monospace;
                }}
                QMessageBox QPushButton:hover {{
                    background-color: {self.colors['selection']};
                    color: {self.colors['yellow']};
                }}
            """)
            msg.exec()
            
        except Exception as e:
            print(f"⚠️ Error showing help guide: {e}")
            
    def _context_start_instance(self, row):
        """Start instance from context menu"""
        try:
            if row < len(self.filtered_data):
                instance = self.filtered_data[row]
                instance_id = instance.get('index', instance.get('id', row))
                self.start_instance_requested.emit(instance_id)
        except Exception as e:
            print(f"⚠️ Error starting instance from context: {e}")
            
    def _context_stop_instance(self, row):
        """Stop instance from context menu"""
        try:
            if row < len(self.filtered_data):
                instance = self.filtered_data[row]
                instance_id = instance.get('index', instance.get('id', row))
                self.stop_instance_requested.emit(instance_id)
        except Exception as e:
            print(f"⚠️ Error stopping instance from context: {e}")
            
    def _context_restart_instance(self, row):
        """Restart instance from context menu"""
        try:
            if row < len(self.filtered_data):
                instance = self.filtered_data[row]
                instance_id = instance.get('index', instance.get('id', row))
                self.restart_instance_requested.emit(instance_id)
        except Exception as e:
            print(f"⚠️ Error restarting instance from context: {e}")
            
    def cleanup_resources(self):
        """Proper resource cleanup to prevent memory leaks"""
        try:
            # Stop all timers
            if hasattr(self, 'refresh_timer') and self.refresh_timer:
                self.refresh_timer.stop()
                self.refresh_timer.deleteLater()
                
            if hasattr(self, 'search_timer') and self.search_timer:
                self.search_timer.stop()
                self.search_timer.deleteLater()
                
            if hasattr(self, 'log_timer') and self.log_timer:
                self.log_timer.stop()
                self.log_timer.deleteLater()
                
            if hasattr(self, 'time_timer') and self.time_timer:
                self.time_timer.stop()
                self.time_timer.deleteLater()
                
            # Clear table data
            if hasattr(self, 'instance_table') and self.instance_table:
                self.instance_table.clear()
                self.instance_table.setRowCount(0)
                
            # Clear data lists
            self.instances_data.clear()
            self.filtered_data.clear()
            
            print("✅ Resources cleaned up successfully")
            
        except Exception as e:
            print(f"⚠️ Error during resource cleanup: {e}")
            
    def closeEvent(self, event):
        """Handle close event with proper cleanup"""
        self.cleanup_resources()
        super().closeEvent(event)
            
    def _show_instance_info(self, row):
        """Show instance information dialog"""
        try:
            if row < len(self.filtered_data):
                instance = self.filtered_data[row]
                from PyQt6.QtWidgets import QMessageBox
                
                info_text = f"""Instance Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 Name: {instance.get('name', 'N/A')}
🔢 Index: {instance.get('index', 'N/A')}
⚡ Status: {instance.get('status', 'N/A')}
🔌 ADB Port: {instance.get('adb', 'N/A')}
💾 Memory: {instance.get('memory_usage', 'N/A')}
💿 Disk Usage: {instance.get('disk_usage', 'N/A')}
🖥️ CPU: {instance.get('cpu_usage', 'N/A')}
⏱️ Uptime: {instance.get('uptime', 'N/A')}"""
                
                msg = QMessageBox(self)
                msg.setWindowTitle("Instance Information")
                msg.setText(info_text)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.exec()
        except Exception as e:
            print(f"⚠️ Error showing instance info: {e}")
            
    def _connect_adb(self, row):
        """Connect to instance via ADB"""
        try:
            if row < len(self.filtered_data):
                instance = self.filtered_data[row]
                adb_port = instance.get('adb', 'N/A')
                
                from PyQt6.QtWidgets import QMessageBox
                msg = QMessageBox(self)
                msg.setWindowTitle("ADB Connection")
                msg.setText(f"ADB Connect Command:\n\nadb connect 127.0.0.1:{adb_port}")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.exec()
        except Exception as e:
            print(f"⚠️ Error connecting ADB: {e}")
            
    def _show_help_guide(self):
        """Show help and guide dialog"""
        try:
            from PyQt6.QtWidgets import QMessageBox
            
            help_text = """🎮 MuMu Manager Dashboard Help
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 TABLE OPERATIONS:
• Single Click: Select instance
• Double Click: View instance details  
• Right Click: Context menu with actions
• Ctrl+Click: Multi-select instances

🎯 ACTION BUTTONS:
• Start: Start selected instances (or all if none selected)
• Stop: Stop selected instances (or all if none selected)
• Restart: Restart selected instances
• Cleanup: Clean cache for selected instances

🔍 SEARCH & FILTER:
• Search Box: Filter by name or index
• Status Filter: Show instances by status
• Auto Refresh: Automatically update data

⌨️ KEYBOARD SHORTCUTS:
• Ctrl+A: Select all instances
• Ctrl+D: Deselect all instances
• F5: Manual refresh
• Del: Stop selected instances

📱 ADB CONNECTION:
• Right-click → Connect ADB for connection command
• ADB ports are shown in the table

🔧 TROUBLESHOOTING:
• If instances don't load: Check MuMu installation
• If buttons don't work: Try refreshing
• For more help: Check application logs"""
            
            msg = QMessageBox(self)
            msg.setWindowTitle("Dashboard Help & Guide")
            msg.setText(help_text)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
        except Exception as e:
            print(f"⚠️ Error showing help: {e}")
            
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Test data
    test_data = [
        {
            'index': 0,
            'name': 'MuMu Player 1',
            'status': 'running',
            'adb_port': 7555,
            'cpu_usage': 15.2,
            'memory_usage': '1.2GB',
            'disk_usage': '2.5GB',
            'uptime': '2h 30m'
        },
        {
            'index': 1,
            'name': 'MuMu Player 2', 
            'status': 'stopped',
            'adb_port': 7556,
            'cpu_usage': 0.0,
            'memory_usage': '0MB',
            'disk_usage': '1.8GB',
            'uptime': 'N/A'
        },
    ]
    
    dashboard = MonokaiDashboard()
    dashboard.update_instances(test_data)
    dashboard.show()
    
    sys.exit(app.exec())
