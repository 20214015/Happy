#!/usr/bin/env python3
"""
Visual Demo - Dashboard Optimization with Feather Icons
Shows the improved dashboard with Feather-style icons and Monokai colors
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont

from dashboard_optimized import OptimizedDashboard
from feather_icons import get_icon, MONOKAI_COLORS

class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 MuMu Manager Pro - Optimized Dashboard with Feather Icons")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Demo header
        header = QLabel("🎨 Dashboard Optimization Demo - Feather Icons + Performance Boost")
        header.setFont(QFont("JetBrains Mono", 14, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {MONOKAI_COLORS['orange']}; padding: 10px;")
        layout.addWidget(header)
        
        # Add optimized dashboard
        self.dashboard = OptimizedDashboard()
        layout.addWidget(self.dashboard)
        
        # Load demo data
        self.load_demo_data()
        
        # Apply Monokai theme
        self.apply_demo_style()
        
    def load_demo_data(self):
        """Load demonstration data"""
        demo_data = [
            {
                'index': 0,
                'name': '🎮 Gaming Instance',
                'status': 'running',
                'adb_port': 7555,
                'cpu_usage': 45.6,
                'memory_usage': '2.1GB',
                'disk_usage': '4.2GB',
                'uptime': '3h 25m'
            },
            {
                'index': 1,
                'name': '📱 Development Instance',
                'status': 'running',
                'adb_port': 7556,
                'cpu_usage': 23.1,
                'memory_usage': '1.8GB',
                'disk_usage': '3.5GB',
                'uptime': '1h 42m'
            },
            {
                'index': 2,
                'name': '🧪 Testing Instance',
                'status': 'stopped',
                'adb_port': 7557,
                'cpu_usage': 0.0,
                'memory_usage': '0MB',
                'disk_usage': '2.1GB',
                'uptime': 'N/A'
            },
            {
                'index': 3,
                'name': '🎯 Target Instance',
                'status': 'starting',
                'adb_port': 7558,
                'cpu_usage': 12.3,
                'memory_usage': '0.8GB',
                'disk_usage': '1.9GB',
                'uptime': '0h 02m'
            },
            {
                'index': 4,
                'name': '🔧 Debug Instance',
                'status': 'stopped',
                'adb_port': 7559,
                'cpu_usage': 0.0,
                'memory_usage': '0MB',
                'disk_usage': '1.5GB',
                'uptime': 'N/A'
            }
        ]
        
        self.dashboard.update_instances(demo_data)
        self.dashboard.add_log("🎨 Demo data loaded with Feather icons")
        self.dashboard.add_log("⚡ Batch updates active for performance")
        self.dashboard.add_log("🔍 Search filtering available")
        
    def apply_demo_style(self):
        """Apply demo styling"""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {MONOKAI_COLORS['bg'] if 'bg' in MONOKAI_COLORS else '#272822'};
                color: {MONOKAI_COLORS['foreground']};
            }}
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("MuMu Manager Pro")
    app.setApplicationVersion("2.0 - Optimized")
    
    # Create and show demo window
    window = DemoWindow()
    window.show()
    
    print("🚀 Dashboard Optimization Demo Started")
    print("🎨 Feather-style icons with Monokai colors")
    print("⚡ Batch table updates for performance")
    print("📊 Enhanced monitoring and stats")
    print("🔍 Optimized search and filtering")
    
    # Run for a few seconds to capture screenshot
    QTimer.singleShot(3000, app.quit)  # Auto-close after 3 seconds
    
    sys.exit(app.exec())