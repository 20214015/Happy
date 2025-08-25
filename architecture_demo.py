"""
Architecture Optimization Demo
=============================

Demo để test các tối ưu hóa architecture:
- ServiceManager
- EventManager  
- StateManager
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QTimer

class ArchitectureDemo(QMainWindow):
    """Demo window để test optimization architecture"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MuMuManager Pro - Architecture Demo")
        self.resize(600, 400)
        
        self.setup_ui()
        print("✅ Architecture Demo initialized")
    
    def setup_ui(self):
        """Setup simple UI"""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Title
        title = QLabel("🚀 MuMuManager Pro - Architecture Optimization")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Test service manager
        try:
            from services import get_service_manager
            service_mgr = get_service_manager()
            services = service_mgr.get_available_services()
            
            service_label = QLabel(f"✅ ServiceManager: {len(services)} services available")
            layout.addWidget(service_label)
            
        except Exception as e:
            error_label = QLabel(f"❌ ServiceManager error: {e}")
            layout.addWidget(error_label)
        
        # Test event manager
        try:
            from core import get_event_manager
            event_mgr = get_event_manager()
            
            event_label = QLabel("✅ EventManager: Initialized successfully")
            layout.addWidget(event_label)
            
        except Exception as e:
            error_label = QLabel(f"❌ EventManager error: {e}")
            layout.addWidget(error_label)
        
        # Test state manager
        try:
            from core import get_state_manager
            state_mgr = get_state_manager()
            
            state_label = QLabel("✅ StateManager: Initialized successfully")
            layout.addWidget(state_label)
            
        except Exception as e:
            error_label = QLabel(f"❌ StateManager error: {e}")
            layout.addWidget(error_label)
        
        # Test button
        test_btn = QPushButton("🧪 Run Integration Test")
        test_btn.clicked.connect(self.run_integration_test)
        layout.addWidget(test_btn)
        
        # Results area
        self.results = QLabel("Click test button to run integration test...")
        self.results.setStyleSheet("background: #f0f0f0; padding: 10px; margin: 10px;")
        layout.addWidget(self.results)
    
    def run_integration_test(self):
        """Run integration test của tất cả components"""
        try:
            results = []
            
            # Test ServiceManager
            from services import get_service_manager
            service_mgr = get_service_manager()
            cache = service_mgr.get_cache()
            if cache:
                cache.set('test', 'value')
                retrieved = cache.get('test')
                if retrieved == 'value':
                    results.append("✅ ServiceManager cache test passed")
                else:
                    results.append("❌ ServiceManager cache test failed")
            else:
                results.append("⚠️ ServiceManager cache not available")
            
            # Test EventManager + StateManager
            from core import get_event_manager, get_state_manager, emit_event, EventTypes
            
            event_mgr = get_event_manager()
            state_mgr = get_state_manager()
            
            # Test event emission
            emit_event(EventTypes.INSTANCES_UPDATED, {'test': True})
            results.append("✅ Event emission test passed")
            
            # Test state update
            state_mgr.update_instances([
                {'id': 0, 'name': 'Test Instance', 'status': 'running'}
            ])
            instances = state_mgr.get_instances()
            if len(instances) == 1:
                results.append("✅ State management test passed")
            else:
                results.append("❌ State management test failed")
            
            # Display results
            self.results.setText("\n".join(results))
            
        except Exception as e:
            self.results.setText(f"❌ Integration test failed: {e}")
            import traceback
            traceback.print_exc()

def run_demo():
    """Run architecture demo"""
    app = QApplication(sys.argv)
    
    demo = ArchitectureDemo()
    demo.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(run_demo())
