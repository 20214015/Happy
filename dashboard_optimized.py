"""
Dashboard Optimized - Tối ưu hóa bảng dashboard với Feather icons và hiệu suất cao
Tích hợp các tối ưu từ TABLE_PERFORMANCE_OPTIMIZATION.md
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QPushButton, QLineEdit, QComboBox, QSplitter,
    QGroupBox, QGridLayout, QProgressBar, QTextEdit, QAbstractItemView,
    QMenu, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QItemSelectionModel
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QPen, QBrush, QAction
import time
import psutil  # For system stats
import shutil  # For disk usage
from datetime import datetime
from typing import Dict, List, Any, Optional

# Import optimized Feather icon system
from feather_icons import get_icon, MONOKAI_COLORS

class OptimizedDashboard(QWidget):
    """Dashboard tối ưu với Feather icons và batch updates"""
    
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
        self.setObjectName("OptimizedDashboard")
        
        # Backend reference
        self.backend = None
        
        # Monokai Colors - Updated with Feather icon colors
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
            'red': '#F92672',          # Error red
        }
        
        # Data management
        self.instances_data = []
        self.filtered_data = []
        self.selected_instances = set()
        
        # Performance optimization
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._batch_update_table)
        self.update_timer.setSingleShot(True)
        self.pending_updates = {}  # {row: instance_data}
        self.row_mapping = {}  # {instance_id: row_index}
        
        # UI Components
        self.instance_table = None
        self.instances_model = None  # For compatibility
        
        # Setup UI
        self.setup_ui()
        self.apply_monokai_style()
        self.connect_signals()
        
        print("✅ OptimizedDashboard initialized with Feather icons and batch updates")
        
    def setup_ui(self):
        """Setup giao diện dashboard với Feather icons"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Header with stats và Feather icons
        header_frame = self.create_header_frame()
        layout.addWidget(header_frame)
        
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
        
    def create_header_frame(self):
        """Tạo header với thống kê và Feather icons"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QHBoxLayout(frame)
        
        # Title với icon
        title_layout = QHBoxLayout()
        
        # Dashboard icon
        dashboard_icon = QPushButton()
        dashboard_icon.setIcon(get_icon('dashboard'))
        dashboard_icon.setIconSize(dashboard_icon.size() * 1.2)
        dashboard_icon.setFlat(True)
        title_layout.addWidget(dashboard_icon)
        
        # Title
        title = QLabel("📊 MuMu Manager Dashboard")
        title.setFont(QFont("JetBrains Mono", 16, QFont.Weight.Bold))
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        # Stats section với Feather icons
        stats_layout = QHBoxLayout()
        
        # Total instances
        total_frame = self.create_stat_widget("apps", "Total", "0", self.colors['blue'])
        stats_layout.addWidget(total_frame)
        
        # Running instances  
        running_frame = self.create_stat_widget("play", "Running", "0", self.colors['green'])
        stats_layout.addWidget(running_frame)
        
        # Stopped instances
        stopped_frame = self.create_stat_widget("stop", "Stopped", "0", self.colors['pink'])
        stats_layout.addWidget(stopped_frame)
        
        layout.addLayout(stats_layout)
        
        # Store references
        self.total_label = total_frame.findChild(QLabel, "value")
        self.running_label = running_frame.findChild(QLabel, "value")
        self.stopped_label = stopped_frame.findChild(QLabel, "value")
        
        return frame
        
    def create_stat_widget(self, icon_name: str, label: str, value: str, color: str):
        """Tạo widget thống kê với Feather icon"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Icon
        icon_btn = QPushButton()
        icon_btn.setIcon(get_icon(icon_name, color))
        icon_btn.setIconSize(icon_btn.size())
        icon_btn.setFlat(True)
        layout.addWidget(icon_btn)
        
        # Text
        text_layout = QVBoxLayout()
        label_widget = QLabel(label)
        label_widget.setFont(QFont("JetBrains Mono", 9))
        
        value_widget = QLabel(value)
        value_widget.setObjectName("value")
        value_widget.setFont(QFont("JetBrains Mono", 12, QFont.Weight.Bold))
        value_widget.setStyleSheet(f"color: {color};")
        
        text_layout.addWidget(label_widget)
        text_layout.addWidget(value_widget)
        layout.addLayout(text_layout)
        
        return frame
        
    def create_left_panel(self):
        """Tạo panel trái với bảng instances tối ưu"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Controls với Feather icons
        controls_layout = self.create_controls_layout()
        layout.addLayout(controls_layout)
        
        # Optimized table
        self.create_optimized_table()
        layout.addWidget(self.instance_table)
        
        return widget
        
    def create_controls_layout(self):
        """Tạo controls với Feather icons"""
        layout = QHBoxLayout()
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.setIcon(get_icon('refresh'))
        refresh_btn.clicked.connect(self.refresh_instances)
        layout.addWidget(refresh_btn)
        
        # Start All button
        start_all_btn = QPushButton("Start All")
        start_all_btn.setIcon(get_icon('play'))
        start_all_btn.clicked.connect(lambda: self.start_all_requested.emit())
        layout.addWidget(start_all_btn)
        
        # Stop All button
        stop_all_btn = QPushButton("Stop All")
        stop_all_btn.setIcon(get_icon('stop'))
        stop_all_btn.clicked.connect(lambda: self.stop_all_requested.emit())
        layout.addWidget(stop_all_btn)
        
        layout.addStretch()
        
        # Search filter
        search_label = QLabel("🔍 Filter:")
        search_label.setFont(QFont("JetBrains Mono", 9))
        layout.addWidget(search_label)
        
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search instances...")
        self.search_box.textChanged.connect(self.filter_instances)
        layout.addWidget(self.search_box)
        
        return layout
        
    def create_optimized_table(self):
        """Tạo bảng tối ưu với batch updates"""
        self.instance_table = QTableWidget()
        
        # Setup columns
        headers = ["#", "Name", "Status", "ADB Port", "CPU %", "Memory", "Disk", "Uptime"]
        self.instance_table.setColumnCount(len(headers))
        self.instance_table.setHorizontalHeaderLabels(headers)
        
        # Table settings
        self.instance_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.instance_table.setAlternatingRowColors(True)
        self.instance_table.setSortingEnabled(True)
        
        # Header settings
        header = self.instance_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        
        # Context menu
        self.instance_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.instance_table.customContextMenuRequested.connect(self.show_context_menu)
        
        # Selection changed
        self.instance_table.itemSelectionChanged.connect(self.on_selection_changed)
        
    def create_right_panel(self):
        """Tạo panel phải với monitoring"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # System info
        system_group = QGroupBox("💻 System Info")
        system_layout = QGridLayout(system_group)
        
        # CPU usage với icon
        cpu_layout = QHBoxLayout()
        cpu_layout.addWidget(QPushButton())  # CPU icon placeholder
        self.cpu_progress = QProgressBar()
        self.cpu_progress.setRange(0, 100)
        cpu_layout.addWidget(self.cpu_progress)
        system_layout.addLayout(cpu_layout, 0, 0)
        
        # Memory usage với icon  
        mem_layout = QHBoxLayout()
        mem_layout.addWidget(QPushButton())  # Memory icon placeholder
        self.mem_progress = QProgressBar()
        self.mem_progress.setRange(0, 100)
        mem_layout.addWidget(self.mem_progress)
        system_layout.addLayout(mem_layout, 1, 0)
        
        layout.addWidget(system_group)
        
        # Logs
        logs_group = QGroupBox("📋 Activity Logs")
        logs_layout = QVBoxLayout(logs_group)
        
        self.logs_text = QTextEdit()
        self.logs_text.setMaximumHeight(200)
        self.logs_text.setReadOnly(True)
        logs_layout.addWidget(self.logs_text)
        
        layout.addWidget(logs_group)
        layout.addStretch()
        
        return widget
        
    def show_context_menu(self, position):
        """Hiển thị context menu với Feather icons"""
        if not self.instance_table.itemAt(position):
            return
            
        menu = QMenu(self)
        
        # Start action
        start_action = QAction(get_icon('play'), "Start", self)
        start_action.triggered.connect(self.start_selected_instance)
        menu.addAction(start_action)
        
        # Stop action
        stop_action = QAction(get_icon('stop'), "Stop", self)
        stop_action.triggered.connect(self.stop_selected_instance)
        menu.addAction(stop_action)
        
        # Restart action
        restart_action = QAction(get_icon('restart'), "Restart", self)
        restart_action.triggered.connect(self.restart_selected_instance)
        menu.addAction(restart_action)
        
        menu.addSeparator()
        
        # Delete action
        delete_action = QAction(get_icon('delete'), "Delete", self)
        delete_action.triggered.connect(self.delete_selected_instance)
        menu.addAction(delete_action)
        
        menu.exec(self.instance_table.mapToGlobal(position))
        
    def connect_signals(self):
        """Kết nối signals"""
        # Performance update timer
        self.update_timer.timeout.connect(self._batch_update_table)
        
    # === OPTIMIZATION METHODS ===
    
    def schedule_table_update(self, instance_data: List[Dict[str, Any]]):
        """Schedule batch table update (Performance optimization)"""
        # Update row mapping for O(1) lookups
        for i, instance in enumerate(instance_data):
            instance_id = instance.get('index', i)
            self.row_mapping[instance_id] = i
            self.pending_updates[i] = instance
            
        # Start batch timer (50ms delay for batching)
        if not self.update_timer.isActive():
            self.update_timer.start(50)
            
    def _batch_update_table(self):
        """Perform batch table update (Performance optimization)"""
        if not self.pending_updates:
            return
            
        # Disable sorting during update
        self.instance_table.setSortingEnabled(False)
        
        try:
            # Set row count once
            max_row = max(self.pending_updates.keys()) + 1 if self.pending_updates else 0
            self.instance_table.setRowCount(max_row)
            
            # Batch update all pending changes
            for row, instance in self.pending_updates.items():
                self._update_table_row(row, instance)
                
        except Exception as e:
            print(f"⚠️ Error in batch table update: {e}")
        finally:
            # Re-enable sorting
            self.instance_table.setSortingEnabled(True)
            self.pending_updates.clear()
            
    def _update_table_row(self, row: int, instance: Dict[str, Any]):
        """Update single table row efficiently"""
        try:
            # Index
            index_item = QTableWidgetItem(str(instance.get('index', row + 1)))
            index_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.instance_table.setItem(row, 0, index_item)
            
            # Name
            name_item = QTableWidgetItem(instance.get('name', f'MuMu-{row}'))
            self.instance_table.setItem(row, 1, name_item)
            
            # Status with Feather icon colors
            status = instance.get('status', 'offline')
            if status == 'running':
                status_display = "▶️ Running"
                status_color = MONOKAI_COLORS['green']
            elif status == 'starting':
                status_display = "⏸️ Starting"
                status_color = MONOKAI_COLORS['yellow']
            else:
                status_display = "⏹️ Stopped"
                status_color = MONOKAI_COLORS['pink']
                
            status_item = QTableWidgetItem(status_display)
            status_item.setForeground(QColor(status_color))
            self.instance_table.setItem(row, 2, status_item)
            
            # ADB Port
            adb_port = instance.get('adb_port', 'N/A')
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
            print(f"⚠️ Error updating row {row}: {e}")
            
    # === PUBLIC INTERFACE ===
    
    def update_instances(self, instances_data: List[Dict[str, Any]]):
        """Update instances với batch optimization"""
        self.instances_data = instances_data.copy()
        self.filter_instances()  # Apply current filter
        self.update_stats()
        
        # Use optimized batch update
        self.schedule_table_update(self.filtered_data)
        
        # Log update
        self.add_log(f"✅ Updated {len(instances_data)} instances (batch optimized)")
        
    def filter_instances(self):
        """Filter instances theo search text"""
        search_text = getattr(self, 'search_box', None)
        if search_text:
            search_text = search_text.text().lower()
        else:
            search_text = ""
            
        if not search_text:
            self.filtered_data = self.instances_data.copy()
        else:
            self.filtered_data = [
                instance for instance in self.instances_data
                if search_text in instance.get('name', '').lower()
                or search_text in instance.get('status', '').lower()
            ]
            
        # Update display với batch optimization
        if hasattr(self, 'instance_table'):
            self.schedule_table_update(self.filtered_data)
            
    def update_stats(self):
        """Cập nhật thống kê với performance optimization"""
        total = len(self.instances_data)
        running = sum(1 for i in self.instances_data if i.get('status') == 'running')
        stopped = total - running
        
        # Update header stats
        if hasattr(self, 'total_label'):
            self.total_label.setText(str(total))
            self.running_label.setText(str(running))
            self.stopped_label.setText(str(stopped))
        
        # Update system stats
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            
            if hasattr(self, 'cpu_progress'):
                self.cpu_progress.setValue(int(cpu_percent))
                self.mem_progress.setValue(int(memory.percent))
                
        except Exception as e:
            print(f"⚠️ Error updating system stats: {e}")
            
    def add_log(self, message: str):
        """Thêm log message"""
        if hasattr(self, 'logs_text'):
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.logs_text.append(f"[{timestamp}] {message}")
            
    # === EVENT HANDLERS ===
    
    def on_selection_changed(self):
        """Handle table selection changes"""
        selected_rows = set()
        for item in self.instance_table.selectedItems():
            selected_rows.add(item.row())
            
        self.selected_instances = selected_rows
        
        # Emit signal for first selected instance
        if selected_rows:
            first_row = min(selected_rows)
            if first_row < len(self.filtered_data):
                instance_index = self.filtered_data[first_row].get('index', first_row)
                self.instance_selected.emit(instance_index)
                
    def refresh_instances(self):
        """Trigger refresh"""
        self.refresh_requested.emit()
        self.add_log("🔄 Refreshing instances...")
        
    def start_selected_instance(self):
        """Start selected instance"""
        if self.selected_instances:
            row = min(self.selected_instances)
            if row < len(self.filtered_data):
                instance_index = self.filtered_data[row].get('index', row)
                self.start_instance_requested.emit(instance_index)
                
    def stop_selected_instance(self):
        """Stop selected instance"""
        if self.selected_instances:
            row = min(self.selected_instances)
            if row < len(self.filtered_data):
                instance_index = self.filtered_data[row].get('index', row)
                self.stop_instance_requested.emit(instance_index)
                
    def restart_selected_instance(self):
        """Restart selected instance"""
        if self.selected_instances:
            row = min(self.selected_instances)
            if row < len(self.filtered_data):
                instance_index = self.filtered_data[row].get('index', row)
                self.restart_instance_requested.emit(instance_index)
                
    def delete_selected_instance(self):
        """Delete selected instance"""
        if self.selected_instances:
            row = min(self.selected_instances)
            if row < len(self.filtered_data):
                instance_index = self.filtered_data[row].get('index', row)
                
                # Confirm deletion
                reply = QMessageBox.question(
                    self, 'Confirm Delete',
                    f'Are you sure you want to delete instance {instance_index}?',
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    self.cleanup_requested.emit([instance_index])
                    
    def apply_monokai_style(self):
        """Áp dụng Monokai style tối ưu"""
        style = f"""
        OptimizedDashboard {{
            background-color: {self.colors['bg']};
            color: {self.colors['fg']};
            font-family: 'JetBrains Mono', 'Consolas', monospace;
        }}
        QTableWidget {{
            background-color: {self.colors['bg_alt']};
            color: {self.colors['fg']};
            gridline-color: #49483E;
            selection-background-color: {self.colors['blue']};
            selection-color: {self.colors['bg']};
            border: 1px solid #49483E;
        }}
        QTableWidget::item {{
            padding: 8px;
            border-bottom: 1px solid #3C3B37;
        }}
        QTableWidget::item:selected {{
            background-color: {self.colors['blue']};
            color: {self.colors['bg']};
        }}
        QHeaderView::section {{
            background-color: {self.colors['bg_alt']};
            color: {self.colors['orange']};
            padding: 8px;
            border: 1px solid #49483E;
            font-weight: bold;
        }}
        QPushButton {{
            background-color: {self.colors['bg_alt']};
            border: 1px solid #49483E;
            padding: 8px 16px;
            color: {self.colors['fg']};
            border-radius: 4px;
        }}
        QPushButton:hover {{
            background-color: #49483E;
        }}
        QPushButton:pressed {{
            background-color: {self.colors['blue']};
        }}
        QLineEdit {{
            background-color: {self.colors['bg_alt']};
            border: 1px solid #49483E;
            padding: 6px;
            color: {self.colors['fg']};
            border-radius: 4px;
        }}
        QGroupBox {{
            color: {self.colors['orange']};
            border: 2px solid #49483E;
            border-radius: 6px;
            margin-top: 1ex;
            font-weight: bold;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }}
        QProgressBar {{
            border: 1px solid #49483E;
            border-radius: 4px;
            text-align: center;
            background-color: {self.colors['bg_alt']};
        }}
        QProgressBar::chunk {{
            background-color: {self.colors['green']};
            border-radius: 3px;
        }}
        QTextEdit {{
            background-color: {self.colors['bg_alt']};
            color: {self.colors['fg']};
            border: 1px solid #49483E;
            border-radius: 4px;
        }}
        QFrame {{
            border: 1px solid #49483E;
            border-radius: 4px;
            background-color: {self.colors['bg_alt']};
        }}
        """
        self.setStyleSheet(style)


# Test function
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
    
    dashboard = OptimizedDashboard()
    dashboard.update_instances(test_data)
    dashboard.show()
    
    sys.exit(app.exec())