import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QFontDatabase

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
    from constants import ORG_NAME, APP_NAME
    from main_window import MainWindow
    
    # Import NEW professional theme instead of old theme
    from professional_theme import apply_professional_theme
        
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

def load_professional_fonts():
    """Load professional fonts from assets folder."""
    try:
        # Determine relative path to assets/fonts folder
        # Works for both direct execution and PyInstaller packaging
        if getattr(sys, 'frozen', False):
            # Running in packaged environment
            base_path = sys._MEIPASS
        else:
            # Running in normal development environment
            base_path = os.path.dirname(__file__)

        font_dir = os.path.join(base_path, 'assets', 'fonts')
        
        if not os.path.isdir(font_dir):
            print(f"Warning: Font directory not found at '{font_dir}'")
            return

        # Professional fonts for business interface
        professional_fonts = [
            'Inter-Regular.ttf',    # Primary UI font
            'Inter-Bold.ttf',       # Bold variant
            'JetBrainsMono-Regular.ttf',  # Monospace for data display
            'JetBrainsMono-Bold.ttf'      # Monospace bold
        ]

        loaded_count = 0
        total_fonts = len(professional_fonts)
        
        # Load professional fonts
        for font_file in professional_fonts:
            font_path = os.path.join(font_dir, font_file)
            if os.path.isfile(font_path):
                font_id = QFontDatabase.addApplicationFont(font_path)
                if font_id != -1:
                    loaded_count += 1
                    font_families = QFontDatabase.applicationFontFamilies(font_id)
                    print(f"✅ Loaded professional font: {font_file} -> {font_families}")
                else:
                    print(f"❌ Failed to load font: {font_file}")
            else:
                print(f"⚠️ Font not found: {font_path}")

        print(f"Successfully loaded {loaded_count}/{total_fonts} professional fonts")
        
    except Exception as e:
        print(f"Error loading professional fonts: {e}")

if __name__ == "__main__":
    # Setup global error handling first
    setup_global_exception_handler()
    
    # Initialize Qt application
    app = QApplication(sys.argv)
    
    # Set organization and application info for QSettings
    app.setOrganizationName(AppConstants.ORG_NAME)
    app.setApplicationName(AppConstants.APP_NAME)
    app.setOrganizationDomain(AppConstants.ORG_DOMAIN)
    
    # Initialize settings and load config
    settings = QSettings()
    app_config.update_from_qsettings(settings)
    
    # Apply NEW professional theme
    print("✅ Applying professional theme...")
    apply_professional_theme(app)
    
    try:
        # Create main window
        print("🚀 Creating MainWindow instance...")
        window = MainWindow()
        print("✅ MainWindow created successfully")
        
        # Set up error handler parent for dialogs
        global_error_handler.set_parent_widget(window)
        
        # Start performance monitoring if enabled
        if app_config.get("performance.monitoring_enabled", True):
            global_performance_monitor.start_monitoring()
        
        global_error_handler.log_info(f"{AppConstants.APP_NAME} {AppConstants.APP_VERSION} started", "Application")
        
        # Show window and run app
        print("🖥️ Showing MainWindow...")
        window.show()
        print("✅ MainWindow shown, starting app loop...")

        # Defer professional font loading to a background thread for faster startup
        worker_manager = get_global_worker_manager(app)
        worker_manager.submit_task("load_professional_fonts", load_professional_fonts)

        exit_code = app.exec()
        
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
            
            # Save configuration
            app_config.save_to_qsettings(settings)
            
            # Cleanup workers
            worker_manager.cleanup()
            
            # Stop performance monitoring
            global_performance_monitor.stop_monitoring()
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
    
    sys.exit(exit_code)
