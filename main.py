import sys
import os
import time

# Set Qt environment variables BEFORE any Qt imports to suppress warnings
os.environ['QT_LOGGING_RULES'] = "*.debug=false;qt.qpa.plugin=false;*.warning=false"
os.environ['QT_ASSUME_STDERR_HAS_CONSOLE'] = '1'

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QFontDatabase

# Import optimized modules
# EXE-specific initialization
if hasattr(sys, '_MEIPASS'):
    # Running from PyInstaller bundle
    import os
    
    # Fix Qt platform plugin path
    app_dir = os.path.dirname(sys.executable)
    platforms_dir = os.path.join(app_dir, 'platforms')
    
    # Ensure platforms directory exists
    if not os.path.exists(platforms_dir):
        os.makedirs(platforms_dir, exist_ok=True)
    
    # Set Qt environment for EXE
    os.environ['QT_PLUGIN_PATH'] = platforms_dir
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = platforms_dir
    
    print(f"EXE Mode: Qt plugins path set to {platforms_dir}")
try:
    from optimizations.app_config import AppConstants, app_config
    from error_handler import global_error_handler, setup_global_exception_handler
    from optimizations.worker_manager import get_global_worker_manager
    from optimizations.performance_monitor import global_performance_monitor
    from optimizations.qt_optimization import optimize_qt_startup, optimize_qt_application, QtWarningFilter
    from optimizations.performance_enhancements import optimize_application_performance, measure_performance
    from optimizations.ai_startup_analytics import start_analytics_session, record_component_load, end_analytics_session
    from optimizations.startup_optimizer import get_startup_optimizer
    from optimizations.font_optimizer import get_font_manager, load_fonts_optimized
    from optimizations.memory_optimizer import get_memory_optimizer
    from optimizations.table_optimizer import get_table_optimizer
    from optimizations.ui_optimizer import get_ui_optimizer, apply_global_ui_optimizations
    from optimizations.optimization_reporter import get_optimization_reporter, print_optimization_summary
    from constants import ORG_NAME, APP_NAME
    from main_window import MainWindow
    
    # Import theme module
    from theme import AppTheme
        
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

def load_fonts():
    """Load custom fonts with optimized non-blocking approach."""
    print("🔤 Starting optimized font loading...")
    
    # Use optimized font loading system
    success = load_fonts_optimized()
    
    if success:
        print("✅ Optimized font loading initiated")
    else:
        print("⚠️ Font loading fallback to system fonts")
    
    return success

def _register_system_fonts_only():
    """Register system fonts only when custom font loading fails."""
    try:
        print("🔤 Using system fonts only - JetBrains Mono, Consolas, or Monaco preferred for code")
        print("🔤 Inter, Arial, or Helvetica preferred for UI text")
    except Exception as e:
        print(f"⚠️ System font registration warning: {e}")

def _register_fallback_fonts(font_config):
    """Register fallback font families for better compatibility with safety checks."""
    try:
        from PyQt6.QtGui import QFontDatabase
        
        # Create font fallback mappings for better rendering
        all_configs = {**font_config['essential'], **font_config['optional']}
        
        # Ensure common font families are available
        font_db = QFontDatabase()
        available_families = font_db.families()
        
        # Register common programming fonts if available
        programming_fonts = ['JetBrains Mono', 'Fira Code', 'Source Code Pro', 'Consolas', 'Monaco']
        available_prog_fonts = [f for f in programming_fonts if f in available_families]
        
        if available_prog_fonts:
            print(f"🔤 Available programming fonts: {', '.join(available_prog_fonts[:3])}")
        else:
            print("🔤 Using system monospace fonts for code display")
            
    except Exception as e:
        print(f"⚠️ Fallback font registration warning: {e}")

