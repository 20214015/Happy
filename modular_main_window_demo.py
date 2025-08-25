"""
Modular Main Window Example
===========================

Demonstrates how the extracted managers can be used to create a much cleaner
and more maintainable main window implementation.

This replaces the 5072-line monolithic main_window.py with a modular approach.
"""

import logging
from typing import Optional, Dict, Any
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QCloseEvent
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QLabel, QPushButton, QProgressBar, QStatusBar
)

# Import our new modular architecture
from services import get_service_manager
from core import get_event_manager, get_state_manager, EventTypes
from managers import InstanceManager, AutomationManager, UIManager

# Import backend and other dependencies (would need to be available)
try:
    from backend import MumuManager
    from theme import AppTheme
    BACKEND_AVAILABLE = True
except ImportError:
    # For testing without full dependencies
    BACKEND_AVAILABLE = False
    
    class MumuManager:
        def get_all_info(self):
            return True, []


class ModularMainWindow(QMainWindow):
    """
    Modular main window using extracted managers.
    
    This demonstrates how the 5072-line main_window.py can be reduced to
    a manageable size by using specialized managers for different concerns.
    
    Key improvements:
    - Separation of concerns
    - Event-driven architecture
    - Centralized state management
    - Unified service access
    - Easier testing and maintenance
    """
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('ModularMainWindow')
        
        # Initialize core services
        self.service_manager = get_service_manager()
        self.event_manager = get_event_manager()
        self.state_manager = get_state_manager()
        
        # Initialize backend
        self.mumu_manager = MumuManager()
        
        # Initialize managers
        self.instance_manager = InstanceManager(self.mumu_manager, self)
        self.automation_manager = AutomationManager(self.mumu_manager, self)
        self.ui_manager = UIManager(self)
        
        # UI Components
        self.central_widget: Optional[QWidget] = None
        self.content_stack: Optional[QStackedWidget] = None
        self.sidebar: Optional[QWidget] = None
        self.status_bar: Optional[QStatusBar] = None
        self.progress_bar: Optional[QProgressBar] = None
        
        # Initialize UI
        self._init_ui()
        self._setup_connections()
        self._load_initial_data()
        
        self.logger.info("ModularMainWindow initialized successfully")
        
    def _init_ui(self):
        """Initialize the user interface"""
        try:
            self.setWindowTitle("MumuM - Modular Architecture Demo")
            self.setGeometry(100, 100, 1200, 800)
            
            # Create central widget
            self.central_widget = QWidget()
            self.setCentralWidget(self.central_widget)
            
            # Create main layout
            main_layout = QHBoxLayout(self.central_widget)
            main_layout.setContentsMargins(0, 0, 0, 0)
            
            # Create sidebar
            self._create_sidebar()
            main_layout.addWidget(self.sidebar)
            
            # Create content area
            self._create_content_area()
            main_layout.addWidget(self.content_stack, 1)
            
            # Create status bar
            self._create_status_bar()
            
            self.logger.info("UI initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize UI: {e}")
            
    def _create_sidebar(self):
        """Create sidebar with navigation"""
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
            }
            QPushButton {
                background-color: #3c3c3c;
                border: none;
                padding: 10px;
                text-align: left;
                color: white;
                margin: 2px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4c4c4c;
            }
            QPushButton:checked {
                background-color: #007ACC;
            }
        """)
        
        layout = QVBoxLayout(self.sidebar)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Title
        title = QLabel("MumuM Pro")
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Navigation buttons
        pages = [
            ("Dashboard", 0),
            ("Instances", 1), 
            ("Automation", 2),
            ("Scripts", 3),
            ("Settings", 4)
        ]
        
        self.nav_buttons = {}
        for name, index in pages:
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, idx=index: self._switch_page(idx))
            layout.addWidget(btn)
            self.nav_buttons[index] = btn
            
        layout.addStretch()
        
        # Set first button as checked
        if 0 in self.nav_buttons:
            self.nav_buttons[0].setChecked(True)
            
    def _create_content_area(self):
        """Create main content area with stacked pages"""
        self.content_stack = QStackedWidget()
        
        # Register page factories with UI manager
        self.ui_manager.register_page_factory(0, self._create_dashboard_page)
        self.ui_manager.register_page_factory(1, self._create_instances_page)
        self.ui_manager.register_page_factory(2, self._create_automation_page)
        self.ui_manager.register_page_factory(3, self._create_scripts_page)
        self.ui_manager.register_page_factory(4, self._create_settings_page)
        
        # Create initial page (dashboard)
        dashboard = self.ui_manager.load_page(0)
        if dashboard:
            self.content_stack.addWidget(dashboard)
        else:
            # Fallback placeholder
            placeholder = self.ui_manager.create_placeholder_widget("Dashboard")
            self.content_stack.addWidget(placeholder)
            
        # Add placeholders for other pages (lazy loading)
        for i in range(1, 5):
            placeholder = self.ui_manager.create_placeholder_widget(f"Page {i}")
            self.content_stack.addWidget(placeholder)
            
    def _create_status_bar(self):
        """Create status bar with progress"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # Initial status
        self.status_bar.showMessage("Ready")
        
    # Page Creation Methods (much simpler than original)
    def _create_dashboard_page(self) -> QWidget:
        """Create dashboard page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Title
        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Instance summary
        summary = QLabel("Instance Summary")
        summary.setStyleSheet("font-size: 16px; margin: 10px;")
        layout.addWidget(summary)
        
        # Quick actions
        actions_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh Instances")
        refresh_btn.clicked.connect(self.instance_manager.refresh_instances)
        actions_layout.addWidget(refresh_btn)
        
        create_btn = QPushButton("Create Instance")
        create_btn.clicked.connect(lambda: self.instance_manager.create_instance(1))
        actions_layout.addWidget(create_btn)
        
        actions_layout.addStretch()
        layout.addLayout(actions_layout)
        
        layout.addStretch()
        return page
        
    def _create_instances_page(self) -> QWidget:
        """Create instances management page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Instance Management")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Instance controls
        controls_layout = QHBoxLayout()
        
        start_btn = QPushButton("Start Selected")
        start_btn.clicked.connect(self._start_selected_instances)
        controls_layout.addWidget(start_btn)
        
        stop_btn = QPushButton("Stop Selected") 
        stop_btn.clicked.connect(self._stop_selected_instances)
        controls_layout.addWidget(stop_btn)
        
        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self._delete_selected_instances)
        controls_layout.addWidget(delete_btn)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Instance list placeholder
        instance_list = QLabel("Instance list would go here")
        instance_list.setStyleSheet("border: 1px dashed #ccc; padding: 20px; margin: 10px;")
        layout.addWidget(instance_list)
        
        return page
        
    def _create_automation_page(self) -> QWidget:
        """Create automation page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Automation")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Automation controls
        controls_layout = QHBoxLayout()
        
        start_automation_btn = QPushButton("Start Automation")
        start_automation_btn.clicked.connect(lambda: self.automation_manager.start_automation("custom"))
        controls_layout.addWidget(start_automation_btn)
        
        stop_automation_btn = QPushButton("Stop Automation")
        stop_automation_btn.clicked.connect(self.automation_manager.stop_automation)
        controls_layout.addWidget(stop_automation_btn)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Automation status
        status_label = QLabel("Automation status would go here")
        status_label.setStyleSheet("border: 1px dashed #ccc; padding: 20px; margin: 10px;")
        layout.addWidget(status_label)
        
        return page
        
    def _create_scripts_page(self) -> QWidget:
        """Create scripts page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Script Management")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Script controls
        controls_layout = QHBoxLayout()
        
        execute_btn = QPushButton("Execute Script")
        execute_btn.clicked.connect(lambda: self.automation_manager.execute_script())
        controls_layout.addWidget(execute_btn)
        
        save_btn = QPushButton("Save Script")
        save_btn.clicked.connect(lambda: self.automation_manager.save_script())
        controls_layout.addWidget(save_btn)
        
        load_btn = QPushButton("Load Script") 
        load_btn.clicked.connect(lambda: self.automation_manager.load_script())
        controls_layout.addWidget(load_btn)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Script editor placeholder
        editor = QLabel("Script editor would go here")
        editor.setStyleSheet("border: 1px dashed #ccc; padding: 20px; margin: 10px;")
        layout.addWidget(editor)
        
        return page
        
    def _create_settings_page(self) -> QWidget:
        """Create settings page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Settings placeholder
        settings = QLabel("Settings would go here")
        settings.setStyleSheet("border: 1px dashed #ccc; padding: 20px; margin: 10px;")
        layout.addWidget(settings)
        
        return page
        
    def _setup_connections(self):
        """Setup signal connections between managers and UI"""
        # Instance manager connections
        self.instance_manager.operation_completed.connect(self._on_operation_completed)
        self.instance_manager.instances_refreshed.connect(self._on_instances_refreshed)
        
        # Automation manager connections
        self.automation_manager.automation_started.connect(self._on_automation_started)
        self.automation_manager.automation_stopped.connect(self._on_automation_stopped)
        self.automation_manager.script_executed.connect(self._on_script_executed)
        
        # UI manager connections
        self.ui_manager.page_changed.connect(self._on_page_changed)
        self.ui_manager.progress_updated.connect(self._on_progress_updated)
        self.ui_manager.status_updated.connect(self._on_status_updated)
        
    def _load_initial_data(self):
        """Load initial application data"""
        # Start services
        self.service_manager.start_all_services()
        
        # Load instances
        self.instance_manager.refresh_instances(silent=True)
        
    # Event Handlers (much simpler than original)
    def _switch_page(self, page_index: int):
        """Switch to a different page"""
        try:
            # Update navigation buttons
            for idx, btn in self.nav_buttons.items():
                btn.setChecked(idx == page_index)
                
            # Load page if not already loaded
            if not self.ui_manager.is_page_loaded(page_index):
                page_widget = self.ui_manager.load_page(page_index)
                if page_widget:
                    # Replace placeholder
                    old_widget = self.content_stack.widget(page_index)
                    self.content_stack.removeWidget(old_widget)
                    old_widget.deleteLater()
                    self.content_stack.insertWidget(page_index, page_widget)
                    
            # Switch to page
            self.content_stack.setCurrentIndex(page_index)
            self.ui_manager.set_current_page(page_index)
            
        except Exception as e:
            self.logger.error(f"Error switching to page {page_index}: {e}")
            
    def _start_selected_instances(self):
        """Start selected instances"""
        selected = self.state_manager.get_selected_instances()
        if selected:
            self.instance_manager.start_instances(selected)
        else:
            self.ui_manager.set_status("No instances selected", "warning")
            
    def _stop_selected_instances(self):
        """Stop selected instances"""
        selected = self.state_manager.get_selected_instances()
        if selected:
            self.instance_manager.stop_instances(selected)
        else:
            self.ui_manager.set_status("No instances selected", "warning")
            
    def _delete_selected_instances(self):
        """Delete selected instances"""
        selected = self.state_manager.get_selected_instances()
        if selected:
            self.instance_manager.delete_instances(selected)
        else:
            self.ui_manager.set_status("No instances selected", "warning")
            
    # Signal Handlers
    def _on_operation_completed(self, operation: str, success: bool, message: str):
        """Handle operation completion"""
        level = "success" if success else "error"
        self.ui_manager.set_status(f"{operation.capitalize()}: {message}", level)
        
    def _on_instances_refreshed(self, instances: list):
        """Handle instances refresh"""
        count = len(instances)
        self.ui_manager.set_status(f"Loaded {count} instances", "success")
        
    def _on_automation_started(self, automation_type: str):
        """Handle automation started"""
        self.ui_manager.set_status(f"Started {automation_type} automation", "info")
        
    def _on_automation_stopped(self, automation_type: str):
        """Handle automation stopped"""
        self.ui_manager.set_status(f"Stopped {automation_type} automation", "info")
        
    def _on_script_executed(self, script_name: str, success: bool, message: str):
        """Handle script execution"""
        level = "success" if success else "error"
        self.ui_manager.set_status(f"Script {script_name}: {message}", level)
        
    def _on_page_changed(self, page_index: int):
        """Handle page change"""
        self.logger.debug(f"Page changed to {page_index}")
        
    def _on_progress_updated(self, value: int, message: str):
        """Handle progress update"""
        if value > 0:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(value)
        else:
            self.progress_bar.setVisible(False)
            
    def _on_status_updated(self, message: str, level: str):
        """Handle status update"""
        if message:
            self.status_bar.showMessage(message)
        else:
            self.status_bar.clearMessage()
            
    def closeEvent(self, event: QCloseEvent):
        """Handle application close"""
        try:
            # Cleanup managers
            self.instance_manager.cleanup()
            self.automation_manager.cleanup()
            self.ui_manager.cleanup()
            
            # Stop services
            self.service_manager.stop_all_services()
            
            event.accept()
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
            event.accept()


# Demo function
def run_modular_demo():
    """Run the modular main window demo"""
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and show window
    window = ModularMainWindow()
    window.show()
    
    print("🚀 Modular MumuM Demo started!")
    print("📊 Compare this clean implementation with the 5072-line original!")
    
    return app.exec()


if __name__ == "__main__":
    import sys
    sys.exit(run_modular_demo())