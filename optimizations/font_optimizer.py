"""
Optimized Font Loading System
============================

Non-blocking font loading with intelligent fallbacks and progressive enhancement.
Reduces startup time by deferring font loading to background threads.

Author: GitHub Copilot
Date: August 26, 2025
Version: 1.0 - Production Ready
"""

import os
import sys
import threading
import time
from typing import Dict, List, Optional, Callable
from PyQt6.QtCore import QObject, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtWidgets import QApplication


class FontLoadWorker(QThread):
    """Background worker for font loading"""
    
    font_loaded = pyqtSignal(str, bool)  # font_name, success
    loading_complete = pyqtSignal(int)   # total_loaded
    
    def __init__(self, fonts_to_load: List[tuple]):
        super().__init__()
        self.fonts_to_load = fonts_to_load  # List of (file_path, font_name) tuples
        self.loaded_count = 0
        
    def run(self):
        """Load fonts in background thread"""
        for font_path, font_name in self.fonts_to_load:
            try:
                if os.path.isfile(font_path):
                    # Verify font file is valid
                    with open(font_path, 'rb') as f:
                        header = f.read(4)
                        if len(header) >= 4:
                            # Load font
                            font_id = QFontDatabase.addApplicationFont(font_path)
                            if font_id != -1:
                                self.loaded_count += 1
                                self.font_loaded.emit(font_name, True)
                            else:
                                self.font_loaded.emit(font_name, False)
                        else:
                            self.font_loaded.emit(font_name, False)
                else:
                    self.font_loaded.emit(font_name, False)
                    
                # Small delay to prevent blocking
                self.msleep(10)
                
            except Exception as e:
                self.font_loaded.emit(font_name, False)
                
        self.loading_complete.emit(self.loaded_count)


