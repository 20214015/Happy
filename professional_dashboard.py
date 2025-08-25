"""
Professional Dashboard - Modern Business Interface
===============================================

Clean, professional dashboard component designed for business applications.
Replaces the coding-style Monokai dashboard with modern UI patterns.

Author: GitHub Copilot
Date: January 2024
Version: 1.0 - Professional Edition
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableView, 
    QHeaderView, QFrame, QPushButton, QLineEdit, QComboBox, QSplitter,
    QGroupBox, QGridLayout, QProgressBar, QTextEdit, QAbstractItemView,
    QScrollArea, QStackedWidget
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QItemSelectionModel, QSize
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor

# Import professional components
try:
    from professional_icons import get_professional_icon, get_status_icon, create_button_icon
    PROFESSIONAL_ICONS_AVAILABLE = True
except ImportError:
    PROFESSIONAL_ICONS_AVAILABLE = False

# Core components
try:
    from core import get_state_manager
    from widgets import InstancesModel, InstancesProxy, StatusPillDelegate
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False

class ProfessionalDashboard(QWidget):
    """Professional dashboard with modern business aesthetics"""
    
    # Signals
    instance_selected = pyqtSignal(str)
    action_requested = pyqtSignal(str, list)
    refresh_requested = pyqtSignal()
    
    def __init__(self, parent=None, backend_manager=None):
        super().__init__(parent)
        self.backend_manager = backend_manager
        self.auto_refresh_timer = QTimer()
        self.auto_refresh_enabled = False
        
        # Initialize UI components
        self.search_edit = None
        self.filter_combo = None
        self.refresh_btn = None
        self.btn_auto_refresh = None
        self.btn_select_all = None
        self.btn_deselect_all = None
        self.instance_table = None
        self.instances_model = None
        self.instances_proxy = None
        self.status_label = None
        self.performance_widget = None
        
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        """Initialize the professional UI"""
        self.setObjectName("ProfessionalDashboard")
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Header section
        header_widget = self.create_header_section()
        layout.addWidget(header_widget)
        
        # Control section
        controls_widget = self.create_controls_section()
        layout.addWidget(controls_widget)
        
        # Main content area
        content_widget = self.create_content_section()
        layout.addWidget(content_widget, 1)
        
        # Status section
        status_widget = self.create_status_section()
        layout.addWidget(status_widget)
        
        # Apply professional styling
        self.apply_professional_styling()
        
    def create_header_section(self) -> QWidget:
        """Create professional header with title and overview"""
        header_frame = QFrame()
        header_frame.setObjectName("HeaderFrame")
        header_frame.setFixedHeight(80)
        
        layout = QHBoxLayout(header_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title and description
        title_layout = QVBoxLayout()
        
        title_label = QLabel("Instance Manager")
        title_label.setObjectName("HeaderTitle")
        title_label.setProperty("styleClass", "heading")
        title_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Manage and monitor your MuMu Android emulator instances")
        subtitle_label.setProperty("styleClass", "subheading")
        title_layout.addWidget(subtitle_label)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Quick stats
        stats_widget = self.create_quick_stats()
        layout.addWidget(stats_widget)
        
        return header_frame
        
    def create_quick_stats(self) -> QWidget:
        """Create quick statistics display"""
        stats_frame = QFrame()
        stats_frame.setObjectName("StatsFrame")
        
        layout = QHBoxLayout(stats_frame)
        layout.setSpacing(16)
        
        # Total instances
        total_widget = self.create_stat_item("Total", "0", "instances")
        layout.addWidget(total_widget)
        
        # Running instances  
        running_widget = self.create_stat_item("Running", "0", "success")
        layout.addWidget(running_widget)
        
        # Stopped instances
        stopped_widget = self.create_stat_item("Stopped", "0", "secondary")
        layout.addWidget(stopped_widget)
        
        return stats_frame
        
    def create_stat_item(self, label: str, value: str, variant: str = "primary") -> QWidget:
        """Create individual statistic item"""
        item_frame = QFrame()
        item_frame.setObjectName(f"StatItem{variant.title()}")
        item_frame.setFixedSize(80, 60)
        
        layout = QVBoxLayout(item_frame)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(2)
        
        # Value
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {self.get_color_for_variant(variant)};
        """)
        layout.addWidget(value_label)
        
        # Label
        label_label = QLabel(label)
        label_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_label.setProperty("styleClass", "muted")
        layout.addWidget(label_label)
        
        return item_frame
        
    def get_color_for_variant(self, variant: str) -> str:
        """Get color for UI variant"""
        colors = {
            "primary": "#3B82F6",
            "success": "#10B981", 
            "warning": "#F59E0B",
            "danger": "#EF4444",
            "secondary": "#6B7280"
        }
        return colors.get(variant, colors["primary"])
        
    def create_controls_section(self) -> QWidget:
        """Create control section with search and action buttons"""
        controls_frame = QFrame()
        controls_frame.setObjectName("ControlsFrame")
        controls_frame.setFixedHeight(60)
        
        layout = QHBoxLayout(controls_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Search section
        search_layout = QHBoxLayout()
        search_layout.setSpacing(8)
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search instances by name or ID...")
        self.search_edit.setMinimumWidth(300)
        search_layout.addWidget(self.search_edit)
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All Instances", "Running", "Stopped", "Starting", "Error"])
        self.filter_combo.setMinimumWidth(150)
        search_layout.addWidget(self.filter_combo)
        
        layout.addLayout(search_layout)
        layout.addStretch()
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(8)
        
        # Refresh button
        self.refresh_btn = QPushButton("Refresh")
        if PROFESSIONAL_ICONS_AVAILABLE:
            self.refresh_btn.setIcon(get_professional_icon("refresh"))
        self.refresh_btn.setProperty("variant", "secondary")
        action_layout.addWidget(self.refresh_btn)
        
        # Auto refresh toggle
        self.btn_auto_refresh = QPushButton("Auto Refresh")
        if PROFESSIONAL_ICONS_AVAILABLE:
            self.btn_auto_refresh.setIcon(get_professional_icon("sync"))
        self.btn_auto_refresh.setCheckable(True)
        self.btn_auto_refresh.setProperty("variant", "info")
        action_layout.addWidget(self.btn_auto_refresh)
        
        # Selection buttons
        self.btn_select_all = QPushButton("Select All")
        if PROFESSIONAL_ICONS_AVAILABLE:
            self.btn_select_all.setIcon(get_professional_icon("select_all"))
        self.btn_select_all.setProperty("variant", "secondary")
        action_layout.addWidget(self.btn_select_all)
        
        self.btn_deselect_all = QPushButton("Clear Selection")
        if PROFESSIONAL_ICONS_AVAILABLE:
            self.btn_deselect_all.setIcon(get_professional_icon("select_none"))
        self.btn_deselect_all.setProperty("variant", "secondary")
        action_layout.addWidget(self.btn_deselect_all)
        
        layout.addLayout(action_layout)
        
        return controls_frame
        
    def create_content_section(self) -> QWidget:
        """Create main content area with instance table"""
        content_widget = QSplitter(Qt.Orientation.Horizontal)
        
        # Main table area
        table_widget = self.create_instance_table()
        content_widget.addWidget(table_widget)
        
        # Side panel for details/actions
        side_panel = self.create_side_panel()
        content_widget.addWidget(side_panel)
        
        # Set splitter proportions
        content_widget.setSizes([700, 300])
        
        return content_widget
        
    def create_instance_table(self) -> QWidget:
        """Create professional instance table"""
        table_container = QFrame()
        table_container.setObjectName("TableContainer")
        
        layout = QVBoxLayout(table_container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Table header
        table_header = QLabel("Instance Overview")
        table_header.setProperty("styleClass", "subheading")
        layout.addWidget(table_header)
        
        # Create table
        self.instance_table = QTableView()
        self.instance_table.setObjectName("InstanceTable")
        self.instance_table.setAlternatingRowColors(True)
        self.instance_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.instance_table.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.instance_table.setSortingEnabled(True)
        
        # Configure headers
        self.instance_table.horizontalHeader().setStretchLastSection(True)
        self.instance_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.instance_table.verticalHeader().setVisible(False)
        
        # Setup model if available
        if CORE_AVAILABLE:
            try:
                self.instances_model = InstancesModel(self)
                self.instances_proxy = InstancesProxy(self)
                self.instances_proxy.setSourceModel(self.instances_model)
                self.instance_table.setModel(self.instances_proxy)
                
                # Set custom delegate for status display
                delegate = StatusPillDelegate()
                self.instance_table.setItemDelegate(delegate)
            except Exception as e:
                print(f"Warning: Could not setup instance model: {e}")
        
        layout.addWidget(self.instance_table)
        
        return table_container
        
    def create_side_panel(self) -> QWidget:
        """Create side panel with actions and details"""
        side_panel = QFrame()
        side_panel.setObjectName("SidePanel")
        side_panel.setFixedWidth(280)
        
        layout = QVBoxLayout(side_panel)
        layout.setContentsMargins(16, 0, 0, 0)
        layout.setSpacing(16)
        
        # Quick Actions section
        actions_group = QGroupBox("Quick Actions")
        actions_layout = QGridLayout(actions_group)
        actions_layout.setSpacing(8)
        
        # Action buttons with professional styling
        start_btn = QPushButton("Start Instance")
        if PROFESSIONAL_ICONS_AVAILABLE:
            start_btn.setIcon(create_button_icon("start", "success"))
        start_btn.setProperty("variant", "success")
        actions_layout.addWidget(start_btn, 0, 0)
        
        stop_btn = QPushButton("Stop Instance")
        if PROFESSIONAL_ICONS_AVAILABLE:
            stop_btn.setIcon(create_button_icon("stop", "danger"))
        stop_btn.setProperty("variant", "danger")
        actions_layout.addWidget(stop_btn, 0, 1)
        
        restart_btn = QPushButton("Restart")
        if PROFESSIONAL_ICONS_AVAILABLE:
            restart_btn.setIcon(create_button_icon("restart", "warning"))
        restart_btn.setProperty("variant", "warning")
        actions_layout.addWidget(restart_btn, 1, 0)
        
        config_btn = QPushButton("Configure")
        if PROFESSIONAL_ICONS_AVAILABLE:
            config_btn.setIcon(create_button_icon("config", "secondary"))
        config_btn.setProperty("variant", "secondary")
        actions_layout.addWidget(config_btn, 1, 1)
        
        layout.addWidget(actions_group)
        
        # Instance Details section
        details_group = QGroupBox("Instance Details")
        details_layout = QVBoxLayout(details_group)
        
        self.details_text = QTextEdit()
        self.details_text.setMaximumHeight(150)
        self.details_text.setPlaceholderText("Select an instance to view details...")
        details_layout.addWidget(self.details_text)
        
        layout.addWidget(details_group)
        
        # Performance Monitor section
        self.performance_widget = self.create_performance_widget()
        layout.addWidget(self.performance_widget)
        
        layout.addStretch()
        
        return side_panel
        
    def create_performance_widget(self) -> QWidget:
        """Create performance monitoring widget"""
        perf_group = QGroupBox("System Monitor")
        layout = QVBoxLayout(perf_group)
        layout.setSpacing(8)
        
        # CPU Usage
        cpu_layout = QHBoxLayout()
        cpu_label = QLabel("CPU:")
        cpu_layout.addWidget(cpu_label)
        
        self.cpu_progress = QProgressBar()
        self.cpu_progress.setMaximum(100)
        self.cpu_progress.setValue(0)
        cpu_layout.addWidget(self.cpu_progress)
        
        layout.addLayout(cpu_layout)
        
        # Memory Usage
        mem_layout = QHBoxLayout()
        mem_label = QLabel("Memory:")
        mem_layout.addWidget(mem_label)
        
        self.memory_progress = QProgressBar()
        self.memory_progress.setMaximum(100)
        self.memory_progress.setValue(0)
        mem_layout.addWidget(self.memory_progress)
        
        layout.addLayout(mem_layout)
        
        return perf_group
        
    def create_status_section(self) -> QWidget:
        """Create status bar section"""
        status_frame = QFrame()
        status_frame.setObjectName("StatusFrame")
        status_frame.setFixedHeight(32)
        
        layout = QHBoxLayout(status_frame)
        layout.setContentsMargins(0, 8, 0, 8)
        
        self.status_label = QLabel("Ready")
        self.status_label.setProperty("styleClass", "muted")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        # Connection status
        self.connection_status = QLabel("Disconnected")
        self.connection_status.setProperty("styleClass", "muted")
        layout.addWidget(self.connection_status)
        
        return status_frame
        
    def setup_connections(self):
        """Setup signal connections"""
        if hasattr(self, 'search_edit') and self.search_edit:
            self.search_edit.textChanged.connect(self.on_search_changed)
            
        if hasattr(self, 'filter_combo') and self.filter_combo:
            self.filter_combo.currentTextChanged.connect(self.on_filter_changed)
            
        if hasattr(self, 'refresh_btn') and self.refresh_btn:
            self.refresh_btn.clicked.connect(self.refresh_instances)
            
        if hasattr(self, 'btn_auto_refresh') and self.btn_auto_refresh:
            self.btn_auto_refresh.toggled.connect(self.toggle_auto_refresh)
            
        if hasattr(self, 'btn_select_all') and self.btn_select_all:
            self.btn_select_all.clicked.connect(self.select_all_instances)
            
        if hasattr(self, 'btn_deselect_all') and self.btn_deselect_all:
            self.btn_deselect_all.clicked.connect(self.clear_selection)
            
        # Auto refresh timer
        self.auto_refresh_timer.timeout.connect(self.refresh_instances)
        
    def apply_professional_styling(self):
        """Apply professional styling to the dashboard"""
        self.setStyleSheet("""
            #ProfessionalDashboard {
                background-color: #FFFFFF;
            }
            
            #HeaderFrame {
                background-color: #F8FAFC;
                border-radius: 12px;
                border: 1px solid #E2E8F0;
            }
            
            #HeaderTitle {
                font-size: 24px;
                font-weight: bold;
                color: #1E293B;
            }
            
            #ControlsFrame {
                background-color: transparent;
                border-bottom: 1px solid #E2E8F0;
                padding: 12px 0;
            }
            
            #TableContainer {
                background-color: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
            }
            
            #InstanceTable {
                background-color: #FFFFFF;
                alternate-background-color: #F8FAFC;
                selection-background-color: #EBF8FF;
                selection-color: #1E293B;
                border: none;
                border-radius: 8px;
            }
            
            #SidePanel {
                background-color: #F8FAFC;
                border-left: 1px solid #E2E8F0;
            }
            
            #StatusFrame {
                background-color: #F8FAFC;
                border-top: 1px solid #E2E8F0;
            }
            
            #StatsFrame {
                background-color: transparent;
            }
            
            QGroupBox {
                font-weight: 600;
                color: #374151;
                border: 1px solid #E2E8F0;
                border-radius: 8px;
                margin-top: 8px;
                padding-top: 12px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 8px;
                background-color: #F8FAFC;
            }
        """)
        
    # Event handlers
    def on_search_changed(self, text: str):
        """Handle search text changes"""
        if hasattr(self, 'instances_proxy') and self.instances_proxy:
            self.instances_proxy.setFilterFixedString(text)
        
    def on_filter_changed(self, filter_text: str):
        """Handle filter changes"""
        # Apply status filter to proxy model
        if hasattr(self, 'instances_proxy') and self.instances_proxy:
            if filter_text == "All Instances":
                self.instances_proxy.setFilterFixedString("")
            else:
                self.instances_proxy.setFilterFixedString(filter_text.lower())
                
    def refresh_instances(self):
        """Refresh instance data"""
        self.status_label.setText("Refreshing instances...")
        self.refresh_requested.emit()
        
        # Update status after delay
        QTimer.singleShot(1000, lambda: self.status_label.setText("Ready"))
        
    def toggle_auto_refresh(self, enabled: bool):
        """Toggle auto refresh functionality"""
        self.auto_refresh_enabled = enabled
        
        if enabled:
            self.auto_refresh_timer.start(5000)  # 5 second intervals
            self.status_label.setText("Auto refresh enabled")
        else:
            self.auto_refresh_timer.stop()
            self.status_label.setText("Auto refresh disabled")
            
    def select_all_instances(self):
        """Select all instances in table"""
        if hasattr(self, 'instance_table') and self.instance_table:
            self.instance_table.selectAll()
            
    def clear_selection(self):
        """Clear instance selection"""
        if hasattr(self, 'instance_table') and self.instance_table:
            self.instance_table.clearSelection()
            
    def update_status(self, message: str):
        """Update status message"""
        if hasattr(self, 'status_label') and self.status_label:
            self.status_label.setText(message)
            
    def update_performance(self, cpu_usage: float, memory_usage: float):
        """Update performance indicators"""
        if hasattr(self, 'cpu_progress'):
            self.cpu_progress.setValue(int(cpu_usage))
        if hasattr(self, 'memory_progress'):
            self.memory_progress.setValue(int(memory_usage))
            
    def get_ui_components(self) -> dict:
        """Get UI components for compatibility with existing code"""
        return {
            'search_edit': self.search_edit,
            'filter_combo': self.filter_combo,
            'refresh_btn': self.refresh_btn,
            'btn_auto_refresh': self.btn_auto_refresh,
            'btn_select_all': self.btn_select_all,
            'btn_deselect_all': self.btn_deselect_all,
            'table': self.instance_table,
            'instances_model': self.instances_model,
            'instances_proxy': self.instances_proxy,
            'ai_tracker_status': self.status_label
        }

# Factory function for component creation
def create_professional_dashboard(parent=None, backend_manager=None):
    """Factory function to create professional dashboard"""
    return ProfessionalDashboard(parent, backend_manager)

# Demo function
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Apply professional theme
    try:
        from professional_theme import apply_professional_theme
        apply_professional_theme(app)
    except ImportError:
        pass
    
    dashboard = ProfessionalDashboard()
    dashboard.show()
    
    sys.exit(app.exec())