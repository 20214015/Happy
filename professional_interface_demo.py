#!/usr/bin/env python3
"""
Professional Interface Demo
===========================

Demo script to showcase the new professional business interface
that replaces the old coding-style Monokai theme.

Usage: python3 professional_interface_demo.py
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

def main():
    app = QApplication(sys.argv)
    
    print("🚀 Professional Interface Demo")
    print("=" * 50)
    
    # Apply professional theme
    try:
        from professional_theme import apply_professional_theme
        apply_professional_theme(app)
        print("✅ Professional theme applied")
    except Exception as e:
        print(f"⚠️ Theme error: {e}")
    
    # Create demo window
    window = QMainWindow()
    window.setWindowTitle("MuMu Manager Pro - Professional Interface")
    window.resize(1200, 800)
    
    # Create central widget
    central = QWidget()
    window.setCentralWidget(central)
    layout = QVBoxLayout(central)
    
    # Header
    header = QLabel("🏢 Professional Interface Demo")
    header.setProperty("styleClass", "heading")
    header.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(header)
    
    # Description
    desc = QLabel("Modern business-ready interface replacing old coding themes")
    desc.setProperty("styleClass", "subheading") 
    desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(desc)
    
    # Create professional dashboard
    try:
        from professional_dashboard import create_professional_dashboard
        dashboard = create_professional_dashboard(parent=window)
        if dashboard:
            layout.addWidget(dashboard)
            print("✅ Professional dashboard created")
        else:
            raise Exception("Dashboard creation failed")
    except Exception as e:
        print(f"⚠️ Dashboard error: {e}")
        # Fallback content
        fallback = QTextEdit()
        fallback.setPlainText("""
Professional Interface Features:
• Clean, modern business design
• Professional color palette (blue/white)
• Inter font for excellent readability
• Material Design icons
• Responsive layout patterns
• Accessible design principles

Old Features Removed:
• Monokai coding theme (dark terminal style)
• Feather icons system
• Coding-style dashboards
• Terminal color schemes
        """)
        layout.addWidget(fallback)
    
    # Show window
    window.show()
    
    # Auto close after demo
    QTimer.singleShot(30000, app.quit)  # Close after 30 seconds
    
    print("📱 Demo window displayed")
    print("💡 Professional interface features:")
    print("   • Clean white/blue business color scheme")
    print("   • Inter font for professional typography")
    print("   • Material Design icons")
    print("   • Modern responsive layouts")
    print("   • Accessible design patterns")
    print()
    print("🗑️ Removed old components:")
    print("   • Monokai dark coding theme")
    print("   • Terminal-style color schemes")
    print("   • Coding-oriented dashboard designs")
    print("   • Feather icon system")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()