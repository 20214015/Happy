"""
Qt Optimization Module
=====================

Enhanced Qt initialization and warning suppression for MumuManager Pro.
Addresses Qt plugin warnings and improves application startup performance.

Author: GitHub Copilot Assistant
Date: August 26, 2025
Version: 1.0 - Qt Enhancement
"""

import os
import sys
import warnings
from PyQt6.QtCore import QLoggingCategory, Qt
from PyQt6.QtWidgets import QApplication


class QtOptimizer:
    """Qt platform optimization and warning suppression"""
    
    def __init__(self):
        self.optimizations_applied = []
        
    def suppress_qt_warnings(self):
        """Suppress specific Qt warnings that don't affect functionality"""
        try:
            # Comprehensive Qt logging suppression
            QLoggingCategory.setFilterRules("qt.qpa.plugin.debug=false")
            QLoggingCategory.setFilterRules("qt.qpa.plugin.warning=false")
            QLoggingCategory.setFilterRules("qt.pointer.dispatch.debug=false")
            QLoggingCategory.setFilterRules("*.debug=false")
            QLoggingCategory.setFilterRules("qt.qpa.window.debug=false")
            
            # Set Qt environment variables for cleaner output
            os.environ['QT_LOGGING_RULES'] = "*.debug=false;qt.qpa.plugin=false"
            os.environ['QT_ASSUME_STDERR_HAS_CONSOLE'] = '1'
            
            self.optimizations_applied.append("Qt warning suppression")
            return True
        except Exception as e:
            print(f"⚠️ Could not suppress Qt warnings: {e}")
            return False
    
    def optimize_qt_platform(self):
        """Optimize Qt platform settings for better performance"""
        try:
            # Set Qt platform optimizations
            os.environ.setdefault('QT_ENABLE_HIGHDPI_SCALING', '0')
            os.environ.setdefault('QT_AUTO_SCREEN_SCALE_FACTOR', '0')
            os.environ.setdefault('QT_SCALE_FACTOR', '1')
            
            # Improve rendering performance
            if not os.environ.get('QT_QPA_PLATFORM'):
                # Only set if not already configured
                if sys.platform.startswith('linux'):
                    # Linux optimizations
                    os.environ.setdefault('QT_X11_NO_MITSHM', '1')
                    
            self.optimizations_applied.append("Qt platform optimization")
            return True
        except Exception as e:
            print(f"⚠️ Could not optimize Qt platform: {e}")
            return False
    
    def configure_application(self, app: QApplication):
        """Configure QApplication with optimized settings"""
        try:
            # Basic application configuration - focus on stable attributes
            app.setQuitOnLastWindowClosed(True)
            
            # Try to set organization info if not already set
            if not app.organizationName():
                app.setOrganizationName("MumuManager")
            if not app.applicationName():
                app.setApplicationName("MumuManager Pro")
            
            self.optimizations_applied.append("QApplication configuration")
            return True
        except Exception as e:
            print(f"⚠️ Could not configure QApplication: {e}")
            return False
    
    def apply_all_optimizations(self, app: QApplication = None):
        """Apply all Qt optimizations"""
        success_count = 0
        
        # Apply platform optimizations first
        if self.optimize_qt_platform():
            success_count += 1
            
        # Apply warning suppression
        if self.suppress_qt_warnings():
            success_count += 1
            
        # Configure application if provided
        if app and self.configure_application(app):
            success_count += 1
            
        return {
            'total_optimizations': len(self.optimizations_applied),
            'success_count': success_count,
            'optimizations': self.optimizations_applied,
            'status': 'success' if success_count > 0 else 'failed'
        }


# Global Qt optimizer instance
qt_optimizer = QtOptimizer()


def optimize_qt_startup():
    """Optimize Qt for startup - call before creating QApplication"""
    return qt_optimizer.optimize_qt_platform() and qt_optimizer.suppress_qt_warnings()


def optimize_qt_application(app: QApplication):
    """Optimize QApplication instance"""
    return qt_optimizer.configure_application(app)


def get_qt_optimization_status():
    """Get current Qt optimization status"""
    return {
        'optimizations_applied': qt_optimizer.optimizations_applied,
        'total_count': len(qt_optimizer.optimizations_applied)
    }


class QtWarningFilter:
    """Context manager to temporarily suppress Qt warnings"""
    
    def __init__(self, suppress_propagate_hints=True):
        self.suppress_propagate_hints = suppress_propagate_hints
        self.original_stderr = None
        self._stderr_buffer = None
        
    def __enter__(self):
        if self.suppress_propagate_hints:
            # Redirect stderr to suppress propagateSizeHints warnings
            import io
            self.original_stderr = sys.stderr
            self._stderr_buffer = io.StringIO()
            sys.stderr = FilteredStderr(self.original_stderr, ["propagateSizeHints"])
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.original_stderr:
            sys.stderr = self.original_stderr


class FilteredStderr:
    """Stderr wrapper that filters out specific warning messages"""
    
    def __init__(self, original_stderr, filter_patterns):
        self.original_stderr = original_stderr
        self.filter_patterns = filter_patterns
    
    def write(self, text):
        # Check if text contains any filter patterns
        should_filter = any(pattern in text for pattern in self.filter_patterns)
        if not should_filter:
            self.original_stderr.write(text)
    
    def flush(self):
        self.original_stderr.flush()
    
    def __getattr__(self, name):
        return getattr(self.original_stderr, name)


# Convenience function for typical usage
def with_qt_optimization(func):
    """Decorator to run function with Qt optimizations"""
    def wrapper(*args, **kwargs):
        optimize_qt_startup()
        result = func(*args, **kwargs)
        return result
    return wrapper


if __name__ == "__main__":
    # Test Qt optimization
    print("🔧 Testing Qt Optimization...")
    
    # Test startup optimization
    result = optimize_qt_startup()
    print(f"Startup optimization: {'✅ Success' if result else '❌ Failed'}")
    
    # Test with QApplication
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    
    app_result = optimize_qt_application(app)
    print(f"Application optimization: {'✅ Success' if app_result else '❌ Failed'}")
    
    # Get status
    status = get_qt_optimization_status()
    print(f"📊 Optimizations applied: {status['total_count']}")
    for opt in status['optimizations_applied']:
        print(f"  ✅ {opt}")
    
    print("🔧 Qt Optimization test completed")