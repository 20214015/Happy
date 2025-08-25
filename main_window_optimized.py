"""
Optimized Main Window - Simplified Architecture
==============================================

Phiên bản tối ưu của MainWindow với:
- ServiceManager thay vì nhiều optimization imports
- EventManager cho event-driven architecture  
- StateManager cho centralized state
- Ít code hơn, dễ maintain hơn
"""

import sys
import time
from typing import List, Dict, Any, Optional

from PyQt6.QtCore import Qt, QTimer, QSettings
from PyQt6.QtGui import QIcon, QFont, QCloseEvent
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame, QMessageBox
)

# Core components
from core import (
    get_event_manager, get_state_manager, EventTypes,
    emit_event, subscribe_event
)
from services import get_service_manager

# Optimizations
from optimizations.worker_manager import get_global_worker_manager

# UI and backend
from constants import APP_NAME, APP_VERSION
from theme import AppTheme
from backend import MumuManager
from widgets import StatusPillDelegate, InstancesModel, InstancesProxy
from ui import ModernButton

class OptimizedMainWindow(QMainWindow):
    """
    Optimized Main Window với simplified architecture
    
    Thay vì 4636 dòng code phức tạp, window này sử dụng:
    - ServiceManager: Quản lý tất cả services
    - EventManager: Event-driven communication
    - StateManager: Centralized state management
    - WorkerManager: Non-blocking background tasks
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"MuMuManager MKV v{APP_VERSION} - Optimized")
        self.resize(1600, 900)
        
        # Initialize managers
        self.service_manager = get_service_manager()
        self.event_manager = get_event_manager()
        self.state_manager = get_state_manager()
        self.worker_manager = get_global_worker_manager(self) # Get worker manager
        
        # Worker tracking
        self.refresh_worker_id: Optional[str] = None
        
        # Settings and backend
        self.settings = QSettings()
        self.mumu_manager = MumuManager(self.settings.value("manager_path", ""))
        
        # Setup UI
        self._setup_ui()
        self._setup_events()
        self._setup_services()
        self._setup_workers()
        
        # Apply theme  
        app_instance = QApplication.instance()
        if app_instance and isinstance(app_instance, QApplication):
            AppTheme.apply_theme(app_instance, self.settings)
        
        print("✅ OptimizedMainWindow initialized successfully")
    
    def _setup_ui(self):
        """Setup basic UI structure"""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        
        # Header
        header = self._create_header()
        layout.addWidget(header)
        
        # Main content area
        content_area = self._create_content_area()
        layout.addWidget(content_area)
        
        # Status bar
        self.status_bar = self.statusBar()
        if self.status_bar:
            self.status_bar.showMessage("Ready")
    
    def _create_header(self) -> QWidget:
        """Create header với app info và quick controls"""
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet("background-color: #2D2A2E; border-bottom: 1px solid #49483E;")
        
        layout = QHBoxLayout(header)
        
        # App title
        title = QLabel(f"{APP_NAME} v{APP_VERSION} - Optimized Edition")
        title.setStyleSheet("color: #F8F8F2; font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Quick control buttons
        self.refresh_btn = ModernButton("🔄 Refresh", "primary", "sm")
        self.refresh_btn.clicked.connect(self._refresh_instances)
        layout.addWidget(self.refresh_btn)
        
        self.settings_btn = ModernButton("⚙️ Settings", "secondary", "sm")
        layout.addWidget(self.settings_btn)
        
        return header
    
    def _create_content_area(self) -> QWidget:
        """Create main content area"""
        content = QWidget()
        layout = QVBoxLayout(content)
        
        # Service status display
        service_status = self._create_service_status()
        layout.addWidget(service_status)
        
        # Instance info display
        instance_info = self._create_instance_info()
        layout.addWidget(instance_info)
        
        return content
    
    def _create_service_status(self) -> QWidget:
        """Create service status display"""
        status_widget = QFrame()
        status_widget.setFixedHeight(100)
        status_widget.setStyleSheet("background-color: #272822; border: 1px solid #49483E; border-radius: 5px;")
        
        layout = QVBoxLayout(status_widget)
        
        title = QLabel("🔧 Service Status")
        title.setStyleSheet("color: #FD971F; font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Service status labels
        self.service_labels = QHBoxLayout()
        layout.addLayout(self.service_labels)
        
        # Update service status
        self._update_service_status()
        
        return status_widget
    
    def _create_instance_info(self) -> QWidget:
        """Create instance information display"""
        info_widget = QFrame()
        info_widget.setStyleSheet("background-color: #272822; border: 1px solid #49483E; border-radius: 5px;")
        
        layout = QVBoxLayout(info_widget)
        
        title = QLabel("📊 Instance Information")
        title.setStyleSheet("color: #A6E22E; font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        self.instance_count_label = QLabel("Instances: Loading...")
        self.instance_count_label.setStyleSheet("color: #F8F8F2;")
        layout.addWidget(self.instance_count_label)
        
        self.selected_count_label = QLabel("Selected: 0")
        self.selected_count_label.setStyleSheet("color: #66D9EF;")
        layout.addWidget(self.selected_count_label)
        
        return info_widget
    
    def _setup_events(self):
        """Setup event subscriptions"""
        # Subscribe to state changes
        self.state_manager.instances_changed.connect(self._on_instances_changed)
        self.state_manager.ui_changed.connect(self._on_ui_changed)
        
        # Subscribe to service events
        self.service_manager.service_started.connect(self._on_service_started)
        self.service_manager.service_stopped.connect(self._on_service_stopped)
        self.service_manager.service_error.connect(self._on_service_error)
        
        # Subscribe to general events
        subscribe_event(EventTypes.INSTANCE_SELECTED, self._on_instance_selected_event)
        subscribe_event(EventTypes.INSTANCES_UPDATED, self._on_instances_updated_event)
        
        print("✅ Event subscriptions setup complete")

    def _setup_workers(self):
        """Connect worker manager signals"""
        self.worker_manager.worker_finished.connect(self._on_worker_finished)
        self.worker_manager.worker_error.connect(self._on_worker_error)
        print("✅ Worker signals connected")
    
    def _setup_services(self):
        """Setup and start services"""
        # Start all available services
        self.service_manager.start_all_services()
        
        # Setup auto-refresh timer
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self._refresh_instances)
        self.refresh_timer.start(30000)  # 30 seconds
        
        # Initial refresh
        self._refresh_instances()
        
        print("✅ Services setup complete")
    
    def _show_status_message(self, message: str, timeout: int = 5000):
        """Helper để show status message với error handling"""
        if self.status_bar:
            self.status_bar.showMessage(message, timeout)

    def _update_service_status(self):
        """Update service status display"""
        # Clear existing labels
        for i in reversed(range(self.service_labels.count())):
            item = self.service_labels.itemAt(i)
            if item and item.widget():
                item.widget().setParent(None)
        
        # Add service status labels
        service_info = self.service_manager.get_service_info()
        for service_name, info in service_info.items():
            status = "✅" if info['status'] else "❌"
            label = QLabel(f"{status} {service_name.title()}")
            label.setStyleSheet("color: #F8F8F2; margin-right: 10px;")
            self.service_labels.addWidget(label)
    
    def _refresh_instances(self):
        """Submit a task to refresh instance data in the background."""
        if self.refresh_worker_id:
            print("⚠️ Refresh already in progress. Skipping.")
            return

        print("🔄 Submitting instance refresh task...")
        self.refresh_btn.setEnabled(False)
        self._show_status_message("🔄 Refreshing instances...")

        # Submit task to worker manager
        self.refresh_worker_id = self.worker_manager.submit_task(
            name="refresh_instances",
            task_func=self.mumu_manager.get_all_info
        )
        
        if not self.refresh_worker_id:
            print("❌ Failed to submit refresh task.")
            self._show_status_message("❌ Error: Could not start refresh task.")
            self.refresh_btn.setEnabled(True)

    # --- Worker Signal Handlers ---

    def _on_worker_finished(self, worker_id: str, result: Any):
        """Handle successful completion of a worker task."""
        if worker_id != self.refresh_worker_id:
            return # Not the worker we are looking for

        print(f"✅ Worker {worker_id} (refresh_instances) finished.")
        success, data = result

        if success and data:
            # Convert to list format
            if isinstance(data, dict):
                instances = list(data.values())
            else:
                instances = data
            
            # Update state
            self.state_manager.update_instances(instances)
            
            # Emit event
            emit_event(EventTypes.INSTANCES_UPDATED, {
                'instances': instances,
                'count': len(instances)
            })
            
            self._show_status_message(f"✅ Refreshed {len(instances)} instances.")
            print(f"✅ Refreshed {len(instances)} instances")
        else:
            self._show_status_message("⚠️ Failed to get instances from backend.")
            print("⚠️ Failed to get instances from backend")

        # Reset
        self.refresh_worker_id = None
        self.refresh_btn.setEnabled(True)

    def _on_worker_error(self, worker_id: str, error_message: str):
        """Handle an error from a worker task."""
        if worker_id != self.refresh_worker_id:
            return

        print(f"❌ Worker {worker_id} (refresh_instances) failed: {error_message}")
        self._show_status_message(f"❌ Error refreshing instances: {error_message}")
        
        # Reset
        self.refresh_worker_id = None
        self.refresh_btn.setEnabled(True)

    # --- Event Handlers ---
    
    def _on_instances_changed(self, instances_data):
        """Handle instances state change"""
        count = len(instances_data)
        self.instance_count_label.setText(f"Instances: {count}")
        
        selected_count = sum(1 for inst in instances_data if inst.get('selected', False))
        self.selected_count_label.setText(f"Selected: {selected_count}")
        
        print(f"📊 Instances updated: {count} total, {selected_count} selected")
    
    def _on_ui_changed(self, ui_data):
        """Handle UI state change"""
        print(f"🎨 UI state changed: {ui_data}")
    
    def _on_service_started(self, service_name):
        """Handle service started"""
        print(f"✅ Service started: {service_name}")
        self._update_service_status()
        self._show_status_message(f"Service '{service_name}' started")
    
    def _on_service_stopped(self, service_name):
        """Handle service stopped"""
        print(f"⏹️ Service stopped: {service_name}")
        self._update_service_status()
        self._show_status_message(f"Service '{service_name}' stopped")
    
    def _on_service_error(self, service_name, error_message):
        """Handle service error"""
        print(f"❌ Service error in '{service_name}': {error_message}")
        self._show_status_message(f"Service error: {service_name}")
    
    def _on_instance_selected_event(self, data):
        """Handle instance selected event"""
        instance_id = data.get('instance_id')
        print(f"📌 Instance selected: {instance_id}")
    
    def _on_instances_updated_event(self, data):
        """Handle instances updated event"""
        count = data.get('count', 0)
        print(f"🔄 Instances updated event received: {count} instances")
    
    def closeEvent(self, event: QCloseEvent):
        """Handle window close"""
        print("🔄 Shutting down...")
        
        # Stop services and timers
        self.service_manager.stop_all_services()
        self.refresh_timer.stop()
        
        # Cancel any running workers
        if self.refresh_worker_id:
            self.worker_manager.cancel_worker(self.refresh_worker_id)
        
        self.worker_manager.cleanup()
        
        print("✅ Shutdown complete")
        event.accept()

# Demo function
def run_optimized_demo():
    """Run optimized main window demo"""
    app = QApplication(sys.argv)
    
    # Set app settings
    app.setOrganizationName("MuMuManager")
    app.setApplicationName("MuMuManager Pro")
    
    window = OptimizedMainWindow()
    window.show()
    
    return app.exec()

if __name__ == "__main__":
    run_optimized_demo()
