"""
Professional Icons - Modern Business Icon System
==============================================

Professional icon management using qtawesome with business-appropriate icons.
Replaces the coding-style Monokai icons with clean, professional variants.

Author: GitHub Copilot
Date: January 2024  
Version: 1.0 - Professional Edition
"""

import qtawesome as qta
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QApplication
from typing import Dict, Optional

# Cache icons to improve performance
_icon_cache: Dict[str, QIcon] = {}

# Professional Color Palette for Icons
PROFESSIONAL_COLORS = {
    "primary": "#3B82F6",      # Professional blue
    "secondary": "#6B7280",    # Professional gray
    "success": "#10B981",      # Professional green
    "warning": "#F59E0B",      # Professional amber
    "danger": "#EF4444",       # Professional red
    "info": "#06B6D4",         # Professional cyan
    "dark": "#1F2937",         # Dark gray
    "light": "#9CA3AF"         # Light gray
}

# Icon color mapping for different action types
PROFESSIONAL_COLOR_MAP = {
    # Primary actions (blue)
    "dashboard": PROFESSIONAL_COLORS["primary"],
    "home": PROFESSIONAL_COLORS["primary"],
    "view": PROFESSIONAL_COLORS["primary"],
    "monitor": PROFESSIONAL_COLORS["primary"],
    
    # Success actions (green)
    "start": PROFESSIONAL_COLORS["success"],
    "play": PROFESSIONAL_COLORS["success"], 
    "run": PROFESSIONAL_COLORS["success"],
    "enable": PROFESSIONAL_COLORS["success"],
    "connect": PROFESSIONAL_COLORS["success"],
    "save": PROFESSIONAL_COLORS["success"],
    "check": PROFESSIONAL_COLORS["success"],
    
    # Warning actions (amber)
    "pause": PROFESSIONAL_COLORS["warning"],
    "warning": PROFESSIONAL_COLORS["warning"],
    "alert": PROFESSIONAL_COLORS["warning"],
    "edit": PROFESSIONAL_COLORS["warning"],
    "config": PROFESSIONAL_COLORS["warning"],
    "settings": PROFESSIONAL_COLORS["warning"],
    
    # Danger actions (red)
    "stop": PROFESSIONAL_COLORS["danger"],
    "delete": PROFESSIONAL_COLORS["danger"],
    "remove": PROFESSIONAL_COLORS["danger"],
    "close": PROFESSIONAL_COLORS["danger"],
    "error": PROFESSIONAL_COLORS["danger"],
    
    # Info actions (cyan)
    "info": PROFESSIONAL_COLORS["info"],
    "help": PROFESSIONAL_COLORS["info"],
    "about": PROFESSIONAL_COLORS["info"],
    "refresh": PROFESSIONAL_COLORS["info"],
    "sync": PROFESSIONAL_COLORS["info"],
    
    # Secondary actions (gray)
    "file": PROFESSIONAL_COLORS["secondary"],
    "folder": PROFESSIONAL_COLORS["secondary"],
    "search": PROFESSIONAL_COLORS["secondary"],
    "filter": PROFESSIONAL_COLORS["secondary"],
    "list": PROFESSIONAL_COLORS["secondary"],
    "menu": PROFESSIONAL_COLORS["secondary"],
}

