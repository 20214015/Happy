# theme.py - Professional Theme System
# Updated to use modern professional design

from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication

# Import NEW professional theme
try:
    from professional_theme import ProfessionalTheme, apply_professional_theme
    PROFESSIONAL_THEME_AVAILABLE = True
except ImportError:
    PROFESSIONAL_THEME_AVAILABLE = False

class AppTheme:
    """Legacy theme wrapper - now redirects to professional theme system"""

    @staticmethod
    def get_dark_palette() -> QPalette:
        """Legacy method - redirects to professional palette"""
        if PROFESSIONAL_THEME_AVAILABLE:
            return ProfessionalTheme.get_palette()
        else:
            # Fallback palette
            p = QPalette()
            p.setColor(QPalette.ColorRole.Window, QColor("#FFFFFF"))
            p.setColor(QPalette.ColorRole.WindowText, QColor("#1E293B"))
            return p

    @staticmethod
    def get_light_palette() -> QPalette:
        """Professional light palette"""
        if PROFESSIONAL_THEME_AVAILABLE:
            return ProfessionalTheme.get_palette()
        else:
            # Fallback palette
            p = QPalette()
            p.setColor(QPalette.ColorRole.Window, QColor("#FFFFFF"))
            p.setColor(QPalette.ColorRole.WindowText, QColor("#1E293B"))
            return p

    @staticmethod
    def apply_theme(app: QApplication, settings=None):
        """Legacy theme application method - redirects to professional theme"""
        if PROFESSIONAL_THEME_AVAILABLE:
            print("🔄 Redirecting to professional theme...")
            apply_professional_theme(app)
        else:
            print("⚠️ Professional theme not available, using basic styling")
            app.setPalette(AppTheme.get_light_palette())

# Legacy function for backward compatibility
def apply_theme(app: QApplication, settings=None):
    """Legacy function - redirects to professional theme"""
    AppTheme.apply_theme(app, settings)