class OptimizedFontManager(QObject):
    """Manages optimized font loading with progressive enhancement"""
    
    fonts_ready = pyqtSignal(int)  # number of fonts loaded
    critical_fonts_ready = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.loaded_fonts = {}
        self.fallback_fonts = {}
        self.loading_started = False
        self.critical_fonts_loaded = False
        
        # Font configuration with priorities
        self.font_config = {
            'critical': {
                'ui_font': {
                    'files': ['Inter-Regular.ttf', 'Inter-Bold.ttf'],
                    'fallbacks': ['Arial', 'Helvetica', 'sans-serif'],
                    'family': 'Inter'
                },
                'mono_font': {
                    'files': ['JetBrainsMono-Regular.ttf', 'JetBrainsMono-Bold.ttf'],
                    'fallbacks': ['Consolas', 'Monaco', 'Courier New', 'monospace'],
                    'family': 'JetBrains Mono'
                }
            },
            'optional': {
                'mono_variants': {
                    'files': [
                        'JetBrainsMono-Medium.ttf',
                        'JetBrainsMono-Italic.ttf',
                        'JetBrainsMono-Bold-Italic.ttf',
                        'JetBrainsMono-ExtraBold.ttf'
                    ],
                    'fallbacks': ['JetBrains Mono', 'Consolas', 'Monaco'],
                    'family': 'JetBrains Mono'
                }
            }
        }
        
    def get_font_directory(self) -> str:
        """Get the fonts directory path"""
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.dirname(__file__))
        return os.path.join(base_path, 'assets', 'fonts')
    
    def setup_immediate_fallbacks(self):
        """Setup immediate font fallbacks for instant UI rendering"""
        try:
            font_db = QFontDatabase()
            available_families = font_db.families()
            
            # Setup fallback mappings
            self.fallback_fonts = {
                'ui_primary': self._select_best_fallback(['Inter', 'Arial', 'Helvetica'], available_families),
                'ui_bold': self._select_best_fallback(['Inter Bold', 'Arial Bold', 'Helvetica Bold'], available_families),
                'mono_primary': self._select_best_fallback(['JetBrains Mono', 'Consolas', 'Monaco', 'Courier New'], available_families),
                'mono_bold': self._select_best_fallback(['JetBrains Mono Bold', 'Consolas Bold', 'Monaco Bold'], available_families)
            }
            
            print("🔤 Immediate font fallbacks configured:")
            for purpose, font in self.fallback_fonts.items():
                print(f"   - {purpose}: {font}")
                
            return True
            
        except Exception as e:
            print(f"⚠️ Font fallback setup warning: {e}")
            return False
    
    def _select_best_fallback(self, preferences: List[str], available: List[str]) -> str:
        """Select the best available fallback font"""
        for font in preferences:
            if font in available:
                return font
        return 'System Default'
    
    def start_background_loading(self) -> bool:
        """Start background font loading"""
        if self.loading_started:
            return True
            
        try:
            # Check if we're in a headless environment
            if os.environ.get('QT_QPA_PLATFORM') == 'offscreen':
                print("🔤 Headless environment - using system fonts only")
                self.critical_fonts_loaded = True
                self.critical_fonts_ready.emit()
                return True
            
            font_dir = self.get_font_directory()
            if not os.path.isdir(font_dir):
                print(f"⚠️ Font directory not found: {font_dir}")
                self.critical_fonts_loaded = True
                self.critical_fonts_ready.emit()
                return False
            
            # Prepare font loading lists
            critical_fonts = []
            optional_fonts = []
            
            # Add critical fonts
            for config in self.font_config['critical'].values():
                for font_file in config['files']:
                    font_path = os.path.join(font_dir, font_file)
                    critical_fonts.append((font_path, config['family']))
            
            # Add optional fonts
            for config in self.font_config['optional'].values():
                for font_file in config['files']:
                    font_path = os.path.join(font_dir, font_file)
                    optional_fonts.append((font_path, config['family']))
            
            # Start loading critical fonts first
            if critical_fonts:
                self.critical_worker = FontLoadWorker(critical_fonts)
                self.critical_worker.font_loaded.connect(self._on_critical_font_loaded)
                self.critical_worker.loading_complete.connect(self._on_critical_loading_complete)
                self.critical_worker.start()
                
                # Start optional fonts after a delay
                QTimer.singleShot(100, lambda: self._start_optional_loading(optional_fonts))
            else:
                self.critical_fonts_loaded = True
                self.critical_fonts_ready.emit()
            
            self.loading_started = True
            return True
            
        except Exception as e:
            print(f"❌ Font loading setup failed: {e}")
            self.critical_fonts_loaded = True
            self.critical_fonts_ready.emit()
            return False
    
    def _start_optional_loading(self, optional_fonts: List[tuple]):
        """Start loading optional fonts"""
        if optional_fonts:
            self.optional_worker = FontLoadWorker(optional_fonts)
            self.optional_worker.font_loaded.connect(self._on_optional_font_loaded)
            self.optional_worker.loading_complete.connect(self._on_optional_loading_complete)
            self.optional_worker.start()
    
    def _on_critical_font_loaded(self, font_name: str, success: bool):
        """Handle critical font loaded"""
        if success:
            self.loaded_fonts[font_name] = 'critical'
            print(f"✅ Critical font loaded: {font_name}")
        else:
            print(f"⚠️ Critical font failed: {font_name}")
    
    def _on_critical_loading_complete(self, count: int):
        """Handle critical fonts loading complete"""
        self.critical_fonts_loaded = True
        self.critical_fonts_ready.emit()
        print(f"🎯 Critical fonts loaded: {count}")
    
    def _on_optional_font_loaded(self, font_name: str, success: bool):
        """Handle optional font loaded"""
        if success:
            self.loaded_fonts[font_name] = 'optional'
        # Silent for optional fonts
    
    def _on_optional_loading_complete(self, count: int):
        """Handle optional fonts loading complete"""
        total_loaded = len(self.loaded_fonts)
        self.fonts_ready.emit(total_loaded)
        print(f"🔤 All fonts loaded: {total_loaded} total")
    
    def get_font(self, purpose: str, size: int = 9, bold: bool = False) -> QFont:
        """Get optimized font for specific purpose"""
        if purpose in ['ui', 'interface']:
            family = self.loaded_fonts.get('Inter', self.fallback_fonts.get('ui_primary', 'Arial'))
        elif purpose in ['code', 'mono', 'monospace']:
            family = self.loaded_fonts.get('JetBrains Mono', self.fallback_fonts.get('mono_primary', 'Consolas'))
        else:
            family = self.fallback_fonts.get('ui_primary', 'Arial')
        
        font = QFont(family, size)
        font.setBold(bold)
        return font
    
    def is_ready(self, critical_only: bool = True) -> bool:
        """Check if fonts are ready for use"""
        if critical_only:
            return self.critical_fonts_loaded
        return self.loading_started and len(self.loaded_fonts) > 0


# Global font manager instance
_font_manager = None

def get_font_manager() -> OptimizedFontManager:
    """Get global font manager instance"""
    global _font_manager
    if _font_manager is None:
        _font_manager = OptimizedFontManager()
    return _font_manager


def load_fonts_optimized() -> bool:
    """Optimized font loading entry point"""
    manager = get_font_manager()
    
    # Setup immediate fallbacks first
    manager.setup_immediate_fallbacks()
    
    # Start background loading
    return manager.start_background_loading()


def get_optimized_font(purpose: str = 'ui', size: int = 9, bold: bool = False) -> QFont:
    """Get optimized font for UI"""
    manager = get_font_manager()
    return manager.get_font(purpose, size, bold)


def wait_for_critical_fonts(timeout_ms: int = 2000) -> bool:
    """Wait for critical fonts to load with timeout"""
    manager = get_font_manager()
    
    if manager.is_ready(critical_only=True):
        return True
    
    # Wait with timeout
    start_time = time.time()
    while time.time() - start_time < timeout_ms / 1000:
        QApplication.processEvents()
        if manager.is_ready(critical_only=True):
            return True
        time.sleep(0.01)
    
    return False