# Professional icon mapping - Business appropriate icons
PROFESSIONAL_ICON_MAP = {
    # Application & Navigation
    "app_icon": "mdi.monitor",
    "dashboard": "mdi.view-dashboard-outline",
    "home": "mdi.home-outline",
    "menu": "mdi.menu",
    "back": "mdi.arrow-left",
    "forward": "mdi.arrow-right",
    "up": "mdi.arrow-up",
    "down": "mdi.arrow-down",
    
    # Instance Management
    "instances": "mdi.server-outline",
    "add_instance": "mdi.plus-circle-outline",
    "remove_instance": "mdi.minus-circle-outline",
    "clone": "mdi.content-copy",
    "import": "mdi.import",
    "export": "mdi.export",
    
    # Control Actions
    "start": "mdi.play-circle-outline",
    "stop": "mdi.stop-circle-outline", 
    "restart": "mdi.restart",
    "pause": "mdi.pause-circle-outline",
    "resume": "mdi.play-circle-outline",
    
    # Monitoring & Status
    "monitor": "mdi.monitor-eye",
    "status": "mdi.information-outline",
    "performance": "mdi.chart-line",
    "analytics": "mdi.chart-bar",
    "health": "mdi.heart-pulse",
    
    # Configuration & Settings
    "settings": "mdi.cog-outline",
    "config": "mdi.tune",
    "preferences": "mdi.account-settings-outline",
    "options": "mdi.dots-horizontal",
    "properties": "mdi.file-document-edit-outline",
    
    # File Operations
    "file": "mdi.file-outline",
    "folder": "mdi.folder-outline",
    "open": "mdi.folder-open-outline",
    "save": "mdi.content-save-outline",
    "save_as": "mdi.content-save-edit-outline",
    "new": "mdi.file-plus-outline",
    
    # Search & Filter
    "search": "mdi.magnify",
    "filter": "mdi.filter-outline",
    "sort": "mdi.sort",
    "clear": "mdi.close-circle-outline",
    
    # Communication
    "sync": "mdi.sync",
    "refresh": "mdi.refresh",
    "reload": "mdi.reload",
    "update": "mdi.update",
    "download": "mdi.download-outline",
    "upload": "mdi.upload-outline",
    
    # Interface Actions
    "edit": "mdi.pencil-outline",
    "delete": "mdi.delete-outline",
    "copy": "mdi.content-copy",
    "paste": "mdi.content-paste",
    "cut": "mdi.content-cut",
    "undo": "mdi.undo",
    "redo": "mdi.redo",
    
    # Selection
    "select_all": "mdi.select-all",
    "select_none": "mdi.select-off",
    "select_inverse": "mdi.select-inverse",
    "checkbox": "mdi.checkbox-outline",
    "checkbox_checked": "mdi.checkbox-marked-outline",
    
    # Information & Help
    "info": "mdi.information-outline",
    "help": "mdi.help-circle-outline",
    "about": "mdi.information-variant",
    "documentation": "mdi.book-open-outline",
    
    # Alerts & Notifications
    "success": "mdi.check-circle-outline",
    "warning": "mdi.alert-outline",
    "error": "mdi.close-circle-outline",
    "notification": "mdi.bell-outline",
    
    # Automation
    "automation": "mdi.robot-outline",
    "script": "mdi.file-code-outline",
    "schedule": "mdi.calendar-clock",
    "task": "mdi.format-list-checks",
    
    # System
    "system": "mdi.desktop-classic",
    "cpu": "mdi.chip",
    "memory": "mdi.memory",
    "network": "mdi.network-outline",
    "disk": "mdi.harddisk",
    
    # Tools
    "tools": "mdi.tools",
    "debug": "mdi.bug-outline",
    "console": "mdi.console",
    "terminal": "mdi.terminal",
    "log": "mdi.text-box-outline",
    
    # View Controls
    "list_view": "mdi.view-list",
    "grid_view": "mdi.view-grid",
    "table_view": "mdi.table",
    "expand": "mdi.expand-all-outline",
    "collapse": "mdi.collapse-all-outline",
    
    # Window Controls
    "minimize": "mdi.window-minimize",
    "maximize": "mdi.window-maximize",
    "close": "mdi.window-close",
    "fullscreen": "mdi.fullscreen",
    
    # Security
    "lock": "mdi.lock-outline",
    "unlock": "mdi.lock-open-outline",
    "key": "mdi.key-outline",
    "shield": "mdi.shield-outline",
}

def get_professional_icon(name: str, color: str = None) -> QIcon:
    """
    Get a professional icon with appropriate colors.
    
    :param name: Icon name from PROFESSIONAL_ICON_MAP
    :param color: Override color (optional)
    :return: QIcon object
    """
    # Create cache key
    cache_key = f"{name}_{color or 'auto'}"
    
    # Return cached icon if available
    if cache_key in _icon_cache:
        return _icon_cache[cache_key]
    
    # Get icon name from mapping
    icon_name = PROFESSIONAL_ICON_MAP.get(name, "mdi.help-circle-outline")
    
    # Determine color
    final_color = color
    if final_color is None:
        final_color = PROFESSIONAL_COLOR_MAP.get(name, PROFESSIONAL_COLORS["secondary"])
    
    try:
        # Create icon with qtawesome
        icon = qta.icon(icon_name, color=final_color)
        
        # Cache the icon
        _icon_cache[cache_key] = icon
        
        return icon
    except Exception as e:
        print(f"Warning: Failed to create icon '{name}': {e}")
        
        # Return fallback icon
        fallback_icon = qta.icon("mdi.help-circle-outline", color=PROFESSIONAL_COLORS["secondary"])
        _icon_cache[cache_key] = fallback_icon
        return fallback_icon

