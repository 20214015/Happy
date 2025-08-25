"""
Professional Theme - Modern Business Interface
=============================================

A clean, professional theme designed for business applications.
Features modern colors, professional typography, and clean layouts.

Author: GitHub Copilot  
Date: January 2024
Version: 1.0 - Professional Edition
"""

from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
import os

class ProfessionalTheme:
    """Professional theme manager with modern business aesthetics"""
    
    # Professional Color Palette - Modern & Clean
    COLORS = {
        # Background colors - Light and professional
        'bg_primary': '#FFFFFF',        # Pure white primary background
        'bg_secondary': '#F8FAFC',      # Light gray secondary background
        'bg_tertiary': '#F1F5F9',       # Subtle gray tertiary background
        'bg_hover': '#E2E8F0',          # Light hover state
        'bg_selected': '#EBF8FF',       # Light blue selection background
        
        # Text colors - Professional hierarchy
        'text_primary': '#1E293B',      # Dark gray primary text
        'text_secondary': '#475569',    # Medium gray secondary text  
        'text_muted': '#94A3B8',        # Light gray muted text
        'text_white': '#FFFFFF',        # White text for dark backgrounds
        
        # Brand colors - Professional blue palette
        'primary': '#3B82F6',           # Professional blue
        'primary_hover': '#2563EB',     # Darker blue on hover
        'primary_light': '#DBEAFE',     # Light blue tint
        
        # Status colors - Clear and accessible
        'success': '#10B981',           # Professional green
        'success_light': '#D1FAE5',     # Light green background
        'warning': '#F59E0B',           # Professional amber
        'warning_light': '#FEF3C7',     # Light amber background
        'danger': '#EF4444',            # Professional red
        'danger_light': '#FEE2E2',      # Light red background
        'info': '#06B6D4',              # Professional cyan
        'info_light': '#CFFAFE',        # Light cyan background
        
        # Border colors - Subtle and clean
        'border_light': '#E2E8F0',      # Light border
        'border_medium': '#CBD5E1',     # Medium border
        'border_dark': '#94A3B8',       # Dark border
        
        # Interactive colors
        'focus': '#3B82F6',             # Focus outline color
        'disabled': '#9CA3AF',          # Disabled state color
        'shadow': 'rgba(0, 0, 0, 0.1)', # Subtle shadow
    }
    
    @staticmethod
    def get_palette() -> QPalette:
        """Create professional QPalette"""
        palette = QPalette()
        colors = ProfessionalTheme.COLORS
        
        # Basic colors
        palette.setColor(QPalette.ColorRole.Window, QColor(colors['bg_primary']))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(colors['text_primary']))
        palette.setColor(QPalette.ColorRole.Base, QColor(colors['bg_primary']))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors['bg_secondary']))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(colors['bg_tertiary']))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(colors['text_primary']))
        palette.setColor(QPalette.ColorRole.Text, QColor(colors['text_primary']))
        palette.setColor(QPalette.ColorRole.Button, QColor(colors['bg_secondary']))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors['text_primary']))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(colors['primary']))
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(colors['text_muted']))
        
        # Selection colors
        palette.setColor(QPalette.ColorRole.Highlight, QColor(colors['primary']))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(colors['text_white']))
        
        return palette
    
    @staticmethod
    def get_professional_fonts():
        """Get professional font configuration"""
        # Primary UI font - Inter for excellent readability
        ui_font = QFont("Inter", 10)
        ui_font.setStyleHint(QFont.StyleHint.SansSerif)
        
        # Fallbacks if Inter not available
        if not ui_font.exactMatch():
            ui_font = QFont("Segoe UI", 10)
            if not ui_font.exactMatch():
                ui_font = QFont("system-ui", 10)
                if not ui_font.exactMatch():
                    ui_font = QFont("Arial", 10)
        
        # Heading font - Inter Bold for headers
        heading_font = QFont("Inter", 14, QFont.Weight.Bold)
        heading_font.setStyleHint(QFont.StyleHint.SansSerif)
        if not heading_font.exactMatch():
            heading_font = QFont("Segoe UI", 14, QFont.Weight.Bold)
        
        # Monospace font - JetBrains Mono for code/data display
        mono_font = QFont("JetBrains Mono", 9)
        mono_font.setStyleHint(QFont.StyleHint.Monospace)
        if not mono_font.exactMatch():
            mono_font = QFont("Consolas", 9)
            if not mono_font.exactMatch():
                mono_font = QFont("Monaco", 9)
                if not mono_font.exactMatch():
                    mono_font = QFont("monospace", 9)
        
        # Small font for secondary text
        small_font = QFont("Inter", 8)
        small_font.setStyleHint(QFont.StyleHint.SansSerif)
        if not small_font.exactMatch():
            small_font = QFont("Segoe UI", 8)
        
        return {
            'ui': ui_font,
            'heading': heading_font,
            'monospace': mono_font,
            'small': small_font
        }
    
    @staticmethod
    def get_professional_stylesheet():
        """Get complete professional stylesheet"""
        colors = ProfessionalTheme.COLORS
        
        return f"""
        /* ===================================
           PROFESSIONAL THEME - MODERN DESIGN
           ================================== */
        
        /* MAIN APPLICATION */
        QMainWindow {{
            background-color: {colors['bg_primary']};
            color: {colors['text_primary']};
            font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
        }}
        
        /* GENERAL WIDGETS */
        QWidget {{
            background-color: {colors['bg_primary']};
            color: {colors['text_primary']};
            selection-background-color: {colors['primary']};
            selection-color: {colors['text_white']};
        }}
        
        /* LABELS */
        QLabel {{
            color: {colors['text_primary']};
            background-color: transparent;
        }}
        
        QLabel[styleClass="heading"] {{
            font-size: 16px;
            font-weight: bold;
            color: {colors['text_primary']};
            padding: 8px 0;
        }}
        
        QLabel[styleClass="subheading"] {{
            font-size: 12px;
            font-weight: 600;
            color: {colors['text_secondary']};
            padding: 4px 0;
        }}
        
        QLabel[styleClass="muted"] {{
            color: {colors['text_muted']};
            font-size: 10px;
        }}
        
        /* BUTTONS - MODERN DESIGN */
        QPushButton {{
            background-color: {colors['primary']};
            color: {colors['text_white']};
            border: none;
            border-radius: 8px;
            padding: 10px 16px;
            font-weight: 500;
            font-size: 11px;
            min-height: 20px;
        }}
        
        QPushButton:hover {{
            background-color: {colors['primary_hover']};
        }}
        
        QPushButton:pressed {{
            background-color: #1D4ED8;
        }}
        
        QPushButton:disabled {{
            background-color: {colors['disabled']};
            color: {colors['text_muted']};
        }}
        
        /* BUTTON VARIANTS */
        QPushButton[variant="secondary"] {{
            background-color: {colors['bg_secondary']};
            color: {colors['text_primary']};
            border: 1px solid {colors['border_medium']};
        }}
        
        QPushButton[variant="secondary"]:hover {{
            background-color: {colors['bg_hover']};
            border-color: {colors['border_dark']};
        }}
        
        QPushButton[variant="success"] {{
            background-color: {colors['success']};
        }}
        
        QPushButton[variant="success"]:hover {{
            background-color: #059669;
        }}
        
        QPushButton[variant="warning"] {{
            background-color: {colors['warning']};
        }}
        
        QPushButton[variant="warning"]:hover {{
            background-color: #D97706;
        }}
        
        QPushButton[variant="danger"] {{
            background-color: {colors['danger']};
        }}
        
        QPushButton[variant="danger"]:hover {{
            background-color: #DC2626;
        }}
        
        /* INPUT FIELDS */
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: {colors['bg_primary']};
            border: 1px solid {colors['border_light']};
            border-radius: 6px;
            padding: 8px 12px;
            color: {colors['text_primary']};
            font-size: 11px;
        }}
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {colors['focus']};
            outline: none;
        }}
        
        QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled {{
            background-color: {colors['bg_secondary']};
            color: {colors['text_muted']};
            border-color: {colors['border_light']};
        }}
        
        /* COMBO BOXES */
        QComboBox {{
            background-color: {colors['bg_primary']};
            border: 1px solid {colors['border_light']};
            border-radius: 6px;
            padding: 8px 12px;
            color: {colors['text_primary']};
            font-size: 11px;
            min-width: 120px;
        }}
        
        QComboBox:hover {{
            border-color: {colors['border_medium']};
        }}
        
        QComboBox:focus {{
            border-color: {colors['focus']};
        }}
        
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border: none;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border: none;
            width: 0;
            height: 0;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 4px solid {colors['text_secondary']};
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {colors['bg_primary']};
            border: 1px solid {colors['border_medium']};
            border-radius: 6px;
            selection-background-color: {colors['bg_selected']};
            selection-color: {colors['text_primary']};
        }}
        
        /* TABLES */
        QTableWidget, QTableView {{
            background-color: {colors['bg_primary']};
            border: 1px solid {colors['border_light']};
            border-radius: 8px;
            gridline-color: {colors['border_light']};
            selection-background-color: {colors['bg_selected']};
            selection-color: {colors['text_primary']};
        }}
        
        QHeaderView::section {{
            background-color: {colors['bg_secondary']};
            color: {colors['text_secondary']};
            padding: 12px 8px;
            border: none;
            border-bottom: 1px solid {colors['border_light']};
            font-weight: 600;
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        QTableWidget::item, QTableView::item {{
            padding: 12px 8px;
            border-bottom: 1px solid {colors['border_light']};
        }}
        
        QTableWidget::item:selected, QTableView::item:selected {{
            background-color: {colors['bg_selected']};
            color: {colors['text_primary']};
        }}
        
        /* PROGRESS BARS */
        QProgressBar {{
            background-color: {colors['bg_secondary']};
            border: none;
            border-radius: 6px;
            text-align: center;
            font-size: 10px;
            font-weight: 500;
            color: {colors['text_secondary']};
            height: 8px;
        }}
        
        QProgressBar::chunk {{
            background-color: {colors['primary']};
            border-radius: 6px;
        }}
        
        /* GROUP BOXES */
        QGroupBox {{
            font-weight: 600;
            font-size: 12px;
            color: {colors['text_primary']};
            border: 1px solid {colors['border_light']};
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 16px;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 8px;
            background-color: {colors['bg_primary']};
        }}
        
        /* TABS */
        QTabWidget::pane {{
            border: 1px solid {colors['border_light']};
            border-radius: 8px;
            background-color: {colors['bg_primary']};
        }}
        
        QTabBar::tab {{
            background-color: {colors['bg_secondary']};
            color: {colors['text_secondary']};
            border: 1px solid {colors['border_light']};
            border-bottom: none;
            border-radius: 8px 8px 0 0;
            padding: 12px 16px;
            margin-right: 2px;
            font-weight: 500;
        }}
        
        QTabBar::tab:selected {{
            background-color: {colors['bg_primary']};
            color: {colors['text_primary']};
            border-color: {colors['border_light']};
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: {colors['bg_hover']};
        }}
        
        /* SCROLLBARS */
        QScrollBar:vertical {{
            background-color: {colors['bg_secondary']};
            width: 8px;
            border-radius: 4px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {colors['border_medium']};
            border-radius: 4px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {colors['border_dark']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
            height: 0;
        }}
        
        QScrollBar:horizontal {{
            background-color: {colors['bg_secondary']};
            height: 8px;
            border-radius: 4px;
            margin: 0;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {colors['border_medium']};
            border-radius: 4px;
            min-width: 20px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {colors['border_dark']};
        }}
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            border: none;
            background: none;
            width: 0;
        }}
        
        /* STATUS BAR */
        QStatusBar {{
            background-color: {colors['bg_secondary']};
            border-top: 1px solid {colors['border_light']};
            color: {colors['text_secondary']};
            font-size: 10px;
        }}
        
        /* MENU BAR */
        QMenuBar {{
            background-color: {colors['bg_primary']};
            border-bottom: 1px solid {colors['border_light']};
            color: {colors['text_primary']};
            font-size: 11px;
        }}
        
        QMenuBar::item {{
            background-color: transparent;
            padding: 8px 12px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {colors['bg_hover']};
            border-radius: 4px;
        }}
        
        QMenu {{
            background-color: {colors['bg_primary']};
            border: 1px solid {colors['border_medium']};
            border-radius: 8px;
            padding: 4px;
        }}
        
        QMenu::item {{
            padding: 8px 16px;
            border-radius: 4px;
        }}
        
        QMenu::item:selected {{
            background-color: {colors['bg_selected']};
        }}
        
        /* FRAMES */
        QFrame[frameShape="StyledPanel"] {{
            background-color: {colors['bg_primary']};
            border: 1px solid {colors['border_light']};
            border-radius: 8px;
        }}
        
        /* SPLITTERS */
        QSplitter::handle {{
            background-color: {colors['border_light']};
        }}
        
        QSplitter::handle:horizontal {{
            width: 1px;
        }}
        
        QSplitter::handle:vertical {{
            height: 1px;
        }}
        
        QSplitter::handle:hover {{
            background-color: {colors['primary']};
        }}
        """

def apply_professional_theme(app: QApplication):
    """Apply professional theme to the entire application"""
    # Set palette
    app.setPalette(ProfessionalTheme.get_palette())
    
    # Set stylesheet
    app.setStyleSheet(ProfessionalTheme.get_professional_stylesheet())
    
    # Set fonts
    fonts = ProfessionalTheme.get_professional_fonts()
    app.setFont(fonts['ui'])
    
    print("✅ Professional theme applied successfully!")

# Demo function
if __name__ == "__main__":
    print("Professional Theme - Modern Business Interface")
    print("=" * 50)
    print("🎨 Features:")
    print("   • Clean, professional color palette")
    print("   • Modern typography with Inter font")
    print("   • Accessible design patterns")
    print("   • Business-ready appearance")
    print("")
    print("🎯 Usage:")
    print("   from professional_theme import apply_professional_theme")
    print("   apply_professional_theme(app)")