if __name__ == "__main__":
    # Apply comprehensive warning filtering for clean startup
    import sys
    import io
    
    class CleanStderr:
        """Clean stderr that filters Qt warnings"""
        def __init__(self, original):
            self.original = original
            
        def write(self, text):
            # Filter out Qt plugin warnings
            if "propagateSizeHints" not in text and "This plugin does not support" not in text:
                return self.original.write(text)
            return len(text)
            
        def flush(self):
            return self.original.flush()
            
        def __getattr__(self, name):
            return getattr(self.original, name)
    
    # Install clean stderr
    sys.stderr = CleanStderr(sys.stderr)
    
    # Initialize optimization systems
    print("🚀 Initializing optimization systems...")
    startup_optimizer = get_startup_optimizer()
    memory_optimizer = get_memory_optimizer()
    font_manager = get_font_manager()
    table_optimizer = get_table_optimizer()
    ui_optimizer = get_ui_optimizer()
    optimization_reporter = get_optimization_reporter()
    
    # Start AI analytics session
    session_id = start_analytics_session()
    print(f"📊 Analytics session started: {session_id}")
    
    # Apply Qt optimizations before creating QApplication
    print("🔧 Applying Qt optimizations...")
    start_time = time.time()
    optimize_qt_startup()
    record_component_load("Qt Optimization", time.time() - start_time)
    
    # Apply performance enhancements
    start_time = time.time()
    optimize_application_performance()
    record_component_load("Performance Enhancement", time.time() - start_time)
    
    # Setup global error handling first
    start_time = time.time()
    setup_global_exception_handler()
    record_component_load("Error Handler Setup", time.time() - start_time)
    
    # Initialize Qt application with optimization
    start_time = time.time()
    app = QApplication(sys.argv)
    record_component_load("QApplication Creation", time.time() - start_time)
    
    # Apply Qt application optimizations
    start_time = time.time()
    optimize_qt_application(app)
    startup_optimizer.optimize_qt_application(app)
    apply_global_ui_optimizations(app)
    record_component_load("Qt Application Config", time.time() - start_time)
    print("✅ Qt optimizations applied")
    
    # Set organization and application info for QSettings
    app.setOrganizationName(AppConstants.ORG_NAME)
    app.setApplicationName(AppConstants.APP_NAME)
    app.setOrganizationDomain(AppConstants.ORG_DOMAIN)
    
    # Initialize settings and load config
    settings = QSettings()
    app_config.update_from_qsettings(settings)
    
    # Start memory monitoring
    memory_optimizer.start_monitoring()
    memory_optimizer.tracker.record_measurement("app_initialization")
    
    # Setup immediate font fallbacks (non-blocking)
    font_manager.setup_immediate_fallbacks()
    
    # Apply theme
    print("✅ Applying theme...")
    start_time = time.time()
    AppTheme.apply_theme(app, settings)
    record_component_load("Theme Application", time.time() - start_time)
    
    try:
        # Create main window with performance measurement
        @startup_optimizer.measure_performance("MainWindow Creation", critical=True)
        def create_main_window():
            start_time = time.time()
            window = MainWindow()
            record_component_load("MainWindow", time.time() - start_time)
            return window
        
        print("🚀 Creating MainWindow instance...")
        window = create_main_window()
        print("✅ MainWindow created successfully")
        
        # Set up error handler parent for dialogs
        global_error_handler.set_parent_widget(window)
        
        # Start performance monitoring if enabled
        if app_config.get("performance.monitoring_enabled", True):
            global_performance_monitor.start_monitoring()
        
        # Start progressive component loading in background
        startup_optimizer.start_progressive_loading()
        
        global_error_handler.log_info(f"{AppConstants.APP_NAME} {AppConstants.APP_VERSION} started", "Application")
        
        # Show window and run app
        print("🖥️ Showing MainWindow...")
        window.show()
        print("✅ MainWindow shown, starting app loop...")

        # Start optimized font loading in background (non-blocking)
        worker_manager = get_global_worker_manager(app)
        worker_manager.submit_task("load_fonts", load_fonts)

        # Record startup complete
        memory_optimizer.tracker.record_measurement("startup_complete")

        exit_code = app.exec()
        
        # End analytics session and generate insights
        optimizations_applied = ['qt_optimization', 'performance_enhancement', 'clean_startup', 'ai_analytics', 'memory_optimization', 'font_optimization', 'ui_optimization', 'table_optimization']
        analysis = end_analytics_session(optimizations_applied)
        print(f"📊 Startup analysis: {analysis.get('status', 'completed')}")
        
        # Generate and display optimization report
        print_optimization_summary()
        optimization_reporter.save_report()
        
    except Exception as e:
        print(f"❌ Exception in ApplicationStartup: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        global_error_handler.handle_exception(type(e), e, e.__traceback__, operation="ApplicationStartup")
        exit_code = 1
    
    finally:
        try:
            # Cleanup on exit
            global_error_handler.log_info("Application shutting down", "Application")
            
            # Memory optimization cleanup
            memory_optimizer.cleanup_on_exit()
            
            # Save configuration
            app_config.save_to_qsettings(settings)
            
            # Cleanup workers
            worker_manager.cleanup()
            
            # Stop performance monitoring
            global_performance_monitor.stop_monitoring()
            
            # Final memory report
            memory_report = memory_optimizer.get_optimization_stats()
            print(f"📊 Final memory usage: {memory_report['memory']['current_mb']}MB")
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
    
    sys.exit(exit_code)