def get_status_icon(status: str, size: int = 16) -> QIcon:
    """Get colored status icon for instance states"""
    status_mapping = {
        "running": ("mdi.play-circle", PROFESSIONAL_COLORS["success"]),
        "stopped": ("mdi.stop-circle", PROFESSIONAL_COLORS["danger"]),
        "paused": ("mdi.pause-circle", PROFESSIONAL_COLORS["warning"]),
        "starting": ("mdi.loading", PROFESSIONAL_COLORS["info"]),
        "unknown": ("mdi.help-circle", PROFESSIONAL_COLORS["secondary"])
    }
    
    icon_name, color = status_mapping.get(status.lower(), status_mapping["unknown"])
    
    try:
        return qta.icon(icon_name, color=color)
    except Exception:
        return qta.icon("mdi.help-circle", color=PROFESSIONAL_COLORS["secondary"])

def create_button_icon(icon_name: str, variant: str = "primary") -> QIcon:
    """Create icon for button with appropriate variant color"""
    color_map = {
        "primary": PROFESSIONAL_COLORS["primary"],
        "secondary": PROFESSIONAL_COLORS["secondary"], 
        "success": PROFESSIONAL_COLORS["success"],
        "warning": PROFESSIONAL_COLORS["warning"],
        "danger": PROFESSIONAL_COLORS["danger"],
        "info": PROFESSIONAL_COLORS["info"]
    }
    
    color = color_map.get(variant, PROFESSIONAL_COLORS["primary"])
    return get_professional_icon(icon_name, color)

def get_themed_icon(name: str, theme: str = "light") -> QIcon:
    """Get icon appropriate for light/dark theme"""
    if theme == "dark":
        color = PROFESSIONAL_COLORS["light"]
    else:
        color = PROFESSIONAL_COLORS["dark"]
    
    return get_professional_icon(name, color)

def clear_icon_cache():
    """Clear icon cache to free memory"""
    global _icon_cache
    _icon_cache.clear()

# Icon validation
def validate_professional_icons():
    """Validate that all professional icons can be created"""
    print("🔍 Validating Professional Icons...")
    
    failed_icons = []
    total_icons = len(PROFESSIONAL_ICON_MAP)
    
    for name, qtawesome_name in PROFESSIONAL_ICON_MAP.items():
        try:
            icon = qta.icon(qtawesome_name, color=PROFESSIONAL_COLORS["primary"])
            if icon.isNull():
                failed_icons.append(name)
        except Exception as e:
            failed_icons.append(f"{name} ({e})")
    
    if failed_icons:
        print(f"⚠️ {len(failed_icons)} icons failed to load:")
        for icon in failed_icons[:5]:  # Show first 5 failures
            print(f"   • {icon}")
        if len(failed_icons) > 5:
            print(f"   • ... and {len(failed_icons) - 5} more")
    else:
        print(f"✅ All {total_icons} professional icons validated successfully!")
    
    return len(failed_icons) == 0

# Demo function
if __name__ == "__main__":
    print("Professional Icons - Modern Business Icon System")
    print("=" * 50)
    print("🎨 Features:")
    print("   • Business-appropriate icon selection")
    print("   • Professional color palette")
    print("   • Status-aware icon variants")
    print("   • Performance optimization with caching")
    print("")
    print("🎯 Usage:")
    print("   from professional_icons import get_professional_icon")
    print("   icon = get_professional_icon('dashboard')")
    print("")
    
    # Validate icons if qtawesome is available
    try:
        validate_professional_icons()
    except ImportError:
        print("⚠️ qtawesome not available - install for icon validation")