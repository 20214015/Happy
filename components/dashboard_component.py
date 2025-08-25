"""
Dashboard Component Module
=========================

Extracted dashboard logic from main_window.py để modularize và improve maintainability.
"""

import time
from typing import Optional, Dict, Any
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QComboBox, QPushButton, QTableWidget)
from PyQt6.QtCore import pyqtSignal, QObject

# Optimization imports
try:
    from services import get_service_manager
    from core import get_event_manager, EventTypes, emit_event
    OPTIMIZATION_AVAILABLE = True
except ImportError:
    OPTIMIZATION_AVAILABLE = False

# Professional dashboard import (NEW)
try:
    from professional_dashboard import ProfessionalDashboard, create_professional_dashboard
    PROFESSIONAL_DASHBOARD_AVAILABLE = True
    print("✅ Professional dashboard available")
except ImportError:
    PROFESSIONAL_DASHBOARD_AVAILABLE = False
    print("⚠️ Professional dashboard not available")

# Monokai dashboard import (DEPRECATED - will be removed)
try:
    from dashboard_monokai_refactored import MonokaiDashboard
    MONOKAI_AVAILABLE = True
    print("⚠️ Monokai dashboard available (deprecated)")
except ImportError:
    MONOKAI_AVAILABLE = False

class DashboardComponent(QObject):
    """
    Modular Dashboard Component sử dụng optimization architecture.
    
    Features:
    - ServiceManager integration cho dependency management
    - EventManager cho component communication
    - StateManager cho centralized state
    - Fallback mechanisms cho compatibility
    """
    
    # Signals for communication
    dashboard_created = pyqtSignal(QWidget)
    search_changed = pyqtSignal(str)
    filter_changed = pyqtSignal(str)
    refresh_requested = pyqtSignal()
    selection_changed = pyqtSignal(bool)  # True = select all, False = deselect all
    
    def __init__(self, parent_window, backend_manager):
        super().__init__()
        self.parent_window = parent_window
        self.backend_manager = backend_manager
        self.widget = None
        self.dashboard_widget = None
        
        # Optimization components
        if OPTIMIZATION_AVAILABLE:
            self.service_manager = get_service_manager()
            self.event_manager = get_event_manager()
            
            # Subscribe to events
            self.event_manager.subscribe(EventTypes.UI_REFRESH_REQUESTED, self._handle_refresh_event)
            self.event_manager.subscribe(EventTypes.SEARCH_QUERY_CHANGED, self._handle_search_event)
        
        # UI components
        self.search_edit: Optional[QLineEdit] = None
        self.filter_combo: Optional[QComboBox] = None
        self.refresh_btn: Optional[QPushButton] = None
        self.btn_auto_refresh: Optional[QPushButton] = None
        self.btn_select_all: Optional[QPushButton] = None
        self.btn_deselect_all: Optional[QPushButton] = None
        self.ai_tracker_status: Optional[QLabel] = None
        self.table: Optional[QTableWidget] = None
        self.instances_model = None
        self.instances_proxy = None
        
    def create_dashboard(self) -> QWidget:
        """Create dashboard widget with professional design priority"""
        
        # Try NEW Professional dashboard first (PRIORITY)
        if PROFESSIONAL_DASHBOARD_AVAILABLE:
            try:
                dashboard = self._create_professional_dashboard()
                if dashboard:
                    self.widget = dashboard
                    self.dashboard_created.emit(dashboard)
                    print("✅ Professional dashboard created successfully")
                    return dashboard
            except Exception as e:
                print(f"⚠️ Professional dashboard creation failed: {e}")
        
        # Fallback to deprecated Monokai dashboard (for compatibility)
        if MONOKAI_AVAILABLE:
            try:
                dashboard = self._create_monokai_dashboard()
                if dashboard:
                    self.widget = dashboard
                    self.dashboard_created.emit(dashboard)
                    print("⚠️ Using deprecated Monokai dashboard")
                    return dashboard
            except Exception as e:
                print(f"⚠️ Monokai dashboard creation failed: {e}")
        
        # Final fallback to standard dashboard
        dashboard = self._create_standard_dashboard()
        self.widget = dashboard
        self.dashboard_created.emit(dashboard)
        print("⚠️ Using basic fallback dashboard")
        return dashboard
    
    def _create_professional_dashboard(self) -> Optional[QWidget]:
        """Create NEW professional dashboard with modern design"""
        try:
            self.dashboard_widget = create_professional_dashboard(
                parent=self.parent_window, 
                backend_manager=self.backend_manager
            )
            
            # Extract UI components for compatibility
            self._extract_professional_components()
            
            # Connect optimization events if available
            if OPTIMIZATION_AVAILABLE and hasattr(self.dashboard_widget, 'refresh_requested'):
                self.dashboard_widget.refresh_requested.connect(
                    lambda: emit_event(EventTypes.UI_REFRESH_REQUESTED, {})
                )
            
            return self.dashboard_widget
            
        except Exception as e:
            print(f"❌ Failed to create professional dashboard: {e}")
            return None
    
    def _extract_professional_components(self):
        """Extract UI components from professional dashboard"""
        if not self.dashboard_widget:
            return
            
        # Get UI components using the standard interface
        components = self.dashboard_widget.get_ui_components()
        
        # Extract components for compatibility
        self.search_edit = components.get('search_edit')
        self.filter_combo = components.get('filter_combo')
        self.refresh_btn = components.get('refresh_btn')
        self.btn_auto_refresh = components.get('btn_auto_refresh')
        self.btn_select_all = components.get('btn_select_all')
        self.btn_deselect_all = components.get('btn_deselect_all')
        
        # Extract table and models
        self.table = components.get('table')
        self.instances_model = components.get('instances_model')
        self.instances_proxy = components.get('instances_proxy')
        self.ai_tracker_status = components.get('ai_tracker_status')
    
    def _create_monokai_dashboard(self) -> Optional[QWidget]:
        """Create enhanced Monokai dashboard"""
        try:
            self.dashboard_widget = MonokaiDashboard(self.parent_window)
            self.dashboard_widget.set_backend(self.backend_manager)
            
            # Extract UI components for compatibility
            self._extract_monokai_components()
            
            # Connect signals
            self._connect_monokai_signals()
            
            print("📊 Monokai dashboard created successfully!")
            return self.dashboard_widget
            
        except Exception as e:
            print(f"❌ Monokai dashboard creation error: {e}")
            return None
    
    def _extract_monokai_components(self):
        """Extract UI components from Monokai dashboard"""
        if not self.dashboard_widget:
            return
            
        # Extract controls for compatibility
        self.search_edit = getattr(self.dashboard_widget, 'search_edit', None)
        self.filter_combo = getattr(self.dashboard_widget, 'filter_combo', None)
        self.refresh_btn = getattr(self.dashboard_widget, 'refresh_btn', None)
        self.btn_auto_refresh = getattr(self.dashboard_widget, 'btn_auto_refresh', None)
        self.btn_select_all = getattr(self.dashboard_widget, 'btn_select_all', None)
        self.btn_deselect_all = getattr(self.dashboard_widget, 'btn_deselect_all', None)
        
        # Extract table and models
        self.table = getattr(self.dashboard_widget, 'instance_table', None)
        self.instances_model = getattr(self.dashboard_widget, 'instances_model', None)
        self.instances_proxy = getattr(self.dashboard_widget, 'instances_proxy', None)
    
    def _connect_monokai_signals(self):
        """Connect Monokai dashboard signals to component signals"""
        if not self.dashboard_widget:
            return
            
        # Connect extracted components to our signals
        if self.search_edit:
            self.search_edit.textChanged.connect(self.search_changed.emit)
        if self.filter_combo:
            self.filter_combo.currentTextChanged.connect(self.filter_changed.emit)
        if self.refresh_btn:
            self.refresh_btn.clicked.connect(self.refresh_requested.emit)
        if self.btn_select_all:
            self.btn_select_all.clicked.connect(lambda: self.selection_changed.emit(True))
        if self.btn_deselect_all:
            self.btn_deselect_all.clicked.connect(lambda: self.selection_changed.emit(False))
    
    def _create_standard_dashboard(self) -> QWidget:
        """Create standard fallback dashboard"""
        dashboard_widget = QWidget()
        layout = QVBoxLayout(dashboard_widget)
        
        # Create filter bar
        filter_bar = self._create_filter_bar()
        layout.addLayout(filter_bar)
        
        # Create main content area
        content_area = self._create_content_area()
        layout.addWidget(content_area)
        
        # Connect standard signals
        self._connect_standard_signals()
        
        self.dashboard_widget = dashboard_widget
        return dashboard_widget
    
    def _create_filter_bar(self) -> QHBoxLayout:
        """Create filter bar with search and controls"""
        filter_bar = QHBoxLayout()
        
        # Search components
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Tìm theo tên hoặc index...")
        
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Tất cả", "Đang chạy", "Đã tắt"])
        
        # Control buttons
        self.btn_select_all = QPushButton("✅ Chọn tất cả")
        self.btn_deselect_all = QPushButton("❌ Bỏ chọn")
        
        # AI status (replaces refresh buttons)
        self.ai_tracker_status = QLabel("🤖 AI Tracker: Đang theo dõi...")
        self.ai_tracker_status.setStyleSheet("color: #A6E22E; font-weight: bold;")
        self.ai_tracker_status.setToolTip("Global AI Tracker đang theo dõi instances real-time")
        
        # Layout
        filter_bar.addWidget(QLabel("Tìm kiếm:"))
        filter_bar.addWidget(self.search_edit)
        filter_bar.addSpacing(15)
        filter_bar.addWidget(QLabel("Trạng thái:"))
        filter_bar.addWidget(self.filter_combo)
        filter_bar.addStretch(1)
        filter_bar.addWidget(self.btn_select_all)
        filter_bar.addWidget(self.btn_deselect_all)
        filter_bar.addWidget(self.ai_tracker_status)
        
        return filter_bar
    
    def _create_content_area(self) -> QWidget:
        """Create main content area with table"""
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        
        # Create table widget
        self.table = QTableWidget()
        self.table.setSortingEnabled(True)
        
        # Hide vertical header to avoid confusion with Index column
        vertical_header = self.table.verticalHeader()
        if vertical_header:
            vertical_header.setVisible(False)
        
        layout.addWidget(self.table)
        return content_widget
    
    def _connect_standard_signals(self):
        """Connect standard dashboard signals"""
        if self.search_edit:
            self.search_edit.textChanged.connect(self.search_changed.emit)
        if self.filter_combo:
            self.filter_combo.currentTextChanged.connect(self.filter_changed.emit)
        if self.btn_select_all:
            self.btn_select_all.clicked.connect(lambda: self.selection_changed.emit(True))
        if self.btn_deselect_all:
            self.btn_deselect_all.clicked.connect(lambda: self.selection_changed.emit(False))
    
    def _handle_refresh_event(self, event_data: Dict[str, Any]):
        """Handle refresh events from EventManager"""
        if OPTIMIZATION_AVAILABLE:
            # Emit refresh signal
            self.refresh_requested.emit()
    
    def _handle_search_event(self, event_data: Dict[str, Any]):
        """Handle search events from EventManager"""
        query = event_data.get('query', '')
        if self.search_edit and self.search_edit.text() != query:
            self.search_edit.setText(query)
    
    def get_ui_components(self) -> Dict[str, Any]:
        """Get UI components for parent window compatibility"""
        return {
            'search_edit': self.search_edit,
            'filter_combo': self.filter_combo,
            'refresh_btn': self.refresh_btn,
            'btn_auto_refresh': self.btn_auto_refresh,
            'btn_select_all': self.btn_select_all,
            'btn_deselect_all': self.btn_deselect_all,
            'ai_tracker_status': self.ai_tracker_status,
            'table': self.table,
            'instances_model': self.instances_model,
            'instances_proxy': self.instances_proxy
        }
    
    def update_ai_status(self, status_text: str):
        """Update AI tracker status"""
        if self.ai_tracker_status:
            self.ai_tracker_status.setText(status_text)
    
    def refresh_dashboard(self):
        """Refresh dashboard content"""
        if OPTIMIZATION_AVAILABLE:
            # Emit refresh event
            self.event_manager.emit(EventTypes.UI_REFRESH_REQUESTED, {
                'source': 'dashboard_component',
                'timestamp': str(time.time())
            })
        else:
            # Fallback refresh
            self.refresh_requested.emit()


# Factory function
def create_dashboard_component(parent_window, backend_manager) -> DashboardComponent:
    """
    Factory function to create professional dashboard component.
    
    Prioritizes professional dashboard design over legacy themes.
    """
    print("🏗️ Creating professional dashboard component...")
    component = DashboardComponent(parent_window, backend_manager)
    dashboard_widget = component.create_dashboard()
    
    if dashboard_widget:
        print("✅ Professional dashboard component created successfully")
    else:
        print("❌ Failed to create dashboard component")
    
    return component
