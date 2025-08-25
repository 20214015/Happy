import sys
import os
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
    from constants import ORG_NAME, APP_NAME
    from main_window import MainWindow
    
    # Import theme module
    from theme import AppTheme
        
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

def load_fonts():
    """Load custom fonts from assets folder with enhanced fallback system and safety checks."""
    try:
        # Early safety check for Qt availability and environment
        try:
            from PyQt6.QtGui import QFontDatabase
            from PyQt6.QtWidgets import QApplication
            
            # Check if we have a QApplication instance
            app = QApplication.instance()
            if app is None:
                print("⚠️ No QApplication instance - skipping font loading")
                return
                
        except ImportError:
            print("⚠️ PyQt6 not available - skipping font loading")
            return
        except Exception as e:
            print(f"⚠️ Qt environment check failed: {e} - skipping font loading")
            return
        
        # Check for headless environment and skip if problematic
        import os
        if os.environ.get('QT_QPA_PLATFORM') == 'offscreen':
            print("🔤 Headless environment detected - using simplified font loading")
            _register_system_fonts_only()
            return
        
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
            print(f"⚠️ Font directory not found at '{font_dir}' - using system fonts")
            _register_system_fonts_only()
            return

        # Enhanced font configuration with fallbacks and safety loading
        font_config = {
            'essential': {
                'Inter-Regular.ttf': ['Inter', 'Arial', 'Helvetica'],
                'Inter-Bold.ttf': ['Inter', 'Arial Bold', 'Helvetica Bold'],
                'JetBrainsMono-Regular.ttf': ['JetBrains Mono', 'Consolas', 'Monaco', 'Courier New'],
                'JetBrainsMono-Bold.ttf': ['JetBrains Mono', 'Consolas Bold', 'Monaco Bold', 'Courier New Bold']
            },
            'optional': {
                'JetBrainsMono-Medium.ttf': ['JetBrains Mono Medium', 'JetBrains Mono', 'Consolas'],
                'JetBrainsMono-Italic.ttf': ['JetBrains Mono Italic', 'JetBrains Mono', 'Consolas Italic'],
                'JetBrainsMono-Bold-Italic.ttf': ['JetBrains Mono Bold Italic', 'JetBrains Mono Bold', 'Consolas Bold'],
                'JetBrainsMono-Medium-Italic.ttf': ['JetBrains Mono Medium Italic', 'JetBrains Mono Medium'],
                'JetBrainsMono-ExtraBold.ttf': ['JetBrains Mono ExtraBold', 'JetBrains Mono Bold'],
                'JetBrainsMono-ExtraBold-Italic.ttf': ['JetBrains Mono ExtraBold Italic', 'JetBrains Mono Bold Italic']
            }
        }

        loaded_count = 0
        failed_fonts = []
        
        # Load essential fonts first with safety checks
        print("🔤 Loading essential fonts...")
        for font_file, fallbacks in font_config['essential'].items():
            font_path = os.path.join(font_dir, font_file)
            if os.path.isfile(font_path):
                try:
                    # Safety check: verify file is readable and valid
                    with open(font_path, 'rb') as f:
                        # Read first few bytes to verify it's a valid font file
                        header = f.read(4)
                        if len(header) < 4:
                            print(f"⚠️ Invalid font file (too small): {font_file}")
                            failed_fonts.append((font_file, fallbacks))
                            continue
                    
                    # Safely attempt to load font
                    font_id = QFontDatabase.addApplicationFont(font_path)
                    if font_id != -1:
                        loaded_count += 1
                        font_families = QFontDatabase.applicationFontFamilies(font_id)
                        print(f"✅ Loaded essential font: {font_file} -> {font_families}")
                    else:
                        print(f"❌ Failed to load essential font: {font_file} - will use fallback: {fallbacks[1]}")
                        failed_fonts.append((font_file, fallbacks))
                except Exception as e:
                    print(f"❌ Error loading essential font {font_file}: {e}")
                    failed_fonts.append((font_file, fallbacks))
            else:
                print(f"⚠️ Essential font not found: {font_file} - will use fallback: {fallbacks[1]}")
                failed_fonts.append((font_file, fallbacks))
        
        # Load optional fonts with graceful degradation and safety checks
        print("🔤 Loading optional fonts...")
        for font_file, fallbacks in font_config['optional'].items():
            font_path = os.path.join(font_dir, font_file)
            if os.path.isfile(font_path):
                try:
                    # Safety check for optional fonts too
                    with open(font_path, 'rb') as f:
                        header = f.read(4)
                        if len(header) < 4:
                            failed_fonts.append((font_file, fallbacks))
                            continue
                    
                    font_id = QFontDatabase.addApplicationFont(font_path)
                    if font_id != -1:
                        loaded_count += 1
                        # Silent loading for optional fonts - no print
                    else:
                        failed_fonts.append((font_file, fallbacks))
                except Exception as e:
                    # Silently handle optional font errors
                    failed_fonts.append((font_file, fallbacks))
            else:
                # For missing optional fonts, create fallback mapping
                failed_fonts.append((font_file, fallbacks))

        total_fonts = len(font_config['essential']) + len(font_config['optional'])
        essential_loaded = min(loaded_count, len(font_config['essential']))
        optional_loaded = max(0, loaded_count - essential_loaded)
        
        print(f"✅ Font loading complete: {loaded_count}/{total_fonts} fonts loaded")
        print(f"   Essential: {essential_loaded}/{len(font_config['essential'])}")
        print(f"   Optional: {optional_loaded}/{len(font_config['optional'])}")
        
        if failed_fonts:
            print(f"🔧 {len(failed_fonts)} fonts using system fallbacks - performance optimized")
        
        # Register fallback fonts in Qt system with safety checks
        try:
            _register_fallback_fonts(font_config)
        except Exception as e:
            print(f"⚠️ Fallback font registration warning: {e}")
        
    except Exception as e:
        print(f"❌ Error loading fonts: {e} - using system defaults")
        _register_system_fonts_only()

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
    
    # Apply theme
    print("✅ Applying theme...")
    AppTheme.apply_theme(app, settings)
    
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

        # Defer font loading to a background thread for faster startup
        worker_manager = get_global_worker_manager(app)
        worker_manager.submit_task("load_fonts", load_fonts)

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
