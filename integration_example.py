"""
Integration Example - Sử dụng Optimization trong Main Window
=========================================================

Example về cách integrate ServiceManager, EventManager, StateManager 
vào existing main_window.py code.
"""

import time
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer

# Import optimization components
from services import get_service_manager  
from core import get_event_manager, get_state_manager, EventTypes, emit_event

class IntegratedMainWindow(QMainWindow):
    """
    Example integration của optimization components
    vào existing MainWindow structure.
    """
    
    def __init__(self):
        super().__init__()
        
        # Mock backend for demo
        self.backend = None
        
        # Replace scattered optimization imports với single managers
        self._init_optimization_managers()
        
        # Replace manual service initialization với ServiceManager
        self._init_services()
        
        # Replace direct signal connections với EventManager
        self._init_events()
        
        # Replace scattered state variables với StateManager
        self._init_state()
        
        print("✅ Integrated MainWindow initialized")
    
    def _init_optimization_managers(self):
        """Initialize all optimization managers"""
        # Thay vì:
        # from optimizations.smart_cache import global_smart_cache
        # from optimizations.progressive_loading import ProgressiveLoader
        # from optimizations.intelligent_worker_pool import IntelligentWorkerPool
        # ... 20+ imports
        
        # Chỉ cần:
        self.services = get_service_manager()
        self.events = get_event_manager()
        self.state = get_state_manager()
        
        print("🔧 Optimization managers initialized")
    
    def _init_services(self):
        """Initialize services using ServiceManager"""
        # Thay vì manual initialization:
        # self.smart_cache = SmartCache()
        # self.memory_manager = get_memory_manager()
        # self.ai_optimizer = get_ai_optimizer()
        # ... manual setup cho từng service
        
        # ServiceManager tự động handle tất cả:
        self.services.start_all_services()
        
        # Access services khi cần:
        self.cache = self.services.get_cache()
        self.database = self.services.get_database()
        self.ai_service = self.services.get_ai()
        
        print(f"🚀 Started {len(self.services.get_available_services())} services")
    
    def _init_events(self):
        """Initialize event handling using EventManager"""
        # Thay vì direct signal connections:
        # self.table.itemSelectionChanged.connect(self.on_selection_changed)
        # self.refresh_timer.timeout.connect(self.refresh_instances)
        # ... nhiều direct connections
        
        # Sử dụng event-driven approach:
        from core import subscribe_event
        
        # Subscribe to events
        subscribe_event(EventTypes.INSTANCE_SELECTED, self._on_instance_selected)
        subscribe_event(EventTypes.INSTANCES_UPDATED, self._on_instances_updated)
        subscribe_event(EventTypes.UI_PAGE_CHANGED, self._on_page_changed)
        
        # Service events
        self.services.service_started.connect(self._on_service_started)
        self.services.service_error.connect(self._on_service_error)
        
        print("📡 Event subscriptions configured")
    
    def _init_state(self):
        """Initialize state management using StateManager"""
        # Thay vì scattered state variables:
        # self.instances = []
        # self.selected_instances = []
        # self.ui_states = {}
        # self.automation_settings = {}
        # ... nhiều state variables
        
        # Centralized state management:
        # StateManager tự động handle tất cả state
        
        # Subscribe to state changes
        self.state.instances_changed.connect(self._on_instances_state_changed)
        self.state.ui_changed.connect(self._on_ui_state_changed)
        self.state.automation_changed.connect(self._on_automation_state_changed)
        
        print("📊 State management configured")
    
    # Event Handlers - Much simpler với optimization
    def _on_instance_selected(self, data):
        """Handle instance selection event"""
        instance_id = data.get('instance_id')
        print(f"📌 Instance {instance_id} selected")
        
        # Update UI based on selection
        self._update_selection_ui(instance_id)
    
    def _on_instances_updated(self, data):
        """Handle instances update event"""
        instances = data.get('instances', [])
        count = len(instances)
        
        print(f"🔄 {count} instances updated")
        
        # Update state - StateManager handles the rest
        self.state.update_instances(instances)
    
    def _on_page_changed(self, data):
        """Handle UI page change event"""
        page_index = data.get('page_index')
        page_name = data.get('page_name', f'Page {page_index}')
        
        print(f"📄 Changed to {page_name}")
        
        # Update UI state
        self.state.update_ui_state(current_page=page_index)
    
    def _on_service_started(self, service_name):
        """Handle service started event"""
        print(f"✅ Service '{service_name}' started")
        
        # Cache service example
        if service_name == 'cache' and self.cache:
            # Store UI state in cache
            self.cache.set('last_startup', time.time())
    
    def _on_service_error(self, service_name, error):
        """Handle service error event"""
        print(f"❌ Service '{service_name}' error: {error}")
        
        # Could emit UI event to show error to user
        emit_event(EventTypes.LOG_ERROR, {
            'message': f"Service {service_name} failed: {error}"
        })
    
    # State Change Handlers
    def _on_instances_state_changed(self, instances_data):
        """Handle instances state change"""
        # UI automatically updates based on state
        total = len(instances_data)
        selected = sum(1 for inst in instances_data if inst.get('selected', False))
        
        print(f"📊 State updated: {total} total, {selected} selected")
        
        # Update UI components
        self._update_instance_display(instances_data)
    
    def _on_ui_state_changed(self, ui_data):
        """Handle UI state change"""
        current_page = ui_data.get('current_page', 0)
        theme = ui_data.get('theme', 'monokai')
        
        print(f"🎨 UI state: page={current_page}, theme={theme}")
    
    def _on_automation_state_changed(self, automation_data):
        """Handle automation state change"""
        running = automation_data.get('running', False)
        current_batch = automation_data.get('current_batch', 0)
        
        print(f"🤖 Automation: running={running}, batch={current_batch}")
    
    # Simplified Methods với Optimization
    def refresh_instances(self):
        """Refresh instances - Much simpler với optimization"""
        # Thay vì complex refresh logic:
        # try:
        #     success, data = self.backend.get_all_info()
        #     if success:
        #         self.instances = data
        #         self.update_table()
        #         self.update_ui_states()
        #         # ... many manual updates
        
        # Simplified với optimization:
        try:
            # Mock data for demo
            demo_data = [
                {'id': 0, 'name': 'Instance 1', 'status': 'running'},
                {'id': 1, 'name': 'Instance 2', 'status': 'stopped'}
            ]
            
            # Emit event - EventManager handles distribution
            emit_event(EventTypes.INSTANCES_UPDATED, {
                'instances': demo_data,
                'source': 'backend_refresh'
            })
        except Exception as e:
            # Emit error event
            emit_event(EventTypes.LOG_ERROR, {'message': str(e)})
    
    def start_automation(self, settings):
        """Start automation - Simplified với StateManager"""
        # Thay vì manual state management:
        # self.automation_running = True
        # self.automation_settings = settings
        # self.update_automation_ui()
        # ... manual updates
        
        # Simplified:
        self.state.update_automation_state(
            running=True,
            **settings
        )
        
        # Emit event
        emit_event(EventTypes.AUTOMATION_STARTED, {'settings': settings})
    
    def select_instances(self, instance_ids):
        """Select instances - Simplified với StateManager"""
        # Thay vì manual selection management:
        # for i, instance in enumerate(self.instances):
        #     instance['selected'] = i in instance_ids
        # self.update_selection_ui()
        # ... manual updates
        
        # Simplified:
        self.state.update_instance_selection(instance_ids, selected=True)
        
        # Event automatically emitted by StateManager
    
    # Helper Methods
    def _update_selection_ui(self, instance_id):
        """Update UI for instance selection"""
        # Get current state
        selected_instances = self.state.get_selected_instances()
        
        # Update UI based on selection
        print(f"UI updated for {len(selected_instances)} selected instances")
    
    def _update_instance_display(self, instances_data):
        """Update instance display"""
        # Update table, status, etc.
        print(f"Display updated for {len(instances_data)} instances")
    
    def cleanup(self):
        """Cleanup resources"""
        # Stop all services
        self.services.stop_all_services()
        
        # Save state if needed
        state_data = self.state.save_to_dict()
        if self.cache:
            self.cache.set('last_state', state_data)
        
        print("🧹 Cleanup completed")

# Usage example
def create_optimized_window():
    """Create window với optimization integration"""
    window = IntegratedMainWindow()
    
    # Example: Load saved state
    cache = window.services.get_cache()
    if cache:
        saved_state = cache.get('last_state')
        if saved_state:
            window.state.load_from_dict(saved_state)
    
    return window

if __name__ == "__main__":
    # Test integration
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = create_optimized_window()
    
    # Test some functionality
    window.refresh_instances()
    window.select_instances([0, 1, 2])
    window.start_automation({'batch_size': 20})
    
    print("🎉 Integration test completed")
    
    window.cleanup()
    app.quit()
